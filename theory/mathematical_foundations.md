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
