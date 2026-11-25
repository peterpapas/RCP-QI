# Conditional correctness

If the current partition contains a solution, its children cover it, and an existence oracle correctly reports whether the left child contains a solution, then selecting left on `true` and right on `false` preserves at least one solution. Repeating this for (n) balanced bit-prefix decisions reaches a leaf. A final verifier call checks the leaf candidate.

Lean proves the one-step preservation theorem and a bitstring result theorem conditional on a reliable oracle at every true-path prefix. The code's finite-shot oracle is probabilistic, so the theorem's reliability assumption does **not** automatically hold for Python runs.

For the unique-solution measured baseline, a false negative on a left child can discard the solution. A verified candidate cannot create a false positive in an empty child. The adaptive benchmark sets each left-present miss probability to at most ((1-c)/n) for target per-run confidence (c), so a union bound gives at least (c) ideal run success under the unique-solution promise. The bound ignores hardware noise and does not transfer to zero/multiple-solution instances. Failed leaves trigger bounded restarts; all unsuccessful runs remain in resource totals.

No-candidate-after-budget is not an UNSAT proof. DPLL and exhaustive search can prove UNSAT after complete exploration; the bounded quantum schedule cannot.
