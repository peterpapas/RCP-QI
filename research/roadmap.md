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
| V5.1 | Does structural partitioning cross over on larger/harder families? | Completed pilot, held-out 8–512 study and 1,024/2,048 tractable controls; local gain over prefix at 256-variable random 3-SAT, no observed gain over direct CDCL; see findings and immutable registry |
| V7 | Which efficiently certified structural promises can support a useful partition observable? | Conditional Lean pair/cost theorems and property-to-operator screen documented; no nontrivial mechanism identified |
| V8 | Does a property-derived quantum operator beat matched baselines? | Gated on a precise property, reversible construction and full resource bound; no implementation justified yet |

Priority next work: pre-register more independent seeds, longer matched time limits and a nonselected public benchmark sample to test the possible crossover without extrapolating from two seeds. V7 should seek a polynomially certified partition property with a reversible implementation before any V8 circuit. Any operator must be compared with quantum backtracking and amplitude amplification with complete oracle/gate/shot costs. Keep failed runs and negative findings visible.
