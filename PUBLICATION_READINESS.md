# Public repository publication audit

Audit date: 26 November 2026. Scope: the path-filtered public copy at `peterpapas/RCP-QI`, derived from the closed V1–V10 research archive. The author authorised public release and the documented licenses. This audit concerns publication readiness and does not reopen the research programme.

## Findings

| Area | Review and disposition |
| --- | --- |
| Scientific claims | The README states the absence of a P versus NP proof, demonstrated quantum advantage, universal SAT impossibility theorem and independently accepted novelty. V8's VP–VNP source claims remain explicitly conditional/unaccepted. The final report, theorem catalogue and negative-results catalogue retain the restricted models and caveats. |
| Historical results | `results/` and `results/manifest.json` were carried over byte for byte. The SHA-256 archive verifier checks all 38 manifest-indexed artifacts. The public release adds no experiment and does not alter historical raw data. |
| Authorship and ownership | Reachable Git commits name one author, Peter Papas. That is provenance evidence, not a complete legal ownership guarantee. The author authorised release of the original work. External papers, software and benchmark submissions are not relicensed. |
| Third-party benchmarks | The SAT Competition 2025 [downloads page](https://satcompetition.github.io/2025/downloads.html) publicly offers the instances, but it does not state redistribution rights for the individual submitted CNFs. Two `.cnf.xz` files were removed from **every public Git commit**. Their source URLs and SHA-256 checks remain in the [benchmark instructions](benchmarks/instances/satcomp2025/README.md); `scripts/fetch_public_benchmarks.py` downloads them locally if needed. |
| Dependencies | Python packages are pinned by `uv.lock`; Lean is pinned by `formal/lean/lean-toolchain`. Python and Lean dependencies are installed from their upstream distributions and are not vendored. Direct Python package metadata identifies Apache, BSD or MIT-style terms among the major dependencies; users must follow each dependency's own license. |
| Licensing | Original code and Lean source use [Apache 2.0](LICENSE); original research prose and generated figures/tables use [CC BY 4.0](LICENSE-DOCS). [LICENSING.md](LICENSING.md) defines the boundary. The official Apache and Creative Commons legal texts were obtained from their respective publishers. |
| Secrets | Gitleaks v8.30.1 scanned the public copy's reachable Git history with redaction; no leaks were reported. A filename check found no tracked credential, private-key or environment files. This is a bounded scan, not a guarantee against every sensitive datum. |
| Commit audit trail | The [public-history map](PUBLICATION_PROVENANCE.md) translates pre-filter commit hashes cited by old research notes to their public equivalents. The local original archive remains unchanged. |
| Cross-platform integrity | Git checkout on Windows initially converted the pinned `results/manifest.json` to CRLF and failed its byte-level SHA-256 check. An exact `.gitattributes` LF rule restores the already-committed manifest bytes without altering the historical Git blob or integrity inventory. |
| Readability | Root README gives the status, research boundaries, entry points and reproduction path. Root theorem, negative-results and roadmap indexes lead to the authoritative consolidated archive. `papers/` points to the final report and labels the LaTeX draft unpublished. |

## Reproduce the validation

Run from the repository root with Python 3.12 and uv:

```powershell
uv sync --locked
uv run python scripts/fetch_public_benchmarks.py  # optional third-party input check
uv run ruff check src tests scripts
uv run pytest -q
uv run python scripts/validate_results.py
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_pilot_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_heldout_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_large_controls_20261126
uv run python scripts/verify_archive.py
```

Then run from `formal/lean`:

```powershell
lake build
lake env lean RCPQI/AxiomAudit.lean
```

The archived [reproducibility record](research/archive/RCPQI_REPRODUCIBILITY.md) lists pinned versions and the limits of these checks. The public CI workflows run Python and Lean validation separately. Historical experiment wall times and every UNSAT claim were not independently reproduced at publication. A successful Lean build verifies its formal statements, not the surrounding complexity-theoretic claims.

**Local publication check:** 65 tests passed with the two source-verified CNFs downloaded; Ruff passed; result and all three V5.1 saved-run validators passed; `verify_archive.py` confirmed 38 artifact hashes, the manifest hash, 47 Lean theorem entries and 76 README/archive links; Lean built 34 jobs and the axiom audit printed only expected standard Lean dependencies. `cffconvert --validate` accepted `CITATION.cff`. The benchmark download verified both compressed SHA-256 digests. A fresh checkout preserved the pinned LF manifest hash. No historical raw result was edited.

## Release conclusion

The repository is fit for public mathematical review as a transparent research archive. The project status remains **SUSPENDED — PENDING NEW MATHEMATICAL INSIGHT**. No V11, new quantum operator, preprint or peer-reviewed novelty claim is part of this release.
