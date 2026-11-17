# ENGINEERING LIMITATIONS & ASSUMPTIONS REGISTER

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Document ID:** MOSAIC-DOC-LIM-001  
**Revision:** 1.0  
**Classification:** Scientific Rigor & Transparent Technical Boundaries  

---

### 1. Transparent Engineering Boundaries
In accordance with Part II Section 3 (Non-Negotiable Project Boundaries), every limitation of this digital design programme is recorded and classified:

```
+---------------------------------------------------------------------------------------------------+
| PROJECT MOSAIC-Σ FORMAL LIMITATIONS LEDGER                                                        |
+---------+---------------------------------+-----------------------+-------------------------------+
| Limit ID| Operational / Physical Domain   | Identified Limitation | Systemic Impact & Mitigation  |
+---------+---------------------------------+-----------------------+-------------------------------+
| **LIM-01**| RF Microwave Penetration in CFRP| Skin depth $< 80\,\mu\text{m}$ at 5GHz  | RF cannot detect deep flaws   |
|         |                                 | due to carbon conductivity    | in CFRP. Ultrasound is used as|
|         |                                 | ($\sigma \sim 10^4\,\text{S/m}$) | primary volumetric deep probe.|
+---------+---------------------------------+-----------------------+-------------------------------+
| **LIM-02**| mmWave Radar Penetration        | Zero penetration in CFRP;     | TI AWR6843 is strictly limited|
|         |                                 | High surface reflection       | to surface standoff, warping, |
|         |                                 | at 60-64 GHz                  | and non-conductive GFRP.      |
+---------+---------------------------------+-----------------------+-------------------------------+
| **LIM-03**| High-Voltage Ultrasonic Duty Cyc| STHV748 pulser thermal limits | Software locks PRF <= 10 kHz  |
|         |                                 | restrict continuous duty      | to maintain average junction  |
|         |                                 | cycle to <= 0.5%              | temperature below 85°C.       |
+---------+---------------------------------+-----------------------+-------------------------------+
| **LIM-04**| AD5940 EIS High-Frequency Limit | Internal TIA bandwidth rolls  | Frequencies > 200 kHz are     |
|         |                                 | off above 200 kHz (1 MHz ext) | handed off to the coherent    |
|         |                                 |                               | RF reflectometer channel.     |
+---------+---------------------------------+-----------------------+-------------------------------+
| **LIM-05**| Discrete Memristor Maturity     | Commercial discrete ReRAM     | Replaced by deterministic     |
|         |                                 | memristors exhibit >25% drift | non-linear microstrip LC      |
|         |                                 | and zero standard SMD packages| transmission line networks.   |
+---------+---------------------------------+-----------------------+-------------------------------+
| **LIM-06**| Digital Simulation Environment  | Fabrication, assembly, and    | All performance claims are    |
|         |                                 | physical measurements are     | classified as `[CALC]`,       |
|         |                                 | strictly excluded by charter  | `[NUM-SIM]`, or `[KICAD-VER]`.|
+---------+---------------------------------+-----------------------+-------------------------------+
```

---

### 2. Physical Measurement Status Notice
> [!CAUTION]
> **NO PHYSICAL MEASUREMENTS ARE CLAIMED OR REPORTED.**
> This project is conducted exclusively as a digital hardware engineering and numerical simulation research investigation. All reported metrics reflect analytical calculations, circuit SPICE models, electromagnetic formulations, and automated KiCad 9.0.2 DRC/ERC verification suites.
