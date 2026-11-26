# Recursive Constraint Partitioning via Quantum Interference

RCP-QI began as **Recursive Complementary Partitioning with Quantum Interference**: could a quantum procedure cheaply identify which half of a constraint search space contains a solution? This repository preserves the V1–V10 investigation, its code, Lean proofs, raw results and negative findings.

**Status: SUSPENDED — PENDING NEW MATHEMATICAL INSIGHT.** The research phase is complete and open for mathematical review. This post-publication correction addresses missing prior art and the scope of V3; it is maintenance, not V11.

The central unresolved question is whether an efficiently certified property of an explicit hard constraint family can yield a quantum information task with a complete cost advantage over equally informed classical and quantum algorithms.

## What the evidence says

- One standard Grover iteration raises correct-half probability to `1/2 + 4/N − 8/N²`, a vanishing `O(1/N)` bias. Independent repeated sampling of that circuit costs `Θ(N²)` shots for fixed confidence.
- The original V3 “local” control reflected **only the partition bit**. It did not test diffusion inside each block. [Grover–Radhakrishnan partial quantum search](research/corrections/PARTIAL_SEARCH_PRIOR_ART.md) is established prior art and gives a constant-factor query saving for a block label while retaining `Θ(√N)` generic query scaling. The [correction results](research/corrections/PARTIAL_SEARCH_RESULTS.md) distinguish the operators and preserve V3 raw data.
- V5.1 observed no crossover over direct modern SAT solving in its limited benchmark. V7–V10 exposed structural-certification, algebraic-transfer, query-model and proof-model limits. These scoped findings are collected in the [final report](research/archive/RCPQI_FINAL_RESEARCH_REPORT.md).
- This work proves neither `P = NP` nor `P ≠ NP`, establishes no novel quantum computational advantage, no universal impossibility theorem for quantum SAT, and no independently established publishable mathematical novelty.

## Navigate the archive

| Purpose | Location |
| --- | --- |
| Executive summary and complete V1–V10 record | [Executive summary](research/archive/RCPQI_EXECUTIVE_SUMMARY.md) · [final report](research/archive/RCPQI_FINAL_RESEARCH_REPORT.md) · [original publication README](README_AT_PUBLICATION.md) |
| Corrections and original-source review | [Adjudication](research/corrections/REVIEWER_ADJUDICATION.md) · [partial search](research/corrections/PARTIAL_SEARCH_PRIOR_ART.md) · [literature review](research/literature_review.md) |
| Theorems and formal scope | [Catalogue](THEOREMS.md) · [Lean source](formal/lean/) · [formal status](theory/formal_status.md) |
| Rejected mechanisms and restart gate | [Negative results](NEGATIVE_RESULTS.md) · [roadmap](ROADMAP.md) · [contributing](CONTRIBUTING.md) |
| Programs and preserved evidence | [Python source](src/rcp_qi_research/) · [experiments](experiments/) · [results](results/) · [tests](tests/) |

## Reproduce and review

Use Python 3.12, [uv](https://docs.astral.sh/uv/) and the pinned Lean toolchain. From the repository root run `uv sync --locked`, `uv run pytest -q`, `uv run ruff check src tests scripts`, `uv run python scripts/validate_results.py`, `uv run python scripts/verify_archive.py` and `uv run python scripts/validate_partial_search.py`. In `formal/lean`, run `lake build` and `lake env lean RCPQI/AxiomAudit.lean`. The [reproducibility record](research/archive/RCPQI_REPRODUCIBILITY.md) gives the remaining checks and limitations. The two third-party SAT Competition files are fetched separately with SHA-256 verification as described in the [benchmark instructions](benchmarks/instances/satcomp2025/README.md).

To challenge a claim, cite its exact model, proof or result row and the relevant [prior art](research/literature_review.md). The [contribution guide](CONTRIBUTING.md) requires a mathematical hypothesis, full costs and independent review before any new operator work. Code and original research prose have [separate licenses](LICENSING.md); [CITATION.cff](CITATION.cff) provides citation metadata.
