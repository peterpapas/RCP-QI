# RCP-QI surviving mathematical results catalogue

**Archive status:** SUSPENDED — PENDING NEW MATHEMATICAL INSIGHT. This catalogue records the actual V1–V10 statements, not stronger interpretations. In the tables, `L` means a Lean 4 theorem with the identifier shown; `A` means an analytic proof in the cited note; `E` means an external theorem cited but **not Lean-verified here**. Every `RCPQI.*` identifier below is in `formal/lean/RCPQI/<module>.lean`; the pinned build and axiom audit cover the named theorems. Trivial helper lemmas are included because their assumptions matter. No entry proves `P≠NP`, `NP⊄BQP`, a general SAT lower bound or a quantum circuit advantage.

## Partition, recursion and probability

| ID | Precise statement and assumptions / model | Proof location and status | Implication, limit, dependency and novelty |
| --- | --- | --- | --- |
| P01 | Any total Boolean side label covers every candidate by its false/true children. | `Partitioning.lean` L `RCPQI.binary_children_cover` | Set-level fact; no oracle cost. Elementary. |
| P02 | The same children are disjoint. | `Partitioning.lean` L `RCPQI.binary_children_disjoint` | Set-level fact; no success guarantee. Elementary. |
| P03 | Cover plus existence implies a solution in at least one child. | `Complementarity.lean` L `RCPQI.at_least_one_partition` | Requires existing solution. Elementary. |
| P04 | Disjoint children and a unique solution cannot both contain it. | `Complementarity.lean` L `RCPQI.not_both_partitions_of_unique` | Unique-solution promise essential. Elementary. |
| P05 | Cover, disjointness and a unique solution imply exactly one child contains it. | `Complementarity.lean` L `RCPQI.unique_solution_partition_complementarity` | Existence relation, not an efficient test for it. Elementary. |
| P06 | A choice that tests exact left existence preserves a solution. | `Partitioning.lean` L `RCPQI.reliable_selection_preserves_solution` | Ideal *reliable* decision is assumed; no construction/cost. Conditional. |
| P07 | The same reliable selected step contains a solution. | `Correctness.lean` L `RCPQI.recursive_step_correct` | Restatement of P06; conditional. |
| P08 | `chooseBits` appends exactly `n` bits to any prefix, regardless of oracle answers. | `Partitioning.lean` L `RCPQI.chooseBits_length` | Structural termination only. |
| P09 | Starting empty, `chooseBits` makes `n` decisions. | `Correctness.lean` L `RCPQI.recursive_decision_count` | Decision count, not query/gate cost. |
| P10 | If an oracle supplies the correct next bit on every true-path prefix, `chooseBits` returns the target. | `Correctness.lean` L `RCPQI.chooseBits_correct_of_reliable_oracle` | Reliability is an explicit assumption; no efficient oracle. |
| P11 | For `N=2^n`, the selected-bit count equals `log₂ N`. | `Complexity.lean` L `RCPQI.balanced_partition_logarithmic_steps` | Counts decisions only. |
| P12 | If each charged decision costs at most `c`, `totalCost(n)≤nc`. | `Complexity.lean` L `RCPQI.totalCost_of_bounded_oracle` | Conditional on a uniform cost bound. |
| P13 | If each positive-depth charged decision costs at least `c`, `totalCost(n)≥nc`. | `Complexity.lean` L `RCPQI.totalCost_of_minimum_oracle` | Conditional; not a general SAT bound. |
| P14 | This self-reduction asks one root question plus one per bit: `n+1` calls. | `Complexity.lean` L `RCPQI.root_plus_recursive_call_count` | Logical call count; independent of implementation cost. |
| P15 | Under normalization and equal unmarked probabilities, `2(N−1)q=N−2+Np`, relating marked probability `p` and correct-half `q`. | `Probability.lean` L `RCPQI.grover_half_relation`; `theory/mathematical_foundations.md` A | Rational algebra only; Grover state symmetry is assumed. |
| P16 | Given the stated one-iteration marked/unmarked probability numerators, the half-probability numerator identity follows. | `Probability.lean` L `RCPQI.one_iteration_half_numerator` | Amplitude formulas are premises, not Lean circuit semantics. |
| P17 | Under those numerators and `N≠0`, `q=1/2+4/N−8/N²`. | `Probability.lean` L `RCPQI.one_iteration_half_formula`; `results/one_iteration.json` numerical check | Conditional Lean algebra plus statevector validation; bias `O(1/N)`. No speedup. |

## Structural transformations and residual constraints

| ID | Precise statement and assumptions / model | Proof location and status | Implication, limit, dependency and novelty |
| --- | --- | --- | --- |
| S01 | Supplied law `f(Tx)=¬f(x)` makes pair truth values opposite. | `Structural.lean` L `RCPQI.complementing_pair` | Discovery/certification omitted. Elementary. |
| S02 | Such a total flip has no fixed point. | `Structural.lean` L `RCPQI.complementing_no_fixed_points` | Does not make a hard family. Elementary. |
| S03 | Supplied validity-preserving `T` gives equal pair values. | `Structural.lean` L `RCPQI.preserving_pair` | Restates premise; no discovery result. |
| S04 | Under total flip, involution and unique winner, every candidate is winner or its partner. | `Structural.lean` L `RCPQI.unique_complementing_universe_is_pair` | Rules out larger unique-solution universes under *all* assumptions. Elementary scoped counterexample. |
| S05 | With a supplied total flip and accessible `x`, one classical `f(x)` evaluation selects a valid member of `{x,Tx}`. | `Structural.lean` L `RCPQI.complementing_one_query_witness` | Transformation cost/certification charged separately; defeats a quantum-specific witness claim. |
| S06 | If `f=g∘q`, then `f` is constant on fibers of `q`. | `Structural.lean` L `RCPQI.factor_implies_fiber_constant` | Value-level necessity; standard quotient fact. |
| S07 | Given a section `r` and fiber constancy, `f(x)=f(r(qx))`. | `Structural.lean` L `RCPQI.fiber_constant_factors` | Supplied maps and proof assumed; standard. |
| S08 | For supplied `q,r` with section and factorization, original and quotient existence answers coincide. | `Structural.lean` L `RCPQI.quotient_existence_equivalence` | No map-computation or reversible gate bound. |
| S09 | For `F(x,b)=b∧H(x)`, flipping `b` preserves full validity iff `H` is everywhere false. | `Structural.lean` L `RCPQI.gated_flip_preserving_iff_unsat`; `research/v7_mathematical_review.md` A reduction | CNF UNSAT gives coNP-hard **semantic** certification (external SAT complexity); syntactic automorphism differs. |
| S10 | A supplied local flip law on domain `D` and accessible `x∈D` yields a witness after one classical value. | `PartialComplementarity.lean` L `RCPQI.local_complementing_witness` | Domain access and law certification assumed. |
| S11 | If `T` flips a constraint and preserves a residual, a **given residual witness** becomes a full witness. | `PartialComplementarity.lean` L `RCPQI.constraint_complement_residual_witness` | Does not find the residual witness. |
| S12 | `∃(x,b), b∧H(x)` iff `∃x,H(x)`. | `PartialComplementarity.lean` L `RCPQI.gated_residual_existence_equivalence` | Arbitrary SAT difficulty can remain under an easy affine gate; external NP-hardness corollary. |
| S13 | A three-literal Boolean clause is equivalent to its stated two-equation quadratic gadget with an auxiliary bit. | `AlgebraicConstraints.lean` L `RCPQI.clause_quadratic_gadget`; `research/v7_1_structural_promise_discovery.md` | Local truth-table theorem; polynomial reduction to MQ is analytic, not a solver. |
| S14 | A known quotient representative query list has identical original-oracle answers. | `QuotientQueries.lean` L `RCPQI.quotient_transcript_to_original` | Fixed classical list; no adaptive/coherent gate cost. |
| S15 | Under supplied `f(x)=f(r(qx))`, original fixed-list answers equal quotient answers. | `QuotientQueries.lean` L `RCPQI.original_transcript_to_quotient` | One-for-one logical queries; map discovery/compilation unproved. |

## Boolean algebra and oracle equivalence

| ID | Precise statement and assumptions / model | Proof location and status | Implication, limit, dependency and novelty |
| --- | --- | --- | --- |
| B01 | Integer `z²−z` evaluates to zero at Boolean `z`. | `AlgebraicTransfer.lean` L `RCPQI.boolean_relation_vanishes` | Formal-expression/cube-evaluation distinction; no ideal theorem. |
| B02 | That expression is nonzero at `z=2`. | `AlgebraicTransfer.lean` L `RCPQI.boolean_relation_nonzero` | Explicit V8 counterexample; elementary. |
| B03 | The same generator vanishes at every Boolean point. | `BooleanIdeal.lean` L `RCPQI.booleanIdealGenerator_on_bool` | One-variable integer result. |
| B04 | One-variable interpolation `f(0)(1−z)+f(1)z` evaluates to `f(b)` at Boolean `b`. | `BooleanIdeal.lean` L `RCPQI.interpolateBool_on_bool` | Does not prove polynomial uniqueness. |
| B05 | Adding `(z²−z)h(z)` to any integer expression preserves Boolean evaluation. | `BooleanIdeal.lean` L `RCPQI.ideal_multiple_same_bool` | One-direction, one-variable relation only. |
| B06 | Recursive Shannon interpolation of any integer table on an `n`-bit cube evaluates to the table at all length-`n` Boolean assignments. | `BooleanIdeal.lean` L `RCPQI.interpolateCube_on_bool` | Evaluation theorem, not full quotient-ring kernel/complexity. |
| B07 | Literal phase signs coincide iff their Boolean inputs coincide. | `BooleanOracle.lean` L `RCPQI.phaseSign_eq_iff` | Integer signs, not physical channels. |
| B08 | Literal diagonal phase-sign functions coincide iff Boolean verifiers coincide pointwise. | `BooleanOracle.lean` L `RCPQI.phaseEntries_eq_iff` | Does not model global-phase equivalence of uncontrolled channels. |
| B09 | Complementing a bit negates its literal phase sign. | `BooleanOracle.lean` L `RCPQI.phaseSign_complement` | Controlled versus uncontrolled access must be specified. |

## V10 finite certificates and distributed reduction

| ID | Precise statement and assumptions / model | Proof location and status | Implication, limit, dependency and novelty |
| --- | --- | --- | --- |
| C01 | The executable scan `checkClauseConflict(p,c)` is true iff every literal in `c` is explicitly falsified by `p`. | `ConflictTree.lean` L `RCPQI.checkClauseConflict_correct` | Syntactic leaf checker, no discovered certificate. |
| C02 | Any total assignment extending `p` makes a literal with an opposing prefix pair false. | `ConflictTree.lean` L `RCPQI.literal_false_of_prefix` | Local semantic step. |
| C03 | An extension of `p` makes a clause with a checked conflict false. | `ConflictTree.lean` L `RCPQI.clause_false_of_conflict` | Local semantic step. |
| C04 | Every assignment extending a complete binary conflict tree's root fails its CNF. | `ConflictTree.lean` L `RCPQI.conflictTree_sound` | Original-clause leaves and both branches required; no oracle/quantum model. |
| C05 | A conflict tree at empty prefix certifies CNF UNSAT. | `ConflictTree.lean` L `RCPQI.conflictTree_root_unsat` | Soundness only; no size/completeness theorem. |
| C06 | Alice's positive and Bob's negative unit requirements have a witness iff their input sets are disjoint. | `DistributedUnits.lean` L `RCPQI.distributed_units_sat_iff_disjoint` | Boolean reduction; communication bounds externally cited. |

## Analytic reductions, counterexamples and cited lower bounds

| ID | Precise statement, assumptions and model | Proof location / external dependency | Complexity implication, limitation and novelty |
| --- | --- | --- | --- |
| A01 | For unique marker `w`, one `H^n U_f H^n` sample has probability `(1−2/N)²` at zero and `4/N²` at each nonzero frequency, independent of `w`. | `research/v7_mathematical_review.md` A; `tests/mathematical/test_v7_walsh.py` numerical check | Blocks only this single-measurement locator; not Lean or a general Fourier no-go. |
| A02 | A free-dummy quotient `f(x,z)=H(x)` has large validity-preserving orbits while retaining arbitrary residual `H`. | `research/v7_mathematical_review.md` A | Symmetry alone does not simplify SAT; elementary construction. |
| A03 | `F(x,b)=b⊕H(x)` has an easy supplied total complement regardless of `H`. | `research/v7_mathematical_review.md` A | Exact complement can trivialize witness search classically; not a hard SAT advantage. |
| A04 | For any field `K`, cube evaluation identifies `K[x₁,…,xₙ]/⟨x_i²−x_i⟩` with all functions on the Boolean cube; unique multilinear interpolation gives the representative. | `research/v9/V9_BOOLEAN_IDEAL_ANALYSIS.md` A; Lean B03–B06 are narrower | Standard algebra; no cheap canonical-circuit constructor proved. |
| A05 | `Q_k=(z²−z)∏(1+a_i b_i)` is Boolean-zero yet has raw coefficient flattening rank `2^k` and `O(k)` arithmetic DAG. | `research/v9/V9_BOOLEAN_IDEAL_ANALYSIS.md` A | Raw formal degree/rank cannot be Boolean-computation invariants; no general circuit lower bound. |
| A06 | Exactly-one row/column CNF `F_m` has assignment-weight generating polynomial `perm_m(z)` and `m!` distinct expanded terms. | `research/v9/V9_SYMBOLIC_PARTITION_MODEL.md` A; [Valiant 1979](https://sites.math.washington.edu/~billey/colombia/references/valiant.completeness.1979.pdf) E for VNP completeness | Unconditional expanded-output size; compressed-DAG lower bound **conditional** on independently accepted VP≠VNP for `char≠2`. Not Lean. |
| A07 | Every fixed-edge partition existence question for the same `F_m` is bipartite matching. | `research/v9/V9_SYMBOLIC_PARTITION_MODEL.md` A; [Hopcroft–Karp](https://epubs.siam.org/doi/10.1137/0202019) E | Polynomial-time decision despite potentially hard full symbolic output. |
| A08 | With `N=2M` unique-marker phase/membership access, bounded-error correct-half extraction costs `Θ(√N)` queries. | `research/v9/V9_QUANTUM_TRANSFER.md` A adversary matrix; [Høyer–Lee–Špalek](https://arxiv.org/abs/quant-ph/0611054) E; [Grover](https://arxiv.org/abs/quant-ph/9605043) E | Black-box query result; no explicit-CNF quantum gate/SAT lower bound; not Lean. |
| A09 | If exactly `t` marks lie wholly in one half and `t` divides `N/2`, a public equal-block subclass gives `Θ(√(N/t))` queries for the half label. | `research/v10/V10_QUANTUM_INFORMATION_BOUNDS.md` A reduction to A08 | Direct known-search corollary; straddling marks make “correct half” undefined. |
| A10 | Distributed unit-clause SAT is set disjointness; randomized communication `Ω(n)` and entanglement-assisted quantum communication `Ω(√n)`. | Lean C06 for Boolean encoding; [Razborov 1992](https://people.cs.uchicago.edu/~razborov/files/dis.pdf), [Razborov 2003](https://arxiv.org/abs/quant-ph/0204025) E | Distributed clause ownership only; no centralized SAT lower bound. |
| A11 | Public width-one equality CNF has an identity evaluation communication matrix of rank `2^n`, yet is trivially satisfiable. | `research/v10/V10_COMMUNICATION_COMPLEXITY.md` A | High evaluation communication rank need not mean hard existential SAT. |
| A12 | A `T`-node, depth-`d` original-clause conflict tree translates into tree-like resolution with weakening with `O(Td)` written-literal work. | `research/v10/V10_PROOF_COMPLEXITY.md` A; Lean C01–C05 prove only checker/soundness; [DPLL/resolution prior art](https://www.cs.cornell.edu/~sabhar/jobapps/pubs/sabharwal-pub-cl-jair04.pdf) E | [Haken's](https://doi.org/10.1016/0304-3975%2885%2990144-6) resolution bound applies only to this restricted proof system, not opaque quantum or CDCL. |

**External-dependency audit:** BBBV/Grover/adversary, Valiant permanent completeness, Hopcroft–Karp, Razborov communication and Haken resolution are *cited mathematical results*, not imported into or proved by the repository's Lean project. The 2026 Anthropic/OpenAI VP≠VNP artifacts are authentic public claims with unresolved independent acceptance ([V8 audit](../v8/V8_SOURCE_VERIFICATION.md)); they enter A06 only as a labeled conditional premise. The catalogue's Lean IDs are reproduced by `lake build` and `lake env lean RCPQI/AxiomAudit.lean`, not a formal refinement of Python/Qiskit or a formal physical quantum model.
