from __future__ import annotations

import random
from typing import Sequence

from oim_sim.mrta import build_mwis_problem, selection_is_feasible
from oim_sim.solvers import KuramotoConfig, KuramotoContext, solve_kuramoto_oim
from oim_sim.types import MRTAInstance, Robot, Task


def _instance() -> MRTAInstance:
    robots = (
        Robot(id=0, capabilities=(2.1, 0.2), position=(0.1, 0.1)),
        Robot(id=1, capabilities=(1.4, 0.8), position=(0.2, 0.2)),
        Robot(id=2, capabilities=(0.4, 1.8), position=(0.8, 0.9)),
        Robot(id=3, capabilities=(0.2, 1.6), position=(0.7, 0.8)),
    )
    tasks = (
        Task(id=0, requirements=(2.8, 0.8), value=6.2, position=(0.12, 0.12)),
        Task(id=1, requirements=(0.5, 2.5), value=5.8, position=(0.75, 0.85)),
    )
    return MRTAInstance(name="kuramoto_case", robots=robots, tasks=tasks)


def _frozen_step(
    theta: Sequence[float],
    context: KuramotoContext,
    cfg: KuramotoConfig,
    rng: random.Random,
    step_ratio: float,
    noise_amp: float,
) -> list[float]:
    _ = (context, cfg, rng, step_ratio, noise_amp)
    return [0.0 for _ in theta]


def test_kuramoto_solver_default_and_modular_step() -> None:
    problem = build_mwis_problem(_instance(), coalition_bound=2, lambda_penalty=11.0)

    default_res = solve_kuramoto_oim(problem, seed=42)
    assert default_res.feasible
    assert selection_is_feasible(problem, default_res.selected)

    swapped_res = solve_kuramoto_oim(
        problem,
        config=KuramotoConfig(restarts=2, steps=8, dt=0.03),
        seed=1,
        step_fn=_frozen_step,
    )
    assert swapped_res.feasible
    assert selection_is_feasible(problem, swapped_res.selected)
