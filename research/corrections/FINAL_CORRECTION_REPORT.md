# Post-publication scientific correction report

**Status:** maintenance of the suspended V1–V10 programme; no V11, new speculative operator or general quantum SAT claim. [Reviewer adjudication](REVIEWER_ADJUDICATION.md) gives the individual dispositions.

## Corrected scientific record

The central correction is that V3 reflected on the partition-label **qubit** only. [Grover–Radhakrishnan partial search](PARTIAL_SEARCH_PRIOR_ART.md) instead uses the oracle with global diffusion, intra-block diffusion on all within-block address qubits, and a final global step. It was established prior art, omitted from V3. At `N=256`, an independently enumerated one-shot sequence reaches 90/95/99% half accuracy in 7/8/9 queries, versus 9/10/11 for standard full-space Grover followed by half measurement. [Full numerical results and cost model](PARTIAL_SEARCH_RESULTS.md) preserve the `Θ(√N)` black-box scaling and do not imply a new RCP-QI advantage.

The [SAT and complexity review](SAT_AND_COMPLEXITY_PRIOR_ART.md) integrates the Valiant–Vazirani randomized uniqueness reduction, Ambainis's structured quantum 3-SAT baseline, quantum backtracking, QSETH formulations, black-box versus explicit-input limits, SAT backdoors, and the distinct costs of independent sampling, amplitude estimation and coherent search. The [reading guide](FUTURE_READING_GUIDE.md) treats DQI, Yamakawa–Zhandry and planted kXOR as distinct promised tasks. The concise [README](../../README.md) and corrected V2/V3 and negative-result notes direct readers to the new evidence.

## Evidence and audit

The new `POSTPUB-PARTIAL-SEARCH-20261127` entry in the [registry](../experiment_registry.md) is separate from V1–V10. Its [artifacts](../../results/corrections/partial_search_20261127/) have a dedicated SHA-256 manifest; historical `results/manifest.json` and raw V1–V10 results were not rewritten. The finite-size analytic recurrence agrees with 60 ideal statevector runs to at most `2.8×10⁻¹⁴`. Five target addresses per size check target independence. Compilation counts are `u,cx` basis counts for an equality oracle; they are not fault-tolerant hardware costs or an explicit SAT oracle estimate. No shot-based empirical success-rate claim is made.

Validation record and exact commands belong in the [correction reproducibility note](CORRECTION_REPRODUCIBILITY.md). Lean source and historical theorem statements were left unchanged; the [formal-status index](../../theory/formal_status.md) identifies what Lean does and does not establish.

## Open limitations

The finite-size query minima apply to the enumerated nonnegative global/local/final-global family and one-shot threshold protocol. They do not establish arbitrary-algorithm optimality or a recursive speedup. The focused literature pass does not certify the present best quantum 3-SAT time exponent, nor independently adjudicate the 2026 VP–VNP mathematical claims. No proof of P versus NP, novel quantum advantage, universal quantum SAT impossibility or publishable original theorem follows. Active research remains suspended pending the [restart gate](../archive/RCPQI_RESTART_PROTOCOL.md).
