# ENGINEERING DECISION LOG & ASSUMPTION LEDGER

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Status:** ACTIVE GOVERNANCE REGISTER  

---

## 1. ENGINEERING DECISION LOG (EDL)

| Decision ID | Date | Affected Subsystem | Baseline Decision | Alternatives Evaluated | Rational & Empirical Justification | Authority |
|---|---|---|---|---|---|---|
| **EDL-001** | 2026-11-18 | Architecture Partition | Architecture C (Hierarchical Modular 3-board family) | Arch A (Monolithic), Arch B (Distributed nodes) | Monolithic creates severe HV-to-analog cross-talk; distributed creates >100us sync jitter. Arch C delivers >80dB isolation and sub-ns sync. | Principal Architect |
| **EDL-002** | 2026-11-18 | MOSAIC-CORE Compute | AMD Zynq UltraScale+ XCZU3EG-1SFVC784E | Artix-7, STM32H7, Discrete NPU | ZU3EG provides quad Cortex-A53 for real-time Linux Bayesian BED + dual Cortex-R5F for deterministic trigger sync + 154k logic cells. | Principal Architect |
| **EDL-003** | 2026-11-18 | MOSAIC-WAVE Unit Cell | Split-Ring Resonator with Skyworks SMV1231 Varactors | PIN Diodes (MACOM), RF MEMS | SMV1231 provides continuous analog phase tuning (>270 deg) at zero DC holding current (reverse bias only), avoiding thermal dissipation on RF aperture. | RF Microwave Lead |
| **EDL-004** | 2026-11-18 | MOSAIC-SENSE EIS | Analog Devices AD5940BCPZ Front-End | Discrete Op-Amp TIA + Lock-in | AD5940 integrates high-speed TIA, 16-bit SAR ADC, and dedicated hardware DFT accelerator in 40-lead LFCSP with documented accuracy. | Precision Lead |
| **EDL-005** | 2026-11-18 | MOSAIC-SENSE Ultrasound | STMicroelectronics STHV748 Pulser + AD8331 LNA | Discrete MOSFET H-bridge + Op-Amp | STHV748 integrates programmable +/-100V 2A pulser with active clamp; AD8331 provides ultra-low noise (0.74 nV/rtHz) with analog TGC gain ramp. | Ultrasonic Lead |
| **EDL-006** | 2026-11-18 | MOSAIC-RADAR Subsystem | TI AWR6843AOP on dedicated optional mezzanine | Integrated directly on SENSE, Completely omitted | mmWave has zero penetration in CFRP; placing it on SENSE would waste expensive board area. Modular mezzanine allows optional use for GFRP and surface metrology. | Systems Architect |
| **EDL-007** | 2026-11-18 | Self-Calibration Method | In-situ on-PCB Short-Open-Load (SOL) + Kelvin resistors | Manual external calibration kits | Eliminates reliance on external bench fixtures; enables autonomous thermal de-embedding every 10 seconds in software. | Metrology Lead |
| **EDL-008** | 2026-11-18 | EDA Tooling Authority | KiCad 9.0.2 exclusively for schematics, layout, DRC, 3D | Altium, Cadence Allegro | Strict compliance with Non-Negotiable Project Boundaries. Native KiCad 9.0.2 CLI and Python API used for automated verification. | Lead EDA Engineer |

---

## 2. ASSUMPTION LEDGER (AL)

| Assumption ID | Category | Assumption Statement | Risk if Invalidated | Validation / Falsification Test | Confidence Level |
|---|---|---|---|---|---|
| **ASM-001** | Electromagnetic | Carbon-fiber laminate plies exhibit planar conductivity $\ge 10^3\,\text{S/m}$. | RF reflectometry cannot penetrate beyond the outer ply ($< 100\,\mu\text{m}$). | Wheeler skin-depth calculation and multi-layer reflection coefficient model. | HIGH (Literature-confirmed) |
| **ASM-002** | Acoustic | Delaminations in composite laminates introduce an air boundary with reflection coefficient $|\Gamma| \ge 0.99$. | Ultrasonic echo amplitude may be insufficient for thin kissing bonds. | 1D wave elastodynamic simulation with acoustic impedance mismatch. | HIGH (Physical First Principles) |
| **ASM-003** | Algorithmic | Expected Information Gain (EIG) can be evaluated in $< 5\,\text{ms}$ on ARM Cortex-A53 using discretized candidate actions. | Bayesian scheduler will stall real-time measurement loop. | Python/C benchmark script evaluating 100 candidate actions on target processor. | HIGH (Simulated) |
| **ASM-004** | Electrical | 2-stage RC low-pass filters ($100\,\text{k}\Omega, 10\,\text{nF}$) attenuate 74HC595 shift-register digital clock harmonics by $> 60\,\text{dB}$ at 2.4 GHz. | Digital switching hash will couple into RF metasurface resonators, raising receiver noise floor. | SPICE frequency-domain AC analysis and PCB layout shielding audit. | HIGH (Verified in SPICE) |
| **ASM-005** | Metrology | On-PCB 0.1% thin-film resistors maintain $50\,\Omega \pm 0.2\,\Omega$ return loss $> 20\,\text{dB}$ up to 6.0 GHz without parasitic inductance degradation. | SOL calibration introduces systematic vector directivity errors. | S-parameter simulation of 0402 package parasitics and microstrip landing pads. | MEDIUM (Requires SMT parasitic de-embedding) |
