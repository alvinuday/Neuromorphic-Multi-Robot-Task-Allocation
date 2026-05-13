# 🧠 Bits to Atoms: Neuromorphic Computing for Physical Intelligence in Industrial Robotics

**Master's Thesis** by Alvin Adarsh Kumar  
BITS Pilani (on-campus advisor: Prof. Dhruv Kumar) + IIT Bombay (off-campus advisor: Prof. Debanjan Bhowmik)

---

## Quick Start

### **Interactive Web Visualizer** (No installation required)
👉 [OIM-MRTA Visualizer](docs/oim_mrta_viz.html) — Explore the full pipeline interactively

### **Complete Thesis** (PDF)
👉 [thesis-final-compiled.pdf](archives/thesis/thesis-final-compiled.pdf) — Full 111-page thesis

### **Run All Experiments**
```bash
# Install dependencies
pip install -r experiments/requirements.txt

# Run full experimental pipeline
python scripts/run_full_experimental_pipeline.py

# Run specific experiments
python -m pytest tests/ -v
```

---

## Project Overview

This research presents two neuromorphic hardware solutions for critical robotics optimization problems:

### **1. Coalition Multi-Robot Task Allocation (OIM-MRTA)**
Formulates multi-robot coordination as a Maximum Weight Independent Set problem and solves it on an OIM (Oscillator Ising Machine).
- **Solve time:** 12 ms end-to-end
- **Approximation ratio:** 0.92 (geometric graphs)
- **Scalability:** 50+ robots with spatial pruning

### **2. Model Predictive Control (SNN-MPC)**
Implements PIPG algorithm on analog Spiking Neural Networks with 100× energy-delay product improvement.
- **Convergence:** 55–80 iterations (~20 ms)
- **Energy efficiency:** >100× vs. OSQP on embedded hardware

---

## 📁 Repository Structure

```
Neuromorphic-Multi-Robot-Task-Allocation/
│
├── README.md                          ← You are here
├── .gitignore
├── requirements.txt                   ← Root dependencies (if any)
│
├── src/                              Core simulation code
│   ├── oim_sim/                      OIM simulation package
│   │   ├── benchmark.py              Benchmarking utilities
│   │   ├── hardware.py               Hardware models
│   │   ├── mrta.py                   MRTA implementation
│   │   ├── solvers/                  Classical solvers (greedy, SA, etc.)
│   │   └── types.py                  Type definitions
│   │
│   └── snn_sim/                      SNN simulation package
│       ├── arm_dynamics.py           Robot arm dynamics
│       ├── lif_neuron.py             Leaky Integrate-and-Fire model
│       ├── snn_solver.py             SNN-based solver
│       └── types.py                  Type definitions
│
├── tests/                            Test suite
│   ├── test_benchmark.py
│   ├── test_classical_solvers.py
│   ├── test_hardware_profiles.py
│   ├── test_kuramoto_solver.py
│   └── test_pipeline.py
│
├── experiments/                      Experimental pipeline & data
│   ├── requirements.txt              Experiment dependencies
│   ├── mrta/                         MRTA experiments
│   ├── mpc/                          MPC experiments
│   ├── validation/                   Mathematical validation tests
│   ├── complexity/                   Complexity analysis
│   ├── figures/                      Generated figures (27 PNGs)
│   ├── tables/                       Generated tables (LaTeX)
│   ├── data/                         Raw experiment data
│   ├── datasets/                     Input datasets
│   ├── factory/                      Factory-scale experiments
│   └── visualization/                Cockpit web interface
│
├── docs/                             Documentation
│   ├── README.md                     Documentation index
│   ├── architecture/                 System architecture docs
│   ├── reports/                      Analysis reports
│   ├── references/                   Literature review & BibTeX
│   ├── thesis/                       Thesis materials (live copy)
│   └── oim_mrta_viz.html            Interactive visualizer
│
├── scripts/                          Utility scripts
│   ├── run_full_experimental_pipeline.py    Main experiment runner
│   ├── generate_html_thesis.py              PDF→HTML converter
│   └── api_server.py                        REST API server
│
├── archives/                         Historical & submitted materials
│   ├── thesis/                       Complete thesis documents
│   │   ├── thesis-final-compiled.pdf
│   │   ├── thesis.html
│   │   ├── ThesisDocument/           LaTeX source + chapters
│   │   └── SlideDeck/                Presentation slides
│   │
│   ├── reports/                      Phase reports & execution summaries
│   │   ├── PLAN.md
│   │   ├── PROGRESS.md
│   │   ├── EXECUTION_SUMMARY.md
│   │   └── ...
│   │
│   └── proposals/                    Initial proposals & blueprints
│       └── THESIS_BLUEPRINT.md
│
├── results/                          Experiment results & artifacts
│   └── (auto-populated by experiments)
│
└── .claude/                          Claude Code configuration
    └── settings.json
```

---

## 📖 What's Where?

### **I want to...**

**Read the thesis**
- Full PDF: `archives/thesis/thesis-final-compiled.pdf`
- HTML version: `archives/thesis/thesis.html`
- LaTeX source: `archives/thesis/ThesisDocument/`

**Explore interactively**
- OIM-MRTA visualizer: `docs/oim_mrta_viz.html`
- Cockpit web UI: Start with `experiments/visualization/server.py`

**Run experiments**
- Full pipeline: `python scripts/run_full_experimental_pipeline.py`
- MRTA only: `python -m src.oim_sim.benchmark`
- MPC only: `python -m src.snn_sim.snn_solver`
- Tests: `pytest tests/ -v`

**Review results**
- Validation reports: `archives/reports/`
- Experiment data: `experiments/data/`
- Generated figures: `experiments/figures/`
- Generated tables: `experiments/tables/`

**Understand the code**
- OIM simulation: `src/oim_sim/` (entry: `mrta.py`)
- SNN simulation: `src/snn_sim/` (entry: `snn_solver.py`)
- Detailed docs: `docs/architecture/`

---

## Key Results

### **Mathematical Validation** ✅
- 12/12 validation tests pass (6 OIM, 6 SNN)
- Theorem 4.1 (penalty coefficient bounds) verified
- All hand calculations cross-checked with code

### **OIM-MRTA Experiments**
- **7-node worked example:** optimal utility = 9.1787, feasibility = 100%
- **Scalability:** <10ms for 20–30 robots, <100ms for 50+ (decomposed)
- **Approximation quality:** 85–92% of optimal on realistic instances
- **Honest limitations:** 37% convergence rate on dense graphs (expected for approximate solver)

### **SNN-MPC Experiments**
- **5-iteration hand trace:** Cost reduction from 0 to −0.009955 (geometric convergence)
- **Closed-loop simulation:** All 3 robot configurations reach target within 2–3 seconds
- **Energy estimates:** 100–1000× reduction vs. OSQP depending on scale

---

## 🚀 Getting Started

### **1. Setup Environment**
```bash
# Clone and navigate
cd Neuromorphic-Multi-Robot-Task-Allocation

# Install dependencies
pip install -r experiments/requirements.txt
```

### **2. Verify Installation**
```bash
# Run test suite
pytest tests/ -v

# Validate mathematical claims
python -m experiments.validation.hand_calc_verify
```

### **3. Run Experiments**
```bash
# Full pipeline (MRTA + MPC + figures + tables)
python scripts/run_full_experimental_pipeline.py

# Individual experiments
python -m src.oim_sim.benchmark --sizes tiny small medium
python -m src.snn_sim.snn_solver --mode closed-loop
```

### **4. Explore Results**
- Generated figures: `experiments/figures/`
- Generated tables: `experiments/tables/`
- Raw data: `experiments/data/`
- Test results: `results/`

---

## 🏗️ System Architecture

### **OIM-MRTA Pipeline**
```
Problem (robots, tasks)
    ↓
Coalition enumeration
    ↓
Conflict graph → Maximum Weight Independent Set
    ↓
QUBO formulation
    ↓
Ising Hamiltonian mapping
    ↓
OIM Hardware (simulated)
    ↓
Optimal/approximate allocation
```

### **SNN-MPC Pipeline**
```
Robot dynamics (nonlinear)
    ↓
Linearization around trajectory
    ↓
Discretization (Runge-Kutta)
    ↓
QP formulation (PIPG algorithm)
    ↓
SNN encoding (spike rates)
    ↓
Analog neuromorphic hardware (simulated)
    ↓
Control signal
```

---

## 📚 Documentation

| Topic | Location |
|-------|----------|
| **Architecture & Design** | `docs/architecture/` |
| **Literature Review** | `docs/references/LITERATURE_REVIEW_SUMMARY.txt` |
| **Interactive Visualizer** | `docs/oim_mrta_viz.html` |
| **API Reference** | `docs/api/` (auto-generated from docstrings) |
| **Experiment Reports** | `archives/reports/` |
| **Historical Plans** | `archives/proposals/` |

---

## ✅ Validation & Testing

All mathematical claims are validated:
- **12/12 test cases passing** (6 OIM, 6 SNN)
- **Theorem 4.1** (penalty coefficient bounds) verified
- **5-iteration hand trace** matches code output exactly
- **Scalability benchmarks** from 3 to 50+ robots

Run tests:
```bash
pytest tests/ -v
python -m experiments.validation.hand_calc_verify
```

---

## 🎯 Key Metrics

### OIM-MRTA
- **Solve time:** 12 ms (end-to-end, 20-robot instance)
- **Approximation ratio:** 0.85–0.92 (realistic graphs)
- **Convergence rate:** 37% (dense), 92% (sparse)
- **Scalability:** <100ms for 50+ robots (decomposed)

### SNN-MPC
- **Convergence:** 55–80 iterations (~20 ms)
- **Energy efficiency:** 100–1000× vs. OSQP
- **Accuracy:** ±2–3% tracking error

---

## 📋 Files & Purposes

**Source Code (`src/`)**
- `oim_sim/` → OIM simulation, QUBO assembly, classical solvers
- `snn_sim/` → SNN implementation, robot dynamics, PIPG solver

**Experiments (`experiments/`)**
- `mrta/` → Coalition enumeration, conflict graphs, benchmarking
- `mpc/` → Linearization, discretization, closed-loop control
- `validation/` → Hand calculation verification
- `figures/` → All publication-quality plots (300 DPI)
- `tables/` → LaTeX tables for thesis
- `data/` → JSON results and ground truth

**Tests (`tests/`)**
- `test_*.py` → Unit tests for all modules
- 5 test files covering 61 Python modules

**Scripts (`scripts/`)**
- `run_full_experimental_pipeline.py` → Execute all experiments
- `generate_html_thesis.py` → Convert PDF to interactive HTML
- `api_server.py` → REST API for remote execution

---

## 🔄 Reproducibility

Every number in the thesis is traceable:
1. **Hand calculations** → `experiments/validation/` (verified by code)
2. **Code execution** → `experiments/figures/`, `tables/` (traced to data)
3. **Data files** → `experiments/data/results/*.json` (ground truth)
4. **PDF generation** → `archives/thesis/thesis-final-compiled.pdf`

To regenerate everything:
```bash
python scripts/run_full_experimental_pipeline.py
```

---

## 📝 Project Statistics

- **Lines of code:** ~4,500 (Python)
- **Lines of tests:** ~1,000 (pytest)
- **Experiments:** 40+ variants (MRTA + MPC + validation)
- **Figures:** 27 (publication-quality, 300 DPI)
- **Tables:** 20 (properly formatted, thesis-ready)
- **Thesis pages:** 111 (auspicious!)

---

## 🎓 Thesis Contents

### Main Chapters
1. **Preface** — Personal motivation
2. **Introduction** — Problem context & contributions
3. **Background** — Literature review (13 papers)
4. **System Overview** — Unified framework
5. **Coalition MRTA via OIM** — Complete derivation
6. **MPC via SNN** — Complete derivation
7. **Results & Analysis** — Experiments + comparisons
8. **India's Opportunity** — Policy & market analysis
9. **Conclusion** — Reflection & future work

### Appendices
- **A.** QUBO ↔ Ising mathematical derivation
- **B.** Sign conventions in coupled oscillators
- **C.** PIPG convergence proof & complexity analysis

See `archives/thesis/` for full document.

---

## 📞 Support

- **Code issues:** Check `tests/` for examples, review docstrings
- **Experiment help:** See `experiments/requirements.txt`
- **Thesis questions:** Refer to `archives/thesis/ThesisDocument/`
- **Contact:** Author: Alvin Adarsh Kumar

---

**Built with neuromorphic precision. Organized with clarity.**

Bits to Atoms — from digital problems to physical solutions.  
*May 2026*