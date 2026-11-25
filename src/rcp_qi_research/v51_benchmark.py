"""V5.1 process-isolated, budgeted classical scaling benchmark."""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import platform
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
from time import monotonic, perf_counter, sleep

import psutil

from .structural import STRATEGIES
from .v51_generators import InstanceSpec, default_specs, generate, instance_digest
from .v51_solvers import execute


def method_plan(spec: InstanceSpec) -> tuple[str, ...]:
    if spec.family in {"random_3sat", "planted_3sat"}:
        methods = ["direct_g4", "direct_cadical", *STRATEGIES]
    elif spec.family == "xor":
        methods = ["direct_g4", "direct_cadical", "xor_gauss", "prefix", "occurrence"]
    elif spec.family == "two_sat":
        methods = ["direct_g4", "direct_cadical", "two_sat_scc", "prefix", "occurrence"]
    elif spec.family == "symmetry":
        methods = ["direct_g4", "direct_cadical", "symmetry_break", "prefix", "symmetry", "occurrence"]
    elif spec.family in {"public_sat", "public_unsat"}:
        methods = ["direct_g4", "direct_cadical", "prefix", "occurrence"]
    else:
        methods = ["direct_g4", "direct_cadical", "prefix", "occurrence", "connectivity", "propagation"]
    if spec.nominal_n <= 32 and spec.family not in {"public_sat", "public_unsat"}:
        methods.append("dpll")
    return tuple(methods)


def _worker(spec_data: dict, expected_digest: str, channel) -> None:
    try:
        spec = InstanceSpec(**spec_data)
        before = perf_counter()
        instance = generate(spec)
        generation_s = perf_counter() - before
        digest = instance_digest(instance.problem)
        if digest != expected_digest:
            raise ValueError("instance digest mismatch")
        channel.send({"ok": True, "generation_s": generation_s})
        while True:
            command = channel.recv()
            if command is None:
                break
            method, max_depth = command
            try:
                result = execute(instance, method, max_depth=max_depth)
                channel.send({"ok": True, "result": result})
            except Exception as exc:  # noqa: BLE001 - record per-method failures without losing the run
                channel.send({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
    except Exception as exc:  # noqa: BLE001 - report worker setup failures to the parent
        channel.send({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
    finally:
        channel.close()


def _start_worker(spec: InstanceSpec, digest: str, *, timeout_s: float):
    context = mp.get_context("spawn")
    parent, child = context.Pipe()
    process = context.Process(target=_worker, args=(asdict(spec), digest, child))
    start = monotonic()
    process.start()
    child.close()
    if not parent.poll(max(5.0, 3 * timeout_s)):
        process.terminate()
        process.join()
        parent.close()
        raise TimeoutError(f"worker setup timed out for {spec.id}")
    ready = parent.recv()
    if not ready["ok"]:
        process.join(1)
        parent.close()
        raise RuntimeError(f"worker setup failed: {ready['error']}")
    return process, parent, monotonic() - start, ready["generation_s"]


def _stop_worker(process, channel) -> None:
    if process.is_alive():
        try:
            channel.send(None)
            process.join(0.5)
        except (BrokenPipeError, EOFError):
            pass
    if process.is_alive():
        process.terminate()
        process.join(1.0)
    if process.is_alive():
        process.kill()
        process.join()
    channel.close()


def run_bounded(process, channel, spec: InstanceSpec, method: str, *, timeout_s: float, memory_mb: int, max_depth: int | None, setup_s: float, generation_s: float) -> dict:
    channel.send((method, max_depth))
    start = monotonic()
    monitor = psutil.Process(process.pid)
    peak_rss = 0
    reason = None
    deadline = start + timeout_s
    payload = None
    while process.is_alive():
        try:
            peak_rss = max(peak_rss, monitor.memory_info().rss)
        except psutil.Error:
            pass
        if channel.poll():
            payload = channel.recv()
            break
        if peak_rss > memory_mb * 1024 * 1024:
            reason = "memory_limit"
            break
        if monotonic() >= deadline:
            reason = "timeout"
            break
        sleep(0.01)
    if payload is None and reason is None and channel.poll():
        payload = channel.recv()
    wall = monotonic() - start
    base = {"instance_id": spec.id, "method": method, "budget_s": timeout_s, "memory_budget_mb": memory_mb, "wall_time_s": wall, "setup_s": setup_s, "generation_s": generation_s, "end_to_end_est_s": setup_s + wall, "sampled_peak_rss_mb": peak_rss / 1024**2, "worker_exit_code": process.exitcode if not process.is_alive() else None}
    if reason:
        return {**base, "status": reason, "completed": False}
    if payload is None:
        return {**base, "status": "worker_failure", "completed": False}
    if not payload["ok"]:
        return {**base, "status": "error", "error": payload["error"], "completed": False}
    result = payload["result"]
    return {**base, **result, "completed": result["status"] in {"sat", "unsat"}}


def _case_metadata(spec: InstanceSpec) -> dict:
    before = perf_counter()
    instance = generate(spec)
    return {"instance_id": spec.id, **asdict(spec), "actual_n": instance.problem.n, "clauses": len(instance.problem.clauses), "literal_count": sum(map(len, instance.problem.clauses)), "sha256_cnf": instance_digest(instance.problem), "sha256_source": instance.source_sha256, "generation_s": perf_counter() - before, "methods": method_plan(spec)}


def _specs_for_stage(stage: str, sizes: tuple[int, ...]) -> list[InstanceSpec]:
    seeds = (101,) if stage == "pilot" else (2001, 2002)
    all_specs = default_specs(seeds, sizes)
    if stage == "pilot":
        # Pilot is for feasibility only. It is excluded from confirmatory claims.
        return [s for s in all_specs if s.level in {"4.25", "unique", "base", "sparse", "official"} or s.family == "pigeonhole"]
    # Held-out family/difficulty matrix fixed before looking at pilot outcomes.
    return [s for s in all_specs if s.level in {"3.8", "4.25", "4.6", "unique", "zero", "base", "sparse", "unsat_k4", "official"} or s.family == "pigeonhole"]


def run_benchmark(output_dir: Path, *, stage: str, sizes: tuple[int, ...], timeout_s: float, memory_mb: int, max_cases: int | None = None, families: tuple[str, ...] | None = None) -> dict:
    if stage not in {"pilot", "heldout"} or timeout_s <= 0 or memory_mb < 64:
        raise ValueError("invalid benchmark configuration")
    if output_dir.exists():
        raise FileExistsError(f"immutable run directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    specs = _specs_for_stage(stage, sizes)
    if families is not None:
        specs = [spec for spec in specs if spec.family in families]
    if max_cases is not None:
        specs = specs[:max_cases]
    config = {"schema_version": 1, "stage": stage, "sizes": sizes, "seeds": (101,) if stage == "pilot" else (2001, 2002), "timeout_s": timeout_s, "memory_mb": memory_mb, "max_cases": max_cases, "families": families, "python": platform.python_version(), "python_sat": version("python-sat"), "psutil": version("psutil"), "platform": platform.platform(), "pid": os.getpid(), "process_start_method": "spawn", "public_partition_depth_cap": 16, "method_plan": "fixed by family in v51_benchmark.py; DPLL only nominal_n<=32", "quantum_runs": 0}
    (output_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    raw_path = output_dir / "runs.jsonl"
    catalog_path = output_dir / "instances.jsonl"
    with catalog_path.open("w", encoding="utf-8") as catalog, raw_path.open("w", encoding="utf-8") as raw:
        for index, spec in enumerate(specs):
            meta = _case_metadata(spec)
            catalog.write(json.dumps(meta) + "\n")
            catalog.flush()
            print(f"[{index + 1}/{len(specs)}] {spec.id} n={meta['actual_n']} clauses={meta['clauses']}", flush=True)
            process = None
            for method in meta["methods"]:
                depth_cap = 16 if spec.family in {"public_sat", "public_unsat"} and method in STRATEGIES else None
                if process is None or not process.is_alive():
                    process, channel, setup_s, generation_s = _start_worker(spec, meta["sha256_cnf"], timeout_s=timeout_s)
                result = run_bounded(process, channel, spec, method, timeout_s=timeout_s, memory_mb=memory_mb, max_depth=depth_cap, setup_s=setup_s, generation_s=generation_s)
                raw.write(json.dumps(result) + "\n")
                raw.flush()
                print(f"  {method:17} {result['status']:12} {result['wall_time_s']:.2f}s", flush=True)
                if result["status"] in {"timeout", "memory_limit", "worker_failure"}:
                    _stop_worker(process, channel)
                    process = None
            if process is not None:
                _stop_worker(process, channel)
    return {"config": config, "cases": len(specs), "raw": str(raw_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("pilot", "heldout"), required=True)
    parser.add_argument("--sizes", default="8,16,32,64,128,256,512")
    parser.add_argument("--timeout-s", type=float, default=2.0)
    parser.add_argument("--memory-mb", type=int, default=512)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--families", help="comma-separated family filter for a predeclared control run")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(value) for value in args.sizes.split(","))
    if not sizes or any(n < 3 for n in sizes):
        parser.error("sizes must contain integers >=3")
    families = tuple(args.families.split(",")) if args.families else None
    report = run_benchmark(args.output_dir, stage=args.stage, sizes=sizes, timeout_s=args.timeout_s, memory_mb=args.memory_mb, max_cases=args.max_cases, families=families)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    mp.freeze_support()
    main()
