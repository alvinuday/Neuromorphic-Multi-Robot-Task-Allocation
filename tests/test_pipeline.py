from __future__ import annotations

from oim_sim.mrta import build_mwis_problem, selection_is_feasible
from oim_sim.solvers import solve_exact_bruteforce, solve_greedy_mwis
from oim_sim.types import MRTAInstance, Robot, Task


def _example_instance() -> MRTAInstance:
    robots = (
        Robot(id=0, capabilities=(2.0, 0.0), position=(0.1, 0.1)),
        Robot(id=1, capabilities=(1.6, 0.7), position=(0.2, 0.2)),
        Robot(id=2, capabilities=(0.0, 2.2), position=(0.9, 0.8)),
    )
    tasks = (
        Task(id=0, requirements=(3.0, 0.5), value=6.0, position=(0.15, 0.15)),
        Task(id=1, requirements=(0.0, 2.0), value=5.0, position=(0.85, 0.85)),
    )
    return MRTAInstance(name="toy_case", robots=robots, tasks=tasks)


def test_build_mwis_problem_and_exact_solution() -> None:
    instance = _example_instance()
    problem = build_mwis_problem(instance, coalition_bound=2, lambda_penalty=11.0)

    assert problem.node_count > 0
    assert len(problem.adjacency) == problem.node_count

    exact = solve_exact_bruteforce(problem, max_nodes=24)
    assert exact.feasible
    assert selection_is_feasible(problem, exact.selected)
    assert exact.utility > 0.0


def test_greedy_solver_returns_feasible_solution() -> None:
    instance = _example_instance()
    problem = build_mwis_problem(instance, coalition_bound=2, lambda_penalty=11.0)

    greedy = solve_greedy_mwis(problem)
    assert greedy.feasible
    assert selection_is_feasible(problem, greedy.selected)
    assert greedy.utility > 0.0
