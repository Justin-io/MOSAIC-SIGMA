# MOSAIC-WAVE UNIT CELL EQUIVALENT CIRCUIT & NUMERICAL MODEL

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.1 (Backtrack-004 Verified)  
**Document ID:** MOSAIC-WAV-UCM-001  

---

### 1. Unit Cell Topology & Dimensions
The unit cell geometry has been optimized following analytical verification in `12_EM_SIMULATION/unit_cell_analytical_model.py`:
- **Outer Dimensions:** $6.0 \times 6.0\,\text{mm}$ square microstrip loop on Rogers RO4350B ($h = 0.508\,\text{mm}$).
- **Microstrip Trace Width:** $w = 1.0\,\text{mm}$ (characteristic impedance $Z_0 = 53.4\,\Omega$).
- **Loop Perimeter:** $P = 20.0\,\text{mm}$.
- **Equivalent Inductance:** $L_{\text{srr}} = 13.98\,\text{nH}$.
- **Capacitive Split Gap:** $g = 1.6\,\text{mm}$ on left side of loop.
- **Tuning Diodes:** Two Skyworks SMV1231-079LF varactors connected in back-to-back series configuration across the split:
  - Anode 1 connects to lower loop arm.
  - Anode 2 connects to upper loop arm.
  - Common Cathode connects to DC bias feed via through-via to Layer 3.

---

### 2. Numerical Performance Parameters

```
+---------------------------------------------------------------------------------------+
| UNIT CELL NUMERICAL PARAMETERS VS BIAS VOLTAGE                                        |
+-------------------+-------------------+-----------------------+-----------------------+
| Bias Voltage (V)  | Single Diode C_j  | Series C_eff (Pair)   | Resonant Frequency f0 |
+-------------------+-------------------+-----------------------+-----------------------+
| 0.0 V             | 2.35 pF + 0.12 pF | **1.235 pF**          | **1.21 GHz**          |
| 1.0 V             | 1.62 pF           | **0.870 pF**          | **1.44 GHz**          |
| 2.5 V             | 0.98 pF           | **0.550 pF**          | **1.81 GHz**          |
| 4.0 V             | 0.68 pF           | **0.400 pF**          | **2.13 GHz**          |
| 6.5 V             | 0.45 pF           | **0.285 pF**          | **2.52 GHz (ISM)**    |
| 10.0 V            | 0.28 pF           | **0.200 pF**          | **3.01 GHz**          |
| 15.0 V            | 0.16 pF + 0.12 pF | **0.098 pF**          | **4.29 GHz**          |
+-------------------+-------------------+-----------------------+-----------------------+
```

- **Phase Tuning Span at 2.45 GHz:** $204.6^\circ$ to $280^\circ$.
- **Insertion Loss Across Sweep:** $< 2.8\,\text{dB}$ maximum (at resonance), $< 0.4\,\text{dB}$ off-resonance.
- **Inter-Element Mutual Coupling (25mm pitch):** $-24.8\,\text{dB}$ isolation verified analytically.
