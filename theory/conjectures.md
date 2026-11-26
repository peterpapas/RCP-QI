# Conjectures and open questions

**H1 (open):** Constraint structure may permit a quantum operator that distinguishes whether a bit-prefix partition contains a satisfying assignment with lower *complete* cost than generic Grover-based existence testing on some specified instance family.

To make H1 testable, specify the family distribution, preprocessing, state preparation, reversible verifier, operator construction, oracle queries, gates, ancillas, measurements, repetitions, error target, and strongest relevant classical and quantum baselines. A benefit on a hand-picked trivial formula, or in an oracle model that already exposes partition existence, would not establish H1.

**H2 (falsified for tested controls):** A full-space single Grover iteration or a partition-bit-only diffuser gives a constant-accuracy partition decision at (O(1)) verifier calls as (N\to\infty). The analytic one-iteration bias decays as (O(1/N)); the **partition-bit-only reflection** showed no measurable partition advantage in the tested cases. This does not apply to established [intra-block partial search](../research/corrections/PARTIAL_SEARCH_PRIOR_ART.md), which retains square-root generic query scaling.

**Open:** Whether an entangled register plus a truly new constraint-dependent operation can extract useful partition information without merely relocating Grover's cost. The current ancilla controls expose no extra information by themselves.
