# Complexity and cost model

An (n)-bit recursive traversal makes (n) logical partition decisions, but its total cost is (T(n)=\sum_{k=1}^{n}C(k)), where (C(k)) includes every operation needed to decide existence in a child with (2^k) candidates. The Lean theorem `totalCost_of_bounded_oracle` proves the conditional bound (T(n)\le nc) if every decision costs at most (c). It **does not** prove that such a cheap oracle exists.

The current measured partition probe uses Grover amplification. With fixed repetitions, the phase-query sum is (\sum_{j=1}^{n}O(\sqrt{N/2^j})=O(\sqrt N)), before gates, measurements, candidate verification, error-control repetitions, and restarts. A desired higher confidence can increase the repetitions. The end-to-end benchmark records actual logical oracle calls, verification calls, preparations, shots, gates, depth, failed runs, and elapsed simulator time.

Counts are not interchangeable: a reversible CNF oracle call is a composed circuit, a clause-parity phase call is a different operator, a classical DPLL literal inspection is not a quantum phase query, and transpiled `u`/`cx` gates are a basis-dependent proxy for hardware cost. Exact statevector simulation is classical and scales exponentially in qubits. Neither lower simulator time nor a smaller partition decision count establishes a quantum speedup.

For fixed confidence, the symmetric full-space Grover partition benchmark needs (\Theta(\sqrt N)) phase queries. The (O(1/N)) one-iteration partition bias needs (\Theta(N^2)) independent partition-bit samples for fixed confidence, even before recursion. The equality-oracle toy construction itself embeds the target, so it does not model a practical black-box database.
