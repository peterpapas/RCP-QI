# Structured benchmark generators

The current deterministic CNF generators live in `src/rcp_qi_research/structural.py`: XOR-chain SAT, implication-chain 2-SAT, planted and unplanted random 3-SAT, graph three-coloring, and symmetric variable pairs. The runner records seed and parameters in `results/phase2_structural.json`; the mathematical family descriptions are in `research/benchmark_families.md`.

Planted assignments only filter clauses during generation and are never passed to PySAT or a selector. Offline exhaustive counts label tiny instances and are excluded from algorithm timings. Add larger generators here only when they can be reproduced and independently audited.
