# V4 — structured SAT controls

`uv run rcp-qi-sat --seed 20261125 --trials 4 --max-attempts 12` compares reversible clause-built oracles, a randomized unknown-count Grover schedule, unit propagation, DPLL, exhaustive search, and a clause-parity negative control. Five tiny CNFs cover unique, multiple, and zero solutions. A bounded no-candidate quantum result is labeled inconclusive. Harder families and competitive SAT baselines remain open.
