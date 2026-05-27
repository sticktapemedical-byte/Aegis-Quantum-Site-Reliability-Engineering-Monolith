# AEGIS v10.0 / PRD v1.0 Mission and Architecture

## Core Mission

AEGIS v10.0 / PRD v1.0 is a hybrid probabilistic continuity infrastructure research platform. Its central thesis is that fragile probabilistic systems should not be managed as all-or-nothing deterministic machines. Instead, AEGIS wraps volatile physical environments in a classical orchestration layer that tracks, routes, verifies, and recovers useful operational state.

The governing law is:

```text
Recovery Rate > Failure Rate
```

The system does not claim to build a better quantum computer or physically preserve exact hidden quantum state. It is designed to preserve bounded operational continuity through:

- classical telemetry orchestration,
- trajectory reconstruction,
- weighted trust governance,
- rolling anchor verification,
- cryptographic lineage,
- coherence-aware scheduling,
- fail-closed runtime safety.

Current implementation status:

- Implemented now: `AegisContinuityKernel`, deterministic scenarios, Monte Carlo simulation, weighted quorum, split kappa scoring, binary `.QOM` snapshot frames, and signed ledger blocks.
- Simulated now: environmental weather, coherence market behavior, anchor disputes, phase holds, security lockdowns, circuit aborts, and continuity scoring.
- Speculative/future: direct quantum hardware interfaces, photonic lane fabrics, long-range coherence infrastructure, Q-Chip silicon, and planetary-scale Q-Fabric routing.

Claims such as 99.49% unsafe-output prevention efficiency, 18.4x lifespan multiplier, un-hackable operation, and carbon-neutral data survival should be treated as target or vision claims until reproduced by the executable simulation suite under documented parameters.

## Vocabulary Locks

Q-SRE, Quantum Site Reliability Engineering, is the umbrella discipline. AEGIS is the flagship implementation of that discipline.

QSR, Quantum State Reconstruction, is the low-level mathematical inversion engine. It maps weak measurement shadows and noisy telemetry into reconstructed proxy state coordinates. QSR should not be used to describe the entire orchestration stack.

PSR, Proxy State Reconstruction, is the runtime layer above QSR. PSR manages observer allocation, cache rings, telemetry fusion, BFT filtering, anchors, failover, and recovery routing.

.QOM should be presented to technical reviewers as Quantum Orchestration Middleware or Quantum Orchestration Mesh. The historical expansion, Quantum Orchestration Monolith, can remain as project lore, but "Middleware" or "Mesh" better communicates a modular, distributed control plane.

Soft determinism means bounded reliable classical outputs derived from probabilistic internals. In the simulation, that means the continuity corridor remains inside the tolerated error envelope, such as `epsilon_P(T) <= epsilon_P_max`.

Coherence is layer-dependent. At the speculative Layer 1 hardware boundary, it can refer to physical quantum coherence. Inside the implemented Layer 3 orchestration runtime, it is treated as a generalized signal-quality and scheduling resource.

Kardashev status belongs in visionary roadmap material, not in strict technical claims.

## Corridor Taxonomy

Drift Corridor: the historical path of phase drift, velocity, and acceleration.

Predictive Corridor: the forward lookahead envelope estimating near-future trajectory.

Trajectory Corridor: the active fused path after Taylor projection and Riemann unwrapping.

Continuity Corridor, `Gamma(t)`: the top-level safety envelope that combines drift, prediction, active trajectory, trust, anchor agreement, and governance state.

## Cache and Ledger Semantics

Ghost Reserve stores decaying state estimates, previous anchors, and failed reconstructions. It is a high-speed residue buffer used by recovery and lookahead logic.

Semantic Cache Reserve combines meaning-based compression with cryptographic lookup indexes. It stores high-utility state summaries and the hashes needed for replay, audit, and fast retrieval.

Birth Certificates are reserved for major state transitions, including governance changes, anchor disputes, crypto seals, phase holds, circuit aborts, and cache migrations. Ordinary steady-state snapshots are ledgered as `SNAPSHOT_COMMIT` records.

Boundary Event Ledger is the near-term simulation term for critical physical-interface, trust-boundary, anchor, hold, and seal events. Collapse Event Ledger remains only as future hardware-roadmap vocabulary for a system physically wired into a literal quantum measurement stack.

Operational Proxy Transfer Engine, OPTE, replaces Qbit Duplication Engine in technical text. "Quantum Fax" is only a public analogy. OPTE makes clear that AEGIS transfers an operational proxy and does not claim to clone unknown quantum states.

Successful QSR reconstruction is measured by the combined outcome: sufficient Meaningful Continuity, quorum agreement, anchor agreement, and local fidelity/confidence passing configured thresholds. `M_c` is the top-level success metric, while fidelity, `Q_conf`, and kappa are supporting metrics.

The simulator distinguishes four continuity layers:

- Data continuity: reconstructed track values remain usable.
- Operational continuity: workloads remain inside allowed governance and recovery envelopes.
- Semantic continuity: meaningful state is preserved even when raw noise is discarded.
- Cryptographic continuity: ledger lineage, signatures, ratchets, and replay integrity remain intact.

## Mathematical Control Stack

Time-Normalized Kinetic Phase Normalization:

Observers may sample in staggered temporal micro-windows, `t_k`, especially during `STORM_PROTECT`. Directly fusing those raw phase metrics causes phase aliasing, so AEGIS projects each observer slice to a shared canonical timestamp, `t_c`, before circular mean fusion:

```text
P_hat_k(t_c) = P_k(t_k) + P_dot_k(t_c - t_k) + 0.5 * P_ddot_k(t_c - t_k)^2

P_star = atan2(
  sum(w_k * sin(P_hat_k(t_c))),
  sum(w_k * cos(P_hat_k(t_c)))
)
```

Riemann Manifold Phase Unwrapping:

The `atan2` branch cut at `-pi` and `+pi` can create false angular jumps. AEGIS lifts wrapped angles onto a continuous phase path:

```text
P_tilde_t = P_tilde_(t-1) + wrap_pi(P_t - P_(t-1))
wrap_pi(x) = ((x + pi) mod 2*pi) - pi
```

`PHASE_HOLD` actuates when acceleration on the unwrapped path exceeds the configured phase acceleration boundary.

Maximum Holdover Ceiling:

```text
T_hold_max = max T such that:
|P_dot|T + 0.5|P_ddot|T^2 + sigma_P * sqrt(T) <= epsilon_P_max

E_hold_max = floor(T_hold_max / delta_t_epoch)
```

Exceeding the holdover ceiling is a fail-closed condition and can trigger `CIRCUIT_ABORT`.

Backaction Accumulation:

The implemented simulation uses the scalar backaction approximation:

```text
backaction_delta = mu^2 * sigma_obs_k^2 * delta_t
```

The broader roadmap frames this as a Lindblad-inspired cumulative disturbance ledger:

```text
B_k(t) = integral(mu_k(t)^2 * sigma_obs,k(t)^2 dt)
kappa_k = (C_k * F_k) / (1 + B_k + epsilon_N)
```

Resource Law:

Useful reconstructed information must outrun noise, backaction, and entropy:

```text
dI_useful/dt > dI_noise/dt + dI_backaction/dt + dI_entropy/dt
```

## .QOM Binary Frame Target

The `.QOM` snapshot format is designed as a structured binary frame rather than JSON. The compact estimator payload target is 176 bits:

| Field | Bits | Meaning |
| --- | ---: | --- |
| `unwrapped_phase_p_tilde` | 32 | Continuous phase trajectory |
| `coherence_c` | 16 | Local signal/coherence budget |
| `collapse_progress_s` | 16 | Calculation lifecycle progress |
| `confidence_kappa` | 16 | Trust/confidence summary |
| `canonical_timestamp_tc` | 64 | Canonical timestamp |
| `backaction_summary_b` | 32 | Integrated disturbance summary |

The current Python implementation emits a larger `QOM1` audit frame because it prioritizes cryptographic auditability: it includes header fields, floating-point simulation values, a checksum, and an HMAC audit signature. The 176-bit layout is the future compact estimator payload target; the current frame is an auditable simulation envelope.

## .QOM Endpoint Map

`.QOM` is best described as the native Quantum Orchestration Middleware/Mesh namespace for AEGIS internal control-plane traffic. It is not a public DNS claim in the current implementation; it is a protocol and naming convention for routing secure runtime functions.

Canonical endpoints:

- `core.gateway.aegis.qom`: Layer 1 gateway loop for hardware boundary gating, `G(t)`, and ingestion control.
- `mesh.routing.prd.qom`: Layer 4 routing namespace for continuity-aware mesh transport, lane selection, and failover.
- `ledger.lineage.sre.qom`: Layer 3 lineage namespace for Merkle continuity records, certificates, signatures, and replay verification.

In technical documentation, avoid claiming literal speed-of-light or un-hackable behavior. The grounded claim is that `.QOM` is designed for compact, signed, auditable metadata routing across a modular control plane.

## Branch Lineage and Key Ratchets

Major state transitions, cache migrations, anchor disputes, and crypto seals create signed ledger records. These records are compiled into Merkle continuity history and signed using branch-isolated key material.

When a lineage fork occurs, each branch derives an isolated subkey:

```text
K_branch = HKDF(K_n, chain_id || branch_id || epoch || parent_hash)
```

The current simulation models this with branch IDs, HMAC signatures, Merkle roots, and key ratcheting. Secure enclave commit capsules and delayed-erasure parent-secret handling remain future implementation targets.

## Temporal Metrics and Timing Intrinsics

Effective-time damping is a roadmap concept for separating wall-clock time from the modeled survivability window of a volatile track:

```text
T_prime = integral(dt / gamma_q(D(t)))
```

In current simulation terms, this maps to holdover, drift, and recovery-window modeling rather than literal manipulation of physical time.

Timing Window Quantization defines controlled observation slots rather than arbitrary sampling. The timing stack is:

- Base Oscillator Tier: establishes system cadence.
- Phase-Lock Layer: synchronizes observer ecology.
- Drift Correction Loop: damps inter-node timing skew.
- Epoch Timing Matrix: aligns snapshot generation.
- Observation Windows: enforces phase-legal sampling gates.

This layer supports storm strobing, Taylor projection, and phase-hold decisions.

## Thermodynamics and Memory Hierarchy

AEGIS treats entropy and noise as a measurable pressure field. The governing runtime thermodynamic constraint is:

```text
dU/dt > dS/dt
```

In implementable simulation terms, this should be expressed as the resource law already used in the control stack:

```text
dI_useful/dt > dI_noise/dt + dI_backaction/dt + dI_entropy/dt
```

Memory hierarchy roadmap:

- L1 Quantum Cache: future hot micro-snapshot layer, potentially mapped to fiber delay-line concepts.
- L2 Quantum Memory: future epoch-state storage, potentially mapped to AFC/spin-wave memory concepts.
- L3 Quantum Storage: future fault-tolerant encoded buffer layer.
- Cold Archival Storage: current implementable layer for proxy state configurations, generated JSON, binary snapshots, and Merkle logs on NVMe.

Live VM state migration and DRAM-style refresh remain future architecture concepts. In the current Python suite, the analogous implemented behavior is snapshot emission, ledger continuity, and fail-closed recovery validation.

## Five-Tier Trust Architecture

AEGIS trust should be represented as a multi-channel certainty index:

```text
T = T_p + T_o + T_h + T_c + T_a
```

Trust channels:

- Physical Trust, `T_p`: raw signal integrity and five-variable environment telemetry.
- Observer Trust, `T_o`: observer reputation and drift behavior.
- Historical Trust, `T_h`: agreement with proxy cache and trajectory momentum.
- Consensus Trust, `T_c`: weighted BFT quorum result.
- Anchor Trust, `T_a`: agreement with independent anchor references and ledger lineage.

The current kernel implements this through split kappa, weighted quorum, rolling anchors, signed ledger blocks, and an explicit `trust_index` in simulation results. Trust is multiplicative:

```text
T = T_p * T_o * T_h * T_c * T_a
```

This is intentionally stricter than additive scoring. A single zero-trust layer collapses the total trust index, which matches the fail-closed discipline. Anchor trust decays exponentially across bad epochs rather than dropping to zero on the first anomalous reading:

```text
T_a,t = T_a,t-1 * exp(-lambda_a)
```

Kappa remains a vector until a final gate requires a scalar decision:

```text
kappa = [kappa_node, kappa_recon, kappa_telemetry]
```

## Product Positioning Definitions

For grounded proposals and public documentation:

- Category: Quantum Continuity Infrastructure.
- Mindset: Runtime-First Quantum Architecture.
- Reality: Software-Driven Unsafe-Output Prevention.

Important boundary: AEGIS does not claim to modify qubit physics, erase measurement backaction, or physically validate a production quantum stack. It records, routes, scores, and corrects metadata through classical orchestration to prevent unsafe outputs from reaching the terminal or polluting the ledger.

## Projection Validation Locks

The first public demo is organized as multiple benchmark tiers:

- Baseline
- Storm
- Adversarial

The `99.49%` target is defined as Unsafe-Output Prevention Efficiency, `UOP_eff`, not physical error erasure and not guaranteed continuity survival. The projection model compares protected runtime decisions against an unprotected raw baseline. In high-entropy storm conditions, the raw unsafe-output risk is modeled between 35.0% and 58.0%. The current cascade projection uses:

```text
UOP_remaining = E_raw * (1 - eta_byzantine) * (1 - eta_taylor) * (1 - eta_riemann)
```

Where:

- `eta_byzantine = 0.85`
- `eta_taylor = 0.90`
- `eta_riemann = 0.95`

At `E_raw = 0.58`, the projected remaining unsafe-output rate is:

```text
0.58 * 0.15 * 0.10 * 0.05 = 0.000435
```

This produces a cascade-projection unsafe-output prevention efficiency of:

```text
1 - (0.000435 / 0.58) = 0.99925
```

The public-demo target remains `0.9949`. The stricter `0.99925` figure is a projection boundary produced by the three-stage filter cascade, not a claim of physical validation.

Fail-closed cycles are categorized as `integrity_preserved`. They are not counted as ordinary continuity successes, but they do count toward unsafe-output prevention when the kernel prevents a bad state from being fused, emitted, or committed as valid.

Unsafe-output prevention is measured only across unsafe-output opportunities:

```text
UOP_eff = Unsafe_Outputs_Prevented / Total_Unsafe_Output_Opportunities
```

An unsafe-output opportunity is any cycle whose raw risk estimate breaches the intervention threshold. Quiet cycles with no unsafe-output opportunity are excluded from this denominator. The suite also reports `unnecessary_shutdown_rate`, which measures fail-closed events during cycles that did not present an unsafe-output opportunity.

The target `unnecessary_shutdown_rate` ceiling is `< 0.05`. Baseline unsafe-output opportunities should remain non-zero but rare, representing isolated transient hardware faults rather than broken clean-room conditions. Bypass probability is concentrated in adversarial scenarios so security stress tests do not report unrealistic perfect prevention.

UOP targets are tiered:

- Public v1 simulation target: `0.9949`.
- Systemic stretch target: `0.9990`.
- Theoretical cascade boundary: `0.99925`.

Efficiency estimates are capped below exact `1.0` in public result fields to avoid implying physically perfect filtering.

## Advanced 150-Step Simulation Report

The executable suite now emits an `advanced_performance_report` with three 50-step benchmark tiers:

1. Baseline ingestion, steps 1-50
2. Environmental storm, steps 51-100
3. Adversarial attack, steps 101-150

Target dashboard metrics used by the report:

| Tier | Fidelity | TPS | `M_c` Target | Governance Target |
| --- | ---: | ---: | ---: | --- |
| Baseline | `0.999995` | `1,420,000` | `19.11x` | `NORMAL` |
| Storm | `0.99412` | `240,000` | `12.45x` | `STORM_PROTECT` |
| Adversarial | `0.99104` | `88,000` | `8.14x` | `STORM_PROTECT | SECURITY_LOCKDOWN` |

The adversarial tier models a poisoning sweep against 37.5% of the node mesh. Late-tier anchor dispute behavior is intentionally allowed to trip `CIRCUIT_ABORT`, demonstrating fail-closed memory protection rather than silent recovery.

Important math boundary: the prose target of `99.49%` is retained as the public demo target, but the stated cascade calculation:

```text
0.58 * 0.15 * 0.10 * 0.05 = 0.000435
1 - (0.000435 / 0.58) = 0.99925
```

evaluates to `99.925%`, not `99.49%`. The generated result file records both values separately.

Meaningful Continuity is split into two values:

- `M_c_raw`: virtual operational lifespan multiplier, so values like `18.4x` or `19.11x` are valid.
- `M_c_norm`: bounded health scalar in `[0,1]` used by decision gates.

Successful continuity is a three-part composite gate:

```text
Gate = (M_c_norm >= theta_M) and (Q_conf >= 0.90) and (Anchor_Status == ACCEPT)
```

The gate thresholds are scenario-calibrated rather than constitutional constants. Storm mode uses a lower adaptive QoS gate so the system can continue processing degraded but acceptable traffic instead of reporting flat zero continuity through every environmental disruption.

Successful continuity can occur while `STORM_PROTECT` or `PHASE_HOLD` are active if the composite gate clears. `CRYPTO_SEAL` is different: it is always categorized as integrity preservation rather than continuity success, because the authentication boundary is compromised even if the state vector remains mathematically clean.

Abort behavior is dual-tier:

- `SOFT_ABORT`: transient, recoverable violations that may auto-recover after parameters realign.
- `HARD_ABORT`: high-severity cryptographic, anchor, or unrecoverable safety failures that latch until authorized reset.

`CIRCUIT_ABORT` remains the umbrella fail-closed state for compatibility, while `SOFT_ABORT` and `HARD_ABORT` describe recovery policy. After `HARD_ABORT`, recovery requires explicit authorized validation. Recovery proceeds through `RECOVERY_VALIDATE`, which is both a governance mode and a ring-fenced execution protocol that suspends active workload trust while fresh anchors and telemetry re-establish a clean corridor.

`HARD_ABORT` records cause codes for post-mortem analysis:

- `CRYPTO_FAILURE`
- `ANCHOR_DRIFT`
- `QUORUM_COLLAPSE`
- `HOLDOVER_BREACH`
- `BACKACTION_BREACH`
- `WEATHER_BREACH`

`RECOVERY_VALIDATE` exits only after both a minimum clean epoch count and rolling trust/anchor confidence thresholds are satisfied.

Boundary certificates are emitted on the first occurrence of an integrity-preserved state and on governance state transitions. Consecutive unchanged boundary states are recorded as steady boundary lineage rather than flooding the ledger with duplicate certificates.

The deterministic suite includes a dedicated `transient_drift` scenario to demonstrate `SOFT_ABORT` behavior without contaminating clean baseline traces.

The OPTE policy context hash is embedded in the binary `.QOM` frame so transferred proxy state cannot be separated from its governance mask, kappa vector, ledger parent root, and branch context.

The CLI supports `--reviewer-mode`, which emits a terse metrics-only console suitable for technical reviewers.

## Production Readiness Modules

The executable suite now models four hardware-facing architecture targets. These are simulation and compilation targets, not claims of fabricated silicon:

- Hardware Register Compilation Target: maps Layer 1 `G(t)` controls into an FPGA/ASIC-style register map with gate control, governance bitmask, O-quantization timing, `.QOM` frame pointer, anchor status, cryogenic index, and enclave mailbox addresses.
- Secure Enclave Memory Vault: models an HSM-style enclave for branch-isolated HKDF key ratchets, forensic commit capsules, delayed-erasure queues, and parent-secret isolation.
- Cryogenic Thermal Balancing Scheduler: computes `P_therm` in milli-watts and chooses nominal, observer-throttle, or lane-spread actions when thermal saturation approaches the configured budget.
- Reviewer Telemetry Stripper: exposes cold metrics for review surfaces: RMSE phase skew, packet transmission jitter in ns, Shannon entropy bounds, compression ratio, latency bound, compact `.QOM` payload size, and register timing.

## Infrastructure Layers

### Layer 0: Classical Baseline Platform

The existing CPU, RAM, NVMe, and network environment running the Python simulation and orchestration engine.

### Layer 1: Q-Chip Gateway Silicon

The proposed hardware co-processor or motherboard-level gateway that controls boundary crossing into quantum-compatible execution corridors through a hardware register gate `G(t)`.

### Layer 2: Q-GPU Acceleration Tier

The acceleration layer intended to offload matrix reconstruction, Kalman-style smoothing, covariance math, and Riemann phase unwrapping to local GPU tensor hardware.

### Layer 3: Distributed Q-Node SRE Racks

Regional orchestration nodes that host observer pools, trust matrices, local lineage caches, and weighted Byzantine voting pools.

### Layer 4: Quantum ISP Mesh Ledger Fabric

The future decentralized communication fabric for continuity-aware routing, validation, provenance, and long-range infrastructure access.

## Twelve Operational Axioms

1. Operational reconstruction is more important than exact ontological state knowledge.
2. Unknown state behavior can be managed through trajectory tracking.
3. Runtime determinism can emerge from probabilistic systems through orchestration.
4. Compute, memory, and communication lanes should be allocated by quality and health.
5. Quantum-adjacent processors require continuous observability and predictive diagnostics.
6. A classical digital twin can preserve useful operational behavior without cloning hidden state.
7. Infrastructure-aware scaling matters more than brittle idealized mathematics.
8. Commercial value depends on measurable operational deltas.
9. Distributed systems primitives apply naturally to probabilistic information architectures.
10. Soft determinism is sufficient when continuity corridors are bounded and reliable.
11. Breakthrough systems require cross-disciplinary synthesis across physics, runtime scheduling, and economics.
12. Computing progress can be decoupled from brute-force hardware scaling by managing probabilistic systems at runtime.

## Fifty-System Principle Directory

### Tier 1: Zero-Trust Cryptographic Provenance Ledgers

1. AEGIS Proof Link
2. Birth Certificate Ledger
3. Tamper-Proof History Chain
4. Forward-Secure Key Ratchet
5. Boundary Event Ledger

### Tier 2: Reconstructive Operational Core

6. AEGIS Runtime
7. QSR: Quantum State Reconstruction
8. PSR: Proxy State Reconstruction
9. Operational Proxy Transfer Engine, OPTE
10. Solve-for-X Reconstruction
11. Proxy Recall Engine
12. Quantum-Classical Boundary Runtime

### Tier 3: Memory Storage Tiering and Cache Networks

13. Proxy Cache
14. Core Caches
15. Ghost State Reserve
16. Semantic Cache Reserve
17. Meaning-Based Compression
18. Hot/Warm/Cold Quantum Memory Tiering

### Tier 4: Observer Ecologies and Hardware Reputation

19. Observer Reputation Matrix
20. Observer Ecology
21. Virtual Observer Nodes
22. Storm Strobing
23. BFT Voting Pool

### Tier 5: Constitutional Operating Governor States

24. STORM_PROTECT
25. PHASE_HOLD
26. ANCHOR_DISPUTE
27. CRYPTO_SEAL
28. CIRCUIT_ABORT
29. SECURITY_LOCKDOWN

Additional recovery gate: `RECOVERY_VALIDATE`

The executable kernel models these as layered bitmask states, so multiple crises can be active at once.

### Tier 6: Environmental Weather and Trajectory Corridors

30. Environmental Weather Model `W(t) = f(T, EM, V, R, L)`
31. Quantum Weather Telemetry
32. Kalman Trajectory Corridor
33. Predictive Lookahead Tracker
34. Drift Corridor System
35. Entropy / Coherence Budgeting Layer

### Tier 7: Global Access Networks and Naming Infrastructure

36. Q-Chip Gateway Silicon
37. Q-GPU Acceleration Tier
38. Q-Node Mesh
39. Q-Sticks
40. Q-Chip Gating Layer
41. Bloch Sphere Testing Layer
42. Fidelity / Coherence Scoring Engine
43. Five-Nines Simulation Targeting
44. Quantum Forensics / Replay Layer
45. Q-Network Mesh Topology
46. Mobile Quantum Access Architecture
47. Q-Gateway / Quantum Modem Concept

### Tier 8: Native .QOM Gateway Networking Map

48. `core.gateway.aegis.qom`
49. `mesh.routing.prd.qom`
50. `ledger.lineage.sre.qom`

## Canonical Runtime Loop

The current implementation lives in `aegis_kernel.py` as `AegisContinuityKernel`.

```text
INCOMING PHYSICAL RAW TELEMETRY
  -> INGEST_TELEMETRY
  -> RECOMPUTE_KAPPA
  -> KINETIC_PROJECTION
  -> MANIFOLD_UNWRAP
  -> ESTIMATE_STATE
  -> VERIFY_QUORUM
  -> CROSS_CHECK_ANCHOR
  -> STATE_GOVERNOR
  -> EMIT_SNAPSHOT
  -> WRITE_LEDGER
SECURE WORKLOAD CONTINUITY METRIC COMMITTED
```

## Current Engineering Direction

The next priority is executable rigor:

- deterministic regression scenarios,
- Monte Carlo failure modeling,
- reproducible result artifacts,
- explicit state-machine tests,
- calibrated target claims,
- eventually a public technical README and architecture diagrams.
