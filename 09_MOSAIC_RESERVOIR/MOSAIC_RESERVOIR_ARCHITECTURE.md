# MOSAIC-RESERVOIR ARCHITECTURE SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Board ID:** MOSAIC-RESERVOIR (Non-Linear Physical Analog Computing Subsystem)  
**Revision:** 1.0  
**EDA Project:** `09_MOSAIC_RESERVOIR/MOSAIC_RESERVOIR.kicad_pro`  

---

### 1. The Physical Analog Computing Paradigm
Conventional digital signal processing samples high-speed physical waveforms with multi-GSPS digitisers, transferring gigabytes of raw data to central processors.
MOSAIC-RESERVOIR implements **Function B (Physical Reservoir Computing)** directly in the analog electromagnetic domain:
- **Input:** Transient RF reflections or amplified ultrasonic echo pulses.
- **Physical Reservoir Substrate:** A multi-node non-linear microstrip transmission line network loaded with coupled LC resonators, Skyworks SMV1231 varactors, and SMS7621 Schottky diodes.
- **Dynamics:** The network exhibits non-linear voltage-dependent propagation delay, localized wave mixing, and fading memory governed by the electromagnetic quality factor $Q$ and group delay.
- **Output:** Multi-port spatial voltage projections $\mathbf{x}_{\text{res}}(t)$ that are linearly separable.
- **Readout Layer:** The FPGA trains a lightweight linear ridge regression readout weight matrix $\mathbf{W}_{\text{out}}$ to classify structural defect classes with minimal digital compute.

---

### 2. Memristor Rejection & PCB LC Mesh Selection
As established in `INITIAL_RESEARCH_AND_FEASIBILITY_AUDIT.md` (Backtrack-002), discrete memristive crossbars were rejected due to extreme cycle-to-cycle device variability ($\sigma > 25\%$), lack of standard SMD packaging, and severe thermal instability.
The non-linear microstrip LC resonator network provides:
1. Standard, highly reproducible surface-mount components (Skyworks SMV1231 and SMS7621).
2. Deterministic voltage-dependent capacitance:
   $$C(V) = \frac{C_0}{(1 + V/V_R)^\gamma}$$
3. Symmetric non-linear current-voltage clamping via anti-parallel Schottky diode pairs:
   $$I(V) = 2 I_s \sinh\left( \frac{q V}{\eta k_B T} \right) \approx a_1 V + a_3 V^3$$
4. Temperature compensation via on-board digital DAC bias regulation (Analog Devices AD5683R).
