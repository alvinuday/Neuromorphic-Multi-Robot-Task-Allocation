from __future__ import annotations

from itertools import combinations
from math import dist, exp

from .types import CoalitionNode, ConflictEdge, MRTAInstance, MWISProblem


def _coalition_subsets(robot_ids: list[int], max_size: int) -> list[tuple[int, ...]]:
    subsets: list[tuple[int, ...]] = []
    for size in range(1, max_size + 1):
        subsets.extend(combinations(robot_ids, size))
    return subsets


def is_feasible_coalition(instance: MRTAInstance, coalition: tuple[int, ...], task_id: int) -> bool:
    task = instance.tasks[task_id]
    for cap_idx, req in enumerate(task.requirements):
        provided = sum(instance.robots[r].capabilities[cap_idx] for r in coalition)
        if provided < req:
            return False
    return True


def coalition_utility(instance: MRTAInstance, coalition: tuple[int, ...], task_id: int) -> float:
    task = instance.tasks[task_id]
    travel_cost = sum(dist(instance.robots[r].position, task.position) * 0.5 for r in coalition)

    excess = 0.0
    for cap_idx, req in enumerate(task.requirements):
        provided = sum(instance.robots[r].capabilities[cap_idx] for r in coalition)
        excess += max(0.0, provided - req)

    efficiency = exp(-0.3 * excess)
    return max(0.1, task.value * efficiency - travel_cost)


def build_mwis_problem(
    instance: MRTAInstance,
    coalition_bound: int,
    lambda_penalty: float,
) -> MWISProblem:
    robot_ids = [r.id for r in instance.robots]
    task_ids = [t.id for t in instance.tasks]

    candidate_subsets = _coalition_subsets(robot_ids, coalition_bound)

    nodes: list[CoalitionNode] = []
    for task_id in task_ids:
        for coalition in candidate_subsets:
            if not is_feasible_coalition(instance, coalition, task_id):
                continue
            utility = coalition_utility(instance, coalition, task_id)
            label = "{" + ",".join(f"r{r + 1}" for r in coalition) + f"}}->t{task_id + 1}"
            nodes.append(
                CoalitionNode(
                    index=len(nodes),
                    robots=coalition,
                    task_id=task_id,
                    utility=utility,
                    label=label,
                )
            )

    adjacency: list[set[int]] = [set() for _ in nodes]
    edges: list[ConflictEdge] = []

    for i, ni in enumerate(nodes):
        robots_i = set(ni.robots)
        for j in range(i + 1, len(nodes)):
            nj = nodes[j]
            shared_robot = bool(robots_i.intersection(nj.robots))
            shared_task = ni.task_id == nj.task_id
            if not (shared_robot or shared_task):
                continue

            if shared_robot and shared_task:
                ctype = "both"
            elif shared_robot:
                ctype = "robot"
            else:
                ctype = "task"

            adjacency[i].add(j)
            adjacency[j].add(i)
            edges.append(ConflictEdge(u=i, v=j, conflict_type=ctype))

    return MWISProblem(
        instance_name=instance.name,
        nodes=nodes,
        adjacency=adjacency,
        edges=edges,
        lambda_penalty=lambda_penalty,
    )


def selection_is_feasible(problem: MWISProblem, selected: list[int]) -> bool:
    chosen = set(selected)
    for i in selected:
        if any(j in chosen for j in problem.adjacency[i]):
            return False
    return True


def selection_utility(problem: MWISProblem, selected: list[int]) -> float:
    return sum(problem.nodes[idx].utility for idx in selected)


def selection_conflicts(problem: MWISProblem, selected: list[int]) -> int:
    chosen = set(selected)
    conflicts = 0
    for i in selected:
        for j in problem.adjacency[i]:
            if j in chosen and j > i:
                conflicts += 1
    return conflicts
