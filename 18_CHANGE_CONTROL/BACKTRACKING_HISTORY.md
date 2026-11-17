# BACKTRACKING HISTORY & FAILURE FINGERPRINT REGISTER

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Status:** ACTIVE AUDIT REGISTER  

---

### 1. Backtracking Procedure
In accordance with Part X (The Recursive Backtracking Engine):
- Every detected failure is fingerprinted with a unique identifier.
- Downstream dependencies are traced and marked `STALE — REQUIRES REVALIDATION`.
- Revisions are committed to version control with full traceability.

---

### 2. Backtracking Event Log

#### BACKTRACK-001: Separation of Electromagnetic Metasurface Functions
- **Timestamp:** 2026-11-18T01:54:00Z
- **Triggering Observation:** Literature analysis of Tzarouchis et al. (Nature Comms 2025) and Keshavarz et al. (Nature Comms 2025). Attempting to merge Function A (programmable spatial aperture), Function B (physical non-linear reservoir), and Function C (wave-based analog matrix multiplication) onto a single planar unit cell leads to conflicting physical requirements: aperture needs linear low-loss continuous tuning, while reservoir requires strong inter-cell mutual coupling and non-linearity.
- **Severity Classification:** S4 — Fundamental Architecture Decision.
- **Rollback Level:** Level 5 — System Architecture Rollback.
- **Root Cause:** Over-ambitious integration hypothesis conflating distinct physical wave behaviors.
- **Action Taken:** Partitioned the hardware:
  - MOSAIC-WAVE is dedicated strictly to Function A (spatial aperture illumination).
  - MOSAIC-RESERVOIR is partitioned as an independent shielded daughterboard dedicated to non-linear physical reservoir computation.
- **Artifacts Invalidated & Regenerated:** `MOSAIC-SIGMA-AUDIT-001`, `MOSAIC_SYSTEM_SPECIFICATION.md`, `ARCHITECTURE_COMPARISON.xlsx`.
- **Status:** RESOLVED & COMMITTED.

#### BACKTRACK-002: Rejection of Discrete Memristors for Primary Signal Path
- **Timestamp:** 2026-11-18T01:55:00Z
- **Triggering Observation:** Component feasibility audit on discrete memristor availability (Knowm memristor packages). Devices exhibit >25% device-to-device variability, extreme thermal drift, and total lack of standard SMD production packaging in 2026.
- **Severity Classification:** S3 — Subsystem Feasibility Failure.
- **Rollback Level:** Level 4 — Subsystem Architecture Rollback.
- **Root Cause:** Laboratory-stage academic devices are not integration-ready for commercial mixed-signal PCB manufacturing.
- **Action Taken:** Replaced discrete memristive crossbar with deterministic microstrip coupled ring resonators loaded with hyperabrupt junction varactor diodes (Skyworks SMV1231) and Schottky barrier diodes (SMS7621).
- **Artifacts Invalidated & Regenerated:** `MOSAIC_RESERVOIR_MODEL.md`, `INTERDISCIPLINARY_DISCOVERY_MATRIX.xlsx`.
- **Status:** RESOLVED & COMMITTED.

#### BACKTRACK-003: Physical Separation of High-Voltage Pulser and Sensitive EIS
- **Timestamp:** 2026-11-18T01:56:00Z
- **Triggering Observation:** Adversarial Reviewer B objection: Placing $\pm 100\,\text{V}$ 2 A fast pulser (STHV748) and sub-microampere EIS transimpedance amplifier (AD5940) on the same board as a high-density DDR4 memory bus creates catastrophic electromagnetic cross-talk and necessitates conflicting 12-layer HDI vs. RF stackups.
- **Severity Classification:** S3 — Subsystem Electrical Isolation Issue.
- **Rollback Level:** Level 5 — Board Partitioning Rollback.
- **Root Cause:** Violating noise domain isolation in early monolithic draft.
- **Action Taken:** Formally locked Architecture C:
  - MOSAIC-CORE retains digital processing and DDR4 memory on a 12-layer FR-4 board.
  - MOSAIC-SENSE houses analog instrumentation on an 8-layer board with isolated ground split planes and opto-isolated trigger lines.
  - MOSAIC-WAVE houses the RF metasurface on a 4-layer low-loss Rogers/Isola hybrid laminate.
- **Artifacts Invalidated & Regenerated:** `MOSAIC_CORE_ARCHITECTURE.md`, `MOSAIC_SENSE_ARCHITECTURE.md`, `MOSAIC_WAVE_ARCHITECTURE.md`.
- **Status:** RESOLVED & COMMITTED.
