# Final reproducibility and integrity audit

**Status:** SUSPENDED — PENDING NEW MATHEMATICAL INSIGHT. Audit date: 26 November 2026, Windows PowerShell, Australia/Sydney. This is a verification of the committed archive and recorded checks, not a rerun of every historical statevector, shot or SAT benchmark. The pre-closeout research head was `536cc3c605d51a133e873228342add9d433d4557`; the final closeout revision is the Git commit containing this document. The final `git status --short` must be empty.

## Pinned environment and provenance

| Item | Recorded state |
| --- | --- |
| Python / package manager | Python `3.12.10`; uv `0.12.5`; `uv sync --locked` uses committed `uv.lock`. |
| Key packages | Qiskit `2.6.2`, Qiskit Aer `0.18.4`, NumPy `2.5.5`, SciPy `1.18.1`, Matplotlib `3.11.2`, PySAT `1.9.dev25`, pytest `9.2.0`, Ruff `0.17.6`. Read `uv.lock` for the full transitive graph. |
| Lock digest | `uv.lock` SHA-256 `C222085FC83F9DC555690109E84EAD8A31D8649F58E23C8F44A6BD7638FFFD37`. |
| Formal toolchain | `formal/lean/lean-toolchain` pins `leanprover/lean4:v4.36.0`; `lake-manifest.json` is committed. No Mathlib project dependency was added. |
| Historical source commits | V7 `79d29f9`; V8 source review `3649594`; V8 Lean `db3a6c3`; V9 formal/analysis/registry `9fbcd8a`, `51f667d`, `331d06e`, `3e3ff14`; V10 formal/analysis/registry `ee275a8`, `257454d`, `536cc3c`. Use full Git history for authorship and exact timestamps. |
| External 2026 VP–VNP artifacts | Anthropic `anthropics/formal-math` `11b6c7e3c927df2658f513b6b68ea7f8929c62c5`; OpenAI `openai/math` `3344da59991ed94f9ba711217b29c1d760badfa6`. [V8 source audit](../v8/V8_SOURCE_VERIFICATION.md) records statement/axiom/build limits; independent mathematical acceptance was **not** established. |
| Result index | `results/manifest.json` SHA-256 `F3D7DC93DB0BBFBD99A9EB6F48533C95F4A4784B94901347CD5CC67991AA9099`, with V1–V10 registry IDs. Closeout adds no new experiment entry or raw result. |

## Final verification commands

Run from the repository root unless stated otherwise. These checks are read-only with respect to historical raw results; `uv sync --locked` may populate `.venv` as usual.

```powershell
uv sync --locked
uv run ruff check src tests scripts
uv run pytest -q
uv run python scripts/validate_results.py
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_pilot_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_heldout_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_large_controls_20261126
uv run python scripts/verify_archive.py
git diff --check
git status --short
```

From `formal/lean`:

```powershell
lake build
lake env lean RCPQI/AxiomAudit.lean
```

On this host, `lake` is available at `~/.elan/bin/lake.exe` if not on `PATH`. The axiom audit checks the printed dependencies of named theorems. Standard Lean `propext`, `Classical.choice` or `Quot.sound` occur on some theorems; no custom project axioms or unfinished proof holes are permitted. A successful Lean build establishes only the formal statements, not their correspondence to a physical circuit or an externally cited complexity theorem.

## Artifact integrity and independent certificate check

`scripts/verify_archive.py` compares the byte count and SHA-256 of **all 38** raw, processed and figure paths indexed by `results/manifest.json` against the once-created [immutable inventory](artifact_integrity.json), and verifies the manifest digest. It also checks coverage of all **47** named Lean theorems in the catalogue and resolves local links in the README/archive notes (**59** at closeout). Theory/source files are versioned by Git and are outside the data hash scope. The inventory includes the V1 one-iteration and V2 probability records, V3/V4/V5/V6 data, V5.1 pilot/held-out/large-control JSONL, processed analyses, certificates and figures. It does not claim those experiments were physically rerun at closeout.

At closeout, `scripts/validate_v51.py` passed for the pilot, held-out and large-control directories. `scripts/certify_v51.py` independently regenerated **28** held-out and **8** larger-control tractable XOR/2-SAT UNSAT certificates into uniquely named temporary files; both outputs matched the committed certificate JSONL files **byte for byte** by SHA-256. The temporary files were removed. This verifies the deterministic generator/digest/certificate path for these controls, not unsatisfiability of every public or hard random instance. V5.1 SAT witnesses were directly checked in its existing validator; no exhaustive large-instance solution-count audit was performed. The two public SAT files were stress controls, not a representative corpus, and no independent public UNSAT certificate exists in this archive.

## Limits of reproducibility

Result validation checks schema, saved V1/V2 analytic-statevector agreement and V1–V6 accounting, plus V5.1 run completeness/known promises. It cannot prove that a simulator represents real hardware, independently verify every arbitrary UNSAT outcome, reproduce historical Windows wall times or establish asymptotic scaling. Re-running old experiment CLIs in the repository could replace historical files; **do not do that**. If an independent investigator wants a fresh replication, use a separate Git worktree/output directory and the original commands/seeds in each immutable [registry entry](../experiment_registry.md), record new dependency/platform versions, and give the run a new ID. Never overwrite archived data or call a new run V11.

## Closeout check record

The final run results, including test count, Ruff, Lean build, axiom audit, result validation, V5.1 validators and archive hash check, are recorded in [the final report](RCPQI_FINAL_RESEARCH_REPORT.md) and the Git closeout commits. There are no outstanding validation failures or intentional raw-data edits.

The post-commit repository audit found an empty `git status --porcelain`; `git diff --check 536cc3c..HEAD` passed, and the changed-path list contained only the closeout documents, index, verifier and README/registry/roadmap links. `git fsck --connectivity-only --no-reflogs` exited successfully and reported one **dangling, unreferenced blob** (`62202814c89a529647ad3c09c610225d3e635c2c`), which does not affect reachable committed objects or the verified historical artifacts. It was left untouched to preserve repository history.
