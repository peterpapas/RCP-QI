# Resource accounting contract

Use the `results/manifest.json` experiment ID and the raw result's metadata before comparing numbers. `SearchResult` in `src/rcp_qi_research/search.py` is the current shared runtime record; experiment-specific fields extend it without changing old JSON.

| Field | Meaning | Comparison limit |
| --- | --- | --- |
| `quantum_oracle_calls` | Complete verifier phase-oracle applications executed | Logical query count, not physical gates |
| `clause_phase_calls` | Individual violated-clause phase applications in the V4 control | Different operator; do not equate to full verifier calls |
| `classical_evaluations`, `verification_calls` | Classical predicate evaluations during search and after samples | Separate from phase calls |
| `total_predicate_queries` | Sum of those three complete-predicate call categories | A transparency total, not equal-cost hardware work |
| `circuit_builds`, `circuit_executions` | Templates constructed/transpiled and actual one-shot circuits run | Repeated shots incur repeated state preparation |
| `state_preparations`, `measurements` | Physical-run-equivalent counts | Exact statevector calculations have no physical shots |
| `gate_count_total`, `circuit_depth_total`, `circuit_depth_max` | Basis-`u`/`cx` transpiled operation count and depth over actual runs | Device-independent proxies; routing and fault tolerance omitted |
| `preprocessing.literal_checks` | DPLL/unit-propagation literal inspections | Classical work with a different unit |
| `elapsed_s` | Local construction, transpilation, simulation, and checking wall time | Classical simulator time, not quantum latency |

Analytic threshold tables distinguish `phase_oracle_calls`, `verification_calls`, `shots`, and `total_predicate_calls`. An ancilla or alternative diffuser must report qubits and transpiled costs as well as logical calls. The result validator checks count identities; it cannot prove the counters reflect a future physical implementation.
