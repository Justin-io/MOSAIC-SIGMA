# MOSAIC-CORE ARCHITECTURE SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Board ID:** MOSAIC-CORE (Computing & Master Control Motherboard)  
**Revision:** 1.0  
**Classification:** Definitive Hardware Architecture Document  
**EDA Project:** `05_MOSAIC_CORE/MOSAIC_CORE.kicad_pro`  

---

### 1. Functional Responsibilities
MOSAIC-CORE is the primary deterministic computing and master control motherboard for Project MOSAIC-Σ. It is engineered to host the autonomous matter intelligence engine:
1. **Application Processing & Active Learning:** Executes embedded real-time Linux on quad-core ARM Cortex-A53 cores (1.2 GHz), hosting the Gaussian Process surrogate models and Sequential Bayesian Experimental Design (BED) algorithm.
2. **Deterministic Real-Time Sync:** Dual-core ARM Cortex-R5F lockstep processors (600 MHz) and UltraScale+ Programmable Logic (PL) provide sub-nanosecond hardware trigger synchronization across the ultrasonic pulser, RF synthesizer, and ADC digitisers.
3. **Data Streaming & Memory Buffer:** 1 GB (8 Gb) 16-bit DDR4-2400 SDRAM interfaces with PL direct-memory access (DMA) engines, providing $> 38.4\,\text{Gbps}$ burst throughput for raw ultrasound echo capture and microwave I/Q reflections.
4. **Mezzanine Expansion Bus:** High-density, controlled-impedance connectors route trigger, clock, SPI, and parallel ADC buses to MOSAIC-SENSE (Mezzanine A) and static bias controls to MOSAIC-WAVE (Mezzanine B).

---

### 2. Device Selection & Clocking Architecture
- **MPSoC:** AMD Zynq UltraScale+ XCZU3EG-1SFVC784E
  - Package: SFVC784 (0.8 mm ball pitch, $23.0 \times 23.0\,\text{mm}$).
  - Logic Resources: 154,350 System Logic Cells, 141,120 CLB flip-flops, 70,560 CLB LUTs, 7.6 Mb Block RAM, 360 DSP48E2 slices.
- **Reference Clocking:**
  - SiTime SiT5356 Elite Platform $\pm 0.5\,\text{ppm}$ VCTCXO ($25.0\,\text{MHz}$) delivers low-jitter differential clock references to the UltraScale+ clock management tiles (CMTs).
  - Integrated PLLs synthesize $1200\,\text{MHz}$ for DDR4, $65\,\text{MHz}$ for ultrasonic ADC capture, and $100\,\text{MHz}$ for AXI interconnects.

---

### 3. High-Speed Mezzanine Interface Mapping

#### Mezzanine A (Samtec QSH-060-01-L-D-A, 120 pins to MOSAIC-SENSE):
- Pins 1, 3: `TRIG_SYNC_P/N` (100 $\Omega$ LVDS hardware trigger, skew $< 2\,\text{ps}$).
- Pins 5, 7: `MGT_REFCLK_P/N` (100 $\Omega$ differential reference clock).
- Pins 10–34: `ADC_DATA[11:0]` (65 MSPS 12-bit parallel ultrasonic echo bus).
- Pin 36: `ADC_CLK_65M` (Global CCIO clock input).
- Pins 40–55: `SPI_SENSE_BUS` (Isolated SPI links for AD5940, ADF4351, ADS8881, and ADG904).
- Pins 60–75: `I2C_THERMAL_BUS` (TMP117 local temperature telemetry).
- Pins 80–120: Power rails (+5V, +3.3V, Analog clean rail, and interleaved ground blades).

#### Mezzanine B (Samtec QSH-040-01-L-D-A, 80 pins to MOSAIC-WAVE):
- Pins 1–16: `WAVE_SPI_CTRL` (High-speed cascaded SPI for 74HC595 shift register array).
- Pins 20–30: `BIAS_PWR_15V` (+15V DC varactor bias rail, isolated via ground pins).
- Pins 35–45: `WAVE_TEMP_SENSE` (Aperture surface temperature sensors).
- Pins 50–80: Solid RF and digital return grounds with integral shielding blade.
