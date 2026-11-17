# MOSAIC-WAVE RF ROUTING CONSTRAINTS & DESIGN RULES

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Classification:** RF Engineering Rules & DRC Enforcement  

---

### 1. RF Transmission Line Geometry
- **Primary Net Class:** `RF_50OHM`
- **Trace Type:** Grounded Coplanar Waveguide (GCPW) on Layer 1 over Layer 2 RF_GND.
- **Trace Dimensions on Rogers RO4350B ($h = 0.508\,\text{mm}, \varepsilon_r = 3.66$):**
  - Center Conductor Width: $w = 0.95\,\text{mm}$ ($37.4\,\text{mils}$).
  - Ground Coplanar Spacing: $g = 0.35\,\text{mm}$ ($13.8\,\text{mils}$).
  - Copper Thickness: $1\,\text{oz}$ ($35\,\mu\text{m}$).
  - Characteristic Impedance: $Z_0 = 50.1\,\Omega \pm 1.5\,\Omega$.

---

### 2. Ground Via Stitching Fence
- **Stitching Drill Diameter:** $0.30\,\text{mm}$ ($11.8\,\text{mils}$).
- **Via Pad Diameter:** $0.60\,\text{mm}$ ($23.6\,\text{mils}$).
- **Via-to-Via Pitch:** $p = 1.0\,\text{mm}$ along the coplanar ground edge.
- **Wavelength Criterion:**
  $$p \le \frac{\lambda_{\min}}{10} = \frac{c}{10 \cdot f_{\max} \sqrt{\varepsilon_{\text{eff}}}} = \frac{3 \times 10^8}{10 \cdot 6.0 \times 10^9 \cdot \sqrt{2.78}} \approx 3.0\,\text{mm}$$
  The implemented $1.0\,\text{mm}$ pitch provides $3\times$ oversampling, preventing parallel-plate waveguide mode resonance and ensuring $> 45\,\text{dB}$ shielding up to $6.0\,\text{GHz}$.

---

### 3. DC Bias Network Isolation
- **Rule RF-01:** No digital or DC bias trace may cross beneath an RF unit cell on Layer 1 or Layer 2. All bias lines are strictly confined to Layer 3 and Layer 4.
- **Rule RF-02:** Every DC bias feed via passing from Layer 3 to Layer 1 must be enclosed by a ground keepout void on Layer 2 and filtered by an adjacent 0402 SMD capacitor connected to RF_GND within $0.8\,\text{mm}$ of the via barrel.
