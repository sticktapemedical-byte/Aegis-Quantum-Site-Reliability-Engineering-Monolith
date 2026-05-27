# AEGIS Validation and Grounding

This repository measures governance-system behavior in simulation. It does not claim to measure real quantum hardware properties.

## Measured in Code

- Weighted Byzantine filtering is tested against synthetic poisoned-node trials in `tests/test_kernel.py`.
- Wrapped-delta phase unwrapping is tested across repeated `[-pi, pi)` branch crossings with acceleration variance below `8.09e-08`.
- Unsafe-output prevention is tested across normal, storm, attack, crypto-seal, anchor-dispute, and phase-hold scenarios.
- Ledger integrity is tested by validating parent links, Merkle roots, block hashes, and HMAC signatures.
- `.QOM` compact payload generation is checked as a 176-bit frame in tests and monitor smoke checks.

## Theoretical or Simulation-Only Claims

- Unsafe-output prevention efficiency is empirical within the synthetic Monte Carlo model, not a physical noise-removal claim.
- The cascade boundary is a theoretical product of mitigation terms and should be treated as a projection until hardware-in-the-loop validation exists.
- The `14.2x` compression ratio is a telemetry-model parameter, not a measured compressor benchmark.
- Qiskit bridge metrics are simulator integration metrics, not laboratory device measurements.

## Not Measured

- Real `T1` / `T2` coherence times.
- Physical gate fidelities or calibration drift over long hardware runs.
- Real network packet loss under production mesh deployment.
- Scalability beyond the configured simulation sizes.

## Baselines

The grounding tests compare the governance loop against random intervention and validate deterministic cryptographic lineage. Additional ablation studies can be added as hardware or larger simulator traces become available.

Run:

`python -m pytest tests -v`
