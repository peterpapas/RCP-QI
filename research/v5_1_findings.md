# V5.1 extended structural partitioning: held-out findings

**Status:** completed classical benchmark, 26 November 2026. The protocol and method plan were set before the held-out seeds. The pilot (seed 101) contains 51 cases and 351 method runs. The main held-out matrix (seeds 2001 and 2002) contains 163 cases and 1,155 method runs: 622 SAT, 380 UNSAT, and 153 timeouts. A separate held-out tractable/symmetry extension at 1,024 and 2,048 nominal variables contains 20 cases and 104 method runs: 51 SAT, 40 UNSAT, and 13 timeouts. All completed SAT witnesses were checked against the original clauses. No large exhaustive solution-count audit was used.

## Question and analysis rule

The comparison is **classical SAT self-reduction**, not a quantum experiment. Every method has a two-second post-setup limit and a 512 MiB sampled RSS limit. Timeouts stay in completion plots and incur a four-second PAR2 penalty. Paired timing comparisons include only cases on which both methods completed; candidate-only and baseline-only completions are reported separately. SAT-only paired comparisons assess branch choices: an UNSAT formula is decided at the root, before choosing a variable. A greater than 5 ms paired difference is treated as a timing win/loss to reduce noise from Windows polling granularity. Distinct CNF hashes, rather than duplicated deterministic control instances, determine the number of independent formulas for uncertainty estimates. The 95% completion intervals are Wilson intervals; with two seeds they remain wide.

## Crossover analysis

At 256-variable random 3-SAT, occurrence scored a median 0.38 times prefix time on **three** paired satisfiable formulas and was faster by over 5 ms on two. Connectivity had a median ratio of 0.39 and residual scoring 0.47. The same occurrence runs took a median **5.06 times direct Glucose4 time**. One easy 3.8-ratio formula reversed the prefix comparison because scoring cost exceeded the solver work saved. On a 4.25-ratio formula, prefix took about 1.25 s, occurrence about 0.48 s (including about 0.12 s of scoring), and direct Glucose4 about 0.10 s. This is a local crossover against an arbitrary prefix rule, not against direct modern SAT solving.

Across 95 paired satisfiable cases, occurrence beat prefix by over 5 ms on 3 and lost on 40; it produced no completed result where prefix timed out. Prefix had no greater than 5 ms win over direct Glucose4 in its 95 paired SAT cases. At 512 variables, direct Glucose4 completed 1/6 random 3-SAT cases and CaDiCaL 2/6; prefix and the measured adaptive partition strategies completed 0/6. Planted 3-SAT at 512 had 0/2 Glucose4 and partition completions, whereas CaDiCaL completed 2/2. Censored observations under this short limit cannot establish asymptotic ordering or rule out a later crossover.

## Family-specific outcomes

| Family | Observation | Interpretation |
| --- | --- | --- |
| Random 3-SAT near transition | Occurrence/connectivity help prefix on two of three completed 256-variable SAT formulas; 512-variable cases largely time out. | A potentially useful **classical branch heuristic** in the recursive architecture; no advantage over direct CDCL was observed. Clause density and solver conflicts are exploratory predictors only. |
| Planted 3-SAT | Direct CaDiCaL completed both 512-variable cases; all tested recursive methods timed out. | A planted witness does not make the partition protocol competitive under this budget. |
| Graph coloring | Direct solvers completed all 128–512-variable encodings. Occurrence and connectivity also completed, but scoring grew; propagation lookahead completed only 2/4 per size. | Structural scoring overhead dominated these sparse/forced-`K4` encodings. These are not a broad graph-coloring challenge set. |
| Pigeonhole UNSAT | All compared methods timed out at nominal sizes 128, 256 and 512. | Root UNSAT dominates; a branching heuristic never gets used. Encoding validity supplies a mathematical UNSAT argument, but no independently checked general proof trace was produced. |
| Exact variable-swap symmetry | Direct CDCL completed through 2,048 variables. Symmetry scoring timed out from 128 onward and occurrence timed out at 2,048; certified symmetry breaking completed 1/2 at 2,048. | Detecting/using this supplied symmetry did not repay its classical cost. These pair gadgets are easy for CDCL. |
| XOR-SAT and 2-SAT | Direct CDCL and dedicated GF(2)/SCC algorithms completed all cases through 2,048. Some occurrence runs timed out at 1,024–2,048. | Polynomial tractable controls expose avoidable scoring overhead. Native XOR equations give Gaussian elimination a representation advantage over CNF-only baselines. |
| Public SAT Competition 2025 | On one SAT and one UNSAT instance, CaDiCaL completed in about 1.69 s and 0.64 s; Glucose4 and the prefix/occurrence probes timed out. | Only two selected stress cases; neither is representative of the competition. The public UNSAT result has no independently checked certificate in this run. |

Posthoc independent tractable-family certificate checks cover 28 held-out zero-control instances and 8 larger controls. They reconstruct contradictory XOR equation combinations or opposite implication paths. SAT witnesses were verified directly. Generated pigeonhole and forced-`K4` UNSAT claims rely on the generator construction and agreement of completed solvers; public UNSAT is only a CaDiCaL verdict.

## Resource and inference limits

Raw JSONL retains per-method wall and algorithm time, worker setup/generation estimates, preprocessing/scoring time and clause visits, solver calls, decisions, conflicts, propagations, restarts, sampled peak RSS, partition depth, log2 search-space reduction, witness hashes, failures and timeouts. The plots show PAR2 scaling, completion and memory. A warm worker executes methods in fixed order; setup is recorded separately, but process-cache effects, 10 ms memory sampling, a 2 s cap, two held-out seeds and Windows timing granularity limit small time differences. The public cases were selected as stress controls, not randomly sampled. No Qiskit simulation or quantum circuit estimate is commensurate with these classical timings.

## V7 implication

The measured 256-variable improvement came from classical variable selection and reduced CDCL work inside self-reduction. It offers no partition observable unavailable to a direct classical solver. V7 should search for a **certifiably discoverable relation** among residual subproblems, with its own detection and reversible implementation cost, and test whether a coherent use improves on direct CDCL, dedicated polynomial algorithms where applicable, and quantum backtracking. The current results do not justify V8 operator implementation. A follow-up intended to test a crossover should pre-register more independent random seeds, longer matched limits, solver versions/order, and a larger nonselected public sample before interpreting scaling.

Reproduce and validate with the commands in [the protocol](../experiments/v5_1_extended/README.md). Machine-readable results and plots are indexed by [the manifest](../results/manifest.json).
