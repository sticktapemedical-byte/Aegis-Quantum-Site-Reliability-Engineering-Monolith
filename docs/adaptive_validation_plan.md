# AEGIS Adaptive IBM Validation Plan

This document maps the QPU upgrade plan to the current repository state. The claim boundary remains narrow: AEGIS currently governs returned IBM Quantum outputs and can select later workloads; it does not modify a running QPU job in real time.

## Implemented

| Plan item | Repo status |
| --- | --- |
| Claim boundary language | README, validation report, and roadmap state that AEGIS is a classical post-processing and workload-governance layer. |
| Confidence intervals | `aegis_stats.py` provides Wilson intervals; validation artifacts and tests use them. |
| Sanitized artifact vault | `docs/validation/raw_counts_sanitized/` and `docs/validation/job_manifest.json` store public-safe count histograms, job IDs, derived metrics, hashes, and version metadata. |
| Exact circuit specs | `circuits/` contains GHZ, phase-sweep, VQE-style toy-H2, and depth-stress specifications. |
| Baseline comparison | `examples/baseline_comparator.py` builds raw-vs-governed-vs-mitigated summaries. |
| Threshold freeze | `docs/validation/threshold_freeze.json` freezes public thresholds before follow-up interpretation. |
| CI and tests | `.github/workflows/test.yml` runs the Python test suite; `tests/` checks kernel safety invariants and validation artifacts. |
| Backend discovery | `examples/ibm_backend_discovery.py` lists accessible operational backends without submitting jobs. |
| Session-style batch loop | `examples/session_batch_loop.py` processes returned batches immediately and falls back to normal jobs if IBM Runtime Sessions are unavailable. |
| Accepted-vs-rejected quality split | `examples/accepted_vs_rejected.py` compares accepted, rejected, and all returned batches. |
| Delay-ramp degradation detection | `examples/delay_ramp.py` runs GHZ workloads with configurable idle delays. |
| Readout mitigation repeat study | `examples/readout_mitigation_repeat.py` repeats raw-vs-basic-readout-mitigation comparisons. |
| Adaptive backend selector | `examples/adaptive_backend_selector.py` probes candidate backends and commits to the highest AEGIS score. |
| Resource efficiency summary | `examples/efficiency_report.py` summarizes shots per accepted artifact from the sanitized vault. |

## Ready-To-Run Real Backend Commands

These commands spend IBM Quantum runtime. Keep shot counts low unless deliberately running a statistical study.

```powershell
python examples/accepted_vs_rejected.py --real --backend ibm_marrakesh --batches 30 --shots 256 --accept-threshold 0.94 --output accepted_vs_rejected.json
python examples/delay_ramp.py --real --backend ibm_marrakesh --shots 1024 --delays-ms 0,1,2,5 --output delay_ramp.json
python examples/readout_mitigation_repeat.py --real --backend ibm_marrakesh --repeats 10 --ghz-shots 1024 --calibration-shots 256 --output readout_mitigation_repeat.json
python examples/adaptive_backend_selector.py --real --backends ibm_marrakesh,ibm_kingston,ibm_fez --probe-shots 256 --commit-shots 1024 --output adaptive_backend_selector.json
python examples/efficiency_report.py --output docs/validation/efficiency_summary.json
```

## Still Future Work

| Plan item | Status |
| --- | --- |
| Layout selector | Not yet implemented as a coupling-map-aware qubit-chain optimizer. |
| Adaptive mitigation selector | Not yet implemented as a probe-then-commit mitigation policy chooser beyond basic readout comparison. |
| Dynamical decoupling controller | Not yet implemented as an inserted DD schedule on idle windows. |
| Dynamic-circuit feedback | Not yet implemented; requires supported IBM backend features and separate circuit design. |
| RB/T1/T2/tomography campaign | Not yet implemented as a full calibration-grade experiment matrix. |
| Blind holdout and ablation tables | Not yet implemented; recommended for a later reviewer-grade study. |
| Publication plots | Not yet implemented; current outputs are JSON and Markdown. |

## Operating Rule

When presenting results, describe them as returned-output governance, quality gating, and adaptive workload selection. Use stronger language only after AEGIS changes a future submitted workload and beats fixed baselines under the same backend and calibration window.
