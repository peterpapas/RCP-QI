# Partial quantum search was established prior art

**Correction scope:** The published V2/V3 controls did not benchmark the established partial-search operator. This note supersedes broad readings of [V3's experiment note](../../experiments/v3_partition_register/README.md), [negative-results entry N06](../archive/RCPQI_NEGATIVE_RESULTS.md), and the corresponding sentence in the original [V2 note](../../experiments/v2_amplitude_amplification/README.md). It does not alter historical data or assert a new RCP-QI discovery.

## Tasks and oracle model

Let `N=2^n`, with exactly one marked address `t`, and let a single coherent phase query apply `O_t|x⟩=(-1)^[x=t]|x⟩`. The searcher initially knows `N` and a fixed partition into `K=2^k` equal blocks, but not `t` or its block. **Exact search** returns `t`; **partial search** returns its block (the first `k` address bits); **half search** is `K=2`. Recursive partial search invokes a new block test on the retained subspace until the complete address is obtained. Restricting the original phase oracle to a known block does not supply a free existence oracle: each subproblem query still calls `O_t` and needs block state preparation and reflection.

[Grover and Radhakrishnan, *Is partial quantum search of a database any easier?* (SPAA 2005)](https://arxiv.org/pdf/quant-ph/0407122) gave a partial-search algorithm and a lower bound. For fixed `K` and `N≫K`, their high-success formulation has `q_K(N)=Θ(√N)` and shows a saving of order `√(N/K)` relative to exact Grover search. Their lower-bound theorem assumes certainty or success at least `1−O(N^(-1/4))`; its displayed coefficients imply `q_K(N)≥(π/4)(1−1/K)√N` asymptotically in that regime. This coefficient is **not** a universal bound for a 90%-success finite-size algorithm. Their construction has success `1−O(N^(-1/2))`, with an exact variant at constant extra query cost. [Korepin's optimization](https://arxiv.org/pdf/quant-ph/0503238) and [Korepin–Liao's sequence comparison](https://arxiv.org/pdf/quant-ph/0510179) analyze the established global/local/global family; the latter does not prove optimality among arbitrary quantum algorithms.

## Operator and sequence

Write `|s_N⟩` for the uniform global state and `|s_b⟩` for the uniform state in a block of size `b=N/K`. Up to global phase, `D_N=2|s_N⟩⟨s_N|−I` and `D_b=⊕_blocks(2|s_b⟩⟨s_b|−I)`. A global iteration is `G_N=D_N O_t`; a **local** iteration is `G_b=D_b O_t`. The local reflection acts on all *within-block* address qubits in every block simultaneously. It is neither the V3 `D_partition-bit` nor a free block-existence oracle. Korepin's Eq. (13) applies `G_N^j1`, then `G_b^j2`, then **one final `G_N`**, giving `j1+j2+1` phase queries. All iterations use the same target-independent `O_t`.

For `K=2` and large blocks, Korepin's Eqs. (17)–(20) give `j1=0`, `j2≈(π/4)√(N/2)`, plus the final global step. The leading query coefficient is `π/(4√2)≈0.55536` times `√N`, compared with `π/4≈0.78540` for near-certain full-item Grover search. This is a constant-factor query improvement for a coarser output, **not** a better asymptotic exponent. Integer rounding and thresholds below certainty require finite-`N` analysis; the [new control](PARTIAL_SEARCH_RESULTS.md) enumerates that defined family independently of the hidden target.

## Why recursion cannot beat generic search

If a hypothetical half-label subroutine at size `m` costs `C(m)=α√m+o(√m)` phase queries and can be reused with the same guarantee on each retained half, the idealized sum down a balanced path is

`T(N)=Σ_{i=0}^{n-1} C(N/2^i)≈[α/(1−1/√2)]√N`, up to lower-order and final-verification costs.

For an exact or asymptotically near-certain **full-item** algorithm using this construction, Zalka's [optimal full-search bound](https://doi.org/10.1103/PhysRevA.60.2746) would require `α≥(π/4)(1−1/√2)≈0.23004` under these specific composability and success assumptions. This weak bound is not a bound on one isolated bounded-error half test. The Grover–Radhakrishnan high-success partial-search theorem gives a stronger direct bound in its own regime. A constant per-level error `ε` would accumulate over `log₂N` levels; making total error at most `η` can require stage errors whose sum is at most `η`, repetitions, and final witness verification. If only constant end-to-end success is required, the general [BBBV black-box search lower bound](https://arxiv.org/abs/quant-ph/9701001) still gives `Ω(√N)` queries, without the near-certain `π/4` coefficient. None of these oracle-model statements proves a gate-time lower bound for explicit structured SAT.

Applying the near-certain `K=2` local-search coefficient recursively would have leading sum `[(π/(4√2))/(1−1/√2)]√N≈1.896√N`, worse than direct full Grover's `≈0.785√N`; finite-size error control can only add costs. More generally, a partial result can be cheaper than finding `t` once, but repeated partial decisions do not create a sub-square-root generic full search.

## V3 interpretation

In [the historical source](../../src/rcp_qi_research/partition_register.py), `local_partition_diffuser` calls `_diffuse(circuit, [n - 1])`: it reflects on the **most-significant partition bit only**. The original V3 result `P_half=1/2` is valid for that tested sequence, as are its ancilla controls. It cannot rule out `D_b` acting on bits `0..n-2`. The corrected operator and finite-size results are a separate post-publication control; no V3 raw JSON or plot was rewritten.
