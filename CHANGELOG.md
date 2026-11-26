# Changelog

## V8 — algebraic complexity and transfer audit

- Pinned and inspected the Anthropic and OpenAI November 2026 VP–VNP primary artifacts, distinguishing claimed border bounds from formalized exact statements and independent review status.
- Reconstructed tensor-price/balanced-cut and tensor-wire/replay proof mechanisms, then costed CNF algebraic representations, partition counts and proposed lower-bound/quantum transfers.
- Added a narrow Lean counterexample to Boolean-to-arithmetic identity transfer, an adversarial hypothesis registry and decision D: investigate scoped limitations; no new quantum operator or experiment.

## V7.1 — structural promise discovery

- Added a source-backed taxonomy and comparison of Simon, Shor, HSP/hidden shift, Fourier, quantum walks/backtracking, affine and quadratic Boolean systems, constraint hypergraphs and local complementarity.
- Formalized in Lean that an accessible local complement yields a classical witness, that one flipped constraint can leave arbitrary residual SAT, and that a three-clause quadratic gadget preserves satisfiability locally.
- Recorded certification/oracle construction costs, NP-hardness reduction scope, counterexamples and a limitations/equivalence research path. V8 circuit work remains suspended.

## V7 — transformation characterization

- Revisited complementing/preserving maps, quotient search, hidden shifts, constraint subspaces and Boolean Fourier structure against original literature and V1–V6/V5.1 evidence.
- Added Lean proofs of the one-classical-query complement witness rule, quotient fiber-factorization/existence equivalence, and a Boolean reduction from UNSAT to semantic certification of a supplied symmetry.
- Derived a target-independent one-sample Walsh distribution for unique marked search and documented a costed V8 operator gate. No new quantum circuit was justified.

## V5.1 — extended classical structural benchmarks

- Added reproducible 8–512-variable held-out SAT family benchmarks and 1,024/2,048-variable tractable controls, with direct Glucose4/CaDiCaL, DPLL, seven V5 selectors, symmetry breaking, GF(2), and 2-SAT SCC comparisons.
- Preserved all timeouts, verified SAT witnesses, checked tractable UNSAT contradiction certificates, and recorded full solver/scoring/memory accounting with PAR2 scaling plots.
- Recorded a limited 256-variable random 3-SAT improvement over prefix self-reduction, no observed improvement over direct CDCL, public stress-case limitations, and V7 conditional Lean characterization. No new quantum operator was introduced.

## Phase II — structural complementarity

- Consolidated the V1/V2 probability derivations and added conditional Lean 4 proofs of their rational algebra and transformation-pair properties.
- Expanded the primary-source literature review and documented why complementing maps, symmetries, and partition-existence promises do not by themselves yield a general SAT speedup.
- Added PySAT-backed V5 classical self-reduction controls across seven branching strategies and 33 seeded structured cases, with direct Glucose4 and DPLL baselines. Recorded negative results and full classical scoring/SAT costs; no new quantum operator was introduced.

## Unreleased — research infrastructure

- Added a pinned Lean 4 project with proofs of partition complementarity, solution preservation, conditional recursive correctness, termination/decision count, and bounded partition-cost summation.
- Added experiment registry, theory notes, result manifest/validation, CI, and manuscript scaffold without moving validated results.

## Phase 2 — multi-iteration and controls

- Swept Grover iterations and validated exact-solution and correct-half probabilities against statevectors and seeded shots.
- Measured a partition-local diffuser, an explicit partition ancilla, clause-built SAT oracles, DPLL, unit propagation, and confidence-controlled recursion.
- Retained negative results, inconclusive UNSAT runs, failed shots, restarts, and complete resource costs. Commit `e0754fb`.

## Phase 1 — initial baseline

- Established Python 3.12/uv project with classical, Grover, and measured recursive baselines.
- Validated the one-iteration correct-half formula numerically and added the research handover. Commits `4346513` and `c6d5584`.
