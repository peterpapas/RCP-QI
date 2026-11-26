# Quantum transfer and partition information

For a Boolean verifier `f:X→{0,1}`, the literal phase oracle is `U_f|x⟩=(-1)^{f(x)}|x⟩`. If two arithmetic expressions agree on the Boolean cube, their derived Boolean verifiers and **literal diagonal phase oracles** agree. Conversely, equality of all literal diagonal entries forces pointwise equality of `f` and `g`. Lean proves the entrywise statement in `BooleanOracle.lean`; it does not formalize Hilbert spaces or gates. Complementing every output gives `U_{1-f}=-U_f`: this is the same **uncontrolled unitary channel** up to global phase, but a controlled use can reveal the relative phase. Therefore “physically indistinguishable” must name the access model.

## T5: unique-marker partition label

Let `N=2M` and the input family be all `N` oracles `f_w(x)=[x=w]`, with an unknown unique marked address. The output is `0` if `w` lies in the first `M` addresses and `1` otherwise, with worst-case success at least `2/3`. Each query is the standard coherent membership/phase oracle; interquery unitaries may be arbitrary but independent of `w`. For the nonnegative adversary method, index rows by first-half targets and columns by second-half targets. Set `Γ` to the all-ones `M×M` matrix. Its spectral norm is `M`. For any address query `x`, the matrix of target pairs whose oracle bit differs at `x` has either one full row or one full column; its Hadamard product with `Γ` has norm `√M`. The [adversary lower-bound theorem](https://arxiv.org/abs/quant-ph/0611054) therefore gives `Ω(M/√M)=Ω(√N)` queries, with the usual bounded-error constant. [Grover search](https://arxiv.org/abs/quant-ph/9605043) uses `O(√N)` queries and returns `w`, hence also its half; the black-box partition-label complexity is `Θ(√N)`.

This analytic adversary calculation is **not Lean-verified**. It restates a standard query lower-bound method for this particular output relation, not a new general SAT theorem. Recursively asking half-existence cannot count only `log N` decisions while treating each decision as unit cost. Explicit formula structure, supplied promises or stronger oracles change the model and require a fresh bound. The theorem does not imply `NP⊄BQP`, a quantum gate lower bound, or any explicit-CNF SAT lower bound.

## T3: known quotient

For known maps `q:X→Y` and `r:Y→X`, suppose `f(x)=f(r(q(x)))` for every `x`. Define `g(y)=f(r(y))`. Then `f=g∘q`. Each **classical** query to `g(y)` is one `f(r(y))` query, and each query to `f(x)` is one `g(q(x))` query. Lean proves this equality pointwise over a list of fixed queries in `QuotientQueries.lean`; the same pointwise substitution applies to adaptive transcripts by induction on a deterministic strategy. For coherent use, reversible circuits for `q` and `r` must write and uncompute work registers and can cost more than one logical oracle call. If `r` is expensive or the factorization/certificate must be discovered, these costs may dominate. A quotient can reduce the number of distinct labels, but this is equally available to a classical algorithm given the maps.

## Other obstructions and open space

- Measuring one amplitude with bias `δ` generally requires repetitions scaling with its variance and `δ`; amplitude-estimation variants still charge queries, controlled operations, precision and state preparation. No free exact zero test follows from symbolic notation.
- Postselection on exponentially rare outcomes is not a standard bounded-error algorithm without charging success probability/repetitions.
- A succinct phase verifier may be compiled reversibly with polynomial overhead in CNF size, but an arithmetic lower bound on one formal expression does not constrain every Boolean-equivalent reversible implementation.
- Known [quantum backtracking](https://arxiv.org/abs/1509.02374) is a relevant comparator for structured search; V9 supplies no result separating it from a proposed RCP-QI operator.
