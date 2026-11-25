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
| V1 (`P(correct half)=1/2+4/N-8/N²`) | Conditional machine-verified rational algebra plus analytic/statevector derivation | `one_iteration_half_formula` assumes the one-iteration marked/unmarked probability numerators and balanced-half equation; Grover circuit semantics and Born measurement are not Lean-verified |
| V2 multi-iteration probability relation | Conditional machine-verified rational algebra plus analytic/statevector derivation | `grover_half_relation` assumes normalization and equal unmarked probabilities; it does not apply to arbitrary quantum operators |
| Supplied complementing/preserving transformations | Conditional machine-verified theorems | `complementing_pair`, `complementing_no_fixed_points`, `preserving_pair` assume the transformation law; no discovery/certification complexity is proved |
| Unique solution with a total complementing involution | Conditional machine-verified pair characterization | `unique_complementing_universe_is_pair` shows every assignment equals the named winner or its transform under the explicit uniqueness/involution/flip assumptions; the finite-cardinality corollary is documented analytically |
| Per-decision minimum cost | Conditional machine-verified bound | `totalCost_of_minimum_oracle` proves `n*c ≤ totalCost oracleCost n` if every charged decision costs at least `c`; this is not a lower bound for all SAT or quantum algorithms |
| Root plus one binary query per bit | Machine-verified call count for this self-reduction | `root_plus_recursive_call_count` gives `n+1` existence questions for `n` chosen bits; it does not compare the cost of those calls with a direct model-producing solve |
| Supplied total complementing map yields a witness after one classical verifier value | Conditional machine-verified theorem | `complementing_one_query_witness`; computing/certifying the map and selecting an initial point are assumed |
| Quotient factorization through a supplied section | Conditional machine-verified characterization | `factor_implies_fiber_constant` and `fiber_constant_factors` give the fiber-constancy condition; `quotient_existence_equivalence` preserves the existence answer. No computation-time bound for quotient or representative maps is proved |
| Semantic preservation of a supplied gate-bit flip | Machine-verified Boolean equivalence, external complexity corollary | `gated_flip_preserving_iff_unsat` proves that the flip preserves `F(x,b)=b∧H(x)` exactly when `H` is UNSAT; coNP-hardness follows by the standard CNF UNSAT reduction outside Lean |
| Unique-marker Walsh measurement distribution | Analytic derivation, not Lean formalized | One `H^⊗n U_f H^⊗n` sample has a distribution independent of target position; this does not rule out other coherent procedures |
| Efficient quantum partition-existence oracle | Open problem | No proof or implementation with better complete cost |
| Polynomial-time RCP-QI on NP-complete families | Unproven conjecture | No claim made |
| Lean-to-Python/Qiskit correspondence | Pending | No formal refinement proof |

Run `lake build` and `lake env lean RCPQI/AxiomAudit.lean` in `formal/lean/`. The axiom audit reports no axioms for partition complementarity and only Lean's standard `propext`, `Classical.choice`, and `Quot.sound` for the new probability and structural algebra. No project axioms or unfinished proofs are used.
