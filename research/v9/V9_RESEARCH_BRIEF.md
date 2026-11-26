# V9 research brief — 26 November 2026

## Baseline and question

V1–V3 and V6 found no unstructured recursive quantum advantage. V5.1 found no observed crossover over direct CDCL within its seeds and budgets. V7/V7.1 found no justified structural quantum operator. V8 authenticated public Anthropic/OpenAI VP–VNP *claims* but did not establish independent acceptance or a transfer to SAT/quantum computation. Its recommendation D motivates this theory-only round. Historical artifacts remain unchanged.

V9 asks which lower bounds survive (i) specifying the output of a symbolic partition procedure, (ii) Boolean equivalence modulo `x_i²−x_i`, and (iii) coherent phase-oracle access. No new quantum circuit or empirical speedup is attempted.

## Work sequence and decision gates

1. Define input, field, output, size, uniformity and cost in [the symbolic model](V9_SYMBOLIC_PARTITION_MODEL.md).
2. Prove an explicit permanent identity and separate full polynomial generation from perfect-matching existence.
3. Establish the Boolean quotient and inspect candidate invariants under it.
4. Bound unique-marker partition-label extraction in the black-box query model, then audit transfer limits.
5. Formalise narrow interpolation, phase-sign and quotient-transcript lemmas in Lean; record unformalised dependencies.
6. Compare against original sources and decide on publication or further theorem work.

Gates 1–4 are resolved separately in the [final report](V9_FINAL_REPORT.md). Gates 5–6 remain conservative: a correct synthesis is not automatically novel, and no constructive operator passes the existing design gate.
