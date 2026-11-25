# Known limitations

- All quantum runs use ideal, noiseless simulators. No hardware routing, noise, fault-tolerant gate synthesis, physical latency, or energy cost is measured.
- Equality targets are embedded in toy oracle circuits; this is not a realistic database loading scheme.
- CNF cases are tiny and structurally easy. DPLL and unit propagation are educational baselines, not modern competitive SAT solvers.
- Some probability checks use exact statevectors, which are not obtainable from a single physical measurement. Shot frequencies have substantial uncertainty at small sample sizes.
- The fixed-iteration threshold search proves a minimum only within its stated identical-shot/majority or verified-candidate protocol family. It is not a lower bound for all quantum algorithms.
- The adaptive recursive confidence guarantee assumes exactly one solution, ideal calibrated Grover probabilities, and independent shots. It does not establish a practical advantage.
- Lean proves abstract partition facts. It does not verify Qiskit circuits, Python resource counters, the unstructured-search lower bound, or any polynomial-time quantum algorithm.
- The paper scaffold is unpublished. No final license, DOI, external affiliation, or publication claim has been assigned.
