# Documentation Hub

Welcome to the documentation for **Bits to Atoms**: Neuromorphic Computing for Physical Intelligence in Industrial Robotics.

---

## 📖 Main Project Documentation

Start here if you're new to the project:
- **[Main README](../README.md)** - Project overview, structure, quick start

---

## 🏗️ Architecture & Design

Detailed technical documentation:
- **[System Overview](architecture/system-overview.md)** - High-level architecture
- **[OIM-MRTA Design](architecture/oim-mrta.md)** - Coalition allocation via Oscillator Ising Machine
- **[SNN-MPC Design](architecture/snn-mpc.md)** - Model Predictive Control via Spiking Neural Networks

---

## 📚 References & Literature

- **[Literature Review](references/LITERATURE_REVIEW_SUMMARY.txt)** - Complete literature survey (13 papers)
- **[BibTeX References](../experiments/references.bib)** - Full bibliography

---

## 🎓 Thesis Materials

- **[Thesis PDF](thesis/thesis-final-compiled.pdf)** - 111-page compiled thesis
- **[Thesis HTML](thesis/thesis.html)** - Interactive HTML version
- **[LaTeX Source](thesis/ThesisDocument/)** - Complete LaTeX source code
- **[Slides](thesis/SlideDeck/)** - Presentation slides

---

## 📊 Experiments & Results

- **[Experiment Data](../experiments/data/)** - Raw JSON results
- **[Generated Figures](../experiments/figures/)** - 27 publication-quality plots (300 DPI)
- **[Generated Tables](../experiments/tables/)** - All 20 thesis tables in LaTeX

---

## 🔍 Interactive Tools

- **[OIM-MRTA Visualizer](oim_mrta_viz.html)** - Explore the full pipeline interactively
- **[Web Cockpit](../experiments/visualization/)** - Experimental control dashboard

---

## 💻 Code Structure

Source code organization:
- **[Source Code](../src/)** - Core simulation packages
  - `oim_sim/` - OIM simulation and MRTA solver
  - `snn_sim/` - SNN simulation and MPC solver
- **[Tests](../tests/)** - Unit test suite (19 tests, all passing)
- **[Scripts](../scripts/)** - Utility scripts for execution and visualization

---

## 🔗 Quick Links

| What | Where |
|------|-------|
| Run experiments | `python scripts/run_full_experimental_pipeline.py` |
| Run tests | `pytest tests/ -v` |
| Read thesis | `archives/thesis/thesis-final-compiled.pdf` |
| View reports | `archives/reports/` |
| Check code | `src/oim_sim/` and `src/snn_sim/` |
| Experiment code | `experiments/mrta/` and `experiments/mpc/` |

---

## 📝 Document Status

Last updated: May 2026

- ✅ Thesis complete (111 pages)
- ✅ All experiments validated (19/19 tests pass)
- ✅ Code reorganized and documented
- ✅ Repository structure professional and clean

---

## 🤝 Contributing

This is a completed thesis project. For questions or issues:
1. Check the main [README.md](../README.md)
2. Review relevant thesis chapters in `thesis/`
3. Check test cases in `tests/`
4. Consult experiment code in `experiments/`
