"""
Fixed OIM Dynamics Simulator

Implements the correct Oscillator Ising Machine (OIM) dynamics with proper sign
conventions for solving QUBO-encoded MWIS problems via coupled oscillator dynamics.

Core dynamics (Blueprint §4.6):
    dθᵢ/dt = Kᵢᵢ·sin(2θᵢ) + Σⱼ Kᵢⱼ·sin(θⱼ - θᵢ) + ξᵢ(t)

Key sign convention (Blueprint §4.5-4.6):
    Kᵢⱼ = -2·Jᵢⱼ  (anti-ferromagnetic coupling for conflict edges)
    Iᵢ = -hᵢ     (external injection current proportional to negative bias)

This ensures:
- Conflict edges (Jᵢⱼ > 0) → Kᵢⱼ < 0 → oscillators prefer phases π apart
- High-utility nodes (hᵢ > 0) → Iᵢ < 0 → injection pulls toward phase 0 (+1 spin)
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Sequence

import numpy as np


@dataclass(frozen=True)
class OIMConfig:
    """Configuration for OIM dynamics simulation.

    Attributes:
        restarts: Number of random initializations (≥5 recommended)
        steps: Number of integration steps per run
        dt: Integration time step
        noise_amplitude: Initial noise strength (annealed over time)
        noise_cooling_rate: Multiplicative cooling factor per step (0.99-0.999)
        threshold_phase: Phase threshold for binarization (typically π/2)
    """
    restarts: int = 5
    steps: int = 400
    dt: float = 0.02
    noise_amplitude: float = 0.1
    noise_cooling_rate: float = 0.998
    threshold_phase: float = math.pi / 2


@dataclass(frozen=True)
class OIMContext:
    """Pre-computed context for OIM dynamics evaluation.

    Attributes:
        h_bias: External field h_k for each node (size N)
        K_coupling: Full coupling matrix K_ij (size N×N)
        adjacency: Adjacency list of conflict edges (for sparse computation)
        node_count: Number of nodes/oscillators
    """
    h_bias: np.ndarray  # shape (N,)
    K_coupling: np.ndarray  # shape (N, N)
    adjacency: tuple[tuple[int, ...], ...]  # adjacency[i] = neighbors of i
    node_count: int


def _binarize_phases(phases: np.ndarray, threshold: float = math.pi / 2) -> list[int]:
    """Convert phases to binary spins via threshold.

    Args:
        phases: Array of phases in [0, 2π)
        threshold: Phase cutoff (default π/2)

    Returns:
        List of spins {-1, +1}: +1 if phase < threshold, -1 otherwise
    """
    return [1 if math.cos(p) >= 0 else -1 for p in phases]


def _decode_to_indices(phases: np.ndarray, threshold: float = math.pi / 2) -> list[int]:
    """Decode phases to selected node indices (where spin ≈ +1).

    Args:
        phases: Array of phases in [0, 2π)
        threshold: Phase threshold

    Returns:
        List of indices i where spin_i ≈ +1 (selected)
    """
    return [i for i, p in enumerate(phases) if math.cos(p) >= 0]


def _repair_feasible(selected: list[int], adjacency: tuple[tuple[int, ...], ...],
                    utilities: np.ndarray) -> list[int]:
    """Greedy repair of infeasible solutions (maximal independent set).

    Removes nodes from conflicts by iteratively removing the lower-utility node
    in each conflicting pair.

    Args:
        selected: List of selected node indices
        adjacency: Adjacency list of conflicts
        utilities: Node utility weights

    Returns:
        Feasible (independent) set with greedy repair
    """
    chosen = set(selected)
    changed = True

    while changed:
        changed = False
        for i in list(chosen):
            for j in adjacency[i]:
                if j in chosen:
                    # Remove lower-utility node
                    if utilities[i] >= utilities[j]:
                        chosen.discard(j)
                    else:
                        chosen.discard(i)
                    changed = True
                    break
            if changed:
                break

    return sorted(chosen)


def oim_dynamics_step(
    phases: np.ndarray,
    context: OIMContext,
    noise_amp: float
) -> np.ndarray:
    """Single OIM dynamics step (explicit Euler integration).

    Computes dθᵢ/dt for each oscillator using the corrected OIM equation:
        dθᵢ/dt = Kᵢᵢ·sin(2θᵢ) + Σⱼ Kᵢⱼ·sin(θⱼ - θᵢ) + ξᵢ(t)

    Args:
        phases: Current phase array (size N)
        context: OIM parameters (coupling matrix, bias)
        noise_amp: Current noise amplitude

    Returns:
        Phase derivatives dθ/dt (size N)
    """
    N = context.node_count
    dtheta = np.zeros(N)

    for i in range(N):
        # Injection locking term: K_ii * sin(2*theta_i)
        # Note: K_ii encodes the bias; higher utility → more negative K_ii → pulls to 0
        dtheta[i] = context.K_coupling[i, i] * math.sin(2.0 * phases[i])

        # Coupling term: sum_j K_ij * sin(theta_j - theta_i)
        # For conflict edges: K_ij < 0 (anti-ferromagnetic)
        for j in context.adjacency[i]:
            dtheta[i] += context.K_coupling[i, j] * math.sin(phases[j] - phases[i])

        # Random noise for escaping local minima
        dtheta[i] += (2.0 * random.random() - 1.0) * noise_amp

    return dtheta


def solve_oim_dynamics(
    h_bias: np.ndarray,
    K_coupling: np.ndarray,
    utilities: np.ndarray,
    adjacency: tuple[tuple[int, ...], ...],
    config: OIMConfig | None = None,
    seed: int = 0,
) -> tuple[list[int], float, dict]:
    """Solve MWIS via OIM dynamics with multi-start and best selection.

    Runs multiple random initializations of the OIM dynamics, each evolving for
    `steps` integration steps with noise annealing. Returns the best feasible
    solution found.

    Args:
        h_bias: External field h_k from Ising mapping (size N)
        K_coupling: Coupling matrix K_ij (size N×N)
        utilities: Node weights w_v for tie-breaking (size N)
        adjacency: Conflict edges as adjacency list
        config: OIMConfig with simulation parameters
        seed: Random seed

    Returns:
        (selected_indices, max_utility, metadata_dict)
            - selected_indices: Best feasible solution found
            - max_utility: Total utility of solution
            - metadata_dict: Convergence/timing info
    """
    cfg = config or OIMConfig()
    start_time = perf_counter()
    rng = random.Random(seed)
    np.random.seed(seed)

    N = len(h_bias)
    # Set diagonal of K_coupling from injection bias: K_ii = I_bias_i = -h_i
    # This encodes the node-selection preference from the Ising field h_i.
    # Without this, K_ii=0 and the injection term is absent from dynamics.
    K_coupling_full = K_coupling.copy()
    for i in range(N):
        K_coupling_full[i, i] = -h_bias[i]

    context = OIMContext(
        h_bias=h_bias,
        K_coupling=K_coupling_full,
        adjacency=adjacency,
        node_count=N,
    )

    best_selected = []
    best_utility = -1.0
    run_history = []

    for restart_idx in range(cfg.restarts):
        # Random initialization: uniform phases in [0, 2π)
        phases = np.array([rng.random() * 2.0 * math.pi for _ in range(N)])
        noise_amp = cfg.noise_amplitude
        phase_history = [phases.copy()]

        # Integration loop with noise annealing
        for step in range(cfg.steps):
            dtheta = oim_dynamics_step(phases, context, noise_amp)
            phases = phases + cfg.dt * dtheta

            # Wrap phases to [0, 2π)
            phases = np.mod(phases, 2.0 * math.pi)

            # Noise annealing
            noise_amp *= cfg.noise_cooling_rate
            phase_history.append(phases.copy())

        # Binarize and repair
        selected = _decode_to_indices(phases)
        selected = _repair_feasible(selected, adjacency, utilities)

        # Compute utility
        util = float(np.sum(utilities[selected])) if selected else 0.0

        # Track best
        if util > best_utility:
            best_utility = util
            best_selected = selected

        run_history.append({
            'restart': restart_idx,
            'selected_count': len(selected),
            'utility': util,
            'feasible': True,  # Repair guarantees feasibility
        })

    runtime_ms = (perf_counter() - start_time) * 1000.0

    metadata = {
        'restarts': cfg.restarts,
        'steps': cfg.steps,
        'dt': cfg.dt,
        'runtime_ms': runtime_ms,
        'best_restart': run_history.index(
            max(run_history, key=lambda x: x['utility'])
        ) if run_history else 0,
        'run_history': run_history,
    }

    return best_selected, max(0.0, best_utility), metadata
