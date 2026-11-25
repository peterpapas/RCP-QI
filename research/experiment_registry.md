# Experiment registry

Every entry uses an immutable ID. Machine-readable raw files and figures are indexed in `results/manifest.json`. Timings are platform-dependent. A new experiment should record its seed, dependency lock, input family, mathematical assumption, baseline, costs, uncertainty, reproduction command, and negative findings before a conclusion is drawn.

## V1-BASELINES

- **Hypothesis:** Measured recursive Grover partition tests may find a unique solution with competitive resource use.
- **Assumptions and inputs:** Unique-solution equality searches, `n=2..4`, plus two three-variable CNFs. Four stratified/seeded trials per case.
- **Methods and baselines:** Classical exhaustive search, full-space Grover, and prefix-recursive measured Grover; ideal Aer statevector with one-shot execution and verified candidates.
- **Expected/actual:** A bounded-error partition decision can fail. At `n=2`, RCP-QI succeeded in 3/4 trials; it used more total predicate calls than Grover in the saved small cases.
- **Costs and uncertainty:** Raw JSON records phase calls, verification calls, preparations, measurements, transpiled gates/depth, time, and Wilson intervals. Four trials are too few for a scaling claim.
- **Reproduce:** `uv run rcp-qi-research --seed 20261125 --trials 4 --max-n 4 --repetitions 3`.
- **Follow-up:** Exact one-iteration probability and confidence-controlled traversal.

## V1-ONE-ITERATION

- **Hypothesis:** One Grover iteration biases measurement toward the correct half.
- **Assumptions and inputs:** One marked equality target; `N=4..256`, both endpoint target positions.
- **Expected/actual:** (P_{\rm half}=1/2+4/N-8/N^2); exact statevector values agree within machine precision. Bias decays with `N`.
- **Costs and uncertainty:** One phase oracle per circuit; circuit gates/depth and simulation time saved. Statevector results are exact probabilities, not finite-shot observations.
- **Reproduce:** `uv run rcp-qi-research` writes `results/one_iteration.json` and a figure.
- **Follow-up:** Sweep iterations and count repeated-shot costs.

## V2-MULTI-ITERATION

- **Hypothesis:** Multiple standard Grover iterations may make the correct half reliable with fewer total calls than exact-solution Grover.
- **Assumptions and inputs:** One marked equality target, `N=4..256`, both half boundaries and seeded positions; two seeded 256-shot samples per selected circuit.
- **Methods and baselines:** Analytic full-space Grover curves, exact statevector validation, partition-bit majority, verified-candidate Grover. Fixed-iteration threshold protocols are exhaustively cost-minimized under a feasible bound.
- **Expected/actual:** Half accuracy is algebraically tied to exact-solution probability. At `N=256`, 90/95/99% one-shot half thresholds take 9/10/11 phase calls. No asymptotic advantage over Grover is indicated.
- **Costs and uncertainty:** Separate phase, verification, shots, state preparation, transpiled gates/depth, simulator time. Exact numerical discrepancy below `6e-14`; seeded frequencies fluctuate. Protocol minimum is not a universal lower bound.
- **Reproduce:** `uv run rcp-qi-phase2 --min-n 2 --max-n 8 --seed 20261125 --shots 256 --sample-seeds 2`.
- **Follow-up:** Test partition-local reflections and explicit registers.

## V3-PARTITION-REGISTER-CONTROL

- **Hypothesis:** A partition-local diffuser or dedicated ancilla may expose extra correct-half information.
- **Assumptions and inputs:** Unique equality target in either half, `N=4..64`, zero/one/near-peak iterations, ideal statevectors.
- **Methods and baselines:** Full diffuser, partition-bit diffuser, oracle-only control; ancilla label before/after Grover and phase-kickback control.
- **Expected/actual:** Local diffusion and oracle-only controls leave half probability at `1/2`; an ancilla labeled before data-only operations has zero left/right trace distance. Labeling after exposes exactly the existing bias.
- **Costs and uncertainty:** JSON stores density matrices, trace distances, phase calls, qubits/ancillas, transpiled gates/depth, simulator time. No shot uncertainty; these are ideal statevectors.
- **Reproduce:** `uv run rcp-qi-register --min-n 2 --max-n 6`.
- **Follow-up:** Specify a new constraint-dependent interaction before claiming a register advantage.

## V4-STRUCTURED-SAT-CONTROL

- **Hypothesis:** Clause structure and classical preprocessing may reduce search cost on stated SAT families.
- **Assumptions and inputs:** Five small CNFs with unique, multiple, and zero solutions; four seeds and 12 quantum attempts per case. Audit solution counts are offline labels, never oracle construction inputs.
- **Methods and baselines:** Reversible clause-built CNF oracle, unknown-count randomized Grover schedule, unit propagation, DPLL, exhaustive search, and clause-parity negative control.
- **Expected/actual:** Unit propagation alone solves the handover instance. DPLL solves all cases in one to three nodes. Bounded quantum failure on a zero-solution instance is inconclusive, not an UNSAT proof.
- **Costs and uncertainty:** Separate complete-verifier phase calls, clause-phase calls, classical literal checks, shots, gates/depth, and elapsed time; tiny cases preclude general conclusions.
- **Reproduce:** `uv run rcp-qi-sat --seed 20261125 --trials 4 --max-attempts 12`.
- **Follow-up:** Harder benchmark families and competitive modern SAT solvers.

## V6-RECURSIVE-BENCHMARK

- **Hypothesis:** Per-level confidence budgets and bounded restarts can control end-to-end errors without hiding costs.
- **Assumptions and inputs:** Unique equality targets, `N=4..32`, three targets and three seeds per confidence group where distinct, 90/95/99% requested per-run confidence.
- **Methods and baselines:** Implicit-prefix measured Grover probes, union-bound shot budgets, at most two restarts, final candidate verification, full-space Grover comparator.
- **Expected/actual:** Failed first runs can be recovered, but all their costs remain. The seeded data had one wrong decision and one failed first run; mean recursive predicate calls exceeded Grover in every saved group.
- **Costs and uncertainty:** Query/gate/depth/time and restart totals, offline per-level decision audit, Wilson intervals. Small empirical groups can deviate from ideal confidence predictions.
- **Reproduce:** `uv run rcp-qi-recursive --min-n 2 --max-n 5 --seed 20261125 --trials 3 --max-restarts 2`.
- **Follow-up:** Multiple/zero-solution handling and adaptive partitioning from structure.

## V5-STRUCTURAL-PARTITION-CONTROL

- **Hypothesis:** Clause structure can guide the choice of branching variable in SAT self-reduction; any resulting benefit must be charged to classical preprocessing unless a distinct quantum mechanism is demonstrated.
- **Inputs:** Eleven clause-built cases per seed, seeds `20261126..20261128`: XOR-chain SAT (unique/multiple/zero), implication-chain 2-SAT (unique/multiple/zero), planted and random 3-SAT with `n=8,m=34`, 3-colorable triangle and non-3-colorable `K4`, and four independent symmetric variable pairs. All `2^n` assignments are evaluated offline only to label solution counts, never to select branches.
- **Methods:** Prefix, occurrence, clause-connectivity, unit-propagation lookahead, exact variable-swap symmetry scoring, residual clause score, and two-sided Jeroslow–Wang score. Each makes an initial PySAT Glucose4 existence call and one incremental assumption call for `v=0` per free variable, then verifies the full candidate. Direct Glucose4 solving and the existing DPLL are controls. Zero-solution cases receive a solver UNSAT verdict, cross-checked by offline exhaustive audit; no proof certificate is produced. This is a **classical** partition benchmark; no quantum operator or oracle is used.
- **Costs:** Raw JSON gives solver calls, internal decisions/conflicts/propagations/restarts, clause scans, lookahead literal checks and assignments, construction/scoring/solver/total wall times, and final verification. The plot compares SAT calls and internal decisions with direct solving. Simulator time and quantum gate counts are inapplicable to this control.
- **Observed:** All 33 cases agree with exhaustive offline labels. Direct Glucose4 uses one call; partition self-reduction uses `n+1` calls on satisfiable inputs. For planted 3-SAT, mean internal decisions over three seeds are `6` direct, `18.33` prefix, and `16` for occurrence/Jeroslow–Wang. For the random 3-SAT generator, they are `6.33`, `19`, and `19`, respectively. Lookahead gives `17.67` on the random group but incurs extra classical propagation. The symmetry scorer selects a variable; it does not construct a quotient or improve these symmetric cases. Timings at this size are too small and noisy for a scaling conclusion.
- **Reproduce:** `uv run rcp-qi-structural --seed 20261126 --seed-count 3`. The version lock is `uv.lock`; solver is PySAT Glucose4.
- **Limitations/follow-up:** These hand-sized families are controls, not representative hard instances. Add scalable family generators and larger independent seeds, a dedicated GF(2) solver and implication-graph 2-SAT baseline, SAT Competition instances and quantum backtracking before any performance claim. No structural quantum operator meets the stated operator gate yet.

## V5.1-EXTENDED-STRUCTURAL-PARTITIONING

- **Immutable ID/status:** V5.1-EXTENDED-STRUCTURAL-PARTITIONING, completed 26 November 2026. Raw pilot, main held-out and larger-control directories are append-only artifacts indexed in `results/manifest.json`; later runs need a new ID or output directory.
- **Hypothesis:** On harder SAT families, structure-aware branching might offset its scoring cost and outperform arbitrary prefix self-reduction or direct CDCL. This tests a classical control, not a quantum algorithm.
- **Inputs and split:** Pilot seed 101 (51 cases, 351 method runs); held-out seeds 2001/2002 (163 cases, 1,155 method runs), nominal 8–512 variables. A separate held-out extension has 20 cases, 104 method runs at 1,024/2,048 variables for XOR, 2-SAT and symmetry. Random 3-SAT ratios 3.8/4.25/4.6, planted 3-SAT, sparse and forced-`K4` 3-coloring, pigeonhole UNSAT, exact swap symmetry, unique/zero XOR and 2-SAT controls, and two official SAT Competition 2025 files are specified by generators/catalog hashes. Some deterministic controls duplicate across seeds and are counted once for independent-formula uncertainty.
- **Baselines:** Direct PySAT Glucose4 and CaDiCaL 1.9.5, the existing simple DPLL for `n≤32`, prefix self-reduction, all seven V5 selectors where applicable, certified known-swap symmetry breaking, dedicated GF(2) elimination and 2-SAT SCC. All methods have a two-second post-setup limit and 512 MiB sampled RSS cap. Public-instance partition probes stop after 16 bits and cannot count as a solution. No quantum operator was run.
- **Accounting:** Raw JSONL retains all SAT/UNSAT/timeout outcomes, wall/algorithm/setup/generation and scoring time, clause visits, SAT calls and internal decisions/conflicts/propagations/restarts, sampled memory, depth, log2 space reduction and direct witness verification. SAT witnesses are checked against CNF; no exhaustive large-instance count is performed. Independently checked XOR and 2-SAT contradiction certificates cover 28 main held-out and 8 larger zero-control instances. No independently checked public UNSAT certificate was obtained.
- **Observed:** Main held-out has 622 SAT, 380 UNSAT and 153 timeout method records; larger controls have 51 SAT, 40 UNSAT and 13 timeouts. On three completed satisfiable 256-variable random 3-SAT formulas, occurrence versus prefix median time ratio is 0.38 (two wins above 5 ms); versus direct Glucose4 it is 5.06. Across 95 paired satisfiable cases, occurrence has 3 wins and 40 losses above 5 ms versus prefix and no candidate-only timeout resolution. At 512-variable random 3-SAT, direct Glucose4 completed 1/6 and CaDiCaL 2/6, while tested recursive methods completed 0/6. The direct/dedicated tractable controls completed through 2,048 variables. A crossover over prefix appears locally; no crossover over direct CDCL is supported.
- **Uncertainty and limitations:** 95% Wilson intervals are recorded but broad with two seeds; paired analysis retains timeout counts and PAR2 penalties. Small elapsed times have Windows polling granularity; fixed warm-worker order, sampled RSS and two-second censoring limit extrapolation. The two selected public files are stress controls, not a representative sample. The fixed generator promises and tractable-family representations do not imply general 3-SAT speedup.
- **Reproduce:** `uv sync --locked`, then commands in `experiments/v5_1_extended/README.md` using fresh output directories; validate with `scripts/validate_v51.py`, analyze with `scripts/analyze_v51.py`, and check tractable UNSAT certificates with `scripts/certify_v51.py`. Inputs, raw files, analysis and figures are indexed by `results/manifest.json`; dependencies are locked by `uv.lock`.
- **Conclusion/follow-up:** The 33-case V5 result was too small to characterize local prefix improvements: V5.1 finds some. The recursive architecture still pays root plus per-bit SAT calls and has not beaten direct CDCL on these data. See `research/v5_1_findings.md` for family conclusions and V7 recommendations. No V8 operator is justified.
