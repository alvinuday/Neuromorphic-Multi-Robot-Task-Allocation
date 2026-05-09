# COMPREHENSIVE THESIS AUDIT PLAN
**Date:** May 10, 2026  
**Status:** In Progress  
**Scope:** Full thesis audit with harsh scientific critique, blueprint alignment, figure validation, and remediation

---

## EXECUTIVE SUMMARY

This document outlines a rigorous, multi-phase audit of the thesis covering:
1. Blueprint compliance (all 8 chapters)
2. Mathematical rigor verification
3. Figure source validation and rebuilding
4. Prose refinement for clarity and style
5. Final validation before commit/push

**Guiding Principles:**
- Investigate before deleting; preserve prior insights and derivations
- Science-first: every claim must be evidence-based
- Professional tone: harsh critique is constructive criticism
- Blueprint is canonical: all deviations must be justified

---

## PHASE 1: BLUEPRINT COMPLIANCE AUDIT

### Methodology
For each chapter, verify:
1. **Content Coverage**: Does chapter contain all §X.Y sections from BLUEPRINT?
2. **Narrative Flow**: Does prose follow "story outline, not table of contents" principle?
3. **Worked Examples**: Are examples (N=3,M=2,k=2 for CMRTA; Cases A,B,C for MPC) properly threaded?
4. **Mathematical Depth**: Are proofs complete? Are equations derived, not just stated?
5. **Figure References**: Does every figure mentioned in blueprint exist and is referenced?

### Chapter-by-Chapter Checklist

#### Chapter 1 — Introduction
- [ ] §1.1 "World is Automating" — warehouse story + optimization bottleneck (3–4 pages ✓)
- [ ] §1.2 "History of Computing Paradigms" — timeline + Von Neumann → neuromorphic (2–3 pages)
  - Current: reads well but timeline could be more rigorous
  - **Issue**: Figure 1.1 (Timeline) is bare template, needs historical data
- [ ] §1.3 "Neuromorphic Hardware Primer" — OIM + SNN explanations (3 pages)
  - **Issue**: Section exists but feels rushed; needs more physical intuition
- [ ] §1.4 "This Thesis: Two Experiments" — clear pipeline (2 pages)
  - **Figure 1.4**: "The Pipeline" diagram present and good
- [ ] §1.5 "Contributions" — 8 numbered items
  - Current: listed but needs elaboration with citations
- [ ] §1.6 "Roadmap" — one paragraph per chapter
  - Current: present but too brief; should read like story

#### Chapter 2 — Background & Related Work
- [ ] §2.1 "Combinatorial Optimization on Physical Hardware" (4 pages)
  - Current: Well-structured coverage of Ising, QA, CIM, OIM, SBM
  - **Issue**: Comparison table (Table 2.1) is mentioned but may be incomplete
- [ ] §2.2 "Multi-Robot Task Allocation" (3 pages)
  - Current: Good taxonomy coverage (Gerkey & Matarić)
  - **Critique**: Gap statement needs sharpening—why is MWIS formulation truly novel?
- [ ] §2.3 "Model Predictive Control for Robots" (3 pages)
  - Current: Good coverage, but missing ANYmal MPC details
- [ ] §2.4 "Neuromorphic Computing Platforms" (3 pages)
  - Current: Loihi, TrueNorth, Bhowmik group—good
- [ ] §2.5 "Related Work on Oscillator Dynamics" (2 pages)
  - Current: Brief, adequate
- [ ] §2.6 "India Context" (1 page)
  - Current: Missing India policy analysis; should be expanded with Semicon data

#### Chapter 3 — System Overview
- [ ] §3.1 "Four-Layer Architecture" — clear diagram (Figure 3.1 ✓)
- [ ] §3.2 "Two Use Cases Comparison Table" — Table present
- [ ] §3.3 "Classical vs. Neuromorphic Trade-offs" — Figure 3.2
  - **Issue**: Figure may be speculative, needs data backing

#### Chapter 4 — CMRTA via OIM
- [ ] §4.1 "Warehouse Floor Motivating Scenario" (1.5 pages)
  - Current: Good narrative with Figure 4.1
- [ ] §4.2 "Mathematical Formulation" (3 pages) — 5 definitions + worked example (N=3,M=2)
  - **Critical**: Table 4.1 (Robot capabilities) ✓, Table 4.2 (Feasibility) ✓, Table 4.3 (Utility) ✓
  - All numbers hand-verified? **NEED TO VERIFY**
- [ ] §4.3 "MRTA to MWIS" (4 pages)
  - §4.3-step1: Coalition explosion calculation
  - §4.3-step2: Coalition bounding
  - §4.3-step3: Feasibility enumeration
  - §4.3-step4: Utility calculation
  - §4.3-step5: Conflict graph + Figure 4.2
  - **Critical**: Lemma 4.1 (MRTA = MWIS) — proof present and complete? **VERIFY**
- [ ] §4.4 "QUBO Formulation" (4 pages)
  - Theorem 4.1 (Penalty Bound) — complete proof?
  - Table 4.4 (QUBO Matrix) — all entries correct?
  - Table 4.5 (QUBO Verification) — minimizer check?
  - **Critical**: These are validation anchors
- [ ] §4.5 "Ising Mapping" (3 pages)
  - Full derivation: QUBO → Ising expansion
  - Table 4.6: Ising parameters
  - **Issue**: Derivation may skip steps
- [ ] §4.6 "OIM Dynamics" (3 pages)
  - Phase equation derivation
  - Binarization rule
  - Figure 4.3: Phase trajectories (OIM simulation)
  - **Issue**: Figure may be simulated/hallucinated; verify against code
- [ ] §4.7 "Scalability" (2 pages)
  - Coalition bounding, spatial pruning, graph decomposition
  - Table 4.7: Scalability table
  - Figure 4.5: Scaling plot
  - **Issue**: May lack empirical data
- [ ] §4.8 "Hybrid Pipeline" (1 page) — Figure 4.6 + Table 4.8
- [ ] §4.9 "Failure Modes & Honest Limitations" (1 page) — **THIS IS CRITICAL**
  - Current: May be superficial; needs honest analysis of OIM's weaknesses

#### Chapter 5 — SNN-MPC
- [ ] §5.1 "Control Problem" (1.5 pages) — Figure 5.1 (robot arm schematic)
- [ ] §5.2 "Robot Physics from First Principles" (4 pages)
  - Lagrangian approach: T, V, L derivation
  - Inertia matrix M(θ) — all 4 entries derived?
  - Table 5.1: System parameters
  - Table 5.2: Matrix values at target pose
  - **Critical**: Parameters match handwritten notebook exactly?
- [ ] §5.3 "Linearization" (3 pages)
  - A_c computation: full 4×4 Jacobian derivation
  - Case studies A, B, C with equilibrium analysis
  - Table 5.3: All A_c, B_c, u_0 values
  - **Critical**: Do Case A, B, C values match handwritten notebook?
- [ ] §5.4 "Discretization" (1.5 pages)
  - ZOH vs. Euler discussion
  - Table 5.4: Discrete matrices A_d, B_d, d
  - Verification check (equilibrium condition)
- [ ] §5.5 "MPC as QP" (3 pages)
  - Cost function equation + all terms explained
  - Decision variable vector z construction
  - Figure 5.2: Block-diagonal Q_qp structure
  - Figure 5.3, 5.4: Constraint matrices
  - Table 5.5: QP dimensions for N=1,2,5,10,20
- [ ] §5.6 "PIPG Algorithm" (3 pages)
  - PIPG iteration equations (three lines)
  - Neural interpretation
  - Figure 5.5: PIPG neural circuit diagram
  - Convergence guarantee statement
- [ ] §5.7 "Mapping to Analog SNN" (2 pages)
  - LIF neuron model equation
  - Bhowmik Group analog SNN description
  - Figure 5.6: SNN architecture diagram
- [ ] §5.8 "Hand Calculation: 5 PIPG Iterations" (3 pages) **CRITICAL**
  - t=0→1, 1→2, 2→3, 3→4, 4→5 with all arithmetic shown
  - Table 5.6: Convergence table
  - Figure 5.7: Convergence plot
  - Analytical verification against unconstrained QP
  - **Issue**: Hand calculations may not be present or verified
- [ ] §5.9 "MPC Closed-Loop Behavior" (1 page)
  - Table 5.7: Performance summary
  - Figure 5.8: 4-panel closed-loop simulation plots
- [ ] §5.10 "Limitations & Extensions" (1 page) — honest failure analysis

#### Chapter 6 — Results, Analysis & Discussion
- [ ] §6.1 "OIM-CMRTA Results" (4 pages)
  - Figure 6.1: Approximation ratio
  - Figure 6.2: Time-to-solution
  - Figure 6.3: Constraint violation rate
  - Figure 6.4: Phase trajectories
  - Table 6.1: Summary results
  - Figure 6.5: QUBO penalty analysis
  - **Issue**: All figures must be based on actual simulation data, not hallucinated
- [ ] §6.2 "SNN-MPC Results" (4 pages)
  - Figure 6.6: Phase-space trajectory
  - Figure 6.7: PIPG convergence curves
  - Figure 6.8: Energy-delay product comparison
  - Figure 6.9: Torque profiles
  - Table 6.2: Linearization accuracy
  - Table 6.3: Solver comparison
- [ ] §6.3 "Cross-Case Discussion" (2 pages)
  - Figure 6.10: Capability map

#### Chapter 7 — India's Opportunity
- [ ] §7.1 "Historical Parallel: Mobile Revolution" (2 pages)
- [ ] §7.2 "Why Neuromorphic is Different" (1.5 pages)
- [ ] §7.3 "India's Existing Assets" (1.5 pages)
  - Figure 7.1: India's neuromorphic ecosystem map
  - **Issue**: May be speculative; needs grounding in real institutions
- [ ] §7.4 "Application Stack" (1 page)
- [ ] §7.5 "What Needs to Happen" (1.5 pages)
  - Table 7.1: TRL assessment

#### Chapter 8 — Conclusion
- [ ] §8.1 "What We Did" (1 page) — reflective summary
- [ ] §8.2 "What We Learned" (1 page) — honest synthesis
- [ ] §8.3 "Future Work" (2 pages) — short/medium/long term roadmap
- [ ] §8.4 "Personal Note" (0.5 page) — author voice

---

## PHASE 2: MATHEMATICAL RIGOR VERIFICATION

### Proofs to Hand-Verify

1. **Lemma 4.1 (MRTA = MWIS)** — Currently: sketch proof
   - Action: Expand to full, formal proof with clear steps
   
2. **Theorem 4.1 (Penalty Bound)** — Currently: proof present
   - Action: Verify logic; check that step "removing either $x_i$ or $x_j$ strictly decreases cost" is rigorous
   
3. **QUBO to Ising Mapping** — Currently: algebraic steps given
   - Action: Verify all intermediate expansions are shown
   - Check: Final formulas for $h_k$ and $J_{ij}$ match literature

4. **PIPG Convergence** — Currently: Convergence guarantee mentioned
   - Action: State the convergence theorem precisely (cite Yu et al. 2021)
   - Verify: Step-size requirements

5. **Linearization Error Bounds** — Currently: none stated
   - Action: Derive/cite error bounds for linearization around equilibrium
   - Quantify: At what deviation does linearization break?

### Key Numerical Values to Verify

| Item | Value | Source | Status |
|------|-------|--------|--------|
| MRTA Worked Example (N=3, M=2) | Table 4.1–4.7 | Hand calculation | NEED TO VERIFY |
| Robot physics parameters (l, m, I) | Table 5.1 | Handwritten notebook | NEED TO VERIFY |
| Linearized matrices (Case A, B, C) | Table 5.3 | Handwritten notebook | NEED TO VERIFY |
| PIPG hand iterations (5 steps) | §5.8 | Hand calculation | MISSING/INCOMPLETE |
| OIM simulation results | Figure 4.3, 6.1–6.5 | Python code | NEED TO VERIFY CODE |
| MPC simulation results | Figure 5.8, 6.6–6.9 | Python code | NEED TO VERIFY CODE |

---

## PHASE 3: FIGURE VALIDATION & REBUILDING

### Current Figure Inventory

**Status Categories:**
- ✅ **Verified**: Figure exists, data is real, properly captioned
- ⚠️ **Suspect**: Figure exists but data source unclear or seems hallucinated
- ❌ **Missing**: Figure referenced in blueprint but not generated
- 🔄 **Needs Rebuild**: Figure exists but is low quality or incorrect

| Fig # | Title | Current Status | Issue | Action |
|-------|-------|---|------|--------|
| 1.1 | Timeline | ⚠️ | Bare template, lacks historical annotations | Rebuild with dates/events |
| 1.2 | Architecture Comparison | ✅ | Good schematic | Review for accuracy |
| 1.3 | Energy-Delay Product | ⚠️ | May lack data sources | Verify against papers |
| 1.4 | Pipeline Diagram | ✅ | Clear flow | Keep |
| 1.5 | Computational Paradigms | ⚠️ | Unclear source | Verify origin |
| 1.6 | Energy-Latency Trade-off | ⚠️ | Data points unclear | Rebuild with real data |
| 2.1 | Ising Hardware Landscape | ⚠️ | Scatter plot, verify papers listed | Check all references |
| 3.1 | Bits-to-Atoms Stack | ✅ | Good architecture | Keep |
| 3.2 | Trade-off Space | ⚠️ | Estimated from literature | Verify estimates |
| 4.1 | Warehouse Scenario | ✅ | Illustrative | Keep |
| 4.2 | Conflict Graph (7-node) | ⚠️ | Must verify against Table 4.3 | Rebuild from table data |
| 4.3 | OIM Phase Trajectories | ⚠️ | Simulated; verify code | Check simulation code |
| 4.4 | Anti-ferromagnetic Intuition | ✅ | Conceptual diagram | Keep |
| 4.5 | Scalability Plot | ⚠️ | Computed; verify formulas | Check computation |
| 4.6 | Hybrid Pipeline | ✅ | Flow diagram | Keep |
| 5.1 | Robot Arm Schematic | ✅ | Technical diagram | Keep |
| 5.2 | Q_qp Block Structure | ⚠️ | Matrix visualization; verify structure | Check dimensions |
| 5.3–5.4 | Constraint Matrices | ⚠️ | Block diagrams; verify structure | Check dimensions |
| 5.5 | PIPG Neural Circuit | ⚠️ | Requires verification | Rebuild from spec |
| 5.6 | SNN Architecture | ⚠️ | Requires Bhowmik Group input | Clarify or replace |
| 5.7 | Convergence Plot | 🔄 | Needs actual hand-calc data | Rebuild from §5.8 |
| 5.8 | Closed-Loop Plots (4-panel) | ⚠️ | Simulation-based; verify code | Check Python code |
| 6.1–6.10 | All Results Figures | ⚠️ | ALL benchmark data must be verified | Run experiments/verify code |
| 7.1 | India Ecosystem Map | ⚠️ | Institutional locations; verify | Update with real institutions |

### Rebuilding Strategy

1. **Figures 4.2, 5.7**: Rebuild from table data (4.3, 5.6)
2. **Figures 1.1, 1.6, 3.2**: Rebuild with explicit data sources and historical/literature citations
3. **Figures 4.3, 5.8, 6.1–6.10**: Verify against Python code; re-run if code is available
4. **Figures 5.5, 5.6, 6.10**: Rebuild with clearer labels and proper attribution

---

## PHASE 4: PROSE REFINEMENT

### Tone & Style Audit

**Current Issues to Address:**

1. **Passive voice**: "The approach is..." → "We show...", "We derive..."
2. **Jargon density**: Some sections (especially 4.3, 5.2) are dense; break up with intuition boxes
3. **Missing intuition**: Equations stated without "why should we care?" context
4. **Inconsistent style**: Introduction is conversational; some technical chapters are dry
5. **Citation coverage**: Some claims lack citations (e.g., energy consumption figures)

### Key Sections Requiring Rewrite

- **§1.3** "Neuromorphic Hardware Primer" — needs more physical intuition
- **§2.6** "India Context" — currently brief; expand with policy data
- **§4.3** "MRTA to MWIS" — add intuition between mathematical steps
- **§5.2** "Robot Physics" — add "why matters" framing before each subsection
- **§4.9, §5.10** "Failure Modes" — currently superficial; deepen honestly

---

## PHASE 5: FINAL VALIDATION CHECKLIST

- [ ] All tables are complete, properly formatted, with captions
- [ ] All figures are referenced in text and have detailed captions (150–200 words)
- [ ] All equations are numbered and cited when referenced
- [ ] All citations present and formatted consistently
- [ ] No orphaned sections or incomplete derivations
- [ ] Worked examples (N=3,M=2 for CMRTA; Cases A,B,C for MPC) are complete and consistent
- [ ] Hand calculations (§4.3 tables, §5.8 convergence) are fully shown
- [ ] Appendices contain all referenced proofs and derivations
- [ ] PDF compiles without errors
- [ ] Page targets met: ~80–90 pages (excluding appendices, references)

---

## EXECUTION ROADMAP

### Week 1: Audit & Planning
1. **Days 1–2**: Phase 1 (Blueprint compliance) — identify gaps
2. **Days 3–4**: Phase 2 (Mathematical rigor) — verify proofs
3. **Days 5**: Phase 3 (Figure validation) — catalog issues

### Week 2: Remediation
1. **Days 6–8**: Phase 4 (Prose refinement) — rewrite sections
2. **Days 9–10**: Phase 3 (Figure rebuild) — fix hallucinated figures

### Week 3: Validation & Release
1. **Days 11–12**: Phase 5 (Final validation) — full pass
2. **Days 13**: Commit & push to main

---

## NOTES FOR FUTURE REFERENCE

### Prior Work Preservation
- Investigate every section tagged "⚠️" before deletion
- Reference the commit messages and insights from better models before you
- Preserve all hand calculations and proofs; only strengthen presentation

### Scientific Integrity
- No figure stays in thesis unless:
  1. Data source is documented
  2. Derivation/simulation code is cited
  3. Numbers have been hand-verified or independently validated
- Claims about "100× energy improvement" must cite specific papers and configurations
- All approximation ratios and performance metrics must be traced to simulation or literature

### Professionalism
- Tone: rigorous but accessible
- Avoid speculation; ground everything in evidence
- Bold admissions of limitations strengthen work, not weaken it

