# Chapter 2: Literature Review and Foundational Concepts

**Chapter Abstract:** This chapter surveys the intersection of four research areas critical to this thesis: combinatorial optimization on physical hardware, multi-robot task allocation, model predictive control for robots, and neuromorphic computing platforms. We first review how NP-hard optimization problems are mapped onto physical systems, then examine task allocation as a combinatorial optimization problem. Next, we cover the control theory needed to translate task allocations into actual robot motion. Finally, we survey neuromorphic platforms—from oscillator-based machines to spiking neural networks—that can solve these problems with dramatically lower energy consumption than conventional von Neumann computers. By the end of this chapter, the reader will understand why neuromorphic computing is not just an academic curiosity but a practical necessity for real-time, energy-efficient multi-robot systems.

---

## 2.1 Combinatorial Optimization on Physical Hardware

Combinatorial optimization problems—finding the best solution among a finite (but exponentially large) set of candidates—appear everywhere in science and engineering. The Traveling Salesman Problem, Maximum Clique, Graph Coloring, and Boolean satisfiability are all classic NP-hard problems. For small instances, brute-force enumeration works. For realistic sizes, classical computers struggle because they must search through an exponential solution space using sequential logic.

A radical alternative: encode the optimization problem into the physics of a system, and let nature itself find the minimum. This idea goes back to the 1980s but has only recently become practical.

### 2.1.1 The Ising Model as a Universal Optimization Framework

The Ising model, borrowed from statistical physics, provides a universal language for optimization problems. An Ising spin system is a collection of binary variables $s_i \in \{-1, +1\}$ with an energy Hamiltonian:

$$H_{\text{Ising}}(\mathbf{s}) = \sum_i h_i s_i + \sum_{i < j} J_{ij} s_i s_j$$

where $h_i$ is an external field bias on spin $i$ and $J_{ij}$ is the coupling strength between spins $i$ and $j$. The ground state—the configuration with minimum energy—encodes the solution to an optimization problem.

**Why is this powerful?** Lucas (2014) demonstrated that virtually any NP-hard problem can be expressed as finding the ground state of an Ising Hamiltonian. The reduction is constructive: given a problem, one can compute the field biases $h_i$ and couplings $J_{ij}$ such that the ground state corresponds to the optimal solution.

### 2.1.2 QUBO Formulation and Problem Mapping

In practice, most optimization problems are formulated using binary variables $x_i \in \{0, 1\}$ rather than spins. The Quadratic Unconstrained Binary Optimization (QUBO) model captures these:

$$\mathcal{Q}(\mathbf{x}) = \sum_i c_i x_i + \sum_{i < j} Q_{ij} x_i x_j$$

QUBO is the modern workhorse for quantum and analog optimization hardware.

---

## 2.2 Multi-Robot Task Allocation

A team of robots must execute a set of tasks. Tasks differ in their complexity and required capabilities. Robots differ in their abilities. The question is: how do we assign tasks to robots to maximize overall utility?

This is the Multi-Robot Task Allocation (MRTA) problem.

### 2.2.1 MRTA Taxonomy (Gerkey & Matarić, 2004)

Gerkey and Matarić (2004) provided the foundational taxonomy that organizes MRTA problems along three dimensions:

1. **Task characteristics:** Single-task (ST) vs. multi-task (MT) assignments
2. **Robot characteristics:** Single-robot (SR) vs. multi-robot (MR) tasks
3. **Information structure:** Off-line vs. on-line

This thesis focuses on **MT-MR-Off-line** problems: multiple robots can work on multiple tasks sequentially, tasks may require coalitions, and all information is known upfront.

### 2.2.2 The Conflict Graph Formulation

The MRTA problem can be reformulated as a Maximum Weight Independent Set (MWIS) problem on a conflict graph. This reformulation is the key bridge to using optimization hardware.

---

## 2.3 Model Predictive Control for Robots

Allocation tells us *what* to do. Control tells us *how* to do it. Once we know which coalition should execute which task, we must compute the actual joint torques or velocities to move the robot arm or body.

### 2.3.1 Rigid-Body Dynamics

A robot manipulator with $n$ joints has joint angles $\boldsymbol{\theta} \in \mathbb{R}^n$. The Euler-Lagrange equations of motion are:

$$\mathbf{M}(\boldsymbol{\theta}) \ddot{\boldsymbol{\theta}} + \mathbf{C}(\boldsymbol{\theta}, \dot{\boldsymbol{\theta}}) \dot{\boldsymbol{\theta}} + \mathbf{G}(\boldsymbol{\theta}) = \boldsymbol{\tau}$$

### 2.3.2 Linearization and Discretization

For control design, we linearize around an equilibrium point. Using Euler's method with timestep $\Delta t$:

$$\mathbf{x}[k+1] = A_d \mathbf{x}[k] + B_d \mathbf{u}[k] + \mathbf{d}$$

### 2.3.3 Model Predictive Control Formulation

The core idea of MPC is to compute a short sequence of future control inputs that minimize a cost function subject to constraints. At each sampling time step $k$, we solve a finite-horizon optimal control problem:

$$\min_{\mathbf{z}} \frac{1}{2} \mathbf{z}^T \mathbf{Q}_{qp} \mathbf{z} + \mathbf{p}^T \mathbf{z}$$

subject to linear constraints.

---

## 2.4 Neuromorphic Computing Platforms

We now shift focus to the hardware side. Neuromorphic computing platforms are devices designed to mimic the structure and operation of biological brains: parallel, low-power, and event-driven rather than clock-driven.

### 2.4.1 Overview of Neuromorphic Architectures

Neuromorphic platforms fall into several categories:

1. **Spiking neural networks (SNNs)** on specialized hardware (Loihi, BrainScaleS, TrueNorth)
2. **Oscillator-based Ising machines** (Optical CIM, Electronic OIM)
3. **Quantum annealing** (out of scope for this thesis)

### 2.4.2 Intel Loihi: A Concrete Example

The Intel Loihi chip (released 2017) is a 128-core neuromorphic processor. Each core simulates ~1,000 spiking neurons using an integrate-and-fire model. Neurons communicate via spikes (binary events), not floating-point values. This event-driven operation means the chip only consumes power when spikes occur—typically resulting in 50-1000x lower power than conventional CPUs.

### 2.4.3 Coherent Ising Machines (CIM)

Coherent Ising Machines are optical systems that encode optimization problems into the phase relationships of laser pulses. McMahon et al. (2016) demonstrated a 100-spin CIM. Honjo et al. (2021) later scaled this to 100,000 spins at room temperature.

---

## 2.5 Oscillator Dynamics and Optimization

To bridge oscillator hardware and task allocation, we must understand how oscillator dynamics solve optimization problems.

### 2.5.1 Oscillator Synchronization as Consensus

Coupled oscillators naturally synchronize. This is a physical realization of consensus, where the "agreed value" is encoded in the common frequency and phase differences.

### 2.5.2 Solving QUBO via OIM

The Oscillator Ising Machine, introduced by Wang & Roychowdhury (2019, 2021), is a general framework for solving optimization problems using coupled oscillators. The parameters are chosen to encode the QUBO problem, and the oscillators evolve toward configurations corresponding to low-energy (optimal) solutions.

---

## 2.6 India Context: Neuromorphic Manufacturing and Future Opportunities

While most of this thesis covers science and engineering, it would be incomplete without addressing the broader context: the opportunity for India to lead in neuromorphic computing and its applications.

### 2.6.1 The Neuromorphic Computing Wave

The field of neuromorphic computing is entering a critical phase. Traditional Moore's Law scaling is slowing. Chip power consumption is rising. Machine learning inference at the edge demands low power and low latency. Neuromorphic hardware directly addresses these challenges.

Major players are investing heavily: Intel (Loihi), IBM (TrueNorth), BrainScaleS collaboration, SpiNNaker in the UK, and significant funding in China.

### 2.6.2 India's Current Position and Opportunities

India has strong theoretical computer science and engineering research. Yet India is largely absent from the neuromorphic hardware race.

**Opportunities:**
- India's semiconductor industry is growing
- Neuromorphic algorithms and software tools can be developed independently
- Applications in agriculture, manufacturing, and infrastructure are natural fits for India's economy
- Collaboration with international partners can bring technology transfer

### 2.6.3 Manufacturing and Task Allocation as a Use Case

India is home to millions of small and medium enterprises (SMEs) in manufacturing. A low-power multi-robot task allocation system would be transformative. A neuromorphic solution would consume 100x less energy, make allocation decisions in microseconds, and be implementable on compact, affordable hardware.

---

## Summary

This chapter has surveyed the four pillars of the thesis:

1. **Ising and QUBO** provide universal languages for encoding optimization problems on physical hardware
2. **MRTA** is formulated as Maximum Weight Independent Set on a conflict graph, enabling hardware-accelerated solutions
3. **MPC** provides the control law for executing allocated tasks
4. **Neuromorphic platforms** (Loihi, CIM, OIM) offer energy efficiency compared to classical computers

The following chapters build on these foundations: Chapter 3 provides a worked example, Chapter 4 details the QUBO formulation for MRTA, Chapter 5 covers MPC on spiking neural networks, and Chapter 6 presents experimental results.

---

## References

Key papers cited in this chapter:
- Lucas (2014): Ising formulations of optimization problems
- Gerkey & Matarić (2004): MRTA taxonomy
- Sandholm et al. (1999): Coalition structure generation
- Wang & Roychowdhury (2019, 2021): OIM theory and implementation
- Rawlings et al. (2020): MPC comprehensive treatment
- McMahon et al. (2016), Honjo et al. (2021): CIM hardware
- Lynch & Park (2017): Modern Robotics textbook
- Mangalore et al. (2024), Yu et al. (2021): Recent neuromorphic systems
