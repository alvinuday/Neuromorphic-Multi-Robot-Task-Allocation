"""
Unit tests for classical MWIS solvers.
Verifies correctness and feasibility of solutions.
"""
import pytest
from src.oim_sim.types import Robot, Task, MRTAInstance
from src.oim_sim.mrta import build_mwis_problem
from src.oim_sim.solvers import (
    solve_greedy_mwis,
    solve_ilp_mwis,
    solve_branch_and_bound,
    solve_local_search_mwis,
)


@pytest.fixture
def simple_mrta_instance():
    """Create a simple 2R1T MRTA instance for testing."""
    robots = (
        Robot(id=0, capabilities=(1.0, 2.0), position=(0, 0)),
        Robot(id=1, capabilities=(1.5, 1.5), position=(5, 5)),
    )
    tasks = (
        Task(id=0, requirements=(1.2, 1.8), value=5.0, position=(2.5, 2.5)),
    )
    return MRTAInstance(name="test_2R1T", robots=robots, tasks=tasks)


@pytest.fixture
def mwis_problem(simple_mrta_instance):
    """Build MWIS problem from MRTA instance."""
    return build_mwis_problem(simple_mrta_instance, coalition_bound=2, lambda_penalty=11.0)


def test_greedy_solver_feasibility(mwis_problem):
    """Test that greedy solver returns feasible solution."""
    result = solve_greedy_mwis(mwis_problem)
    assert result.feasible, "Greedy solver should return feasible solution"
    assert result.utility >= 0, "Utility should be non-negative"
    assert len(result.selected) <= mwis_problem.node_count


def test_branch_and_bound_solver_feasibility(mwis_problem):
    """Test that branch & bound solver returns feasible solution."""
    result = solve_branch_and_bound(mwis_problem, timeout_sec=5.0)
    assert result.feasible, "Branch & bound solver should return feasible solution"
    assert result.utility >= 0, "Utility should be non-negative"


def test_local_search_solver_feasibility(mwis_problem):
    """Test that local search solver returns feasible solution."""
    result = solve_local_search_mwis(mwis_problem, timeout_sec=5.0)
    assert result.feasible, "Local search solver should return feasible solution"
    assert result.utility >= 0, "Utility should be non-negative"


def test_ilp_solver_feasibility(mwis_problem):
    """Test that ILP solver returns feasible solution (if PuLP available)."""
    try:
        result = solve_ilp_mwis(mwis_problem, timeout_sec=5.0)
        assert result.feasible or "error" in result.metadata, \
            "ILP should return feasible solution or error"
        if result.feasible:
            assert result.utility >= 0, "Utility should be non-negative"
    except ImportError:
        pytest.skip("PuLP not available")


def test_selected_nodes_conflict_free(mwis_problem):
    """Test that selected nodes don't conflict (independent set property)."""
    result = solve_greedy_mwis(mwis_problem)

    selected_set = set(result.selected)
    for node_idx in result.selected:
        # Check this node doesn't conflict with others
        for neighbor_idx in mwis_problem.adjacency[node_idx]:
            assert neighbor_idx not in selected_set, \
                f"Nodes {node_idx} and {neighbor_idx} conflict but both selected"


def test_runtime_is_positive(mwis_problem):
    """Test that all solvers report positive runtime."""
    solvers = [
        solve_greedy_mwis,
        solve_branch_and_bound,
        solve_local_search_mwis,
    ]

    for solver in solvers:
        result = solver(mwis_problem)
        assert result.runtime_ms >= 0, f"{solver.__name__} reported negative runtime"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
