# MOSAIC-Σ SYSTEM SPECIFICATION (MASTER ARCHITECTURE SPEC)

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Document ID:** MOSAIC-SYS-SPEC-001  
**Revision:** 1.0  
**Classification:** Definitive Engineering Architecture Specification  
**EDA Platform:** KiCad 9.0.2  

---

### 1. System Overview & Physical Partition
MOSAIC-Σ is partitioned into a modular family of high-performance printed circuit boards interconnected via precision high-speed, controlled-impedance mezzanine connectors (Samtec QSH/QTH series or SEARAY 0.8 mm):

```
+---------------------------------------------------------------------------------------------------+
| MOSAIC-Σ HARDWARE FAMILY ARCHITECTURE                                                             |
+-------------------+-----------------------------------+-----------------------+-------------------+
| Board Name        | Primary Functional Responsibility | PCB Technology        | Layer Count       |
+-------------------+-----------------------------------+-----------------------+-------------------+
| **MOSAIC-CORE**   | Master SoC/FPGA, Real-Time Linux, | High-Density FR-4     | 12 Copper Layers  |
|                   | Bayesian Engine, DDR4, Power Dist | (0.8mm BGA, Microvias)| (HDI 1-b-10-b-1)  |
+-------------------+-----------------------------------+-----------------------+-------------------+
| **MOSAIC-WAVE**   | 8x8 Varactor Metasurface Array,   | Controlled-Z Hybrid   | 4 Copper Layers   |
|                   | Shift-Register Bias Control, RF   | (Rogers RO4350B / FR4)| (LoPro RF Top)    |
+-------------------+-----------------------------------+-----------------------+-------------------+
| **MOSAIC-SENSE**  | AD5940 EIS + Coherent RF I/Q +    | Mixed-Signal Low-Noise| 8 Copper Layers   |
|                   | STHV748 Ultrasound + On-PCB SOL   | (Split Ground Domains)| (Dedicated Shield)|
+-------------------+-----------------------------------+-----------------------+-------------------+
| **MOSAIC-RADAR**  | TI AWR6843AOP 60 GHz mmWave Radar | FR-4 / ENIG           | 4 Copper Layers   |
| (Optional Mezz.)  | Non-contact surface metrology     | (AoP Antenna keepout) | (Standard)        |
+-------------------+-----------------------------------+-----------------------+-------------------+
| **MOSAIC-RESERVOIR**| Non-linear LC microstrip delay  | Low-Loss High-Q       | 4 Copper Layers   |
| (Optional Mezz.)  | line physical reservoir network   | (Isola FR408HR)       | (RF Microstrip)   |
+-------------------+-----------------------------------+-----------------------+-------------------+
```

---

### 2. Subsystem Specifications

#### 2.1 BOARD A: MOSAIC-CORE (Computing & Experiment Control)
- **Primary Processor:** AMD Zynq UltraScale+ MPSoC (XCZU3EG-1SFVC784E)
  - Processing System (PS): Quad-core ARM Cortex-A53 up to 1.2 GHz, Dual-core ARM Cortex-R5F real-time processor.
  - Programmable Logic (PL): 154k Logic Cells, 7.6 Mb Block RAM, 360 DSP48E2 slices.
- **System Memory:** 1 GB (8 Gb) 16-bit DDR4-2400 SDRAM (Micron MT40A512M16LY-075:E) on dedicated PL/PS memory controller.
- **Non-Volatile Storage:** 16 GB eMMC 5.1 + 64 MB Quad-SPI NOR Flash for bootloader and golden bitstream fallback.
- **Deterministic Timebase:** SiTime SiT5356 $\pm 0.5\,\text{ppm}$ VCTCXO reference delivering low-jitter differential clocks to PL clock management tiles (CMTs).
- **Communication & Telemetry:** Gigabit Ethernet (Marvell Alaska 88E1512 PHY), USB 2.0 OTG, isolated CAN-FD bus, and high-speed UART debug.
- **Mezzanine Interfaces:**
  - Mezzanine A (to MOSAIC-SENSE): 120-pin Samtec QSH/QTH connector carrying high-speed parallel/LVDS ADC data (65 MSPS), SPI buses, I2C telemetry, and precision differential hardware triggers.
  - Mezzanine B (to MOSAIC-WAVE): 80-pin connector carrying high-speed SPI/shift-register data, varactor high-voltage bias rail ($15\,\text{V}$), and auxiliary analog lines.

#### 2.2 BOARD B: MOSAIC-WAVE (Programmable Metasurface Aperture)
- **Aperture Topology:** $8 \times 8$ planar array (64 unit cells total), grid pitch $d = 25.0\,\text{mm}$ (total active aperture $200 \times 200\,\text{mm}$).
- **Operating Frequency:** 1.0 GHz to 6.0 GHz (optimized for 2.4 GHz – 5.8 GHz ISM bands).
- **Unit Cell Architecture:** Modified rectangular split-ring resonator (SRR) with dual Skyworks SMV1231-079LF hyperabrupt junction varactor diodes placed across the capacitive gap.
- **Tuning Range:** Capacitance variation from $2.35\,\text{pF}$ ($V_{\text{bias}} = 0\,\text{V}$) down to $0.46\,\text{pF}$ ($V_{\text{bias}} = 15\,\text{V}$), producing $> 270^\circ$ of continuous reflection phase shift.
- **Bias Network:** Eight cascaded 8-bit serial-in parallel-out shift registers (Nexperia 74HC595PW) providing 64 independent static DC bias channels. Each channel is filtered through a 2-stage SMD $RC$ low-pass network ($R = 100\,\text{k}\Omega, C = 10\,\text{nF}$) delivering $f_c \approx 160\,\text{Hz}$ to eliminate digital noise coupling into the RF resonators.
- **RF Feeds:** Dual edge-mounted SMA connectors coupled via microstrip Wilkinson power dividers or hybrid couplers for dual-orthogonal polarization testing.

#### 2.3 BOARD C: MOSAIC-SENSE (Multi-Physics Acquisition & Calibration)
- **Channel 1 — Wideband RF Reflectometer ($1.0 - 6.0\,\text{GHz}$):**
  - Synthesizer: Analog Devices ADF4351 fractional-N PLL ($35 - 4400\,\text{MHz}$) and extended doubling up to $6\,\text{GHz}$.
  - Coupler: Mini-Circuits / TDK wideband 20 dB directional coupler with $> 20\,\text{dB}$ directivity.
  - Demodulator: Analog Devices LTC5586 high-linearity direct conversion I/Q demodulator providing DC-coupled in-phase ($I$) and quadrature ($Q$) baseband voltages.
  - Digitization: Dual 18-bit 2 MSPS SAR ADC (Texas Instruments ADS8881).
- **Channel 2 — Electrochemical Impedance Spectroscopy (EIS):**
  - Front-End: Analog Devices AD5940BCPZ ($0.016\,\text{Hz} - 200\,\text{kHz}$).
  - Interface: 4-wire Kelvin electrode interface with integrated switch matrix, high-speed transimpedance amplifier (TIA), and hardware DFT accelerator.
- **Channel 3 — High-Voltage Ultrasonic Pulse-Echo ($1.0 - 5.0\,\text{MHz}$):**
  - Pulser: STMicroelectronics STHV748 4-channel monolithic high-voltage pulser producing programmable unipolar/bipolar pulses up to $\pm 100\,\text{V}$ with 2 A peak drive.
  - Protection: Microchip MD0100 bidirectional high-voltage T/R protection switch.
  - Receiver LNA/VGA: Analog Devices AD8331 ultra-low noise variable gain amplifier ($0.74\,\text{nV}/\sqrt{\text{Hz}}$), 48 dB gain range, analog Time-Gain Compensation (TGC).
  - Digitizer: 12-bit 65 MSPS ADC (Analog Devices AD9235) streaming directly to FPGA block RAM.
- **Channel 4 — In-Situ Self-Calibration Standards:**
  - Microwave SP4T Switch: Analog Devices ADG904 / HMC241 routing between the DUT and on-PCB Short, Open, $50\,\Omega$ Precision Load, and Through line.
  - EIS Reference: Vishay $0.05\%$ $10\,\text{ppm/}^\circ\text{C}$ metal foil resistors ($100\,\Omega, 1\,\text{k}\Omega, 100\,\text{k}\Omega$) and $0.1\%$ C0G capacitors.

---

### 3. Power Architecture & Voltage Rail Budget
The system is powered from an external $+12\,\text{V} \pm 10\%$ DC input. The power distribution tree isolates high-voltage digital switching noise from sensitive analog circuits:

```
+---------------------------------------------------------------------------------------+
| MOSAIC-Σ POWER DISTRIBUTION & REGULATION TREE                                         |
|                                                                                       |
|   +12V Main DC Input                                                                  |
|        |                                                                              |
|        +--> [ Buck 1: 5.0V @ 4A ] --------> Serves daughterboards & Mezzanine         |
|        |                                                                              |
|        +--> [ Buck 2: 3.3V @ 6A ] --------> Digital I/O, eMMC, Ethernet PHY, Clocks  |
|        |                                                                              |
|        +--> [ Buck 3: 1.2V @ 8A ] --------> DDR4 VDD, FPGA VCCINT_IO                 |
|        |                                                                              |
|        +--> [ Buck 4: 0.85V @ 15A ] ------> FPGA Core VCCINT (Low ripple <10mV)      |
|        |                                                                              |
|        +--> [ Boost 1: +15V @ 200mA ] ----> MOSAIC-WAVE Varactor Bias Rail            |
|        |                                                                              |
|        +--> [ Isolated Flyback / Boost ] -> +/-100V Pulser Rail (MOSAIC-SENSE)        |
|        |                                                                              |
|        +--> [ Low-Noise LDO Array ]                                                   |
|                 +--> Ultra-Clean +3.3V_ANA (AD5940, AD8331, ADF4351)                  |
|                 +--> Ultra-Clean +5.0V_ANA (LTC5586 Demodulator)                      |
|                 +--> Precision +2.500V Ref (ADR4525 Voltage Standard)                 |
+---------------------------------------------------------------------------------------+
```

---

### 4. Environmental & Operating Limits
- **Operating Temperature Range:** $-10^\circ\text{C}$ to $+60^\circ\text{C}$ (guaranteed calibration tracking).
- **Storage Temperature Range:** $-40^\circ\text{C}$ to $+85^\circ\text{C}$.
- **Maximum RF Input Power:** $+15\,\text{dBm}$ (protected by limiters).
- **Maximum High-Voltage Pulser Duty Cycle:** $0.5\%$ (thermal protection for STHV748).
- **DC Isolation Barrier (SENSE vs. CORE):** $500\,\text{V}$ galvanic isolation on trigger lines via high-speed digital isolators (TI ISO7741).
