# V10 research brief — bounded theorem screen

**Date:** 26 November 2026. **Scope:** theory, original-source review and narrow Lean verification; no quantum circuit or new experiment. V1–V9 experimental and formal findings remain unchanged, including V9's perfect-matching generating-polynomial/decision separation, Boolean-ideal barrier, and unique-marker half-label `Θ(√N)` **query** bound. The public November 2026 VP–VNP claims remain conditional inputs, never a premise of V10.

## Feasibility screen before development

| Candidate | Feasibility and stopping test | Decision |
| --- | --- | --- |
| T1 supplied structural certificate, partition query | A listed candidate set of size `K` gives ordinary unique-marker search on `K`; existing adversary bound applies. A certificate disclosing the half makes the answer free. | Stop: direct known query result; no new theorem. |
| T2 distributed partition communication | Unit-clause CNF with separately owned clauses is exactly set disjointness. Boolean reduction is short and formalizable; inherited communication bounds have clear scope. | **Select** for one bounded reduction/simulation analysis. |
| T3 conflict-certified branch elimination | A complete binary tree whose leaves cite falsified original clauses translates to tree-like resolution with weakening. A syntactic checker and soundness lemma are formalizable. | **Select** for one bounded simulation analysis. |
| T4 proof lower bound for the same architecture | Follows from T3 plus established resolution lower bounds, only for that restricted tree/certificate model. | Treat as corollary of T3, not a third deep candidate. |
| T5 discovery versus exploitation | V7 semantic-symmetry certification can encode UNSAT; supplied syntactic promises can be cheap. | Already established in narrower form; stop. |
| T6 Boolean-invariant measure gives quantum extraction bound | Requires a specified oracle/promise and efficient certificate; none beyond standard adversary/approximate-degree cases identified. | Stop before speculative transfer. |
| T7 certified structure without quantum advantage | Bounded-width and gated affine controls have strong classical algorithms or arbitrary residual difficulty. | Use as adversarial controls, not a theorem program. |

The two selected candidates have explicit stopping conditions: if each reduces to known disjointness or DPLL/tree-like-resolution results without a model-preserving extension, record it and stop. The [final report](V10_FINAL_REPORT.md) applies this gate. A formal proof of a known elementary reduction is a reproducibility asset, not evidence of mathematical novelty.
