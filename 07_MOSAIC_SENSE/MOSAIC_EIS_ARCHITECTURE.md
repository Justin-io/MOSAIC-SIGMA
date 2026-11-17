# MOSAIC-SENSE ELECTRICAL IMPEDANCE SPECTROSCOPY (EIS) SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Subsystem:** Low-Frequency Electrochemical & Dielectric Front-End (AD5940)  

---

### 1. Functional Overview
The EIS channel operates across $0.016\,\text{Hz}$ to $200\,\text{kHz}$ using the Analog Devices AD5940BCPZ front-end. Its primary scientific mission is measuring the complex interfacial impedance $Z^*(\omega)$ of adhesively bonded composite joints and carbon-fiber plies to detect:
1. **Moisture Saturation:** Ingress of liquid water increases localized relative permittivity from $\varepsilon_r \approx 3.6$ (dry epoxy) up to $> 15$, creating a diagnostic capacitive phase shift in the $10\,\text{Hz} - 10\,\text{kHz}$ regime.
2. **Ionic Conductive Degradation:** Chemical breakdown of the cross-linked polymer matrix reduces bulk resistivity, increasing low-frequency dielectric loss $\tan\delta = \varepsilon'' / \varepsilon'$.
3. **Micro-Cracking & Contact Degradation:** Interfacial debonding introduces contact resistance spikes that are decoupled via 4-wire Kelvin measurement.

---

### 2. 4-Wire Kelvin Electrode Architecture
To eliminate parasitic contact resistance ($R_{\text{contact}} \approx 5 - 25\,\Omega$) from contaminating the true material bulk impedance ($R_{\text{bulk}} \approx 10 - 150\,\Omega$):
- **Current Drive Electrodes (`CE0` and `WE0`):** Excitation current is injected through outer electrodes via the AD5940 low-noise digital-to-analog converter and high-speed output amplifier.
- **Voltage Sense Electrodes (`RE0` and `SE0`):** Differential voltage is sensed through inner electrodes by the high-input-impedance ($Z_{\text{in}} > 10^{12}\,\Omega$) instrumentation amplifier.
- **Transimpedance Amplifier (TIA):** Programmed with calibrated internal feedback resistors ($R_{\text{TIA}} \in \{200\,\Omega, 1\,\text{k}\Omega, 10\,\text{k}\Omega, 100\,\text{k}\Omega\}$) to maximize dynamic range across varying composite samples.
- **Hardware DFT Accelerator:** Directly computes the real ($R$) and imaginary ($X$) impedance components at the excitation frequency in hardware, transferring complex values via SPI without software FFT overhead.
