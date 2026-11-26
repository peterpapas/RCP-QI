# V9 theorem and hypothesis registry

Statuses distinguish local analytic proof, Lean verification, conditional external premise and rejection. “Formal” refers only to the **stated** Lean proposition, not its broader prose interpretation.

| ID | Statement, assumptions and evidence | Complexity scope / prior art | Status |
| --- | --- | --- | --- |
| T1a | `p` and `q` induce the same Boolean table iff `p−q∈⟨x_i²−x_i⟩` over any field; prove via multilinear reduction and cube interpolation | Standard Boolean quotient result; general `n` proof analytic, one-variable identity Lean | Conditionally established (analytic); narrow Lean component formally established |
| T1b | Identical Boolean verifiers have identical literal diagonal phase signs, and conversely | Entrywise Lean proof; uncontrolled channels also identify global sign, which Lean does not model | Formally established for signs |
| T2a | Exactly-one row/column CNF has generating polynomial `perm_m`; its explicit monomial list has `m!` entries | Analytic bijection; unconditional output-size lower bound only | Conditionally established (analytic) |
| T2b | All exact arithmetic-DAG symbolic outputs for this family require superpolynomial size | Follows **only conditional on accepted permanent/VP–VNP circuit lower bound** for `char≠2`; public 2026 claims not independently accepted | Inconclusive as unconditional theorem |
| T2c | Hard full symbolic output forces hard partition existence | Perfect-matching partition decisions are polynomial-time | Refuted |
| T3 | Known `q,r` with fiber constancy give one-for-one oracle-answer simulation; coherent simulation additionally needs reversible maps | Fixed-list transcript Lean theorem; general adaptive/coherent complexity outside Lean; V7 antecedent | Formally established for fixed classical lists |
| T4 | Raw formal degree, monomial count and raw coefficient rank lower-bound all Boolean-equivalent computations | `Q_k=(z²−z)∏(1+a_i b_i)` is Boolean zero with rank `2^k` and `O(k)` DAG | Refuted |
| T5 | Unique-marker balanced-half extraction with standard oracle and bounded error needs `Θ(√N)` quantum queries | Analytic all-ones adversary calculation plus Grover; standard black-box result; no explicit-SAT/gate transfer | Conditionally established on cited adversary theorem; not Lean-verified |
| T6 | A supplied fiber-constant quotient may be cheap to exploit while semantic certification is hard | V7 Lean gate-bit flip iff residual UNSAT; coNP-hardness reduction external; syntactic certificate may be cheap | Conditionally established with explicit promise/certification split |
| C1 | A Boolean-invariant and efficiently certifiable structural measure yields a new quantum-specific SAT speedup | No candidate, costed operator or lower-bound transfer found | Blocked |

No row claims a new general quantum impossibility theorem. T2a is a useful exact-format separation; T5 and T1 are established methods; the strongest remaining opportunity is a precisely delimited restricted-model theorem whose novelty and premise can be independently checked.
