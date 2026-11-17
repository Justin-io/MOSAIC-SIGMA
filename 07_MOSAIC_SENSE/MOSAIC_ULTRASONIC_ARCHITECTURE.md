# MOSAIC-SENSE ULTRASONIC PULSE-ECHO ARCHITECTURE

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Subsystem:** High-Voltage Acoustic Inspection Chain ($1.0 - 5.0\,\text{MHz}$)  

---

### 1. Transmit/Receive Signal Chain Architecture

```
                 +-----------------------+
                 | MOSAIC-CORE FPGA      |
                 | Differential Trigger  |
                 +-----------------------+
                             |
                     TRIG_P / TRIG_N (LVDS)
                             v
                 +-----------------------+
                 | TI ISO7741            |
                 | Galvanic Isolator     |
                 +-----------------------+
                             |
                             v
                 +-----------------------+
                 | STMicro STHV748       |<--- +/-100V DC Rails
                 | Monolithic Pulser     |
                 +-----------------------+
                             |
                   +/-100V Fast Pulse (50 ns)
                             |
                             +-------------------------> [ Piezo Transducer ]
                             |                                  |
                             v                                  | Return Echo
                 +-----------------------+                      | (15 mV peak)
                 | Microchip MD0100      |<---------------------+
                 | Bidirectional T/R     |
                 | Protection Switch     |
                 +-----------------------+
                             |
                  Clamped Voltage (< 380 mV)
                             v
                 +-----------------------+
                 | Analog Dev AD8331     |<--- VGA Gain Ramp (TGC)
                 | Ultra-Low Noise LNA   |
                 +-----------------------+
                             |
                  Amplified Output (+30 dB)
                             v
                 +-----------------------+
                 | Analog Dev AD9235     |
                 | 12-Bit 65 MSPS ADC    |
                 +-----------------------+
                             |
                   12-Bit Parallel Echo Stream
                             v
                 [ Mezzanine Bus to CORE FPGA ]
```

---

### 2. Time-Gain Compensation (TGC) Physics
Acoustic attenuation in carbon-fiber composites follows an exponential decay law:
$$A(z) = A_0 e^{-\alpha(f) \cdot z}$$
where $\alpha(f) \approx 2.5 - 6.0\,\text{dB/cm}$ for $2.5\,\text{MHz}$ ultrasound in CFRP.
- An echo from a $1.0\,\text{mm}$ deep delamination experiences $0.5\,\text{dB}$ attenuation.
- An echo from a $10.0\,\text{mm}$ back-wall defect experiences $> 12.0\,\text{dB}$ attenuation.
- The AD8331 variable-gain amplifier provides an analog linear-in-dB gain ramp controlled by an external DAC voltage:
  $$\text{Gain}(t) = G_0 + \beta \cdot t \quad (0\,\text{dB to } 48\,\text{dB})$$
  This equalizes return echo amplitudes across depth, ensuring that deep internal defects are digitized with full 12-bit dynamic range without clipping shallow echoes.
