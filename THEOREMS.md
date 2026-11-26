# Mathematical theorem catalogue

The [V1–V10 catalogue](research/archive/RCPQI_THEOREM_CATALOGUE.md) is the authoritative index of surviving theorems, lemmas, reductions and counterexamples. Each entry states assumptions, model, proof location, Lean identifier where applicable, external dependencies, complexity scope and prior-art status.

Lean builds check the stated formal propositions. Externally cited quantum-query, communication, proof-complexity and arithmetic-complexity results have **not** been formalised by this project. No catalogue entry proves a general SAT lower bound or P versus NP result.

The named Lean statements include elementary Boolean/arithmetic identities, conditional modelling lemmas, reduction-correctness statements and restricted-model soundness. Their count is an audit index, **not** a measure of originality or theorem depth. In particular, the [partial-search prior-art bounds](research/corrections/PARTIAL_SEARCH_PRIOR_ART.md), amplitude-estimation bounds and quantum 3-SAT algorithms in the [correction review](research/corrections/SAT_AND_COMPLEXITY_PRIOR_ART.md) are external mathematical results, not Lean theorems here. [Formal-status table](theory/formal_status.md).
