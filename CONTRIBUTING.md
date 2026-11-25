# Contributing

This is an independent research repository. Contributions should make a falsifiable claim, show their assumptions, and preserve results that disagree with the hypothesis.

1. Open an issue or draft a short hypothesis note in `research/hypotheses/` before adding a new quantum operator. Compare it with the relevant existing algorithm and the unstructured-search lower bound.
2. Add a seeded experiment entry to `research/experiment_registry.md`. Record inputs, analytical expectations, logical oracle calls, physical circuit costs, simulator settings, and limitations.
3. Add meaningful Python tests and, when a mathematical statement is stable, a separate Lean theorem. Do not describe a simulator test as a formal proof.
4. Run the Python and Lean checks described in `AGENTS.md`. Keep routine CI small; expensive sweeps belong in a documented local run.
5. Keep raw results immutable once committed. Put corrected or extended results under a new experiment identifier and explain the change in `CHANGELOG.md`.

No license has been selected. Contribution, reuse, or redistribution terms need author approval before accepting external contributions or public release.
