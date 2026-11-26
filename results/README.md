# Results and provenance

`manifest.json` indexes committed raw outputs and figures by experiment ID. The flat file paths predate the repository restructure and remain canonical so v1 and Phase 2 reproduction commands and notebooks continue to work. Runtime columns are machine-dependent; seeded measurement outcomes and analytical values should be reproducible with `uv.lock`.

Use `uv run python scripts/validate_results.py` to check file presence, schema invariants, oracle accounting, and analytic/statevector agreement. Use `uv run python scripts/build_processed_summary.py` to create `processed/phase2_summary.csv` from committed raw files. Future experiment runners may write into `raw/<experiment-id>/` and figures into `figures/<experiment-id>/`; update the manifest and registry when that happens.

`figures/phase2_recursive_accuracy_v2.png` is a readability revision generated from the **unchanged** committed recursive JSON with `uv run python scripts/plot_recursive_results.py`. The original figure remains indexed for provenance.

`phase2_structural.json` and `phase2_structural.png` are V5 **classical** controls. The JSON retains all 33 cases from three seeds; the figure shows the first seed for legibility. PySAT existence calls and internal solver work are separately recorded. The offline exhaustive audit labels each case and is not included in algorithm times. No quantum circuit or gate count is implied by this artifact.

Do not overwrite a committed raw result to hide a negative outcome. Publish a new experiment version with its own seed and explanation.

V5.1 raw outputs are stored in `raw/v5_1_pilot_20261126/`, `raw/v5_1_heldout_20261126/`, and `raw/v5_1_large_controls_20261126/`. Each has an immutable configuration, CNF digest catalog and one JSONL row per attempted method, including timeouts. `processed/v5_1/` and `processed/v5_1_large_controls/` contain the analysis, three scaling/completion/memory plots each, and independently checked tractable-family UNSAT certificates. See `research/v5_1_findings.md` for interpretation and `experiments/v5_1_extended/README.md` for reproduction and limits. These are classical benchmark times, not quantum query costs or circuit simulations.

V7 is a mathematical and literature investigation with no numerical run. Its manifest entry indexes the theory and axiom-audit artifacts under `theory` rather than inventing a raw experiment file. The conditional proofs and limitations are summarized in `research/v7_mathematical_review.md`.

V7.1 similarly has no raw benchmark or circuit artifact. Its theory-only manifest entry links the structural promise taxonomy, original-source review, Lean local-complementarity/residual/MQ-gadget proofs and axiom audit. See `research/v7_1_structural_promise_discovery.md` for recommendations; historical V1–V7 raw results are unchanged.

## V8 theory-only entry

`V8-ALGEBRAIC-TRANSFER-AUDIT` in `manifest.json` indexes research and Lean artifacts only. No V8 raw data, plots, quantum shots, or new operator were produced; the conditional experiment gate did not pass. See `research/v8/V8_FINAL_REPORT.md`.
