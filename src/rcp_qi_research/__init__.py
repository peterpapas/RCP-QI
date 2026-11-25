"""Reproducible, cost-aware search baselines for the RCP-QI hypothesis."""

from .problems import CNFProblem, EqualityProblem
from .search import classical_exhaustive, grover_search, recursive_partition_search

__all__ = [
    "CNFProblem",
    "EqualityProblem",
    "classical_exhaustive",
    "grover_search",
    "recursive_partition_search",
]
