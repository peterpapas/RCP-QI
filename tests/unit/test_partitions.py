import pytest

from rcp_qi_research.core import BitPrefixPartition


@pytest.mark.parametrize("n", range(1, 7))
def test_implicit_partitions_are_disjoint_exhaustive_and_halve(n):
    root = BitPrefixPartition(n)
    assert root.size == 2**n
    frontier = [root]
    for _ in range(n):
        next_frontier = []
        for parent in frontier:
            left, right = parent.split()
            assert left.size == right.size == parent.size // 2
            assert all(parent.contains(x) == (left.contains(x) or right.contains(x)) for x in range(2**n))
            assert not any(left.contains(x) and right.contains(x) for x in range(2**n))
            next_frontier.extend((left, right))
        frontier = next_frontier
    assert {leaf.only_candidate() for leaf in frontier} == set(range(2**n))


def test_invalid_partition_and_leaf_split():
    with pytest.raises(ValueError):
        BitPrefixPartition(2, (0, 1, 0))
    with pytest.raises(ValueError):
        BitPrefixPartition(2, (2,))
    with pytest.raises(ValueError):
        BitPrefixPartition(1, (0,)).split()
