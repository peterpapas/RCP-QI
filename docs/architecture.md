# Architecture and non-destructive migration plan

The existing package is `src/rcp_qi_research`, with stable CLI commands and notebooks. The requested diagram used `src/rcp_qi`; renaming now would break imports and editable installations without adding scientific value. New interfaces live under the existing package. The repository folder remains `rcp-qi-research` for the same reason.

| Current asset | Risk if moved | Decision |
| --- | --- | --- |
| `src/rcp_qi_research/*.py` | CLI entry points and tests import these paths | Preserve; add small functional subpackages as needed |
| `results/initial.*`, `one_iteration.*` | V1 reproduction and notebook use flat paths | Preserve as immutable V1 history |
| `results/phase2_*` | Phase 2 commands and registry use flat paths | Preserve; manifest identifies raw data and figures |
| `notebooks/initial_experiment.ipynb` | Relative result paths | Preserve |
| Git commits | Evidence of experiment progression | Preserve; new infrastructure is a later commit |

`src/rcp_qi_research/core` defines implicit bit-prefix partitions. Existing `problems.py`, `search.py`, and experiment modules remain the working implementations; a future migration can move them behind stable imports once there is a concrete benefit. The top-level `experiments/` entries describe methods and link immutable data, while `benchmarks/` holds cross-experiment validation and instance documentation. `theory/` separates derivations from Lean proofs. `formal/lean/` is a standalone, core-Lean Lake project; no Mathlib dependency is needed for the initial finite-partition theorems. `research/` tracks hypotheses and negative findings. `paper/` is an unpublished manuscript scaffold.

The flat `results/` files remain canonical raw history. New processed tables go under `results/processed/`; future experiments may use `--output-dir results/raw/<id>` and copy figures to `results/figures/<id>` after their consumers are updated. No files are moved by this infrastructure change.

The Python and Lean CI jobs are independent. Neither checks hardware performance, proves the implementation corresponds to the Lean model, or establishes an NP-complete speedup.
