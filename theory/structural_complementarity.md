# Structural complementarity: precise claims and failure modes

Let `X={0,1}^n`, `f:X→{0,1}`, and `T:X→X`. A property of `T` must be supplied with a proof or derived from the input representation. Its discovery and certification costs are part of an algorithm.

## Complementing map

If `f(T(x))=1-f(x)` for every `x`, each pair `(x,T(x))` has one satisfying element. If `T²=id`, `T` has no fixed points and its orbits are disjoint pairs. This promise **does not** identify the satisfying member; one classical evaluation per pair suffices to identify both values. An arbitrary CNF need not admit a cheaply discoverable complementing map. In fact, such a total map is impossible for a formula with zero satisfying assignments, and also impossible when the satisfying and nonsatisfying assignment counts differ (a bijective involution pairs them). Thus it cannot be assumed for unique-solution SAT when `|X|>2`. The new Lean theorem `unique_complementing_universe_is_pair` proves the conditional pair characterization; [V7](../research/v7_structural_investigation.md) explains its consequence and limits.

For a known bit-flip mask `d`, `T(x)=x⊕d` complements the parity predicate `f(x)=b⊕(a·x mod 2)` exactly when `a·d=1 mod 2`. The vector `a` is obtainable by linear algebra when the affine XOR representation is supplied. This is a tractable-family control and gives no evidence for general 3-SAT.

## Preserving map and symmetry

If `f(T(x))=f(x)`, each orbit is either entirely satisfying or entirely unsatisfying. If `T` is a CNF automorphism, a clause multiset comparison certifies it. In V5, the variable-swap test checks the *entire* signed clause multiset for equality; its clause scans and runtime are charged. Symmetry breaking may reduce equivalent branches, but the reduction is available classically too. Merely selecting an orbit variable first is not a quotient algorithm and should not be credited with symmetry reduction.

## Partition relation

For disjoint exhaustive `A,B`, a **unique** solution gives `G(A) XOR G(B)=1` where `G(S)=∨_{x∈S}f(x)`. This follows from the promise; it does not compute either `G(A)` or `G(B)`. With multiple solutions, both may contain a solution. With zero solutions, neither does. Any recursive algorithm must test or prove existence at each step, account for errors, and verify the final candidate.

## Variable dependencies and residual subproblems

Unit clauses, implications, XOR equations, and graph-color constraints may shrink a residual formula after an assignment. Define `F|α` as substitution by partial assignment `α`; branching `v=0/1` gives `(F|α)|v=0` and `(F|α)|v=1`. A literal-count, connectivity, or propagation score can predict branch difficulty but does not prove which branch is satisfiable. V5 tests these scores with PySAT existence calls. The score may itself cost more than solving the original formula.

## Operator gate

Before a new quantum operator is implemented, specify a family `𝓕`, a polynomial-time recognizer/certificate for its structural property, a reversible circuit for that property, and a predicted measurement distribution that differs from matched Grover/quantum-backtracking baselines. Include construction, state preparation, uncomputation, verification, shots, and failures. No V5 result currently passes this gate, so no new speculative circuit is introduced.

Lean proves the conditional pair and unique-partition claims in `formal/lean/RCPQI/{Structural,Complementarity}.lean`. The Lean statements take transformation laws as hypotheses and prove no efficient method for finding them.

The [completed V7 review](../research/v7_mathematical_review.md) extends this note with a classical one-query witness theorem for total complementarity, a necessary-and-sufficient known-quotient factorization condition, a coNP-hardness reduction for **semantic** symmetry certification, and a target-independent unique-marker Walsh measurement calculation. It distinguishes these from syntactic automorphism checks and from hidden-shift oracle promises.
