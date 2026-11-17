# MOSAIC-RADAR FEASIBILITY & SYSTEM TRADE STUDY

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Board ID:** MOSAIC-RADAR (Optional mmWave Standoff Daughterboard)  
**Revision:** 1.0  
**Target Device:** Texas Instruments AWR6843AOP ($60 - 64\,\text{GHz}$)  

---

### 1. Physical Penetration Assessment: CFRP vs. GFRP
- **Carbon-Fiber Reinforced Polymers (CFRP):**
  - High electrical conductivity ($\sigma \sim 10^4\,\text{S/m}$).
  - Skin depth at $60\,\text{GHz}$:
    $$\delta = \sqrt{\frac{1}{\pi \cdot 60 \times 10^9 \cdot 4\pi \times 10^{-7} \cdot 10^4}} \approx 20.5\,\mu\text{m}$$
  - **Scientific Reality:** High-frequency $60\,\text{GHz}$ millimeter waves cannot penetrate beyond the first $20\,\mu\text{m}$ of a carbon-fiber laminate. All radiation is reflected from the surface. **Any claim of deep internal defect imaging in CFRP using mmWave radar is physically false.**
- **Glass-Fiber Reinforced Polymers (GFRP) & Radomes:**
  - Non-conductive dielectric ($\sigma < 10^{-10}\,\text{S/m}, \varepsilon_r \approx 3.8, \tan\delta \approx 0.01$).
  - Attenuation is low, permitting volumetric penetration through $> 20\,\text{mm}$ of glass composite. In GFRP, the AWR6843 can detect internal delaminations, resin voids, and water treeing.

---

### 2. Selected Role for MOSAIC-Σ
Rather than attempting internal inspection of carbon composites, MOSAIC-RADAR is assigned two vital complementary tasks:
1. **Non-Contact Surface Topography & Standoff Correction:** Measures the exact physical distance ($10\,\text{mm} - 500\,\text{mm}$) and tilt angle of the composite panel relative to the instrument, providing geometric calibration for ultrasonic and RF incidence angles.
2. **Sub-Micrometer Vibration & Micro-Doppler Tracking:** The $60\,\text{GHz}$ FMCW chirp provides sub-micrometer phase sensitivity to mechanical surface oscillations and structural acoustic resonances induced by external excitation.

---

### 3. Board Placement & Packaging Strategy
- **Antenna-on-Package (AoP):** The AWR6843AOP integrates the $3 \times 4$ MIMO antenna array directly onto the package substrate, eliminating the need for expensive high-frequency Rogers laminates on the PCB.
- **Daughterboard Architecture:** Implemented as a compact $50 \times 50\,\text{mm}$ daughterboard that plugs into MOSAIC-CORE only when standoff profiling or GFRP testing is required, preventing thermal dissipation ($2.1\,\text{W}$) from heating the sensitive low-noise analog circuits of MOSAIC-SENSE.
