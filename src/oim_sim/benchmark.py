from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Callable

from .mrta import build_mwis_problem
from .solvers import (
    KuramotoConfig,
    solve_exact_bruteforce,
    solve_greedy_mwis,
    solve_kuramoto_oim,
    solve_random_restarts,
    solve_simulated_annealing,
)
from .types import MRTAInstance, Robot, SolverResult, Task

SolverFn = Callable[[object], SolverResult]


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    instance: MRTAInstance
    coalition_bound: int
    lambda_penalty: float


def _rand_case(name: str, n_robots: int, n_tasks: int, n_caps: int, seed: int) -> MRTAInstance:
    rng = random.Random(seed)

    robots = []
    for i in range(n_robots):
        caps = tuple(round(rng.uniform(0.5, 3.5), 2) for _ in range(n_caps))
        pos = (round(rng.random(), 3), round(rng.random(), 3))
        robots.append(Robot(id=i, capabilities=caps, position=pos))

    tasks = []
    for j in range(n_tasks):
        req = tuple(round(rng.uniform(0.4, 2.8), 2) for _ in range(n_caps))
        value = round(rng.uniform(3.0, 10.0), 2)
        pos = (round(rng.random(), 3), round(rng.random(), 3))
        tasks.append(Task(id=j, requirements=req, value=value, position=pos))

    return MRTAInstance(name=name, robots=tuple(robots), tasks=tuple(tasks))


def default_cases() -> list[BenchmarkCase]:
    specs = [
        ("N3_M2_S7", 3, 2, 2, 7, 2, 11.0),
        ("N4_M2_S8", 4, 2, 2, 8, 2, 11.0),
        ("N4_M3_S9", 4, 3, 2, 9, 2, 11.0),
        ("N5_M2_S10", 5, 2, 2, 10, 2, 11.0),
        ("N6_M3_S21", 6, 3, 2, 21, 2, 11.0),
        ("N8_M4_S31", 8, 4, 2, 31, 2, 11.0),
    ]
    out: list[BenchmarkCase] = []
    for name, n, m, k, seed, cbound, lam in specs:
        out.append(
            BenchmarkCase(
                name=name,
                instance=_rand_case(name, n, m, k, seed),
                coalition_bound=cbound,
                lambda_penalty=lam,
            )
        )
    return out


def run_benchmark(cases: list[BenchmarkCase], exact_node_limit: int = 22) -> dict:
    solvers: dict[str, Callable[[object], SolverResult]] = {
        "greedy_mwis": solve_greedy_mwis,
        "simulated_annealing": lambda p: solve_simulated_annealing(p, steps=2600, seed=11),
        "kuramoto_oim": lambda p: solve_kuramoto_oim(
            p,
            config=KuramotoConfig(restarts=8, steps=280, dt=0.035, kinj_min=0.15, kinj_max=3.4, coupling_gain=1.0, bias_gain=0.55, noise_amp=0.04),
            seed=13,
        ),
        "random_restarts": lambda p: solve_random_restarts(p, restarts=120, seed=17),
    }

    rows: list[dict] = []

    for case in cases:
        problem = build_mwis_problem(
            instance=case.instance,
            coalition_bound=case.coalition_bound,
            lambda_penalty=case.lambda_penalty,
        )

        optimum = None
        if problem.node_count <= exact_node_limit:
            optimum = solve_exact_bruteforce(problem, max_nodes=exact_node_limit).utility

        for solver_name, solver_fn in solvers.items():
            result = solver_fn(problem)
            ratio = None if optimum in (None, 0.0) else result.utility / optimum
            rows.append(
                {
                    "case": case.name,
                    "nodes": problem.node_count,
                    "solver": solver_name,
                    "utility": result.utility,
                    "feasible": result.feasible,
                    "runtime_ms": result.runtime_ms,
                    "approx_ratio": ratio,
                    "optimum_utility": optimum,
                }
            )

    summary = {}
    for solver_name in {r["solver"] for r in rows}:
        subset = [r for r in rows if r["solver"] == solver_name]
        ratios = [r["approx_ratio"] for r in subset if r["approx_ratio"] is not None]
        summary[solver_name] = {
            "avg_utility": mean(r["utility"] for r in subset),
            "avg_runtime_ms": mean(r["runtime_ms"] for r in subset),
            "feasibility_rate": mean(1.0 if r["feasible"] else 0.0 for r in subset),
            "avg_approx_ratio": mean(ratios) if ratios else None,
        }

    return {"rows": rows, "summary": summary}


def benchmark_markdown(report: dict) -> str:
    lines: list[str] = []
    lines.append("# OIM-MRTA Benchmark Results")
    lines.append("")
    lines.append("## Setup")
    lines.append("- Solvers: kuramoto_oim, simulated_annealing, greedy_mwis, random_restarts")
    lines.append("- Coalition bound: k=2")
    lines.append("- Exact optimum: brute-force MWIS when node count <= 22")
    lines.append("")

    lines.append("## Case Results")
    lines.append("| Case | Nodes | Solver | Utility | Feasible | Runtime (ms) | Approx ratio |")
    lines.append("|---|---:|---|---:|:---:|---:|---:|")
    for row in report["rows"]:
        ratio = "n/a" if row["approx_ratio"] is None else f"{row['approx_ratio']:.3f}"
        feasible = "Y" if row["feasible"] else "N"
        lines.append(
            f"| {row['case']} | {row['nodes']} | {row['solver']} | {row['utility']:.3f} | {feasible} | {row['runtime_ms']:.2f} | {ratio} |"
        )

    lines.append("")
    lines.append("## Aggregate Summary")
    lines.append("| Solver | Avg utility | Avg runtime (ms) | Feasibility rate | Avg approx ratio |")
    lines.append("|---|---:|---:|---:|---:|")
    for solver, stats in sorted(report["summary"].items()):
        ratio = "n/a" if stats["avg_approx_ratio"] is None else f"{stats['avg_approx_ratio']:.3f}"
        lines.append(
            f"| {solver} | {stats['avg_utility']:.3f} | {stats['avg_runtime_ms']:.2f} | {stats['feasibility_rate']:.3f} | {ratio} |"
        )

    return "\n".join(lines) + "\n"


def save_report(report: dict, markdown_path: Path, json_path: Path) -> None:
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(benchmark_markdown(report), encoding="utf-8")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
