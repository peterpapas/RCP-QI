# Post-publication partial-search control

**Experiment ID:** `POSTPUB-PARTIAL-SEARCH-20261127`. This is an established-algorithm comparison, not V11 or a novel RCP-QI operator. The immutable V1–V10 [manifest](../../results/manifest.json) and closeout [integrity inventory](../archive/artifact_integrity.json) are unchanged. New [machine-readable rows, threshold CSV, plot and SHA-256 inventory](../../results/corrections/partial_search_20261127/) are separate.

## Method and finite-size derivation

The [reference implementation](../../src/rcp_qi_research/partial_search.py) applies the [published global/local/final-global sequence](PARTIAL_SEARCH_PRIOR_ART.md). A local step uses a full-register equality phase oracle and reflects on the `n−1` within-block qubits. A global step uses the same phase oracle and reflects on all `n` data qubits. The final step is always global. The schedule is chosen from `N` and the confidence threshold, never the target address. For each total call count `q`, all nonnegative integer pairs `(j1,j2)` with `j1+j2+1=q` are considered. The first `q` meeting the threshold is therefore minimum **within this one-shot sequence family**, not among all partial-search algorithms or repeated-shot protocols.

The analytic calculation tracks three amplitudes per basis state: `a` for the target, `b` for the other `N/2−1` states in its block and `c` for all states in the other block. A global oracle step negates `a`, then replaces each amplitude `u` by `2μ−u`, with `μ=(a+(N/2−1)b+(N/2)c)/N` after that negation. A local oracle step negates `a`, then reflects only `a,b` about `ν=(a+(N/2−1)b)/(N/2)`; `c` remains unchanged. After `j1` global, `j2` local and one global step, `P_half=a²+(N/2−1)b²` and `P_solution=a²`. This exact finite-size recurrence predicts all statevectors; no marked position is used in it.

## Results

| `N` | Threshold | Partial queries | V2 one-shot queries |
| ---: | ---: | ---: | ---: |
| 16 | 90% / 95% / 99% | 2 / 2 / 2 | 2 / 2 / 9 |
| 64 | 90% / 95% / 99% | 4 / 4 / 5 | 4 / 5 / 6 |
| 256 | 90% / 95% / 99% | **7 / 8 / 9** | **9 / 10 / 11** |
| 512 | 90% / 95% / 99% | 9 / 10 / 12 | 13 / 14 / 16 |

The reviewer’s `N=256` call counts are **confirmed** in this stated schedule family. The actual probabilities and compiled resources at `N=256`, target `0`, are:

| Required half accuracy | `(j1,j2,final)` | Achieved half / exact-item probability | Partial gates / depth | V2 gates / depth |
| --- | --- | --- | ---: | ---: |
| ≥90% | `(0,6,1)` | `0.9469626746` / `0.5306190308` | 4,773 / 2,016 | 8,163 / 3,224 |
| ≥95% | `(0,7,1)` | `0.9881238042` / `0.5752070980` | 5,416 / 2,292 | 9,069 / 3,582 |
| ≥99% | `(2,6,1)` | `0.9999523265` / `0.6324572931` | 6,585 / 2,732 | 9,975 / 3,940 |

The 60 Qiskit ideal statevectors cover five marked positions for each size and threshold. Their largest absolute difference from the three-amplitude prediction is `2.8×10⁻¹⁴`; the correct-half probability is target-position independent to numerical precision. The new [accuracy-versus-oracle-query plot](../../results/corrections/partial_search_20261127/accuracy_vs_queries.png) displays the finite-size comparison. Local 99% at `N=256` is not exact-item 99%: partial search returns less information.

Every local or global step costs one equality phase-oracle call. Each row records one state preparation, one planned partition-bit measurement, zero sampled shots (statevector computation), zero candidate-verification calls, zero ancillas, circuit-build time, simulation time, transpilation time and compiled gate/depth counts in Qiskit's `u,cx` basis at optimization level 0. The V2 gate/depth comparator also measures one partition bit. These are simulator/compilation resources for an equality oracle, not hardware or fault-tolerant costs. A complete recursive or SAT solution would add subproblem preparation, errors/retries and final witness verification; no quantum SAT advantage follows.

## Reproduce and validate

```powershell
uv sync --locked
uv run pytest -q tests/mathematical/test_partial_search.py
uv run python scripts/validate_partial_search.py
uv run python -m rcp_qi_research.partial_search --output-dir <new-empty-directory>
```

The last command refuses to overwrite an existing artifact directory. Compare the newly generated numerical probabilities and accounting to the committed rows; wall times and exact image bytes can vary by host. The new validator checks the pinned hashes of committed artifacts, analytic and statevector agreement, schedule minima and target independence. Its [SHA-256 inventory](../../results/corrections/partial_search_20261127/manifest.json) covers only these correction artifacts.
