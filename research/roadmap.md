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
| V7 | Which efficiently certified transformations can reveal useful information? | Completed theorem-driven screen: one-query classical complement witness, quotient factorization equivalence, semantic-symmetry certification reduction, Walsh counterexample and original-source review; no operator passed the gate |
| V8 | Does a property-derived quantum operator beat matched baselines? | Deferred until a mathematically justified mechanism has a full cost bound and falsifiable advantage; no implementation justified |

Primary next work: test the mathematical premises in `research/v7_mathematical_review.md`: can a relation be efficiently discovered and certified on a genuinely hard family, and does its quotient/residual verifier retain structure beyond generic search? Challenge the recursive architecture and seek stronger equivalence or impossibility statements if no mechanism survives. V5.1 follow-up, if needed, requires pre-registered independent seeds, longer matched limits and a nonselected public sample; do not tune prefixes without a new mathematical reason. Any eventual operator must be compared with quantum backtracking and amplitude amplification with complete oracle/gate/shot costs. Keep negative results visible.
