# V9 Lean status

The existing standalone Lean 4.36.0 project was preserved. New modules are `RCPQI/BooleanIdeal.lean`, `BooleanOracle.lean` and `QuotientQueries.lean`, imported by `RCPQI.lean` and `AxiomAudit.lean`.

| Proposition actually checked | Scope and omitted claim |
| --- | --- |
| `booleanIdealGenerator_on_bool` | Integer `z*z−z` evaluates to zero at one Boolean point. It is not a multivariable polynomial-ideal isomorphism. |
| `interpolateBool_on_bool` | One-variable interpolation recovers an arbitrary integer-valued Boolean table at `0,1`. |
| `ideal_multiple_same_bool` | Adding any integer-valued multiple of the one-variable relation preserves Boolean evaluation. It does not prove a general ideal-membership converse. |
| `interpolateCube_on_bool` | Recursive Shannon interpolation of any integer-valued table on `n` Boolean coordinates evaluates to that table on every length-`n` Boolean assignment. This does not prove uniqueness of a polynomial normal form or identify the quotient ideal. |
| `phaseEntries_eq_iff` and `phaseSign_complement` | Equality of literal integer phase signs iff Boolean verifiers equal, and complement changes sign. Hilbert-space channels, controlled oracles and physical indistinguishability are not formalised. |
| `quotient_transcript_to_original` and `original_transcript_to_quotient` | One-for-one equality of **fixed classical query-list answers** under a supplied fiber-constancy assumption. Adaptive quantum query simulation, reversible map cost and discovery are not formalised. |

General `n`-variable quotient-ring equivalence, the permanent CNF identity and `m!` output-size argument, the perfect-matching decision algorithm, the adversary spectral-norm calculation, and all cited external complexity theorems remain analytic/cited rather than Lean-verified. This boundary is intentional and visible in the theorem registry.

Reproduce from `formal/lean` with `lake build` and `lake env lean RCPQI/AxiomAudit.lean` (on this host `~/.elan/bin/lake.exe`). Axiom audit reports no **project-defined** axioms; new theorems use at most Lean's standard `propext` or `Quot.sound`, and some use none. No `sorry` or `admit` is in the new proof modules. The full root validation commands and results are recorded in the final report.
