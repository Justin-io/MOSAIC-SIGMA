# MOSAIC PASSIVE CHIPLESS SENSOR TAG SPECIFICATION

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Domain:** Passive Chipless Resonant Sensor Tags (Extension Modality)  

---

### 1. Tag Concept & Physical Principle
In addition to direct material interrogation, MOSAIC-Σ supports an ecosystem of passive, chipless multi-resonant sensor tags embedded within or mounted upon composite structures.
- **Physical Structure:** Planar metallic split-ring resonators (SRRs) or C-folded dipole resonators printed directly on thin polyimide film ($25\,\mu\text{m}$ Kapton).
- **Zero Active Electronics:** The tags contain zero semiconductors, batteries, or microchips.
- **Interrogation Mechanism:** The MOSAIC-WAVE aperture illuminates the tag with a frequency sweep ($2.0 - 5.0\,\text{GHz}$). The tag re-scatters the wave, introducing sharp notch signatures into the backscatter reflection spectrum $\Gamma(f)$:
  $$f_{\text{res}} = \frac{1}{2\pi \sqrt{L_{\text{tag}} C_{\text{tag}}(\varepsilon_{\text{mat}}, \varepsilon_{\text{moisture}})}}$$
  A shift in the notch frequency $\Delta f_{\text{res}}$ directly encodes localized strain, resin cure state, or moisture concentration at the tag's physical embedding location.

---

### 2. Multi-Notch Encoding & Calibration
- **Spatial / Structural Tag IDs:** By combining 4 to 8 decoupled nested concentric rings with distinct resonant notches:
  $$\mathbf{f}_{\text{notches}} = [2.2\,\text{GHz}, 2.8\,\text{GHz}, 3.4\,\text{GHz}, 4.1\,\text{GHz}]$$
  each tag acts as an embedded structural health identifier.
- **Reader Interface:** The coherent RF reflectometer on MOSAIC-SENSE tracks the notch center frequencies with $< 0.1\,\text{MHz}$ resolution, de-embedding fixture drift via the on-PCB SOL standards.
