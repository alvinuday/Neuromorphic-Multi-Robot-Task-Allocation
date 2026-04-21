from __future__ import annotations

from time import perf_counter

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


def solve_exact_bruteforce(problem: MWISProblem, max_nodes: int = 24) -> SolverResult:
    start = perf_counter()
    n = problem.node_count
    if n > max_nodes:
        raise ValueError(f"exact brute-force disabled for n={n} > {max_nodes}")

    best_sel: list[int] = []
    best_utility = 0.0

    for mask in range(1 << n):
        selected = [i for i in range(n) if (mask >> i) & 1]
        if not selection_is_feasible(problem, selected):
            continue
        util = selection_utility(problem, selected)
        if util > best_utility:
            best_utility = util
            best_sel = selected

    runtime_ms = (perf_counter() - start) * 1000
    return SolverResult(
        name="exact_bruteforce",
        selected=best_sel,
        utility=best_utility,
        feasible=True,
        runtime_ms=runtime_ms,
    )
