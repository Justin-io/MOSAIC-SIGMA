# MOSAIC-CORE BGA BREAKOUT & HDI ESCAPE STRATEGY

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Package:** AMD SFVC784 ($28 \times 28$ Ball Matrix, $0.8\,\text{mm}$ Ball Pitch)  
**Board Technology:** 12-Layer HDI ($1\text{-b-}10\text{-b-}1$ or Microvia Stackup)  

---

### 1. Geometric Constraints & BGA Pitch Physics
At a ball pitch $P = 0.80\,\text{mm}$ ($31.5\,\text{mils}$):
- BGA Pad Diameter (SMD or NSMD): $D_{\text{pad}} = 0.40\,\text{mm}$ ($15.7\,\text{mils}$). Non-Solder-Mask Defined (NSMD) pads are selected for superior fatigue life.
- Solder Mask Opening: $D_{\text{mask}} = 0.50\,\text{mm}$ ($19.7\,\text{mils}$).
- Clearance between adjacent pad edges:
  $$C_{\text{pad}} = P - D_{\text{pad}} = 0.80 - 0.40 = 0.40\,\text{mm} \quad (15.75\,\text{mils})$$

```
          Pad (0.40mm)            Pad (0.40mm)
             ( O )                   ( O )
               <------- 0.80 mm ------>
                     [ 0.40 mm gap ]
```

---

### 2. Multi-Layer Escape Strategy

#### Ring 1 & Ring 2 (Outer Two Perimeter Rows):
- Routed directly on **Layer 1 (Top Copper)** without vias.
- Trace width: $w = 0.100\,\text{mm}$ ($3.9\,\text{mils}$).
- Clearance to adjacent pads:
  $$\text{Clearance} = \frac{0.40 - 0.10}{2} = 0.15\,\text{mm} \quad (5.9\,\text{mils})$$
  Well within standard PCB fabrication capabilities (minimum clearance $\ge 0.075\,\text{mm}$).

#### Ring 3 & Ring 4 (Intermediate Rows):
- Escaped using **Dog-Bone Microvias (L1 to L2)**:
  - Microvia pad diameter: $0.25\,\text{mm}$ ($9.8\,\text{mils}$).
  - Laser drill hole: $0.10\,\text{mm}$ ($3.9\,\text{mils}$).
  - Microvia placed diagonal to BGA pad at offset $\Delta x = \Delta y = 0.40\,\text{mm}$.
- Routed out on **Layer 3 (Inner Signal 01 - Stripline)**.
- Trace width: $w = 0.090\,\text{mm}$ ($3.5\,\text{mils}$) for $50\,\Omega$ controlled impedance.

#### Ring 5 & Ring 6 (Inner Rows):
- Escaped using **Staggered Microvias (L1 to L2, L2 to L3) or Buried Vias (L3 to L10)**.
- Routed out on **Layer 10 (Inner Signal 02 - Stripline)**.

#### Central Thermal / Power Core (Center $10 \times 10$ Balls):
- Dedicated to $0.85\,\text{V}$ `VCCINT` and solid `GND` return balls.
- Through-hole vias ($0.45\,\text{mm}$ pad, $0.20\,\text{mm}$ drill) connect directly to solid copper power planes on Layer 5 (`VCCINT`) and Layer 4/6/7 (`GND`).
- Decoupling capacitors (32x 0.1 uF 0402 and 24x 1.0 uF 0402) placed on the bottom layer (Layer 12) directly beneath the BGA field, connecting to via pads with $< 0.4\,\text{mm}$ trace length to minimize loop inductance ($L_{\text{loop}} < 0.25\,\text{nH}$).
