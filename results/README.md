# Results and provenance

`manifest.json` indexes committed raw outputs and figures by experiment ID. The flat file paths predate the repository restructure and remain canonical so v1 and Phase 2 reproduction commands and notebooks continue to work. Runtime columns are machine-dependent; seeded measurement outcomes and analytical values should be reproducible with `uv.lock`.

Use `uv run python scripts/validate_results.py` to check file presence, schema invariants, oracle accounting, and analytic/statevector agreement. Use `uv run python scripts/build_processed_summary.py` to create `processed/phase2_summary.csv` from committed raw files. Future experiment runners may write into `raw/<experiment-id>/` and figures into `figures/<experiment-id>/`; update the manifest and registry when that happens.

`figures/phase2_recursive_accuracy_v2.png` is a readability revision generated from the **unchanged** committed recursive JSON with `uv run python scripts/plot_recursive_results.py`. The original figure remains indexed for provenance.

Do not overwrite a committed raw result to hide a negative outcome. Publish a new experiment version with its own seed and explanation.
