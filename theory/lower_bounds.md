# Relevant lower bounds and scope

For unstructured search with a black-box verifier and one marked item, bounded-error quantum algorithms require (\Omega(\sqrt N)) verifier queries. Grover attains the matching order. Recursive partitioning and an extra register do not, by themselves, remove the information-theoretic obstruction.

Primary sources:

- Bennett, Bernstein, Brassard, Vazirani, [*Strengths and Weaknesses of Quantum Computing*](https://arxiv.org/abs/quant-ph/9701001) (1997).
- Zalka, [*Grover's quantum searching algorithm is optimal*](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.60.2746) (1999).
- Brassard, Høyer, Mosca, Tapp, [*Quantum Amplitude Amplification and Estimation*](https://arxiv.org/abs/quant-ph/0005055) (2002).

These black-box statements do not rule out advantage from a separately specified problem structure and costed oracle model. They do rule out treating an exact partition-existence oracle as free. A polynomial-time quantum algorithm for a genuinely NP-complete family would imply (\mathrm{NP}\subseteq\mathrm{BQP}), not necessarily classical (\mathrm P=\mathrm{NP}). No such algorithm is claimed here.
