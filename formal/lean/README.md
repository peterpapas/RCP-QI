# Lean 4 verification

This standalone Lake project pins Lean `v4.36.0` in `lean-toolchain`. Its initial proofs need only Lean's bundled library, so no Mathlib dependency is declared or downloaded. If later proofs require Mathlib, add a compatible pinned revision and record that change in `lake-manifest.json`.

Install [Elan](https://lean-lang.org/install/manual/) and run from this directory:

```powershell
lake build
lake env lean RCPQI/AxiomAudit.lean
```

On this Windows workspace, Elan was installed without changing the user PATH, so `lake` is at `~/.elan/bin/lake.exe`. The build and audit succeeded with Lean 4.36.0. The audit reports no axioms for partition complementarity. Other theorems use only Lean's standard `propext`, `Classical.choice`, or `Quot.sound`; there are no new project axioms. See `theory/formal_status.md` for the exact scope and remaining work.

`RCPQI/Probability.lean` also proves the V2 half/solution relation and V1 formula as rational algebra **given** the marked/unmarked probability equations. `RCPQI/Structural.lean` proves pair properties **given** a complementing or preserving transformation. These assumptions are listed in the theorem signatures. The proofs do not show an efficient partition oracle, a way to discover a transformation, or correspondence to the Python/Qiskit circuits.

The V7 addition `unique_complementing_universe_is_pair` characterizes a unique-solution universe with a total complementing involution as the winner and its partner. `totalCost_of_minimum_oracle` gives a conditional lower bound on the *sum of charged decisions*, and `root_plus_recursive_call_count` counts root plus one existence query per bit in this specified self-reduction. None is a generic SAT or quantum lower bound. The [formal status](../../theory/formal_status.md) records the precise assumptions.

Further V7 theorems show that a supplied total complementing map gives a classical witness after one verifier value; a verifier factors through a known quotient with section exactly when it is constant on fibers; and a supplied gate-bit flip preserves `b∧H(x)` exactly when `H` is unsatisfiable. The last theorem supplies the Boolean part of a reduction from CNF UNSAT to **semantic** symmetry certification. Lean does not formalize the standard complexity-class corollary, oracle-query lower bounds or physical gate costs.

V7.1 adds `PartialComplementarity.lean` and `AlgebraicConstraints.lean`: a local complement law plus an accessible point gives a classical witness; flipping one constraint only transfers a **given** residual witness; a fresh affine gate bit leaves arbitrary residual satisfiability unchanged; and a three-literal clause has an equivalent two-equation quadratic gadget. These are conditional or local Boolean theorems. The corresponding NP-hardness claims use standard reductions outside Lean; no quantum circuit is formalized.

V8 adds `AlgebraicTransfer.lean`, proving that the integer expression `z*z-z` vanishes on Boolean values but is nonzero at `z=2`. This is a scoped counterexample to equating Boolean-cube agreement with all-input arithmetic equality; it does not formalize polynomial rings or an arithmetic/quantum circuit lower bound. See `research/v8/V8_LEAN_STATUS.md`.

V9 adds `BooleanIdeal.lean`, `BooleanOracle.lean` and `QuotientQueries.lean` for one-variable interpolation/evaluation, literal phase-sign equivalence, and equality of fixed classical query transcripts through a supplied quotient and representative map. The general Boolean-ideal isomorphism, permanent encoding, matching algorithm and adversary bound are not Lean-verified. See `research/v9/V9_LEAN_STATUS.md`.
