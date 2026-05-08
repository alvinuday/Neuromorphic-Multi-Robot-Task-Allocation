# 🧠 THESIS BLUEPRINT & AGENT SPECIFICATION
## *"Bits to Atoms: Neuromorphic Hardware for Physical Intelligence in Industrial Robotics"*

**Author:** Alvin Adarsh Kumar  
**Degree:** Master of Science (M.S.) Physics and Bachelor of Engineering (B.E.) Computer Science 
**Supervisor:** [Advising Faculty — Prof. Dr. Debanjan Bhowmik]  
**Affiliation:** [Institution — BITS in Collaboration with IITB]  
**Target Length:** ~80–90 pages (excluding references and appendices)  
**Target Audience:** Graduate researchers, hardware engineers, roboticists, neuromorphic computing community, curious engineers, and *anyone willing to think big*  
**Public Release Intent:** Yes — designed for maximum reach and impact  
**Last Blueprint Updated:** May 2026

---

> *"Over the last few years, there has been a drastic shift in the way things work. We are seeing a lot of work being cognitively offloaded to agentic systems. These systems are becoming smart enough to be deployed on both the digital and physical realms."*
> — Alvin Adarsh Kumar, handwritten notes, 2025

---

## TABLE OF CONTENTS — BLUEPRINT

1. [Meta-Instructions for the Agent Army](#1-meta-instructions)
2. [Thesis Overview & Philosophy](#2-overview)
3. [Proposed Title & Abstract](#3-title-abstract)
4. [Chapter-by-Chapter Specifications](#4-chapters)
5. [Master Figure & Visualization List](#5-figures)
6. [Master Table List](#6-tables)
7. [Validation & Verification Specification](#7-validation)
8. [Literature Review Pipeline Specification](#8-literature)
9. [LaTeX & Formatting Specification](#9-latex)
10. [Implementation & Testing Specification](#10-implementation)
11. [Tone, Style & Voice Guide](#11-style)
12. [Publishing & Outreach Plan](#12-outreach)

---

## 1. META-INSTRUCTIONS FOR THE AGENT ARMY

This document is the **single source of truth** for the entire thesis production pipeline. Every agent in the pipeline should read this document in full before beginning any task.

### 1.1 What This Document Is

This is a **pre-thesis specification document** — a blueprint that describes:
- **What** every section contains, down to the paragraph level
- **Why** each section exists (narrative purpose)
- **How** it should look (figures, tables, equations, layout)
- **What** needs to be verified/validated before writing
- **Where** to find or generate the relevant data

### 1.2 What This Document Is NOT

- It is NOT the thesis itself
- It is NOT a literature survey (the lit survey is auto-generated via Python pipeline — see Section 8)
- It is NOT a final version — it is a living spec that can be updated by the Architect Agent

### 1.3 Agent Roles & Assignments

| Agent Role | Primary Tasks | Key Sections |
|---|---|---|
| **Architect Agent** | Keep this blueprint updated; resolve conflicts | All |
| **Writer Agent** | Write prose for all sections following voice guide | §4, §11 |
| **Math Agent** | Verify all equations, derivations, proofs | §4.4–4.7, §7 |
| **Figure Agent** | Generate all plots, diagrams, visualizations | §5 |
| **Table Agent** | Generate all tables from data/derivations | §6 |
| **Literature Agent** | Run Python pipeline, extract citations, write summaries | §8 |
| **Validator Agent** | Run numerical experiments, hand-verify key results | §7 |
| **LaTeX Agent** | Assemble final PDF in LaTeX | §9 |
| **QA Agent** | Final pass: consistency, citations, grammar, flow | All |

### 1.4 Critical Consistency Rules

- **Notation is fixed**: all symbols defined in §9.3 must be used consistently across ALL sections
- **The handwritten derivation (SNN_MPC) uses point-mass arms** ($I=0$); the full derivation (uploaded PDF) uses **distributed-rod arms** ($I = ml^2/3$). The thesis uses the **distributed rod** model throughout — this is the more physically accurate version and is what is in the SNN_MPC_Complete_Derivation.md file
- **Example numbers**: the MRTA worked example uses $N=3, M=2, k=2$ throughout — do not change these without updating ALL tables and figures that reference it
- **The OIM worked example** corresponds exactly to the handwritten notebook pages 24–39 — all numbers must match
- **Tone**: conversational-academic hybrid (see §11). Do not write in dry journal prose. Write like you're explaining to a brilliant friend.

---

## 2. THESIS OVERVIEW & PHILOSOPHY

### 2.1 The Story in One Paragraph

> The world is automating. Machines are moving from spreadsheets and databases into factories, hospitals, and homes. But here's the thing nobody talks about enough: *the hardware is the bottleneck*. The algorithms are brilliant — Model Predictive Control, combinatorial optimization, multi-agent coordination — but they still run on silicon chips designed for spreadsheets. This thesis asks a different question: what if we built hardware that *thinks like the problem itself*? What if we solved robot coordination problems on networks of coupled oscillators, and control optimization on networks of spiking neurons? What if the silicon looked less like a calculator and more like a brain? This is the story of two experiments in physical intelligence — and a vision for where India, and the world, should go next.

### 2.2 The "Bits to Atoms" Frame

The thesis is organized around a **central metaphor**: the journey from **bits** (digital computation, abstract optimization) to **atoms** (physical machines, physical hardware, the real world). 

- **Bits**: QUBO formulations, QP optimization, binary variables
- **The Bridge**: Neuromorphic hardware (OIM, SNN) — the interface layer between digital problem statements and physical computation
- **Atoms**: Robot arms moving, warehouses allocating tasks, factories coordinating, India manufacturing at scale

This frame should appear in:
- The cover/front matter (visual metaphor)
- The introduction
- The conclusion
- Chapter transitions

### 2.3 Why This Matters (The "So What")

The thesis must make three levels of argument:

**Level 1 — Technical:** OIM and SNN hardware can solve robotics optimization problems (task allocation, motion control) with competitive quality and potentially orders-of-magnitude better energy-delay product than classical solvers.

**Level 2 — Systems:** These solvers can be integrated into real robot pipelines. The full chain from physics → math → hardware → allocation/control is not just theoretically possible but practically achievable.

**Level 3 — Civilizational:** Post-silicon hardware is the next frontier. Countries like India that invest in neuromorphic manufacturing ecosystems now will define the next economy. The democratization argument: cheaper chips → cheaper robots → cheaper goods → broader prosperity.

**WRITER AGENT NOTE:** Level 3 belongs in the introduction and conclusion, not in technical chapters. Keep it grounded in evidence (cite India's electronics manufacturing push, Semicon India policy, etc.). Don't let it become empty rhetoric.

### 2.4 What Makes This Thesis Unique

Most neuromorphic-robotics work is either:
(a) Hardware papers with toy benchmarks, or
(b) Robotics papers that treat hardware as a black box

This thesis sits at the **intersection**: it derives the full mathematical chain from first principles, maps it to real hardware, and validates every step by hand. It is also unusual for its:

- **India perspective**: explicit argument for India's role in the neuromorphic chip ecosystem
- **Conversational style**: written like a brilliant person explaining their work, not a journal paper
- **Full hand-verification**: every key number is computed by hand AND by code
- **Honest failure analysis**: we do not hide OIM's limitations — we study them

---

## 3. PROPOSED TITLE & ABSTRACT

### 3.1 Candidate Titles (Pick One, Architect to Decide)

1. **"Bits to Atoms: Neuromorphic Computing for Physical Intelligence in Industrial Robotics"** *(recommended — broad, memorable, captures the frame)*
2. "Oscillators as Allocators, Neurons as Controllers: Neuromorphic Hardware for Multi-Robot Systems"
3. "Physical Intelligence at the Edge: Spiking Networks and Ising Machines for Real-Time Robot Optimization"
4. "From QUBO to Motion: Neuromorphic Approaches to Coalition Task Allocation and Model Predictive Control"

**Recommended subtitle:** *"A Study in OIM-Based Coalition Task Allocation and SNN-Based Model Predictive Control for Industrial Robotic Systems"*

### 3.2 Abstract Specification

**Length:** 300–350 words  
**Structure:** Problem → Gap → This work → Methods → Results → Significance  
**Tone:** Authoritative, clear, accessible. Avoid jargon in first two sentences.

**Paragraph 1 — Hook & Problem (60 words):**  
Open with the industrial automation context. The convergence of agentic AI and physical robotics is creating demand for real-time optimization solvers that can run at the edge — on robots themselves. Classical solvers (MILP, OSQP) are too slow or too power-hungry for embedded deployment. [Do NOT start with "This thesis..."]

**Paragraph 2 — Gap & Opportunity (60 words):**  
Neuromorphic hardware — systems that compute like brains — offers a physically different approach. Oscillator Ising Machines (OIMs) and Spiking Neural Networks (SNNs) are hardware architectures that encode optimization problems in their physical dynamics. They are CMOS-compatible and promise orders-of-magnitude improvements in energy-delay product. However, their application to practical robotics problems remains underexplored.

**Paragraph 3 — This Work (80 words):**  
This thesis presents a complete, verified framework for two robotics optimization problems solved on neuromorphic hardware. First: Coalition Multi-Robot Task Allocation (CMRTA), formulated as Maximum Weight Independent Set → QUBO → Ising Hamiltonian and solved on an OIM. Second: Model Predictive Control (MPC) for a 2-DOF robotic arm, formulated as a Quadratic Program and solved via a Proportional-Integral Projected Gradient (PIPG) algorithm mapped to an analog Spiking Neural Network.

**Paragraph 4 — Methods & Results (80 words):**  
We provide full mathematical derivations from first principles, explicit worked examples with hand-verified numerical results, and a Python-based experimental validation framework. For CMRTA: the OIM achieves approximation ratios ≥0.85 on realistic spatial instances, with end-to-end solve times of ~5–15 ms. For SNN-MPC: convergence is achieved within 55–80 PIPG iterations (~20 ms solve time), with >100× energy-delay improvement over classical CPU solvers. Penalty coefficient bounds and Ising parameter derivations are formally verified.

**Paragraph 5 — Significance (50 words):**  
This work demonstrates that post-silicon neuromorphic hardware can be productively deployed in industrial robotics pipelines today. It also argues for India's strategic opportunity in neuromorphic chip manufacturing. The results provide a foundation for future embedded neuromorphic controllers in edge robotics applications.

**Keywords (8–10):** Neuromorphic Computing, Oscillator Ising Machine, Spiking Neural Network, Multi-Robot Task Allocation, Model Predictive Control, QUBO, Industrial Robotics, Physical Intelligence, Edge Computing, Post-Silicon Hardware

---

## 4. CHAPTER-BY-CHAPTER SPECIFICATIONS

---

### CHAPTER 0 — PREFACE / AUTHOR'S NOTE

**Page target:** 2–3 pages  
**Tone:** Personal, philosophical, first-person. This is the author's voice, not academic prose.  
**Purpose:** Set the stage. Invite the reader into the journey. Explain why this work exists.

**Content Outline:**

**Opening paragraph:** Begin with a personal observation — watching automation accelerate, watching agentic systems take over cognitive tasks, wondering what happens when they enter the physical world. Reference the handwritten notes' framing: *"Over the last few years, there has been a drastic shift in the way things work..."*

**The Question:** Every breakthrough in intelligence — biological or artificial — comes when the *hardware* catches up to the *algorithm*. Deep learning didn't work until GPUs made it possible. What is the GPU-moment for physical intelligence? The author's answer: neuromorphic hardware.

**The Journey:** Brief honest account of how this thesis came to be. What was the author trying to solve? What surprised them? What did they learn about the limits of their own approach?

**India Paragraph:** Why India? Why now? The author's belief: India built a mobile revolution by enabling cheap, reliable connectivity. The next revolution is cheap, reliable physical intelligence — robots, edge devices, biomechanical sensors. The argument for neuromorphic manufacturing in India should feel like a conviction, not a policy paper.

**Invitation:** "I've written this thesis as a conversation. I want you to argue with it, build on it, prove me wrong. The footnotes are for when I'm being pedantic. The main text is for when I'm being myself."

**Visual:** A hand-drawn style illustration (or photograph of the author's notebook) showing the "bits to atoms" concept — digital signals transforming into a robot arm or factory floor.

---

### CHAPTER 1 — INTRODUCTION: A NEW KIND OF HARDWARE FOR A NEW KIND OF PROBLEM

**Page target:** 12–15 pages  
**Tone:** Narrative-explanatory. Start with stories, build to technical framing.  
**Purpose:** Orient the reader. Establish the problem, the opportunity, and this work's place in the landscape.

#### 1.1 The World is Automating (3–4 pages)

**Opening story:** Describe a warehouse — hundreds of robots, thousands of tasks, microsecond decisions. Or describe a surgical robot. Or a precision agriculture drone fleet. The point: **coordination** is the hard problem, not raw capability. A single robot moving is solved. A thousand robots cooperating in real time is not.

**The optimization bottleneck:** Every multi-robot system has, at its core, an optimization problem: who does what, when, with whom. These problems are NP-hard in general. Classical solvers (MILP, constraint programming) work on a laptop in a lab but fail on an embedded processor with a 10 ms deadline.

**The control bottleneck:** Model Predictive Control is the gold standard for trajectory optimization. At its core: solve a quadratic program every 20 ms. On a CPU, this is feasible for small robots. For legged robots (ANYmal), quadrupeds, humanoids — the QP is large and the deadline is tight.

**Key quote to include:** From Mangalore et al. (2024): *"When applied to model predictive control problems for the quadruped robotic platform ANYmal, the neuromorphic method achieves over two orders of magnitude reduction in combined energy-delay product..."*

**Analogy:** Classic computers are like calculators — great at arithmetic, bad at finding the lowest valley in a rugged landscape. Neuromorphic hardware is like physics itself — systems that *fall* to their minimum energy state, because that's what physics does. The question is whether we can engineer that fall to solve our problems.

#### 1.2 A Brief History of Computing Paradigms (2–3 pages)

**Structure:** Timeline/narrative hitting key inflection points:
- Von Neumann architecture (1945): separate memory and compute → great for sequential tasks, bad for parallel/adaptive tasks
- GPUs (1990s–2000s): parallel arithmetic → unlocked deep learning
- TPUs/accelerators (2010s): specialized arithmetic → further unlocked AI
- **The coming inflection:** Post-silicon hardware: memristors, FeFETs, OIMs, SNNs → designed for optimization and inference, not arithmetic

**The key insight:** Each paradigm shift matched hardware to a *new class of problems*. Von Neumann matched digital logic. GPUs matched matrix multiplication. The question for neuromorphic is: *what class of problems does it natively solve?* Answer: energy minimization, constraint satisfaction, approximate combinatorial optimization.

**FIGURE 1.1:** Timeline visualization — "The Hardware-Algorithm Co-evolution" — showing each era's dominant hardware and the class of problems it unlocked. Should be beautiful and clear.

**Key references:** Mead (1990) "Neuromorphic electronic systems"; Davies et al. (2021) "Advancing neuromorphic computing"; Schuman et al. (2022) review.

#### 1.3 Neuromorphic Hardware: A Primer (3 pages)

**What is neuromorphic?** Coined by Carver Mead (Caltech, 1990): hardware that mimics the structure and/or dynamics of biological neural systems. Not necessarily mimicking the brain's *intelligence* — rather its *computational efficiency*.

**Two flavors relevant to this thesis:**

**(A) Oscillator Ising Machines (OIM):**  
- Physical systems of coupled oscillators (CMOS ring oscillators, FeFET-based, LC oscillators)  
- Each oscillator settles to phase 0 or π → binary spin +1 or -1  
- Coupling between oscillators encodes the Ising Hamiltonian  
- System naturally minimizes energy → finds approximate QUBO solutions  
- Key paper: Wang & Roychowdhury (2019, 2021)  
- **Analogy:** Like a room full of people clapping — they naturally synchronize into patterns. The pattern encodes the solution.

**(B) Spiking Neural Networks (SNN) on Neuromorphic Chips:**  
- Neurons communicate via discrete spikes (events), not continuous signals  
- Sparse, event-driven computation → massive energy savings vs. continuous ANN  
- Intel Loihi 2: 128 cores, up to 1M neurons  
- Bhowmik Group (IIT Bombay): analog SNN using spintronic synapses  
- When PIPG algorithm is mapped to SNN dynamics, MPC QP is solved in spike-time  
- **Analogy:** Rather than calculating every number in a gradient descent, you only "fire" when something changes. Like a brain that stays quiet until something moves, then responds instantly.

**FIGURE 1.2:** Side-by-side comparison diagram — conventional CMOS chip (arithmetic units, cache, bus) vs. OIM chip (coupled oscillators, coupling matrix) vs. SNN chip (neuron arrays, spike buses). Make it visually striking.

**FIGURE 1.3:** The energy-delay product comparison chart — OIM/SNN vs. CPU/GPU for optimization tasks. Based on published data from Mangalore et al. (2024), Honjo et al. (2021), McMahon et al. (2016).

#### 1.4 This Thesis: Two Experiments (2 pages)

Clear, direct statement of what this thesis does:

**Experiment 1 — Allocation:** We take the Coalition Multi-Robot Task Allocation problem, derive its full mathematical structure, map it to QUBO and then to Ising, and solve it on an OIM. We verify every step — from conflict graph construction to penalty coefficient bounds to oscillator dynamics.

**Experiment 2 — Control:** We take a 2-DOF robotic arm, derive its nonlinear dynamics from the Lagrangian, linearize and discretize, formulate MPC as a QP, apply the PIPG algorithm, and map it to an analog SNN. We trace the entire pipeline numerically.

**FIGURE 1.4:** "The Pipeline" — a single horizontal diagram showing the full flow:  
`[Physical Robot] → [Mathematical Model] → [Optimization Problem] → [Neuromorphic Hardware] → [Solution] → [Robot Action]`  
This figure is the thesis's organizing visual and should appear on the inside cover / first chapter page.

#### 1.5 Contributions (1 page)

Numbered list, precise and honest:

1. **Complete CMRTA→MWIS→QUBO→Ising chain** with formal proofs of equivalence, explicit conflict graph construction rules, and penalty coefficient bounds with analytical derivation.
2. **Worked 7-node MRTA example** with all numerical values computed by hand and verified by code.
3. **Formal penalty coefficient analysis**: Theorem stating the sufficient condition $\lambda > \max_{(i,j)\in E}(w_i + w_j)$ with proof, and analysis of the tightness of this bound.
4. **Hardware-aware scalability framework**: coalition bounding (CB) and spatial proximity pruning (SP) with complexity analysis and hardware node budget calculations.
5. **Full SNN-MPC pipeline** from Lagrangian robot dynamics to PIPG iterations, with 5-iteration hand calculation verified against analytical solution.
6. **Case studies** for three robot arm configurations (Cases A, B, C) with full Jacobian and equilibrium calculations.
7. **India-focused policy analysis**: quantitative argument for neuromorphic chip manufacturing ecosystem.
8. **Python validation pipeline**: open-source code for all experiments.

#### 1.6 Thesis Roadmap (0.5 page)

One paragraph per chapter, telling the reader what's coming and *why in that order*. Should read like a story outline, not a table of contents.

---

### CHAPTER 2 — BACKGROUND & RELATED WORK

**Page target:** 15–18 pages  
**Tone:** Survey-like but opinionated. Don't just describe papers — tell the reader what each contribution added and what it left unsolved.  
**Purpose:** Place this work in context. Show you know the field. Identify the gap.

**LITERATURE AGENT NOTE:** This chapter is auto-generated via the Python pipeline described in §8, but the Writer Agent must then rewrite it in the thesis voice. The pipeline generates structured summaries; the writer makes them flow.

#### 2.1 Combinatorial Optimization on Physical Hardware (4 pages)

**Opening:** The idea that physics can compute is old. Boltzmann machines, Hopfield networks, quantum annealing — all exploit physical dynamics to minimize energy. The modern resurgence is driven by the maturation of fabrication technologies.

**Coverage (chronological + thematic):**

**(A) Ising Model & QUBO:**  
- Lucas (2014) *"Ising formulations of many NP problems"* — the canonical reference showing that NP-hard problems (Max-Cut, TSP, graph coloring, MIS) map to Ising. **Must read.** Summarize Table 1 from that paper.
- Kochenberger et al. (2014) QUBO survey — connecting integer programming to QUBO.
- Glover, Kochenberger & Du (2019) *"A tutorial on formulating and using QUBO models"*

**(B) Quantum Annealers:**  
- D-Wave systems — 5000+ qubits, probabilistic tunneling, cloud access.
- Limitations: cryogenic infrastructure, limited connectivity, calibration noise.
- Results: Max-Cut, portfolio optimization, logistics.
- Reference: King et al. (2023) Nature

**(C) Coherent Ising Machines (CIM):**  
- Optical parametric oscillators — McMahon et al. (2016) Science.
- 100,000 spin scale: Honjo et al. (2021) Science Advances.
- Fast but expensive and non-portable.

**(D) Oscillator Ising Machines (OIM):** ← primary focus
- Wang & Roychowdhury (2019, 2021) — foundational theory and CMOS demonstration.
- Dutta et al. (2021) — FeFET-based OIM.
- Raychowdhury et al. (2019) — VO₂ oscillator demonstrations.
- Key advantage: CMOS-compatible → embeddable.
- Key question: approximation quality vs. graph structure?

**(E) Simulated Bifurcation Machines (SBM):**  
- Goto et al. (2019), Tatsumura et al. (2021) — FPGA-based, digital, fast.
- Honorable mention; not the focus.

**Synthesis box:** Create a "comparison table" of hardware IM platforms — substrate, scale (spins), deployment, approximate quality, power. This becomes Table 2.1 in the thesis.

#### 2.2 Multi-Robot Task Allocation (3 pages)

**Taxonomy:** Use the Gerkey & Matarić (2004) MRTA taxonomy — ST-SR-IA, ST-MR-IA, MT-MR-IA, etc. Place coalition MRTA in the MT-MR bucket.

**Key papers:**
- Gerkey & Matarić (2004) — foundational taxonomy
- Sandholm et al. (1999) — coalition structure generation complexity
- Shehory & Kraus (1998) — early coalition formation methods
- Vig & Adams (2006) — market-based task allocation
- Graber & Hofmann (2024) — modern coalition MRTA formulation ← direct predecessor
- Jones et al. (2011) — MRTA survey

**Gap:** No prior work maps coalition MRTA to QUBO/Ising or attempts OIM hardware solution. The MWIS formulation is novel for coalition MRTA.

#### 2.3 Model Predictive Control for Robots (3 pages)

**What is MPC?** Receding-horizon optimal control — solve QP at every timestep, apply first control input, shift horizon. Standard reference: Rawlings, Mayne & Diehl (2020) *"Model Predictive Control: Theory, Computation, and Design"* 2nd ed.

**Key papers in robot MPC:**
- Neunert et al. (2018) — real-time MPC for legged robots
- Di Carlo et al. (2018) — MIT Cheetah MPC
- Grandia et al. (2023) — ANYmal perceptive MPC
- Sleiman et al. (2021) — unified MPC for ANYmal

**The QP solver bottleneck:**
- OSQP (Stellato et al., 2020) — state-of-the-art CPU solver
- HPIPM (Frison & Diehl, 2020) — structured QP solver
- All require CPU/GPU → power-hungry, latency issues at edge

**Neuromorphic MPC:**
- Mangalore et al. (2024) — **key paper** — Loihi 2 + PIPG for ANYmal → 100× EDP improvement
- Yu, Elango & Açıkmeşe (2021) — PIPG algorithm paper

#### 2.4 Neuromorphic Computing: Platforms & Programming (3 pages)

**Coverage:**
- Intel Loihi / Loihi 2: Davies et al. (2018, 2021), Orchard et al. (2021)
- IBM TrueNorth: Merolla et al. (2014) Science
- BrainScaleS: Furber (2016)
- SpiNNaker: Furber et al. (2014)
- Bhowmik Group (IIT Bombay) — analog spintronic SNN → closest to this thesis
- LIF neuron model — standard reference: Gerstner & Kistler (2002)

**Programming paradigms:**  
- Rate coding vs. temporal coding vs. Δ-modulation
- Neuromorphic compilers: PyNN, Norse, Lava (Intel)
- The challenge: mapping algorithms designed for digital hardware to event-driven spiking substrate

#### 2.5 Related Work on Oscillator Dynamics & Optimization (2 pages)

- Kuramoto model (1984) — original coupled oscillator model, synchronization theory
- Hopfield networks (1982, 1985) — continuous Hopfield network for TSP, seminal
- Delacour et al. (2025) LagONN — Lagrangian oscillator neural networks for constrained QP (distinct from our binary QUBO approach)
- Chou et al. (2019) — analog VLSI coupled oscillators for graph problems

#### 2.6 The India Context: Neuromorphic Manufacturing (1 page)

**Framing:** Not a policy paper, but an argument grounded in economics and history.

**Key datapoints to include/research:**
- India's mobile revolution: from 2G to 5G, from near-zero to world's largest data market
- Semicon India Programme (2021) — ₹76,000 crore investment in semiconductor ecosystem
- India's manufacturing cost advantage for analog chips vs. digital VLSI
- Post-silicon technologies (memristors, FeFET, spintronic) are less mature → entry barrier is lower → opportunity
- Bhowmik group at IIT Bombay as existence proof

**The argument:** Countries that built the transistor didn't need to understand biology to build CPUs. Countries that build neuromorphic hardware don't need to solve AGI to democratize physical intelligence.

---

### CHAPTER 3 — SYSTEM OVERVIEW: THE BITS-TO-ATOMS ARCHITECTURE

**Page target:** 4–6 pages  
**Tone:** Clear, architectural, use diagrams heavily  
**Purpose:** Give the reader the "map" before the details. This is the chapter people will share.

#### 3.1 The Four-Layer Architecture

Present a layered architecture diagram (FIGURE 3.1 — "The Stack"):

```
┌─────────────────────────────────────────┐
│  LAYER 4: PHYSICAL WORLD                │
│  Robots, factories, sensors, actuators  │
├─────────────────────────────────────────┤
│  LAYER 3: NEUROMORPHIC HARDWARE         │
│  OIM chip (allocation) + SNN chip (ctrl)│
├─────────────────────────────────────────┤
│  LAYER 2: MATHEMATICAL ENCODING         │
│  QUBO, Ising H, Quadratic Program, KKT  │
├─────────────────────────────────────────┤
│  LAYER 1: PROBLEM FORMULATION           │
│  CMRTA objective, MPC objective         │
└─────────────────────────────────────────┘
```

Explain each layer and how information flows up and down. Key insight: **downward flow** = problem encoding; **upward flow** = solution readout.

#### 3.2 Two Use Cases, One Philosophy

Table comparing the two use cases:

| | CMRTA (Allocation) | MPC (Control) |
|---|---|---|
| **Input** | Robot capabilities, task requirements, positions | Current joint angles/velocities, target pose |
| **Problem Type** | Binary combinatorial (NP-hard) | Continuous quadratic (polynomial) |
| **Hardware** | OIM (coupled oscillators) | Analog SNN (spiking neurons) |
| **Output** | Allocation assignment | Incremental torque commands |
| **Timescale** | 5–15 ms | 15–20 ms (per MPC step) |
| **Analogy** | "Who does what?" | "How to move?" |

#### 3.3 The Classical vs. Neuromorphic Comparison

Use a race-track analogy: classical solvers and neuromorphic hardware are racing to the answer. Classical is faster on the straightaways (numerical arithmetic), neuromorphic wins on the curves (energy minimization, constraint satisfaction). The question is: which race track does your problem live on?

**FIGURE 3.2:** "The Trade-off Space" — scatter plot (approximate): axes = problem size vs. time-to-solution, with regions colored for where each solver type wins. Clearly mark the robotics-relevant window.

---

### CHAPTER 4 — COALITION MULTI-ROBOT TASK ALLOCATION VIA OSCILLATOR ISING MACHINE

**Page target:** 22–26 pages  
**Tone:** Rigorous but narrative. Each derivation should be preceded by "why we're doing this" and followed by "what this tells us."  
**Purpose:** Complete, from-scratch derivation of the CMRTA→OIM pipeline.

#### 4.1 Motivating Scenario: The Warehouse Floor (1.5 pages)

**Tell a story:** A warehouse with 10 robots and 5 tasks. Task 1 needs a heavy lifter AND a gripper — no single robot can do it alone. Task 2 just needs any robot with a camera. Task 3 requires three specialists. Classic task allocation algorithms either enumerate all combinations (exponentially slow) or use greedy heuristics (bad solutions). The warehouse manager needs an answer in 100 ms, not 10 seconds.

**Define the problem precisely after the story** — connect the story to the mathematical objects.

**FIGURE 4.1:** The warehouse scenario — a schematic showing robots with capability labels (icons: strength ⚡, camera 📷, gripper 🤖) and tasks with requirement labels. Colorful, clear, memorable.

#### 4.2 Mathematical Problem Formulation (3 pages)

Present all definitions formally, but with plain-English explanations in parallel.

**Definition 4.1 (Robot Capability Vector):**  
$$\mathbf{c}_i = [c_i^{(1)}, \ldots, c_i^{(K)}]^T \in \mathbb{R}^K$$  
*"Each robot has a profile — how much of each type of capability it brings. Robot 1 might have strength=2, camera=0; Robot 3 has strength=1, camera=1."*

**Definition 4.2 (Task Requirement Vector):**  
$$\mathbf{q}_j = [q_j^{(1)}, \ldots, q_j^{(K)}]^T \in \mathbb{R}^K$$

**Definition 4.3 (Feasible Coalition):** Capability sum ≥ requirements for all K types.

**Definition 4.4 (Utility Function):**  
$$U(S, j) = V_j \cdot \phi(S, j) - \sum_{r_i \in S} \text{cost}(r_i, j)$$  
Explain each component. Note: $\phi = \exp(-\alpha \cdot \text{excess})$ penalizes wasteful over-provisioning.

**Definition 4.5 (Coalition Allocation):** Set of (coalition, task) pairs satisfying disjointness, uniqueness, and feasibility.

**The Objective:** Maximize total utility — equation in a boxed display.

**Worked example setup:** Introduce the $N=3, M=2, K=2$ example here and carry it through the entire chapter.

**TABLE 4.1:** The example — robots × capabilities matrix, tasks × requirements matrix.

#### 4.3 From MRTA to Maximum Weight Independent Set (4 pages)

**The key insight** (explain with words before math): If we think of each (coalition, task) pair as a "candidate allocation," then finding the best total allocation is the same as finding the largest set of candidates that don't conflict with each other. This is exactly the Maximum Weight Independent Set problem.

**Step 1 — Coalition explosion:** Show $|\mathcal{C}| \leq M \cdot 2^N$ calculation. For $N=20, M=10$: ~10M candidates. Not tractable.

**Step 2 — Coalition bounding (CB):** Restrict to coalitions of size ≤ k. Derive complexity reduction. For $k=2, N=20, M=10$: ≤ 2100 candidates. Hardware-feasible.

**Step 3 — Feasibility enumeration:** Show the feasibility check for each candidate. **TABLE 4.2:** Feasibility check table for the worked example (all 6 candidates × 2 tasks).

**Step 4 — Utility calculation:** Apply utility formula to all feasible candidates. **TABLE 4.3:** Utility table with columns: Coalition, Task, Combined capability, Excess, φ, Travel costs, U(S,j). All numbers hand-verified.

**Step 5 — Conflict graph construction:**  
Two types of conflicts — robot conflict ($S_a \cap S_b \neq \emptyset$) and task conflict ($j_a = j_b$).  

Formal definition of edge rule, then:  
**FIGURE 4.2:** The conflict graph for the worked example. Show all 7 nodes (only nodes with U>0), all 18 edges, edge types distinguished by color (robot conflict = red, task conflict = blue, both = purple). Node sizes proportional to utility weight.  
This is the most important single figure in the chapter. Make it beautiful. Label every node and edge.

**Lemma 4.1 (MRTA = MWIS):** State formally. Proof in 10 lines — clear and complete.

#### 4.4 QUBO Formulation (4 pages)

**The key idea:** MWIS has constraints ($x_i + x_j \leq 1$). QUBO has none. We absorb constraints as a penalty in the objective.

**The penalty method:** Introduce $\lambda x_i x_j$ penalty for conflict edges.

**Theorem 4.1 (Penalty Bound):** State formally:  
*"If $\lambda > \max_{(i,j)\in E}(w_i + w_j)$, then every QUBO minimizer is a feasible MWIS solution."*  
**Proof:** Must be complete and clean, 1 page maximum. This is a validation anchor — see §7.

**QUBO matrix form:** $\mathcal{Q}(\mathbf{x}) = \mathbf{x}^T Q \mathbf{x}$, identify $Q_{ii} = -w_i$ and $Q_{ij} = Q_{ji} = \lambda/2$.

**Full QUBO matrix for worked example:** Show the $7 \times 7$ matrix explicitly. **TABLE 4.4.** Every entry calculated by hand.

**Verification:** Compute $\mathcal{Q}(\mathbf{x})$ for the optimal solution and 2–3 suboptimal solutions. Verify that optimal has lowest QUBO value. **TABLE 4.5:** QUBO evaluation table.

**Note on penalty coefficient selection:** In practice, set $\lambda = 2 \cdot \max_v w_v$ as a conservative heuristic. Discuss the tightness issue — overly large $\lambda$ makes conflict penalties dominant and weakens utility optimization. This is a subtle but important practical point.

#### 4.5 Ising Hamiltonian Mapping (3 pages)

**The substitution:** $x_k = (1 + s_k)/2$, $s_k \in \{-1, +1\}$.

**Full derivation** of QUBO → Ising expansion. Do NOT skip steps — every intermediate expression matters for understanding. This is the algebraic core of the chapter.

$$h_k = -\frac{w_k}{2} + \frac{\lambda \deg_E(k)}{4}, \quad J_{ij} = \frac{\lambda}{4} \mathbf{1}[(i,j)\in E]$$

**Physical interpretation box:** What does $h_k$ mean? It's a bias pulling spin $k$ toward +1 (selected). High-utility nodes have strong positive bias. But high-degree nodes (many conflicts) have their bias reduced — a self-regulating mechanism. Explain with the worked example numbers.

**TABLE 4.6:** Ising parameters for worked example — for each node: $w_v$, $\deg_E(v)$, $h_v$; for each edge: $J_{ij}$.

#### 4.6 OIM Dynamics (3 pages)

**The physical system:** Coupled nonlinear oscillators. Each oscillator has phase $\theta_i \in [0, 2\pi)$. Phases self-organize under coupled dynamics.

**Phase dynamics equation:**  
$$\frac{d\theta_i}{dt} = K_{ii} \sin(2\theta_i) + \sum_{j \neq i} K_{ij} \sin(\theta_j - \theta_i) + \xi_i(t)$$  

where $K_{ii}$ is the injection locking strength (bias), $K_{ij}$ is the coupling, $\xi_i(t)$ is noise.

**Binarization:** $\theta_i \approx 0 \Rightarrow s_i = +1$ (selected); $\theta_i \approx \pi \Rightarrow s_i = -1$ (not selected).

**OIM parameter derivation:** From Ising → OIM:  
$$K_{ij} = -2J_{ij}, \quad I_{\text{bias},i} = -h_i$$

**FIGURE 4.3:** OIM dynamics simulation for the worked example. Show phase trajectories $\theta_i(t)$ over time for all 7 nodes. Highlight convergence to binarized phases. Use a clean time-series plot with colored lines per node.

**Sign interpretation:** Conflict edge → $K_{ij} < 0$ → anti-ferromagnetic → phases prefer $\pi$ apart → spins anti-aligned → at most one selected. Draw this as an intuition diagram (FIGURE 4.4).

**Convergence analysis:** Brief discussion of conditions for convergence, typical convergence time, and effect of noise term (helps escape local minima).

#### 4.7 Hardware-Aware Scalability (2 pages)

**The constraint:** Current CMOS OIM hardware: ~100–2000 nodes. FeFET-based: potentially ~10,000.

**Strategy 1 — Coalition Bounding (CB):** Already covered in 4.3. Tabulate scale reduction.

**Strategy 2 — Spatial Proximity Pruning (SP):** Only include robot-task pairs where robots are within radius $r_{\max}$ of the task. Derive effective reduction.

**Strategy 3 — Graph Decomposition:** For very large instances, decompose by spatial clusters. Solve each cluster independently on OIM. Merge solutions with greedy repair.

**TABLE 4.7:** Scalability table — for different $(N, M, k)$ configurations: $|V|$ before pruning, $|V|$ after CB, $|V|$ after CB+SP, OIM feasibility.

**FIGURE 4.5:** Scaling plot — $|V|$ vs. $N$ for different $k$ and pruning strategies. Show the "feasibility window" where OIM can run.

#### 4.8 The Hybrid Pipeline (1 page)

Present the full pipeline diagram (already described in §1.4 but expanded here):  
Pre-processing (classical) → OIM solve → Post-processing (classical).  

**TABLE 4.8:** Timing breakdown — each pipeline stage, typical duration, notes.

**FIGURE 4.6:** The hybrid pipeline block diagram. Clean, colored, with timing annotations.

#### 4.9 Failure Modes & Honest Limitations (1 page)

**Be honest.** This is rare in theses and immediately distinguishes good work from great work.

- Local minima: dense conflict graphs trap OIM → multi-restart strategy
- Calibration sensitivity: real OIM hardware has fabrication noise → coupling mismatch
- Static problem only: OIM solves one-shot; dynamic MRTA needs warm-starting
- Coupling programmability latency: reprogramming weights takes time

For each failure mode: describe the problem, quantify the impact if data exists, and propose a mitigation.

---

### CHAPTER 5 — MODEL PREDICTIVE CONTROL VIA ANALOG SPIKING NEURAL NETWORK

**Page target:** 22–25 pages  
**Tone:** Pedagogical. This is the "show your work" chapter. Every step should feel like a tutorial. Use worked numbers everywhere.  
**Purpose:** Complete, verified derivation from robot physics to SNN iterations.

#### 5.1 The Control Problem: Moving a Robot Arm (1.5 pages)

**Story:** A robot arm needs to move from [0°, 0°] to [45°, 45°]. Simple to say, hard to do — because gravity is always pulling, inertia changes with configuration, and you only have 20 ms between control updates. Classical approaches work. But can a network of spiking neurons do it better?

**FIGURE 5.1:** The 2-DOF robot arm diagram. Beautiful, labeled schematic showing:
- Base pivot (fixed)
- Link 1 (length $l_1 = 0.5$ m, mass $m_1 = 1$ kg)  
- Link 2 (length $l_2 = 0.5$ m, mass $m_2 = 1$ kg)
- Joint angles $\theta_1$, $\theta_2$
- Torques $\tau_1$, $\tau_2$
- Gravity arrow
- End-effector position
- Initial and target configurations shown simultaneously

#### 5.2 Robot Physics from First Principles (4 pages)

**Philosophy:** "We could just write down the answer. Instead, we'll derive it from scratch — because understanding where equations come from is the difference between a user and an engineer."

**The Lagrangian approach:** Define kinetic energy $T$, potential energy $V$, Lagrangian $\mathcal{L} = T - V$. Reference: Lynch & Park *Modern Robotics* Ch. 8.

**Kinetic energy derivation:**  
Step 1 — Velocity of link 1 tip.  
Step 2 — Velocity of link 2 tip (end-effector) via Jacobian.  
Step 3 — $T = \frac{1}{2}\dot{\boldsymbol{\theta}}^T \mathbf{M}(\theta) \dot{\boldsymbol{\theta}}$  
State the inertia matrix $\mathbf{M}(\theta)$ with all four entries. For distributed rod ($I = ml^2/3$):

$$M_{11} = \left(\frac{m_1}{3} + m_2\right)l_1^2 + \frac{m_2 l_2^2}{3} + m_2 l_1 l_2 \cos\theta_2$$
$$M_{12} = M_{21} = m_2\left(\frac{l_2^2}{3} + \frac{l_1 l_2}{2}\cos\theta_2\right)$$
$$M_{22} = \frac{m_2 l_2^2}{3}$$

**Potential energy derivation:** Height of each center of mass → gravity vector $\mathbf{G}(\theta)$.

**The Coriolis matrix:** Define $\mathbf{C}(\theta, \dot\theta)$ via Christoffel symbols. Give explicit entries. Note: $\mathbf{C}$ depends on joint velocities — this is key to nonlinearity.

**Standard form:** $\mathbf{M}(\theta)\ddot{\boldsymbol{\theta}} + \mathbf{C}(\theta,\dot\theta)\dot{\boldsymbol{\theta}} + \mathbf{G}(\theta) = \boldsymbol{\tau}$

**Sidebar box:** "Why does M depend on $\theta_2$ but not $\theta_1$?" — intuitive explanation about rotational symmetry.

**TABLE 5.1:** System parameters for the full-derivation case ($l_1=l_2=0.5$ m, $m_1=m_2=1$ kg, $g=9.81$ m/s²).

**TABLE 5.2:** Numerical values of all matrix entries at the target pose $\theta^* = [\pi/4, \pi/4]$. Include det(M), $M^{-1}$, $\mathbf{G}(\theta^*)$.

#### 5.3 Linearization Around Equilibrium (3 pages)

**Why linearize?** MPC requires a linear model for the QP to be convex. We "zoom in" around a reference trajectory.

**Taylor expansion:** State-space form $\dot{x} = f(x, u)$ where $x = [\theta_1, \theta_2, \dot\theta_1, \dot\theta_2]^T$, $u = [\tau_1, \tau_2]^T$.

$$\dot{x} \approx f(\bar{x}, \bar{u}) + A_c(x - \bar{x}) + B_c(u - \bar{u})$$

**Computing $A_c$:** Full $4 \times 4$ Jacobian derivation. The block structure:
$$A_c = \begin{bmatrix} 0_{2\times2} & I_{2\times2} \\ -M^{-1}\frac{\partial G}{\partial\theta} & -M^{-1}C(\theta,\dot\theta) \end{bmatrix}$$

**At stationary points ($\dot\theta = 0$):** $C = 0$, so bottom-right block = 0. This simplifies the Jacobian enormously.

**Computing $A_{21} = -M^{-1}\frac{\partial G}{\partial\theta}$:** Full derivation of the gravity Jacobian. Step through all four partial derivatives.

**Case Studies (A, B, C):** Derived from handwritten notebook:
- **Case A:** $x_0 = [0°, 0°, 0, 0]$ — both links horizontal. $A_{21} = 0_{2\times2}$ (no gravity coupling at flat configuration). Physical meaning: double integrator — no self-stabilization.
- **Case B:** $x_0 = [30°, 0°, 0, 0]$ — link 1 tilted. $A_{21} = \begin{bmatrix}5&-5\\-5&15\end{bmatrix}$. Gravity acts as restoring force.
- **Case C:** $x_0 = [0°, 90°, 0, 0]$ — link 2 vertical. $A_{21} = \begin{bmatrix}0&0\\10&10\end{bmatrix}$. Physical meaning: $\theta_1$ changes have no effect, $\theta_2$ changes have large effect.

**TABLE 5.3:** Linearized matrices $A_c$, $B_c$, and equilibrium torques $u_0$ for all three cases. Must match handwritten notebook values exactly.

**Computing $B_c$:** $B_c = [0_{2\times2}; M^{-1}(\bar{x})]$. Derive for all cases.

**Computing equilibrium torque $u_0 = G(x_0)$:** For Case A: $u_0 = [30, 10]^T$ Nm. For Case B: $u_0 \approx [25.98, 8.66]^T$ Nm. For Case C: $u_0 = [20, 0]^T$ Nm.

#### 5.4 Discretization (1.5 pages)

**Zero-Order Hold (ZOH) method:** Exact discrete-time Jacobians:
$$A_d = e^{A_c \Delta t}, \quad B_d = \int_0^{\Delta t} e^{A_c s} ds \cdot B_c$$

**Euler approximation (for small $\Delta t$):**  
$$A_d \approx I + A_c \Delta t, \quad B_d \approx B_c \Delta t$$  
For $\Delta t = 0.02$ s, Euler error is $\mathcal{O}(\Delta t^2) \approx 4\times 10^{-4}$ — acceptable for real-time MPC.

**Affine offset:** For operating in absolute (not deviation) coordinates:  
$$d = (f(\bar{x},\bar{u}) - A_c \bar{x} - B_c \bar{u})\Delta t$$  
At equilibrium: $f = 0$, so $d = (-A_c \bar{x} - B_c \bar{u})\Delta t$.

**TABLE 5.4:** Discrete matrices $A_d$, $B_d$, $d$ for Case A (full numerical values). All verified against code and handwritten notebook.

**Verification check:** Confirm $A_d x_0 + B_d u_0 + d = x_0$ (equilibrium condition). Show the calculation explicitly.

#### 5.5 MPC as a Quadratic Program (3 pages)

**The MPC problem:** Over a horizon of $N$ steps, find control inputs $\{u_0, \ldots, u_{N-1}\}$ that drive the system toward a target state $x_{ref}$, minimizing cost $J$.

**Cost function:**
$$J = \sum_{k=0}^{N-1} \left[(x_k - x_{ref,k})^T Q_x (x_k - x_{ref,k}) + u_k^T R u_k\right] + (x_N - x_{ref,N})^T Q_f (x_N - x_{ref,N}) + \sum_{k=0}^{N} s_k^T Q_s s_k$$

Explain each term: tracking cost ($Q_x$), control effort ($R$), terminal cost ($Q_f$), soft constraint penalty ($Q_s$). Explain the weight hierarchy: $Q_s \gg Q_f > Q_x \gg R$.

**Hard constraints:** $-\tau_{max} \leq u_k \leq \tau_{max}$

**Soft constraints (angle limits):** $\theta_{min} \leq \theta_k - s_k$ (slack variable $s_k \geq 0$).

**Decision variable vector $z$:**  
For $N=1$: $z = [x_0, u_0, x_1, s_0, s_1]$ — 14 elements.  
General form: $n_z = N(n_x + n_u) + n_x = 8N + 4$ for our system.

**The QP form:**  
$$\min_z \frac{1}{2} z^T \mathbf{Q}_{qp} z + \mathbf{p}^T z$$  
$$\text{s.t. } A_{eq} z = b_{eq}, \quad l \leq A_{ineq} z \leq k_{ineq}$$

**FIGURE 5.2:** Block-diagonal structure of $\mathbf{Q}_{qp}$ — visually show how the blocks $2Q_x, 2R, 2Q_f, 2Q_s$ tile along the diagonal. This is a key visualization.

**Weight values for Case A:**  
$Q_x = \text{diag}(2000, 2000, 100, 100)$, $R = \text{diag}(0.001, 0.001)$, $Q_f = \text{diag}(5000, 5000, 200, 200)$, $Q_s = 10^6 \cdot I$.

**Equality constraint matrix $A_{eq}$:**  
Row Block 1: initial condition ($z[0:4] = x_0$)  
Row Block 2: dynamics at each timestep  
Show explicitly for $N=1$. **FIGURE 5.3:** Block structure of $A_{eq}$ as a visual matrix diagram.

**Inequality constraint matrix $A_{ineq}$:**  
Torque limits (hard), angle limits via slack (soft).  
Show for $N=1$. **FIGURE 5.4:** Block structure of $A_{ineq}$.

**TABLE 5.5:** All QP dimensions for $N=1, 2, 5, 10, 20$. Show $n_z$, number of equality constraints, number of inequality constraints, and matrix sizes. Demonstrates scaling.

#### 5.6 PIPG: From Optimization to Neural Dynamics (3 pages)

**What is PIPG?** The Proportional-Integral Projected Gradient method — a first-order algorithm for constrained QP that naturally maps to recurrent neural network dynamics.

**Key paper:** Yu, Elango & Açıkmeşe (2021) IEEE L-CSS.

**PIPG iteration (three lines):**
$$y_{t+1} = \theta_G(y_t + \beta_t(w_t + \beta_t(\mathbf{A}x_t - k)))$$
$$x_{t+1} = x_t - \alpha_t(\mathbf{Q}_{qp} x_t + \mathbf{p} + \mathbf{A}^T y_{t+1})$$
$$x_{t+1} = \text{proj}_{[\ell, u]}(x_{t+1})$$

where $\theta_G(\cdot) = \max(\cdot, 0)$ is the ReLU / projection onto non-negative cone.

**Neural interpretation:**  
- $x$ = "gradient neurons" (primal variables = decision variables)
- $y$ = "constraint neurons" (dual variables = Lagrange multipliers)
- Gradient neurons compute a gradient step, projected to the feasible box
- Constraint neurons compute how much the constraints are violated
- The "PI" (proportional-integral) structure = integrating constraint violations over time → robust convergence

**FIGURE 5.5:** The PIPG neural circuit diagram. Show $x$ neurons (blue) and $y$ neurons (red/orange) with arrows representing the computation graph. Should look like a neural network diagram. Each connection labeled with the corresponding matrix multiplication.

**Convergence guarantee:** $\mathcal{O}(1/t)$ convergence rate for convex objectives. Requires $\alpha_t \leq 1/\|\mathbf{Q}_{qp}\|$ and appropriate $\beta_t$ schedule.

**Annealing schedule:** Step sizes $\alpha_t, \beta_t$ decrease over time (piecewise constant in blocks of $T=50$–$100$ iterations).

#### 5.7 Mapping PIPG to Analog SNN (2 pages)

**The LIF neuron model:** Leaky Integrate-and-Fire — membrane potential integrates input current, fires when it crosses threshold, then resets.

$$\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I_{in}(t)$$

**The mapping (Mangalore et al. 2024 framework):**
- Gradient computation → current injection to gradient neurons
- Spike train → continuous variable via Δ-modulation (delta encoding)
- Matrix multiply $\mathbf{Q}_{qp}x$ → synaptic weight matrix
- Constraint neurons → different population with ReLU-like threshold

**Analog implementation (Bhowmik Group):** Spintronic synapses (domain wall or skyrmion devices) implement the weight matrix in analog. Inference is done in continuous time — no discrete clocking.

**FIGURE 5.6:** The full SNN architecture diagram for the MPC QP. Show gradient neuron population, constraint neuron population, weight matrices as synaptic connections, input/output encoding.

**Energy efficiency argument:** Event-driven computation → only active when neurons fire → sparse activity → low power. Quantify: typical spike rate in PIPG SNN → compute energy per operation → compare to CPU OSQP.

#### 5.8 Hand Calculation: 5 PIPG Iterations (3 pages)

**Philosophy:** "Numbers are not decoration. They are proof."

**Setup:** Case A configuration ($\theta^* = [45°, 45°]$), $N=1$ horizon, starting at $x_0 = [0, 0, 0, 0]^T$. $x_{ref} = [\pi/4, \pi/4, 0, 0]^T$.

**Iteration t=0→1:**
- Compute gradient $\nabla f = \mathbf{Q}_{qp} x^{(0)} + \mathbf{p}$
- Compute $\mathbf{p} = -2Q_x x_{ref}[0:4]$ for initial state slice → explicit numerical values
- Gradient step: $x^{(1)} = x^{(0)} - \alpha_0 \nabla f$
- Projection: clip to $[-25, 25]$
- Cost: $J(x^{(1)})$ — show it decreased

**Iterations t=1→2, 2→3, 3→4, 4→5:** Shorter presentation, focus on the dominant component $x_2$ (Δu₀₂) converging toward optimal.

**TABLE 5.6:** Convergence table — iteration, $x_2^{(t)}$, cost $J$, constraint violation. Show geometric convergence.

**FIGURE 5.7:** Convergence plot — cost $J$ vs. iteration number. Show the geometric decrease. Mark the 8% optimal threshold and the iteration where it's crossed (~55–80).

**Analytical verification:** For unconstrained QP, $x^* = -\mathbf{Q}^{-1}\mathbf{p}$. Compute dominant component: $x_2^* \approx -p_2/Q_{22} \approx -0.0249$. Show that the iteration converges to this value.

**Physical meaning:** $\Delta u_{02}^* \approx -0.025$ Nm on top of gravity compensation $\tau_2^* = 0$ Nm. "A tiny nudge to joint 2, barely more than a whisper, beginning the journey to 45°."

#### 5.9 MPC Closed-Loop Behavior (1 page)

**Describe the full simulation** (implemented in Python, see §10):
- Initial transient: 0–0.5 s — large torques, rapid motion
- Convergence: 0.5–1.5 s — oscillations damp out
- Steady state: t > 1.5 s — both joints at 45°, error < 0.1°

**TABLE 5.7:** Closed-loop performance summary — steady-state error, settling time, max torque, energy consumption.

**FIGURE 5.8:** Closed-loop simulation plots — 4-panel figure:
1. $\theta_1(t)$ and $\theta_2(t)$ vs. time (with reference lines at 45°)
2. $\tau_1(t)$ and $\tau_2(t)$ vs. time
3. Tracking error $\|\theta(t) - \theta^*\|$ on log scale
4. Per-step solve time (PIPG iterations to convergence)

#### 5.10 Limitations & Extensions (1 page)

Honest discussion:
- Linearization validity: $\|\Delta\theta\| < ~20°$ — beyond that, need nonlinear MPC or gain scheduling
- SNN hardware noise: spintronic devices have stochastic switching → solution quality degrades with noise level
- Warm-starting: PIPG benefits from good initialization; in MPC receding horizon, previous solution is a natural warm start
- Real hardware latency: spike communication takes time → real $\Delta t$ must account for SNN solve time

---

### CHAPTER 6 — RESULTS, ANALYSIS & DISCUSSION

**Page target:** 10–12 pages  
**Tone:** Results-driven, data-forward, honest about limitations.  
**Purpose:** What did we find? What does it mean?

#### 6.1 OIM-CMRTA Results (4 pages)

**Simulation setup:**
- Python ODE solver (RK45) simulating Wang-Roychowdhury OIM dynamics
- 4 problem sizes: Tiny (5 robots, 3 tasks), Small (10/5), Medium (20/10), Large (50/20, decomposed)
- Comparison baselines: CPLEX MILP (exact, small only), greedy auction, random restart

**Key results:**

**FIGURE 6.1:** Approximation ratio $\rho$ vs. problem size for all methods. Box-and-whisker plot over 100 random instances per size. Show OIM, greedy, multi-start OIM. Include CPLEX for small sizes.

**FIGURE 6.2:** Time-to-solution vs. $|V|$ (number of graph nodes). Log-log plot. Show cross-over point where OIM becomes competitive with exact solver.

**FIGURE 6.3:** Constraint violation rate vs. problem density ($|E|/|V|^2$). Show how repair frequency increases with dense graphs.

**FIGURE 6.4:** Phase trajectory plots for the 6-node worked example. Animated/static, showing convergence to $\{v_1, v_4\}$ solution.

**TABLE 6.1:** Summary table of all results — per problem size, per method: mean $\rho$, std $\rho$, mean time, constraint violation rate.

**FIGURE 6.5:** The MWIS solution quality as a function of penalty coefficient $\lambda$. Show optimal window (too small → infeasible, too large → poor solution). This directly validates Theorem 4.1.

#### 6.2 SNN-MPC Results (4 pages)

**Simulation setup:**
- Python MPC loop with PIPG solver
- 3 operating points (Cases A, B, C)
- Comparison: OSQP (standard QP solver), PIPG on CPU, PIPG on simulated SNN

**Key results:**

**FIGURE 6.6:** Phase-space trajectory of robot arm — $(\theta_1, \theta_2)$ path from initial to target. Show Case A, B, C. Overlay the constraint boundaries.

**FIGURE 6.7:** PIPG convergence curves for Cases A, B, C. Iterate count vs. cost J. Show how the gravity coupling (Case B, C) affects convergence rate.

**FIGURE 6.8:** Energy-delay product comparison bar chart — OSQP CPU, PIPG CPU, PIPG SNN (simulated). Based on Mangalore et al. (2024) scaling and our system parameters.

**FIGURE 6.9:** Torque profiles $\tau_1(t)$, $\tau_2(t)$ for all cases. Note different gravity compensation requirements.

**TABLE 6.2:** Linearization accuracy — compare linear prediction vs. nonlinear simulation for different deviation magnitudes. Shows where linearization breaks down.

**TABLE 6.3:** MPC solver comparison — OSQP vs. PIPG — iterations/time/energy for our problem size.

#### 6.3 Cross-Case Discussion (2 pages)

**What these two use cases have in common:**
- Both reduce a physical problem to an optimization problem
- Both exploit hardware that "falls" to the answer
- Both have post-processing / repair for constraint handling
- Both face approximation quality vs. speed trade-offs

**The complementary hardware story:** OIM for binary combinatorial, SNN for continuous constrained QP — together they cover the two dominant optimization problem classes in robotics. This is a vision for a complete neuromorphic robotics co-processor.

**FIGURE 6.10:** The "capability map" — a 2D space of problem types (binary vs. continuous, constrained vs. unconstrained) with different hardware solutions placed appropriately. OIM and SNN occupy complementary regions.

---

### CHAPTER 7 — INDIA'S OPPORTUNITY: NEUROMORPHIC MANUFACTURING ECOSYSTEM

**Page target:** 5–7 pages  
**Tone:** Visionary but grounded. Economic and technical argument.  
**Purpose:** The "so what for the world" chapter.

**WRITER AGENT NOTE:** This chapter must be carefully written. It should NOT read like a government report or corporate strategy document. It should read like a passionate argument from someone who has thought deeply about this. Use analogies, historical parallels, and economic data. Do NOT make unsubstantiated claims.

#### 7.1 The Historical Parallel: India's Mobile Revolution

India built a mobile revolution without manufacturing the transistors. By creating the *demand-side conditions* (cheap SIM cards, affordable handsets, government digital infrastructure), India created conditions where global chip manufacturers competed to serve the Indian market. The cost of connectivity in India fell to among the lowest in the world.

The argument: **neuromorphic hardware is at the same inflection point that mobile was in 2000.** The technology works. The manufacturing infrastructure doesn't yet exist at scale. The first countries to build that infrastructure will define the economics of physical intelligence for the next 50 years.

#### 7.2 Why Neuromorphic Manufacturing is Different

Classical semiconductor manufacturing (Intel, TSMC, Samsung) requires:
- Ultra-precision lithography ($< 5$ nm)
- Massive capital investment ($10+ billion per fab)
- Decades of process development
- Fundamental physics limits approaching

Neuromorphic/post-silicon manufacturing potentially requires:
- Novel materials (FeFET, memristors, spintronic devices)
- Less extreme precision (device-to-device variation is exploitable, not fatal)
- Analog processes (more tolerant of fab variation)
- Different expertise profile: materials science + physics + systems integration

**This is an entry point.** The race hasn't been run yet.

#### 7.3 India's Existing Assets

- IIT Bombay (Bhowmik Group): analog spintronic SNN — existence proof that Indian academic research can lead here
- IIT Delhi, IIT Madras: strong semiconductor device physics programs
- DRDO, ISRO, BARC: government R&D capacity for novel devices
- Semicon India Program: ₹76,000 crore commitment signals national intent
- Young engineering workforce: 1.5M engineering graduates/year
- Cost structure: analog device development costs 5–10× less than digital VLSI

**FIGURE 7.1:** India's neuromorphic manufacturing ecosystem map — show existing research groups, proposed fab locations, application markets (industrial robots, defense, smart cities, healthcare devices).

#### 7.4 The Application Stack: Killer Apps

Three domains where neuromorphic hardware makes India competitive:

**Industrial automation:** India is late to industrial robotics. But neuromorphic edge processors → cheap robot brains → leapfrog to next generation, not catch up to the last one.

**Edge AI for Bharat:** Rural India, IoT agriculture, village-level health monitoring — all need ultra-low-power inference. Neuromorphic beats conventional AI chips on energy per inference.

**Smart manufacturing of smart chips:** India can manufacture neuromorphic chips for use in India's manufacturing sector. Positive feedback loop.

#### 7.5 What Needs to Happen

Honest list of what's missing and what needs to be built:
- EDA tools for analog neuromorphic design (mostly missing)
- Standard programming frameworks (immature)
- Fab processes for FeFET and spintronic devices at scale (early stage)
- Trained human capital in neuromorphic engineering (small but growing)
- Industry-academia collaboration infrastructure (nascent)

**TABLE 7.1:** Technology readiness level (TRL) assessment for key neuromorphic technologies in India.

---

### CHAPTER 8 — CONCLUSION & FUTURE DIRECTIONS

**Page target:** 4–5 pages  
**Tone:** Reflective, forward-looking, personal.  
**Purpose:** Land the story. What did we learn? Where should we go?

#### 8.1 What We Did (1 page)

Clean summary of contributions — not a repeat of the abstract, but a reflective look back. "We started with a warehouse and ended with physics. We started with equations and ended with oscillators and neurons. The journey matters as much as the destination."

#### 8.2 What We Learned (1 page)

Honest synthesis — including surprises and limitations:
- OIM works well on sparse, geometric conflict graphs (natural in spatial robot problems) — better than expected
- OIM struggles on dense, frustrating graphs — expected but quantified
- PIPG convergence is fast (55–80 iters) but sensitive to weight tuning
- The linearization is the weakest link — real improvement may come from online re-linearization along the trajectory

#### 8.3 Future Work (2 pages)

**Short-term (1–2 years):**
- Physical OIM chip deployment: test the full pipeline on actual CMOS OIM hardware
- Warm-started OIM: exploit previous solution for faster convergence in replanning
- Nonlinear MPC via successive linearization + SNN
- Dynamic MRTA: handle task arrivals and robot failures online

**Medium-term (3–5 years):**
- Multi-chip integration: OIM for allocation + SNN for control on same embedded platform
- Learning-enhanced OIM: learn good initial phases from past instances
- FeFET OIM fabrication at IIT Bombay / TIFR

**Long-term (5–10 years):**
- Fully embedded neuromorphic robot brain: all sensing, planning, control on one neuromorphic chip
- Digital consciousness studies: reservoir computing, predictive coding — the consciousness studies path referenced in notes

#### 8.4 A Personal Note (0.5 page)

Return to the Preface's voice. What does this mean to the author? What is the vision beyond the thesis?

"I believe physical intelligence is the next great project of human civilization. Not artificial general intelligence in a data center — but a billion small machines, each with a sliver of real-world intelligence, working together to build, heal, grow, and solve. This thesis is one small brick in that wall. I hope it helps someone else lay the next one."

---

## 5. MASTER FIGURE & VISUALIZATION LIST

**FIGURE AGENT NOTE:** All figures must be:
- Generated in Python (matplotlib / seaborn / plotly) or as SVG diagrams
- At minimum 300 DPI for raster, scalable for vector
- Consistent color palette (see §9.4)
- Each must have a detailed caption (150–200 words) that can stand alone
- All data behind quantitative figures must be in /experiments/ directory

| Fig # | Chapter | Title | Type | Data Source | Priority |
|---|---|---|---|---|---|
| 1.1 | 1 | Hardware-Algorithm Co-evolution Timeline | Timeline illustration | Curated from literature | HIGH |
| 1.2 | 1 | CPU vs OIM vs SNN Architecture Comparison | Schematic diagram | Hand-designed | HIGH |
| 1.3 | 1 | Energy-Delay Product Comparison | Bar chart | Mangalore 2024 + literature | HIGH |
| 1.4 | 1 | "The Pipeline" — Full System Flow | Flow diagram | Hand-designed | HIGH |
| 2.1 | 2 | Ising Hardware Platform Landscape | Scatter/bubble chart | Literature survey | MEDIUM |
| 3.1 | 3 | The Bits-to-Atoms Four-Layer Stack | Architecture diagram | Hand-designed | HIGH |
| 3.2 | 3 | Trade-off Space: Problem Type vs. Solver | Annotated scatter | Estimated from literature | MEDIUM |
| 4.1 | 4 | Warehouse Scenario Schematic | Illustrative diagram | Hand-designed | HIGH |
| 4.2 | 4 | Conflict Graph — 7-node worked example | Graph visualization | Computed from example | CRITICAL |
| 4.3 | 4 | OIM Phase Trajectories — worked example | Time-series plot | OIM simulation | CRITICAL |
| 4.4 | 4 | Anti-ferromagnetic coupling intuition | Conceptual diagram | Hand-designed | MEDIUM |
| 4.5 | 4 | Scalability plot — |V| vs N with pruning | Line chart | Computed | HIGH |
| 4.6 | 4 | Hybrid pipeline block diagram | Flow diagram | Hand-designed | HIGH |
| 5.1 | 5 | 2-DOF Robot Arm Schematic | Technical diagram | Hand-designed | CRITICAL |
| 5.2 | 5 | Q_qp Block Diagonal Structure | Matrix visualization | Computed | HIGH |
| 5.3 | 5 | A_eq Matrix Block Structure | Matrix visualization | Computed | HIGH |
| 5.4 | 5 | A_ineq Matrix Block Structure | Matrix visualization | Computed | HIGH |
| 5.5 | 5 | PIPG Neural Circuit Diagram | Neural network diagram | Hand-designed | CRITICAL |
| 5.6 | 5 | Full SNN Architecture for MPC | Architecture diagram | Based on Mangalore 2024 | HIGH |
| 5.7 | 5 | PIPG Convergence Plot (5 iters + full) | Line chart | Computed | CRITICAL |
| 5.8 | 5 | Closed-Loop Simulation — 4 panels | Multi-panel plot | Python simulation | CRITICAL |
| 6.1 | 6 | Approximation Ratio vs Problem Size | Box-whisker plot | OIM simulation | CRITICAL |
| 6.2 | 6 | Time-to-Solution vs |V| — all methods | Log-log plot | Timing experiments | CRITICAL |
| 6.3 | 6 | Constraint Violation vs Graph Density | Line chart | OIM simulation | HIGH |
| 6.4 | 6 | Phase Trajectories — Worked Example | Time-series | OIM simulation | HIGH |
| 6.5 | 6 | MWIS Quality vs Lambda | Line chart | Penalty sweep experiment | CRITICAL |
| 6.6 | 6 | Phase-Space Arm Trajectory | 2D trajectory plot | MPC simulation | HIGH |
| 6.7 | 6 | PIPG Convergence Curves — 3 Cases | Multi-line chart | MPC simulation | HIGH |
| 6.8 | 6 | Energy-Delay Product Bar Chart | Bar chart | Based on Mangalore 2024 | HIGH |
| 6.9 | 6 | Torque Profiles — 3 Cases | Multi-panel plot | MPC simulation | HIGH |
| 6.10 | 6 | Capability Map — Problem Types vs Hardware | Annotated 2D diagram | Conceptual | MEDIUM |
| 7.1 | 7 | India Neuromorphic Ecosystem Map | Geographic/conceptual | Research + policy docs | MEDIUM |

---

## 6. MASTER TABLE LIST

| Table # | Chapter | Title | Key Columns | Priority |
|---|---|---|---|---|
| 2.1 | 2 | IM Hardware Platform Comparison | Platform, substrate, scale, deployment, power, quality | HIGH |
| 4.1 | 4 | MRTA Example Setup | Robots/capabilities, Tasks/requirements | HIGH |
| 4.2 | 4 | Feasibility Check Table | Coalition, Task, Σc₁, Σc₂, q₁, q₂, Feasible? | CRITICAL |
| 4.3 | 4 | Utility Calculation Table | Coalition, Task, Combined cap, Excess, φ, Σcost, U(S,j) | CRITICAL |
| 4.4 | 4 | QUBO Matrix Q (7×7) | Full matrix, annotated | CRITICAL |
| 4.5 | 4 | QUBO Evaluation — All solutions | x vector, Q(x) value, feasible? | HIGH |
| 4.6 | 4 | Ising Parameters | Node, w, deg, h; Edge pair, J_ij | CRITICAL |
| 4.7 | 4 | Scalability Numbers | (N,M,k): |V| raw, after CB, after SP, OIM feasible? | HIGH |
| 4.8 | 4 | Pipeline Timing | Stage, operation count, typical duration | MEDIUM |
| 5.1 | 5 | System Parameters | Symbol, value, units, description | HIGH |
| 5.2 | 5 | Matrices at θ* | M(θ*), det(M), M⁻¹, G(θ*), ∂G/∂θ | CRITICAL |
| 5.3 | 5 | Linear Matrices — All 3 Cases | Ac, Bc, u₀ per case | CRITICAL |
| 5.4 | 5 | Discrete Matrices — Case A | Ad, Bd, d — full numerical values | CRITICAL |
| 5.5 | 5 | QP Dimensions vs N | N, n_z, eq constraints, ineq constraints | HIGH |
| 5.6 | 5 | PIPG Convergence — 5 Iterations | t, x₂⁽ᵗ⁾, J(x⁽ᵗ⁾), violation | CRITICAL |
| 5.7 | 5 | MPC Closed-Loop Performance | Case, steady-state error, settling time, max torque | HIGH |
| 6.1 | 6 | MRTA Results Summary | Problem size, method, ρ mean/std, time, violation rate | CRITICAL |
| 6.2 | 6 | Linearization Accuracy | Δθ magnitude, linear prediction error, nonlinear | HIGH |
| 6.3 | 6 | MPC Solver Comparison | Solver, iters, time, energy estimate | HIGH |
| 7.1 | 7 | TRL Assessment — India Neuromorphic | Technology, current TRL, target TRL, required actions | MEDIUM |

---

## 7. VALIDATION & VERIFICATION SPECIFICATION

**VALIDATOR AGENT:** This section specifies every mathematical claim that must be verified by at least two independent methods: (1) by-hand calculation, and (2) Python code. Claims marked CRITICAL must be verified before any writing begins.

### 7.1 CMRTA Validation Targets

**V-OIM-1 (CRITICAL): MWIS Equivalence**  
*Claim:* The coalition MRTA optimization problem is equivalent to MWIS on the conflict graph $G$.  
*Method 1 (Hand):* Show that a valid allocation corresponds to an independent set, and vice versa, for the 3-robot 2-task example.  
*Method 2 (Code):* Enumerate all valid allocations via brute force for small examples; verify they correspond to independent sets in the Python-generated conflict graph.  
*Expected result:* Perfect agreement.

**V-OIM-2 (CRITICAL): Penalty Bound Theorem**  
*Claim:* If $\lambda > \max_{(i,j)\in E}(w_i + w_j)$, then every QUBO minimizer is a feasible MWIS solution.  
*Method 1 (Hand):* Proof by contradiction — assume an infeasible QUBO minimum and show $\lambda$ too large to allow it.  
*Method 2 (Code):* Sweep $\lambda$ from $0.1 \cdot \max(w_i+w_j)$ to $10 \cdot \max(w_i+w_j)$. Plot QUBO solution feasibility rate vs. $\lambda$. Verify the theorem threshold.  
*Expected result:* 100% feasibility rate for $\lambda > \max(w_i + w_j)$.  
*This directly generates Figure 6.5.*

**V-OIM-3 (CRITICAL): QUBO Matrix Values**  
*Claim:* The 7×7 QUBO matrix in Table 4.4 is correct.  
*Method 1 (Hand):* Calculate every entry of $Q$ from definition: $Q_{ii} = -w_i$, $Q_{ij} = \lambda/2$ for conflict edges.  
*Method 2 (Code):* Auto-generate QUBO matrix from conflict graph and weights. Compare entry by entry.  
*Expected result:* Exact match (to floating-point precision).

**V-OIM-4 (CRITICAL): Optimal MWIS Solution**  
*Claim:* The MWIS of the worked example is $\{v_0, v_2\}$ (nodes corresponding to {r₃}→T₁ and {r₁}→T₂) with total utility = handwritten value.  
*Method 1 (Hand):* Notebook pages 29–31 — enumerate all independent sets, identify maximum weight one.  
*Method 2 (Code):* Brute-force MWIS solver on the 7-node graph.  
*Expected result:* Agreement with handwritten notebook values.  
**CONSISTENCY NOTE:** There is a discrepancy risk here. The handwritten notes show a slightly different example (different utility values) than the proposal document. VALIDATOR AGENT must reconcile and use ONE consistent set of numbers throughout.

**V-OIM-5: Ising Parameter Values**  
*Claim:* Table 4.6 values for $h_k$ and $J_{ij}$ are correct.  
*Method 1 (Hand):* Calculate from formula using QUBO Q values and graph degrees.  
*Method 2 (Code):* Python computation. Compare.

**V-OIM-6: OIM → MWIS Convergence on Worked Example**  
*Claim:* OIM simulation converges to (at least) the MWIS solution for the 7-node worked example in >90% of random initializations.  
*Method 1 (Simulation):* Run 100 OIM simulations with random initial phases. Count convergence to optimal.  
*Expected result:* >90% success rate (note: OIM is approximate; lower rate is also an acceptable finding if honestly reported).

### 7.2 SNN-MPC Validation Targets

**V-SNN-1 (CRITICAL): Inertia Matrix at θ***  
*Claim:* $M(\theta^*)$ for Case A ($\theta^* = [0,0]$) equals $\begin{bmatrix}0.6667 & 0.2083 \\ 0.2083 & 0.0833\end{bmatrix}$ (from SNN_MPC file).  
*Method 1 (Hand):* Calculate from formula with $l_1=l_2=0.5$m, $m_1=m_2=1$kg, distributed rod.  
*Method 2 (Code):* Python calculation.  
*Expected result:* Match to 4 decimal places.  

**CONSISTENCY NOTE:** Handwritten notebook pages 40–45 use point-mass model (I=0) with $l_1=l_2=1$m. The SNN_MPC_Complete_Derivation.md uses distributed-rod model with $l_1=l_2=0.5$m. The thesis uses the **distributed-rod, 0.5m** version throughout. Do NOT mix these.

**V-SNN-2 (CRITICAL): Equilibrium Torques**  
*Claim:* For Case A: $u_0 = G(x_0) = [14.142, 0]^T$ Nm.  
*Method 1 (Hand):* $G_1 = (m_1 l_1/2 + m_2 l_1)g\sin\theta_1 + m_2 l_2 g/2 \sin(\theta_1+\theta_2)$ with $\theta = [\pi/4, \pi/4]$. Calculate.  
*Method 2 (Code):* Python.  
*Expected result:* $G_1 = 10\sqrt{2}/1 \approx 14.142$, $G_2 = 0$.

**V-SNN-3 (CRITICAL): Discrete Matrices for Case A**  
*Claim:* $A_d$, $B_d$, $d$ in Table 5.4 are correct.  
*Method 1 (Hand):* $A_d = I + A_c \cdot 0.02$, $B_d = B_c \cdot 0.02$, $d = -B_c u_0 \cdot 0.02$ (at rest, $x_0 = 0$).  
*Method 2 (Code):* scipy.linalg.expm for ZOH comparison.  
*Expected result:* Euler and ZOH agree to 3 significant figures for $\Delta t = 0.02$ s.

**V-SNN-4 (CRITICAL): PIPG Iteration Values**  
*Claim:* Table 5.6 values (cost J at each iteration) are correct.  
*Method 1 (Hand):* Compute by hand for iterations 0–2 (full detail), 3–5 (abbreviated).  
*Method 2 (Code):* Run PIPG in Python.  
*Expected result:* Geometric convergence, agreement to 3 significant figures.

**V-SNN-5: Equilibrium Verification**  
*Claim:* $A_d x_0 + B_d u_0 + d = x_0$ for Case A.  
*Method 1 (Hand):* Substitute values. Verify equality.  
*Method 2 (Code):* Python assertion.  
*Expected result:* Exact (within floating-point tolerance).

**V-SNN-6: Gravity Jacobian Cases B and C**  
*Claim:* $\frac{\partial G}{\partial \theta}$ for Cases B and C match notebook values (pages 49–52).  
*Method 1 (Hand):* Calculate from formula.  
*Method 2 (Code):* Symbolic differentiation via sympy.  
*Expected result:* Case B: $\begin{bmatrix}-15&-5\\-5&-5\end{bmatrix}$; Case C: $\begin{bmatrix}-10&-10\\-10&-10\end{bmatrix}$.

### 7.3 Consistency Cross-Checks

**CC-1:** All utility values in MRTA example must be internally consistent (hand-computed from the capability/requirement/position data in Tables 4.1–4.3, not copied from one document without re-verification).

**CC-2:** The $\lambda$ value used throughout the CMRTA chapter must satisfy Theorem 4.1 for the worked example. Verify: $\lambda = 8$ (from notebook page 35) satisfies $\lambda > \max_{(i,j)\in E}(w_i + w_j)$ for the worked example.

**CC-3:** The PIPG iteration results in Table 5.6 must be achievable starting from $x^{(0)} = \mathbf{0}$ and using the $\mathbf{Q}_{qp}$ constructed from Case A weight matrices. Verify the gradient calculation at $x^{(0)}$ explicitly.

---

## 8. LITERATURE REVIEW PIPELINE SPECIFICATION

**LITERATURE AGENT:** This section specifies the Python-based pipeline for the automated literature review. The pipeline output feeds into Chapter 2 but also creates the bibliography for the entire thesis.

### 8.1 Pipeline Architecture

```
Stage 1: Seed Query Generation
   Input: Topic keywords from this blueprint
   Output: 50–80 seed queries for arXiv, IEEE, ACM

Stage 2: Paper Retrieval
   APIs: arxiv.org REST API, Semantic Scholar API, IEEE Xplore API
   Target: 200–300 relevant papers

Stage 3: Relevance Filtering
   Method: Title + abstract embedding similarity (sentence-transformers)
   Target: 80–100 high-relevance papers

Stage 4: Full Text Extraction
   For each paper: download PDF, extract text via pdfminer
   Fallback: abstract + metadata only

Stage 5: Structured Summary Generation
   For each paper: Claude API call with structured output
   Output fields: {title, authors, year, venue, problem, method, result, gap, quote}

Stage 6: Citation Network Analysis
   Build citation graph
   Identify "bridge" papers (connecting OIM to robotics, etc.)
   Find most-cited papers in each sub-area

Stage 7: Synthesis & Table Generation
   Auto-generate Table 2.1 (IM Platform Comparison)
   Auto-generate literature timeline
   Group papers by sub-area
```

### 8.2 Seed Keywords

```python
PRIMARY_TOPICS = [
    "Oscillator Ising Machine robotics",
    "QUBO multi-robot task allocation",
    "neuromorphic model predictive control",
    "spiking neural network optimization",
    "PIPG projected gradient robotics",
    "coalition formation multi-robot",
    "maximum weight independent set hardware",
    "FeFET oscillator Ising",
    "analog computing optimization",
    "Loihi robot control",
]

BACKGROUND_TOPICS = [
    "Ising formulations NP problems Lucas",
    "Wang Roychowdhury oscillator Ising machine",
    "Mangalore neuromorphic quadratic programming",
    "MRTA survey Gerkey Mataric",
    "model predictive control robot arm",
    "Rawlings Mayne Diehl MPC",
    "Kuramoto coupled oscillator synchronization",
    "Bhowmik spintronic neural network IIT Bombay",
    "legged robot MPC ANYmal",
    "OSQP quadratic programming solver",
]

INDIA_TOPICS = [
    "India neuromorphic computing research",
    "Semicon India semiconductor manufacturing",
    "IIT spintronic device neuromorphic",
    "post-silicon computing India",
]
```

### 8.3 Key Papers to Confirm (All Must Be Verified)

The following papers are cited in existing documents and MUST be confirmed via actual DOI/arXiv lookup:

| Paper | Expected DOI/arXiv | Status |
|---|---|---|
| Lucas (2014) Ising formulations | Frontiers in Physics, 2014 | Must verify |
| Wang & Roychowdhury (2019) OIM UCNC | Springer LNCS | Must verify |
| Wang & Roychowdhury (2021) Natural Computing | Nature Computing doi | Must verify |
| Mangalore et al. (2024) Loihi MPC | arXiv:2401.14885 | Confirmed |
| Yu et al. (2021) PIPG | arXiv:2009.06980 | Confirmed |
| Gerkey & Matarić (2004) MRTA taxonomy | Int J Robotics Research | Must verify |
| Sandholm et al. (1999) coalition complexity | Artificial Intelligence | Must verify |
| Delacour et al. (2025) LagONN | arXiv 2025 | Must find |
| Honjo et al. (2021) 100K CIM | Science Advances | Must verify |
| McMahon et al. (2016) CIM | Science | Must verify |
| Rawlings, Mayne & Diehl (2020) MPC book | Nob Hill Publishing | Must verify |
| Siciliano et al. (2009) Robotics textbook | Springer | Must verify |
| Lynch & Park Modern Robotics | Cambridge UP | Must verify |

---

## 9. LATEX & FORMATTING SPECIFICATION

**LATEX AGENT:** Produce the thesis in LaTeX. This section specifies every formatting decision.

### 9.1 Document Class & Packages

```latex
\documentclass[12pt, twoside, a4paper]{report}

% Core
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Math
\usepackage{amsmath, amssymb, amsthm}
\usepackage{mathtools}
\usepackage{bm}  % bold math

% Fonts (choose one premium option)
% Option A: Standard academic
\usepackage{lmodern}
% Option B: More distinctive
\usepackage{newpxtext, newpxmath}  % Palatino-style

% Layout
\usepackage[margin=2.5cm, inner=3cm]{geometry}
\usepackage{setspace}
\onehalfspacing  % or \doublespacing for certain institutions

% Figures
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{float}
\usepackage{tikz, pgfplots}  % for programmatic figures

% Tables
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{longtable}  % for multi-page tables
\usepackage{multirow}
\usepackage[table]{xcolor}

% Code
\usepackage{listings}
\usepackage{algorithm, algorithmicx, algpseudocode}

% References
\usepackage[backend=biber, style=ieee, sorting=none]{biblatex}
\addbibresource{references.bib}

% Cross-references
\usepackage[hidelinks]{hyperref}
\usepackage{cleveref}

% Aesthetics
\usepackage{epigraph}  % for chapter-opening quotes
\usepackage{fancyhdr}  % custom headers/footers
\usepackage{titlesec}  % chapter title formatting
\usepackage{mdframed}  % boxed environments for theorems, examples
```

### 9.2 Custom Environments

```latex
% Theorem environments (numbered)
\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{definition}[theorem]{Definition}

% Non-numbered
\newtheorem*{remark}{Remark}

% Special box for key equations
\newmdenv[
  linecolor=darkblue,
  backgroundcolor=lightblue!10,
  frametitle={Key Result},
  roundcorner=5pt
]{keyresult}

% Conversation box (author's voice)
\newmdenv[
  linecolor=gray,
  backgroundcolor=gray!5,
  frametitle={A Note},
  roundcorner=5pt,
  fontcolor=black!80
]{authornote}

% Example environments (colored left bar)
\newmdenv[
  leftline=true, rightline=false, topline=false, bottomline=false,
  linecolor=orange, linewidth=3pt,
  backgroundcolor=orange!5
]{example}
```

### 9.3 Notation Table (FIXED — All Agents Must Follow)

| Symbol | Meaning | First Use |
|---|---|---|
| $\mathcal{R}$ | Set of robots | Ch 4 |
| $\mathcal{T}$ | Set of tasks | Ch 4 |
| $N$ | Number of robots | Ch 4 |
| $M$ | Number of tasks | Ch 4 |
| $K$ | Number of capability types | Ch 4 |
| $\mathbf{c}_i$ | Capability vector of robot $i$ | Ch 4 |
| $\mathbf{q}_j$ | Requirement vector of task $j$ | Ch 4 |
| $S$ | Coalition (subset of $\mathcal{R}$) | Ch 4 |
| $U(S,j)$ | Utility of coalition $S$ for task $j$ | Ch 4 |
| $\phi(S,j)$ | Efficiency factor | Ch 4 |
| $\mathcal{A}$ | Coalition allocation | Ch 4 |
| $G = (V,E)$ | Conflict graph | Ch 4 |
| $w_v$ | Node weight (= utility) | Ch 4 |
| $\mathcal{Q}(\mathbf{x})$ | QUBO objective | Ch 4 |
| $Q$ | QUBO matrix | Ch 4 |
| $\lambda$ | QUBO penalty coefficient | Ch 4 |
| $H_{\text{Ising}}(\mathbf{s})$ | Ising Hamiltonian | Ch 4 |
| $h_i$ | External bias (Ising) | Ch 4 |
| $J_{ij}$ | Coupling strength (Ising) | Ch 4 |
| $K_{ij}$ | OIM coupling parameter | Ch 4 |
| $\theta_i$ | Oscillator phase | Ch 4 |
| $s_i \in \{-1,+1\}$ | Ising spin | Ch 4 |
| $x_i \in \{0,1\}$ | QUBO binary variable | Ch 4 |
| $\boldsymbol{\theta}$ | Joint angle vector | Ch 5 |
| $\mathbf{M}(\theta)$ | Inertia matrix | Ch 5 |
| $\mathbf{C}(\theta,\dot\theta)$ | Coriolis matrix | Ch 5 |
| $\mathbf{G}(\theta)$ | Gravity vector | Ch 5 |
| $\boldsymbol{\tau}$ | Joint torque vector | Ch 5 |
| $A_c, B_c$ | Continuous Jacobians | Ch 5 |
| $A_d, B_d, d$ | Discrete matrices | Ch 5 |
| $\mathbf{Q}_{qp}$ | QP cost Hessian | Ch 5 |
| $\mathbf{p}$ | QP cost gradient | Ch 5 |
| $z$ | QP decision variable | Ch 5 |
| $N_h$ | MPC horizon | Ch 5 |
| $\Delta t$ | Discretization timestep | Ch 5 |

### 9.4 Color Palette

```
PRIMARY BLUE: #1B4F72 (equations, key results, headers)
SECONDARY ORANGE: #D35400 (examples, author notes)
ACCENT GREEN: #1E8449 (positive results, confirmations)
ACCENT RED: #C0392B (warnings, limitations, conflict edges)
NEUTRAL GRAY: #566573 (secondary text, captions)
BACKGROUND LIGHT: #FDFEFE (page background)
GRAPH PALETTE: Seaborn "colorblind" palette — accessible to all readers
```

### 9.5 Chapter Opening Format

Each chapter opens with:
1. A large chapter number (typographically styled)
2. The chapter title
3. An **epigraph** — a quote from a relevant scientist, philosopher, or engineer (2–3 lines)
4. A **chapter abstract** (5–8 sentences): what this chapter does and why
5. A **"chapter pipeline" diagram** (small, inline): showing where this chapter fits in the overall thesis flow

**EPIGRAPH CANDIDATES (Writer Agent should select the best fit):**

*Chapter 1:* "The question of whether a computer can think is no more interesting than the question of whether a submarine can swim." — Edsger Dijkstra

*Chapter 2:* "In God we trust; all others must bring data." — W. Edwards Deming

*Chapter 4:* "Optimization is the process of finding the best from a set of alternatives." — Richard Bellman (paraphrased)

*Chapter 5:* "To understand recursion, one must first understand recursion." *(comedic, for the Lagrangian recursion*) OR "A theory is something nobody believes, except the person who made it. An experiment is something everybody believes, except the person who made it." — Albert Einstein

*Chapter 7:* "India is not, as people keep calling it, an underdeveloped country, but rather, in the context of its history and development, a highly developed one in an advanced state of decay." — Shashi Tharoor (provocative, for the "opportunity" framing) OR use a more constructive Narayan Murthy / APJ Abdul Kalam quote.

*Chapter 8:* "We choose to go to the Moon not because it is easy, but because it is hard." — JFK (for the aspirational close)

---

## 10. IMPLEMENTATION & TESTING SPECIFICATION

**IMPLEMENTATION AGENT:** Build all code in Python. All code goes to `/experiments/`. Every numerical claim in the thesis must be reproducible from this code. README must describe how to reproduce every figure and table.

### 10.1 Repository Structure

```
/thesis_experiments/
├── README.md              ← How to reproduce every figure/table
├── requirements.txt       ← numpy, scipy, matplotlib, networkx, cvxpy, osqp
├── /mrta/
│   ├── coalition_enum.py  ← Enumerate coalitions, feasibility check
│   ├── conflict_graph.py  ← Build conflict graph G=(V,E)
│   ├── qubo_formulate.py  ← Assemble QUBO matrix
│   ├── ising_map.py       ← QUBO → Ising parameters
│   ├── oim_simulate.py    ← ODE solver for OIM dynamics
│   ├── greedy_repair.py   ← Post-processing repair
│   ├── benchmark.py       ← Run all experiments, generate Tables 6.1
│   └── worked_example.py  ← Reproduce all Tables 4.2–4.6, Fig 4.2, 4.3
├── /mpc/
│   ├── robot_dynamics.py  ← M(θ), C(θ,θ̇), G(θ) for 2-DOF distributed rod
│   ├── linearize.py       ← Ac, Bc computation + Cases A, B, C
│   ├── discretize.py      ← Ad, Bd, d via Euler and ZOH
│   ├── qp_formulate.py    ← Assemble Q_qp, p, A_eq, A_ineq
│   ├── pipg_solver.py     ← PIPG iterations
│   ├── mpc_loop.py        ← Full closed-loop simulation
│   ├── compare_solvers.py ← PIPG vs OSQP comparison
│   └── worked_example.py  ← Reproduce Table 5.6, Fig 5.7, 5.8
├── /validation/
│   ├── penalty_sweep.py   ← Validate Theorem 4.1 (generate Fig 6.5)
│   ├── mwis_bruteforce.py ← Exact MWIS for small graphs (ground truth)
│   ├── equilibrium_check.py ← Verify Ad*x0 + Bd*u0 + d = x0
│   └── hand_calc_verify.py  ← Compare hand calcs to code
├── /figures/
│   └── generate_all.py    ← Generate every figure in the thesis
└── /data/
    └── /results/          ← Saved experiment outputs
```

### 10.2 Key Functions to Implement

**`oim_simulate.py`:**
```python
def simulate_oim(h: np.ndarray, J: np.ndarray, 
                 T_solve: float = 100.0,
                 K_inject: float = 1.0,
                 noise_strength: float = 0.01,
                 n_restarts: int = 1) -> np.ndarray:
    """
    Simulate OIM dynamics and return binarized spin vector.
    
    ODE: dθᵢ/dt = K_inject * sin(2θᵢ) - Σⱼ Kᵢⱼ * sin(θⱼ - θᵢ) + noise
    where Kᵢⱼ = -2 * Jᵢⱼ
    
    Returns: s ∈ {-1, +1}^n (binarized phases)
    """
```

**`pipg_solver.py`:**
```python
def pipg_solve(Q_qp: np.ndarray, p: np.ndarray,
               A_eq: np.ndarray, b_eq: np.ndarray,
               A_ineq: np.ndarray, k_ineq: np.ndarray,
               u_lo: np.ndarray, u_hi: np.ndarray,
               max_iter: int = 200,
               alpha_0: float = 0.5,
               beta_0: float = 0.05,
               anneal_period: int = 50) -> dict:
    """
    PIPG solver for constrained QP.
    Returns: {'x': solution, 'cost': final cost, 'iters': iterations, 
              'cost_history': list, 'violation_history': list}
    """
```

### 10.3 Experiment Checklist

Before thesis submission, every item below must be checked:

- [ ] `worked_example.py` (MRTA): reproduces all numerical values in Tables 4.2–4.6
- [ ] `worked_example.py` (MPC): reproduces Table 5.6 to 3 sig. figures
- [ ] `penalty_sweep.py`: generates Figure 6.5, confirms Theorem 4.1 threshold
- [ ] `benchmark.py`: generates Table 6.1 and Figures 6.1–6.3
- [ ] `mpc_loop.py`: generates Figures 5.8 and 6.6–6.9
- [ ] `equilibrium_check.py`: passes for all 3 cases
- [ ] `hand_calc_verify.py`: all assertions pass

---

## 11. TONE, STYLE & VOICE GUIDE

**WRITER AGENT:** This section is your contract. Read it carefully. Violating the voice guide makes the thesis worse, not better.

### 11.1 The Core Voice

The thesis is written in the voice of:

> *A very smart, very curious person who has spent a year thinking deeply about something and wants to explain it to their most intelligent friend — clearly, honestly, and without condescension.*

This is NOT:
- The dry passive-voice voice of most journal papers ("It was observed that...")
- The overselling voice of grant proposals ("This transformative research will revolutionize...")
- The textbook voice ("The reader is encouraged to verify...")

This IS:
- Direct and active ("We show that...", "This means...", "Notice that...")
- Honest about limitations ("This fails when...", "We don't yet know...")
- Conversational at transitions ("Before we can get there, we need to understand X")
- Precise where it matters ("Specifically, we require $\lambda > \max_{(i,j)\in E}(w_i + w_j)$")

### 11.2 Sentence-Level Rules

1. **Maximum sentence length:** 30 words. If longer, split.
2. **No passive voice in explanatory text.** Allowed in formal theorem statements.
3. **Jargon introduction:** First use of every technical term gets a plain-English definition immediately after it. No exceptions.
4. **"We" vs "I":** "We" for technical derivations (standard academic), "I" for personal observations in the Preface and Chapter 8. Do not use "I" in technical chapters.
5. **Analogies:** Every major concept should have at least one analogy. The analogy comes *before* the equation, not after.
6. **Questions:** Use rhetorical questions to signal transitions. "But why would this work? Because..."
7. **Numbers:** All numbers below 10 spelled out in prose ("three robots"), numbers ≥ 10 as numerals ("20 robots"). Exceptions: equations, tables, figures.

### 11.3 Chapter Transition Sentences

Every chapter must end with a sentence that points forward. Every chapter must begin with a sentence that points back. Example:

> End of Chapter 4: "We now have a complete, verified pipeline from coalition MRTA to oscillator dynamics. The question of how these oscillators actually move a robot arm is the subject of the next chapter."
> 
> Begin of Chapter 5: "In the previous chapter, we solved the *allocation* problem — who does what. Now we face the *control* problem: how to do it."

### 11.4 Figure Captions

Every figure caption must:
1. Have a title line (bold) stating what the figure shows
2. Have 2–4 sentences explaining what to notice
3. Reference the relevant equation or table
4. Note any simplifications or assumptions

Example:
> **Figure 4.2: Conflict graph for the 3-robot 2-task worked example.** Nodes represent feasible (coalition, task) pairs with sizes proportional to utility weight. Red edges indicate robot conflicts (shared robots between coalitions); blue edges indicate task conflicts (same task assigned twice); purple edges indicate both simultaneously. The Maximum Weight Independent Set (highlighted nodes v₀ and v₃) corresponds to the optimal allocation (Definition 4.5), verified against the brute-force solution in Table 4.5.

### 11.5 Mathematical Writing Rules

1. **Every equation has a number** unless it is trivially in-line.
2. **Every equation has a preceding sentence** that says what it expresses.
3. **No "it can be shown"** — either show it or cite it.
4. **Proofs:** Begin with "Proof." on a separate line. End with $\square$. Keep to one page maximum. If longer, move to appendix and reference.
5. **Worked numbers:** Substituted expressions must show at least the first substitution step explicitly. Don't jump from formula to answer.

---

## 12. PUBLISHING & OUTREACH PLAN

### 12.1 Academic Track

**Target venues for adapted chapter content:**

| Content | Target Journal/Conference | Target Date |
|---|---|---|
| CMRTA-OIM (Chapter 4) | IEEE Robotics and Automation Letters (RA-L) | 6 months post-thesis |
| SNN-MPC (Chapter 5) | IEEE Control Systems Letters (L-CSS) | 9 months post-thesis |
| Full systems view | International Symposium on Experimental Robotics (ISER) | 1 year |
| India perspective | IEEE Spectrum (opinion) / National Academy of Sciences India | Flexible |

### 12.2 Public Release Track

The thesis is designed to go viral because:
- It tells a story, not just presents results
- The India angle resonates with a massive, underserved audience
- The visual quality is high
- The handwritten-notebook aesthetic (referenced in preface) is unusual and personal

**Release plan:**
- Upload PDF to arXiv (cs.RO + cs.ET)
- LinkedIn post: "I spent a year asking whether robot brains could look more like real brains. Here's what I found."
- Twitter/X thread: 15-tweet unrolled version of the core insight
- YouTube: Optional — author narrates the "bits to atoms" journey over key figures
- Medium: Adapted version of Chapter 1 as a standalone essay
- GitHub: All experiments code, open-source (MIT license)

### 12.3 The "Viral Hook" Elevator Pitch

> "Robots today run on the same chips your laptop uses. But what if we built chips that were *designed* to solve robot problems — chips that think like networks of neurons or oscillators, not like calculators? That's what I spent my thesis exploring. The physics is beautiful, the results are real, and the manufacturing opportunity for India is enormous."

---

## APPENDIX A — RAW SOURCE MATERIAL INDEX

| Source | Type | Key Content |
|---|---|---|
| `OIM_MRTA_Proposal_v2.md` | Technical proposal | Complete CMRTA→OIM derivation, worked example, validation plan |
| `SNN_MPC_Complete_Derivation.md` | Technical derivation | Full SNN-MPC from Lagrangian to PIPG, 5 iterations |
| `ilovepdf_merged.pdf` pages 1–23 | Handwritten notes | Author's vision, India argument, thesis structure ideas |
| `ilovepdf_merged.pdf` pages 24–39 | Handwritten math | MRTA scenario, MWIS, QUBO, Ising, OIM dynamics |
| `ilovepdf_merged.pdf` pages 40–55 | Handwritten math | Robot dynamics, linearization Cases A/B/C |
| `ilovepdf_merged.pdf` pages 56–70 | Handwritten math | Full derivation (distributed rod), MPC formulation, QP assembly |

**CONSISTENCY NOTE:** Pages 40–52 of the PDF use the **point-mass model** ($I_1 = I_2 = 0$, $l_1=l_2=1$m). Pages 56–70 use the **distributed-rod model** ($I_i = m_i l_i^2/3$, $l_1=l_2=0.5$m). The SNN_MPC file uses the distributed-rod model. **The thesis uses distributed-rod throughout.** When referencing notebook pages 40–52 for explanation or pedagogy, note the model difference explicitly.

---

## APPENDIX B — CRITICAL NUMBERS CROSS-REFERENCE

These numbers appear multiple times across documents. They must be consistent everywhere.

| Quantity | Value | Source | Used In |
|---|---|---|---|
| MRTA N | 3 robots | All MRTA docs | Tables 4.1–4.6, Figs 4.2–4.4 |
| MRTA M | 2 tasks | All MRTA docs | Tables 4.1–4.6 |
| MRTA K | 2 capability types | All MRTA docs | All MRTA tables |
| Task T₁ requirements | [1,1] | Notebook p25; Proposal | Table 4.1 |
| Task T₂ requirements | [2,0] | Notebook p25; Proposal | Table 4.1 |
| Robot r₁ capabilities | [2,0] | Notebook p27 | Table 4.1 |
| Robot r₂ capabilities | [0,2] | Notebook p27 | Table 4.1 |
| Robot r₃ capabilities | [1,1] | Notebook p27 | Table 4.1 |
| V₁ (task 1 base value) | 6.0 | Notebook p28 | Table 4.3 |
| V₂ (task 2 base value) | 5.0 | Notebook p28 | Table 4.3 |
| α (efficiency penalty) | 0.5 | Notebook p30 | Utility formula |
| OIM penalty coefficient | λ = 8 | Notebook p35 | Table 4.4, 4.6 |
| Robot arm l₁, l₂ | 0.5 m each | SNN_MPC file | All Ch5 derivations |
| Robot arm m₁, m₂ | 1 kg each | SNN_MPC file | All Ch5 derivations |
| Gravity g | 9.81 m/s² | SNN_MPC file (full deriv) | All Ch5 |
| MPC timestep Δt | 0.02 s (50 Hz) | SNN_MPC file | Tables 5.4, 5.5 |
| MPC horizon N_h | 10 | SNN_MPC file | Table 5.5 |
| PIPG convergence | ~55–80 iters | SNN_MPC file | Table 5.7, Fig 5.7 |
| EDP improvement | >100× vs OSQP | Mangalore 2024 | Ch 1, Ch 5, Ch 6 |

---

## APPENDIX C — OPEN QUESTIONS FOR THE ARCHITECT

These must be resolved before writing begins:

1. **Institution name:** Birla Institute of Technology and Sciences, Pilani
2. **Off Campus Supervisor:** Prof. Dr. Debanjan Bhowmik
2. **On Campus Supervisor:** Prof. Dr. Dhruv Kumar 
3. **Model choice for worked examples in Chapter 5:** The two notebook sections use different robot arm parameters ($l=1$m point mass vs. $l=0.5$m distributed rod). The SNN_MPC derivation uses $l=0.5$m distributed rod. **Confirm: use distributed rod throughout, and note the simplification used in the notebook's hand calculations is for pedagogical clarity.** This is already assumed in this blueprint. "Use distributed rod throughout" - author choice
4. **MRTA example utility values:** The notebook shows slightly different utility calculations than the proposal document. Validate Agent must compute these from scratch using the given parameters and confirm the ground-truth values before any writing begins. Validate every ground truth - Author
5. **Whether to include a Chapter on hardware implementation:** The notes mention FeFET and CMOS OIM hardware. Does the author have access to hardware results, or is this simulation-only? If simulation-only, Chapter 4's framing should be adjusted to "framework for future hardware deployment." Keep it simulation only right now.
6. **Code availability:** Will the GitHub repository be public at submission time? This affects the thesis language around reproducibility. Github code will be available on request, write accordingly, but the visual interfaces will be available publicly to try it out.
7. **Target degree:** M.Sc. Physics 

---

*End of Thesis Blueprint v1.0*  
*This document is LIVING — the Architect Agent may update it as the work progresses.*  
*All agents must flag inconsistencies they discover to the Architect immediately.*  
*Generated: May 2026*
