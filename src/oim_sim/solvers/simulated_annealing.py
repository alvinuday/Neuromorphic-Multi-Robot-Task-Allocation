from __future__ import annotations

import math
import random
from time import perf_counter

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


def _energy(problem: MWISProblem, x: list[int]) -> float:
    reward = sum(problem.nodes[i].utility * x[i] for i in range(problem.node_count))
    conflicts = 0.0
    for i in range(problem.node_count):
        if x[i] == 0:
            continue
        for j in problem.adjacency[i]:
            if j > i and x[j] == 1:
                conflicts += 1.0
    return -reward + problem.lambda_penalty * conflicts


def _decode(x: list[int]) -> list[int]:
    return [i for i, bit in enumerate(x) if bit == 1]


def _repair(problem: MWISProblem, selected: list[int]) -> list[int]:
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


def solve_simulated_annealing(
    problem: MWISProblem,
    steps: int = 3000,
    t_start: float = 3.0,
    t_end: float = 0.02,
    seed: int = 0,
) -> SolverResult:
    start = perf_counter()
    rng = random.Random(seed)
    n = problem.node_count

    x = [rng.randint(0, 1) for _ in range(n)]
    e = _energy(problem, x)
    best_x = x[:]
    best_e = e

    for k in range(steps):
        t = t_start * ((t_end / t_start) ** (k / max(1, steps - 1)))
        idx = rng.randrange(n)
        x[idx] ^= 1
        e_new = _energy(problem, x)
        delta = e_new - e
        if delta < 0 or rng.random() < math.exp(-delta / max(1e-9, t)):
            e = e_new
            if e < best_e:
                best_e = e
                best_x = x[:]
        else:
            x[idx] ^= 1

    selected = _repair(problem, _decode(best_x))
    runtime_ms = (perf_counter() - start) * 1000
    return SolverResult(
        name="simulated_annealing",
        selected=selected,
        utility=selection_utility(problem, selected),
        feasible=selection_is_feasible(problem, selected),
        runtime_ms=runtime_ms,
        metadata={"steps": steps, "t_start": t_start, "t_end": t_end},
    )
