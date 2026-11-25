# V2 — multi-iteration and partition-local amplification

Run `uv run rcp-qi-phase2 --min-n 2 --max-n 8 --seed 20261125 --shots 256 --sample-seeds 2` for the standard Grover sweep and threshold costs. Run `uv run rcp-qi-register --min-n 2 --max-n 6` for the partition-bit-only diffuser control. Correct-half probability follows the exact-solution probability; the local diffuser showed no improvement. Raw outputs and figures are indexed in `results/manifest.json`.
