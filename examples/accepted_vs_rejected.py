from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegis_stats import mean, sample_std, wilson_interval
from examples.session_batch_loop import run_fake_batch_loop, run_real_session_batch_loop


def summarize_acceptance(payload: dict, accept_threshold: float | None = None) -> dict[str, object]:
    records = payload["records"]
    if accept_threshold is None:
        accepted = [record for record in records if record["continuity_gate_passed"]]
        rejected = [record for record in records if not record["continuity_gate_passed"]]
        acceptance_rule = "continuity_gate_passed"
    else:
        accepted = [
            record for record in records
            if record["continuity_gate_passed"] and float(record["ghz_population"]) >= accept_threshold
        ]
        rejected = [record for record in records if record not in accepted]
        acceptance_rule = f"continuity_gate_passed AND ghz_population >= {accept_threshold:.4f}"

    def group(name: str, rows: list[dict]) -> dict[str, object]:
        ghz_values = [float(row["ghz_population"]) for row in rows]
        q_values = [float(row["q_conf"]) for row in rows]
        total_good = sum(int(row.get("good_counts_0000_1111", 0)) for row in rows)
        total_shots = sum(int(row.get("shots", 0)) for row in rows)
        ci = wilson_interval(total_good, total_shots) if total_shots else None
        states = sorted({state for row in rows for state in row.get("governance_states", [])})
        return {
            "group": name,
            "count": len(rows),
            "mean_ghz": mean(ghz_values),
            "std_ghz": sample_std(ghz_values),
            "min_ghz": min(ghz_values) if ghz_values else None,
            "max_ghz": max(ghz_values) if ghz_values else None,
            "q_conf_mean": mean(q_values),
            "governance_states": states,
            "ghz_wilson_95": {"low": ci.low, "high": ci.high} if ci else None,
        }

    all_group = group("all", records)
    accepted_group = group("accepted", accepted)
    rejected_group = group("rejected", rejected)
    success_condition = (
        accepted_group["count"] > 0
        and rejected_group["count"] > 0
        and accepted_group["mean_ghz"] > all_group["mean_ghz"] > rejected_group["mean_ghz"]
    )
    return {
        **payload,
        "acceptance_rule": acceptance_rule,
        "acceptance_summary": [all_group, accepted_group, rejected_group],
        "success_condition": "F_accepted > F_all > F_rejected",
        "success_condition_met": success_condition,
        "claim_boundary": "Quality-gate comparison over returned count histograms; not physical noise suppression.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Accepted-vs-rejected GHZ quality-gate test for AEGIS.")
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--backend", default="ibm_marrakesh")
    parser.add_argument("--channel", default="ibm_quantum_platform")
    parser.add_argument("--batches", type=int, default=30)
    parser.add_argument("--shots", type=int, default=256)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--accept-threshold", type=float, default=None, help="Optional GHZ quality threshold for accepted-vs-rejected split.")
    parser.add_argument("--output", type=Path, default=Path("accepted_vs_rejected.json"))
    args = parser.parse_args()
    if args.real:
        payload = run_real_session_batch_loop(args.backend, args.batches, args.shots, args.seed, args.channel)
    else:
        payload = run_fake_batch_loop(args.batches, args.shots, args.seed)
    summary = summarize_acceptance(payload, accept_threshold=args.accept_threshold)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
