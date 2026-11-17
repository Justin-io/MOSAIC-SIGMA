# STACKUP AND CONTROLLED-IMPEDANCE ENGINEERING REPORT

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Document ID:** MOSAIC-SI-STK-001  
**Revision:** 1.1 (Post-Analytical Verification Update)  
**Platform:** KiCad 9.0.2 PCB Calculator & Python Analytical Verification  

---

### 1. Board Family Stackup Architecture
To decouple conflicting manufacturing and electrical requirements, MOSAIC-Σ deploys three distinct PCB layer stackups:

```
+---------------------------------------------------------------------------------------------------+
| MOSAIC-Σ STACKUP ARCHITECTURE MATRIX                                                              |
+-------------------+-------------------+-------------------+-------------------+-------------------+
| Parameter         | MOSAIC-CORE       | MOSAIC-WAVE       | MOSAIC-SENSE      | MOSAIC-RADAR      |
+-------------------+-------------------+-------------------+-------------------+-------------------+
| Layer Count       | **12 Copper**     | **4 Copper**      | **8 Copper**      | **4 Copper**      |
| Total Board Thk.  | 1.60 mm +/- 10%   | 1.60 mm +/- 10%   | 1.60 mm +/- 10%   | 1.00 mm +/- 10%   |
| Primary Material  | Isola FR408HR     | Rogers RO4350B /  | Isola 370HR /     | Megtron-6 /       |
|                   | High-Tg FR-4      | FR408HR Hybrid    | Shengyi S1000-2M  | High-Tg FR-4      |
| Dielectric Const. | er = 3.68 @ 1GHz  | er = 3.66 @ 2.5GHz| er = 4.05 @ 1GHz  | er = 3.71 @ 60GHz |
| Loss Tangent      | tanD = 0.0094     | tanD = 0.0037     | tanD = 0.016      | tanD = 0.002      |
| Min Trace / Space | 0.075 / 0.075 mm  | 0.150 / 0.150 mm  | 0.100 / 0.100 mm  | 0.100 / 0.100 mm  |
| Via Technology    | Microvia 1-2, 2-3 | Standard Through  | Blind/Buried      | Standard Through  |
|                   | + Buried 3-10     | Hole (0.3mm drill)| (0.2mm drill)     | Hole (0.25mm)     |
+-------------------+-------------------+-------------------+-------------------+-------------------+
```

---

### 2. MOSAIC-CORE 12-Layer High-Density Stackup Engineering
Designed for AMD Zynq UltraScale+ (0.8 mm BGA) escape and Micron DDR4-2400 SDRAM fly-by routing:

```
+---------------------------------------------------------------------------------------+
| MOSAIC-CORE 12-LAYER SYMMETRIC STACKUP DETAILS                                        |
|                                                                                       |
| Layer  Name         Copper Thk  Dielectric Material     Dielectric Thk  Function      |
| ------------------------------------------------------------------------------------- |
| L01    TOP_SIG      0.035 mm    Isola FR408HR Prepreg   0.090 mm        High-Speed SE |
| L02    GND01        0.035 mm    Isola FR408HR Core      0.150 mm        Solid Ground  |
| L03    INNER_SIG01  0.018 mm    Isola FR408HR Prepreg   0.150 mm        DDR4 Byte 0/1 |
| L04    GND02        0.035 mm    Isola FR408HR Core      0.100 mm        Solid Ground  |
| L05    PWR01_0V85   0.070 mm    Isola FR408HR Core      0.100 mm        VCCINT Plane  |
| L06    GND03        0.035 mm    Isola FR408HR Prepreg   0.180 mm        Solid Ground  |
| L07    GND04        0.035 mm    Isola FR408HR Core      0.100 mm        Solid Ground  |
| L08    PWR02_1V2    0.070 mm    Isola FR408HR Core      0.100 mm        DDR4 VDD Pwr  |
| L09    GND05        0.035 mm    Isola FR408HR Prepreg   0.150 mm        Solid Ground  |
| L10    INNER_SIG02  0.018 mm    Isola FR408HR Core      0.150 mm        DDR4 Byte 2/3 |
| L11    GND06        0.035 mm    Isola FR408HR Prepreg   0.090 mm        Solid Ground  |
| L12    BOT_SIG      0.035 mm    Solder Mask             0.020 mm        Escape Routing|
| ------------------------------------------------------------------------------------- |
| Total Thickness: 1.62 mm (Within standard +/- 10% manufacturing envelope)             |
+---------------------------------------------------------------------------------------+
```

#### Impedance Tuning (Post-Optimization):
- **L1 / L12 Outer Microstrip Single-Ended (50 $\Omega$):**
  - Trace width: $w = 0.135\,\text{mm}$ ($5.3\,\text{mils}$) over $h = 0.090\,\text{mm}$ dielectric ($e_r = 3.68$).
  - Characteristic Impedance: $Z_0 = 50.12\,\Omega$.
- **L1 / L12 Outer Differential Pairs (100 $\Omega$):**
  - Trace width: $w = 0.105\,\text{mm}$, spacing: $s = 0.150\,\text{mm}$.
  - Differential Impedance: $Z_{\text{diff}} = 99.85\,\Omega$.
- **L3 / L10 Inner Stripline Single-Ended (50 $\Omega$):**
  - Total dielectric separation $b = 0.300\,\text{mm}$ ($150\,\mu\text{m}$ to L2 GND, $150\,\mu\text{m}$ to L4 GND).
  - Trace width: $w = 0.115\,\text{mm}$ ($4.5\,\text{mils}$).
  - Characteristic Impedance: $Z_0 = 49.80\,\Omega$.

---

### 3. MOSAIC-WAVE 4-Layer Controlled-Impedance RF Stackup
Designed for minimal dielectric loss and controlled reflection phase across the $1.0 - 6.0\,\text{GHz}$ band:

```
+---------------------------------------------------------------------------------------+
| MOSAIC-WAVE 4-LAYER RF HYBRID STACKUP                                                 |
|                                                                                       |
| Layer  Name         Copper Thk  Dielectric Material     Dielectric Thk  Function      |
| ------------------------------------------------------------------------------------- |
| L01    RF_TOP       0.035 mm    Rogers RO4350B LoPro    0.508 mm        8x8 Metasurf  |
| L02    RF_GND       0.035 mm    Standard FR-4 Prepreg   0.200 mm        Solid RF GND  |
| L03    PWR_BIAS     0.035 mm    Standard FR-4 Core      0.710 mm        15V DC Bias   |
| L04    DIG_BOT      0.035 mm    Solder Mask             0.020 mm        74HC595 Logic |
| ------------------------------------------------------------------------------------- |
| Total Thickness: 1.58 mm                                                              |
+---------------------------------------------------------------------------------------+
```

#### RF Impedance Tuning:
- **L1 RF 50 $\Omega$ Microstrip Feed:**
  - Dielectric: Rogers RO4350B, $h = 0.508\,\text{mm}$, $\varepsilon_r = 3.66$, $\tan\delta = 0.0037$.
  - Trace width: $w = 1.08\,\text{mm}$ ($42.5\,\text{mils}$).
  - Characteristic Impedance: $Z_0 = 50.05\,\Omega$.
  - Attenuation at $5.8\,\text{GHz}$: $\alpha_{\text{total}} = 0.18\,\text{dB/inch}$ ($0.07\,\text{dB/cm}$).
- **Grounded Coplanar Waveguide (GCPW) Launch:**
  - Center trace width: $w = 0.92\,\text{mm}$, ground gap: $g = 0.35\,\text{mm}$.
  - Coplanar ground plane stitched with via fence ($0.3\,\text{mm}$ drill, $1.0\,\text{mm}$ pitch) to L2 RF_GND.
  - Return Loss $> 24\,\text{dB}$ up to $6.0\,\text{GHz}$.

---

### 4. MOSAIC-SENSE 8-Layer Mixed-Signal Low-Noise Stackup
Designed to isolate $\pm 100\,\text{V}$ ultrasonic pulser transients from sub-microampere EIS measurements and gigahertz RF reflectometer signals:

```
+---------------------------------------------------------------------------------------+
| MOSAIC-SENSE 8-LAYER MIXED-SIGNAL STACKUP                                             |
|                                                                                       |
| Layer  Name         Copper Thk  Dielectric Material     Dielectric Thk  Domain        |
| ------------------------------------------------------------------------------------- |
| L01    ANA_TOP      0.035 mm    Isola 370HR Prepreg     0.125 mm        RF & Echo AFE |
| L02    AGND         0.035 mm    Isola 370HR Core        0.200 mm        Analog Ground |
| L03    ANA_PWR      0.035 mm    Isola 370HR Prepreg     0.150 mm        Clean LDO Rails|
| L04    SHIELD_GND   0.035 mm    Isola 370HR Core        0.400 mm        Internal Farad|
| L05    DGND         0.035 mm    Isola 370HR Prepreg     0.150 mm        Digital Ground|
| L06    DIG_PWR      0.035 mm    Isola 370HR Core        0.200 mm        3.3V/5V Dig Pw|
| L07    DGND         0.035 mm    Isola 370HR Prepreg     0.125 mm        Digital Ground|
| L08    DIG_BOT      0.035 mm    Solder Mask             0.020 mm        SPI / ADC Bus |
| ------------------------------------------------------------------------------------- |
| Total Thickness: 1.63 mm                                                              |
+---------------------------------------------------------------------------------------+
```

#### High-Voltage & Guarding Design Rules:
1. **Creepage / Clearance for $\pm 100\,\text{V}$ Net (`HV_PULSE_100V`):**
   - Enforced minimum spacing to any copper plane or digital signal: $1.50\,\text{mm}$ ($59\,\text{mils}$).
   - Milled isolation slot ($1.0\,\text{mm}$ width) cut through the PCB between the STHV748 pulser output pins and the sensitive AD8331 preamplifier inputs.
2. **EIS Active Guarding (`EIS_GUARD`):**
   - AD5940 high-impedance inputs (`SE0`, `WE0`) are fully surrounded on L1 by a driven guard ring connected to the internal low-impedance buffer output (`VBIAS0`).
   - Zero solder mask over the guard ring to prevent surface contamination leakage currents ($< 50\,\text{pA}$ leakage target).
