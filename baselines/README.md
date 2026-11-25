# Baselines

Working implementations remain at their stable import paths:

- Classical exhaustive search: `rcp_qi_research.search.classical_exhaustive`.
- Full-space Grover: `rcp_qi_research.search.grover_search`; an unknown-count randomized experimental schedule is in `sat_benchmark.py`.
- Classical unit propagation and DPLL: `rcp_qi_research.sat_benchmark`.

The source is intentionally not duplicated under this directory. Every comparison must report the different cost units separately: complete verification calls, clause-phase calls, literal checks, transpiled gates, depth, shots, and runtime.
