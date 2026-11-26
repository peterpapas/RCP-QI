# Contributing

This is an independent public research archive. The research phase is complete; contributions should offer mathematical review, reproducibility corrections, or a restart proposal that passes the [nine-part gate](research/archive/RCPQI_RESTART_PROTOCOL.md). Active circuit work remains suspended. Contributions should make a falsifiable claim, state assumptions, cite original prior art, compare equally informed classical and quantum baselines, and preserve evidence that disagrees with the hypothesis.

1. Open an issue or draft a short hypothesis note in `research/hypotheses/` for mathematical review. New quantum operators require independent review and passage through the restart gate before implementation. Compare a proposal with the relevant existing algorithms and lower bounds.
2. Add a seeded experiment entry to `research/experiment_registry.md`. Record inputs, analytical expectations, logical oracle calls, physical circuit costs, simulator settings, and limitations.
3. Add meaningful Python tests and, when a mathematical statement is stable, a separate Lean theorem. Do not describe a simulator test as a formal proof.
4. Run the Python and Lean checks described in `AGENTS.md`. Keep routine CI small; expensive sweeps belong in a documented local run.
5. Keep raw results immutable once committed. Put corrected or extended results under a new experiment identifier and explain the change in `CHANGELOG.md`.

Read [LICENSING.md](LICENSING.md) before submitting code, prose, data or images. Do not include third-party benchmark files, private data, credentials, or material you cannot license. Cite sources and specify whether a claim is analytic, Lean-verified, experimental, conditional or conjectural. Review the [negative-results catalogue](NEGATIVE_RESULTS.md) before reopening a historical mechanism.
