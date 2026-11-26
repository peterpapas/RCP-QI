# V8 final research report

**Research round:** 26 November 2026. **Primary recommendation: D — pivot towards lower-bound and impossibility research.** This is a scoped model-comparison result, not an assertion that unrestricted SAT or quantum speedups are impossible.

## What was examined

The complete RCP-QI history through commit `a46da18` was reviewed, including the user-named V7 commit `79d29f9`, V1–V6 operators/cost counters, V5/V5.1 classical benchmarks, V7/V7.1 proofs, formal axiom audit, registry, raw-result manifest and negative findings. V1–V7.1 findings remain valid within their stated models. No code or immutable experimental data from those phases was altered.

Two public November 2026 VP–VNP claims were located in pinned primary repositories. [Anthropic](https://github.com/anthropics/formal-math/tree/11b6c7e3c927df2658f513b6b68ea7f8929c62c5/vp-vnp) claims an exact and Laurent-series border arithmetic separation over every field, with its permanent lower bound except in characteristic two. [OpenAI's 23 November paper](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/VP-and-VNP-are-different-November-23-2026) claims a stronger quantitative border bound for an explicit VNP family, while its [Lean scope note](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/lean/docs/379.md) describes an exact superpolynomial theorem and identifies stronger border rates as unformalized. Anthropic explicitly disclaims human mathematical review. Publication and internal formal checks do not establish independent acceptance. Exact revision hashes, audit commands, theorem scope and build outcomes are in [source verification](V8_SOURCE_VERIFICATION.md).

The [technique analysis](V8_PROOF_TECHNIQUE_ANALYSIS.md) reconstructs the claimed mechanisms. Anthropic's two-case route uses tensor spectral prices and balanced cuts, or contraction identities followed by counting-program diagonalization. OpenAI uses Euclidean tensor-wire rigidity or a strict-shortening replay construction with algebraic-geometric boundary handling. Both prove lower bounds in arithmetic models if correct; neither supplies an algorithm for discovering SAT structure or a quantum partition-existence operator.

## Decision gates

| Gate | Outcome | Evidence |
| --- | --- | --- |
| 0. Source authenticity | **Pass for authentic public claims; proof validity unresolved** | Pinned papers and Lean repositories exist. No independent semantic expert acceptance was established in this audit. External build status is separately recorded. |
| 1. Mathematical relevance | **Pass as a scoped analogy** | Tensor cuts, symbolic counting and network structure are relevant mathematical representations of CNF factors/partitions. |
| 2. Transfer validity | **Fail for unrestricted Boolean or quantum claims** | Exact formal-polynomial equality is stronger than agreement on the Boolean cube; `z²−z` is a concrete Lean-backed counterexample. Nonuniform arithmetic lower bounds lack a model-preserving reduction to uniform SAT or quantum circuits. |
| 3. Complete-cost advantage | **Fail** | A compact clause polynomial gives cheap evaluation at one assignment, not cheap partition counts. Low width has classical dynamic programming; low rank has discovery cost; QSVT of a marker still needs a prepared state and observable gap. No candidate beats matched CDCL, structural classical methods, Grover/amplification or backtracking. |
| 4. New architecture | **Not authorized** | No candidate survived Gates 2–3; no speculative Qiskit operator or V8 experimental result was produced. |

## New mathematical findings and limits

The [transfer report](V8_MATHEMATICAL_TRANSFER.md) gives a clause-validity expression `q_F`, an exact partition count `Z_F(p)` and a phase-amplitude relation. Their construction, evaluation at one assignment, extraction of a count, and coherent use are distinct cost steps. In characteristic two, even witness counts can cancel. A supplied low-width decomposition may make the same task classically tractable; a supplied low-rank or symmetry certificate must be obtained and checked. A generic black-box unique residual still obeys the established [quantum search bound](https://arxiv.org/abs/quant-ph/9701001).

The new Lean module verifies only that `z*z-z` is zero on Boolean inputs but nonzero at `2`; the arbitrary-field polynomial-ring statement and all complexity corollaries remain informal. This is enough to falsify an unqualified **transfer argument**, not either VP–VNP paper. The [hypothesis registry](V8_HYPOTHESIS_REGISTRY.md) and [adversarial review](V8_ADVERSARIAL_REVIEW.md) retain rejected and unresolved mechanisms. No positive V8 experiment was justified, so the conditional `V8_EXPERIMENTAL_RESULTS.md` artifact is intentionally absent.

## Highest-value next question

Define a restricted **symbolic arithmetic partition-operator** model and prove, or refute, that a hard VNP family is a charged projection of its symbolic output and that every permitted operator has an arithmetic-circuit simulation. In parallel, strengthen V7's quotient/oracle characterization with explicit discovery and section costs. This can produce a defensible limitations theorem without pretending it rules out general Boolean or quantum SAT solving. Revisit a constructive quantum direction only when a cheaply certified structural promise leaves a meaningful hard residual and supplies a proved measurement gap after full resource accounting.
