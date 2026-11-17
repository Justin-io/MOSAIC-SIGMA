# INVENTION CANDIDATES: SELECTION, PHYSICS, AND TRADE STUDIES

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Classification:** Invention Evaluation & Subsystem Selection  

---

### 1. The Top Three Selected Inventions
From the 30-candidate interdisciplinary discovery matrix (catalogued in `INTERDISCIPLINARY_DISCOVERY_MATRIX.xlsx`), the three highest-scoring candidates were chosen for full engineering development into the MOSAIC-Σ architecture:

```
+---------------------------------------------------------------------------------------------------+
| TOP THREE MOSAIC-Σ TECHNICAL CONTRIBUTIONS                                                        |
+-----+---------------------------+-------------------------------------+---------------------------+
| Rank| Candidate Title           | Underlying Physical Mechanism       | Target System Role        |
+-----+---------------------------+-------------------------------------+---------------------------+
| 1   | **Adaptive Metasurface    | Varactor-tuned unit-cell phase      | Primary spatial RF        |
|     | Aperture + Bayesian BED** | modulation dynamically focused by   | illumination engine on    |
|     | (Candidate 01 - Score 32) | real-time Information Gain planner  | MOSAIC-WAVE / MOSAIC-CORE |
+-----+---------------------------+-------------------------------------+---------------------------+
| 2   | **In-Situ Multi-Physics   | Autonomous electronic switching     | Instrument drift          |
|     | Self-Calibration Engine** | to on-PCB Short-Open-Load and       | decoupling and metrology  |
|     | (Candidate 04 - Score 32) | Kelvin precision standards          | on MOSAIC-SENSE           |
+-----+---------------------------+-------------------------------------+---------------------------+
| 3   | **Coherent Orthogonal     | Simultaneous high-voltage ultrasound| Multi-physics defect      |
|     | Multi-Physics Fusion**    | (acoustic impedance) + wideband RF  | state estimation on       |
|     | (Candidate 03 - Score 30) | (permittivity) + EIS (conductivity) | MOSAIC-SENSE              |
+-----+---------------------------+-------------------------------------+---------------------------+
```

---

### 2. Deep Technical Breakdown: Candidate 01 — Adaptive Metasurface Aperture + Bayesian BED
- **Scientific Foundation:** Reconfigurable intelligent surface theory combined with optimal sequential experimental design (Shannon Information Theory).
- **Physical Mechanism:**
  - An $8 \times 8$ array of microstrip split-ring resonators (SRRs) loaded with Skyworks SMV1231 hyperabrupt junction varactor diodes.
  - By applying reverse bias voltages ($0 - 15\,\text{V}$) via cascaded 74HC595 shift registers, each unit cell's reflection phase $\angle \Gamma_{i,j}(f)$ is continuously steered across $0^\circ$ to $280^\circ$.
  - The resulting interference pattern synthesizes dynamic near-field focal spots, Bessel beams, and phase gradients across the material under test.
- **Autonomous Feedback Loop:**
  - The FPGA Bayesian engine evaluates the current posterior distribution $p(\boldsymbol{\theta} \mid \mathcal{D}_t)$.
  - It searches candidate phase masks $\mathbf{V}_{\text{bias}} \in \mathbb{R}^{64}$ that maximize Expected Information Gain (EIG) at the predicted defect boundary.
  - The aperture shifts illumination dynamically to confirm or refute the defect hypothesis in minimum steps.

---

### 3. Deep Technical Breakdown: Candidate 04 — In-Situ Self-Calibration Engine
- **Scientific Foundation:** Vector network analyzer (VNA) 12-term error correction models and ratiometric bridge metrology.
- **Physical Mechanism:**
  - RF Domain: High-isolation RF switches (Analog Devices ADG904, DC to $2.5\,\text{GHz}$, and Hittite/ADI microwave switches up to $6\,\text{GHz}$) select between the Material Probe (DUT) and precision on-board microstrip reference standards:
    1. Short: Low-inductance via array to ground.
    2. Open: Truncated open-circuit microstrip stub.
    3. Load: Two $100\,\Omega$ $0.1\%$ thin-film microwave resistors in parallel ($50\,\Omega \pm 0.05\,\Omega$).
    4. Through: Calibrated transmission delay line.
  - EIS Domain: Low-leakage analog multiplexers route the AD5940 excitation and TIA sensing terminals to precision $100\,\Omega$, $1\,\text{k}\Omega$, and $100\,\text{k}\Omega$ $0.05\%$ $10\,\text{ppm/}^\circ\text{C}$ Vishay metal foil resistors and $0.1\%$ C0G capacitors.
  - Drift Elimination: Every 10 seconds or upon detecting a $\Delta T > 0.5^\circ\text{C}$ via on-board digital temperature sensors (TI TMP117, $\pm 0.1^\circ\text{C}$), the system executes an automated 2-millisecond self-calibration routine, calculating:
    $$\Gamma_{\text{actual}} = \frac{\Gamma_{\text{measured}} - e_{00}}{e_{01} + e_{11}\Gamma_{\text{measured}}}$$
    This guarantees that temperature excursions or cable bending are never falsely attributed to target material defects.

---

### 4. Deep Technical Breakdown: Candidate 03 — Coherent Orthogonal Multi-Physics Fusion
- **Scientific Foundation:** Multi-modal sensor fusion across distinct physical constitutive relations (Maxwell's equations, elastodynamics, and electrochemical transport).
- **Physical Mechanism:**
  - Acoustic Channel: STHV748 high-voltage pulser transmits $\pm 100\,\text{V}$ sub-50 ns pulses to a $2.5\,\text{MHz}$ piezoelectric transducer; AD8331 variable-gain LNA amplifies return echoes with time-gain compensation, resolving deep delaminations via acoustic impedance mismatch $\Delta Z$.
  - Dielectric/RF Channel: ADF4351 synthesizer and LTC5586 I/Q demodulator illuminate the target via the MOSAIC-WAVE metasurface, recording complex reflection $\Gamma(f) = I + jQ$ between $1.0 - 6.0\,\text{GHz}$, resolving near-surface fiber breakages and matrix micro-cracks.
  - Electrochemical Channel: AD5940 executes multi-frequency 4-wire Kelvin EIS ($0.1\,\text{Hz} - 200\,\text{kHz}$), measuring real and imaginary interfacial impedance $Z^*(\omega)$, resolving adhesive chemical cross-linking degradation and moisture saturation.
- **Fusion Decision Matrix:**
  $$\begin{bmatrix} \text{Delamination Depth } d \\ \text{Moisture Volume Fraction } \phi_w \\ \text{Fiber Alignment Angle } \theta_f \end{bmatrix} = \mathcal{F}_{\text{Bayes}}\left( \mathbf{y}_{\text{US}}(t), \mathbf{y}_{\text{RF}}(\omega), Z_{\text{EIS}}(\omega) \right)$$
  The three modalities provide non-overlapping physical constraints, eliminating parameter degeneracies.
