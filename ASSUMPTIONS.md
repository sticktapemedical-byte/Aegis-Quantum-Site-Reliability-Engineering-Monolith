# AEGIS Simulation Assumptions

## Telemetry Model

- The default simulation uses 12 logical nodes.
- Environmental telemetry is normalized into thermal, electromagnetic, voltage, radiation, and latency channels.
- Phase motion is simulated and filtered with standard wrapped-delta unwrapping.
- The model is designed for governance validation, not direct physical state estimation.

## Attack Model

- Synthetic Byzantine nodes may report corrupted vectors.
- Cryptographic failures are modeled as invalid signatures or timing slips.
- Attackers are not modeled as breaking SHA-256 or HMAC primitives.

## Hardware Model

- Hardware registers are represented as software abstractions suitable for FPGA/ASIC mapping documentation.
- Cryogenic and scheduler values are normalized operational telemetry values in the simulator.
- Qiskit integration is optional and isolated from the standard-library core.

## Not Modeled

- Real qubit decoherence in laboratory hardware.
- Long-duration hardware calibration drift.
- Real distributed network packet loss and leader election.
- Production throughput on multi-host deployments.
