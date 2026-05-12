"""
Factory Instance Generator
==========================
Generates reproducible MRTA instances at four industrial scales.

Economic parameters are grounded in:
- IFR (2023): average industrial robot cost $120K-$250K
- McKinsey (2022): factory automation ROI 15-35%
- Deloitte (2023): smart factory energy reduction 10-25%
- Operator cost: US BLS manufacturing wage $22/hr + 60% overhead = $35/hr
"""
from __future__ import annotations
import random
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from oim_sim.types import Robot, Task, MRTAInstance
from oim_sim.mrta import build_mwis_problem

# ---------------------------------------------------------------------------
# Factory scale definitions
# ---------------------------------------------------------------------------

FACTORY_SCALES = {
    "small": {
        "label": "Small Factory (SME)",
        "n_robots": 5,
        "n_tasks": 8,
        "coalition_bound": 2,
        "annual_revenue_usd": 2_000_000,
        "n_operators": 20,
        "robot_unit_cost_usd": 80_000,
        "manual_alloc_hours_per_shift": 0.75,   # 45 min
        "operators_in_alloc": 2,
        "shifts_per_year": 750,                  # 3 shifts/day × 250 days
        "operator_hourly_rate_usd": 35,
        "oim_hw_cost_usd": 50_000,              # OIM analog chip unit
        "snn_hw_cost_usd": 30_000,              # Loihi-2 equivalent
        "hw_amortization_years": 5,
        "cpu_power_w": 100,
        "oim_power_w": 0.1,
        "snn_power_w": 0.5,
        "error_rate_manual": 0.15,              # 15% allocations need correction
        "downtime_cost_usd_per_hour": 500,
        "hours_downtime_per_error": 0.5,
        "revenue_sensitivity": 0.02,            # 2% revenue from allocation quality
    },
    "medium": {
        "label": "Medium Factory (Mid-market)",
        "n_robots": 15,
        "n_tasks": 20,
        "coalition_bound": 3,
        "annual_revenue_usd": 25_000_000,
        "n_operators": 80,
        "robot_unit_cost_usd": 120_000,
        "manual_alloc_hours_per_shift": 2.0,
        "operators_in_alloc": 4,
        "shifts_per_year": 750,
        "operator_hourly_rate_usd": 35,
        "oim_hw_cost_usd": 50_000,
        "snn_hw_cost_usd": 30_000,
        "hw_amortization_years": 5,
        "cpu_power_w": 100,
        "oim_power_w": 0.1,
        "snn_power_w": 0.5,
        "error_rate_manual": 0.15,
        "downtime_cost_usd_per_hour": 3_000,
        "hours_downtime_per_error": 0.5,
        "revenue_sensitivity": 0.02,
    },
    "large": {
        "label": "Large Factory (Enterprise)",
        "n_robots": 30,
        "n_tasks": 40,
        "coalition_bound": 4,
        "annual_revenue_usd": 200_000_000,
        "n_operators": 300,
        "robot_unit_cost_usd": 150_000,
        "manual_alloc_hours_per_shift": 4.0,
        "operators_in_alloc": 8,
        "shifts_per_year": 750,
        "operator_hourly_rate_usd": 35,
        "oim_hw_cost_usd": 50_000,
        "snn_hw_cost_usd": 30_000,
        "hw_amortization_years": 5,
        "cpu_power_w": 100,
        "oim_power_w": 0.1,
        "snn_power_w": 0.5,
        "error_rate_manual": 0.15,
        "downtime_cost_usd_per_hour": 15_000,
        "hours_downtime_per_error": 0.5,
        "revenue_sensitivity": 0.02,
    },
    "mega": {
        "label": "Mega Factory (Hyperscale)",
        "n_robots": 60,
        "n_tasks": 80,
        "coalition_bound": 5,
        "annual_revenue_usd": 2_000_000_000,
        "n_operators": 1500,
        "robot_unit_cost_usd": 200_000,
        "manual_alloc_hours_per_shift": 8.0,
        "operators_in_alloc": 20,
        "shifts_per_year": 750,
        "operator_hourly_rate_usd": 35,
        "oim_hw_cost_usd": 50_000,
        "snn_hw_cost_usd": 30_000,
        "hw_amortization_years": 5,
        "cpu_power_w": 100,
        "oim_power_w": 0.1,
        "snn_power_w": 0.5,
        "error_rate_manual": 0.15,
        "downtime_cost_usd_per_hour": 100_000,
        "hours_downtime_per_error": 0.5,
        "revenue_sensitivity": 0.02,
    },
}


def generate_instance(scale_key: str, seed: int = 42) -> tuple[MRTAInstance, object, float]:
    """Generate a reproducible factory MRTA instance at the given scale.

    Returns (instance, mwis_problem, lambda_penalty).
    Lambda is set to 1.05 × max(wi+wj) over all conflict edges.
    """
    cfg = FACTORY_SCALES[scale_key]
    n_robots = cfg["n_robots"]
    n_tasks = cfg["n_tasks"]
    coalition_bound = cfg["coalition_bound"]
    rng = random.Random(seed)

    robots = []
    for i in range(n_robots):
        cap = (round(rng.uniform(1, 5), 2), round(rng.uniform(1, 5), 2))
        pos = (round(rng.uniform(0, 100), 1), round(rng.uniform(0, 100), 1))
        robots.append(Robot(i, cap, pos))

    tasks = []
    for j in range(n_tasks):
        req = (round(rng.uniform(1, 4), 2), round(rng.uniform(1, 4), 2))
        val = round(rng.uniform(5, 50), 2)
        pos = (round(rng.uniform(0, 100), 1), round(rng.uniform(0, 100), 1))
        tasks.append(Task(j, req, val, pos))

    inst = MRTAInstance(f"{scale_key}_{n_robots}R{n_tasks}T_s{seed}", tuple(robots), tuple(tasks))

    # Preliminary build to compute adaptive lambda
    prob0 = build_mwis_problem(inst, coalition_bound, lambda_penalty=1.0)
    if prob0.edges:
        utils = [n.utility for n in prob0.nodes]
        max_pair = max(utils[e.u] + utils[e.v] for e in prob0.edges)
        lam = max_pair * 1.05
    else:
        lam = 10.0

    prob = build_mwis_problem(inst, coalition_bound, lambda_penalty=round(lam, 4))
    return inst, prob, lam


if __name__ == "__main__":
    print("Factory Instance Statistics")
    print("=" * 65)
    for key, cfg in FACTORY_SCALES.items():
        inst, prob, lam = generate_instance(key, seed=42)
        n_nodes = len(prob.nodes)
        n_edges = len(prob.edges)
        utils = [n.utility for n in prob.nodes]
        print(f"\n{cfg['label']}")
        print(f"  Robots={cfg['n_robots']}  Tasks={cfg['n_tasks']}  k={cfg['coalition_bound']}")
        print(f"  Coalition nodes (n): {n_nodes}")
        print(f"  Conflict edges (m):  {n_edges}")
        print(f"  Lambda:              {lam:.4f}")
        print(f"  Utility range:       [{min(utils):.3f}, {max(utils):.3f}]")
        print(f"  Graph density:       {2*n_edges/(n_nodes*(n_nodes-1)):.3f}" if n_nodes > 1 else "")
