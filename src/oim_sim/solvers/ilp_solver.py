"""
Integer Linear Programming solver for Maximum Weighted Independent Set (MWIS).
Uses PuLP with CBC solver backend.
"""
from __future__ import annotations

from time import perf_counter
from typing import Optional

try:
    import pulp
except ImportError:
    pulp = None

from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


def solve_ilp_mwis(problem: MWISProblem, timeout_sec: float = 30.0) -> SolverResult:
    """
    Solve MWIS using Integer Linear Programming.

    Formulation:
        max Σᵢ wᵢ·xᵢ
        subject to: xᵢ + xⱼ ≤ 1 for all (i,j) ∈ E
                   xᵢ ∈ {0, 1}

    Args:
        problem: MWISProblem instance
        timeout_sec: Time limit for solver (default 30s)

    Returns:
        SolverResult with solution quality and runtime
    """
    start = perf_counter()

    if pulp is None:
        # Fallback to greedy if PuLP not available
        from .greedy import solve_greedy_mwis
        return solve_greedy_mwis(problem)

    # Create LP problem
    lp_problem = pulp.LpProblem("MWIS", pulp.LpMaximize)

    # Decision variables: xᵢ ∈ {0, 1}
    x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(problem.node_count)]

    # Objective: maximize total utility
    lp_problem += pulp.lpSum(problem.nodes[i].utility * x[i] for i in range(problem.node_count))

    # Constraints: xᵢ + xⱼ ≤ 1 for each conflict edge (i,j)
    for edge in problem.edges:
        lp_problem += x[edge.u] + x[edge.v] <= 1, f"conflict_{edge.u}_{edge.v}"

    # Solve with timeout
    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=timeout_sec)
    lp_problem.solve(solver)

    # Extract solution
    selected = [i for i in range(problem.node_count) if x[i].varValue and x[i].varValue > 0.5]

    runtime_ms = (perf_counter() - start) * 1000

    return SolverResult(
        name="ilp_mwis",
        selected=selected,
        utility=selection_utility(problem, selected),
        feasible=selection_is_feasible(problem, selected),
        runtime_ms=runtime_ms,
        metadata={
            "solver_status": str(pulp.LpStatus[lp_problem.status]),
            "lp_relaxation_bound": lp_problem.objective.value() if lp_problem.status == 1 else None,
        }
    )
