from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.ibm_bridge import run_fake_backend_once, run_real_hardware_once


def run_delay_ramp(
    real: bool,
    backend: str,
    shots: int,
    delays_ms: list[float],
    seed: int,
    channel: str,
) -> dict[str, object]:
    records = []
    for index, delay in enumerate(delays_ms):
        if real:
            payload = run_real_hardware_once(shots=shots, seed=seed + index, channel=channel, backend_name=backend, delay_ms=delay)
        else:
            payload = run_fake_backend_once(shots=shots, seed=seed + index, delay_ms=delay)
        records.append(payload)
    ghz_values = [float(record["ghz_population"]) for record in records]
    q_values = [float(record["q_conf"]) for record in records]
    monotonic_ghz_down = all(left >= right for left, right in zip(ghz_values, ghz_values[1:]))
    monotonic_q_down = all(left >= right for left, right in zip(q_values, q_values[1:]))
    return {
        "source": "aegis_delay_ramp_degradation_detection",
        "backend": backend if real else records[0]["backend"],
        "real": real,
        "shots_per_delay": shots,
        "delays_ms": delays_ms,
        "records": records,
        "monotonic_ghz_down": monotonic_ghz_down,
        "monotonic_q_conf_down": monotonic_q_down,
        "claim_boundary": "Detects degradation in returned outputs; does not claim physical coherence extension.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Delay-ramp degradation detection for AEGIS.")
    parser.add_argument("--real", action="store_true")
    parser.add_argument("--backend", default="ibm_marrakesh")
    parser.add_argument("--channel", default="ibm_quantum_platform")
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--delays-ms", default="0,1,2,5")
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", type=Path, default=Path("delay_ramp.json"))
    args = parser.parse_args()
    delays = [float(item.strip()) for item in args.delays_ms.split(",") if item.strip()]
    payload = run_delay_ramp(args.real, args.backend, args.shots, delays, args.seed, args.channel)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
