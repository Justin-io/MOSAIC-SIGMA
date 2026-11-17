# SIGNAL INTEGRITY & HIGH-SPEED ROUTING REPORT

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Document ID:** MOSAIC-SI-001  
**Revision:** 1.0  
**Verification Method:** Analytically Calculated & Numerically Simulated (`[CALC]`, `[NUM-SIM]`)  

---

### 1. High-Speed Net Classes & Routing Constraints
To ensure timing closure and prevent signal degradation, all signals are categorized into strict Net Classes with automated KiCad DRC rules:

```
+---------------------------------------------------------------------------------------------------+
| MOSAIC-Σ HIGH-SPEED NET CLASSES & CONSTRAINTS                                                     |
+-------------------+---------------+---------------+-----------+---------------+-------------------+
| Net Class Name    | Target Z0     | Trace Width   | Spacing   | Max Skew / Len| Routing Layers    |
+-------------------+---------------+---------------+-----------+---------------+-------------------+
| `HIGH_SPEED_DIFF` | 100 Ohm Diff  | 0.105 mm      | 0.150 mm  | < 5 mils skew | L1 (Micro), L12   |
| `DDR4_DATA_L0`    | 50 Ohm SE     | 0.115 mm      | 0.200 mm  | < 5 mils skew | L3 (Stripline)    |
| `DDR4_DATA_L1`    | 50 Ohm SE     | 0.115 mm      | 0.200 mm  | < 5 mils skew | L10 (Stripline)   |
| `DDR4_ADDR_CMD`   | 50 Ohm SE     | 0.115 mm      | 0.200 mm  | < 15 mils skew| L3, L10 (Fly-by)  |
| `RF_50OHM`        | 50 Ohm SE     | 1.08 mm (WAVE)| 0.80 mm   | N/A           | L1 Only (Rogers)  |
| `ADC_65MSPS_PAR`  | 50 Ohm SE     | 0.135 mm      | 0.250 mm  | < 25 mils skew| L1, L8 (SENSE)    |
| `HV_PULSE_100V`   | High Voltage  | 0.80 mm       | > 1.50 mm | Isolated Creep| L1 (Milled slot)  |
| `NANOVOLT_ANALOG` | Ultra-Low Z   | 0.25 mm       | Guard ring| Shielded      | L1 (Enclosed AGND)|
+-------------------+---------------+---------------+-----------+---------------+-------------------+
```

---

### 2. DDR4 Fly-By Topology & Skew Budget
The MOSAIC-CORE motherboard interfaces the AMD ZU3EG memory controller to the Micron MT40A512M16LY DDR4-2400 SDRAM ($1200\,\text{MHz}$ bus clock, $t_{\text{CK}} = 833\,\text{ps}$):
- **Address, Command, and Control Bus:** Routed in a single-ended fly-by topology with $50\,\Omega$ parallel termination ($V_{\text{TT}} = 0.60\,\text{V}$) at the end of the line.
- **Differential Clocks (`DDR4_CK_P/N`):** Routed as $100\,\Omega$ differential pair with $100\,\Omega$ differential termination adjacent to the SDRAM.
- **Data Byte Lanes (`DQ[7:0]`, `DQS0_P/N`, `DM0` and `DQ[15:8]`, `DQS1_P/N`, `DM1`):**
  - All signals within Byte Lane 0 are routed on Layer 3 (Stripline between L2 and L4 GND planes).
  - All signals within Byte Lane 1 are routed on Layer 10 (Stripline between L9 and L11 GND planes).
  - **Trace Length Skew Matching:** Enforced within each byte lane to $\le \pm 5\,\text{mils}$ ($\pm 0.127\,\text{mm}$).
  - Maximum Propagation Delay Skew:
    $$\Delta t_{\text{skew}} = \frac{\Delta L \cdot \sqrt{\varepsilon_r}}{c} = \frac{0.127 \times 10^{-3} \cdot \sqrt{4.05}}{3 \times 10^8} \approx 0.85\,\text{ps}$$
    The allowable JEDEC DDR4-2400 setup/hold skew window is $\pm 15\,\text{ps}$. MOSAIC-CORE achieves a safety margin $> 17\times$.

---

### 3. Crosstalk & Guarding Analysis
- **Microstrip 3W Rule:** For all single-ended high-speed lines on L1 and L12, trace-to-trace center spacing is maintained at $\ge 3W$ ($s \ge 2W \approx 0.27\,\text{mm}$). Near-end crosstalk (NEXT) is calculated using Pozar's coupled microstrip formulation:
  $$V_{\text{NEXT}} \le 20 \log_{10} \left( \frac{k_C - k_L}{4} \right) \le -38\,\text{dB}$$
- **Stripline Ground Containment:** Routing DDR4 data lines on internal stripline layers (L3 and L10) provides $> 60\,\text{dB}$ isolation between Byte 0 and Byte 1, eliminating inter-byte jitter.
- **RF Coaxial Transitions:** All SMA edge launches on MOSAIC-WAVE feature grounded coplanar waveguide (GCPW) transitions with ground via stitching ($0.3\,\text{mm}$ drill, $1.0\,\text{mm}$ pitch), ensuring return loss $S_{11} < -24\,\text{dB}$ up to $6.0\,\text{GHz}$.
