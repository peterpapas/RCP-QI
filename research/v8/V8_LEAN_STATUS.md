# V8 Lean status

## Project formalization

`formal/lean/RCPQI/AlgebraicTransfer.lean` adds two elementary theorems about the integer expression `z*z-z`:

- `boolean_relation_vanishes`: evaluation at either Boolean value (`0` or `1`) is zero.
- `boolean_relation_nonzero`: evaluation at `2` is nonzero.

Together they refute the implication from agreement on Boolean inputs to equality of **integer polynomial expressions**. The corresponding formal-polynomial statement over arbitrary fields follows by the nonzero coefficient of `z²`; it is an analytic observation, **not** formalized in this module. These proofs do not assert `VP≠VNP`, any SAT hardness, a quantum query lower bound, or a theorem about arbitrary arithmetic circuits. They require only the project's pinned Lean 4.36.0 and no Mathlib.

Run from `formal/lean`:

```text
lake build
lake env lean RCPQI/AxiomAudit.lean
```

The audit file prints the axioms of both new theorems. Existing V7/V7.1 theorems and their assumptions remain unchanged. The V8 source verification document separately records attempts to build external Anthropic/OpenAI formalizations; success or failure there must never be conflated with this project's narrow Lean results.

**This round's result:** project `lake build` passed (24 jobs) and `lake env lean RCPQI/AxiomAudit.lean` passed; both new theorems report **no axioms**. The initial audit call failed because its import was missing; the import was added and the same audit then passed. Anthropic's external `Statement` target built, but the full external build failed locally with repeated Windows file-read errors, so its proof and axiom audit were **not** independently reproduced here. OpenAI's external build was not reproduced. Exact revisions and commands are in `V8_SOURCE_VERIFICATION.md`.

## Unformalized obligations

1. A polynomial-ring theorem over a chosen field: `x²−x` is nonzero formally but zero on the Boolean cube, with an explicit quotient by the Boolean ideal.
2. A scoped simulation theorem for a specified oracle/partition model, including section and quotient costs, against the standard quantum query bound.
3. Any claimed transfer from a hard arithmetic polynomial family to a symbolic partition operator: explicit projection, circuit simulation, gate convention and field assumptions.

None of these is silently assumed by the new Lean proofs. A future formalization must not import an unreviewed external theorem as an axiom merely to claim a result.
