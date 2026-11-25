# V7: structural complementarity investigation

Status: mathematical characterization and candidate-property screen, **no new quantum operator**. This note runs alongside the V5.1 classical scaling benchmark and does not depend on its outcome.

## 1. A strong complementing map is incompatible with unique search

Assume `T²=id` and `f(Tx)=1-f(x)` for every assignment. Each orbit has two members, exactly one satisfying. If `f` has one satisfying assignment `w`, then every assignment must be either `w` or `T(w)`. Thus a unique-solution search space with more than two assignments cannot have a total complementing involution. `RCPQI.unique_complementing_universe_is_pair` proves the conditional pair characterization in Lean 4; the cardinality consequence requires a finite type and is stated here analytically. This eliminates the original global pair hypothesis for ordinary unique-solution SAT at `n>1`.

A **partial** complementing relation on selected candidates may exist, but discovering the relation and its domain from a CNF can conceal satisfiability work. Every proposed relation needs an efficiently checkable certificate and an explicit domain fraction. A map supplied as an oracle is a stronger input model.

## 2. Recursive cost characterization

An exact classical SAT-existence self-reduction first checks root satisfiability, then asks one branch question for each of `n` variables: `n+1` solver calls on a satisfiable instance. The direct CDCL baseline asks once and returns a model. The number of calls alone does **not** prove a wall-time ordering: incremental assumptions may be cheaper than a fresh solve, and learned clauses may be reused. V5.1 records cumulative solver work and complete scoring time to test this distinction.

The Lean theorem `totalCost_of_minimum_oracle` proves that if every charged decision costs at least `c`, the sum of `n` decisions costs at least `n c`. It is conditional and makes no unstructured or NP-complete lower-bound claim. A quantum partition decision would need a reversible implementation and its own cost `C(k)`; substituting a classical SAT solver is only a control.

## 3. Property-to-operator screen

| Property | Efficient certificate on supplied representation | Classical exploitation | Quantum question | Current decision |
| --- | --- | --- | --- | --- |
| Affine XOR constraints | Gaussian elimination over `GF(2)` | Direct polynomial-time solution | Could Fourier sampling recover a hidden linear form when it is not explicitly supplied? What is the phase-oracle construction cost? | Tractable control; no SAT speedup claim. |
| 2-CNF implications | Implication graph and SCC | Direct linear-time decision | Can coherent traversal improve anything once SCC is available? | Tractable control; no operator justified. |
| Exact variable-swap CNF symmetry | Signed clause-multiset equality for a supplied swap | Symmetry-breaking predicates or orbit representatives | Can a group action be implemented and a useful quotient state prepared below classical detection/reduction cost? | V5.1 charges certification; no coherent quotient circuit yet. |
| Unit propagation / residual simplification | Polynomial-time literal propagation | DPLL/CDCL already exploit it | Can a reversible partial-assignment walk exploit a smaller tree beyond quantum backtracking? | Requires comparison with Montanaro-style quantum backtracking and reversible update cost. |
| Low residual score / occurrence | Cheap heuristic, no correctness certificate for existence | Branch choice | Is there a provable correlation with successful-partition amplitude on a specified distribution? | V5.1 empirical screen only; not an operator hypothesis. |

## 4. Gate for V8

Advance only after a specified family has: (i) an efficiently recognizable structural promise, (ii) a theorem or falsifiable quantitative prediction for a partition measurement, (iii) a reversible construction with all preprocessing, setup, ancilla, oracle, uncomputation, measurement, repetition, and verification costs, and (iv) an advantage over direct classical CDCL, the dedicated family algorithm, standard amplitude amplification, and relevant quantum backtracking under matched success criteria. The present work satisfies none of those conditions for a nontrivial NP-complete family. A negative or equivalence result is an acceptable V7 outcome.
