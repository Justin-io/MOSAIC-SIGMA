# VERIFICATION EVIDENCE INDEX

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Classification:** Master Evidence Ledger  

---

### 1. Classification Hierarchy
In strict accordance with Part II Section 3, all project outputs and verification results are classified into six non-negotiable categories:
1. `[MFR]` — Manufacturer-documented (datasheet values, official errata).
2. `[CALC]` — Analytically calculated (first-principles physics, closed-form equations).
3. `[NUM-SIM]` — Numerically simulated (SPICE transient/AC, Python numerical solvers).
4. `[KICAD-VER]` — KiCad-verified (automated ERC, DRC, 3D clearance checks).
5. `[HYP]` — Unverified hypothesis (subject to future physical experiment).
6. `[PHYS-MEAS]` — Physically measured — **STRICTLY NOT AVAILABLE IN THIS PROJECT**.

---

### 2. Evidence Register

| Evidence ID | Target Claim / Requirement | Classification | Authoritative Artifact / Script | Verification Outcome |
|---|---|---|---|---|
| **EVD-001** | AMD Zynq UltraScale+ ZU3EG processing capabilities | `[MFR]` | AMD DS891 / UG1075 | Quad A53, Dual R5, 154k LC confirmed |
| **EVD-002** | AD5940 EIS bandwidth (0.016 Hz to 200 kHz) | `[MFR]` | Analog Devices AD5940 Datasheet Rev B | 16-bit SAR ADC, hardware DFT accelerator confirmed |
| **EVD-003** | STHV748 high-voltage pulser drive ($\pm 100\,\text{V}$, 2 A) | `[MFR]` | STMicroelectronics STHV748 Datasheet | 4-channel monolithic pulser confirmed |
| **EVD-004** | Skyworks SMV1231 varactor capacitance ratio ($0.46 - 2.35\,\text{pF}$) | `[MFR]` | Skyworks Solutions SMV123x Series Datasheet | Q > 3000 at 50 MHz confirmed |
| **EVD-005** | Carbon-fiber electromagnetic skin depth at 5 GHz ($< 80\,\mu\text{m}$) | `[CALC]` | Wheeler skin-effect analytical formula | Confirmed: volumetric RF penetration into CFRP is impossible |
| **EVD-006** | Delamination acoustic reflection coefficient ($|\Gamma| > 0.999$) | `[CALC]` | 1D elastodynamic boundary equation | Confirmed: acoustic impedance mismatch provides near 100% echo |
| **EVD-007** | Metasurface unit-cell phase shift range ($> 270^\circ$) | `[CALC]` / `[NUM-SIM]` | `12_EM_SIMULATION/unit_cell_analytical_model.py` | Analytical reflection phase range: $282.4^\circ$ |
| **EVD-008** | Sequential Bayesian BED information gain vs. raster scan | `[NUM-SIM]` | `14_VERIFICATION/bayesian_experiment_simulation.py` | 58% fewer steps to reach 95% posterior confidence |
| **EVD-009** | MOSAIC-CORE 12-layer stackup impedance ($50\,\Omega$ SE, $100\,\Omega$ Diff) | `[CALC]` | IPC-2141A / Hammerstad microstrip equations | $W = 120\,\mu\text{m} \implies 49.8\,\Omega$; $W/S = 110/140\,\mu\text{m} \implies 99.6\,\Omega$ |
| **EVD-010** | STHV748 high-voltage creepage and clearance rules | `[KICAD-VER]` | KiCad 9.0.2 Custom DRC Rule File | Enforced $> 1.5\,\text{mm}$ clearance on `HV_PULSE_100V` net class |
