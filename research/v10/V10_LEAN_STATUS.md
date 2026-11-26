# V10 Lean verification status

The standalone pinned Lean 4.36.0 project adds two modules, without Mathlib or new axioms.

| Lean theorem | Precisely verified scope | Outside Lean |
| --- | --- | --- |
| `checkClauseConflict_correct` | Executable scan of a finite original clause/prefix is equivalent to every literal being explicitly falsified by the prefix. | Certificate discovery and cost of a SAT-oracle verdict. |
| `literal_false_of_prefix`, `clause_false_of_conflict` | A matching total assignment makes the cited literal/clause false. | Resolution proof translation and its size. |
| `conflictTree_sound`, `conflictTree_root_unsat` | A finite tree with both branches at every node and an original-clause conflict at each leaf rules out every total satisfying assignment. | Tree-like resolution proof construction, Haken lower bound, CDCL or quantum behavior. |
| `distributed_units_sat_iff_disjoint` | A witness satisfies Alice's positive and Bob's negative unit requirements exactly when their index sets are disjoint. | Classical/quantum communication lower bounds and an actual network protocol. |

`ConflictTree` is a **restricted classical certificate datatype**. It has no learned-clause, opaque SAT call, error probability, quantum state or coherent oracle constructor. Its root theorem is soundness, not completeness for an efficient search procedure. `DistributedUnits` is a Boolean semantic encoding, not a formalized CNF parser or communication lower bound. Earlier V1–V9 modules and axioms are unchanged.

Reproduce in `formal/lean` with `lake build` and `lake env lean RCPQI/AxiomAudit.lean` using the pinned `lean-toolchain`. The new audit lines print axioms for every new named theorem; use only Lean's standard accepted principles (if any), with no custom axiom, `sorry` or `admit`. The final report records run results.
