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
| V7.1 | Can a weaker structural promise retain a hard residual and support a distinct quantum advantage? | Completed promise taxonomy, original-source comparison and Lean local-complement/residual/MQ-gadget results; no candidate passes the V8 gate |
| V8 | Do November 2026 VP–VNP claims transfer to RCP-QI or reveal a costed quantum structural mechanism? | Theory/source-audit round complete: authentic public claims, independent proof acceptance unresolved; formal-polynomial to Boolean/quantum transfer fails without new model-preserving theorems; no new circuit authorized; decision D |
| V9 | Which symbolic, Boolean-ideal and quantum-query obstructions survive a precise model? | Theory round complete: perfect-matching CNF gives permanent as full symbolic output but polynomial-time partition decisions; Boolean-equivalent formal expressions can have different raw measures; unique-marker half extraction has `Θ(√N)` black-box queries; compressed arithmetic lower bound remains conditional; decision D |
| V10 | Can Boolean-invariant certificates yield a meaningful explicit-SAT bound or quantum advantage? | Bounded theory screen complete: distributed unit-CNF is known disjointness; original-clause conflict trees simulate tree-like resolution; Lean checks Boolean reductions/soundness; no novel theorem or operator survives; decision D to suspend active development |

Active RCP-QI theorem and circuit development is suspended after V10's bounded novelty screen. A restart requires a precise original theorem proposal, an efficiently obtainable explicit-input certificate, a model-preserving lower-bound or algorithmic reduction, and independent prior-art review. V1–V9 experimental history remains available for reproducibility. Do not import either VP–VNP claim as independently accepted without semantic review, and do not relabel Simon/Shor/hidden-shift oracle controls as SAT algorithms. Generic recursive partition tuning and quantum operator implementation remain suspended.
