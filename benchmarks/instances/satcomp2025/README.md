# SAT Competition 2025 public stress instances

The CNF files are third-party inputs and are **not included in this public Git repository or its reachable history** because the competition download page does not state a redistribution license for individual submissions. To reproduce the public-instance check, download from the official Global Benchmark Database and verify the exact compressed SHA-256 values below:

```powershell
uv run python scripts/fetch_public_benchmarks.py
```

This command stores the files locally in this directory, which is Git-ignored. The integration test skips only this optional input check if the files are absent; the public CI workflow fetches and checks them before testing. A failure to download is a source-availability issue, not evidence about the research result. The saved V5.1 raw results remain committed and unchanged.

Both files were downloaded on 2026-11-26 from the [official SAT Competition 2025 benchmark listing](https://satcompetition.github.io/2025/downloads.html) via the [Global Benchmark Database](https://benchmark-database.de/?context=cnf&track=main_2025). They were selected by compressed availability/size and opposite listed outcomes before performance inspection. They are stress controls, not a representative random sample of the competition.

| Local file | Official GBD hash / listed result | Download URL | SHA-256 of compressed file | DIMACS size |
| --- | --- | --- | --- | --- |
| `Break_12_50.xml.cnf.xz` | `0e1d562093d5f4fc9013cf4a14a03f70` / SAT | [GBD file](https://benchmark-database.de/file/0e1d562093d5f4fc9013cf4a14a03f70?context=cnf) | `e56a8b6d9099fab4950ca38c9c759958d9d7c31ca8bc0ea78fad5238d7d67382` | 14,036 variables; 53,685 clauses |
| `s38417.cnf.xz` | `09cd83e233380d0ba1fc56cee88367b1` / UNSAT | [GBD file](https://benchmark-database.de/file/09cd83e233380d0ba1fc56cee88367b1?context=cnf) | `03d81a900d1f6481daec12e2539de6139cc1579d7fab571ceac02ec68f8b6e99` | 20,100 variables; 50,412 clauses |

The runner verifies compressed SHA-256 and canonical CNF SHA-256 in the instance catalog. It parses `.xz` directly; no exhaustive audit is attempted. Partition traversals on these instances are capped at 16 decisions, and a partial traversal is **not** a solved result. The GBD outcome label and agreement between CDCL solvers do not constitute an independently checked UNSAT proof certificate.
