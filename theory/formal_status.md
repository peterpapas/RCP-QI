# Formal verification status

| Claim | Status | Evidence and scope |
| --- | --- | --- |
| Children induced by a total Boolean partition label are disjoint and exhaustive | Machine-verified theorem | `binary_children_cover`, `binary_children_disjoint`; no axioms reported |
| Disjoint/exhaustive halves with a unique solution have complementary existence | Machine-verified theorem | `unique_solution_partition_complementarity`; no axioms reported |
| Correct binary existence choice preserves a solution | Conditional machine-verified theorem | `reliable_selection_preserves_solution`; oracle reliability assumed |
| Structural recursion terminates after `n` bit decisions | Machine-verified theorem | `chooseBits_length`, `recursive_decision_count` |
| Decision count is `log2 N` when `N=2^n` | Machine-verified theorem | `balanced_partition_logarithmic_steps`; counts decisions, not oracle work |
| Full selected bitstring equals target | Conditional machine-verified theorem | `chooseBits_correct_of_reliable_oracle`; reliable oracle along the true path assumed |
| Sum of `n` partition costs is at most `n c` when every cost is at most `c` | Conditional machine-verified theorem | `totalCost_of_bounded_oracle`; does not establish a cheap oracle |
| V1 (P(\text{correct half})=1/2+4/N-8/N^2) | Analytically derived and statevector-supported | `theory/mathematical_foundations.md`, v1/V2 numerical checks; Lean proof pending |
| V2 multi-iteration probability relation | Analytically derived and statevector-supported | Same derivation and Phase 2 results; Lean proof pending |
| Efficient quantum partition-existence oracle | Open problem | No proof or implementation with better complete cost |
| Polynomial-time RCP-QI on NP-complete families | Unproven conjecture | No claim made |
| Lean-to-Python/Qiskit correspondence | Pending | No formal refinement proof |

Run `lake build` and `lake env lean RCPQI/AxiomAudit.lean` in `formal/lean/`. The axiom audit reports no axioms for complementarity and only Lean's standard `propext`, `Classical.choice`, and `Quot.sound` for other selected theorems. No project axioms or unfinished proofs are used.
