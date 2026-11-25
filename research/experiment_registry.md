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
