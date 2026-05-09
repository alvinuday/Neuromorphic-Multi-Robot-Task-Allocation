# Thesis Execution Plan: "Bits to Atoms"
## Neuromorphic Hardware for Physical Intelligence in Industrial Robotics

**Author:** Alvin Adarsh Kumar | **Degree:** M.Sc. Physics, BITS Pilani  
**Supervisors:** Prof. Dr. Debanjan Bhowmik (IITB, off-campus) + Prof. Dr. Dhruv Kumar (on-campus)  
**Blueprint version read:** v1.0 (May 2026, 1659 lines)

---

## Context

The blueprint specifies a complete ~80–90 page master's thesis combining:
1. **OIM-MRTA**: Coalition Multi-Robot Task Allocation → MWIS → QUBO → Ising → Oscillator Ising Machine simulation
2. **SNN-MPC**: 2-DOF robot arm Lagrangian dynamics → MPC QP → PIPG algorithm → Analog SNN mapping
3. A full experiment pipeline, 18+ publication-quality figures, 20+ hand-verified tables, a literature review, India manufacturing policy chapter, and a creative conversational writing style

The existing codebase (`src/oim_sim/`) has working baselines (greedy, SA, random restarts) and a partially-working Kuramoto OIM simulator (poor convergence currently). The IPLeiria LaTeX template is already in `ThesisDocument/`. A detailed `SNN_MPC_Complete_Derivation.md` file exists (not yet read — Agent Phase 1 must retrieve it).

**This plan is the single execution sequence for agents to follow. The blueprint is the bible — read it before each phase.**

---

## Phase 0 — Setup & Repository Structure

**Goal:** Establish clean repo structure, copy in the LaTeX template, configure metadata, and build the experiments scaffold before any writing.

### 0.1 Update Metadata in LaTeX Template

File: `ThesisDocument/Metadata/Metadata.tex`

Replace all placeholder values:
- `\FirstAuthor{Alvin Adarsh Kumar}`
- `\FirstAuthorNumber{<BITS-ID>}` ← leave placeholder `XXXXXXX` for author to fill
- `\Supervisor{Dhruv Kumar}` + mail/title
- `\CoSupervisor{Debanjan Bhowmik}` + mail + `Associate Professor, IIT Bombay`
- `\Title{Bits to Atoms: Neuromorphic Computing for Physical Intelligence in Industrial Robotics}`
- `\Subtitle{A Study in OIM-Based Coalition Task Allocation and SNN-Based Model Predictive Control}`
- `\University{Birla Institute of Technology and Science, Pilani}`
- `\School{Department of Physics}` (or closest match in template)
- `\Degree{Master of Science in Physics}`
- `\AcademicYear{2024/25}`

### 0.2 Replace Template Chapters with Thesis Chapters

Remove boilerplate chapters from `IPLeiriaMain.tex`:
```
\include{Chapters/02-User-Guide}
\include{Chapters/03-Latex-Tutorial}
```

Add all thesis chapters:
```
\include{Chapters/00-Preface}
\include{Chapters/01-Introduction}
\include{Chapters/02-Background}
\include{Chapters/03-SystemOverview}
\include{Chapters/04-CMRTA-OIM}
\include{Chapters/05-SNN-MPC}
\include{Chapters/06-Results}
\include{Chapters/07-India}
\include{Chapters/08-Conclusion}
```

Also add appendices:
```
\input{Chapters/Appendices/00-QUBODerivation}
\input{Chapters/Appendices/01-IsingSigns}
\input{Chapters/Appendices/02-PIPGProof}
```

### 0.3 Create Experiments Directory Structure

Create `/experiments/` at repo root matching blueprint §10.1:
```
experiments/
├── README.md
├── requirements.txt         # numpy scipy matplotlib networkx cvxpy osqp sympy
├── mrta/
│   ├── coalition_enum.py    # reuse src/oim_sim/mrta.py logic
│   ├── conflict_graph.py
│   ├── qubo_formulate.py    # NEW: assemble full Q matrix
│   ├── ising_map.py         # NEW: QUBO → h_i, J_ij
│   ├── oim_simulate.py      # REWRITE Kuramoto - fix convergence
│   ├── greedy_repair.py
│   ├── benchmark.py         # extend existing benchmark.py
│   └── worked_example.py    # reproduce Tables 4.2–4.6
├── mpc/
│   ├── robot_dynamics.py    # M(θ), C(θ,θ̇), G(θ) — distributed rod
│   ├── linearize.py         # Ac, Bc, Cases A/B/C
│   ├── discretize.py        # Ad, Bd, d
│   ├── qp_formulate.py      # Q_qp, p, A_eq, A_ineq
│   ├── pipg_solver.py       # PIPG iterations
│   ├── mpc_loop.py          # closed-loop simulation
│   ├── compare_solvers.py   # PIPG vs OSQP
│   └── worked_example.py    # Table 5.6, Fig 5.7
├── validation/
│   ├── penalty_sweep.py     # Fig 6.5 — Theorem 4.1 validation
│   ├── mwis_bruteforce.py   # ground truth (reuse src/oim_sim/solvers/exact.py)
│   ├── equilibrium_check.py # V-SNN-5
│   └── hand_calc_verify.py  # all V-OIM/V-SNN assertions
├── figures/
│   └── generate_all.py      # one command → all 18 thesis figures
└── data/results/            # saved experiment outputs + JSON
```

---

## Phase 1 — Math Validation (Validator Agent)

**MUST complete before any writing. Blueprint §7.**

All claims below need two-method verification (hand + code). See blueprint §7 for exact expected values.

### 1.1 MRTA Validation (V-OIM-1 through V-OIM-6)

Run `experiments/validation/hand_calc_verify.py`:

1. **V-OIM-1**: Verify MRTA ↔ MWIS equivalence for N=3, M=2 worked example
2. **V-OIM-2**: Sweep λ from 0.1× to 10× max(wᵢ+wⱼ) → confirm 100% feasibility above threshold → generates **Figure 6.5**
3. **V-OIM-3**: Auto-generate 7×7 QUBO matrix, compare entry-by-entry to hand calculation
4. **V-OIM-4**: Brute-force MWIS on 7-node graph → confirm optimal solution, reconcile with notebook values  
   - **CRITICAL NOTE**: Blueprint flags a discrepancy between notebook utility values and proposal values. Compute from scratch using: V₁=6, V₂=5, α=0.5, robot caps [2,0],[0,2],[1,1], task reqs [1,1],[2,0]
5. **V-OIM-5**: Compute h_k and J_ij from Q matrix, compare code vs hand
6. **V-OIM-6**: Run 100 OIM simulations on 7-node example, record convergence rate

### 1.2 SNN-MPC Validation (V-SNN-1 through V-SNN-6)

**USE DISTRIBUTED ROD MODEL THROUGHOUT** (l₁=l₂=0.5m, m₁=m₂=1kg, I=ml²/3). Do not mix with point-mass notebook pages 40-52.

1. **V-SNN-1**: M(θ*) at θ=[0,0] → expected [[0.6667, 0.2083],[0.2083, 0.0833]]
2. **V-SNN-2**: Equilibrium torques for Cases A, B, C
3. **V-SNN-3**: Ad, Bd, d for Case A via Euler and ZOH — compare
4. **V-SNN-4**: PIPG iterations 0–5 → Table 5.6 values
5. **V-SNN-5**: Verify Ad*x0 + Bd*u0 + d = x0 for all 3 cases
6. **V-SNN-6**: Gravity Jacobian Cases B ([[-15,-5],[-5,-5]]) and C ([[-10,-10],[-10,-10]])

**Output:** A `validation_report.json` with PASS/FAIL for each check and the ground-truth numerical values. These numbers are locked — thesis writing uses them.

---

## Phase 2 — OIM Simulator Fix (Implementation Agent)

The existing Kuramoto OIM in `src/oim_sim/solvers/kuramoto.py` achieves near-zero utility on benchmarks. This must be fixed before experiments.

### What needs to change in `experiments/mrta/oim_simulate.py` (new file):

Implement the correct OIM dynamics from blueprint §4.6:
```
dθᵢ/dt = K_inject * sin(2θᵢ) + Σⱼ Kᵢⱼ * sin(θⱼ - θᵢ) + ξᵢ(t)
where Kᵢⱼ = -2 * Jᵢⱼ   (anti-ferromagnetic for conflict edges)
```

Key fixes vs current code:
- **Sign convention**: Kᵢⱼ = -2Jᵢⱼ, not +2Jᵢⱼ. Conflict edges have Jᵢⱼ > 0 → Kᵢⱼ < 0 → anti-ferromagnetic. Verify this is correct.
- **Bias term**: Kᵢᵢ proportional to -hᵢ (node utility bias), not degree
- **Noise annealing**: Start high (escape local minima), anneal to zero
- **Multi-start**: ≥5 random initializations, keep best solution by utility
- **Post-processing**: Greedy repair only if infeasible

Also add `experiments/mrta/qubo_formulate.py` (new) and `experiments/mrta/ising_map.py` (new) implementing the explicit QUBO matrix assembly and QUBO→Ising parameter derivation.

---

## Phase 3 — Literature Review (Literature Agent)

Blueprint §8 specifies a Python pipeline. Implement `experiments/literature/lit_pipeline.py`:

1. Query Semantic Scholar API and arXiv for the primary + background + India topics in blueprint §8.2
2. Filter to 80–100 high-relevance papers
3. For each paper, generate structured summary: {title, authors, year, venue, problem, method, result, gap, key_quote}
4. Verify all 13 critical papers from blueprint §8.3 (confirm DOIs, get full citations)
5. Output `references.bib` for LaTeX
6. Generate draft text for Chapter 2 sections 2.1–2.6 — Writer Agent then rewrites in thesis voice

**Key references to confirm:**
- Lucas (2014) Frontiers in Physics — Ising formulations
- Wang & Roychowdhury (2019, 2021) — OIM foundations  
- Mangalore et al. (2024) arXiv:2401.14885 — Loihi MPC (**confirmed**)
- Yu et al. (2021) arXiv:2009.06980 — PIPG (**confirmed**)
- Gerkey & Matarić (2004) Int J Robotics Research — MRTA taxonomy

---

## Phase 4 — Figure Generation (Figure Agent)

Blueprint §5 lists all 18 required figures. All must be generated in Python (matplotlib/seaborn/plotly), ≥300 DPI, using the color palette:
- PRIMARY BLUE: #1B4F72
- SECONDARY ORANGE: #D35400  
- ACCENT GREEN: #1E8449
- ACCENT RED: #C0392B

Generate via `experiments/figures/generate_all.py`.

### Priority order:

**CRITICAL (blocking thesis writing):**
- **Fig 4.2**: 7-node conflict graph (networkx + matplotlib). Node size ∝ utility. Red=robot conflict, blue=task conflict, purple=both. Highlight MWIS solution nodes.
- **Fig 4.3**: OIM phase trajectories for 7-node example — 7 colored lines converging to {0, π}
- **Fig 5.1**: 2-DOF robot arm technical diagram (matplotlib patches or SVG). Label all parameters.
- **Fig 5.5**: PIPG neural circuit diagram — x neurons (blue), y neurons (orange), connection arrows
- **Fig 5.7**: PIPG convergence — cost J vs iteration, geometric decrease
- **Fig 5.8**: 4-panel closed-loop simulation (θ₁,θ₂ vs time; τ₁,τ₂ vs time; error on log scale; solve time)
- **Fig 6.1**: Box-whisker: approximation ratio ρ vs problem size (4 sizes × methods)
- **Fig 6.2**: Log-log: time-to-solution vs |V|
- **Fig 6.5**: MWIS quality vs λ — validates Theorem 4.1

**HIGH:**
- Fig 1.1: Hardware-algorithm co-evolution timeline
- Fig 1.2: CPU vs OIM vs SNN architecture comparison
- Fig 1.3: Energy-delay product bar chart (from Mangalore 2024 data)
- Fig 1.4: "The Pipeline" flow diagram
- Fig 3.1: 4-layer bits-to-atoms stack
- Fig 4.5: Scalability |V| vs N with pruning strategies
- Fig 4.6: Hybrid pipeline block diagram
- Fig 6.8: Energy-delay product comparison bar chart

**For figures that need simulation data not yet available**: generate with **placeholder styling** (correct axes, labels, color scheme, correct shape) with `[PLACEHOLDER — run experiments/mrta/benchmark.py to regenerate]` in caption. This way the document compiles and looks professional.

---

## Phase 5 — Experiment Runs (Validator Agent)

All experiments produce JSON output to `experiments/data/results/`. All figures regenerate from these results.

### 5.1 MRTA Experiments
```bash
python experiments/mrta/worked_example.py    # Tables 4.2–4.6
python experiments/validation/penalty_sweep.py  # Fig 6.5
python experiments/mrta/benchmark.py --sizes tiny small medium large --restarts 5
# → Table 6.1, Fig 6.1, Fig 6.2, Fig 6.3
```

Benchmark sizes per blueprint §6.1:
- Tiny: N=5, M=3, k=2 (~30 nodes)
- Small: N=10, M=5, k=2 (~100 nodes)
- Medium: N=20, M=10, k=2 (~200 nodes)
- Large: N=50, M=20, decomposed (~500 nodes, decomposed into ~150-node subproblems)

100 random instances per size. Compare: OIM (fixed), greedy, SA, random-restarts, exact (tiny only).

### 5.2 MPC Experiments
```bash
python experiments/mpc/worked_example.py    # Table 5.6 — 5 PIPG iterations
python experiments/mpc/mpc_loop.py --case A --case B --case C  # Fig 5.8, 6.6–6.9
python experiments/mpc/compare_solvers.py   # Table 6.3 — OSQP vs PIPG
python experiments/validation/equilibrium_check.py  # V-SNN-5 assertion
```

### 5.3 Validation Suite
```bash
python experiments/validation/hand_calc_verify.py   # All V-OIM + V-SNN checks
```
Must pass all assertions before thesis submission.

---

## Phase 6 — Thesis Writing (Writer Agent)

Write all chapters in LaTeX. Files go into `ThesisDocument/Chapters/`. Follow blueprint §11 voice guide strictly.

**Writing order** (each chapter depends on validation of its data):

### Chapter files to create:

| File | Blueprint | Pages | Depends on |
|------|-----------|-------|------------|
| `00-Preface.tex` | Ch 0 | 2-3 | Nothing — write first |
| `01-Introduction.tex` | Ch 1 | 12-15 | Lit review draft, Fig 1.1–1.4 |
| `02-Background.tex` | Ch 2 | 15-18 | Literature pipeline output |
| `03-SystemOverview.tex` | Ch 3 | 4-6 | Fig 3.1, 3.2 |
| `04-CMRTA-OIM.tex` | Ch 4 | 22-26 | All V-OIM validations, Tables 4.1–4.8, Figs 4.1–4.6 |
| `05-SNN-MPC.tex` | Ch 5 | 22-25 | All V-SNN validations, Tables 5.1–5.7, Figs 5.1–5.8 |
| `06-Results.tex` | Ch 6 | 10-12 | Benchmark results, Figs 6.1–6.10 |
| `07-India.tex` | Ch 7 | 5-7 | Fig 7.1, Table 7.1 |
| `08-Conclusion.tex` | Ch 8 | 4-5 | Nothing beyond previous chapters |
| `Appendices/00-QUBODerivation.tex` | App A | 3-4 | V-OIM-3 validation |
| `Appendices/01-IsingSigns.tex` | App B | 2-3 | V-OIM-5 validation |

### Key writing rules (blueprint §11):
- Max 30 words per sentence. Active voice. Analogy before equation.
- "We" for technical chapters, "I" only in Preface + Ch 8
- Every chapter: epigraph → chapter abstract → chapter pipeline diagram → content → transition sentence
- Every equation numbered. Every equation preceded by a sentence. No "it can be shown."
- Figure captions: bold title + 2-4 sentences + equation reference + assumptions

### LaTeX environments to use (blueprint §9.2):
- `\begin{theorem}...\end{theorem}` — numbered, with Proof...□
- `\begin{keyresult}` — blue box for key equations
- `\begin{authornote}` — gray box for author's conversational asides
- `\begin{example}` — orange left-bar for worked examples

---

## Phase 7 — Tables (Table Agent)

All 20 tables from blueprint §6. Every number in every table must come from `validation_report.json` or `experiments/data/results/`. No manual typing.

**CRITICAL tables (reproduce exactly from hand calculation):**
- Table 4.2: Feasibility check (all 6 coalition-task pairs)
- Table 4.3: Utility calculation (coalition, task, excess, φ, travel cost, U)
- Table 4.4: 7×7 QUBO matrix Q
- Table 4.6: Ising parameters hₖ and Jᵢⱼ
- Table 5.2: M(θ*), det(M), M⁻¹, G(θ*), ∂G/∂θ for all 3 cases
- Table 5.3: Ac, Bc, u₀ for all 3 cases
- Table 5.4: Ad, Bd, d for Case A (full numerical values)
- Table 5.6: PIPG convergence — 5 iterations

Format: `booktabs` style (no vertical lines, `\toprule \midrule \bottomrule`). Use `\rowcolor` for alternating rows on large tables.

---

## Phase 8 — GitHub Integration

### 8.1 Repo structure at time of push:
```
Neuromorphic-Multi-Robot-Task-Allocation/
├── ThesisDocument/           ← LaTeX source (full thesis)
├── experiments/              ← All Python code (reproducible)
├── src/oim_sim/              ← Core simulation package (existing)
├── oim_mrta_viz.html         ← Public interactive demo (existing)
├── SlideDeck/                ← Presentation (existing)
├── THESIS_BLUEPRINT.md       ← Living spec
└── README.md                 ← Updated with thesis description + links
```

### 8.2 README.md update:
```markdown
# Bits to Atoms: Neuromorphic Computing for Physical Intelligence

Master's thesis by Alvin Adarsh Kumar, BITS Pilani / IIT Bombay
Supervisor: Prof. Dr. Debanjan Bhowmik

## Try it
→ [Interactive OIM-MRTA Visualizer](oim_mrta_viz.html) (public)

## Reproduce experiments
cd experiments && pip install -r requirements.txt
python validation/hand_calc_verify.py   # validate all math
python figures/generate_all.py          # regenerate all figures
python mrta/benchmark.py                # OIM vs greedy benchmark

## Code available on request
Contact: [email]

## Thesis PDF
Available on arXiv: [link once submitted]
```

### 8.3 Commit strategy:
- One commit per major phase (experiments, figures, chapters)
- Tag `v1.0-submission` at final compile

---

## Phase 9 — Final Assembly & QA

### 9.1 LaTeX compile check:
```bash
cd ThesisDocument
latexmk -pdf IPLeiriaMain.tex
```
Must compile with zero errors and zero warnings.

### 9.2 QA checklist (QA Agent):
- [ ] All figures present and rendering at ≥300 DPI
- [ ] All tables consistent with `validation_report.json`
- [ ] All equation numbers referenced correctly
- [ ] Notation table (blueprint §9.3): every symbol consistent across all chapters
- [ ] No mixed models (distributed rod throughout Ch 5, not point-mass)
- [ ] Example numbers: N=3, M=2, k=2 unchanged throughout Ch 4
- [ ] λ=8 used in Ch 4 QUBO matrix, satisfies Theorem 4.1
- [ ] All 13 critical citations present in `references.bib` with verified DOIs
- [ ] Chapter transitions: each chapter ends pointing forward, each begins pointing back
- [ ] Preface uses "I" voice; technical chapters use "We"
- [ ] Abstract: exactly 300–350 words, structure matches blueprint §3.2
- [ ] GitHub repo linked from thesis
- [ ] `hand_calc_verify.py` passes all assertions

---

## Critical Files

| File | Role |
|------|------|
| `THESIS_BLUEPRINT.md` | Single source of truth — read before every task |
| `OIM_MRTA_Proposal_v2.md` | Full MRTA→OIM derivation source |
| `SNN_MPC_Complete_Derivation.md` | Full SNN-MPC derivation source (must be found in repo) |
| `ThesisDocument/IPLeiriaMain.tex` | Master LaTeX document |
| `ThesisDocument/Metadata/Metadata.tex` | Author/supervisor info |
| `experiments/validation/hand_calc_verify.py` | Math validation suite |
| `experiments/figures/generate_all.py` | All figure generation |
| `experiments/data/results/validation_report.json` | Locked ground-truth numbers |

---

## Execution Order Summary

```
Phase 0: Setup (metadata, directory structure)           [1 day]
Phase 1: Math validation                                  [2 days]
Phase 2: OIM simulator fix + QUBO/Ising modules           [2 days]
Phase 3: Literature review pipeline                       [2 days]
Phase 4: Figure generation (placeholders → real)          [ongoing]
Phase 5: Experiment runs                                  [2 days]
Phase 6: Writing (all 9 chapters + appendices)            [7 days]
Phase 7: Tables (from locked numbers)                     [2 days]
Phase 8: GitHub push + README                             [1 day]
Phase 9: QA + final compile                               [1 day]
Total estimated: ~20 days parallel agent execution
```

---

## Agent Assignment

| Agent | Phases | Key deliverables |
|-------|--------|-----------------|
| **Architect Agent** | All | Keep blueprint updated; resolve discrepancies |
| **Validator Agent** | 1, 5 | `validation_report.json`, all V-OIM + V-SNN checks |
| **Implementation Agent** | 0, 2 | Experiments scaffold, fixed OIM, QUBO/Ising modules |
| **Literature Agent** | 3 | `references.bib`, Chapter 2 draft text, paper summaries |
| **Figure Agent** | 4 | All 18 figures in `experiments/figures/`, placeholders first |
| **Writer Agent** | 6 | All `.tex` chapter files, voice per blueprint §11 |
| **Table Agent** | 7 | All 20 tables embedded in chapter `.tex` files |
| **LaTeX Agent** | 0, 9 | Template setup, final compile, zero warnings |
| **QA Agent** | 9 | Final consistency pass against checklist above |

Each agent must re-read `THESIS_BLUEPRINT.md` before starting. Flag any inconsistency to Architect Agent immediately. The numbers in `experiments/data/results/validation_report.json` are the ground truth — no agent may override them.