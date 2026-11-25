# V5.1 extended structural partitioning benchmark

The V5.1 protocol was fixed before the held-out run. Pilot seed `101` assesses feasibility; held-out seeds `2001,2002` are for the reported comparisons. Generated sizes are nominally `8,16,32,64,128,256,512` Boolean variables; graph-coloring and pigeonhole encodings have nearby actual counts, which are recorded. Random 3-SAT uses clause-to-variable ratios `3.8,4.25,4.6`; planted 3-SAT uses `4.25`; coloring has sparse satisfiable and forced-`K4` unsatisfiable levels. XOR and 2-SAT include unique/zero controls; symmetry has independent swappable pairs. Two official SAT Competition 2025 files are included as large stress controls.

Reproduce from the repository root (choose fresh output directories; raw runs refuse to overwrite an existing directory):

```powershell
uv sync --locked
uv run python -m rcp_qi_research.v51_benchmark --stage pilot --sizes 8,16,32,64,128,256,512 --timeout-s 2 --memory-mb 512 --output-dir results/raw/v5_1_pilot_20261126
uv run python -m rcp_qi_research.v51_benchmark --stage heldout --sizes 8,16,32,64,128,256,512 --timeout-s 2 --memory-mb 512 --output-dir results/raw/v5_1_heldout_20261126
uv run python -m rcp_qi_research.v51_benchmark --stage heldout --sizes 1024,2048 --families xor,two_sat,symmetry --timeout-s 2 --memory-mb 512 --output-dir results/raw/v5_1_large_controls_20261126
uv run python scripts/analyze_v51.py --run-dir results/raw/v5_1_heldout_20261126 --output-dir results/processed/v5_1
uv run python scripts/analyze_v51.py --run-dir results/raw/v5_1_large_controls_20261126 --output-dir results/processed/v5_1_large_controls
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_heldout_20261126
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_large_controls_20261126
uv run python scripts/certify_v51.py --run-dir results/raw/v5_1_heldout_20261126 --output results/processed/v5_1/heldout_certificates.jsonl
uv run python scripts/certify_v51.py --run-dir results/raw/v5_1_large_controls_20261126 --output results/processed/v5_1_large_controls/certificates.jsonl
```

All applicable methods receive the same **2-second post-setup method limit** and **512 MiB sampled RSS limit**. A warm isolated worker holds one instance and runs the methods sequentially; process setup and generation time are recorded separately and an independent-execution total estimate adds setup to each method. If a method times out or exceeds memory, the worker is terminated and restarted for the next method. Method order is fixed; process-cache effects and coarse Windows scheduling are limitations. The monitor samples RSS every 10 ms, so instantaneous peaks may be missed. Python `elapsed_s` includes solver construction, scoring, calls, and candidate verification; parent `wall_time_s` includes IPC and polling but excludes worker startup.

Direct Glucose4, CaDiCaL 1.9.5, simple DPLL (`n≤32`), and prefix are comparators. All seven V5 variable selectors are run on random and planted 3-SAT. Family-specific runs add a certified known-swap symmetry-breaking control, GF(2) Gaussian elimination on original XOR equations, and SCC 2-SAT solving. Those dedicated algorithms receive the richer native family representation, a deliberate representation advantage that must be considered when comparing costs. The public instances receive direct CDCL and 16-step prefix/occurrence probes; partial probes cannot be counted as solutions.

The machine-readable catalog has an instance SHA-256, actual variable/clauses/literal counts and seed. Each raw JSONL method row retains SAT/UNSAT/partial/timeout/error, method wall time, setup/generation time, sampled peak RSS, calls, cumulative CDCL decisions/conflicts/propagations/restarts, scoring time and clause visits, partition depth, log2 search-space reduction, and a hash of any directly verified witness. No large exhaustive solution counting, Qiskit simulation, or quantum advantage claim is involved. Some UNSAT labels follow generator mathematics (pigeonhole, forced `K4`, contradictory XOR/2-SAT); public UNSAT has no independently checked certificate in this run.

On a killed timeout, the worker cannot return partial CDCL counters or a reliable partition depth; the raw row retains the timeout, elapsed wall time, budget and sampled memory. Missing counters must not be interpreted as zero work. Public stress files and source hashes are documented in `benchmarks/instances/satcomp2025/README.md`.

The analysis uses two-second censoring, a four-second PAR2 penalty, SAT-only paired branch comparisons, distinct-CNF Wilson completion intervals and an exploratory (nonconfirmatory) feature screen. Plots include timeout penalties. The posthoc checker reconstructs XOR contradictory equation combinations and 2-SAT implication paths for zero controls. It does not check general CDCL UNSAT proof traces. The [findings](../../research/v5_1_findings.md) retain negative cases and limit the crossover claim to the observed paired formulas.
