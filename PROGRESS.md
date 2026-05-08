# Thesis Execution Progress

**Thesis Title:** Bits to Atoms: Neuromorphic Computing for Physical Intelligence in Industrial Robotics  
**Author:** Alvin Adarsh Kumar  
**Target:** 80-90 pages, 8 chapters + preface + 3 appendices  
**Master Plan:** See `/Users/alvin/.claude/plans/thesis-blueprint-md-here-is-this-melodic-stardust.md`

---

## Phase Status

### ✅ Phase 0 — Setup & Repository Structure [COMPLETE]

- [x] 0.1 Updated `ThesisDocument/Metadata/Metadata.tex` with thesis info
  - Author: Alvin Adarsh Kumar
  - Supervisors: Dhruv Kumar (BITS) + Debanjan Bhowmik (IITB)
  - Title: "Bits to Atoms: Neuromorphic Computing..."
  - University: BITS Pilani
  - Degree: M.Sc. Physics

- [x] 0.2 Updated `ThesisDocument/IPLeiriaMain.tex` chapter includes
  - Removed template chapters (02-User-Guide, 03-Latex-Tutorial)
  - Added 8 thesis chapters: 00-Preface through 08-Conclusion
  - Updated appendices to match thesis structure

- [x] 0.3 Created experiments directory structure
  - `experiments/mrta/` — Coalition MRTA code
  - `experiments/mpc/` — Model Predictive Control code
  - `experiments/validation/` — Math validation suite
  - `experiments/figures/` — Figure generation
  - `experiments/literature/` — Literature review pipeline
  - `experiments/data/results/` — Experiment outputs

- [x] Created `experiments/requirements.txt` with all Python dependencies

**Status:** Ready for Phase 1

---

### ⏳ Phase 1 — Math Validation (Validator Agent) [PENDING]

**Expected outputs:**
- `experiments/validation/hand_calc_verify.py` — All V-OIM-1 through V-OIM-6, V-SNN-1 through V-SNN-6
- `experiments/data/results/validation_report.json` — Ground-truth locked numbers

**Key validations needed:**
- V-OIM-1: MRTA ↔ MWIS equivalence
- V-OIM-2: λ penalty coefficient sweep → Figure 6.5
- V-OIM-3: 7×7 QUBO matrix Q
- V-OIM-4: Optimal MWIS solution
- V-OIM-5: Ising parameters h_k, J_ij
- V-OIM-6: OIM convergence on worked example
- V-SNN-1 through V-SNN-6: All MPC inertia/linearization/PIPG values

**Model:** Distributed rod (l₁=l₂=0.5m, m₁=m₂=1kg, I=ml²/3)

---

### ⏳ Phase 2 — OIM Simulator Fix (Implementation Agent) [PENDING]

**New files to create:**
- `experiments/mrta/oim_simulate.py` — Fixed OIM dynamics with correct signs
- `experiments/mrta/qubo_formulate.py` — Explicit QUBO matrix assembly
- `experiments/mrta/ising_map.py` — QUBO → Ising parameter derivation

**Key fixes:**
- Sign convention: K_ij = -2*J_ij (not +2*J_ij)
- Bias term: proportional to -h_i (not degree)
- Multi-start ≥5 random initializations
- Noise annealing schedule

---

### ⏳ Phase 3 — Literature Review (Literature Agent) [PENDING]

**Output files:**
- `references.bib` — Verified citations for LaTeX
- Chapter 2 draft text sections 2.1–2.6

**13 critical papers to verify/locate:**
- Lucas (2014) Frontiers in Physics
- Wang & Roychowdhury (2019, 2021)
- Mangalore et al. (2024) arXiv:2401.14885 ✓
- Yu et al. (2021) arXiv:2009.06980 ✓
- Gerkey & Matarić (2004) IJRR
- Sandholm et al. (1999)
- Vig & Adams (2006)
- Rawlings, Mayne & Diehl (2020)
- Lynch & Park (Modern Robotics)
- Others per blueprint §8.3

---

### ⏳ Phase 4 — Figure Generation (Figure Agent) [PENDING]

**18 publication-quality figures required:**

**CRITICAL (blocking writing):**
1. Fig 4.2 — 7-node conflict graph
2. Fig 4.3 — OIM phase trajectories
3. Fig 5.1 — 2-DOF robot arm diagram
4. Fig 5.5 — PIPG neural circuit
5. Fig 5.7 — PIPG convergence
6. Fig 5.8 — 4-panel closed-loop simulation
7. Fig 6.1 — Approximation ratio box plot
8. Fig 6.2 — Time-to-solution log-log
9. Fig 6.5 — MWIS quality vs λ

**HIGH priority:**
- Fig 1.1–1.4 (Ch 1)
- Fig 3.1–3.2 (Ch 3)
- Fig 4.5–4.6 (Ch 4)
- Fig 6.8–6.10 (Ch 6)
- Fig 7.1 (Ch 7)

**All figures:** ≥300 DPI, color palette per blueprint §9.4

---

### ⏳ Phase 5 — Experiment Runs (Validator Agent) [PENDING]

**Commands:**
```bash
# MRTA experiments
python experiments/mrta/worked_example.py    # Tables 4.2–4.6
python experiments/validation/penalty_sweep.py  # Fig 6.5
python experiments/mrta/benchmark.py --sizes tiny small medium large

# MPC experiments
python experiments/mpc/worked_example.py    # Table 5.6
python experiments/mpc/mpc_loop.py --case A --case B --case C
python experiments/mpc/compare_solvers.py   # Table 6.3
```

**Output:** All results to `experiments/data/results/` as JSON

---

### ⏳ Phase 6 — Thesis Writing (Writer Agent) [PENDING]

**8 chapters + preface to write:**
1. `Chapters/00-Preface.tex` — Personal voice
2. `Chapters/01-Introduction.tex` — Problem, opportunity, contributions
3. `Chapters/02-Background.tex` — Literature review
4. `Chapters/03-SystemOverview.tex` — Architecture overview
5. `Chapters/04-CMRTA-OIM.tex` — Coalition MRTA derivation
6. `Chapters/05-SNN-MPC.tex` — Robot control derivation
7. `Chapters/06-Results.tex` — Experimental results
8. `Chapters/07-India.tex` — Manufacturing opportunity
9. `Chapters/08-Conclusion.tex` — Reflection & future work

**Appendices:**
- `Chapters/Appendices/00-QUBODerivation.tex`
- `Chapters/Appendices/01-IsingSigns.tex`
- `Chapters/Appendices/02-PIPGProof.tex`

**Voice guide:** Blueprint §11 — conversational-academic hybrid, max 30 word sentences, active voice, "we" in technical chapters, "I" in preface/conclusion

---

### ⏳ Phase 7 — Table Generation (Table Agent) [PENDING]

**20 critical tables**, all data from `validation_report.json` + experiment results:
- Tables 4.1–4.8 (MRTA)
- Tables 5.1–5.7 (MPC)
- Tables 6.1–6.3 (Results)
- Table 7.1 (India TRL assessment)
- Table 2.1 (IM hardware platforms)

**Format:** `booktabs` style (no vertical lines), alternating row colors for large tables

---

### ⏳ Phase 8 — GitHub Integration [PENDING]

**Final repo structure:**
```
Neuromorphic-Multi-Robot-Task-Allocation/
├── ThesisDocument/           ← LaTeX source
├── experiments/              ← All reproducible code
├── src/oim_sim/              ← Core simulation package
├── oim_mrta_viz.html         ← Interactive demo
├── SlideDeck/                ← Presentation
├── THESIS_BLUEPRINT.md       ← Living spec
├── PROGRESS.md               ← This file
└── README.md                 ← Updated with thesis info
```

**Commits:**
- Phase 0 → Phase 1 checkpoint
- Phase 1 → Phase 2 checkpoint
- Phase 3 → Phase 4 checkpoint
- Phase 5 → Phase 6 checkpoint
- Phase 9 final → `v1.0-submission` tag

---

### ⏳ Phase 9 — QA & Final Compile [PENDING]

**Checklist:**
- [ ] All figures ≥300 DPI
- [ ] All tables from `validation_report.json`
- [ ] All equations numbered and referenced
- [ ] Notation table (§9.3) consistent across chapters
- [ ] Distributed rod model throughout Ch 5
- [ ] N=3, M=2, k=2 examples unchanged in Ch 4
- [ ] λ=8, θ*=[π/4,π/4] throughout
- [ ] All 13 critical citations verified
- [ ] Chapter transitions (forward/back pointers)
- [ ] Preface "I" voice, technical "We" voice
- [ ] Abstract 300–350 words
- [ ] GitHub linked in thesis
- [ ] Hand validation suite passes
- [ ] LaTeX compiles with zero errors/warnings

---

## Critical Files

| File | Purpose | Status |
|------|---------|--------|
| `/THESIS_BLUEPRINT.md` | Single source of truth | ✓ Read & understood |
| `/ThesisDocument/Metadata/Metadata.tex` | Author/supervisor info | ✓ Updated |
| `/ThesisDocument/IPLeiriaMain.tex` | Master LaTeX document | ✓ Updated |
| `experiments/validation/hand_calc_verify.py` | Math validation | ⏳ To create |
| `experiments/data/results/validation_report.json` | Ground truth | ⏳ To generate |
| `experiments/figures/generate_all.py` | All figures | ⏳ To create |
| All `ThesisDocument/Chapters/*.tex` | Thesis content | ⏳ To write |

---

## Key Decision Points

1. **MRTA example numbers:** N=3, M=2, K=2 locked. Utility values (V₁=6, V₂=5, α=0.5) must be computed from scratch first.
2. **Robot arm model:** Distributed rod (l=0.5m each) throughout — NOT point mass.
3. **OIM penalty:** λ=8 fixed, must satisfy Theorem 4.1 for N=3 example.
4. **Writing voice:** Conversational-academic per §11 — strict adherence required.
5. **GitHub:** Code available on request, visualizers public.

---

## Handoff Instructions for Next Agent

If execution stops, the next agent should:

1. **Read the plan:** `/Users/alvin/.claude/plans/thesis-blueprint-md-here-is-this-melodic-stardust.md`
2. **Check this file:** See current phase status above
3. **Verify Phase 0 completion:** All setup done ✓
4. **Pick up where it stopped:** Launch Phase 1+ agents as specified in plan
5. **Update this file:** Add progress after each phase
6. **Maintain git commits:** One per phase with status tag
7. **Test reproducibility:** Every code commit should allow clean re-run from `requirements.txt`

---

**Last updated:** [Auto-update as work progresses]  
**Current phase:** Phase 0 ✓ → Phase 1 ready to start
