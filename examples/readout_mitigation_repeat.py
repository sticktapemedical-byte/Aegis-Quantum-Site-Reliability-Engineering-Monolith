from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegis_stats import mean, sample_std
from examples.readout_mitigation_comparison import run_readout_mitigation_comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="Repeated readout mitigation comparison for AEGIS.")
    parser.add_argument("--real", action="store_true", help="Required for IBM hardware. Without this, exits after printing run plan.")
    parser.add_argument("--backend", default="ibm_marrakesh")
    parser.add_argument("--channel", default="ibm_quantum_platform")
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--ghz-shots", type=int, default=1024)
    parser.add_argument("--calibration-shots", type=int, default=256)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", type=Path, default=Path("readout_mitigation_repeat.json"))
    args = parser.parse_args()
    if not args.real:
        plan = {
            "dry_run": True,
            "command": "add --real to execute IBM jobs",
            "backend": args.backend,
            "repeats": args.repeats,
            "shots_per_repeat": args.ghz_shots + (8 * args.calibration_shots),
            "total_planned_shots": args.repeats * (args.ghz_shots + (8 * args.calibration_shots)),
        }
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    records = []
    for index in range(args.repeats):
        records.append(
            run_readout_mitigation_comparison(
                backend_name=args.backend,
                ghz_shots=args.ghz_shots,
                calibration_shots=args.calibration_shots,
                seed=args.seed + index,
                channel=args.channel,
            )
        )
    deltas = [float(record["mitigation_delta"]) for record in records]
    payload = {
        "source": "aegis_readout_mitigation_repeat",
        "backend": args.backend,
        "repeats": args.repeats,
        "total_shots": sum(int(record["total_shots"]) for record in records),
        "mean_raw_ghz": mean(record["raw_ghz_population"] for record in records),
        "mean_mitigated_ghz": mean(record["mitigated_ghz_population"] for record in records),
        "mean_delta": mean(deltas),
        "std_delta": sample_std(deltas),
        "records": records,
        "claim_boundary": "Classical readout mitigation comparison plus AEGIS governance over returned raw counts.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
