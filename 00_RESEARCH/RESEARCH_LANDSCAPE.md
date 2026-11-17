# RESEARCH LANDSCAPE: AUTONOMOUS MULTI-PHYSICS NDE & MATTER INTELLIGENCE

**Programme:** MOSAIC-Σ  
**Revision:** 1.0  
**Status:** APPROVED FOR ARCHITECTURE COMMIT  
**Author:** Principal Research Scientist — Experimental Physics & Systems Architecture  

---

### 1. The Physical State of Matter and Inspection Limits
Non-destructive evaluation (NDE) of heterogeneous materials—specifically Carbon Fiber Reinforced Polymers (CFRP), Glass Fiber Reinforced Polymers (GFRP), and adhesively bonded composite lap joints—is inherently constrained by the governing wave equations and constitutive electromagnetic and acoustic relations:

$$\nabla \times \mathbf{E} = - \frac{\partial \mathbf{B}}{\partial t}, \quad \nabla \times \mathbf{H} = \mathbf{J} + \frac{\partial \mathbf{D}}{\partial t}$$
$$\rho \frac{\partial^2 \mathbf{u}}{\partial t^2} = (\lambda + \mu)\nabla(\nabla \cdot \mathbf{u}) + \mu \nabla^2 \mathbf{u}$$

#### Dielectric and Conductive Anisotropy (CFRP vs. GFRP):
- **CFRP:** Exhibits highly anisotropic electrical conductivity ($\sigma_\parallel \approx 10^3 - 10^4\,\text{S/m}$ along carbon fiber axes, $\sigma_\perp \approx 1 - 10\,\text{S/m}$ across transverse ply boundaries). At microwave frequencies ($1 - 6\,\text{GHz}$), the electromagnetic skin depth:
  $$\delta = \sqrt{\frac{1}{\pi f \mu \sigma}} \approx 65 - 160\,\mu\text{m}$$
  Consequently, high-frequency electromagnetic waves reflect predominantly from the outer plies. RF reflectometry is ultra-sensitive to near-surface resin starvation, matrix cracking, fiber orientation, and surface moisture, but **cannot** interrogate deep ($> 1\,\text{mm}$) core defects.
- **GFRP:** Non-conductive glass fibers embedded in epoxy resin ($\sigma \approx 10^{-12}\,\text{S/m}$, $\varepsilon_r \approx 3.8 - 4.5$, $\tan\delta \approx 0.01 - 0.02$). Electromagnetic waves penetrate deeply without skin-effect reflection, allowing volumetric dielectric inspection, subsurface delamination tracking, and water treeing detection across microwave frequencies.

#### Acoustic Propagation and Elastodynamics:
- Acoustic waves propagate as longitudinal ($c_L \approx 2800 - 3200\,\text{m/s}$) and shear ($c_S \approx 1400 - 1800\,\text{m/s}$) modes through both CFRP and GFRP.
- Acoustic impedance mismatch:
  $$Z_0 = \rho c \approx 3.0 - 4.5 \times 10^6\,\text{kg}/(\text{m}^2\cdot\text{s})$$
  Air voids (delaminations, disbonds) have $Z_{\text{air}} \approx 400\,\text{kg}/(\text{m}^2\cdot\text{s})$. The reflection coefficient:
  $$\Gamma = \frac{Z_{\text{air}} - Z_0}{Z_{\text{air}} + Z_0} \approx -0.9997$$
  Hence, ultrasonic pulse-echo at $1 - 5\,\text{MHz}$ delivers near $100\%$ reflection at internal air gaps, making it the definitive physical modality for volumetric depth resolving.

#### Electrochemical and Low-Frequency Dielectric Relaxation:
- In the frequency range from $0.1\,\text{Hz}$ to $200\,\text{kHz}$, dipolar relaxation and Maxwell-Wagner-Sillars (MWS) interfacial polarization dominate.
- Moisture ingress into epoxy matrices alters the low-frequency complex permittivity $\varepsilon^*(\omega) = \varepsilon'(\omega) - j\varepsilon''(\omega)$, increasing ionic conductivity and the loss tangent $\tan\delta = \varepsilon'' / \varepsilon'$.
- Electrical Impedance Spectroscopy (EIS) provides direct chemical and molecular insight into adhesive cross-linking breakdown and moisture saturation.

---

### 2. The Orthogonal Multi-Physics Matrix
No single modality can solve the composite inspection problem:

| Physical Defect Type | RF Reflectometry (1–6 GHz) | Ultrasonic Echo (1–5 MHz) | EIS (0.1 Hz – 200 kHz) | mmWave Radar (60 GHz) |
|---|---|---|---|---|
| **Deep Delamination (>2 mm in CFRP)** | Blind (Skin-effect reflection) | **Primary (100% echo reflection)** | Indirect (Resistive anisotropy) | Blind (Zero penetration) |
| **Surface Resin Cracking / Scratches** | **Primary (Phase notch shift)** | Weak (Near-surface blind zone) | Weak (Contact electrode dependent)| Secondary (Standoff profiling) |
| **Volumetric Void in GFRP** | **Primary (Dielectric cavity shift)**| **Primary (Acoustic backscatter)** | Moderate | Secondary (Standoff imaging) |
| **Adhesive Moisture Degradation** | Moderate (Surface permittivity)| Weak (Acoustic velocity shift <1%)| **Primary (Ionic conductivity spike)** | Blind |
| **Fiber Misalignment / Wrinkling** | **Primary (Polarization rotation)**| Secondary (Velocity anisotropy) | Moderate (Directional resistance)| Blind |
| **External Standoff / Warping** | Blind | Blind | Blind | **Primary (Sub-mm range & Doppler)**|

---

### 3. State-of-the-Art Research Convergence (2024–2026)
1. **Electromagnetic Wave Computing:** Tzarouchis et al. (Nature Comms 2025) and Keshavarz et al. (Nature Comms 2025) proved that microwave meshes can perform spatial filtering and linear matrix projections at light speed with micro-watt power.
2. **Physical Reservoir Computing:** Liang et al. (Nature Electronics 2024) demonstrated that non-linear physical dynamics can compress complex temporal echoes into linearly separable feature spaces, reducing downstream ADC and processor load.
3. **Bayesian Active Experimentation:** Emerging NDT literature (2024–2026) demonstrates that sequential Bayesian experimental design reduces the number of inspection points by $60 - 80\%$ compared to rigid raster scanning, focusing energy on ambiguous defect boundaries.

MOSAIC-Σ is the first unified electronic instrument engineered to synthesize these distinct breakthroughs into a closed-loop digital hardware platform.
