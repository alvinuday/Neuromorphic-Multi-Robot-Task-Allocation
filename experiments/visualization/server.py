"""Cockpit Flask server — port 5001.

REST endpoints:
  GET  /                     -> serves index.html
  POST /api/solve            -> run solver(s) on MRTA instance
  GET  /api/oim_dynamics     -> OIM theta trace data
  GET  /api/snn_dynamics     -> SNN voltage trace data
  POST /api/benchmark        -> time complexity benchmark
  GET  /api/arm              -> 2-DOF arm dynamics at theta
  GET  /api/proofs           -> run empirical proofs
  GET  /api/export           -> export datasets as ZIP
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import zipfile
import io
import random
from datetime import datetime
from pathlib import Path

# Add src to path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from flask import Flask, request, jsonify, send_file, send_from_directory

from oim_sim.types import Robot, Task, MRTAInstance
from oim_sim.mrta import build_mwis_problem
from oim_sim.solvers.kuramoto import solve_kuramoto_oim, KuramotoConfig
from oim_sim.solvers.greedy import solve_greedy_mwis
from oim_sim.solvers.simulated_annealing import solve_simulated_annealing
from oim_sim.solvers.exact import solve_exact_bruteforce
from snn_sim import SNNSolver, SNNConfig, ArmDynamics
from snn_sim.arm_dynamics import ArmParams

app = Flask(__name__, static_folder=str(Path(__file__).parent))
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


def log_run(endpoint: str, data: dict):
    """Log run to JSON file."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    log_path = LOGS_DIR / f"{endpoint}_{ts}.json"
    with open(log_path, "w") as f:
        json.dump({"timestamp": ts, "endpoint": endpoint, "data": data}, f, indent=2)


def get_default_instance():
    robots = (
        Robot(id=0, capabilities=(2.0, 0.0), position=(0.0, 0.0)),
        Robot(id=1, capabilities=(0.0, 2.0), position=(1.0, 1.0)),
        Robot(id=2, capabilities=(1.0, 1.0), position=(2.0, 0.0)),
    )
    tasks = (
        Task(id=0, requirements=(1.0, 1.0), value=6.0, position=(0.5, 0.5)),
        Task(id=1, requirements=(2.0, 0.0), value=5.0, position=(2.0, 0.5)),
    )
    return MRTAInstance(name="3R2T_Worked_Example", robots=robots, tasks=tasks)


def build_instance_from_params(params: dict) -> MRTAInstance:
    """Build MRTA instance from API parameters."""
    n_robots = int(params.get("n_robots", 3))
    n_tasks = int(params.get("n_tasks", 2))
    seed = int(params.get("seed", 42))
    rng = random.Random(seed)

    robots = tuple(
        Robot(
            id=i,
            capabilities=tuple(round(rng.uniform(0.5, 2.0), 2) for _ in range(2)),
            position=(round(rng.uniform(0, 3), 2), round(rng.uniform(0, 3), 2)),
        )
        for i in range(n_robots)
    )
    tasks = tuple(
        Task(
            id=j,
            requirements=tuple(round(rng.uniform(0.5, 1.5), 2) for _ in range(2)),
            value=round(rng.uniform(4.0, 8.0), 2),
            position=(round(rng.uniform(0, 3), 2), round(rng.uniform(0, 3), 2)),
        )
        for j in range(n_tasks)
    )
    return MRTAInstance(name=f"random_{n_robots}R{n_tasks}T", robots=robots, tasks=tasks)


# ---- Routes ----

@app.route("/")
def index():
    return send_from_directory(str(Path(__file__).parent), "index.html")


@app.route("/api/solve", methods=["POST"])
def api_solve():
    """Run solver(s) on an MRTA instance."""
    data = request.get_json(force=True) or {}
    params = data.get("instance", {})
    solvers_req = data.get("solvers", ["oim", "greedy", "sa", "exact"])
    coalition_bound = int(data.get("coalition_bound", 2))
    lambda_penalty = float(data.get("lambda_penalty", 8.0))

    if params:
        instance = build_instance_from_params(params)
    else:
        instance = get_default_instance()

    prob = build_mwis_problem(instance, coalition_bound=coalition_bound, lambda_penalty=lambda_penalty)

    # Build graph data for visualization
    nodes_data = [
        {"id": n.index, "label": n.label, "utility": round(n.utility, 4),
         "task_id": n.task_id, "robots": list(n.robots)}
        for n in prob.nodes
    ]
    edges_data = [
        {"u": e.u, "v": e.v, "type": e.conflict_type}
        for e in prob.edges
    ]

    results = {}
    solver_map = {
        "oim": ("OIM Kuramoto", lambda: solve_kuramoto_oim(prob, config=KuramotoConfig(restarts=5, steps=280), seed=42)),
        "greedy": ("Greedy", lambda: solve_greedy_mwis(prob)),
        "sa": ("Simulated Annealing", lambda: solve_simulated_annealing(prob, seed=42)),
        "exact": ("Exact BF", lambda: solve_exact_bruteforce(prob, max_nodes=24)),
        "snn": ("SNN LIF", lambda: SNNSolver(SNNConfig(sim_time_ms=200, dt_ms=0.1, restarts=5, seed=42)).solve(
            [n.utility for n in prob.nodes], prob.adjacency, prob.lambda_penalty)),
    }

    for key in solvers_req:
        if key not in solver_map:
            continue
        name, fn = solver_map[key]
        try:
            r = fn()
            results[key] = {
                "name": name,
                "selected": r.selected,
                "labels": [prob.nodes[i].label for i in r.selected],
                "utility": round(r.utility, 4),
                "feasible": r.feasible if hasattr(r, 'feasible') else True,
                "runtime_ms": round(r.runtime_ms, 3),
            }
        except Exception as e:
            results[key] = {"name": name, "error": str(e)}

    response = {
        "instance_name": instance.name,
        "n_robots": len(instance.robots),
        "n_tasks": len(instance.tasks),
        "n_coalition_nodes": prob.node_count,
        "n_edges": len(prob.edges),
        "nodes": nodes_data,
        "edges": edges_data,
        "results": results,
    }
    log_run("solve", response)
    return jsonify(response)


@app.route("/api/oim_dynamics", methods=["GET"])
def api_oim_dynamics():
    """Return OIM theta evolution data."""
    n_restarts = int(request.args.get("restarts", 3))
    n_steps = int(request.args.get("steps", 100))

    instance = get_default_instance()
    prob = build_mwis_problem(instance, coalition_bound=2, lambda_penalty=8.0)

    import math as _math
    import random as _random

    n = prob.node_count
    weights = [node.utility for node in prob.nodes]
    adjacency = [list(prob.adjacency[i]) for i in range(n)]
    lam = prob.lambda_penalty
    dt = 0.035
    kinj_min, kinj_max = 0.15, 3.4
    coupling_gain = 1.0
    bias_gain = 0.55
    noise_amp = 0.04
    noise_cooling = 0.995

    all_traces = []
    rng = _random.Random(42)

    for restart in range(n_restarts):
        theta = [rng.random() * 2 * _math.pi for _ in range(n)]
        noise = noise_amp
        trace = {"restart": restart, "theta_history": [], "steps": []}

        for step in range(n_steps):
            if step % max(1, n_steps // 20) == 0:
                trace["theta_history"].append([round(t, 4) for t in theta])
                trace["steps"].append(step)

            ratio = step / max(1, n_steps - 1)
            kinj = kinj_min + (kinj_max - kinj_min) * ratio
            new_theta = []
            for i in range(n):
                d = kinj * _math.sin(2 * theta[i])
                for j in adjacency[i]:
                    kij = coupling_gain * (lam / 10.0)
                    d += kij * _math.sin(theta[j] - theta[i] - _math.pi)
                local_field = bias_gain * (weights[i] - 0.32 * lam * len(adjacency[i]))
                d += local_field * (-_math.sin(theta[i]))
                d += (rng.random() * 2 - 1) * noise
                new_theta.append(((theta[i] + dt * d) % (2*_math.pi) + 2*_math.pi) % (2*_math.pi))
            theta = new_theta
            noise *= noise_cooling

        # Final spins
        spins = [1 if _math.cos(t) >= 0 else -1 for t in theta]
        trace["final_theta"] = [round(t, 4) for t in theta]
        trace["final_spins"] = spins
        all_traces.append(trace)

    response = {
        "n_nodes": n,
        "node_labels": [n_.label for n_ in prob.nodes],
        "traces": all_traces,
    }
    log_run("oim_dynamics", {"n_restarts": n_restarts, "n_steps": n_steps})
    return jsonify(response)


@app.route("/api/snn_dynamics", methods=["GET"])
def api_snn_dynamics():
    """Return SNN voltage trace data."""
    sim_time = float(request.args.get("sim_time_ms", 200.0))
    dt = float(request.args.get("dt_ms", 0.5))

    instance = get_default_instance()
    prob = build_mwis_problem(instance, coalition_bound=2, lambda_penalty=8.0)
    utilities = [n.utility for n in prob.nodes]

    cfg = SNNConfig(sim_time_ms=sim_time, dt_ms=dt, restarts=1, seed=42)
    solver = SNNSolver(cfg)
    sim = solver.simulate(utilities, prob.adjacency, prob.lambda_penalty, record_traces=True)

    response = {
        "n_neurons": sim.n_neurons,
        "node_labels": [n.label for n in prob.nodes],
        "time_axis_ms": [round(t, 2) for t in sim.time_axis_ms],
        "voltage_traces": [[round(v, 4) for v in tr] for tr in sim.voltage_traces],
        "spike_times": [sr.spike_times_ms for sr in sim.spike_records],
        "spike_counts": [sr.spike_count for sr in sim.spike_records],
    }
    log_run("snn_dynamics", {"sim_time_ms": sim_time, "dt_ms": dt})
    return jsonify(response)


@app.route("/api/benchmark", methods=["POST"])
def api_benchmark():
    """Run time complexity benchmark."""
    data = request.get_json(force=True) or {}
    sizes = data.get("sizes", [3, 5, 7, 10, 15])

    # Import benchmark_size inline using importlib to avoid package path issues
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "time_complexity",
        str(ROOT / "experiments" / "complexity" / "time_complexity.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    results = []
    for n_nodes in sizes:
        r = mod.benchmark_size(n_nodes, n_reps=1)
        results.append(r)

    log_run("benchmark", {"sizes": sizes, "results": results})
    return jsonify({"results": results})


@app.route("/api/arm", methods=["GET"])
def api_arm():
    """Return 2-DOF arm state at given theta."""
    theta1 = float(request.args.get("theta1", 0.0))
    theta2 = float(request.args.get("theta2", 0.0))

    arm = ArmDynamics()
    M = arm.inertia_matrix(theta1, theta2)
    G = arm.gravity_torques(theta1, theta2)
    elbow, tip = arm.forward_kinematics(theta1, theta2)
    p = arm.p

    response = {
        "theta1": theta1,
        "theta2": theta2,
        "M": [[round(v, 4) for v in row] for row in M],
        "G": [round(v, 4) for v in G],
        "elbow": [round(elbow[0], 4), round(elbow[1], 4)],
        "tip": [round(tip[0], 4), round(tip[1], 4)],
        "base": [0.0, 0.0],
        "params": {
            "l1": p.l1, "l2": p.l2, "m1": p.m1, "m2": p.m2,
            "g": p.g, "I1": round(p.I1, 6), "I2": round(p.I2, 6),
        },
    }
    return jsonify(response)


@app.route("/api/proofs", methods=["GET"])
def api_proofs():
    """Run quick empirical proofs and return results."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "empirical_proof",
        str(ROOT / "experiments" / "validation" / "empirical_proof.py"),
    )
    emp_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(emp_mod)

    instance = get_default_instance()
    prob = build_mwis_problem(instance, coalition_bound=2, lambda_penalty=8.0)

    proof_qubo_correctness = emp_mod.proof_qubo_correctness
    proof_penalty_theorem = emp_mod.proof_penalty_theorem
    proof_mwis_qubo_min = emp_mod.proof_mwis_qubo_min

    _, all_match = proof_qubo_correctness(prob)
    _, _fv, _iv, theorem_holds = proof_penalty_theorem(prob)
    qsel, msel, qval, mval, match = proof_mwis_qubo_min(prob)

    response = {
        "qubo_correctness": {"pass": all_match, "description": "x^T Q x matches formula for all 128 assignments"},
        "penalty_theorem": {
            "pass": theorem_holds,
            "min_infeasible": round(min(_iv), 4),
            "min_feasible": round(min(_fv), 4),
            "description": "min(infeasible QUBO) > min(feasible QUBO)",
        },
        "mwis_qubo_min": {
            "pass": match,
            "qubo_min_nodes": qsel,
            "mwis_nodes": msel,
            "description": "QUBO minimizer = MWIS solution",
        },
    }
    log_run("proofs", response)
    return jsonify(response)


@app.route("/api/export", methods=["GET"])
def api_export():
    """Export all datasets as ZIP."""
    datasets_dir = ROOT / "experiments" / "datasets"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in datasets_dir.glob("*.xlsx"):
            zf.write(f, f.name)
    buf.seek(0)
    return send_file(
        buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name="neuromorphic_mrta_datasets.zip",
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check imports and exit")
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    if args.check:
        print("All imports OK")
        sys.exit(0)

    print(f"Starting cockpit server on http://localhost:{args.port}")
    app.run(host="0.0.0.0", port=args.port, debug=False)
