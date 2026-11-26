# V10 final report — bounded theorem-development result

## Research outcome

V10 screened seven theorem families and deeply developed **two**: distributed unit-clause SAT as set disjointness (T2), and original-clause-certified binary branch elimination as tree-like resolution with weakening (T3). Both reductions are precise, and their Boolean cores are Lean-verified. Both are direct instances of established results. The review found no efficiently obtainable structural certificate that yields a new Boolean-invariant explicit-SAT lower bound or a justified quantum advantage. No quantum operator or circuit was created.

**T2:** with separately owned clauses, SAT of positive/negative unit clauses is `DISJ_n`; known randomized `Ω(n)` and entanglement-assisted quantum `Ω(√n)` communication bounds transfer to this **distributed** input model. A central solver given the union finds contradictions in linear time, so this is not a centralized SAT lower bound. A public width-one equality CNF has high assignment-split communication rank but trivial SAT existence, further blocking a naive transfer.

**T3:** if every discarded branch ends in a checkable original-clause conflict and the full binary tree is present, its root is unsatisfiable (Lean). Analytically, each leaf can be weakened to the opposite-prefix clause; each internal node resolves its children. A tree of `T` nodes and maximum depth `d` yields a tree-like resolution-with-weakening refutation with `O(Td)` written-literal work. Existing resolution lower bounds then constrain this *restricted certificate architecture*. An opaque quantum partition oracle, CDCL learned clauses or stronger proof system need not produce such a tree and are outside the result. Lean does not yet construct the resolution derivation or verify that size bound.

**Information screen:** exact/approximate degree, adversary, sensitivity, certificates, Fourier and communication ranks are Boolean-function invariants in their fixed models, but an explicit CNF need not reveal their values or useful certificates. A supplied balanced candidate list reduces to ordinary search on its length; a direct partition-existence oracle is a stronger access model whose construction must be charged. Multiple-solution half labels need a new output definition. Two structural controls show the same caution: supplied bounded width gives classical dynamic programming, and a cheap affine certificate can leave arbitrary 3-SAT residual difficulty.

## Decision and stopping gates

| Gate | Finding |
| --- | --- |
| Precise models | Pass for T2 distributed clause ownership and T3 syntactic conflict trees; no transfer to unrestricted RCP-QI is asserted. |
| Proof/certificate validity | Lean verifies Boolean reductions and conflict-tree soundness. Resolution translation and external lower bounds remain analytic/cited. |
| Boolean invariance / efficient acquisition | Measures are invariant as functions under fixed conventions; no broadly useful CNF-efficient certificate was found. |
| Prior art | T2 reduces to known disjointness; T3 to known DPLL/tree-like resolution. Both hit the stated stopping condition. |
| Constructive quantum gate | Fail: no distinct costed mechanism; quantum circuit work remains unauthorised. |
| Publication | No original restricted-model theorem or credible novel paper contribution survives focused review. |

This is a **rigorous negative assessment of investigated directions**, not a universal SAT or quantum impossibility theorem. V1–V9 findings and the conditional status of the 2026 VP–VNP claims remain intact. The V10 theorem/novelty and source notes record assumptions, counterexamples and citations.

## Validation

On 26 November 2026, `uv sync --locked` completed (120 resolved, 117 checked); `uv run ruff check src tests scripts` passed; `uv run pytest -q` passed **65 tests**; `uv run python scripts/validate_results.py` passed the manifest and historical result checks; `lake build` from `formal/lean` completed **34 jobs**; `lake env lean RCPQI/AxiomAudit.lean` passed with no project-defined axioms (the new proofs use at most standard `propext`, `Classical.choice` or `Quot.sound`); and `git diff --check` passed. There are no V10 numerical datasets, random seeds, plots, statevectors or shots.

## Primary recommendation

**D — suspend active RCP-QI development pending a genuinely new mathematical insight.** The candidate directions met their bounded stopping conditions: both substantive simulations are known, and the suspected transfers fail at input ownership, proof-system strength or oracle-access boundaries. Do not continue generic recursion tuning or initiate V11 by default. A restart should require a precise new theorem statement, a source-backed novelty gap, an efficiently obtainable certificate and a model-preserving proof path before any implementation.
