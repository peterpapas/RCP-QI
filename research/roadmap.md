# Research roadmap

| Version | Scientific question | Current state |
| --- | --- | --- |
| V0 | What would an exact ideal partition oracle imply? | Conceptual control only; never a speedup result |
| V1 | Does one Grover iteration bias the correct half? | Formula derived and numerically validated |
| V2 | Can more iterations or a partition-local reflection reduce full cost? | Standard sweep and local-reflection negative control complete |
| V3 | Does a partition register add readable information? | Initial reduced-state and kickback controls complete; no added advantage |
| V4 | Can SAT constraints improve a costed quantum oracle? | Clause-built controls, preprocessing, and DPLL comparison complete; hard families pending |
| V5 | Can mathematical structure guide adaptive partitions? | Open; no operator or benchmark yet |
| V6 | Can recursion achieve end-to-end accuracy efficiently? | Initial confidence/restart benchmark complete under unique promise |

Priority next work: design a nontrivial structural SAT family, add a competitive SAT solver baseline, specify any proposed partition interaction before implementation, and derive complete oracle/gate/shot bounds. Extend to zero/multiple solutions before general claims. Keep failed runs and negative findings visible.
