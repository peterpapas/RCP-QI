from math import isclose

from rcp_qi_research.multi_iteration import correct_half_probability
from rcp_qi_research.partition_register import run_register_experiment


def test_partition_register_experiment_exposes_no_free_information(tmp_path):
    report = run_register_experiment(tmp_path, min_n=2, max_n=4)
    assert (tmp_path / "phase2_partition_register.json").exists()
    assert (tmp_path / "phase2_partition_register.png").exists()
    for row in report["rows"]:
        assert row["phase_oracle_calls"] == row["iterations"]
        assert row["gate_count_before_measurement"] > 0
        assert row["depth_before_measurement"] > 0
        if row["variant"] == "standard":
            assert isclose(
                row["correct_half_probability_from_data"],
                correct_half_probability(row["n"], row["iterations"]),
                abs_tol=1e-10,
            )
        if row["variant"] == "local_partition_diffuser":
            assert isclose(row["correct_half_probability_from_data"], 0.5, abs_tol=1e-10)
    for pair in report["left_right_pairs"]:
        if pair["variant"] in ("label_before", "phase_kickback"):
            assert isclose(pair["left_vs_right_ancilla_trace_distance"], 0, abs_tol=1e-10)
        elif pair["variant"] == "label_after":
            expected = abs(2 * correct_half_probability(pair["n"], pair["iterations"]) - 1)
            assert isclose(pair["left_vs_right_ancilla_trace_distance"], expected, abs_tol=1e-10)
