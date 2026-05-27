from __future__ import annotations

import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegis_kernel import AegisContinuityKernel, EnvironmentVector, NodeTelemetry, normalize_vector


def require_qiskit():
    try:
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
    except ImportError as exc:
        raise SystemExit(
            "Qiskit bridge requires optional packages: qiskit and qiskit-aer. "
            "Install them in a separate environment with: pip install qiskit qiskit-aer"
        ) from exc
    return QuantumCircuit, transpile, AerSimulator, NoiseModel, depolarizing_error, thermal_relaxation_error


def build_ghz_circuit(quantum_circuit):
    circuit = quantum_circuit(4, 4)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.cx(2, 3)
    circuit.measure(range(4), range(4))
    return circuit


def build_noise_model(noise_model_cls, depolarizing_error, thermal_relaxation_error):
    model = noise_model_cls()
    single_qubit_thermal = thermal_relaxation_error(t1=50_000, t2=70_000, time=120)
    two_qubit_thermal = thermal_relaxation_error(t1=50_000, t2=70_000, time=350).expand(
        thermal_relaxation_error(t1=50_000, t2=70_000, time=350)
    )
    model.add_all_qubit_quantum_error(single_qubit_thermal.compose(depolarizing_error(0.002, 1)), ["h"])
    model.add_all_qubit_quantum_error(two_qubit_thermal.compose(depolarizing_error(0.006, 2)), ["cx"])
    return model


def counts_to_expectations(counts: dict[str, int], shots: int) -> list[float]:
    expectations = []
    for qubit_index in range(4):
        z_sum = 0.0
        for bitstring, count in counts.items():
            bit = bitstring[::-1][qubit_index]
            z_sum += (1.0 if bit == "0" else -1.0) * count
        expectations.append(z_sum / max(1, shots))
    return expectations


def telemetry_from_counts(counts: dict[str, int], shots: int, epoch: int, rng: random.Random) -> list[NodeTelemetry]:
    expectations = counts_to_expectations(counts, shots)
    parity_mass = sum(count for bitstring, count in counts.items() if bitstring in {"0000", "1111"}) / max(1, shots)
    entropy_proxy = 1.0 - parity_mass
    environment = EnvironmentVector(
        thermal=min(1.0, 0.10 + entropy_proxy * 0.40),
        electromagnetic=min(1.0, 0.08 + abs(expectations[0] - expectations[1]) * 0.30),
        voltage=min(1.0, 0.06 + entropy_proxy * 0.20),
        radiation=min(1.0, 0.05 + (1.0 - abs(sum(expectations) / 4.0)) * 0.18),
        latency=min(1.0, 0.06 + epoch * 0.002),
    )
    telemetry = []
    for index, expectation in enumerate(expectations):
        phase = math.atan2(math.sqrt(max(0.0, 1.0 - expectation * expectation)), expectation)
        vector = normalize_vector([expectation, entropy_proxy + rng.uniform(-0.01, 0.01), 1.0 - entropy_proxy])
        telemetry.append(
            NodeTelemetry(
                node_id=f"Q_NODE_{index}",
                raw_phase=phase,
                phase_velocity=0.08 + entropy_proxy * 0.22,
                phase_acceleration=rng.uniform(-0.20, 0.20) + entropy_proxy * 0.35,
                bloch_vector=vector,
                signal_mu=0.30 + entropy_proxy * 0.35,
                environment=environment,
                suspected_attack=False,
                crypto_valid=True,
                mission_priority=0.65,
            )
        )
    return telemetry


def run_bridge(cycles: int = 6, shots: int = 2048, seed: int = 2026) -> list[dict[str, object]]:
    quantum_circuit, transpile, simulator_cls, noise_model_cls, depolarizing_error, thermal_relaxation_error = require_qiskit()
    rng = random.Random(seed)
    noise_model = build_noise_model(noise_model_cls, depolarizing_error, thermal_relaxation_error)
    simulator = simulator_cls(noise_model=noise_model, seed_simulator=seed)
    circuit = transpile(build_ghz_circuit(quantum_circuit), simulator)
    kernel = AegisContinuityKernel(seed=seed)
    results = []

    for epoch in range(1, cycles + 1):
        job = simulator.run(circuit, shots=shots)
        counts = job.result().get_counts()
        telemetry = telemetry_from_counts(counts, shots, epoch, rng)
        cycle = kernel.execute_cycle(telemetry, scenario=f"qiskit_ghz_epoch_{epoch}")
        results.append(
            {
                "epoch": epoch,
                "counts": counts,
                "q_conf": cycle.q_conf,
                "continuity_gate_passed": cycle.continuity_gate_passed,
                "governance_states": cycle.governance_states,
                "qom_compact_payload_bits": cycle.qom_compact_payload_bits,
                "qom_compact_payload_hex": cycle.qom_compact_payload_hex,
                "merkle_root": cycle.merkle_root,
            }
        )
    return results


def main() -> None:
    for item in run_bridge():
        states = "|".join(item["governance_states"])
        print(
            f"epoch={item['epoch']} q_conf={item['q_conf']:.4f} "
            f"gate={item['continuity_gate_passed']} qom={item['qom_compact_payload_bits']}b states={states}"
        )


if __name__ == "__main__":
    main()
