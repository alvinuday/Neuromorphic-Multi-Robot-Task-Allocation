#!/usr/bin/env python3
"""
Flask API server for MRTA solver comparison.
Exposes endpoints for running different solvers and comparing results.
"""
import json
from dataclasses import asdict
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from oim_sim.types import Robot, Task, MRTAInstance
from oim_sim.mrta import build_mwis_problem, coalition_utility, selection_utility, selection_is_feasible
from oim_sim.solvers.greedy import solve_greedy_mwis
from oim_sim.solvers.kuramoto import solve_kuramoto_oim
from oim_sim.solvers.exact import solve_exact_bruteforce
from oim_sim.solvers.simulated_annealing import solve_simulated_annealing
from oim_sim.solvers.random_restarts import solve_random_restarts

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# SOLVER DESCRIPTIONS
SOLVER_DESCRIPTIONS = {
    "greedy_mwis": {
        "name": "Greedy (MWIS)",
        "description": "Greedy Maximum Weighted Independent Set - sorts nodes by utility descending, greedily selects feasible nodes.",
        "time_complexity": "O(n + m)",
        "guarantee": "Approximation (~0.5 for general graphs, often optimal on small problems)",
        "characteristics": [
            "Deterministic - always returns same result",
            "Very fast (<1ms) even for large graphs",
            "Good for quick feasible solutions"
        ]
    },
    "kuramoto_oim": {
        "name": "OIM Kuramoto Dynamics",
        "description": "Oscillator Ising Machine using coupled Kuramoto oscillators with injection locking. Uses 8 independent random restarts with different noise seeds.",
        "time_complexity": "O(8 × n² × steps) = O(8 × n² × 280)",
        "guarantee": "Heuristic - may find better solutions than greedy on larger problems",
        "characteristics": [
            "Stochastic - different result each run due to random noise",
            "Slow (100-300ms) but explores solution space better",
            "Phase-coupled oscillators naturally avoid conflicts",
            "8 restarts increase robustness"
        ]
    },
    "exact_bruteforce": {
        "name": "Exact Brute-Force",
        "description": "Exhaustive search through all 2^n possible subsets to find globally optimal solution. Reference ground truth.",
        "time_complexity": "O(2^n × poly(n))",
        "guarantee": "Guaranteed optimal solution",
        "characteristics": [
            "Only practical for n ≤ 22 (computation time explodes)",
            "Used as verification baseline for small problems",
            "Provides ground truth for testing other methods"
        ]
    },
    "simulated_annealing": {
        "name": "Simulated Annealing",
        "description": "Metaheuristic that escapes local optima by accepting worse solutions with decreasing probability as 'temperature' cools.",
        "time_complexity": "O(temperature × n × iterations)",
        "guarantee": "Heuristic - asymptotically optimal with infinite time",
        "characteristics": [
            "Often finds good solutions faster than random search",
            "Temperature schedule controls exploration vs exploitation",
            "Probability of accepting worse moves decreases over time"
        ]
    },
    "random_restarts": {
        "name": "Random Restarts",
        "description": "Runs multiple independent greedy solves from random starting configurations, returns best result found.",
        "time_complexity": "O(restarts × (n + m))",
        "guarantee": "Heuristic - benefits from increased restarts",
        "characteristics": [
            "Simple but effective for small problems",
            "Each restart is independent greedy from different seed",
            "More restarts → higher chance of finding global optimum"
        ]
    }
}


def build_instance_from_request(data):
    """Build MRTAInstance from JSON request data."""
    robots = []
    for i, r in enumerate(data['robots']):
        robots.append(Robot(
            id=i,
            capabilities=tuple(r['capabilities']),
            position=tuple(r['position'])
        ))
    
    tasks = []
    for j, t in enumerate(data['tasks']):
        tasks.append(Task(
            id=j,
            requirements=tuple(t['requirements']),
            value=t['value'],
            position=tuple(t['position'])
        ))
    
    return MRTAInstance(
        name=data.get('name', 'instance'),
        robots=tuple(robots),
        tasks=tuple(tasks)
    )


@app.route('/api/solvers', methods=['GET'])
def get_solver_descriptions():
    """Return descriptions of all available solvers."""
    return jsonify(SOLVER_DESCRIPTIONS)


@app.route('/api/solve', methods=['POST'])
def solve():
    """
    Solve MRTA problem with specified solver.
    
    Request JSON:
    {
        "method": "greedy_mwis" | "kuramoto_injected" | "exact_brute_force" | "simulated_annealing" | "random_restarts",
        "coalition_bound": 3,
        "lambda_penalty": 8,
        "robots": [
            {"capabilities": [2.0, 0.0], "position": [0.82, 0.33]},
            ...
        ],
        "tasks": [
            {"requirements": [1.0, 1.0], "value": 6.0, "position": [0.0, 0.0]},
            ...
        ]
    }
    """
    try:
        data = request.json
        method = data.get('method', 'greedy_mwis')
        coalition_bound = int(data.get('coalition_bound', 3))
        lambda_penalty = float(data.get('lambda_penalty', 8.0))
        
        # Build MRTA instance
        instance = build_instance_from_request(data)
        
        # Build MWIS problem
        problem = build_mwis_problem(instance, coalition_bound, lambda_penalty)
        
        # Solve with requested method
        if method == 'greedy_mwis':
            result = solve_greedy_mwis(problem)
        elif method == 'kuramoto_oim':
            result = solve_kuramoto_oim(problem)
        elif method == 'exact_bruteforce':
            result = solve_exact_bruteforce(problem)
        elif method == 'simulated_annealing':
            result = solve_simulated_annealing(problem)
        elif method == 'random_restarts':
            result = solve_random_restarts(problem)
        else:
            return jsonify({'error': f'Unknown method: {method}'}), 400
        
        # Convert result to JSON
        result_dict = asdict(result)
        
        # Add selected coalition details
        selected_details = []
        for idx in result.selected:
            node = problem.nodes[idx]
            selected_details.append({
                'index': idx,
                'robots': list(node.robots),
                'task_id': node.task_id,
                'utility': node.utility,
                'label': node.label
            })
        result_dict['selected_details'] = selected_details
        
        # Add problem metadata
        result_dict['node_count'] = problem.node_count
        result_dict['edge_count'] = len(problem.edges)
        
        return jsonify(result_dict)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/solve-all', methods=['POST'])
def solve_all():
    """
    Run all solvers on the same problem and return comparison.
    Returns best result first.
    """
    try:
        data = request.json
        coalition_bound = int(data.get('coalition_bound', 3))
        lambda_penalty = float(data.get('lambda_penalty', 8.0))
        
        # Build MRTA instance
        instance = build_instance_from_request(data)
        
        # Build MWIS problem
        problem = build_mwis_problem(instance, coalition_bound, lambda_penalty)
        
        results = {}
        methods = ['greedy_mwis', 'kuramoto_oim', 'exact_bruteforce', 'simulated_annealing', 'random_restarts']
        
        # Handle exact solver gracefully
        if problem.node_count > 22:
            methods.remove('exact_bruteforce')
        
        for method in methods:
            try:
                if method == 'greedy_mwis':
                    result = solve_greedy_mwis(problem)
                elif method == 'kuramoto_oim':
                    result = solve_kuramoto_oim(problem)
                elif method == 'exact_bruteforce':
                    result = solve_exact_bruteforce(problem)
                elif method == 'simulated_annealing':
                    result = solve_simulated_annealing(problem)
                elif method == 'random_restarts':
                    result = solve_random_restarts(problem)
                
                result_dict = asdict(result)
                result_dict['selected_details'] = [
                    {
                        'index': idx,
                        'robots': list(problem.nodes[idx].robots),
                        'task_id': problem.nodes[idx].task_id,
                        'utility': problem.nodes[idx].utility,
                        'label': problem.nodes[idx].label
                    }
                    for idx in result.selected
                ]
                results[method] = result_dict
            except Exception as e:
                results[method] = {'error': str(e), 'runtime_ms': -1}
        
        # Sort by utility (descending) and add metadata
        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1].get('utility', -1000),
            reverse=True
        )
        
        return jsonify({
            'problem_size': problem.node_count,
            'edge_count': len(problem.edges),
            'coalition_bound': coalition_bound,
            'lambda_penalty': lambda_penalty,
            'results': {k: v for k, v in sorted_results}
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
