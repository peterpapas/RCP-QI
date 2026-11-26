# Complexity invariants under Boolean equivalence

“Invariant” means unchanged when two formal polynomials agree on every Boolean assignment. It does **not** mean efficiently computable from a CNF. A lower bound must name the input encoding and resource.

| Candidate | Boolean-invariant? | Computing/certifying it | Valid lower-bound scope and transfer limit |
| --- | --- | --- | --- |
| Degree of the **canonical multilinear** polynomial | Yes, field-dependent | Truth-table interpolation uses up to `2^n` values; no generic efficient CNF extraction shown | Exact polynomial *query* degree for the appropriate oracle-input variables; high degree of a verifier on assignment bits alone does not make SAT search hard (`∧_i x_i` is easy) |
| Approximate degree of a Boolean function (over reals, fixed error) | Yes | Optimization over truth table is large; no efficient CNF certificate supplied | [Beals et al.](https://arxiv.org/abs/quant-ph/9802049) relate degree to **black-box query** count; not an explicit-CNF gate/time bound |
| Walsh–Fourier support/sparsity or norm of the canonical truth table | Yes after fixing field, basis and normalization | Full transform has `2^n` entries; succinct cases may be accessible | Function property, not by itself a general SAT or quantum lower bound; choice of Fourier basis matters |
| Communication rank of the truth table under a **fixed** variable split | Yes | Matrix can have exponentially many entries; structural certificates need proof | Communication cost for that split/model, not unrestricted SAT time; changing split changes the measure |
| Tensor rank of the truth table with a fixed tensorization | Yes | Generally hard to obtain; no cheap detector supplied | Only a lower bound if a theorem links it to the exact restricted circuit/network model |
| General adversary value for a specified black-box input family | Yes | May need large semidefinite optimization or analytic witness | Quantum **query** lower bound under its oracle and promise, not a quantum gate or SAT lower bound |
| Formal polynomial degree, monomial count, partial derivatives, raw coefficient tensor rank | **No** | May be easy on an input expression while irrelevant to the function | `Q_k` in the Boolean-ideal analysis equals zero on all Boolean inputs but can change these measures arbitrarily with `k` |
| Arithmetic circuit size of a chosen formal representative | **No** as a function invariant | Minimization is not provided by the syntax | Arithmetic lower bound concerns that formal polynomial over the field, not all cube-equivalent representations |

The search domain matters. For unique-marker search, the input to the query algorithm is a length-`N` **oracle truth table**; the output is a partition bit. Its approximate degree/adversary lower bound concerns those `N` black-box bits. For explicit SAT, input bits encode clauses, while assignment bits are *variables queried by the verifier*. Interchanging them invalidates a transfer.

The canonical multilinear polynomial is unique in the quotient ring, but the interpolation formula is not an efficient circuit constructor. A highly structured function can have a small compressed circuit even when its expanded coefficient list is large. Conversely, a large raw coefficient rank of a noncanonical expression can coexist with a tiny circuit and the zero Boolean function. These facts disqualify representation-sensitive rank/degree arguments as direct RCP-QI obstructions.

Prior art: unique multilinear/Fourier expansion is standard in [O'Donnell's author-hosted book](https://www.cs.cmu.edu/~./odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf); quantum polynomial query bounds are in [Beals et al.](https://arxiv.org/abs/quant-ph/9802049); quantum adversary bounds are in [Høyer–Lee–Špalek](https://arxiv.org/abs/quant-ph/0611054). The table does not claim that all listed measures are equally useful or that any gives a new SAT lower bound.
