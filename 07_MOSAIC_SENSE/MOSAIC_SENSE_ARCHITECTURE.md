# MOSAIC-SENSE ARCHITECTURE SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Board ID:** MOSAIC-SENSE (Multi-Physics Acquisition & Calibration Board)  
**Revision:** 1.0  
**EDA Project:** `07_MOSAIC_SENSE/MOSAIC_SENSE.kicad_pro`  

---

### 1. Functional Responsibilities
MOSAIC-SENSE is the precision mixed-signal instrumentation core of Project MOSAIC-Σ. It integrates four physically orthogonal measurement and calibration channels onto a single shielded 8-layer board:
1. **Coherent RF Vector Reflectometer ($1.0 - 6.0\,\text{GHz}$):** ADF4351 synthesizer + wideband directional coupler + LTC5586 direct I/Q demodulator for complex reflection coefficient $\Gamma(f)$ logging.
2. **Electrochemical Impedance Spectroscopy ($0.016\,\text{Hz} - 200\,\text{kHz}$):** AD5940 4-wire Kelvin interface for measuring complex interfacial dielectric permittivity and adhesive degradation.
3. **High-Voltage Ultrasonic Pulse-Echo ($1.0 - 5.0\,\text{MHz}$):** STHV748 $\pm 100\,\text{V}$ pulser + MD0100 bidirectional T/R clamp + AD8331 ultra-low noise preamplifier with Time-Gain Compensation (TGC).
4. **In-Situ Self-Calibration Standards:** ADG904 SP4T switch selecting between the Material Under Test and on-PCB Short, Open, and $50.0\,\Omega$ thin-film Load standards.

---

### 2. Physical Layout & Ground Partitioning
- **Board Dimensions:** $140.0 \times 110.0\,\text{mm}$ ($5.51 \times 4.33\,\text{inches}$).
- **Stackup:** 8-Layer Mixed-Signal Low-Noise Stackup (Isola 370HR, $1.63\,\text{mm}$ thickness).
- **Domain Splitting:**
  - **High-Voltage Ultrasonic Domain (Zone A - Top Left):** Hosts STHV748 and $\pm 100\,\text{V}$ DC-DC power supply. Isolated by a $1.5\,\text{mm}$ milled PCB air slot from the analog receive section.
  - **Low-Noise Analog Receiver Domain (Zone B - Bottom Left):** Hosts AD8331, MD0100, and AD5940. Enclosed by unbroken analog ground (`AGND`) with star-point single-connection to system digital ground at Mezzanine J1.
  - **RF Microwave Domain (Zone C - Top Right):** Hosts ADF4351, LTC5586, and on-board SOL standards. Solid RF ground plane on Layer 2 with coplanar via shielding fences.
  - **Digital Mezzanine Interface (Zone D - Bottom Right):** Hosts Samtec QTH-060 mezzanine plug, AD9235 65 MSPS ADC, and TI ISO7741 digital isolators.
