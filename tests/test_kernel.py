from __future__ import annotations

import math
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aegis_kernel import (  # noqa: E402
    AegisContinuityKernel,
    GovernanceState,
    KernelConfig,
    build_nominal_telemetry,
)


def test_crypto_invalidation_closes_hardware_gate_and_sets_crypto_seal() -> None:
    kernel = AegisContinuityKernel(seed=7)
    rng = random.Random(7)

    telemetry = build_nominal_telemetry(kernel.config.node_count, rng, "crypto_seal")
    result = kernel.execute_cycle(telemetry, scenario="crypto_signature_slip")

    assert result.governance_mask & GovernanceState.CRYPTO_SEAL
    assert not result.continuity_gate_passed
    assert result.hardware_register_target["gate_open"] is False
    assert result.unsafe_output_prevented is True


def test_holdover_ceiling_breach_triggers_circuit_abort() -> None:
    config = KernelConfig(epsilon_p_max=0.01)
    kernel = AegisContinuityKernel(config=config, seed=11)
    rng = random.Random(11)

    telemetry = build_nominal_telemetry(kernel.config.node_count, rng, "normal")
    for sample in telemetry:
        sample.phase_velocity = 10.0
        sample.phase_acceleration = 0.0

    result = kernel.execute_cycle(telemetry, scenario="holdover_decay_stress")

    assert result.governance_mask & GovernanceState.CIRCUIT_ABORT
    assert "HOLDOVER_BREACH" in result.hard_abort_causes
    assert result.hardware_register_target["gate_open"] is False
    assert result.integrity_preserved is True


def test_riemann_unwrap_continuity_across_branch_cut() -> None:
    kernel = AegisContinuityKernel(seed=17)
    node_id = "Q_NODE_0"
    entry = kernel.track_registry[node_id]

    true_phases = [3.10 + index * 0.02 for index in range(24)]
    wrapped = [((phase + math.pi) % (2.0 * math.pi)) - math.pi for phase in true_phases]
    entry.last_raw_phase = wrapped[0]
    entry.unwrapped_phase = wrapped[0]

    unwrapped_track = [entry.unwrapped_phase]
    for phase in wrapped[1:]:
        unwrapped_track.append(kernel.manifold_unwrap({node_id: phase})[node_id])

    deltas = [right - left for left, right in zip(unwrapped_track, unwrapped_track[1:])]
    acceleration = [right - left for left, right in zip(deltas, deltas[1:])]
    accel_variance = statistics.pvariance(acceleration)

    assert all(abs(delta - 0.02) < 1e-12 for delta in deltas)
    assert accel_variance < 8.09e-8
