"""
Branch and Bound solver for Maximum Weighted Independent Set (MWIS).
Uses LP relaxation for bounding, depth-first search with pruning.
"""
from __future__ import annotations

from time import perf_counter
from dataclasses import dataclass
from typing import Optional


from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


@dataclass
class Node:
    """Branch-and-bound tree node."""
    selected: set[int]
    excluded: set[int]
    lower_bound: float
    upper_bound: float


def _greedy_upper_bound(problem: MWISProblem, selected: set[int], excluded: set[int]) -> float:
    """Compute greedy upper bound on remaining nodes."""
    remaining = set(range(problem.node_count)) - selected - excluded
    bound = sum(problem.nodes[i].utility for i in selected)

    # Greedy selection on remaining nodes
    candidates = sorted(remaining, key=lambda i: problem.nodes[i].utility, reverse=True)
    temp_selected = set(selected)
    for i in candidates:
        if i not in excluded and all(j not in temp_selected for j in problem.adjacency[i]):
            temp_selected.add(i)
            bound += problem.nodes[i].utility

    return bound


def _lp_upper_bound(problem: MWISProblem, selected: set[int], excluded: set[int]) -> float:
    """
    Compute LP relaxation upper bound.
    Simple version: sum of utilities of selected + fractional values for remaining.
    """
    remaining = set(range(problem.node_count)) - selected - excluded
    bound = sum(problem.nodes[i].utility for i in selected)

    # For remaining nodes, compute LP relaxation
    # x_i ∈ [0, 1], with constraints from selected nodes
    for i in remaining:
        # If i conflicts with any selected node, x_i = 0
        if any(j in selected and j in problem.adjacency[i] for j in selected):
            continue
        # Otherwise, x_i can be at most 1
        bound += problem.nodes[i].utility

    return bound


def solve_branch_and_bound(problem: MWISProblem, timeout_sec: float = 30.0) -> SolverResult:
    """
    Solve MWIS using branch-and-bound with LP relaxation bounding.

    Args:
        problem: MWISProblem instance
        timeout_sec: Time limit for solver (default 30s)

    Returns:
        SolverResult with solution quality and runtime
    """
    start = perf_counter()
    best_solution = []
    best_value = 0.0
    nodes_explored = 0

    def is_timeout() -> bool:
        return (perf_counter() - start) > timeout_sec

    def branch(selected: set[int], excluded: set[int]) -> None:
        """Recursive branch-and-bound function."""
        nonlocal best_solution, best_value, nodes_explored

        if is_timeout():
            return

        nodes_explored += 1

        # All nodes decided
        if selected | excluded == set(range(problem.node_count)):
            value = sum(problem.nodes[i].utility for i in selected)
            if value > best_value:
                best_value = value
                best_solution = list(selected)
            return

        # Compute bounds
        current_value = sum(problem.nodes[i].utility for i in selected)
        upper_bound = _greedy_upper_bound(problem, selected, excluded)

        # Pruning: if upper bound can't improve best solution, skip
        if upper_bound <= best_value:
            return

        # Choose variable to branch on (most promising remaining node)
        remaining = set(range(problem.node_count)) - selected - excluded
        if not remaining:
            value = current_value
            if value > best_value:
                best_value = value
                best_solution = list(selected)
            return

        # Pick node with highest utility
        branch_node = max(remaining, key=lambda i: problem.nodes[i].utility)

        # Branch 1: include branch_node
        if all(j not in selected for j in problem.adjacency[branch_node]):
            new_selected = selected | {branch_node}
            new_excluded = excluded | set(problem.adjacency[branch_node])
            branch(new_selected, new_excluded)

        if not is_timeout():
            # Branch 2: exclude branch_node
            branch(selected, excluded | {branch_node})

    # Start branch-and-bound
    branch(set(), set())

    runtime_ms = (perf_counter() - start) * 1000

    return SolverResult(
        name="branch_and_bound_mwis",
        selected=best_solution,
        utility=best_value,
        feasible=selection_is_feasible(problem, best_solution),
        runtime_ms=runtime_ms,
        metadata={
            "nodes_explored": nodes_explored,
        }
    )
