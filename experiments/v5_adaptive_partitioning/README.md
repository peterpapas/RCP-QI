# V5: adaptive structural partitioning control

Run `uv run rcp-qi-structural --seed 20261126 --seed-count 3` from the repository root. The runner writes `results/phase2_structural.json` and `results/phase2_structural.png`.

The seven variable selectors are prefix, occurrence, clause connectivity, unit-propagation lookahead, exact variable-swap symmetry scoring, residual clause score, and Jeroslow–Wang. Every existence decision is an incremental **classical PySAT Glucose4** call under the current partial assignment. Direct Glucose4 and the existing DPLL implementation are baselines. Final candidates are checked against the clause verifier; unsatisfiable cases are reported UNSAT by the solver rather than inferred from failed samples. No independently checked UNSAT certificate is produced.

The 33 cases cover three seeds of eleven templates with unique, multiple, and zero outcomes. The [family definitions](../../research/benchmark_families.md), [registry](../../research/experiment_registry.md), and [negative results](../../research/negative_results.md) describe assumptions and limitations. Solver calls, internal work, scoring scans and propagation, construction time, and verification are charged. No quantum operator was introduced; an operator requires the structural certification and matched-cost gate in [structural complementarity](../../theory/structural_complementarity.md).
