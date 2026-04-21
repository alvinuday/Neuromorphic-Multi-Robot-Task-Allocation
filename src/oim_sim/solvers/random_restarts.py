from __future__ import annotations

import random
from time import perf_counter

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


def solve_random_restarts(problem: MWISProblem, restarts: int = 80, seed: int = 0) -> SolverResult:
    start = perf_counter()
    rng = random.Random(seed)

    best_sel: list[int] = []
    best_util = 0.0

    for _ in range(restarts):
        order = list(range(problem.node_count))
        rng.shuffle(order)
        selected: list[int] = []
        chosen = set()
        blocked = set()

        for idx in order:
            if idx in blocked:
                continue
            selected.append(idx)
            chosen.add(idx)
            blocked.add(idx)
            blocked.update(problem.adjacency[idx])

        util = selection_utility(problem, selected)
        if util > best_util:
            best_util = util
            best_sel = selected

    runtime_ms = (perf_counter() - start) * 1000
    return SolverResult(
        name="random_restarts",
        selected=best_sel,
        utility=best_util,
        feasible=selection_is_feasible(problem, best_sel),
        runtime_ms=runtime_ms,
        metadata={"restarts": restarts},
    )
