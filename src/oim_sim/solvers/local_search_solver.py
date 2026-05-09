"""
Local Search solver for Maximum Weighted Independent Set (MWIS).
Combines greedy initialization with 2-opt and 3-opt local improvements.
"""
from __future__ import annotations

from time import perf_counter
from ..mrta import selection_is_feasible, selection_utility
from ..types import MWISProblem, SolverResult


def solve_local_search_mwis(
    problem: MWISProblem,
    timeout_sec: float = 30.0,
    multistart: int = 3
) -> SolverResult:
    """
    Solve MWIS using greedy + local search improvements.

    Algorithm:
    1. Start with greedy solution
    2. Apply 2-opt local improvements (swap pairs of nodes)
    3. Apply 3-opt improvements (swap triplets)
    4. Repeat with different random orderings (multistart)

    Args:
        problem: MWISProblem instance
        timeout_sec: Time limit for solver
        multistart: Number of random restarts with different greedy orderings

    Returns:
        SolverResult with best solution found
    """
    start = perf_counter()
    best_solution = []
    best_value = 0.0

    def is_timeout() -> bool:
        return (perf_counter() - start) > timeout_sec

    def greedy_with_order(order: list[int]) -> tuple[list[int], float]:
        """Greedy selection with given order."""
        selected = []
        blocked = set()
        for idx in order:
            if idx in blocked:
                continue
            selected.append(idx)
            blocked.add(idx)
            blocked.update(problem.adjacency[idx])
        return selected, sum(problem.nodes[i].utility for i in selected)

    def two_opt(solution: list[int]) -> list[int]:
        """Apply 2-opt improvements: try swapping pairs of nodes."""
        sol = set(solution)
        improved = True
        iterations = 0
        max_iterations = 50

        while improved and iterations < max_iterations and not is_timeout():
            improved = False
            iterations += 1

            # Try removing one node and adding another
            for remove_idx in list(sol):
                for add_idx in range(problem.node_count):
                    if add_idx in sol or add_idx in problem.adjacency[remove_idx]:
                        continue

                    # Check if adding add_idx conflicts with remaining selected
                    conflicts = any(
                        other in problem.adjacency[add_idx]
                        for other in sol if other != remove_idx
                    )

                    if not conflicts:
                        old_utility = problem.nodes[remove_idx].utility
                        new_utility = problem.nodes[add_idx].utility

                        if new_utility > old_utility:
                            sol.discard(remove_idx)
                            sol.add(add_idx)
                            improved = True
                            break

                if improved:
                    break

        return list(sol)

    def three_opt(solution: list[int]) -> list[int]:
        """Apply 3-opt improvements: try swapping triplets of nodes."""
        sol = set(solution)
        improved = True
        iterations = 0
        max_iterations = 20

        while improved and iterations < max_iterations and not is_timeout():
            improved = False
            iterations += 1

            # Try removing 2 nodes and adding 1
            for i, remove_idx1 in enumerate(list(sol)):
                for remove_idx2 in list(sol)[i+1:]:
                    for add_idx in range(problem.node_count):
                        if add_idx in sol or add_idx in problem.adjacency[remove_idx1] or add_idx in problem.adjacency[remove_idx2]:
                            continue

                        # Check conflicts
                        conflicts = any(
                            other in problem.adjacency[add_idx]
                            for other in sol if other not in {remove_idx1, remove_idx2}
                        )

                        if not conflicts:
                            old_utility = problem.nodes[remove_idx1].utility + problem.nodes[remove_idx2].utility
                            new_utility = problem.nodes[add_idx].utility

                            if new_utility > old_utility:
                                sol.discard(remove_idx1)
                                sol.discard(remove_idx2)
                                sol.add(add_idx)
                                improved = True
                                break

                    if improved:
                        break
                if improved:
                    break

        return list(sol)

    # Try multiple random orderings
    import random
    for restart in range(multistart):
        if is_timeout():
            break

        # Greedy with random order
        order = list(range(problem.node_count))
        random.shuffle(order)
        solution, value = greedy_with_order(order)

        # Apply local search improvements
        solution = two_opt(solution)
        if not is_timeout():
            solution = three_opt(solution)

        # Check if best so far
        final_value = sum(problem.nodes[i].utility for i in solution)
        if final_value > best_value:
            best_value = final_value
            best_solution = solution

    runtime_ms = (perf_counter() - start) * 1000

    return SolverResult(
        name="local_search_mwis",
        selected=best_solution,
        utility=best_value,
        feasible=selection_is_feasible(problem, best_solution),
        runtime_ms=runtime_ms,
        metadata={
            "multistart_restarts": multistart,
        }
    )
