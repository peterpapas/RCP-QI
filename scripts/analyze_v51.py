"""Summarize immutable V5.1 runs without dropping timeouts or partial traversals."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from math import isfinite, log1p
from pathlib import Path
from statistics import median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    radius = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denominator
    return (max(0.0, center - radius), min(1.0, center + radius))


def par2(row: dict) -> float:
    return row["wall_time_s"] if row["completed"] else 2 * row["budget_s"]


def median_field(rows: list[dict], key: str) -> float | None:
    values = [row[key] for row in rows if key in row and row[key] is not None]
    return median(values) if values else None


def analyze(run_dir: Path, output_dir: Path) -> dict:
    config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    if config["stage"] != "heldout":
        raise ValueError("crossover analysis is reserved for the held-out run")
    instances = read_jsonl(run_dir / "instances.jsonl")
    rows = read_jsonl(run_dir / "runs.jsonl")
    index = {case["instance_id"]: case for case in instances}
    by_case: dict[str, dict[str, dict]] = defaultdict(dict)
    for row in rows:
        by_case[row["instance_id"]][row["method"]] = row
    sat_cases = {case_id for case_id, runs in by_case.items() if any(row["status"] == "sat" for row in runs.values())}
    missing = [(case["instance_id"], method) for case in instances for method in case["methods"] if method not in by_case[case["instance_id"]]]
    if missing:
        raise ValueError(f"incomplete run: {len(missing)} method records missing")

    summaries = []
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        case = index[row["instance_id"]]
        if row.get("status") == "sat" and row.get("witness_verified") is not True:
            raise ValueError(f"unverified witness: {row['instance_id']} {row['method']}")
        groups[(case["family"], case["level"], case["nominal_n"], row["method"])].append(row)
    for (family, level, n, method), group in sorted(groups.items()):
        successes = sum(row["completed"] for row in group)
        unique_formulas: dict[str, list[dict]] = defaultdict(list)
        for row in group:
            unique_formulas[index[row["instance_id"]]["sha256_cnf"]].append(row)
        unique_successes = sum(all(row["completed"] for row in repeats) for repeats in unique_formulas.values())
        lo, hi = wilson(unique_successes, len(unique_formulas))
        finished = [row for row in group if row["completed"]]
        solver_stats = [row["solver_stats"] for row in finished if "solver_stats" in row]
        summaries.append({"family": family, "level": level, "nominal_n": n, "method": method, "runs": len(group), "independent_cnf_formulas": len(unique_formulas), "completed": successes, "run_completion_rate": successes / len(group), "completion_rate": unique_successes / len(unique_formulas), "completion_wilson95": [lo, hi], "timeouts": sum(row["status"] == "timeout" for row in group), "memory_limits": sum(row["status"] == "memory_limit" for row in group), "partial": sum(row["status"] == "partial" for row in group), "median_par2_s": median(map(par2, group)), "par2_range_s": [min(map(par2, group)), max(map(par2, group))], "median_algorithm_s_completed": median_field(finished, "elapsed_s"), "median_solver_calls_completed": median_field(finished, "solver_calls"), "median_partition_depth_completed": median_field(finished, "partition_depth"), "median_sampled_peak_rss_mb": median_field(group, "sampled_peak_rss_mb"), "median_scoring_s_completed": median_field(finished, "scoring_s"), "median_decisions_completed": median_field(solver_stats, "decisions"), "median_conflicts_completed": median_field(solver_stats, "conflicts"), "median_propagations_completed": median_field(solver_stats, "propagations"), "median_restarts_completed": median_field(solver_stats, "restarts")})

    comparisons = []
    families = ("all", *sorted({case["family"] for case in instances} - {"public_sat", "public_unsat"}))
    for family in families:
        for method in ("prefix", "occurrence", "connectivity", "propagation", "symmetry", "residual", "jeroslow_wang", "symmetry_break"):
            for baseline in ("prefix", "direct_g4", "direct_cadical"):
                if method == baseline:
                    continue
                pairs = [(index[case_id], runs[method], runs[baseline]) for case_id, runs in by_case.items() if case_id in sat_cases and method in runs and baseline in runs and index[case_id]["family"] not in {"public_sat", "public_unsat"} and (family == "all" or index[case_id]["family"] == family)]
                completed_pairs = [(case, candidate, base) for case, candidate, base in pairs if candidate["completed"] and base["completed"]]
                wins = sum(candidate["elapsed_s"] + 0.005 < base["elapsed_s"] for _, candidate, base in completed_pairs)
                losses = sum(candidate["elapsed_s"] > base["elapsed_s"] + 0.005 for _, candidate, base in completed_pairs)
                ratios = [candidate["elapsed_s"] / base["elapsed_s"] for _, candidate, base in completed_pairs if base["elapsed_s"] > 0]
                comparisons.append({"family": family, "method": method, "baseline": baseline, "paired_instances": len(pairs), "both_completed": len(completed_pairs), "wins_over_5ms": wins, "losses_over_5ms": losses, "ties_within_5ms": len(completed_pairs) - wins - losses, "median_algorithm_time_ratio": median(ratios) if ratios else None, "median_ratio_range": [min(ratios), max(ratios)] if ratios else None, "candidate_only_completed": sum(c["completed"] and not b["completed"] for _, c, b in pairs), "baseline_only_completed": sum(b["completed"] and not c["completed"] for _, c, b in pairs)})

    size_comparisons = []
    for family in sorted({case["family"] for case in instances} - {"public_sat", "public_unsat"}):
        for n in sorted({case["nominal_n"] for case in instances if case["family"] == family}):
            for method in ("occurrence", "connectivity", "propagation", "symmetry", "residual", "jeroslow_wang", "symmetry_break", "prefix"):
                for baseline in ("prefix", "direct_g4", "direct_cadical"):
                    if method == baseline:
                        continue
                    pairs = [(case, by_case[case["instance_id"]][method], by_case[case["instance_id"]][baseline]) for case in instances if case["instance_id"] in sat_cases and case["family"] == family and case["nominal_n"] == n and method in by_case[case["instance_id"]] and baseline in by_case[case["instance_id"]]]
                    complete = [(case, a, b) for case, a, b in pairs if a["completed"] and b["completed"]]
                    ratios = [a["elapsed_s"] / b["elapsed_s"] for _, a, b in complete if b["elapsed_s"] > 0]
                    if pairs:
                        size_comparisons.append({"family": family, "nominal_n": n, "method": method, "baseline": baseline, "pairs": len(pairs), "unique_cnf_digests": len({case["sha256_cnf"] for case, _, _ in pairs}), "both_completed": len(complete), "median_ratio": median(ratios) if ratios else None, "wins_over_5ms": sum(a["elapsed_s"] + 0.005 < b["elapsed_s"] for _, a, b in complete), "candidate_only_completed": sum(a["completed"] and not b["completed"] for _, a, b in pairs), "baseline_only_completed": sum(b["completed"] and not a["completed"] for _, a, b in pairs)})

    predictor_screen = []
    for family in ("random_3sat", "planted_3sat", "coloring", "xor", "two_sat", "symmetry"):
        for method in ("occurrence", "connectivity", "propagation", "symmetry", "residual", "jeroslow_wang", "symmetry_break"):
            seen = set()
            data = []
            for case in instances:
                if case["family"] != family or case["sha256_cnf"] in seen:
                    continue
                seen.add(case["sha256_cnf"])
                runs = by_case[case["instance_id"]]
                if method not in runs or "prefix" not in runs or runs[method]["status"] != "sat" or runs["prefix"]["status"] != "sat" or runs["prefix"]["elapsed_s"] <= 0:
                    continue
                cadical = runs.get("direct_cadical", {})
                conflicts = cadical.get("solver_stats", {}).get("conflicts")
                data.append((case, runs[method]["elapsed_s"] / runs["prefix"]["elapsed_s"], conflicts))
            if len(data) < 6:
                continue
            features = {"nominal_n": [case["nominal_n"] for case, _, _ in data], "clause_density": [case["clauses"] / case["actual_n"] for case, _, _ in data], "mean_clause_length": [case["literal_count"] / case["clauses"] for case, _, _ in data]}
            if all(conflicts is not None for _, _, conflicts in data):
                features["log1p_cadical_conflicts"] = [log1p(conflicts) for _, _, conflicts in data]
            for name, values in features.items():
                if len(set(values)) < 2:
                    continue
                rho = float(spearmanr(values, [ratio for _, ratio, _ in data]).statistic)
                predictor_screen.append({"family": family, "method": method, "feature": name, "independent_formulas": len(data), "spearman_rho_of_time_ratio": rho if isfinite(rho) else None})

    output_dir.mkdir(parents=True, exist_ok=True)
    report = {"source": str(run_dir), "config": config, "instance_count": len(instances), "method_runs": len(rows), "status_counts": {status: sum(row["status"] == status for row in rows) for status in sorted({row["status"] for row in rows})}, "summary": summaries, "paired_comparisons": comparisons, "size_comparisons": size_comparisons, "exploratory_predictor_screen": predictor_screen, "timing_note": "PAR2 uses post-setup method wall time and 2x timeout for incomplete methods. Adaptive-versus-prefix and crossover comparisons use SAT instances only: on UNSAT the root call ends traversal before any variable choice. Algorithm ratios exclude process startup and include scoring, construction, solving, verification. End-to-end estimate adds worker setup to each method. Five-millisecond tolerance avoids classifying timer noise as wins. With two held-out seeds, Wilson intervals remain wide. Spearman screens are descriptive and confounded by size/family; duplicated deterministic formulas are deduplicated in that screen.", "unsat_note": "Generator-known contradictions and dedicated XOR/2-SAT algorithms provide independent checks for selected families; public UNSAT has no independently checked proof certificate."}
    (output_dir / "v5_1_analysis.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    _plot(summaries, output_dir)
    return report


def _plot(summaries: list[dict], output_dir: Path) -> None:
    families = ("random_3sat", "planted_3sat", "coloring", "pigeonhole", "xor", "two_sat", "symmetry")
    methods = ("direct_g4", "direct_cadical", "prefix", "occurrence", "propagation", "xor_gauss", "two_sat_scc", "symmetry_break")
    fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharex=False)
    for ax, family in zip(axes.flat, families, strict=False):
        entries = [row for row in summaries if row["family"] == family and row["level"] in {"4.25", "unique", "sparse", "base"}]
        for method in methods:
            points = sorted((row for row in entries if row["method"] == method), key=lambda row: row["nominal_n"])
            if points:
                ax.plot([row["nominal_n"] for row in points], [row["median_par2_s"] for row in points], marker="o", linewidth=1.4, label=method)
        ax.set(title=family, xlabel="nominal variables", ylabel="median PAR2 seconds", xscale="log", yscale="log")
        ax.grid(alpha=0.2)
    axes.flat[-1].axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower right", bbox_to_anchor=(0.98, 0.06), ncol=2, fontsize=8)
    fig.suptitle("V5.1 held-out scaling: incomplete runs charged 2× time limit")
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    fig.savefig(output_dir / "v5_1_scaling_par2.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharex=False)
    for ax, family in zip(axes.flat, families, strict=False):
        entries = [row for row in summaries if row["family"] == family and row["level"] in {"4.25", "unique", "sparse", "base"}]
        for method in methods:
            points = sorted((row for row in entries if row["method"] == method), key=lambda row: row["nominal_n"])
            if points:
                ax.plot([row["nominal_n"] for row in points], [row["completion_rate"] for row in points], marker="o", linewidth=1.4, label=method)
        ax.set(title=family, xlabel="nominal variables", ylabel="completion fraction", xscale="log", ylim=(-0.05, 1.05))
        ax.grid(alpha=0.2)
    axes.flat[-1].axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower right", bbox_to_anchor=(0.98, 0.06), ncol=2, fontsize=8)
    fig.suptitle("V5.1 held-out completion under matched per-method budgets")
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    fig.savefig(output_dir / "v5_1_completion.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharex=False)
    for ax, family in zip(axes.flat, families, strict=False):
        entries = [row for row in summaries if row["family"] == family and row["level"] in {"4.25", "unique", "sparse", "base"}]
        for method in methods:
            points = sorted((row for row in entries if row["method"] == method and row["median_sampled_peak_rss_mb"] is not None), key=lambda row: row["nominal_n"])
            if points:
                ax.plot([row["nominal_n"] for row in points], [row["median_sampled_peak_rss_mb"] for row in points], marker="o", linewidth=1.4, label=method)
        ax.set(title=family, xlabel="nominal variables", ylabel="median sampled RSS (MiB)", xscale="log")
        ax.grid(alpha=0.2)
    axes.flat[-1].axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower right", bbox_to_anchor=(0.98, 0.06), ncol=2, fontsize=8)
    fig.suptitle("V5.1 held-out peak sampled worker memory (10 ms polling)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.96))
    fig.savefig(output_dir / "v5_1_memory.png", dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = analyze(args.run_dir, args.output_dir)
    print(f"Analyzed {report['instance_count']} instances and {report['method_runs']} methods: {report['status_counts']}")


if __name__ == "__main__":
    main()
