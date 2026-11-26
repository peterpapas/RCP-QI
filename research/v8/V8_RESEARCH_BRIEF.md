# V8 research brief and initial plan

**Opened:** 26 November 2026. **Object:** test whether the November 2026 VP–VNP claims supply a valid mathematical transfer to RCP-QI. This is a theory and source-audit round, not an approved V8 circuit experiment. The historical V1–V7.1 results and raw data are controls.

## Plan and gates

1. **Gate 0 — authenticity:** pin the Anthropic and OpenAI primary commits, read the papers and exact Lean theorem statements, reproduce available builds where feasible, audit axioms and semantic scope, and check correction/review status. A paper claim, a Lean build, and independent mathematical acceptance are different evidence.
2. **Gate 1 — relevance:** reconstruct the proof mechanisms as dependency graphs and identify the exact invariant that might touch SAT partitions, witnesses, or quantum amplitudes.
3. **Gate 2 — transfer:** make all changes of model explicit: formal polynomial versus Boolean cube; nonuniform arithmetic circuit versus uniform SAT or quantum algorithm; exact/border polynomial identity versus bounded-error measurement. Prove a scoped transfer or exhibit a counterexample.
4. **Gate 3 — advantage:** compare any surviving promise with the best equally informed classical and quantum baselines, including discovery, certification, state preparation, circuit and repeated-measurement costs.
5. **Gate 4 — implementation:** only build a circuit after a precise operator, costed oracle, falsifiable output prediction, and strict advantage survive the previous gates. Otherwise document negative results and the next theorem.

The deliverables under this directory are a source audit, algebraic complexity review, technique analysis, mathematical transfer, hypothesis registry, adversarial review, Lean status, final report and one decision brief. `V8_EXPERIMENTAL_RESULTS.md` is created only if Gate 4 authorizes an experiment. The committed registry entry is theory-only otherwise.

## Fixed research rules

Use the paper's theorem statements as **claims** until independently checked. Credit external Lean builds only as checks of formalized propositions. Do not infer `P ≠ NP`, `NP ⊄ BQP`, Boolean SAT hardness, or a new quantum operator from `VP ≠ VNP`. For any proposed reduction, state the input representation and the uniformity, field, oracle, precision, and success conventions. Count all preprocessing and failed attempts. No public release is authorized by this round.
