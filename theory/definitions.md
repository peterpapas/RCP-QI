# Definitions and assumptions

An `n`-bit search space is (X_n=\{0,1\}^n), with (N=2^n) candidates. A verifier is (f:X_n\to\{0,1\}). For a bit prefix (p), the implicit partition (S_p) consists of candidates whose first (|p|) bits equal (p). The two children (S_{p0}) and (S_{p1}) are disjoint, exhaustive subsets of (S_p), each of size (2^{n-|p|-1}).

The existence predicate is (G(S)=\bigvee_{x\in S} f(x)). Under the **exactly-one-solution** promise, (G(S_{p0})\oplus G(S_{p1})=1) whenever the current partition contains the unique solution. This logical fact says nothing about the cost of evaluating (G).

The working quantum verifier is a phase oracle (U_f|x\rangle=(-1)^{f(x)}|x\rangle). Equality examples embed a marked target in the circuit and are toy oracles. CNF examples synthesize a reversible phase circuit from clauses; they do not embed a precomputed satisfying assignment.

`formal/lean/RCPQI/Definitions.lean` defines finite candidate types, abstract verifier and partition predicates, existence, cover, disjointness, uniqueness, and logical exclusive-or. The Lean definitions are not yet formally related to the Python dataclasses or Qiskit circuits.
