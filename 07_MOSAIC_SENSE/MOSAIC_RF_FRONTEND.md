# MOSAIC-SENSE RF FRONT-END SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Domain:** Coherent Microwave Vector Reflectometry ($1.0 - 6.0\,\text{GHz}$)  

---

### 1. RF Signal Chain Architecture

```
                    +-------------------+
                    | Analog Devices    |
                    | ADF4351 Synth     |
                    +-------------------+
                              |
                        RF Out (0 dBm)
                              v
                    +-------------------+
                    | 20 dB Directional |-------- Forward Coupled Ref (-20 dBm) --------+
                    | Coupler           |                                               |
                    +-------------------+                                               |
                              | Main Thru (0 dBm)                                       |
                              v                                                         |
                    +-------------------+                                               |
                    | ADG904 / HMC241   |                                               |
                    | Absorptive SP4T   |                                               |
                    +-------------------+                                               |
                     |       |    |   |                                                 |
             +-------+       |    |   +-------+                                         |
             |               |    |           |                                         |
             v               v    v           v                                         |
           [DUT]          [SHORT][OPEN]    [LOAD 50R]                                   |
             |                                                                          |
             | Reflected Wave Gamma(f)                                                  |
             +--------------------+                                                     |
                                  v                                                     |
                    +---------------------------+                                       |
                    | Analog Devices LTC5586    |<--------------------------------------+
                    | Direct I/Q Demodulator    | (LO Port)
                    +---------------------------+
                       |                     |
                     I_out (DC-coupled)    Q_out (DC-coupled)
                       v                     v
                    +---------------------------+
                    | Dual 18-Bit 2 MSPS SAR ADC|
                    | (Texas Instruments ADS8881)|
                    +---------------------------+
```

---

### 2. Performance Specifications
- **Frequency Coverage:** $1.0\,\text{GHz}$ to $6.0\,\text{GHz}$ (continuous fractional-N tuning with $10\,\text{kHz}$ frequency step).
- **Output Power:** $-4\,\text{dBm}$ to $+5\,\text{dBm}$ programmable in $3\,\text{dB}$ increments.
- **Direct Conversion Demodulation:** DC-coupled $I$ and $Q$ differential baseband signals eliminate IF filtering and phase ambiguities, allowing vector reflectometry down to stationary reflection coefficients.
- **Dynamic Range:** Calculated $> 75\,\text{dB}$ across the band; verified by SPICE reflection simulation.
- **Third-Order Input Intercept (IIP3):** $+30.5\,\text{dBm}$ at $2.14\,\text{GHz}$, preventing intermodulation distortion when interrogating non-linear targets.
