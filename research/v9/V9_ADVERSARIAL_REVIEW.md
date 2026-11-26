# V9 adversarial review and negative findings

| Proposed transfer | Counterexample or unresolved cost | Disposition |
| --- | --- | --- |
| Hard symbolic output means hard partition bit | Perfect-matching CNF generates permanent but every forced-edge partition reduces to bipartite matching | Refuted for this model |
| Many monomials imply large arithmetic circuit | `∏_i(1+z_i)` has `2^n` expanded monomials and `O(n)` DAG | Refuted |
| A high formal tensor/derivative measure obstructs Boolean computation | `Q_k=(z²−z)∏(1+a_i b_i)` computes the zero Boolean function and has raw flattening rank `2^k` | Refuted without Boolean-invariant canonicalization |
| Canonicalization is free | Truth-table interpolation has `2^n` terms; no general cheap compressed constructor proved | Blocked |
| A query lower bound forbids explicit SAT speedup | The adversary input is an `N`-bit oracle family, while an explicit CNF reveals structure; compiler/gate model differs | Invalid transfer |
| Quotient gives a free quantum oracle | Discovery, semantic certification and reversible `q/r` are uncharged in that claim; V7's semantic flip reduction can encode UNSAT | Blocked without promise/costs |
| Permanent lower bound follows unconditionally from 2026 public claims | V8 found no independent semantic acceptance or fully reproduced external proof; `char=2` permanent equals determinant | Conditional, not established here |
| `P_F(1)` tests existence in every field | Counts can cancel modulo characteristic; use formal distinct-monomial zero testing or Boolean decision instead | Refuted |
| An exponentially rare measurement or postselection extracts an exact partition bit cheaply | Repetitions, precision and preparation must be charged; no bounded-cost scheme supplied | Unsupported |
| A nonuniform small DAG gives a uniform efficient constructor | Existence of a circuit family need not yield an algorithm printing it | Invalid implication |

The negative result here is scoped: a complete symbolic generating polynomial is a materially stronger output than partition existence; formal-expression measures may disappear modulo the Boolean ideal; and generic half-label extraction retains search-scale black-box query cost. None rules out all structured quantum SAT algorithms or establishes `P≠NP`, `NP⊄BQP`, or unrestricted quantum gate lower bounds.
