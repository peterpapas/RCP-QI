# V9 final report — Boolean-ideal and quantum-transfer audit

## Result

V9 defines a precise **symbolic polynomial output** task and proves analytically that a polynomial-size perfect-matching CNF produces the permanent as its satisfying-assignment generating polynomial. An expanded monomial list needs `m!` entries. A superpolynomial bound for a compressed exact arithmetic DAG remains **conditional** on an independently accepted permanent/VP–VNP lower bound (outside characteristic 2). Yet every forced-edge partition-existence question for this family is polynomial-time bipartite matching. This defeats an unqualified transfer from symbolic-output hardness to partition-decision hardness.

The Boolean quotient `K[x]/⟨x_i²−x_i⟩` identifies precisely the polynomials agreeing on the Boolean cube. Raw formal degree/rank/monomial measures are not invariants of the Boolean verifier. The explicit zero-function family `(z²−z)∏(1+a_i b_i)` has raw coefficient flattening rank `2^k` but a linear-size arithmetic DAG. Canonical multilinear measures are invariant, but extracting or representing them is a separate computational task.

For **unique-marker black-box access**, extracting only the balanced-half label still needs `Θ(√N)` quantum queries: the all-ones cross-half adversary matrix has norm `M` and each address difference matrix has norm `√M`, with `N=2M`. This established query-method application does not imply an explicit-SAT gate or time lower bound. Boolean-equivalent arithmetic representations induce identical literal phase oracles; a full-output complement differs by global sign for uncontrolled use. No new quantum operator is justified.

## Decision gates

| Gate | Result |
| --- | --- |
| 1. Precise model | **Pass** for exact formal generating-polynomial output, expanded list, partition decision, and standard query oracle as separate models. |
| 2. Invariant survives equivalence | **Pass** for canonical Boolean function, its Fourier/approximate-degree properties and oracle action; **fail** for raw formal degree/rank/monomial measures. |
| 3. Bound reaches intended model | **Pass** for expanded-output size and unique-marker query complexity; **fail** for general SAT decision, explicit quantum gate complexity and unrestricted symbolic DAG bounds. |
| 4. Premise status | Output-list bound and model counterexample are analytic unconditional results. Arithmetic-DAG lower bound is conditional on unsettled public claims. Query bound uses established cited adversary theorem. |
| 5. Contribution beyond literature | A clear model-boundary synthesis, but no independently credible novel standalone lower bound identified. |
| 6. Constructive opportunity | None passes supplied/discovered structure, complete-cost, matched-baseline and falsifiability requirements. Quantum architecture work remains suspended. |

## Validation and evidence level

New Lean proofs cover arbitrary finite-cube **interpolation evaluation**, one-variable ideal-generator identities, literal phase signs and fixed classical quotient-query transcripts. The general quotient-ring theorem, permanent identity, matching reduction and adversary norm calculation are analytic arguments, **not** Lean theorems. Established external complexity results are cited in the [prior-art review](V9_PRIOR_ART_AND_NOVELTY.md). V8's source-authentication limitations remain; no independent acceptance of the claimed 2026 VP–VNP proofs was found in this round.

Validation on 26 November 2026: `uv sync --locked` completed (120 packages resolved, 117 checked); `uv run ruff check src tests scripts` passed; `uv run pytest -q` passed **65 tests**; `uv run python scripts/validate_results.py` passed the manifest, V1/V2 probabilities and V1–V6 accounting; from `formal/lean`, `lake build` completed **30 jobs** and `lake env lean RCPQI/AxiomAudit.lean` completed with no new project axioms. `git diff --check` passed. No V9 numerical or quantum-circuit experiment exists, so no raw quantum results or plots are asserted.

## Recommendation

**D — continue foundational mathematical research because the transfer remains unresolved.** The next bounded question is whether a *Boolean-invariant*, efficiently certifiable structural measure yields a lower bound or algorithm for a precisely restricted **explicit-input** SAT model after accounting for certificate discovery and coherent implementation. The permanent encoding is valuable as a control showing why a stronger symbolic task cannot substitute for partition decision. Independently review any proposed theorem for prior art before a limitations-paper decision. Preserve V1–V8 and do not implement a speculative V9/V10 operator.
