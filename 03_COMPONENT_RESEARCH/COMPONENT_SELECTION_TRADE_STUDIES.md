# COMPONENT SELECTION TRADE STUDIES & DEVICE JUSTIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Classification:** Deep Engineering Trade Studies  

---

### 1. FPGA & Compute SoC Trade Study (MOSAIC-CORE)

#### Evaluated Candidates:
1. **AMD Zynq UltraScale+ MPSoC (XCZU3EG-1SFVC784E):** Quad-core ARM Cortex-A53 (1.2 GHz), Dual-core Cortex-R5F (600 MHz), 154k System Logic Cells, 7.6 Mb BRAM, 360 DSP48E2 slices. 0.8 mm BGA package ($23 \times 23\,\text{mm}$).
2. **AMD Kintex-7 (XC7K70T-1FBG676C):** High-performance pure FPGA, 65.6k Logic Cells, 240 DSP slices. Requires external host processor for Linux and Bayesian BED loop.
3. **AMD Artix-7 (XC7A100T-1FGG484C):** Low-cost FPGA, 101k Logic Cells, 240 DSP slices. Lacks integrated hard ARM cores; requires MicroBlaze soft processor (insufficient compute for real-time Gaussian Process BED).
4. **STM32H743ZI (Dual-core ARM Cortex-M7/M4):** 480 MHz MCU. Lacks high-speed programmable logic, parallel LVDS buses, and nanosecond multi-channel trigger generation.

```
+---------------------------------------------------------------------------------------------------+
| COMPUTE CORE TRADE EVALUATION MATRIX                                                              |
+---------------------------+-------------------+-------------------+---------------+---------------+
| Selection Metric (Weight) | Zynq UltraScale+  | AMD Kintex-7      | AMD Artix-7   | STM32H743ZI   |
|                           | (XCZU3EG) [WINNER]| (XC7K70T)         | (XC7A100T)    | (Microctrl)   |
+---------------------------+-------------------+-------------------+---------------+---------------+
| Embedded Linux Compute (0.25)| 5 (Quad A53)   | 1 (None)          | 2 (MicroBlaze)| 2 (No Linux)  |
| Real-Time Trigger Sync (0.20)| 5 (Dual R5F + PL)| 5 (Pure PL)       | 5 (Pure PL)   | 3 (Timer IRQ) |
| DSP / Math Engine (0.20)  | 5 (360 DSP48E2)   | 4 (240 DSP48E1)   | 3 (240 DSP)   | 2 (Hardware FP)|
| Board Area & Routing (0.15)| 4 (784-BGA 0.8mm)| 3 (676-BGA 1.0mm) | 4 (484-BGA)   | 5 (LQFP-144)  |
| Power Dissipation (0.10)  | 4 (~5.2 W typ.)   | 3 (~6.5 W)        | 4 (~3.2 W)    | 5 (~0.8 W)    |
| Component Cost & Avail (0.10)| 4 (High Stock) | 3 (Moderate)      | 4 (High Stock)| 5 (In Stock)  |
+---------------------------+-------------------+-------------------+---------------+---------------+
| Weighted Composite Score  | **4.60 / 5.00**   | 3.05 / 5.00       | 3.50 / 5.00   | 3.15 / 5.00   |
+---------------------------+-------------------+-------------------+---------------+---------------+
```

**Conclusion:** The **AMD Zynq UltraScale+ XCZU3EG** is the definitive selection. It unites the real-time Linux OS (executing the Bayesian active learning engine on Cortex-A53), deterministic microsecond trigger distribution (on Cortex-R5F), and nanosecond parallel ADC streaming (on UltraScale+ PL).

---

### 2. Metasurface Tuning Element Trade Study (MOSAIC-WAVE)

#### Evaluated Candidates:
1. **Skyworks SMV1231-079LF Hyperabrupt Varactor:** Capacitance $0.46 - 2.35\,\text{pF}$ ($C_R = 5.1\times$), series resistance $R_s = 1.5\,\Omega$, quality factor $Q > 3000$ at $50\,\text{MHz}$. SC-79 ($1.6 \times 0.8\,\text{mm}$) package. Continuous analog tuning with zero static DC current.
2. **MACOM MADP-000907-14020 PIN Diode:** Ultra-low forward resistance ($R_s = 1.2\,\Omega$ at $10\,\text{mA}$), off-capacitance $C_{\text{off}} = 0.025\,\text{pF}$. 1-bit or 2-bit binary phase tuning only; requires $10\,\text{mA}$ forward bias per diode ($64 \text{ diodes} \implies 640\,\text{mA}$ continuous DC current $\implies 3.2\,\text{W}$ thermal heat generated directly on the RF sensing aperture).
3. **Infineon BB833 Silicon Varactor:** $C = 0.75 - 9.0\,\text{pF}$. Tuning range too large for sub-6 GHz microwave split rings; high parasitic package inductance ($1.8\,\text{nH}$).
4. **RF MEMS Switches (Menlo Micro):** Ultra-high linearity, zero power, but very high unit cost ($>\$35/\text{switch}$), multi-voltage gate drive ($85\,\text{V}$), and limited commercial sourcing.

```
+---------------------------------------------------------------------------------------------------+
| RF TUNING ELEMENT TRADE STUDY                                                                     |
+---------------------------+-----------------------+-----------------------+-----------------------+
| Selection Metric (Weight) | Skyworks SMV1231      | MACOM PIN Diode       | Infineon BB833        |
|                           | (Varactor) [WINNER]   | (MADP-000907)         | (Tuning Diode)        |
+---------------------------+-----------------------+-----------------------+-----------------------+
| Phase Resolution (0.30)   | 5 (Continuous analog) | 2 (Binary 0/180 deg)  | 4 (Continuous analog) |
| Thermal Dissipation (0.25)| 5 (Zero DC current)   | 1 (3.2W continuous DC)| 5 (Zero DC current)   |
| High-Frequency Q (0.20)   | 5 (Q > 3000 at 50MHz) | 4 (Low loss)          | 3 (Q < 1000)          |
| Package Parasitics (0.15) | 5 (L_s < 0.4 nH)      | 5 (L_s < 0.3 nH)      | 2 (L_s > 1.8 nH)      |
| SMT Assembly Ease (0.10)  | 4 (SC-79 / 0402 eq)   | 4 (SOD-323)           | 4 (SOD-323)           |
+---------------------------+-----------------------+-----------------------+-----------------------+
| Weighted Composite Score  | **4.85 / 5.00**       | 2.95 / 5.00           | 3.75 / 5.00           |
+---------------------------+-----------------------+-----------------------+-----------------------+
```

**Conclusion:** The **Skyworks SMV1231-079LF** is selected. It delivers continuous analog phase control across $> 270^\circ$ at microwave frequencies while eliminating heating on the sensitive composite interrogation surface.

---

### 3. RF Direct Reflectometry Receiver Trade Study (MOSAIC-SENSE)

#### Evaluated Candidates:
1. **Analog Devices LTC5586 (Direct Conversion I/Q Demodulator):** $300\,\text{MHz}$ to $6.0\,\text{GHz}$, input IP3 $+30.5\,\text{dBm}$, noise figure $10.5\,\text{dB}$, DC-coupled baseband differential outputs ($I/Q$).
2. **Analog Devices AD8302 (Logarithmic Magnitude & Phase Detector):** DC to $2.7\,\text{GHz}$. Output is scalar magnitude ratio ($\text{dB}$) and relative phase ($0^\circ - 180^\circ$). Bandwidth limited to $2.7\,\text{GHz}$ (cannot cover $5.8\,\text{GHz}$ ISM band); phase ambiguity ($180^\circ$ wrap without sign).
3. **Analog Devices AD9361 (Agile RF SDR Transceiver):** Dual $70\,\text{MHz} - 6.0\,\text{GHz}$ transceiver with integrated 12-bit ADC/DAC. Extreme register programming complexity; AC-coupled internal analog baseband filters degrade low-speed reflectometry; high power dissipation ($> 2.5\,\text{W}$).

```
+---------------------------------------------------------------------------------------------------+
| RF DEMODULATOR TRADE STUDY                                                                        |
+---------------------------+-----------------------+-----------------------+-----------------------+
| Selection Metric (Weight) | Analog Devices LTC5586| Analog Devices AD8302 | Analog Devices AD9361 |
|                           | (Direct I/Q) [WINNER] | (Mag/Phase Log Amp)   | (Full SDR Transceiver)|
+---------------------------+-----------------------+-----------------------+-----------------------+
| Frequency Range (0.25)    | 5 (300MHz to 6.0GHz)  | 2 (DC to 2.7GHz only) | 5 (70MHz to 6.0GHz)   |
| Complex Vector Sign (0.25)| 5 (Full 360 deg I/Q)  | 2 (0-180 deg sign amb)| 5 (Full 360 deg I/Q)  |
| Dynamic Range & IIP3 (0.2)| 5 (IIP3 +30.5 dBm)    | 4 (Dynamic range 60dB)| 3 (IIP3 -10 dBm)      |
| Firmware Simplicity (0.15)| 5 (Direct SPI + DC-IQ)| 5 (Direct analog out) | 1 (Massive Linux API) |
| DC-Coupled Reflect (0.15) | 5 (True DC baseband)  | 4 (DC outputs)        | 2 (AC-coupled HPF)    |
+---------------------------+-----------------------+-----------------------+-----------------------+
| Weighted Composite Score  | **5.00 / 5.00**       | 3.15 / 5.00           | 3.40 / 5.00           |
+---------------------------+-----------------------+-----------------------+-----------------------+
```

**Conclusion:** The **Analog Devices LTC5586** is selected. Combined with an ADF4351 synthesizer, it provides vector reflectometry across the entire $1.0 - 6.0\,\text{GHz}$ band with unambiguous $360^\circ$ phase reconstruction and high linearity.

---

### 4. High-Voltage Ultrasonic Pulser Trade Study (MOSAIC-SENSE)

#### Evaluated Candidates:
1. **STMicroelectronics STHV748L:** 4-channel monolithic high-voltage pulser producing programmable pulses up to $\pm 100\,\text{V}$ with 2 A peak output current, integrated active return-to-zero (RTZ) clamping, and integrated high-voltage T/R switch. QFN-64 ($10 \times 10\,\text{mm}$).
2. **Microchip MD1711 + TC6320 (Controller + Discrete HV Bridge):** Requires separate controller IC and external discrete high-voltage P-channel/N-channel MOSFETs. Increases PCB component count by $> 16$ parts and expands board footprint by $3\times$.
3. **Discrete Avalanche Transistor Pulser:** Ultra-fast sub-nanosecond risetime, but fixed pulse amplitude, high trigger jitter, and severe component aging.

**Conclusion:** The **STMicroelectronics STHV748L** is selected. It replaces 20+ discrete components with a single monolithic IC, integrating active clamping to damp transducer ringing and direct LVDS/CMOS trigger interfaces.
