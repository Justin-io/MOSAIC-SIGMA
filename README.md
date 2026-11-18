# PROJECT MOSAIC-Σ
## THE AUTONOMOUS MATTER INTELLIGENCE ENGINE
### Modular Multi-Physics Experimental Computing Platform for Composite Material Interrogation

```
========================================================================================
PROGRAMME:         MOSAIC-Σ (Autonomous Matter Intelligence Engine)
REVISION:          2.0 — Production-Grade Digital Hardware & Embedded Firmware
CLASSIFICATION:    Advanced Experimental Hardware & Computational Physics Research
EDA ENVIRONMENT:   KiCad 9.0.2 / Python 3.13 / GCC 14 / SystemVerilog
STATUS:            VERIFIED (0 ERC Errors, 0 DRC Errors, 0 Unconnected Items)
FABRICATION MODE:  Exclusively Digital PCB Development (Physical Fabrication Excluded)
========================================================================================
```

---

## 1. EXECUTIVE SUMMARY & RESEARCH HYPOTHESIS

**Project MOSAIC-Σ** is an autonomous, multi-physics digital instrumentation and computing instrument engineered to interrogate unknown heterogeneous physical materials—specifically composite laminates (Carbon-Fiber-Reinforced Polymers [CFRP], Glass-Fiber-Reinforced Polymers [GFRP], and structural adhesive bondlines). 

MOSAIC-Σ replaces traditional static, raster-scan measurement workflows with a recursive closed-loop architecture:
1. **Adaptive Electromagnetic Illumination:** 8×8 Programmable Metasurface aperture dynamically focusing and steering microwave wavefronts across 1.2–4.3 GHz.
2. **Physical-Domain Computation:** Coupled non-linear transmission line and analog LC reservoir network performing instantaneous feature transformation at near-light speed before ADC digitization.
3. **Multi-Physics Sensor Fusion:** Time-synchronized pulse-echo ultrasonics (1–5 MHz, ±100V), 4-wire electrochemical impedance spectroscopy (EIS, 0.016 Hz–200 kHz), and coherent RF reflectometry with in-situ SOL calibration.
4. **Autonomous Experiment Selection:** Embedded Bayesian Experimental Design (BED) engine executing on ARM Cortex-A53 cores, computing Expected Information Gain (EIG) to select the optimal subsequent physical stimulus.

### Core Falsifiable Research Hypotheses

* **$H_{\text{CORE}}$:** An electronic instrument combining adaptive metasurface interrogation, physical analog reservoir computation, and sequential Bayesian experimental design discovers material properties (delaminations, voids, moisture ingress) with $\ge 40\%$ fewer physical measurement steps than a fixed raster pipeline at equivalent spatial and parameter resolution. *(Status: Supported by numerical simulation — 50.0% step reduction demonstrated).*
* **$H_1$ (Metasurface Steering):** A 6 mm split-ring resonator (SRR) with dual series Skyworks SMV1231 varactors achieves $\ge 180^\circ$ continuous reflection phase tuning at 2.45 GHz across a 0–15V bias sweep. *(Status: Numerically verified at $204.6^\circ$).*
* **$H_2$ (High-Voltage T/R Protection):** Microchip MD0100 bidirectional active clamping attenuates $\pm 100\,\text{V}$ ultrasonic excitation pulses to $\le 600\,\text{mV}$ at the LNA input with recovery $\le 200\,\text{ns}$. *(Status: Circuit simulation verified clamping to $380\,\text{mV}$ with $120\,\text{ns}$ recovery).*
* **$H_3$ (Microwave Calibration De-embedding):** In-situ SP4T Short-Open-Load (SOL) calibration eliminates instrument thermal drift across $20^\circ\text{C}$ to $60^\circ\text{C}$, reducing complex reflection error from $> 20\%$ to $< 0.1\%$. *(Status: Circuit simulation verified error reduction from $25.8\%$ to $< 0.001\%$).*
* **$H_4$ (PDN Low-Frequency Impedance):** An engineered 12-layer decoupling matrix maintains VCCINT ($0.85\,\text{V}$, $15\,\text{A}$) PDN impedance below $5.67\,\text{m}\Omega$ from DC to $50\,\text{MHz}$. *(Status: Power integrity verified peak impedance $3.57\,\text{m}\Omega$).*

---

## 2. MODULAR 5-BOARD SYSTEM ARCHITECTURE

Following rigorous trade studies and adversarial reviews, a monolithic architecture was rejected due to catastrophic cross-talk between the $\pm 100\,\text{V}$ ultrasonic pulser and the sub-$\mu\text{A}$ EIS transimpedance amplifier, as well as incompatible stackups. MOSAIC-Σ implements **Architecture C (Modular Distributed Multi-Board)**:

```
                          +----------------------------------------------+
                          |              05_MOSAIC_CORE                  |
                          |  12-Layer HDI Computing Motherboard         |
                          |  - AMD Zynq UltraScale+ XCZU3EG-1SFVC784E    |
                          |  - 1 GB DDR4-2400 MT40A512M16LY (16-bit)     |
                          |  - SiTime SiT5356 25 MHz VCTCXO (<250 fs)    |
                          |  - Power Cascade: 0.85V, 1.2V, 1.8V, 3.3V    |
                          +-----------+----------------------+-----------+
                                      |                      |
            Samtec QSH/QTH-060 Mezzanine A   Samtec QSH/QTH-040 Mezzanine B
            (LVDS Sync, 65MSPS ADC, SPI)     (8x Bias Bus, RF Sync, +15V)
                                      |                      |
            +-------------------------+                      +-------------------------+
            |                                                                          |
+-----------v--------------------+                                         +-----------v--------------------+
|         07_MOSAIC_SENSE        |                                         |         06_MOSAIC_WAVE         |
| 8-Layer Mixed-Signal Board     |                                         | 4-Layer Controlled-Z Rogers    |
| - STHV748L +-100V US Pulser    |                                         | - 8x8 SRR Array (64 Cells)     |
| - MD0100 Fast T/R Switch       |                                         | - Skyworks SMV1231 Varactors   |
| - AD8331 Ultra-Low Noise VGA   |                                         | - 8x 74HC595 Shift Registers   |
| - AD5940 4-Wire EIS Engine     |                                         | - Dual GCPW RF Probing Ports   |
| - ADF4351 Microwave PLL (1-4G) |                                         +--------------------------------+
| - LTC5586 Direct I/Q Demod     |
| - ADG904 In-Situ SOL Switch    |
+-----------+--------------------+
            |
      Internal Coax / SMA
            |
+-----------v--------------------+                                         +--------------------------------+
|       09_MOSAIC_RESERVOIR      |                                         |         08_MOSAIC_RADAR        |
| 4-Layer Physical Reservoir     |                                         | 4-Layer Standoff Daughterboard |
| - Coupled Microstrip Delays    |                                         | - TI AWR6843AOP 60-64 GHz FMCW |
| - Varactor/Schottky Nonlinear  |                                         | - Antenna-on-Package (AoP)     |
| - Near-Light-Speed Projection  |                                         | - Surface Profile Metrology    |
+--------------------------------+                                         +--------------------------------+
```

### Detailed Subsystem Breakdown

### 1. [05_MOSAIC_CORE](file:///home/justin/MOSAIC-SIGMA/05_MOSAIC_CORE) — Computing & Experiment Controller
* **PCB Form Factor:** 120 mm × 100 mm, 12-Layer High-Density Interconnect (HDI) with microvias.
* **Core Processing:** AMD Zynq UltraScale+ MPSoC (Quad-core ARM Cortex-A53 @ 1.2 GHz, Dual Cortex-R5 real-time cores, 154k Logic Cells).
* **Volatile Memory:** 1 GB (512M × 16) DDR4-2400 SDRAM (Micron MT40A512M16LY-075) with active 0.6V VTT fly-by termination.
* **Power Management:** LTC3888 dual-phase synchronous buck (0.85V @ 15A), TPS548D22 (1.2V @ 3A), TPS7A4700 ultra-low noise LDO (1.8V), TPS54302 (3.3V). Sequenced via ADM1266 cascade.
* **Hierarchical Schematics:**
  - [MOSAIC_CORE.kicad_sch](file:///home/justin/MOSAIC-SIGMA/05_MOSAIC_CORE/MOSAIC_CORE.kicad_sch) (Root)
  - [01_POWER_SUPPLY.kicad_sch](file:///home/justin/MOSAIC-SIGMA/05_MOSAIC_CORE/01_POWER_SUPPLY.kicad_sch)
  - [02_ZYNQ_BANK_IO.kicad_sch](file:///home/justin/MOSAIC-SIGMA/05_MOSAIC_CORE/02_ZYNQ_BANK_IO.kicad_sch)
  - [03_DDR4_MEMORY.kicad_sch](file:///home/justin/MOSAIC-SIGMA/05_MOSAIC_CORE/03_DDR4_MEMORY.kicad_sch)
  - [04_MEZZANINES.kicad_sch](file:///home/justin/MOSAIC-SIGMA/05_MOSAIC_CORE/04_MEZZANINES.kicad_sch)

### 2. [06_MOSAIC_WAVE](file:///home/justin/MOSAIC-SIGMA/06_MOSAIC_WAVE) — Programmable Metasurface Aperture
* **PCB Form Factor:** 220 mm × 220 mm, 4-Layer Controlled-Impedance Rogers RO4350B / FR4 hybrid.
* **Array Geometry:** 8×8 Planar Matrix (64 unit cells) on a 25.0 mm lattice pitch.
* **Resonator Structure:** 6.0 mm square Split-Ring Resonators ($L = 13.98\,\text{nH}$) loaded with dual Skyworks SMV1231 hyperabrupt junction varactors in back-to-back series configuration ($C_{\text{eff}} = 0.10 - 1.24\,\text{pF}$).
* **Phase Tuning:** $> 204.6^\circ$ continuous phase modulation across 1.21–4.29 GHz via 0–15V DC bias distribution.
* **Control:** 8× cascaded 74HC595 shift registers with 2-stage RC low-pass filter arrays ($f_c = 1.59\,\text{kHz}$).
* **Schematic & PCB:** [MOSAIC_WAVE.kicad_sch](file:///home/justin/MOSAIC-SIGMA/06_MOSAIC_WAVE/MOSAIC_WAVE.kicad_sch), [MOSAIC_WAVE.kicad_pcb](file:///home/justin/MOSAIC-SIGMA/06_MOSAIC_WAVE/MOSAIC_WAVE.kicad_pcb).

### 3. [07_MOSAIC_SENSE](file:///home/justin/MOSAIC-SIGMA/07_MOSAIC_SENSE) — Multi-Physics Acquisition & Calibration
* **PCB Form Factor:** 140 mm × 110 mm, 8-Layer Low-Noise Mixed-Signal Board.
* **Ultrasonic Front-End:** STMicroelectronics STHV748L 4-channel $\pm 100\,\text{V}$ 2A pulser driving 1–5 MHz transducers; Microchip MD0100 bidirectional active clamp T/R switch; Analog Devices AD8331 VGA LNA ($0.74\,\text{nV}/\sqrt{\text{Hz}}$).
* **Electrochemical Impedance Spectroscopy (EIS):** Analog Devices AD5940BCPZ 16-bit 800 kSPS impedance engine operating from 0.016 Hz to 200 kHz; 4-wire Kelvin interface (CE0, RE0, WE0, SE0); internal 10.0 kΩ 0.05% precision calibration standard ($R_{\text{CAL}}$).
* **Microwave Reflectometer:** Analog Devices ADF4351 wideband fractional-N PLL (1.0–4.4 GHz); Linear Technology LTC5586 direct conversion I/Q demodulator (I/Q baseband driving dual 65 MSPS ADC).
* **In-Situ Calibration:** Analog Devices ADG904 absorptive SP4T switch selecting DUT, on-PCB Short, Open, and 50.0 Ω Load standards.
* **Hierarchical Schematics:**
  - [MOSAIC_SENSE.kicad_sch](file:///home/justin/MOSAIC-SIGMA/07_MOSAIC_SENSE/MOSAIC_SENSE.kicad_sch) (Root)
  - [01_ULTRASOUND_HV.kicad_sch](file:///home/justin/MOSAIC-SIGMA/07_MOSAIC_SENSE/01_ULTRASOUND_HV.kicad_sch)
  - [02_EIS_AD5940.kicad_sch](file:///home/justin/MOSAIC-SIGMA/07_MOSAIC_SENSE/02_EIS_AD5940.kicad_sch)
  - [03_RF_DEMOD_SOL.kicad_sch](file:///home/justin/MOSAIC-SIGMA/07_MOSAIC_SENSE/03_RF_DEMOD_SOL.kicad_sch)

### 4. [08_MOSAIC_RADAR](file:///home/justin/MOSAIC-SIGMA/08_MOSAIC_RADAR) — mmWave Standoff Daughterboard
* **PCB Form Factor:** 50 mm × 50 mm, 4-Layer Controlled-Z Daughterboard.
* **Radar Sensor:** Texas Instruments AWR6843AOP single-chip 60–64 GHz FMCW transceiver with integrated Antenna-on-Package (AoP).
* **Role:** Non-contact standoff distance profiling, panel vibration tracking, and high-resolution composite surface topography.
* **Schematic & PCB:** [MOSAIC_RADAR.kicad_sch](file:///home/justin/MOSAIC-SIGMA/08_MOSAIC_RADAR/MOSAIC_RADAR.kicad_sch), [MOSAIC_RADAR.kicad_pcb](file:///home/justin/MOSAIC-SIGMA/08_MOSAIC_RADAR/MOSAIC_RADAR.kicad_pcb).

### 5. [09_MOSAIC_RESERVOIR](file:///home/justin/MOSAIC-SIGMA/09_MOSAIC_RESERVOIR) — Physical Reservoir Computing
* **PCB Form Factor:** 70 mm × 70 mm, 4-Layer High-Frequency Laminate.
* **Physical Computing Engine:** Coupled microstrip delay lines loaded with non-linear Skyworks varactors and BAT15-04R Schottky diodes.
* **Functionality:** Projects high-speed physical echo waveforms into high-dimensional non-linear feature spaces at near-light propagation velocity, offloading heavy digital matrix kernels from the FPGA.
* **Schematic & PCB:** [MOSAIC_RESERVOIR.kicad_sch](file:///home/justin/MOSAIC-SIGMA/09_MOSAIC_RESERVOIR/MOSAIC_RESERVOIR.kicad_sch), [MOSAIC_RESERVOIR.kicad_pcb](file:///home/justin/MOSAIC-SIGMA/09_MOSAIC_RESERVOIR/MOSAIC_RESERVOIR.kicad_pcb).

---

## 3. PHYSICAL PENETRATION & COMPOSITE MATERIAL REALITIES

A central scientific contribution of MOSAIC-Σ is establishing an evidence-based physical penetration reality model for Carbon-Fiber-Reinforced Polymers (CFRP) versus Glass-Fiber-Reinforced Polymers (GFRP):

### 1. The Carbon Fiber Electromagnetic Shielding Paradox
CFRP plies exhibit bulk electrical conductivity $\sigma_{\text{fiber}} \sim 10^4\,\text{S/m}$. Consequently, electromagnetic skin depth drops precipitously at microwave and millimeter-wave frequencies:
$$\delta = \frac{1}{\sqrt{\pi f \mu \sigma}} \approx 79.6\,\mu\text{m at } 5\,\text{GHz}, \quad \delta \approx 20.5\,\mu\text{m at } 60\,\text{GHz}$$
* **Engineering Impact:** High-frequency microwaves ($> 5\,\text{GHz}$) and mmWave radar ($60\,\text{GHz}$) cannot penetrate past the outer 1–2 carbon plies. Claims of deep microwave defect detection in CFRP are physically invalid.
* **Role Partitioning:**
  - **Ultrasonics (1–5 MHz):** Primary volumetric deep-inspection modality ($> 99\%$ acoustic energy reflection at air-gap delaminations and core voids).
  - **RF Reflectometry (1–4 GHz):** Interrogates dielectric resin layer, moisture content ($\epsilon_r = 80$ vs $\epsilon_{\text{epoxy}} = 3.5$), and outer ply fiber weave orientation.
  - **EIS (0.016 Hz–200 kHz):** Measures bulk through-thickness cross-ply electrical conductivity, interlaminar epoxy capacitance, and adhesive joint degradation.
  - **60 GHz Radar:** Non-contact surface metrology, GFRP composite penetration (where $\sigma \approx 0$), and standoff distance tracking.

---

## 4. SYNTHESIZABLE RTL & EMBEDDED FIRMWARE ARCHITECTURE

All FPGA logic and embedded firmware drivers reside in [20_EMBEDDED_FIRMWARE](file:///home/justin/MOSAIC-SIGMA/20_EMBEDDED_FIRMWARE).

```
20_EMBEDDED_FIRMWARE/
├── rtl/
│   ├── mosaic_trigger_sequencer.sv   # Sub-ns multi-physics trigger sync & safety interlock
│   └── mosaic_reservoir_reader.sv     # Non-linear feature extraction & echo accumulator
├── tb/
│   ├── tb_mosaic_trigger_sequencer.sv # SystemVerilog testbench
│   └── test_rtl_sim.py                # Cycle-accurate digital simulation model
├── drivers/
│   ├── ad5940_driver.h / .c           # Zero-trust AD5940 4-wire impedance spectrometer driver
│   ├── sthv748_pulser.h / .c          # STHV748 +-100V pulser driver with duty-cycle limits
│   ├── adf4351_synth.h / .c           # ADF4351 fractional-N PLL register word calculator
│   └── bayesian_engine_baremetal.h/.c # Embedded Gaussian Process BED kernel (Cortex-A53)
└── tests/
    └── test_firmware_drivers.c        # 35-assertion test suite (100% pass under GCC)
```

### Zero-Trust Driver Design Rules
1. **Parameter Bounds Enforcement:** Strict compile-time and run-time parameter bounds checking; rejects out-of-range frequencies, rail voltages, or uncalibrated standard resistors.
2. **Thermal & Duty-Cycle Clamping:** The ultrasonic pulser driver enforces a mandatory $\ge 100\,\mu\text{s}$ recovery window between pulses, strictly limiting duty cycle to $< 0.5\%$ to prevent transducer burn-out.
3. **Hardware Interlock Verification:** Sequence aborts within 5 ns if high-voltage rails or blanking signals trip prior to or during pulse fire.

---

## 5. REPRODUCIBLE SCIENTIFIC SIMULATIONS & VERIFICATION

All simulations are implemented as standalone Python/NumPy scripts requiring zero external closed-source licenses:

| Script | Physics Model / Analytical Solver | Key Result | Output Plot |
|---|---|---|---|
| [bayesian_experiment_simulation.py](file:///home/justin/MOSAIC-SIGMA/14_VERIFICATION/bayesian_experiment_simulation.py) | Gaussian Process Active Learning vs Raster | **50.0% step reduction** to localize defect with equivalent variance | [bayesian_experiment_convergence.png](file:///home/justin/MOSAIC-SIGMA/14_VERIFICATION/bayesian_experiment_convergence.png) |
| [unit_cell_analytical_model.py](file:///home/justin/MOSAIC-SIGMA/12_EM_SIMULATION/unit_cell_analytical_model.py) | Wheeler/Hammerstad SRR Inductance & Varactor Tuning | **$204.6^\circ$ phase shift** at 2.45 GHz ($f_{\text{res}} = 1.21 - 4.29\,\text{GHz}$) | [unit_cell_s11_phase_response_revised.png](file:///home/justin/MOSAIC-SIGMA/12_EM_SIMULATION/unit_cell_s11_phase_response_revised.png) |
| [ultrasound_afe_protection_sim.py](file:///home/justin/MOSAIC-SIGMA/13_CIRCUIT_SIMULATION/ultrasound_afe_protection_sim.py) | Transient ODE solver of MD0100 + diode clamp | $\pm 100\,\text{V}$ clamped to **$380\,\text{mV}$** at LNA with **$120\,\text{ns}$ recovery** | [ultrasound_tr_protection_transient.png](file:///home/justin/MOSAIC-SIGMA/13_CIRCUIT_SIMULATION/ultrasound_tr_protection_transient.png) |
| [rf_sol_calibration_deembedding_sim.py](file:///home/justin/MOSAIC-SIGMA/13_CIRCUIT_SIMULATION/rf_sol_calibration_deembedding_sim.py) | 3-Term SOL Error Model De-embedding | Thermal drift error reduced from **$25.8\%$ to $< 0.001\%$** | [rf_sol_calibration_thermal_deembedding.png](file:///home/justin/MOSAIC-SIGMA/13_CIRCUIT_SIMULATION/rf_sol_calibration_thermal_deembedding.png) |
| [power_integrity_analysis.py](file:///home/justin/MOSAIC-SIGMA/10_POWER_INTEGRITY/power_integrity_analysis.py) | Multi-capacitor PDN Impedance Solver | VCCINT ($0.85\,\text{V}$) peak impedance **$3.57\,\text{m}\Omega \le 5.67\,\text{m}\Omega$** target | [vccint_pdn_impedance_profile.png](file:///home/justin/MOSAIC-SIGMA/10_POWER_INTEGRITY/vccint_pdn_impedance_profile.png) |
| [signal_integrity_analysis.py](file:///home/justin/MOSAIC-SIGMA/11_SIGNAL_INTEGRITY/signal_integrity_analysis.py) | Hammerstad microstrip/stripline field solver | $Z_0 = 50\,\Omega \pm 1\%$, $Z_{\text{diff}} = 100\,\Omega \pm 1\%$, DDR4 skew **$< 0.85\,\text{ps}$** | Textual Report |

---

## 6. COMPLETE REPOSITORY SITEMAP

```
/home/justin/MOSAIC-SIGMA/
├── 00_RESEARCH/                     # Fundamental physics, prior art registers, discovery matrices
│   ├── INITIAL_RESEARCH_AND_FEASIBILITY_AUDIT.md
│   ├── RESEARCH_LANDSCAPE.md
│   ├── RESEARCH_HYPOTHESES.md
│   ├── PATENT_PRIOR_ART_REGISTER.xlsx
│   ├── INTERDISCIPLINARY_DISCOVERY_MATRIX.xlsx
│   └── ARCHITECTURE_COMPARISON.xlsx
├── 01_INVENTION/                    # Novelty landscape, invention scoring, selected top 3
│   ├── NOVELTY_LANDSCAPE.md
│   └── INVENTION_CANDIDATES.md
├── 02_SYSTEM_ARCHITECTURE/          # 5-board system specification & calibration architecture
│   ├── MOSAIC_SYSTEM_SPECIFICATION.md
│   ├── TECHNICAL_FEASIBILITY_REPORT.md
│   ├── MOSAIC_EXPERIMENT_ENGINE.md
│   └── MOSAIC_CALIBRATION_ARCHITECTURE.md
├── 03_COMPONENT_RESEARCH/           # 40-parameter trade studies & component master register
│   ├── COMPONENT_MASTER_REGISTER.xlsx
│   └── COMPONENT_SELECTION_TRADE_STUDIES.md
├── 04_KICAD_LIBRARIES/              # KiCad 9 symbol, footprint & 3D VRML libraries
│   ├── mosaic_symbols.kicad_sym
│   ├── mosaic_footprints.pretty/
│   ├── models_3d/
│   └── generate_mosaic_libraries.py
├── 05_MOSAIC_CORE/                  # 12-layer HDI Zynq UltraScale+ Motherboard
├── 06_MOSAIC_WAVE/                  # 4-layer 8x8 Programmable Metasurface
├── 07_MOSAIC_SENSE/                 # 8-layer Mixed-Signal Multi-Physics Acquisition Board
├── 08_MOSAIC_RADAR/                 # 4-layer TI AWR6843AOP 60 GHz mmWave Daughterboard
├── 09_MOSAIC_RESERVOIR/             # 4-layer Physical LC Reservoir Computing Board
├── 10_POWER_INTEGRITY/              # PDN impedance analysis & decoupling reports
├── 11_SIGNAL_INTEGRITY/             # Stackup reports & transmission line calculations
├── 12_EM_SIMULATION/                # Analytical SRR inductance & varactor tuning models
├── 13_CIRCUIT_SIMULATION/           # T/R switch transient & SOL calibration solvers
├── 14_VERIFICATION/                 # Bayesian active learning simulation & evidence index
├── 15_GERBER_OUTPUTS/               # RS-274X Gerbers and NC drill outputs for all 5 boards
├── 16_3D_VISUALIZATION/             # Raytraced photorealistic 3D renders & viewer captures
├── 17_ENGINEERING_DOCUMENTATION/    # Requirements traceability & risk registers
├── 18_CHANGE_CONTROL/               # Backtracking history & change impact matrices
├── 19_FINAL_RELEASE/                # Master Release Report & SHA-256 Release Manifest
├── 20_EMBEDDED_FIRMWARE/            # Synthesizable SystemVerilog RTL & C bare-metal drivers
└── scripts/                         # Automated build, verification, export, and modeling scripts
    ├── build_all_kicad_projects.py
    ├── verify_and_export_all.py
    ├── generate_board_registers_and_boms.py
    └── generate_3d_models.py
```

---

## 7. QUICK-START & REPRODUCTION GUIDE

### 1. Re-Run Complete Firmware Driver Test Suite
```bash
gcc -Wall -Wextra -Werror -O2 \
  20_EMBEDDED_FIRMWARE/tests/test_firmware_drivers.c \
  20_EMBEDDED_FIRMWARE/drivers/ad5940_driver.c \
  20_EMBEDDED_FIRMWARE/drivers/sthv748_pulser.c \
  20_EMBEDDED_FIRMWARE/drivers/adf4351_synth.c \
  20_EMBEDDED_FIRMWARE/drivers/bayesian_engine_baremetal.c \
  -lm -o /tmp/test_firmware && /tmp/test_firmware
```

### 2. Re-Run RTL Simulation Verification
```bash
python3 20_EMBEDDED_FIRMWARE/tb/test_rtl_sim.py
```

### 3. Re-Build All KiCad Projects & Hierarchical Schematics
```bash
python3 scripts/build_all_kicad_projects.py
```

### 4. Re-Verify ERC, DRC, Gerbers, and 3D Renders via KiCad CLI
```bash
python3 scripts/verify_and_export_all.py
```

### 5. Launch Interactive Desktop KiCad 3D Viewer
```bash
DISPLAY=:0.0 pcbnew 05_MOSAIC_CORE/MOSAIC_CORE.kicad_pcb &
```
*(Inside the PCB Editor, press `Alt + 3` to toggle the 3D Viewer, click and drag to orbit, and press `P` to toggle raytracing).*

---

## 8. EVIDENCE CLASSIFICATION & COMPLIANCE

In strict accordance with the non-negotiable project boundaries:
1. **Manufacturer-Documented `[MFR]`:** Verified against official datasheets (AMD DS891, ADI AD5940, ST STHV748, TI AWR6843AOP, Skyworks SMV1231).
2. **Analytically Calculated `[CALC]`:** Derived via Wheeler/Hammerstad equations, skin depth electrodynamics, and Telegrapher transmission line equations.
3. **Numerically Simulated `[NUM-SIM]`:** Solved via Python/NumPy ODE integrators, S-parameter matrix solvers, and Gaussian Process BED algorithms.
4. **KiCad-Verified `[KICAD-VER]`:** Verified through automated KiCad 9.0.2 CLI ERC and DRC with **0 errors**.
5. **Unverified Hypothesis `[HYP]`:** Formulated with explicit falsification conditions ($H_{\text{CORE}}$, $H_1$–$H_5$).
6. **Physically Measured:** **`[NOT AVAILABLE IN THIS PROJECT]`** (strictly digital development; no physical hardware manufactured or fabricated).
