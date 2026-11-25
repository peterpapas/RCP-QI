# Lean 4 verification

This standalone Lake project pins Lean `v4.36.0` in `lean-toolchain`. Its initial proofs need only Lean's bundled library, so no Mathlib dependency is declared or downloaded. If later proofs require Mathlib, add a compatible pinned revision and record that change in `lake-manifest.json`.

Install [Elan](https://lean-lang.org/install/manual/) and run from this directory:

```powershell
lake build
lake env lean RCPQI/AxiomAudit.lean
```

On this Windows workspace, Elan was installed without changing the user PATH, so `lake` is at `~/.elan/bin/lake.exe`. The build and audit succeeded with Lean 4.36.0. The audit reports no axioms for partition complementarity. Other theorems use only Lean's standard `propext`, `Classical.choice`, or `Quot.sound`; there are no new project axioms. See `theory/formal_status.md` for the exact scope and remaining work.

`RCPQI/Probability.lean` also proves the V2 half/solution relation and V1 formula as rational algebra **given** the marked/unmarked probability equations. `RCPQI/Structural.lean` proves pair properties **given** a complementing or preserving transformation. These assumptions are listed in the theorem signatures. The proofs do not show an efficient partition oracle, a way to discover a transformation, or correspondence to the Python/Qiskit circuits.
