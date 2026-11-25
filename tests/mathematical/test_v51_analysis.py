"""Censoring and uncertainty checks for the scaling report."""

import runpy
from pathlib import Path

namespace = runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts" / "analyze_v51.py"))
par2 = namespace["par2"]
wilson = namespace["wilson"]


def test_par2_keeps_timeout_and_partial_penalty() -> None:
    assert par2({"completed": False, "budget_s": 2, "wall_time_s": 2}) == 4
    assert par2({"completed": False, "budget_s": 2, "wall_time_s": 0.1}) == 4
    assert par2({"completed": True, "budget_s": 2, "wall_time_s": 0.25}) == 0.25


def test_wilson_interval_is_wide_for_two_seeds() -> None:
    low, high = wilson(2, 2)
    assert low < 0.35
    assert high == 1.0
