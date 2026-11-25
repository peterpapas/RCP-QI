# V6 — end-to-end recursive benchmark

`uv run rcp-qi-recursive --min-n 2 --max-n 5 --seed 20261125 --trials 3 --max-restarts 2` applies conservative per-level confidence budgets, implicit prefixes, final verification, and bounded restarts. All failed runs and costs remain in the raw result. Offline target audits assess decision errors but never guide the algorithm. The unique-solution promise is required for the stated confidence bound.
