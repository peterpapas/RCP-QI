# V9 symbolic arithmetic partition model

## Exact generating-polynomial task

Input is an explicit CNF `F` on `n` Boolean witness variables `y₁,…,yₙ`, a consistent partial assignment `p` encoded as a bit mask plus values, and `n` distinct formal weight variables `z₁,…,zₙ`. The input length includes every literal and prefix bit. The field `K` is fixed in advance; for the permanent conditional below assume `char K ≠ 2`. Output is the **formal** polynomial

`P_{F,p}(z) = Σ_{y extends p} [F(y)] ∏_{i=1}^n z_i^{y_i} ∈ K[z₁,…,zₙ]`.

The verifier indicator is the field element `0` or `1`. Distinct assignments have distinct monomials, so `P_{F,p}=0` as a formal polynomial exactly when the partition is empty, in **every** characteristic. Evaluating all `z_i=1` instead returns a count in `K`, which can vanish through characteristic cancellation even with solutions. A fixed prefix changes the restricted polynomial, not the semantic distinction.

The exact arithmetic-DAG model uses binary `+`, `−`, `×` gates, inputs `z_i` and arbitrary field constants, arbitrary fan-out, exact equality in `K[z]`, with size equal to gate count and formal degree at most `n` at the output. Intermediate formal degree is **unrestricted** in this model; any bounded-intermediate-degree version requires a separately stated reduction. A **uniform constructor** must run in polynomial time in CNF length and print its DAG; a nonuniform size claim only says some polynomial DAG exists for each input family. Parsing, preprocessing, reductions, construction, output serialization and (for quantum use) reversible compilation are charged. No partition-existence oracle is granted. Approximate/border circuits are a different output model, not inferred from exact results.

Alternative outputs: (a) an explicit sparse list of nonzero monomial/coefficient pairs; (b) a decision bit `G_{F,p}=1[P_{F,p}≠0]`; (c) a satisfying extension; (d) a count in integers or in `K`. Their complexities must not be interchanged. A quantum phase oracle `U_F` evaluates the Boolean verifier on basis states; it does not output `P_{F,p}`. A black-box query charges one call to `U_F`, while an explicit-CNF gate model additionally charges coherent reversible verifier compilation, state preparation, reflections, measurement and repetition.

## Perfect-matching reduction (analytic proof)

For each `m`, introduce `m²` witness bits `y_{ij}`. Let `F_m` have, for each row and column, one at-least-one clause and all pairwise at-most-one clauses. It has `2m` length-`m` clauses and `2m·C(m,2)` binary clauses, hence polynomial encoding size `O(m³)`. A satisfying assignment is precisely a permutation matrix. Give `y_{ij}` the distinct formal weight `z_{ij}`. Then

`P_{F_m,∅}(z) = Σ_{σ∈S_m} ∏_{i=1}^m z_{i,σ(i)} = perm_m(z)`.

**Proof:** exactly-one row/column constraints give a bijection between satisfying matrices and permutations. Each corresponding assignment contributes exactly its permutation monomial with coefficient `1`. Different permutations contribute different monomials; no cancellation occurs. The clauses and distinct weight names can be listed uniformly with `O(m³)` work, so this is a polynomial-cost mapping from `m` to an explicit CNF and formal output. The root partition is part of the required output domain. It does **not** reduce arbitrary SAT decision to permanent computation.

An explicit sparse monomial list has exactly `m!` entries. Thus any algorithm required to print that representation has unconditional `Ω(m!)` output time and entries, despite polynomial input. This is an output-format bound. A compressed arithmetic DAG could be much smaller; proving it cannot be polynomial requires a separate circuit lower bound. By [Valiant's original algebraic completeness result](https://sites.math.washington.edu/~billey/colombia/references/valiant.completeness.1979.pdf), permanent is VNP-complete under the relevant characteristic assumptions. **Conditional on an accepted `VP ≠ VNP` over the chosen field**, no polynomial-size exact arithmetic DAG family computes all these `P_{F_m,∅}`. The November 2026 [Anthropic claim](https://github.com/anthropics/formal-math/blob/11b6c7e3c927df2658f513b6b68ea7f8929c62c5/vp-vnp/Statement.lean) is not used as an unconditional premise. In characteristic 2, permanent equals determinant, so this route to a hard permanent DAG fails.

In contrast, a prefix fixes some edges present and others absent. Check whether present edges conflict in a row or column; remove their endpoints, remove forbidden edges, then test whether the remaining bipartite graph has a perfect matching. This is polynomial time by [Hopcroft–Karp](https://epubs.siam.org/doi/10.1137/0202019), including witness construction. Therefore the very same family has potentially hard *formal symbolic output* but easy *partition decision*. No quantum advantage or SAT lower bound follows. This is the key counterexample to an unqualified symbolic-to-decision transfer.

## Limits

The equality is exact, field-independent and analytically proved here, but the general quotient-ring theorem, VNP completeness and matching complexity are cited rather than Lean-verified. A polynomial constructor would imply polynomial DAGs; the converse need not yield a uniform constructor. No claim is made about arbitrary CNF SAT, quantum gates, counting hardness, or claimed proof acceptance.
