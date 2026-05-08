"""
MRTA Benchmark Script

Benchmarks OIM, Greedy, Simulated Annealing, Random Restarts, and Exact solver
across problem sizes: Tiny, Small, Medium, Large.

Benchmark sizes:
- Tiny (N=5, M=3): all solvers including exact
- Small (N=10, M=5): all solvers
- Medium (N=20, M=10): OIM, greedy, SA, random restarts
- Large (N=50, M=20): OIM, greedy, SA, random restarts (no exact)

Usage:
    python experiments/mrta/benchmark.py --sizes tiny small medium large --restarts 5

Outputs:
    /experiments/data/results/mrta_benchmark.json
"""

import json
import sys
import argparse
import random
import numpy as np
from pathlib import Path
from datetime import datetime
from time import perf_counter
from typing import List, Dict, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from oim_sim.types import Robot, Task, MRTAInstance
from oim_sim.mrta import build_mwis_problem
from oim_sim.solvers.greedy import solve_greedy_mwis
from oim_sim.solvers.simulated_annealing import solve_simulated_annealing
from oim_sim.solvers.random_restarts import solve_random_restarts
from oim_sim.solvers.exact import solve_exact_bruteforce
from oim_sim.solvers.kuramoto import solve_kuramoto_oim  # OIM


def generate_random_instance(num_robots: int, num_tasks: int, seed: int) -> MRTAInstance:
    """Generate random MRTA instance.

    Args:
        num_robots: Number of robots
        num_tasks: Number of tasks
        seed: Random seed

    Returns:
        MRTAInstance with random capabilities and requirements
    """
    random.seed(seed)
    np.random.seed(seed)

    # Generate random robots with random capabilities
    robots = []
    for i in range(num_robots):
        # 2-dimensional capabilities, uniform [0.5, 2.5]
        cap = tuple(np.random.uniform(0.5, 2.5, 2))
        pos = tuple(np.random.uniform(0, 10, 2))
        robots.append(Robot(id=i, capabilities=cap, position=pos))

    # Generate random tasks with random requirements
    tasks = []
    for i in range(num_tasks):
        # Requirements proportional to task importance
        scale = np.random.uniform(0.5, 2.0)
        req = tuple(scale * np.random.uniform(0.5, 2.0, 2))
        val = np.random.uniform(3.0, 10.0)
        pos = tuple(np.random.uniform(0, 10, 2))
        tasks.append(Task(id=i, requirements=req, value=val, position=pos))

    return MRTAInstance(
        name=f"{num_robots}R{num_tasks}T_Random",
        robots=tuple(robots),
        tasks=tuple(tasks)
    )


def benchmark_instance(
    instance: MRTAInstance,
    solvers: List[str],
    coalition_bound: int = 2,
    lambda_penalty: float = 8.0
) -> Dict:
    """Benchmark a single instance across specified solvers.

    Args:
        instance: MRTA instance
        solvers: List of solver names to run
        coalition_bound: Coalition size limit
        lambda_penalty: Penalty coefficient for QUBO

    Returns:
        Dict with results for each solver
    """
    # Build MWIS problem
    mwis_problem = build_mwis_problem(instance, coalition_bound=coalition_bound, lambda_penalty=lambda_penalty)

    results = {
        "instance": instance.name,
        "num_nodes": mwis_problem.node_count,
        "num_edges": len(mwis_problem.edges),
        "solvers": {}
    }

    # Greedy solver
    if "greedy" in solvers:
        t0 = perf_counter()
        sol = solve_greedy_mwis(mwis_problem)
        t1 = perf_counter()
        utility = sum(mwis_problem.nodes[i].utility for i in sol.selected)
        results["solvers"]["greedy"] = {
            "utility": round(utility, 4),
            "runtime_ms": round((t1 - t0) * 1000, 3),
            "selected_count": len(sol.selected)
        }

    # Simulated Annealing
    if "sa" in solvers:
        t0 = perf_counter()
        sol = solve_simulated_annealing(mwis_problem, steps=2000)
        t1 = perf_counter()
        utility = sum(mwis_problem.nodes[i].utility for i in sol.selected)
        results["solvers"]["sa"] = {
            "utility": round(utility, 4),
            "runtime_ms": round((t1 - t0) * 1000, 3),
            "selected_count": len(sol.selected)
        }

    # Random restarts (greedy)
    if "random_restarts" in solvers:
        t0 = perf_counter()
        sol = solve_random_restarts(mwis_problem, restarts=10)
        t1 = perf_counter()
        utility = sum(mwis_problem.nodes[i].utility for i in sol.selected)
        results["solvers"]["random_restarts"] = {
            "utility": round(utility, 4),
            "runtime_ms": round((t1 - t0) * 1000, 3),
            "selected_count": len(sol.selected)
        }

    # OIM (Kuramoto oscillator Ising machine)
    if "oim" in solvers:
        t0 = perf_counter()
        sol = solve_kuramoto_oim(mwis_problem)
        t1 = perf_counter()
        utility = sum(mwis_problem.nodes[i].utility for i in sol.selected)
        results["solvers"]["oim"] = {
            "utility": round(utility, 4),
            "runtime_ms": round((t1 - t0) * 1000, 3),
            "selected_count": len(sol.selected)
        }

    # Exact solver (brute force, small instances only)
    if "exact" in solvers and mwis_problem.node_count <= 20:
        t0 = perf_counter()
        sol = solve_exact_bruteforce(mwis_problem)
        t1 = perf_counter()
        utility = sum(mwis_problem.nodes[i].utility for i in sol.selected)
        results["solvers"]["exact"] = {
            "utility": round(utility, 4),
            "runtime_ms": round((t1 - t0) * 1000, 3),
            "selected_count": len(sol.selected)
        }

    # Compute approximation ratios (if exact is available)
    if "exact" in results["solvers"]:
        exact_util = results["solvers"]["exact"]["utility"]
        for solver_name in results["solvers"]:
            if solver_name != "exact":
                sol_util = results["solvers"][solver_name]["utility"]
                ratio = sol_util / exact_util if exact_util > 0 else 1.0
                results["solvers"][solver_name]["approx_ratio"] = round(ratio, 4)

    return results


def benchmark_size(
    size_name: str,
    num_robots: int,
    num_tasks: int,
    num_instances: int = 100,
    coalition_bound: int = 2,
    lambda_penalty: float = 8.0
) -> Dict:
    """Benchmark a specific problem size.

    Args:
        size_name: Name of size class (tiny, small, etc.)
        num_robots: Number of robots
        num_tasks: Number of tasks
        num_instances: Number of random instances to test
        coalition_bound: Coalition size limit
        lambda_penalty: Penalty coefficient for QUBO

    Returns:
        Dict with aggregated results
    """
    print(f"Benchmarking {size_name} ({num_robots}R, {num_tasks}T)...")

    # Determine which solvers to run
    solvers = ["oim", "greedy", "sa", "random_restarts"]
    if num_robots <= 5:  # Exact only for tiny
        solvers.append("exact")

    results = {
        "size": size_name,
        "num_robots": num_robots,
        "num_tasks": num_tasks,
        "num_instances": num_instances,
        "instances": []
    }

    for seed in range(num_instances):
        instance = generate_random_instance(num_robots, num_tasks, seed)
        result = benchmark_instance(instance, solvers, coalition_bound, lambda_penalty)
        results["instances"].append(result)
        if (seed + 1) % 10 == 0:
            print(f"  Completed {seed + 1}/{num_instances} instances")

    # Aggregate statistics
    results["summary"] = compute_aggregate_stats(results["instances"])

    return results


def compute_aggregate_stats(instances_results: List[Dict]) -> Dict:
    """Compute aggregate statistics over multiple instances.

    Args:
        instances_results: List of instance benchmark results

    Returns:
        Dict with mean, std, min, max for each solver
    """
    solver_utilities = {}
    solver_runtimes = {}

    for instance_result in instances_results:
        for solver_name, solver_result in instance_result["solvers"].items():
            if solver_name not in solver_utilities:
                solver_utilities[solver_name] = []
                solver_runtimes[solver_name] = []

            solver_utilities[solver_name].append(solver_result["utility"])
            solver_runtimes[solver_name].append(solver_result["runtime_ms"])

    summary = {}
    for solver_name in solver_utilities:
        utils = np.array(solver_utilities[solver_name])
        times = np.array(solver_runtimes[solver_name])

        summary[solver_name] = {
            "utility": {
                "mean": round(np.mean(utils), 4),
                "std": round(np.std(utils), 4),
                "min": round(np.min(utils), 4),
                "max": round(np.max(utils), 4)
            },
            "runtime_ms": {
                "mean": round(np.mean(times), 3),
                "std": round(np.std(times), 3),
                "min": round(np.min(times), 3),
                "max": round(np.max(times), 3)
            }
        }

    return summary


def main():
    """Parse arguments and run benchmarks."""

    parser = argparse.ArgumentParser(description="MRTA benchmark suite")
    parser.add_argument("--sizes", nargs="+", choices=["tiny", "small", "medium", "large"],
                        default=["tiny", "small", "medium", "large"],
                        help="Problem sizes to benchmark")
    parser.add_argument("--instances", type=int, default=100,
                        help="Number of instances per size")
    parser.add_argument("--restarts", type=int, default=5,
                        help="Number of restarts (currently not used)")

    args = parser.parse_args()

    size_configs = {
        "tiny": (5, 3),
        "small": (10, 5),
        "medium": (20, 10),
        "large": (50, 20),
    }

    benchmark_results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "experiment": "mrta_benchmark",
        "status": "PASS",
        "notes": f"Benchmarked {args.instances} instances per size",
        "data": {
            "sizes": []
        }
    }

    for size_name in args.sizes:
        num_robots, num_tasks = size_configs[size_name]
        size_result = benchmark_size(size_name, num_robots, num_tasks, args.instances)
        benchmark_results["data"]["sizes"].append(size_result)

    # Save results
    output_path = Path(__file__).parent.parent / "data" / "results" / "mrta_benchmark.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Custom JSON encoder for NumPy types
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            return super().default(obj)

    with open(output_path, "w") as f:
        json.dump(benchmark_results, f, indent=2, cls=NumpyEncoder)

    print(f"\nBenchmark results saved to {output_path}")

    # Print summary
    for size_data in benchmark_results["data"]["sizes"]:
        print(f"\n{size_data['size'].upper()} ({size_data['num_robots']}R, {size_data['num_tasks']}T):")
        for solver_name, stats in size_data["summary"].items():
            print(f"  {solver_name:15} utility: {stats['utility']['mean']:.4f} ± {stats['utility']['std']:.4f} "
                  f"time: {stats['runtime_ms']['mean']:.2f} ms")

    return benchmark_results


if __name__ == "__main__":
    main()
