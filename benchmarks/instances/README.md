# Current benchmark instances

The canonical tiny CNF cases are defined in `rcp_qi_research.sat_benchmark._cases` until a larger instance library justifies a separate parser and stable data format. They include the handover formula, a unique case without initial unit clauses, a multiple-solution case, and zero-solution cases with and without units. The offline solution-count audit labels outcomes and is never passed to oracle construction or iteration scheduling.

New benchmark families should include generation seed, clause list, variable convention, provenance, expected solution-count category, and reasons a classical solver may find them easy. Avoid selecting only instances with favorable quantum outcomes.
