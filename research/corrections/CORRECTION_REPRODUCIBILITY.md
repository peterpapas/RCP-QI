# Post-publication correction reproducibility record

**Experiment:** `POSTPUB-PARTIAL-SEARCH-20261127`. Source branch `research/partial-search-prior-art-corrections` started at `b1c645911ea16fad207e3a268eb65903fc5158d4`. The dedicated [artifact manifest](../../results/corrections/partial_search_20261127/manifest.json) pins the three newly generated files by bytes and SHA-256. The historical [V1–V10 manifest](../../results/manifest.json) and [closeout inventory](../archive/artifact_integrity.json) were not edited.

## Environment

Validation host: Windows PowerShell, Python 3.12.10, uv 0.12.5, Qiskit 2.6.2, Aer 0.18.4, NumPy 2.5.5, SciPy 1.18.1, Matplotlib 3.11.2, pytest 9.2.0, Ruff 0.17.6 and Lean 4.36.0. Dependencies resolve from the existing `uv.lock` and Lean toolchain file; no dependency lock was changed. The ideal Qiskit statevector is deterministic. Circuit construction, simulation and transpilation times are host dependent; image bytes can vary across plotting environments.

## Commands and results

From the repository root:

```powershell
uv sync --locked --python 3.12
uv run ruff check src tests scripts
uv run pytest -q
uv run python scripts/validate_results.py
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_pilot_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_heldout_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_large_controls_20261126
uv run python scripts/verify_archive.py
uv run python scripts/validate_partial_search.py
git diff --check
```

All passed on 27 November 2026: **74 pytest tests**, Ruff, historical result validator, all three V5.1 validators, **38** unchanged historical artifact digests, **47** named Lean catalogue entries, **64** checked local links at the first correction pass, and the new validator's **12 schedules, 60 statevector rows and 3 correction artifacts**. `git diff --check` found no whitespace errors. The link count may grow as new documentation is added.

From `formal/lean`:

```powershell
& "$env:USERPROFILE\.elan\bin\lake.exe" build
& "$env:USERPROFILE\.elan\bin\lake.exe" env lean RCPQI/AxiomAudit.lean
```

Both passed: **34 Lean build jobs**; the audit reports no project-defined axioms and only the existing standard Lean axioms where printed. No Lean source or theorem statement was changed. Externally cited complexity theorems and the new Qiskit circuit are not Lean-verified.

## Fresh numerical replication

From the root, write into a **new empty** directory:

```powershell
uv run python -m rcp_qi_research.partial_search --output-dir <new-empty-directory>
```

The program refuses to overwrite populated output. Compare schedules, statevector probabilities and logical query counts with the committed JSON/CSV. The manifest validator checks the committed run, not a newly generated file with different host times. Tests check basis-state operator targeting, 90/95/99% minimum schedules within the specified family, target independence and analytic/statevector agreement. No noise, sampled shots, fault-tolerant resources, explicit SAT construction or end-to-end recursive runtime is inferred from this control.
