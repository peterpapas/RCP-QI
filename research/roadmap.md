# Research roadmap

| Version | Scientific question | Current state |
| --- | --- | --- |
| V0 | What would an exact ideal partition oracle imply? | Conceptual control only; never a speedup result |
| V1 | Does one Grover iteration bias the correct half? | Formula derived and numerically validated |
| V2 | Can more iterations or a partition-local reflection reduce full cost? | Standard sweep and local-reflection negative control complete |
| V3 | Does a partition register add readable information? | Initial reduced-state and kickback controls complete; no added advantage |
| V4 | Can SAT constraints improve a costed quantum oracle? | Clause-built controls, preprocessing, and DPLL comparison complete; hard families pending |
| V5 | Can mathematical structure guide adaptive partitions? | Initial classical PySAT partition control across seven heuristics and eleven case templates, three seeds; no quantum advantage observed or asserted |
| V6 | Can recursion achieve end-to-end accuracy efficiently? | Initial confidence/restart benchmark complete under unique promise |

Priority next work: scale independently generated structured families, add dedicated GF(2) and implication-graph controls, compare SAT Competition instances with direct CDCL, and specify a certified structural property before designing a reversible operator. Any operator must be compared with quantum backtracking and amplitude amplification with complete oracle/gate/shot costs. V5 already includes zero/multiple/unique outcomes, but only at small sizes. Keep failed runs and negative findings visible.
