"""Independently check tractable-family UNSAT certificates in a V5.1 run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rcp_qi_research.v51_generators import InstanceSpec, generate, instance_digest
from rcp_qi_research.v51_solvers import two_sat_scc, xor_gauss


def certify(run_dir: Path, output_path: Path) -> list[dict]:
    cases = [json.loads(line) for line in (run_dir / "instances.jsonl").read_text(encoding="utf-8").splitlines() if line]
    rows = []
    for case in cases:
        if case["family"] not in {"xor", "two_sat"} or case["level"] != "zero":
            continue
        spec = InstanceSpec(case["family"], case["nominal_n"], case["seed"], case["level"], case["source"])
        instance = generate(spec)
        if instance_digest(instance.problem) != case["sha256_cnf"]:
            raise ValueError(f"instance checksum mismatch: {case['instance_id']}")
        proof = xor_gauss(instance) if case["family"] == "xor" else two_sat_scc(instance)
        if proof["status"] != "unsat" or proof["unsat_certificate_checked"] is not True:
            raise ValueError(f"certificate failed: {case['instance_id']}")
        rows.append({"instance_id": case["instance_id"], "sha256_cnf": case["sha256_cnf"], "certificate_type": "GF2 contradiction" if case["family"] == "xor" else "opposite implication paths", "certificate_checked": True, "certificate": proof.get("unsat_certificate_equation_indices") if case["family"] == "xor" else proof.get("unsat_certificate_paths")})
    if output_path.exists():
        raise FileExistsError(f"certificate file is immutable: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = certify(args.run_dir, args.output)
    print(f"Checked {len(rows)} independent tractable-family UNSAT certificates")


if __name__ == "__main__":
    main()
