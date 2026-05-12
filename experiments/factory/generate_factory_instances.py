"""
Generate factory MRTA instances for all 4 scales.
"""
import random
import sys
import math

sys.path.insert(0, 'src')
from oim_sim.types import Robot, Task, MRTAInstance
from oim_sim.mrta import build_mwis_problem, coalition_utility

FACTORY_SCALES = {
    'SmallFactory': {
        'n_robots': 5, 'n_tasks': 8, 'coalition_bound': 2,
        'annual_revenue': 2_000_000, 'n_operators': 20,
        'robot_cost': 80_000, 'manual_alloc_hours': 0.75,  # 45 min
    },
    'MediumFactory': {
        'n_robots': 15, 'n_tasks': 20, 'coalition_bound': 3,
        'annual_revenue': 25_000_000, 'n_operators': 80,
        'robot_cost': 120_000, 'manual_alloc_hours': 2.0,
    },
    'LargeFactory': {
        'n_robots': 30, 'n_tasks': 40, 'coalition_bound': 4,
        'annual_revenue': 200_000_000, 'n_operators': 300,
        'robot_cost': 150_000, 'manual_alloc_hours': 4.0,
    },
    'MegaFactory': {
        'n_robots': 60, 'n_tasks': 80, 'coalition_bound': 5,
        'annual_revenue': 2_000_000_000, 'n_operators': 1500,
        'robot_cost': 200_000, 'manual_alloc_hours': 8.0,
    },
}


def generate_factory_instance(n_robots, n_tasks, coalition_bound, seed=42, scale_name=''):
    """Generate a random factory MRTA instance with adaptive lambda."""
    rng = random.Random(seed)

    robots = []
    for i in range(n_robots):
        cap1 = rng.uniform(1, 5)
        cap2 = rng.uniform(1, 5)
        pos = (rng.uniform(0, 100), rng.uniform(0, 100))
        robots.append(Robot(i, (round(cap1, 2), round(cap2, 2)), pos))

    tasks = []
    for j in range(n_tasks):
        req1 = rng.uniform(1, 4)
        req2 = rng.uniform(1, 4)
        value = rng.uniform(5, 50)
        pos = (rng.uniform(0, 100), rng.uniform(0, 100))
        tasks.append(Task(j, (round(req1, 2), round(req2, 2)), round(value, 2), pos))

    instance = MRTAInstance(f'{scale_name}_{n_robots}R{n_tasks}T', tuple(robots), tuple(tasks))

    # Compute adaptive lambda
    prob_prelim = build_mwis_problem(instance, coalition_bound, lambda_penalty=1.0)
    if prob_prelim.edges:
        utils = [n.utility for n in prob_prelim.nodes]
        edges = [(e.u, e.v) for e in prob_prelim.edges]
        max_sum = max(utils[i] + utils[j] for i, j in edges)
        lam = max_sum * 1.05
    else:
        lam = 10.0

    prob = build_mwis_problem(instance, coalition_bound, lambda_penalty=lam)
    return instance, prob


if __name__ == '__main__':
    print("=" * 60)
    print("Factory Instance Generation Report")
    print("=" * 60)
    for scale_name, cfg in FACTORY_SCALES.items():
        instance, prob = generate_factory_instance(
            cfg['n_robots'], cfg['n_tasks'], cfg['coalition_bound'],
            seed=42, scale_name=scale_name
        )
        n_nodes = prob.node_count
        n_edges = len(prob.edges)
        lam = prob.lambda_penalty
        fleet_cost = cfg['n_robots'] * cfg['robot_cost']
        print(f"\n{scale_name}:")
        print(f"  Robots: {cfg['n_robots']}, Tasks: {cfg['n_tasks']}, CoalitionBound: {cfg['coalition_bound']}")
        print(f"  Coalition graph: {n_nodes} nodes, {n_edges} edges")
        print(f"  Lambda penalty: {lam:.3f}")
        print(f"  Fleet cost: ${fleet_cost:,}")
        print(f"  Annual revenue: ${cfg['annual_revenue']:,}")
