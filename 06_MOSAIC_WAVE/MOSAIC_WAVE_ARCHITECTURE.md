# MOSAIC-WAVE ARCHITECTURE SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Board ID:** MOSAIC-WAVE ($8 \times 8$ Programmable Metasurface Aperture)  
**Revision:** 1.1 (Post Backtrack-004 Revision)  
**EDA Project:** `06_MOSAIC_WAVE/MOSAIC_WAVE.kicad_pro`  

---

### 1. Functional Responsibilities
MOSAIC-WAVE implements **Function A (Programmable Interrogation Aperture)** of the system hypothesis:
1. **Adaptive Spatial Wavefront Synthesis:** Synthesizes localized near-field microwave focal spots, phase gradients, and Bessel beams to illuminate the composite material under test with controlled incident angles and spatial wavefront shapes.
2. **Frequency-Coded Spatial Probing:** Translates bias voltage patterns from the MOSAIC-CORE Bayesian engine into spatial reflection phase distributions $\angle \Gamma_{i,j}(f)$, enabling spatial scanning without physical probe movement.
3. **Dual-Polarization Operation:** Orthogonal feeds probe carbon-fiber anisotropy and fiber orientation across the $1.0 - 6.0\,\text{GHz}$ band.

---

### 2. Physical Array Architecture & Dimensions
- **Aperture Topology:** $8 \times 8$ planar square array (64 unit cells total).
- **Physical Dimensions:**
  - Board Size: $220.0 \times 220.0\,\text{mm}$ ($8.66 \times 8.66\,\text{inches}$).
  - Unit-Cell Pitch: $d = 25.0\,\text{mm}$ ($0.984\,\text{inches}$).
  - Active Aperture: $200.0 \times 200.0\,\text{mm}$.
- **Substrate System:** 4-Layer Controlled-Impedance Hybrid Stackup:
  - Top RF Layer: Rogers RO4350B LoPro core ($h = 0.508\,\text{mm}$, $\varepsilon_r = 3.66$, $\tan\delta = 0.0037$).
  - Ground Reference: Solid copper RF ground plane on Layer 2 (`RF_GND`).
  - Core & Prepreg: Low-cost FR-4 backing for mechanical stiffness and digital bias routing on Layer 3 and Layer 4.

---

### 3. Cascaded Shift-Register Bias Subsystem
- **Bias Shift Registers:** Eight 8-bit serial-in parallel-out shift registers (Nexperia 74HC595PW) in TSSOP-16 packages cascaded in series.
- **Serial Interface:** Driven by MOSAIC-CORE via Mezzanine Connector B (`SPI_MOSI`, `SPI_SCK`, `LATCH_ENABLE`).
- **Update Latency:** 64 bias bits clocked at $20\,\text{MHz}$ in $< 3.5\,\mu\text{s}$, enabling full metasurface phase mask re-configuration at rates exceeding $50\,\text{kHz}$.
- **Two-Stage RF Isolation Filter:**
  - Every shift register output drives its corresponding unit-cell varactor through a dedicated 2-stage SMD low-pass filter:
    $$R_1 = 47\,\text{k}\Omega, \quad C_1 = 10\,\text{nF}, \quad R_2 = 47\,\text{k}\Omega, \quad C_2 = 10\,\text{nF}$$
  - Cutoff frequency: $f_c \approx 160\,\text{Hz}$.
  - Attenuation at $2.4\,\text{GHz}$: $> 85\,\text{dB}$, completely eliminating digital clock hash from entering the RF resonant cavities.
