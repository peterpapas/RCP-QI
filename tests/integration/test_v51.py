"""Independent checks of V5.1 family promises and dedicated solvers."""

import pytest

from rcp_qi_research.v51_generators import InstanceSpec, generate, instance_digest
from rcp_qi_research.v51_solvers import direct_cdcl, execute, partition_cdcl


@pytest.mark.parametrize("n,seed", [(8, 7), (16, 19), (32, 31)])
def test_xor_gaussian_elimination_matches_clause_solver(n: int, seed: int) -> None:
    for level in ("unique", "zero"):
        instance = generate(InstanceSpec("xor", n, seed, level))
        gf2 = execute(instance, "xor_gauss")
        cdcl = direct_cdcl(instance, "g4")
        assert gf2["status"] == cdcl["status"] == ("sat" if level == "unique" else "unsat")
        if level == "unique":
            assert gf2["witness_verified"]
        else:
            assert gf2["unsat_certificate_checked"]


@pytest.mark.parametrize("n", [8, 16, 32])
def test_two_sat_scc_matches_clause_solver(n: int) -> None:
    for level in ("unique", "zero"):
        instance = generate(InstanceSpec("two_sat", n, 0, level))
        scc = execute(instance, "two_sat_scc")
        cdcl = direct_cdcl(instance, "cadical195")
        assert scc["status"] == cdcl["status"] == ("sat" if level == "unique" else "unsat")
        if level == "unique":
            assert scc["witness_verified"]
        else:
            assert scc["unsat_certificate_checked"]


def test_graph_pigeonhole_and_symmetry_controls() -> None:
    cases = (("coloring", "sparse", "sat"), ("coloring", "unsat_k4", "unsat"), ("pigeonhole", "base", "unsat"), ("symmetry", "base", "sat"))
    for family, level, expected in cases:
        instance = generate(InstanceSpec(family, 16, 5, level))
        assert direct_cdcl(instance, "g4")["status"] == expected
        if family == "symmetry":
            assert execute(instance, "symmetry_break")["status"] == expected


def test_partition_depth_cap_is_incomplete_not_success() -> None:
    instance = generate(InstanceSpec("xor", 16, 3, "unique"))
    row = partition_cdcl(instance, "prefix", max_depth=5)
    assert row["status"] == "partial"
    assert row["partition_depth"] == 5
    assert row["solver_calls"] == 6
    assert row["witness_verified"] is None


def test_seeded_instance_digest_is_stable() -> None:
    spec = InstanceSpec("random_3sat", 32, 73, "4.25")
    assert instance_digest(generate(spec).problem) == instance_digest(generate(spec).problem)


def test_public_instance_headers_and_hashes() -> None:
    for family, n in (("public_sat", 14036), ("public_unsat", 20100)):
        instance = generate(InstanceSpec(family, 0, 0, "official"))
        assert instance.problem.n == n
        assert len(instance.problem.clauses) > 50_000
        assert instance.source_sha256 is not None
