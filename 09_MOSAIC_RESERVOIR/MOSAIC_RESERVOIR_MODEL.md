# MOSAIC-RESERVOIR MATHEMATICAL & STATE-SPACE MODEL

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Document ID:** MOSAIC-RES-MOD-001  

---

### 1. State-Space Dynamical Formulation
The physical reservoir consists of an $N$-node coupled non-linear transmission line lattice. Let $v_k(t)$ represent the voltage at node $k \in \{1, \dots, N\}$:

$$C_k(v_k) \frac{d v_k}{d t} = \frac{v_{k-1} - v_k}{R_k} - \frac{v_k - v_{k+1}}{R_{k+1}} + \sum_{m} M_{km} \frac{d i_m}{dt} - I_{\text{diode}}(v_k) + u_k(t)$$

where:
- $C_k(v_k) = \frac{C_0}{(1 + v_k / V_R)^\gamma}$: Non-linear voltage-dependent varactor capacitance.
- $I_{\text{diode}}(v_k) = 2 I_s \sinh\left( \alpha v_k \right)$: Anti-parallel Schottky barrier diode non-linear current sink.
- $M_{km}$: Inter-resonator magnetic mutual coupling matrix.
- $u_k(t)$: Injected high-frequency material echo input signal.

---

### 2. Echo State Property & Fading Memory
For the physical reservoir to compute effectively, it must satisfy two fundamental mathematical conditions:
1. **Echo State Property (ESP):** The state trajectories $\mathbf{v}(t)$ must be asymptotically independent of initial conditions $\mathbf{v}(0)$ and uniquely driven by the input history $u(t - \tau)$. In the non-linear network, the maximum Lyapunov exponent $\lambda_{\max}$ is bounded below zero ($\lambda_{\max} < 0$) by series copper damping resistors ($R_{\text{damp}} \ge 0.5\,\Omega$).
2. **Fading Memory Time Constant:** The decay time constant of the resonant nodes is:
   $$\tau_{\text{mem}} \approx \frac{2 Q}{\omega_0} \approx \frac{2 \times 65}{2\pi \times 2.45 \times 10^9} \approx 8.4\,\text{ns}$$
   This matches the pulse width of ultrasonic and RF return echo packets ($5 - 20\,\text{ns}$), ensuring that successive reflections interfere constructively within the non-linear state space.

---

### 3. Readout Training & Computational Complexity
- **Readout Layer:** The state vector $\mathbf{x}(t) = [v_1(t), \dots, v_N(t)]^T$ is sampled by low-speed ADCs.
- **Linear Readout:**
  $$\hat{\mathbf{y}}(t) = \mathbf{W}_{\text{out}} \mathbf{x}(t)$$
  $$\mathbf{W}_{\text{out}} = \mathbf{Y}_{\text{target}} \mathbf{X}^T (\mathbf{X} \mathbf{X}^T + \lambda_{\text{reg}} \mathbf{I})^{-1}$$
- **Computational Advantage:** Training requires only a single ridge regression matrix inversion in the FPGA. Non-linear kernel mapping occurs in the analog physical domain at the speed of light, avoiding deep neural network inference power penalties.
