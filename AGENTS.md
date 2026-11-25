# Agent instructions for RCP-QI

RCP-QI is an unproven research hypothesis. Prioritize mathematical correctness and scientific integrity over a positive result.

- Preserve the validated v1 files and all committed raw experiments. Do not rename `rcp_qi_research` or move flat result files without updating import paths, notebooks, manifests, and reproduction commands.
- Use Python 3.12 and `uv sync --locked`. Run `uv run ruff check src tests scripts`, `uv run pytest -q`, and `uv run python scripts/validate_results.py` after relevant changes.
- Build formal proofs from `formal/lean` with the pinned toolchain: `lake build` and `lake env lean RCPQI/AxiomAudit.lean`.
- State whether a claim is an observation, analytic derivation, Lean theorem, conditional theorem, conjecture, negative result, or open question. Python tests and statevector calculations are not Lean proofs or physical quantum experiments.
- Count verification-oracle calls, clause-phase calls, circuit executions, state preparations, measurements, classical preprocessing, transpiled gates/depth, and failed runs separately. Never present an ideal partition oracle as a computational speedup.
- Keep target values and audited satisfying assignments out of the algorithmic decision path. An offline audit may know them if its cost and purpose are labeled.
- Record seeds, versions, assumptions, exact commands, input families, statistical uncertainty, negative findings, and limitations in the experiment registry and results manifest.
- Add Lean theorems without `sorry`, `admit`, or new axioms. Audit dependencies. A conditional proof that assumes a reliable partition oracle is not a proof that the oracle is efficient.
- Keep new modules proportional to measured needs. Preserve Git history and avoid changing working V2 experiments while they run; use a separate worktree if a concurrent run would conflict.
- Do not choose a license, make the repository public, publish a preprint, or disclose the research externally without explicit author approval.

The central question is whether structure in an NP-complete problem can support a partition-existence interference operator whose **complete** computational cost is below generic search. The unstructured quantum query lower bound remains a constraint.
