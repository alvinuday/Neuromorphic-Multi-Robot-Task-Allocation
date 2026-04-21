from __future__ import annotations

import math
import random
from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Sequence

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


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
    kinj = cfg.kinj_min + (cfg.kinj_max - cfg.kinj_min) * step_ratio
    dtheta: list[float] = []

    for i, t_i in enumerate(theta):
        d = kinj * math.sin(2.0 * t_i)

        for j in context.adjacency[i]:
            kij = cfg.coupling_gain * (context.lambda_penalty / 10.0)
            d += kij * math.sin(theta[j] - t_i - math.pi)

        local_field = cfg.bias_gain * (
            context.weights[i] - (0.32 * context.lambda_penalty * context.degrees[i])
        )
        d += local_field * (-math.sin(t_i))
        d += (rng.random() * 2.0 - 1.0) * noise_amp
        dtheta.append(d)

    return dtheta


def solve_kuramoto_oim(
    problem: MWISProblem,
    config: KuramotoConfig | None = None,
    seed: int = 0,
    step_fn: KuramotoStepFunction = kuramoto_injected_step,
) -> SolverResult:
    cfg = config or KuramotoConfig()
    start = perf_counter()
    rng = random.Random(seed)

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
