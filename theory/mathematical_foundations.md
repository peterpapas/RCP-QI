# Interference derivations

For one marked state in a uniform (N=2^n) search space, let (\theta=\arcsin(1/\sqrt N)). After (r) standard Grover iterations, the marked probability is

\[
P_{\rm sol}(r)=\sin^2((2r+1)\theta).
\]

Symmetry gives each unmarked state probability ((1-P_{\rm sol})/(N-1)). The half containing the solution therefore has

\[
P_{\rm half}(r)=P_{\rm sol}(r)+\left(\frac N2-1\right)\frac{1-P_{\rm sol}(r)}{N-1}
=\frac{N-2+N P_{\rm sol}(r)}{2(N-1)}.
\]

At (r=1), (P_{\rm half}=1/2+4/N-8/N^2). This was analytically derived and checked by statevector simulation to machine precision in V1. The V2 multi-iteration sweep checks both probabilities for multiple target locations and seeded shot samples. This is analytical and numerical evidence, **not** a Lean proof of the formula or a physical experiment.

For a desired one-shot half accuracy (q>1/2), the relation implies (P_{\rm sol}\ge 2q-1+2(1-q)/N). A constant half accuracy therefore entails substantial exact-solution amplification in this symmetric Grover construction. At one iteration the half bias is (4/N-8/N^2); independent partition-bit majority votes need order (N^2) shots for fixed confidence. Each shot repeats the phase oracle, state preparation, and measurement.

An ancilla copied before data-only Grover operations cannot reveal the target half through its own reduced state, because partial trace is invariant under a unitary acting solely on the traced-out data: (\operatorname{Tr}_D[(U_D\otimes I)\rho(U_D^\dagger\otimes I)]=\operatorname{Tr}_D(\rho)). Copying after Grover exposes the already-created half bias; it does not amplify it.

## Exact algebra and scope of the Lean statements

For a balanced partition and one marked item, set `p=P_sol(r)`, and let `u=(1-p)/(N-1)` be the probability of each unmarked item. Normalization is `p+(N-1)u=1`. The correct-half probability is `q=p+(N/2-1)u`. Eliminating `u` gives `2(N-1)q=N-2+Np`. This is the V2 relation for **standard Grover interference with equal unmarked amplitudes**, not an arbitrary quantum operator or nonuniform preparation. At fixed target half accuracy `q>1/2`, `p=2q-1+2(1-q)/N`; the exact-solution probability must therefore be a positive constant asymptotically within this circuit family.

For one Grover iteration, uniform preparation gives every amplitude `1/√N`. The phase oracle negates the marked amplitude, so the post-oracle mean is `(N-2)/(N√N)`. Reflecting amplitudes about that mean gives marked amplitude `2(N-2)/(N√N)+1/√N=(3N-4)/N^(3/2)` and each unmarked amplitude `2(N-2)/(N√N)-1/√N=(N-4)/N^(3/2)` (a global sign has no effect). Hence `N³p=(3N-4)²` and `N³u=(N-4)²`. Substitution yields `2N³q=N³+8N²-16N`, or `q=1/2+4/N-8/N²` for `N>0`. Lean proves the algebraic V2 and V1 identities **conditional on these amplitude/probability equations** in `RCPQI/Probability.lean`. It does not formalize Qiskit gates, trigonometric Grover rotation, Born measurement, or hardware behavior. The statevector comparison checks the implementation separately; there is no refinement proof linking Lean to Qiskit.

The one-iteration bias `4/N-8/N²` requires `Θ(N²)` independent shots for a fixed-confidence majority decision if this single-iteration circuit is repeated. This is a sampling statement for that protocol, not a lower bound on every partition algorithm. The black-box `Ω(√N)` search lower bound applies to unstructured verification queries, while any claim for a structured input family needs its own full cost analysis.
