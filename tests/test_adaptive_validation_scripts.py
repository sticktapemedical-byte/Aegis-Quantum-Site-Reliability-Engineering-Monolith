from examples.accepted_vs_rejected import summarize_acceptance
from examples.adaptive_backend_selector import score_backend


def _record(ghz, passed, batch):
    return {
        "batch": batch,
        "ghz_population": ghz,
        "q_conf": ghz,
        "continuity_gate_passed": passed,
        "good_counts_0000_1111": int(ghz * 1000),
        "shots": 1000,
        "governance_states": ["NORMAL"] if passed else ["PHASE_HOLD"],
    }


def test_accepted_vs_rejected_summary_orders_quality_groups():
    payload = {
        "records": [
            _record(0.96, True, 1),
            _record(0.94, True, 2),
            _record(0.80, False, 3),
            _record(0.78, False, 4),
        ]
    }
    summary = summarize_acceptance(payload)
    all_group, accepted_group, rejected_group = summary["acceptance_summary"]
    assert summary["success_condition_met"] is True
    assert accepted_group["mean_ghz"] > all_group["mean_ghz"] > rejected_group["mean_ghz"]
    assert accepted_group["ghz_wilson_95"]["low"] < accepted_group["mean_ghz"]


def test_adaptive_backend_score_rewards_quality_and_penalizes_risk():
    strong = {"ghz_population": 0.96, "q_conf": 0.95, "round_trip_seconds": 60, "raw_error_rate": 0.04}
    weak = {"ghz_population": 0.82, "q_conf": 0.80, "round_trip_seconds": 60, "raw_error_rate": 0.18}
    slow = {"ghz_population": 0.96, "q_conf": 0.95, "round_trip_seconds": 600, "raw_error_rate": 0.04}
    assert score_backend(strong) > score_backend(weak)
    assert score_backend(strong) > score_backend(slow)
