# V8 decision brief

**Recommendation: D — pivot towards lower-bound and impossibility research.**

Two genuine public research artifacts claim `VP ≠ VNP`. Their mathematical and formal scopes differ, and independent acceptance was not established in this review. Both concern arithmetic circuits computing *formal polynomials*, not arbitrary SAT solvers or quantum circuits. Neither supplies a partition oracle, a new quantum operator, or a route to `P≠NP` on the evidence inspected.

The clearest result for RCP-QI is a **transfer barrier**: `z²−z` vanishes on all Boolean inputs while changing formal arithmetic behavior. Thus an arithmetic lower-bound invariant cannot simply be applied to any Boolean verifier or quantum circuit. The project now has a narrow Lean proof of this evaluation counterexample, a costed algebraic reconstruction of CNF partitions, and a registry of failed or incomplete transfer hypotheses. V1–V7.1 evidence is preserved.

**Investment decision:** fund a bounded theorem effort, not V8 circuit engineering. Specify a symbolic arithmetic partition model; test whether its output projects to a hard VNP polynomial with charged polynomial overhead; then check whether any resulting obstruction survives Boolean-ideal equivalence and coherent quantum operations. The strongest practical comparator remains direct structure-aware SAT solving plus known quantum search/backtracking. A candidate quantum architecture can return only after its input promise, certification, observable signal, and full cost beat those baselines.

**Principal blockers:** source claims await independent semantic review; OpenAI's paper-level border rate is stronger than its documented Lean scope; formal-polynomial identities do not transfer to Boolean agreement; no cheap structural promise with a hard residual and quantum-specific gap has been identified. The decision is **not** a universal impossibility claim.
