from __future__ import annotations

import math
import random
from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Sequence

import numpy as np

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult

# Problems with more nodes than this use the numpy-vectorized step
_NP_THRESHOLD = 40


@dataclass(frozen=True)
class KuramotoConfig:
    restarts: int = 8
    steps: int = 280
    dt: float = 0.035
    kinj_min: float = 0.15
    kinj_max: float = 3.4
    coupling_gain: float = 1.0
    bias_gain: float = 0.55
    noise_amp: float = 0.04
    noise_cooling: float = 0.995


@dataclass(frozen=True)
class KuramotoContext:
    weights: tuple[float, ...]
    degrees: tuple[int, ...]
    adjacency: tuple[tuple[int, ...], ...]
    lambda_penalty: float


KuramotoStepFunction = Callable[
    [Sequence[float], KuramotoContext, KuramotoConfig, random.Random, float, float],
    list[float],
]


def _wrap(theta: float) -> float:
    return ((theta % (2 * math.pi)) + 2 * math.pi) % (2 * math.pi)


def _spin(theta: float) -> int:
    return 1 if math.cos(theta) >= 0 else -1


def _decode(theta: Sequence[float]) -> list[int]:
    return [i for i, t in enumerate(theta) if _spin(t) > 0]


def _repair_feasible(problem: MWISProblem, selected: list[int]) -> list[int]:
    chosen = set(selected)
    changed = True
    while changed:
        changed = False
        for i in list(chosen):
            for j in problem.adjacency[i]:
                if j in chosen:
                    wi = problem.nodes[i].utility
                    wj = problem.nodes[j].utility
                    if wi >= wj:
                        chosen.remove(j)
                    else:
                        chosen.remove(i)
                    changed = True
                    break
            if changed:
                break
    return sorted(chosen)


def kuramoto_injected_step(
    theta: Sequence[float],
    context: KuramotoContext,
    cfg: KuramotoConfig,
    rng: random.Random,
    step_ratio: float,
    noise_amp: float,
) -> list[float]:
    # Correct OIM dynamics derived from QUBO → Ising → OIM mapping:
    #   QUBO:  Q(x) = -Σ wᵢ xᵢ + λ Σ_{(i,j)∈E} xᵢ xⱼ
    #   Ising: H = -Σ hᵢ sᵢ + Σ Jᵢⱼ sᵢ sⱼ
    #          hᵢ = wᵢ/2 - λ·deg(i)/4,   Jᵢⱼ = λ/4
    #   OIM:   dθᵢ/dt = Kᵢᵢ sin(2θᵢ) + Σⱼ Kᵢⱼ sin(θⱼ - θᵢ)
    #          Kᵢᵢ = -hᵢ  (K<0 for selectable nodes → stable attractors at θ=0 AND θ=π)
    #          Kᵢⱼ = -2Jᵢⱼ = -λ/2  (K<0 → anti-ferromagnetic in Lyapunov energy)
    #
    # Lyapunov function: V = Σ Kᵢᵢ cos(2θᵢ)/2 + Σ_{i<j} Kᵢⱼ cos(θⱼ-θᵢ)
    #   Kᵢᵢ < 0  → minima of injection at θ=0 (selected) and θ=π (not selected)
    #   Kᵢⱼ < 0  → minimum of coupling at θⱼ-θᵢ=π (anti-aligned = anti-ferromagnetic)
    #   Anti-ferromagnetic dominates when |Kᵢᵢ| >> |Kᵢⱼ|, which holds for high-utility nodes.

    dtheta: list[float] = []
    lam = context.lambda_penalty
    K_couple = -lam / 2.0  # anti-ferromagnetic coupling for conflict edges

    for i, t_i in enumerate(theta):
        # Ising field: h_i = -w_i/2 + λ·deg_i/4  (negative utility + connectivity penalty)
        # OIM injection: K_ii = -h_i = w_i/2 - λ·deg_i/4
        # For the 3R2T instance with λ=8, all nodes have K_ii < 0:
        # → stable Lyapunov attractors at θ=0 (selected) and θ=π (rejected)
        K_ii = context.weights[i] / 2.0 - lam * context.degrees[i] / 4.0
        d = K_ii * math.sin(2.0 * t_i)

        # Coupling: K_ij = -λ/2 for all conflict edges (anti-ferromagnetic)
        # Lyapunov V_couple = Σ K_ij·cos(θⱼ-θᵢ): K_ij<0 → minimum at θⱼ-θᵢ=π ✓
        for j in context.adjacency[i]:
            d += K_couple * math.sin(theta[j] - t_i)

        d += (rng.random() * 2.0 - 1.0) * noise_amp
        dtheta.append(d)

    return dtheta


def _solve_kuramoto_numpy(
    problem: MWISProblem,
    cfg: KuramotoConfig,
    rng: random.Random,
) -> tuple[list[int], float]:
    """Numpy-vectorised Kuramoto solver for large graphs.

    Same dynamics as the scalar version; uses numpy for O(n²) matrix ops
    instead of Python loops — roughly 100× faster for n > 100.
    """
    n = problem.node_count
    weights = np.array([node.utility for node in problem.nodes], dtype=np.float64)
    degrees = np.array([len(problem.adjacency[i]) for i in range(n)], dtype=np.float64)

    # Dense adjacency matrix (float, 0/1) — for n=563 this is ~2.5 MB: fine
    adj = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in problem.adjacency[i]:
            adj[i, j] = 1.0

    lam = problem.lambda_penalty
    K_ii = weights / 2.0 - lam * degrees / 4.0   # injection strengths
    K_couple = -lam / 2.0                          # anti-ferromagnetic coupling

    nprng = np.random.default_rng(rng.randint(0, 2**31))

    best_selected: list[int] = []
    best_utility = -1.0

    for _ in range(cfg.restarts):
        theta = nprng.uniform(0, 2 * np.pi, n)
        noise_amp = cfg.noise_amp

        for step in range(cfg.steps):
            sin_t = np.sin(theta)
            cos_t = np.cos(theta)
            # d_inj[i] = K_ii[i] * sin(2*theta[i])
            d_inj = K_ii * np.sin(2.0 * theta)
            # d_couple[i] = K_couple * Σ_j adj[i,j] * sin(theta[j] - theta[i])
            #             = K_couple * (cos_t[i] * (adj @ sin_t) - sin_t[i] * (adj @ cos_t))
            adj_sin = adj @ sin_t
            adj_cos = adj @ cos_t
            d_couple = K_couple * (cos_t * adj_sin - sin_t * adj_cos)
            noise = nprng.uniform(-1, 1, n) * noise_amp
            theta = (theta + cfg.dt * (d_inj + d_couple + noise)) % (2 * np.pi)
            noise_amp *= cfg.noise_cooling

        # Decode: cos(theta) >= 0 → selected
        selected_raw = [i for i in range(n) if np.cos(theta[i]) >= 0]
        selected = _repair_feasible(problem, selected_raw)
        util = selection_utility(problem, selected)
        if util > best_utility:
            best_utility = util
            best_selected = selected

    return best_selected, max(0.0, best_utility)


def solve_kuramoto_oim(
    problem: MWISProblem,
    config: KuramotoConfig | None = None,
    seed: int = 0,
    step_fn: KuramotoStepFunction = kuramoto_injected_step,
) -> SolverResult:
    cfg = config or KuramotoConfig()
    start = perf_counter()
    rng = random.Random(seed)

    if problem.node_count > _NP_THRESHOLD:
        best_selected, best_utility = _solve_kuramoto_numpy(problem, cfg, rng)
        runtime_ms = (perf_counter() - start) * 1000
        return SolverResult(
            name="kuramoto_oim",
            selected=best_selected,
            utility=best_utility,
            feasible=selection_is_feasible(problem, best_selected),
            runtime_ms=runtime_ms,
            metadata={"restarts": cfg.restarts, "steps": cfg.steps,
                      "dt": cfg.dt, "backend": "numpy"},
        )

    weights = tuple(node.utility for node in problem.nodes)
    degrees = tuple(len(problem.adjacency[i]) for i in range(problem.node_count))
    adjacency = tuple(tuple(problem.adjacency[i]) for i in range(problem.node_count))
    context = KuramotoContext(
        weights=weights,
        degrees=degrees,
        adjacency=adjacency,
        lambda_penalty=problem.lambda_penalty,
    )

    best_selected: list[int] = []
    best_utility = -1.0

    for _ in range(cfg.restarts):
        theta = [rng.random() * 2.0 * math.pi for _ in range(problem.node_count)]
        noise = cfg.noise_amp

        for step in range(cfg.steps):
            ratio = step / max(1, cfg.steps - 1)
            dtheta = step_fn(theta, context, cfg, rng, ratio, noise)
            theta = [_wrap(t + cfg.dt * dt) for t, dt in zip(theta, dtheta, strict=True)]
            noise *= cfg.noise_cooling

        selected = _repair_feasible(problem, _decode(theta))
        util = selection_utility(problem, selected)
        if util > best_utility:
            best_utility = util
            best_selected = selected

    runtime_ms = (perf_counter() - start) * 1000
    return SolverResult(
        name="kuramoto_oim",
        selected=best_selected,
        utility=max(0.0, best_utility),
        feasible=selection_is_feasible(problem, best_selected),
        runtime_ms=runtime_ms,
        metadata={
            "restarts": cfg.restarts,
            "steps": cfg.steps,
            "dt": cfg.dt,
        },
    )
