# Two explicit structured controls

V10 selects exactly two families, both to **falsify** a proposed transfer rather than to benchmark quantum circuits.

## 1. CNF with a supplied primal-tree decomposition of width `k`

The input is a CNF and bags of variables on a tree satisfying coverage, edge/clause containment and running intersection, with maximum bag size `k+1`. Checking a supplied decomposition is polynomial in its explicit size; finding a minimum-width one is a separate task. Standard bag dynamic programming stores up to `2^(k+1)` local assignments per bag, giving `2^{O(k)}·poly(|F|+|certificate|)` classical SAT decision and witness reconstruction. For fixed `k` this is polynomial; unrestricted `k` preserves general SAT difficulty. Direct CDCL and width-based DP are mandatory comparators. A decomposition is a Boolean-structural certificate; Fourier/communication ranks of the verifier under an arbitrary split are Boolean-invariant but need not characterize the DP cost.

**Adversarial instance:** `E(u,v)=∧_i(u_i↔v_i)` has primal graph a matching, width one, and trivial satisfying assignment `u=v=0`. Under the `u|v` evaluation split its communication matrix is an identity of rank `2^n`. Thus efficiently certified low width can coexist with high communication rank, and neither fact supplies a quantum SAT advantage. This is an analytic counterexample, not a claim of hard bounded-width SAT. Prior structural CSP decompositions and width algorithms are reviewed in [Gottlob–Leone–Scarcello](https://ijcai.org/proceedings/1999/57) and the project's V7.1 review.

## 2. Supplied affine subsystem with arbitrary nonlinear residual

The input has explicit GF(2) equations `Ax=b` plus CNF `H(x)`. Row reduction and verification of a claimed basis/particular solution are polynomial. If consistent, write `x=x₀+Bz` with `d=n−rank(A)` free coordinates; satisfiability becomes `∃z H(x₀+Bz)`. The affine-subspace size `2^d` is a semantic property of the **supplied subsystem**, while Fourier/adversary values of the full residual verifier are Boolean-function invariants under fixed conventions and are not automatically computable from the CNF. Gaussian elimination plus residual CDCL, direct CDCL, width DP where applicable, Grover on `d` bits and quantum backtracking are comparators; each must charge substituted-verifier construction and preparation.

**Adversarial instance:** add one fresh constrained bit `b=1` and let `H(z)` be an arbitrary 3-CNF on unconstrained variables. The affine certificate is trivial, while the residual is exactly arbitrary 3-SAT. Existing V7.1 Lean `gated_residual_existence_equivalence` proves the Boolean existential equivalence for `b∧H(z)`; NP-hardness of unrestricted 3-SAT is an external result. An affine certificate may reduce dimension, but it does not by itself identify a satisfying partition or a quantum-specific operation. No full Qiskit simulation or new operator is warranted.
