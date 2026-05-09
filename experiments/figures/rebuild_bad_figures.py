#!/usr/bin/env python3
"""
Rebuild 6 low-quality thesis figures using Plotly + kaleido.
Each figure is saved as both PDF and PNG to ThesisDocument/Figures/.

Figures rebuilt:
  1. fig_1_5.pdf/png     — Three Computational Paradigms (grouped bar comparison)
  2. fig_6_4_phase_trajectories_worked.pdf/png — OIM Phase Trajectories
  3. fig_2_2.pdf/png     — Scalability Plot (conflict graph size vs robots)
  4. fig_3_4.pdf/png     — Bits-to-Atoms Stack Diagram
  5. fig_7_2.pdf/png     — OIM Scalability: Latency and Quality (dual-axis)
  6. fig_7_1_india_ecosystem.png / fig_8_1.pdf/png — India Growth Opportunity
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================================
# PROFESSIONAL STYLE CONSTANTS
# ============================================================================

FONT_FAMILY = "Computer Modern, serif"

COLORS = {
    'blue':     '#1a6faf',
    'orange':   '#e07b00',
    'green':    '#1a7f37',
    'red':      '#d1242f',
    'purple':   '#6f42c1',
    'gray':     '#57606a',
    'light_bg': '#f6f8fa',
}

BASE_LAYOUT = dict(
    font=dict(family=FONT_FAMILY, size=13, color="#24292f"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=60, r=40, t=50, b=60),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#d0d7de",
        borderwidth=1,
    ),
)

REPO_ROOT = "/Users/alvin/Documents/Alvin/College/Academics/Master's Thesis/Code/Neuromorphic-Multi-Robot-Task-Allocation"
OUT = os.path.join(REPO_ROOT, "ThesisDocument", "Figures")
os.makedirs(OUT, exist_ok=True)


def save(fig, stem, width, height, scale=2):
    pdf_path = os.path.join(OUT, f"{stem}.pdf")
    png_path = os.path.join(OUT, f"{stem}.png")
    fig.write_image(pdf_path, width=width, height=height, scale=scale)
    fig.write_image(png_path, width=width, height=height, scale=scale)
    print(f"  Saved {stem}.pdf  and  {stem}.png")


# ============================================================================
# FIG 1 — fig_1_5: Three Computational Paradigms
# ============================================================================

def fig_1_5_computational_paradigms():
    """
    Grouped bar chart comparing Classical CPU, Neuromorphic (OIM/SNN),
    and Quantum Annealing across 5 dimensions.
    """
    dimensions = ["Latency", "Energy\nEfficiency", "Real-time\nCapable",
                  "Scalability", "Commercial\nReadiness"]

    # Scores 0-10 (higher = better)
    cpu_scores      = [3,  2, 4, 8, 10]
    neuro_scores    = [9,  9, 9, 6,  4]
    quantum_scores  = [5,  4, 2, 4,  2]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Classical CPU",
        x=dimensions,
        y=cpu_scores,
        marker_color=COLORS['gray'],
        marker_line=dict(color="#24292f", width=1),
        text=[str(v) for v in cpu_scores],
        textposition="outside",
        textfont=dict(size=12, family=FONT_FAMILY),
    ))

    fig.add_trace(go.Bar(
        name="Neuromorphic (OIM/SNN)",
        x=dimensions,
        y=neuro_scores,
        marker_color=COLORS['blue'],
        marker_line=dict(color="#24292f", width=1),
        text=[str(v) for v in neuro_scores],
        textposition="outside",
        textfont=dict(size=12, family=FONT_FAMILY),
    ))

    fig.add_trace(go.Bar(
        name="Quantum Annealing",
        x=dimensions,
        y=quantum_scores,
        marker_color=COLORS['orange'],
        marker_line=dict(color="#24292f", width=1),
        text=[str(v) for v in quantum_scores],
        textposition="outside",
        textfont=dict(size=12, family=FONT_FAMILY),
    ))

    layout = dict(**BASE_LAYOUT)
    layout.update(
        width=900,
        height=420,
        barmode="group",
        bargap=0.25,
        bargroupgap=0.05,
        yaxis=dict(
            title="Score (0–10, higher is better)",
            range=[0, 12],
            gridcolor="#e0e0e0",
            showline=True,
            linecolor="#d0d7de",
        ),
        xaxis=dict(
            showline=True,
            linecolor="#d0d7de",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d0d7de",
            borderwidth=1,
        ),
        margin=dict(l=60, r=40, t=80, b=70),
    )
    fig.update_layout(**layout)

    save(fig, "fig_1_5", width=900, height=420)


# ============================================================================
# FIG 2 — fig_6_4_phase_trajectories_worked: OIM Phase Trajectories
# ============================================================================

def fig_6_4_phase_trajectories():
    """
    Phase trajectories of 5 coupled OIM oscillators (v0-v4) over 0-100ms.
    v0, v1 converge to 0 (selected); v2, v3, v4 converge to pi (rejected).
    """
    np.random.seed(7)
    t = np.linspace(0, 100, 500)   # ms

    def converge(phi_target, phi0, tau=25, noise=0.06):
        """Exponential convergence with early noise."""
        signal = phi_target + (phi0 - phi_target) * np.exp(-t / tau)
        noise_term = noise * np.exp(-t / 15) * np.random.randn(len(t))
        return signal + noise_term

    PI = np.pi

    trajectories = {
        "v0 (selected)": converge(0,  np.random.uniform(0.3, 1.5), tau=20),
        "v1 (selected)": converge(0,  np.random.uniform(0.5, 2.0), tau=28),
        "v2 (rejected)": converge(PI, np.random.uniform(1.5, 2.5), tau=22),
        "v3 (rejected)": converge(PI, np.random.uniform(1.0, 2.0), tau=30),
        "v4 (rejected)": converge(PI, np.random.uniform(0.8, 1.8), tau=18),
    }

    selected_colors = [COLORS['blue'], '#2d96d4']
    rejected_colors = [COLORS['red'], '#e84c5a', '#c0392b']

    fig = go.Figure()

    # Shaded convergence zones
    fig.add_hrect(y0=-0.35, y1=0.35, fillcolor="rgba(26,127,55,0.12)",
                  line_width=0, annotation_text="0-phase zone",
                  annotation_position="right", annotation_font_size=11)
    fig.add_hrect(y0=PI - 0.35, y1=PI + 0.35, fillcolor="rgba(209,36,47,0.12)",
                  line_width=0, annotation_text="π-phase zone",
                  annotation_position="right", annotation_font_size=11)

    # Horizontal dashed reference lines
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['green'],
                  line_width=1.5, opacity=0.7)
    fig.add_hline(y=PI, line_dash="dash", line_color=COLORS['red'],
                  line_width=1.5, opacity=0.7)

    # Trajectories
    s_idx = 0
    r_idx = 0
    for name, traj in trajectories.items():
        if "selected" in name:
            color = selected_colors[s_idx % len(selected_colors)]
            s_idx += 1
        else:
            color = rejected_colors[r_idx % len(rejected_colors)]
            r_idx += 1

        fig.add_trace(go.Scatter(
            x=t, y=traj,
            mode="lines",
            name=name,
            line=dict(color=color, width=2.2),
        ))

    layout = dict(**BASE_LAYOUT)
    layout.update(
        width=850,
        height=380,
        xaxis=dict(
            title="Time (ms)",
            showgrid=True,
            gridcolor="#e8e8e8",
            showline=True,
            linecolor="#d0d7de",
            range=[0, 100],
        ),
        yaxis=dict(
            title="Oscillator Phase (rad)",
            showgrid=True,
            gridcolor="#e8e8e8",
            showline=True,
            linecolor="#d0d7de",
            tickvals=[0, PI/2, PI, 3*PI/2, 2*PI],
            ticktext=["0", "π/2", "π", "3π/2", "2π"],
            range=[-0.6, 2*PI + 0.3],
        ),
        legend=dict(
            x=0.75, y=0.98,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d0d7de",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=65, r=90, t=40, b=60),
    )
    fig.update_layout(**layout)

    save(fig, "fig_6_4_phase_trajectories_worked", width=850, height=380)


# ============================================================================
# FIG 3 — fig_2_2: Scalability Plot (conflict graph size vs robots)
# ============================================================================

def fig_2_2_scalability():
    """
    |V| (conflict graph nodes) vs Number of Robots N for three strategies.
    Log-Y axis. Shaded OIM hardware feasibility window (100–2000 nodes).
    """
    N = np.arange(2, 51)

    no_pruning     = 2 ** N                      # exponential
    coalition_k2   = N * (N - 1) / 2 * 4        # quadratic (k=2 coalitions)
    spatial_pruned = 2.8 * N * np.log(N + 1)    # near-linear

    # Clip to reasonable display range
    no_pruning = np.clip(no_pruning, None, 1e8)

    fig = go.Figure()

    # OIM feasibility band
    fig.add_hrect(y0=100, y1=2000,
                  fillcolor="rgba(26,111,175,0.08)",
                  line_width=0)

    # Annotation for the feasibility window
    fig.add_annotation(
        x=48, y=np.log10(450),
        xref="x", yref="y",
        text="OIM hardware<br>feasibility window<br>(100–2000 nodes)",
        showarrow=False,
        font=dict(size=10, color=COLORS['blue']),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor=COLORS['blue'],
        borderwidth=1,
        align="right",
    )

    fig.add_trace(go.Scatter(
        x=N, y=no_pruning,
        mode="lines",
        name="No pruning (exponential)",
        line=dict(color=COLORS['red'], width=2.5, dash="solid"),
    ))

    fig.add_trace(go.Scatter(
        x=N, y=coalition_k2,
        mode="lines",
        name="Coalition bounding k=2 (quadratic)",
        line=dict(color=COLORS['orange'], width=2.5, dash="dash"),
    ))

    fig.add_trace(go.Scatter(
        x=N, y=spatial_pruned,
        mode="lines",
        name="CB + Spatial pruning (near-linear)",
        line=dict(color=COLORS['green'], width=2.5, dash="dot"),
    ))

    layout = dict(**BASE_LAYOUT)
    layout.update(
        width=800,
        height=420,
        xaxis=dict(
            title="Number of Robots (N)",
            showgrid=True,
            gridcolor="#e8e8e8",
            showline=True,
            linecolor="#d0d7de",
            range=[2, 50],
        ),
        yaxis=dict(
            title="Conflict Graph Nodes |V|",
            type="log",
            showgrid=True,
            gridcolor="#e8e8e8",
            showline=True,
            linecolor="#d0d7de",
        ),
        legend=dict(
            x=0.03, y=0.97,
            bgcolor="rgba(255,255,255,0.93)",
            bordercolor="#d0d7de",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=65, r=40, t=40, b=60),
    )
    fig.update_layout(**layout)

    save(fig, "fig_2_2", width=800, height=420)


# ============================================================================
# FIG 4 — fig_3_4: Bits-to-Atoms Stack Diagram
# ============================================================================

def fig_3_4_bits_to_atoms_stack():
    """
    4-layer vertical architecture diagram using Plotly shapes + annotations.
    """
    W, H = 700, 550

    layers = [
        {
            "title": "Layer 4: Problem Formulation",
            "content": "Robot specs · utilities · task constraints",
            "side": "Application knowledge",
            "fill": "rgba(209, 36, 47, 0.18)",
            "border": COLORS['red'],
            "y0": 0.74, "y1": 0.95,
        },
        {
            "title": "Layer 3: Mathematical Encoding",
            "content": "Coalition→MWIS→QUBO→Ising  ·  Dynamics→MPC→QP→PIPG",
            "side": "Problem to Physics",
            "fill": "rgba(224, 123, 0, 0.18)",
            "border": COLORS['orange'],
            "y0": 0.50, "y1": 0.71,
        },
        {
            "title": "Layer 2: Neuromorphic Hardware",
            "content": "OIM (coupled oscillators)  ·  SNN (spiking neurons)",
            "side": "Co-design principle",
            "fill": "rgba(26, 111, 175, 0.18)",
            "border": COLORS['blue'],
            "y0": 0.26, "y1": 0.47,
        },
        {
            "title": "Layer 1: Physical World",
            "content": "Robots · tasks · real-time constraints (10–20 ms)",
            "side": "Constraints driving design",
            "fill": "rgba(26, 127, 55, 0.18)",
            "border": COLORS['green'],
            "y0": 0.02, "y1": 0.23,
        },
    ]

    shapes = []
    annotations = []

    for layer in layers:
        # Main box
        shapes.append(dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0.01, x1=0.72,
            y0=layer["y0"], y1=layer["y1"],
            fillcolor=layer["fill"],
            line=dict(color=layer["border"], width=2),
        ))

        # Side label box
        shapes.append(dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0.75, x1=0.99,
            y0=layer["y0"] + 0.04, y1=layer["y1"] - 0.04,
            fillcolor="rgba(246,248,250,0.95)",
            line=dict(color="#d0d7de", width=1),
        ))

        ymid = (layer["y0"] + layer["y1"]) / 2

        # Layer title
        annotations.append(dict(
            xref="paper", yref="paper",
            x=0.365, y=ymid + 0.05,
            text=f"<b>{layer['title']}</b>",
            showarrow=False,
            font=dict(family=FONT_FAMILY, size=13, color="#24292f"),
            align="center",
        ))

        # Layer content
        annotations.append(dict(
            xref="paper", yref="paper",
            x=0.365, y=ymid - 0.04,
            text=f"<i>{layer['content']}</i>",
            showarrow=False,
            font=dict(family=FONT_FAMILY, size=10, color=COLORS['gray']),
            align="center",
        ))

        # Side label text
        annotations.append(dict(
            xref="paper", yref="paper",
            x=0.87, y=ymid,
            text=layer["side"],
            showarrow=False,
            font=dict(family=FONT_FAMILY, size=11, color="#24292f"),
            align="center",
        ))

        # (arrows drawn separately via annotations below)

    # Arrow heads between layers using pixel-offset annotations
    for i in range(3):
        y_top = layers[i]["y0"]
        # Point at the gap between boxes; ax/ay are pixel offsets from x/y
        annotations.append(dict(
            xref="paper", yref="paper",
            x=0.365, y=y_top - 0.01,
            ax=0, ay=-30,         # pixel offsets: straight down
            axref="pixel", ayref="pixel",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowcolor="#24292f",
            arrowwidth=2,
            text="",
        ))

    fig = go.Figure()
    fig.update_layout(
        width=W, height=H,
        paper_bgcolor="white",
        plot_bgcolor="white",
        shapes=shapes,
        annotations=annotations,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        font=dict(family=FONT_FAMILY, size=13, color="#24292f"),
    )

    save(fig, "fig_3_4", width=W, height=H)


# ============================================================================
# FIG 5 — fig_7_2: OIM Scalability — Latency and Quality (dual-axis)
# ============================================================================

def fig_7_2_oim_scalability():
    """
    Dual Y-axis: Latency (ms) and Solution Quality ratio vs problem size (nodes).
    """
    nodes = np.array([10, 20, 50, 100, 150, 200, 300, 400, 500])
    latency = np.array([0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19])
    quality = np.array([0.92, 0.91, 0.90, 0.90, 0.89, 0.89, 0.88, 0.87, 0.85])

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=nodes, y=latency,
            mode="lines+markers",
            name="Latency (ms)",
            line=dict(color=COLORS['blue'], width=2.5),
            marker=dict(symbol="circle", size=9, color=COLORS['blue'],
                        line=dict(color="white", width=1.5)),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=nodes, y=quality,
            mode="lines+markers",
            name="Solution Quality Ratio",
            line=dict(color=COLORS['orange'], width=2.5, dash="dash"),
            marker=dict(symbol="diamond", size=9, color=COLORS['orange'],
                        line=dict(color="white", width=1.5)),
        ),
        secondary_y=True,
    )

    # Annotation at key points
    fig.add_annotation(
        x=100, y=0.14,
        xref="x", yref="y",
        text="0.14 ms<br>(100 nodes)",
        showarrow=True, arrowhead=2,
        ax=40, ay=-30,
        font=dict(size=10, color=COLORS['blue']),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor=COLORS['blue'],
        borderwidth=1,
    )

    fig.update_layout(
        font=dict(family=FONT_FAMILY, size=13, color="#24292f"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        width=800,
        height=420,
        margin=dict(l=70, r=80, t=50, b=65),
        legend=dict(
            x=0.5, y=0.97,
            xanchor="center",
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#d0d7de",
            borderwidth=1,
            font=dict(size=11),
            orientation="h",
        ),
    )

    fig.update_yaxes(
        title_text="Latency (ms)",
        secondary_y=False,
        gridcolor="#e8e8e8",
        showline=True,
        linecolor="#d0d7de",
        range=[0.10, 0.21],
        tickformat=".2f",
    )
    fig.update_yaxes(
        title_text="Solution Quality Ratio",
        secondary_y=True,
        gridcolor=None,
        showgrid=False,
        showline=True,
        linecolor="#d0d7de",
        range=[0.83, 0.95],
        tickformat=".2f",
    )
    fig.update_xaxes(
        title_text="Problem Size (nodes)",
        showgrid=True,
        gridcolor="#e8e8e8",
        showline=True,
        linecolor="#d0d7de",
    )

    save(fig, "fig_7_2", width=800, height=420)


# ============================================================================
# FIG 6 — fig_8_1 / fig_7_1_india_ecosystem: India Growth Opportunity
# ============================================================================

def fig_8_1_india_growth():
    """
    Market size (Billion USD) vs Year 2026-2035.
    Three lines: Global neuromorphic, India opportunity, India manufacturing.
    Shaded area for global market.
    """
    years = np.arange(2026, 2036)

    global_market = np.array([1.2, 1.6, 2.2, 3.0, 4.1, 5.5, 7.2, 9.4, 12.0, 15.2])
    india_opp     = np.array([0.05, 0.08, 0.13, 0.22, 0.36, 0.56, 0.82, 1.15, 1.55, 2.10])
    india_mfg     = np.array([0.01, 0.02, 0.04, 0.08, 0.14, 0.22, 0.35, 0.52, 0.74, 1.05])

    fig = go.Figure()

    # Shaded global market area
    fig.add_trace(go.Scatter(
        x=list(years) + list(years[::-1]),
        y=list(global_market) + [0]*len(years),
        fill="toself",
        fillcolor="rgba(87,96,106,0.12)",
        line=dict(color="rgba(87,96,106,0)"),
        showlegend=False,
        hoverinfo="skip",
    ))

    fig.add_trace(go.Scatter(
        x=years, y=global_market,
        mode="lines+markers",
        name="Global neuromorphic market",
        line=dict(color=COLORS['gray'], width=2.5),
        marker=dict(symbol="circle", size=8, color=COLORS['gray']),
    ))

    fig.add_trace(go.Scatter(
        x=years, y=india_opp,
        mode="lines+markers",
        name="India opportunity",
        line=dict(color=COLORS['blue'], width=2.5),
        marker=dict(symbol="square", size=8, color=COLORS['blue']),
    ))

    fig.add_trace(go.Scatter(
        x=years, y=india_mfg,
        mode="lines+markers",
        name="India manufacturing capacity",
        line=dict(color=COLORS['green'], width=2.5, dash="dash"),
        marker=dict(symbol="diamond", size=8, color=COLORS['green']),
    ))

    # Endpoint annotations
    endpoint_data = [
        (2035, global_market[-1], f"${global_market[-1]:.1f}B", COLORS['gray'], "middle right"),
        (2035, india_opp[-1],     f"${india_opp[-1]:.2f}B",     COLORS['blue'],  "middle right"),
        (2035, india_mfg[-1],     f"${india_mfg[-1]:.2f}B",     COLORS['green'], "middle right"),
    ]
    for xv, yv, label, color, _ in endpoint_data:
        fig.add_annotation(
            x=xv + 0.2, y=yv,
            text=label,
            showarrow=False,
            font=dict(size=10, color=color, family=FONT_FAMILY),
            xanchor="left",
        )

    layout = dict(**BASE_LAYOUT)
    layout.update(
        width=850,
        height=420,
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor="#e8e8e8",
            showline=True,
            linecolor="#d0d7de",
            dtick=1,
        ),
        yaxis=dict(
            title="Market Size (Billion USD)",
            showgrid=True,
            gridcolor="#e8e8e8",
            showline=True,
            linecolor="#d0d7de",
            tickprefix="$",
            ticksuffix="B",
        ),
        legend=dict(
            x=0.03, y=0.97,
            bgcolor="rgba(255,255,255,0.93)",
            bordercolor="#d0d7de",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=65, r=80, t=40, b=60),
    )
    fig.update_layout(**layout)

    # Save as fig_8_1 (used in conclusion chapter)
    save(fig, "fig_8_1", width=850, height=420)

    # Also save as fig_7_1_india_ecosystem.png (referenced in India chapter)
    png_path = os.path.join(OUT, "fig_7_1_india_ecosystem.png")
    fig.write_image(png_path, width=850, height=420, scale=2)
    print(f"  Also saved fig_7_1_india_ecosystem.png")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("REBUILDING 6 BAD THESIS FIGURES WITH PLOTLY + KALEIDO")
    print("=" * 60 + "\n")

    print("1. fig_1_5 — Three Computational Paradigms")
    fig_1_5_computational_paradigms()

    print("2. fig_6_4_phase_trajectories_worked — OIM Phase Trajectories")
    fig_6_4_phase_trajectories()

    print("3. fig_2_2 — Scalability Plot")
    fig_2_2_scalability()

    print("4. fig_3_4 — Bits-to-Atoms Stack")
    fig_3_4_bits_to_atoms_stack()

    print("5. fig_7_2 — OIM Scalability Dual-Axis")
    fig_7_2_oim_scalability()

    print("6. fig_8_1 / fig_7_1_india_ecosystem — India Growth Opportunity")
    fig_8_1_india_growth()

    print("\n" + "=" * 60)
    print("ALL 6 FIGURES REBUILT SUCCESSFULLY")
    print("=" * 60 + "\n")
