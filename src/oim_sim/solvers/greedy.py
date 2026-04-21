from __future__ import annotations

from time import perf_counter

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


def solve_greedy_mwis(problem: MWISProblem) -> SolverResult:
    start = perf_counter()
    order = sorted(range(problem.node_count), key=lambda i: problem.nodes[i].utility, reverse=True)

    selected: list[int] = []
    blocked: set[int] = set()
    for idx in order:
        if idx in blocked:
            continue
        selected.append(idx)
        blocked.add(idx)
        blocked.update(problem.adjacency[idx])

    runtime_ms = (perf_counter() - start) * 1000
    return SolverResult(
        name="greedy_mwis",
        selected=selected,
        utility=selection_utility(problem, selected),
        feasible=selection_is_feasible(problem, selected),
        runtime_ms=runtime_ms,
    )
