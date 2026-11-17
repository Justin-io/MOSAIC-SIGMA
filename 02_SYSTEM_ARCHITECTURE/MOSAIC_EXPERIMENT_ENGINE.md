# MOSAIC-Σ AUTONOMOUS EXPERIMENT ENGINE & STATE MACHINE

**Programme:** MOSAIC-Σ (Autonomous Matter Intelligence Engine)  
**Revision:** 1.0  
**Classification:** Algorithmic & Control Architecture  

---

### 1. Mathematical Formulation of the Autonomous Matter Engine
The core intelligence of MOSAIC-Σ is an active learning agent executing Sequential Bayesian Experimental Design (BED) in hardware.

#### State Space:
Let the physical state of the material under test be represented by a discrete hypothesis $H \in \{H_0, H_1, \dots, H_M\}$ or a continuous parameter vector $\boldsymbol{\theta} \in \Theta \subset \mathbb{R}^d$:
$$\boldsymbol{\theta} = \begin{bmatrix} d_{\text{defect}} & \sigma_{\text{eff}} & \varepsilon_r' & \tan\delta & h_{\text{delam}} \end{bmatrix}^T$$
where:
- $d_{\text{defect}}$: Spatial coordinates and depth of defect.
- $\sigma_{\text{eff}}$: Local electrical conductivity.
- $\varepsilon_r', \tan\delta$: Complex relative permittivity.
- $h_{\text{delam}}$: Delamination gap thickness.

#### Action Space $\mathcal{A}$:
An experiment action $a \in \mathcal{A}$ is a parameterized hardware configuration:
$$a = \langle \text{Modality } m, \text{Frequency } f, \text{Bias Mask } \mathbf{V}_{\text{bias}}, \text{Gain } G_{\text{TGC}}, \text{Averaging } N_{\text{avg}} \rangle$$
where:
- $m \in \{\text{RF\_REFLECT}, \text{ULTRASOUND\_ECHO}, \text{EIS\_KELVIN}, \text{RADAR\_STANDOFF}, \text{SELF\_CAL}\}$.
- $f \in [f_{\min}^{(m)}, f_{\max}^{(m)}]$.
- $\mathbf{V}_{\text{bias}} \in [0, 15\,\text{V}]^{64}$ (metasurface unit-cell voltages).

#### Recursive Bayesian Update:
Given measurement history $\mathcal{D}_t = \{(a_1, y_1), \dots, (a_t, y_t)\}$, upon executing action $a_{t+1}$ and observing outcome $y_{t+1}$:
$$p(\boldsymbol{\theta} \mid \mathcal{D}_{t+1}) = \frac{p(y_{t+1} \mid \boldsymbol{\theta}, a_{t+1}) \, p(\boldsymbol{\theta} \mid \mathcal{D}_t)}{\int_{\Theta} p(y_{t+1} \mid \boldsymbol{\theta}', a_{t+1}) \, p(\boldsymbol{\theta}' \mid \mathcal{D}_t) \, d\boldsymbol{\theta}'}$$

#### Expected Information Gain (EIG) Acquisition Function:
The agent evaluates candidate actions $a \in \mathcal{A}_{\text{cand}}$ by computing the Expected Mutual Information between parameter $\boldsymbol{\theta}$ and observation $Y$:
$$\mathcal{U}(a) = \mathbb{E}_{y \sim p(y \mid a, \mathcal{D}_t)} \left[ D_{\text{KL}}\left( p(\boldsymbol{\theta} \mid y, a, \mathcal{D}_t) \,\|\, p(\boldsymbol{\theta} \mid \mathcal{D}_t) \right) \right]$$
To enforce energy and thermal discipline, the acquisition is normalized by the hardware execution cost $C(a)$:
$$a^* = \arg\max_{a \in \mathcal{A}_{\text{cand}}} \frac{\mathcal{U}(a)}{\left[ C_{\text{energy}}(a) + \lambda_t C_{\text{time}}(a) \right]^\gamma}$$
where $\gamma \ge 0.5$ balances information yield against hardware dissipation.

---

### 2. Autonomous State Machine

```
+---------------------------------------------------------------------------------------+
| MOSAIC-Σ EMBEDDED REAL-TIME STATE MACHINE                                             |
|                                                                                       |
|   +--------------------+                                                              |
|   | STATE 0: INIT_BOOT | ---> Power-On Self Test (POST), Check Clocks & Voltages      |
|   +--------------------+                                                              |
|             |                                                                         |
|             v                                                                         |
|   +--------------------+                                                              |
|   | STATE 1: CAL_SOL   | ---> Automated RF Short-Open-Load & EIS Kelvin Standards     |
|   +--------------------+                                                              |
|             |                                                                         |
|             v                                                                         |
|   +--------------------+      Target Placed / Trigger Received                        |
|   | STATE 2: HYP_INIT  | <--------------------------------------------------------+   |
|   +--------------------+                                                          |   |
|             | Initialize Prior Distribution p(theta | D_0)                        |   |
|             v                                                                     |   |
|   +--------------------+                                                          |   |
|   | STATE 3: PLAN_EXP  | ---> Search Action Space A; Evaluate EIG vs. Cost        |   |
|   +--------------------+                                                          |   |
|             | Optimal Action a* Selected                                          |   |
|             v                                                                     |   |
|   +--------------------+                                                          |   |
|   | STATE 4: EXEC_STIM | ---> Program Synthesizer, Pulser, Metasurface Bias       |   |
|   +--------------------+                                                          |   |
|             | Synchronous Trigger & Baseband Digitization                         |   |
|             v                                                                     |   |
|   +--------------------+                                                          |   |
|   | STATE 5: OBS_ACQ   | ---> Coherent I/Q, Echo A-Scan, Real/Imag Impedance      |   |
|   +--------------------+                                                          |   |
|             | De-embed using Calibration Table                                    |   |
|             v                                                                     |   |
|   +--------------------+                                                          |   |
|   | STATE 6: BAYES_UPD | ---> Update Posterior p(theta | D_{t+1}); Update Entropy |   |
|   +--------------------+                                                          |   |
|             |                                                                     |   |
|             +---------> [ Check Stopping Criteria ]                               |   |
|                               |                                                   |   |
|            +------------------+------------------+                                |   |
|            | Entropy < Threshold                 | Max Steps or Timeout           |   |
|            v                                     v                                |   |
|   +--------------------+                +--------------------+                    |   |
|   | STATE 7: REPORT    |                | STATE 8: INCONCLUS |                    |   |
|   | (Defect Classified |                | (Insufficient Ev.  |                    |   |
|   | with 95% Conf.)    |                | Return Error Bounds|                    |   |
|   +--------------------+                +--------------------+                    |   |
|            |                                     |                                |   |
|            +-----------------+-------------------+                                |   |
|                              |                                                    |   |
|                              v                                                    |   |
|                     [ Next Target Cycle ] ----------------------------------------+   |
+---------------------------------------------------------------------------------------+
```

---

### 3. Stopping Criteria & Error Handling
1. **Confidence Convergence:** Terminate successfully when $\max_i p(H_i \mid \mathcal{D}) \ge 0.95$ and continuous parameter variance $\sigma_{\theta_k}^2 \le \sigma_{\text{target}}^2$.
2. **Maximum Experiment Budget:** Terminate with code `INSUFFICIENT_EVIDENCE` if $N_{\text{steps}} \ge 30$ and entropy remains above threshold. The system must **never** force a classification under excessive ambiguity.
3. **Drift Exception:** If on-board temperature sensors report $|\Delta T| \ge 1.0^\circ\text{C}$ since the last calibration, the planner immediately suspends target inspection and invokes `STATE 1: CAL_SOL` before resuming.
