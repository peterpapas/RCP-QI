# Negative results and inconclusive outcomes

1. **V1 one-iteration bias vanishes asymptotically.** The analytic correct-half advantage is (4/N-8/N^2). Repeated independent partition-bit sampling at one iteration needs order (N^2) shots for fixed confidence. See `results/one_iteration.json`.
2. **V2 full-space Grover does not give cheap partition existence.** Correct-half probability is algebraically linked to exact-solution probability; fixed-accuracy detection still takes order (\sqrt N) phase queries. The plotted small cases support this relationship, not a speedup.
3. **V3 partition-bit-only diffusion fails in tested cases.** It leaves correct-half probability at `0.5`. An ancilla copied before data-only Grover has zero left/right trace distance; copied after Grover it exposes no more than the existing data bias. See `results/phase2_partition_register.json`.
4. **V4 clause-parity phase is not a SAT conjunction oracle.** It phases odd counts of violated clauses. Occasional satisfying measurements do not make it a correct replacement. Unit propagation already solves the simplest unique instance without quantum work.
5. **V4 zero-solution quantum runs can be inconclusive.** Exhausting a finite measurement budget does not certify UNSAT. The saved zero-no-units quantum runs remain inconclusive; DPLL proves the instance unsatisfiable.
6. **V6 recursive confidence costs exceed full-space Grover in the saved tiny groups.** The benchmark retains one failed first run and all restart costs. The sample is too small for a general performance ratio.

These findings remain part of the project history. A new operator should be compared against them at matched success targets and full resource cost.
