"""
Explicit QUBO Matrix Assembly

Converts MWIS problem (nodes with utilities and conflict edges) into QUBO form.

QUBO objective (Blueprint §4.4):
    Q(x) = x^T Q x = -Σᵢ wᵢ·xᵢ + λ·Σ_{(i,j)∈E} xᵢ·xⱼ

QUBO matrix format:
    Q_ii = -wᵢ                    (negative utility on diagonal)
    Q_ij = λ/2 for (i,j) ∈ E     (penalty coupling for conflicts)

Penalty bound (Blueprint §4.4 Theorem 4.1):
    If λ > max_{(i,j)∈E} (wᵢ + wⱼ), then QUBO minimizers are MWIS solutions.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Sequence


@dataclass
class QUBOMatrix:
    """QUBO problem representation.

    Attributes:
        Q: Full N×N QUBO matrix (symmetric)
        node_count: Number of binary variables
        utilities: Original node utilities (for reference)
        lambda_penalty: Penalty coefficient used
        edges: List of conflict edges as (i, j) pairs
    """
    Q: np.ndarray  # shape (N, N)
    node_count: int
    utilities: np.ndarray  # shape (N,)
    lambda_penalty: float
    edges: list[tuple[int, int]]


def assemble_qubo_matrix(
    utilities: Sequence[float],
    edges: Sequence[tuple[int, int]],
    lambda_penalty: float,
) -> QUBOMatrix:
    """Assemble QUBO matrix from utilities and conflict edges.

    Constructs the explicit N×N QUBO matrix Q where:
    - Q[i,i] = -utilities[i]
    - Q[i,j] = λ/2 for all (i,j) ∈ edges (conflicts)
    - Q is symmetric

    The objective being minimized is:
        x^T Q x = -Σᵢ wᵢ·xᵢ + λ·Σ_{(i,j)∈E} xᵢ·xⱼ

    Args:
        utilities: Node weights w_i (positive values)
        edges: Conflict edges as list of (i, j) pairs with i < j
        lambda_penalty: Penalty coefficient λ

    Returns:
        QUBOMatrix with assembled Q, utilities, edges, etc.

    Raises:
        ValueError: If utilities are invalid or edge indices out of range
    """
    utilities = np.array(utilities, dtype=np.float64)
    N = len(utilities)

    # Validate utilities
    if N == 0:
        raise ValueError("Cannot create QUBO with 0 nodes")
    if np.any(utilities < 0):
        raise ValueError("Utilities must be non-negative")

    # Initialize Q matrix (symmetric, dense)
    Q = np.zeros((N, N), dtype=np.float64)

    # Diagonal: -w_i
    np.fill_diagonal(Q, -utilities)

    # Off-diagonal: λ/2 for conflict edges
    penalty_half = lambda_penalty / 2.0
    edge_list = []

    for i, j in edges:
        if not (0 <= i < N and 0 <= j < N):
            raise ValueError(f"Edge ({i}, {j}) out of range [0, {N})")
        if i == j:
            raise ValueError(f"Self-loop ({i}, {i}) not allowed")

        # Enforce i < j for canonical form
        if i > j:
            i, j = j, i

        Q[i, j] += penalty_half
        Q[j, i] += penalty_half
        edge_list.append((i, j))

    return QUBOMatrix(
        Q=Q,
        node_count=N,
        utilities=utilities,
        lambda_penalty=lambda_penalty,
        edges=edge_list,
    )


def verify_qubo_signs(qubo: QUBOMatrix, verbose: bool = False) -> dict:
    """Verify QUBO matrix has correct signs and structure.

    Checks:
    - Diagonal entries Q[i,i] = -w_i (negative utilities)
    - Symmetric: Q[i,j] = Q[j,i]
    - Off-diagonal: Q[i,j] > 0 for conflict edges (penalty)
    - Off-diagonal: Q[i,j] = 0 for non-conflict pairs

    Args:
        qubo: QUBOMatrix to verify
        verbose: Print diagnostic info

    Returns:
        Dictionary with verification results
    """
    N = qubo.node_count
    Q = qubo.Q
    violations = []

    # Check diagonals
    for i in range(N):
        expected = -qubo.utilities[i]
        actual = Q[i, i]
        if not np.isclose(actual, expected):
            violations.append(f"Q[{i},{i}] = {actual}, expected {expected}")

    # Check symmetry
    for i in range(N):
        for j in range(i + 1, N):
            if not np.isclose(Q[i, j], Q[j, i]):
                violations.append(f"Q[{i},{j}] = {Q[i,j]} != Q[{j},{i}] = {Q[j,i]}")

    # Check penalties
    edges_set = set(qubo.edges)
    for i in range(N):
        for j in range(i + 1, N):
            if (i, j) in edges_set:
                if Q[i, j] <= 0:
                    violations.append(
                        f"Edge ({i},{j}) has non-positive penalty {Q[i,j]}"
                    )
            else:
                if not np.isclose(Q[i, j], 0):
                    violations.append(
                        f"Non-edge ({i},{j}) has non-zero entry {Q[i,j]}"
                    )

    result = {
        'valid': len(violations) == 0,
        'violations': violations,
        'diagonal_sum': float(np.sum(np.diag(Q))),
        'off_diagonal_sum': float(np.sum(Q) - np.sum(np.diag(Q))),
    }

    if verbose:
        print("QUBO Verification:")
        print(f"  Valid: {result['valid']}")
        if violations:
            print(f"  Violations ({len(violations)}):")
            for v in violations:
                print(f"    - {v}")
        print(f"  Diagonal sum: {result['diagonal_sum']:.6f}")
        print(f"  Off-diagonal sum: {result['off_diagonal_sum']:.6f}")

    return result


def evaluate_qubo(qubo: QUBOMatrix, x: Sequence[int]) -> float:
    """Evaluate QUBO objective for a binary vector.

    Computes: Q(x) = x^T Q x = Σᵢⱼ x_i Q_ij x_j

    Args:
        qubo: QUBOMatrix object
        x: Binary vector {0, 1}^N

    Returns:
        Objective value (float)
    """
    x = np.array(x, dtype=np.float64)
    return float(x @ qubo.Q @ x)


def verify_penalty_bound(qubo: QUBOMatrix, verbose: bool = False) -> dict:
    """Verify penalty coefficient satisfies Theorem 4.1.

    Theorem 4.1 (Blueprint §4.4):
    If λ > max_{(i,j)∈E} (w_i + w_j), then every QUBO minimizer
    is a feasible MWIS solution.

    Args:
        qubo: QUBOMatrix object
        verbose: Print diagnostic

    Returns:
        Dictionary with bound verification
    """
    if not qubo.edges:
        return {
            'satisfies_bound': True,
            'max_edge_weight_sum': 0.0,
            'lambda': qubo.lambda_penalty,
            'margin': float('inf'),
        }

    # Find max(w_i + w_j) over all edges
    max_sum = 0.0
    max_edge = None
    for i, j in qubo.edges:
        edge_sum = qubo.utilities[i] + qubo.utilities[j]
        if edge_sum > max_sum:
            max_sum = edge_sum
            max_edge = (i, j)

    satisfies = qubo.lambda_penalty > max_sum
    margin = qubo.lambda_penalty - max_sum

    result = {
        'satisfies_bound': satisfies,
        'max_edge_weight_sum': float(max_sum),
        'max_edge': max_edge,
        'lambda': qubo.lambda_penalty,
        'margin': float(margin),
    }

    if verbose:
        print("Penalty Bound Verification (Theorem 4.1):")
        print(f"  λ = {qubo.lambda_penalty}")
        print(f"  max(w_i + w_j) = {max_sum} (edge {max_edge})")
        print(f"  Satisfies λ > max: {satisfies}")
        print(f"  Margin: {margin:.6f}")

    return result


def print_qubo_matrix(qubo: QUBOMatrix, precision: int = 3):
    """Pretty-print QUBO matrix.

    Args:
        qubo: QUBOMatrix to print
        precision: Decimal places for rounding
    """
    Q = np.round(qubo.Q, precision)
    N = qubo.node_count

    print(f"QUBO Matrix ({N}×{N}):")
    print(f"λ = {qubo.lambda_penalty}")
    print(f"Edges: {len(qubo.edges)}")
    print()

    # Header
    print("     " + "".join(f"{i:>8}" for i in range(N)))
    print("    " + "-" * (8 * N + 2))

    # Rows
    for i in range(N):
        print(f"{i:>3} |", end="")
        for j in range(N):
            val = Q[i, j]
            print(f"{val:>8.3f}", end="")
        print()
