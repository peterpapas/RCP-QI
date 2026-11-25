# H001 — constraint-aware partition existence

**Status:** Open research question, not a theorem.

Can internal CNF constraint structure be compiled into a quantum operator that distinguishes a satisfiable bit-prefix partition from an unsatisfiable one at lower complete cost than generic Grover-based testing on a specified family?

The operator must be built from clauses, never from a precomputed satisfying assignment. Its evaluation must include classical preprocessing, state preparation, reversible clause computation/uncomputation, all verifier queries, ancillas, transpiled gates/depth, measurement repetitions, error control, and final candidate verification. Compare against DPLL/modern SAT solvers, full Grover, and the current recursive baseline. Zero- and multiple-solution instances must be included.

**Falsification criteria:** If the operator's required verifier calls or physical gate cost matches or exceeds Grover at equal success, or if classical propagation solves the proposed family cheaply, record a negative result. A free partition-existence oracle does not test H001.
