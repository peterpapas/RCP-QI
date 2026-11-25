# Changelog

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
