from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.ibm_bridge import load_dotenv_if_available, require_runtime


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def compact_artifact(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    return {
        "artifact": str(path.relative_to(ROOT)).replace("\\", "/"),
        "source": payload.get("source"),
        "source_file": payload.get("source_file"),
        "backend": payload.get("backend"),
        "job_id": payload.get("job_id"),
        "shots": payload.get("shots") or payload.get("total_shots"),
        "status": payload.get("status"),
        "ghz_population": payload.get("ghz_population") or payload.get("raw_ghz_population"),
        "mitigated_ghz_population": payload.get("mitigated_ghz_population"),
        "selected_survival": payload.get("selected_survival"),
        "qaoa_expected_cut": payload.get("qaoa_expected_cut"),
        "qom_compact_payload_bits": payload.get("qom_compact_payload_bits"),
        "qom_compact_payload_hex": payload.get("qom_compact_payload_hex"),
        "merkle_root": payload.get("merkle_root"),
        "artifact_sha256": payload.get("artifact_sha256"),
    }


def local_workloads() -> list[dict[str, Any]]:
    raw_dir = ROOT / "docs" / "validation" / "raw_counts_sanitized"
    rows = []
    for path in sorted(raw_dir.glob("*.json")):
        row = compact_artifact(path)
        if (
            row.get("job_id")
            or str(row.get("source") or "").startswith(("ibm_", "aegis_"))
            or row.get("backend")
        ):
            rows.append(row)
    return rows


def status_value(job: Any) -> str:
    try:
        status = job.status()
    except Exception as exc:
        return f"status_unavailable:{exc}"
    name = getattr(status, "name", None)
    return name or str(status)


def backend_name(job: Any) -> str | None:
    for attr in ("backend", "_backend"):
        try:
            value = getattr(job, attr)
            value = value() if callable(value) else value
            if value is None:
                continue
            return getattr(value, "name", None) or str(value)
        except Exception:
            continue
    return None


def cloud_jobs(channel: str, limit: int, include_results: bool) -> list[dict[str, Any]]:
    load_dotenv_if_available()
    qiskit_runtime_service, _, _ = require_runtime()
    service = qiskit_runtime_service(channel=channel)
    jobs = service.jobs(limit=limit)
    rows = []
    for job in jobs:
        job_id = job.job_id() if hasattr(job, "job_id") else getattr(job, "job_id", None)
        row: dict[str, Any] = {
            "job_id": job_id,
            "backend": backend_name(job),
            "status": status_value(job),
        }
        for attr in ("creation_date", "created_at", "usage_estimation"):
            try:
                value = getattr(job, attr)
                value = value() if callable(value) else value
                if value is not None:
                    row[attr] = str(value)
            except Exception:
                pass
        if include_results:
            try:
                result = job.result()
                row["result_repr"] = repr(result)[:2000]
                row["result_available"] = True
            except Exception as exc:
                row["result_available"] = False
                row["result_error"] = str(exc)
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Export accessible IBM workload/job metadata without exposing credentials.")
    parser.add_argument("--cloud", action="store_true", help="Query IBM Runtime job history. May hang or fail during IBM maintenance.")
    parser.add_argument("--local", action="store_true", help="Include locally sanitized IBM workload artifacts.")
    parser.add_argument("--channel", default="ibm_quantum_platform")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--include-results", action="store_true", help="Attempt job.result(); may wait or fail for queued jobs.")
    parser.add_argument("--output", type=Path, default=Path("docs/validation/ibm_workload_results_export.json"))
    args = parser.parse_args()

    if not args.cloud and not args.local:
        args.local = True

    payload: dict[str, Any] = {
        "source": "aegis_ibm_workload_export",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_boundary": "Workload/job metadata export; does not add new QPU evidence unless cloud results are explicitly retrieved.",
        "local_sanitized_workloads": [],
        "cloud_jobs": [],
        "cloud_status": "not_requested",
    }
    if args.local:
        payload["local_sanitized_workloads"] = local_workloads()
    if args.cloud:
        try:
            payload["cloud_jobs"] = cloud_jobs(args.channel, args.limit, args.include_results)
            payload["cloud_status"] = "ok"
        except Exception as exc:
            payload["cloud_status"] = "failed"
            payload["cloud_error"] = str(exc)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "local_count": len(payload["local_sanitized_workloads"]),
        "cloud_count": len(payload["cloud_jobs"]),
        "cloud_status": payload["cloud_status"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
