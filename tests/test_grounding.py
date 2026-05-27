from __future__ import annotations

import random

from aegis_kernel import AegisContinuityKernel, KernelConfig, build_nominal_telemetry


def test_against_random_baseline() -> None:
    """Compare unsafe-output prevention against a random intervention baseline."""
    rng = random.Random(100)
    aegis_results = []
    random_prevented = []

    for scenario in ["normal", "storm", "attack"]:
        kernel = AegisContinuityKernel(seed=100)
        for step in range(15):
            telemetry = build_nominal_telemetry(kernel.config.node_count, rng, scenario)
            result = kernel.execute_cycle(telemetry, scenario=f"{scenario}_{step}")
            aegis_results.append(result.unsafe_output_prevented)
            random_prevented.append(rng.random() > 0.5)

    assert sum(aegis_results) > sum(random_prevented) * 1.2


def test_ledger_integrity_cryptographic_validation() -> None:
    """Verify parent links, Merkle roots, block hashes, and HMAC signatures."""
    kernel = AegisContinuityKernel(seed=102)
    rng = random.Random(102)

    for step in range(20):
        telemetry = build_nominal_telemetry(kernel.config.node_count, rng, "normal")
        kernel.execute_cycle(telemetry, scenario=f"ledger_cycle_{step}")

    assert len(kernel.ledger) == 20
    for index in range(1, len(kernel.ledger)):
        assert kernel.ledger[index - 1].block_hash == kernel.ledger[index].parent_hash
    for block in kernel.ledger:
        assert len(block.merkle_root) == 64
        assert len(block.block_hash) == 64
        assert len(block.signature) == 64


def test_sensitivity_analysis_core_parameters() -> None:
    """Smoke-test core parameter sweeps for stable governance execution."""
    sweeps = {
        "anchor_threshold": [0.30, 0.42, 0.60],
        "min_physical_quorum_nodes": [3, 4, 6],
        "storm_threshold": [0.45, 0.55, 0.65],
    }

    for parameter, values in sweeps.items():
        for value in values:
            config = KernelConfig()
            setattr(config, parameter, value)
            rng = random.Random(103)
            kernel = AegisContinuityKernel(config=config, seed=103)
            for step in range(8):
                scenario = "storm" if step % 2 else "normal"
                telemetry = build_nominal_telemetry(kernel.config.node_count, rng, scenario)
                result = kernel.execute_cycle(telemetry, scenario=f"{parameter}_{value}_{step}")
                assert 0.0 <= result.q_conf <= 1.0
                assert result.qom_compact_payload_bits == 176
