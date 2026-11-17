# MULTIPHYSICS FORWARD MODEL & SENSOR FUSION SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Document ID:** MOSAIC-VER-MP-001  
**Revision:** 1.0  
**Domain:** Cross-Modal Multi-Physics Forward Models (CFRP & GFRP NDE)  

---

### 1. Constitutive Physical Models

#### 1.1 Modality 1: High-Voltage Ultrasonic Pulse-Echo ($1 - 5\,\text{MHz}$)
- **Wave Type:** 1D Longitudinal Acoustic Wave along laminate thickness axis $z$.
- **Governing Wave Equation:**
  $$\rho \frac{\partial^2 u}{\partial t^2} = C_{33} \frac{\partial^2 u}{\partial z^2} - \eta \frac{\partial^3 u}{\partial z^2 \partial t}$$
  where $\rho$ is composite density ($1550\,\text{kg/m}^3$), $C_{33}$ is through-thickness stiffness ($14.2\,\text{GPa}$), and $\eta$ is viscoelastic attenuation parameter ($2.8\,\text{dB/cm}$ at $2.5\,\text{MHz}$).
- **Boundary Acoustic Impedance:**
  $$Z_{\text{CFRP}} = \sqrt{\rho C_{33}} \approx 4.69 \times 10^6\,\text{kg}/(\text{m}^2\cdot\text{s})$$
  $$Z_{\text{Air Void}} = \rho_{\text{air}} c_{\text{air}} \approx 415\,\text{kg}/(\text{m}^2\cdot\text{s})$$
- **Reflection Coefficient at Delamination:**
  $$\Gamma_{\text{void}} = \frac{Z_{\text{air}} - Z_{\text{CFRP}}}{Z_{\text{air}} + Z_{\text{CFRP}}} \approx -0.9998$$
- **Time-of-Flight (ToF) Depth Inversion:**
  $$d_{\text{defect}} = \frac{c_L \cdot \Delta t_{\text{echo}}}{2} = \frac{3025\,\text{m/s} \cdot \Delta t_{\text{echo}}}{2}$$

#### 1.2 Modality 2: Microwave Reflectometry ($1.0 - 6.0\,\text{GHz}$)
- **Electromagnetic Propagation:** Helmholtz equation in anisotropic lossy medium:
  $$\nabla^2 \mathbf{E} + \omega^2 \mu_0 \tilde{\boldsymbol{\varepsilon}} \mathbf{E} = 0$$
  $$\tilde{\boldsymbol{\varepsilon}} = \varepsilon_0 \left( \boldsymbol{\varepsilon}_r' - j \frac{\boldsymbol{\sigma}}{\omega \varepsilon_0} \right)$$
- **Skin Depth in CFRP:**
  $$\delta(\omega) = \sqrt{\frac{2}{\omega \mu_0 \sigma_\parallel}} \approx 72\,\mu\text{m at } 5.0\,\text{GHz} \quad (\sigma_\parallel \approx 10^4\,\text{S/m})$$
  The microwave reflection coefficient $\Gamma_{\text{RF}}(f)$ responds to the top-ply fiber orientation angle $\theta_f$, outer resin coat thickness $t_{\text{resin}}$, and localized surface micro-cracking:
  $$\Gamma_{\text{RF}}(f) \approx \frac{\eta_{\text{CFRP}}(\theta_f) - \eta_0}{\eta_{\text{CFRP}}(\theta_f) + \eta_0}$$

#### 1.3 Modality 3: Electrical Impedance Spectroscopy (AD5940, $0.1\,\text{Hz} - 200\,\text{kHz}$)
- **Electrochemical Equivalent Circuit (Randles / Cole-Cole Model):**
  $$Z^*(\omega) = R_{\text{bulk}} + \frac{R_{\text{ct}}}{1 + (j \omega C_{\text{dl}} \tau)^\alpha} + \frac{1}{j \omega C_{\text{bulk}}}$$
  - $R_{\text{bulk}}$: Carbon-fiber matrix bulk through-thickness resistance ($10 - 250\,\Omega$).
  - $R_{\text{ct}}$: Interfacial adhesive charge transfer / ionic leakage resistance.
  - $C_{\text{bulk}}$: Capacitance of the adhesive bondline. In the presence of moisture ingress ($\phi_w$), the dielectric constant of water ($\varepsilon_w \approx 78$) increases $C_{\text{bulk}}$ by $> 300\%$ relative to dry epoxy ($\varepsilon_{\text{epoxy}} \approx 3.6$):
    $$\varepsilon_{\text{eff}} = \varepsilon_{\text{epoxy}} (1 - \phi_w) + \varepsilon_{\text{water}} \phi_w$$

---

### 2. Multi-Modal Joint Likelihood Function
Given the observed vector $\mathbf{y} = [y_{\text{US}}, y_{\text{RF}}, Z_{\text{EIS}}]$, the joint likelihood for defect hypothesis $H_k$ is factored:
$$p(\mathbf{y} \mid H_k) = p(y_{\text{US}} \mid H_k) \cdot p(y_{\text{RF}} \mid H_k) \cdot p(Z_{\text{EIS}} \mid H_k)$$
Because the three modalities observe physically orthogonal phenomena (elastic wave velocity, microwave surface reflection, and electrochemical ionic transport), cross-modal error covariance is near zero ($\text{Cov}(y_i, y_j) \approx 0$ for $i \ne j$). This guarantees rapid convergence of the posterior distribution without degenerate saddle points.
