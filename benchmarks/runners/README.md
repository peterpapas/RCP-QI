# Benchmark runners

The CLI runners are `rcp-qi-research`, `rcp-qi-phase2`, `rcp-qi-register`, `rcp-qi-sat`, and `rcp-qi-recursive`. Their implementations remain in `src/rcp_qi_research` to preserve working entry points. `scripts/validate_results.py` checks committed raw files and cost invariants; `scripts/build_processed_summary.py` builds a Pandas-derived table. Use a new experiment ID and output path for major protocol changes.
