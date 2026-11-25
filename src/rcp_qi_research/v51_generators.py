"""Deterministic V5.1 CNF families. Generation never gives solvers a witness."""

from __future__ import annotations

import hashlib
import lzma
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np

from .problems import CNFProblem
from .structural import (
    graph_coloring,
    random_three_sat,
    symmetric_pairs,
    two_sat_chain,
    xor_constraint,
)


@dataclass(frozen=True)
class InstanceSpec:
    family: str
    nominal_n: int
    seed: int
    level: str = "base"
    source: str = "generated"

    @property
    def id(self) -> str:
        return f"{self.family}_n{self.nominal_n}_{self.level}_s{self.seed}"


@dataclass(frozen=True)
class Instance:
    problem: CNFProblem
    xor_equations: tuple[tuple[int, int], ...] = ()
    symmetric_pairs: tuple[tuple[int, int], ...] = ()
    source_sha256: str | None = None


def _xor_case(n: int, seed: int, level: str) -> Instance:
    rng = np.random.default_rng(seed)
    rhs = [int(v) for v in rng.integers(0, 2, n - 2)]
    equations = []
    clauses: list[tuple[int, ...]] = []
    for i, bit in enumerate(rhs):
        vars_ = (i + 1, i + 2, i + 3)
        equations.append((sum(1 << (v - 1) for v in vars_), bit))
        clauses.extend(xor_constraint(vars_, bit))
    if level in {"unique", "zero"}:
        for i in (1, 2):
            value = int(rng.integers(0, 2))
            equations.append((1 << (i - 1), value))
            clauses.append((i if value else -i,))
    if level == "zero":
        equations.append((equations[0][0], 1 - rhs[0]))
        clauses.extend(xor_constraint((1, 2, 3), 1 - rhs[0]))
    return Instance(CNFProblem(n, tuple(clauses)), tuple(equations))


def _pigeonhole(target_n: int) -> Instance:
    # k pigeons into k-1 holes; use the closest variable count to target.
    k = min(range(3, 40), key=lambda k: abs(k * (k - 1) - target_n))
    holes = k - 1
    var = lambda p, h: p * holes + h + 1
    clauses: list[tuple[int, ...]] = []
    for p in range(k):
        clauses.append(tuple(var(p, h) for h in range(holes)))
        clauses.extend((-var(p, a), -var(p, b)) for a, b in combinations(range(holes), 2))
    for h in range(holes):
        clauses.extend((-var(a, h), -var(b, h)) for a, b in combinations(range(k), 2))
    return Instance(CNFProblem(k * holes, tuple(clauses)))


def _color_case(target_n: int, seed: int, level: str) -> Instance:
    vertices = max(4, target_n // 3)
    rng = np.random.default_rng(seed)
    if level == "unsat_k4":
        edges = set(combinations(range(4), 2))
        edges.update((u, u + 1) for u in range(4, vertices - 1))
    else:
        colors = [int(v) for v in rng.integers(0, 3, vertices)]
        density = 0.2 if level == "sparse" else 0.5
        edges = {(u, v) for u, v in combinations(range(vertices), 2) if colors[u] != colors[v] and rng.random() < density}
    return Instance(graph_coloring(vertices, 3, tuple(sorted(edges))))


PUBLIC_SHA256 = {
    "Break_12_50.xml.cnf.xz": "e56a8b6d9099fab4950ca38c9c759958d9d7c31ca8bc0ea78fad5238d7d67382",
    "s38417.cnf.xz": "03d81a900d1f6481daec12e2539de6139cc1579d7fab571ceac02ec68f8b6e99",
}


def _public_case(name: str) -> Instance:
    path = Path(__file__).resolve().parents[2] / "benchmarks" / "instances" / "satcomp2025" / name
    if not path.is_file():
        raise FileNotFoundError(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != PUBLIC_SHA256[name]:
        raise ValueError(f"public benchmark checksum mismatch: {name}")
    clauses: list[tuple[int, ...]] = []
    n = 0
    buffer: list[int] = []
    with lzma.open(path, "rt", encoding="ascii", errors="replace") as stream:
        for line in stream:
            if not line or line[0] in "c%":
                continue
            if line.startswith("p "):
                n = int(line.split()[2])
                continue
            for token in line.split():
                lit = int(token)
                if lit == 0:
                    if not buffer:
                        raise ValueError("public CNF has an empty clause")
                    clauses.append(tuple(buffer))
                    buffer = []
                else:
                    buffer.append(lit)
    if buffer:
        raise ValueError("unterminated DIMACS clause")
    return Instance(CNFProblem(n, tuple(clauses)), source_sha256=digest)


PUBLIC_FILES = {
    "public_sat": "Break_12_50.xml.cnf.xz",
    "public_unsat": "s38417.cnf.xz",
}


def generate(spec: InstanceSpec) -> Instance:
    n = spec.nominal_n
    if spec.family == "random_3sat":
        ratio = float(spec.level)
        return Instance(random_three_sat(n, round(n * ratio), seed=spec.seed, planted=False))
    if spec.family == "planted_3sat":
        ratio = float(spec.level)
        return Instance(random_three_sat(n, round(n * ratio), seed=spec.seed, planted=True))
    if spec.family == "xor":
        return _xor_case(n, spec.seed, spec.level)
    if spec.family == "two_sat":
        return Instance(two_sat_chain(n, variant=spec.level))
    if spec.family == "coloring":
        return _color_case(n, spec.seed, spec.level)
    if spec.family == "pigeonhole":
        return _pigeonhole(n)
    if spec.family == "symmetry":
        problem = symmetric_pairs(n // 2)
        return Instance(problem, symmetric_pairs=tuple((2 * i, 2 * i + 1) for i in range(n // 2)))
    if spec.family in PUBLIC_FILES:
        return _public_case(PUBLIC_FILES[spec.family])
    raise ValueError(f"unknown family {spec.family}")


def instance_digest(problem: CNFProblem) -> str:
    h = hashlib.sha256()
    h.update(f"n={problem.n}\n".encode())
    for clause in problem.clauses:
        h.update((" ".join(map(str, clause)) + " 0\n").encode())
    return h.hexdigest()


def default_specs(seeds: tuple[int, ...], sizes: tuple[int, ...]) -> list[InstanceSpec]:
    specs = []
    for n in sizes:
        for seed in seeds:
            specs.extend(
                [
                    InstanceSpec("random_3sat", n, seed, "3.8"),
                    InstanceSpec("random_3sat", n, seed, "4.25"),
                    InstanceSpec("random_3sat", n, seed, "4.6"),
                    InstanceSpec("planted_3sat", n, seed, "4.25"),
                    InstanceSpec("coloring", n, seed, "sparse"),
                    InstanceSpec("coloring", n, seed, "unsat_k4"),
                    InstanceSpec("xor", n, seed, "unique"),
                    InstanceSpec("xor", n, seed, "zero"),
                    InstanceSpec("two_sat", n, seed, "unique"),
                    InstanceSpec("two_sat", n, seed, "zero"),
                    InstanceSpec("symmetry", n, seed),
                ]
            )
        # Pigeonhole has no random seed; it is included once per size.
        specs.append(InstanceSpec("pigeonhole", n, 0))
    specs.extend(InstanceSpec(family, 0, 0, "official", "SAT Competition 2025") for family in PUBLIC_FILES)
    return specs
