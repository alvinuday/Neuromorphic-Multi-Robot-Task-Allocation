"""
QUBO to Ising Hamiltonian Mapping

Converts QUBO binary problem to Ising spin formulation via the substitution:
    x_k = (1 + s_k)/2,  s_k ∈ {-1, +1}

Ising Hamiltonian (Blueprint §4.5):
    H = Σᵢ hᵢ·sᵢ + Σ_{(i,j)∈E} Jᵢⱼ·sᵢ·sⱼ

Ising parameters derived from QUBO (Blueprint §4.5):
    hₖ = -wₖ/2 + (λ·degₑ(k))/4
    Jᵢⱼ = λ/4  for all (i,j) ∈ E

Sign convention (CRITICAL — Blueprint §4.6):
    Kᵢⱼ = -2·Jᵢⱼ  (couples to OIM dynamics)
    Iᵢ = -hᵢ      (couples to OIM injection current)

This ensures:
- Conflict edges have anti-ferromagnetic coupling (Kᵢⱼ < 0)
- High-utility nodes have attractive injection (Iᵢ < 0 → phase ≈ 0)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Sequence


@dataclass
class IsingHamiltonian:
    """Ising problem representation.

    Attributes:
        h_field: External field h_k for each spin (size N)
        J_coupling: Coupling matrix J_ij (size N×N)
        adjacency: Adjacency list of coupled pairs
        node_count: Number of spins
        lambda_penalty: Original QUBO penalty (for reference)
        utilities: Original node utilities (for reference)
    """
    h_field: np.ndarray  # shape (N,)
    J_coupling: np.ndarray  # shape (N, N)
    adjacency: tuple[tuple[int, ...], ...]
    node_count: int
    lambda_penalty: float
    utilities: np.ndarray  # shape (N,)


def qubo_to_ising(
    utilities: Sequence[float],
    edges: Sequence[tuple[int, int]],
    lambda_penalty: float,
) -> IsingHamiltonian:
    """Convert QUBO problem to Ising Hamiltonian form.

    Performs the substitution x_k = (1 + s_k)/2 on the QUBO objective:
        Q(x) = -Σᵢ wᵢ·xᵢ + λ·Σ_{(i,j)∈E} xᵢ·xⱼ

    Expanding and collecting terms gives the Ising energy:
        H(s) = Σᵢ hᵢ·sᵢ + Σ_{(i,j)∈E} Jᵢⱼ·sᵢ·sⱼ + const

    where:
        hₖ = -wₖ/2 + (λ·degₑ(k))/4
        Jᵢⱼ = λ/4

    Args:
        utilities: Node weights w_i (positive)
        edges: Conflict edges as list of (i, j) with i < j
        lambda_penalty: QUBO penalty coefficient λ

    Returns:
        IsingHamiltonian with h_field, J_coupling, adjacency
    """
    utilities = np.array(utilities, dtype=np.float64)
    N = len(utilities)

    # Initialize Ising parameters
    h_field = np.zeros(N, dtype=np.float64)
    J_coupling = np.zeros((N, N), dtype=np.float64)

    # Build adjacency list for reference
    adjacency_lists = [[] for _ in range(N)]

    # Compute external field: h_k = -w_k/2 + (λ·deg(k))/4
    # First, count degree of each node in conflict graph
    degrees = np.zeros(N, dtype=np.int32)
    for i, j in edges:
        if not (0 <= i < N and 0 <= j < N):
            raise ValueError(f"Edge ({i}, {j}) out of range [0, {N})")
        degrees[i] += 1
        degrees[j] += 1

    # Compute h_field with correct sign
    for k in range(N):
        h_field[k] = -utilities[k] / 2.0 + (lambda_penalty * degrees[k]) / 4.0

    # Coupling: J_ij = λ/4 for all edges
    J_val = lambda_penalty / 4.0
    for i, j in edges:
        if i > j:
            i, j = j, i
        J_coupling[i, j] = J_val
        J_coupling[j, i] = J_val
        adjacency_lists[i].append(j)
        adjacency_lists[j].append(i)

    # Convert adjacency lists to tuple of tuples
    adjacency = tuple(tuple(sorted(set(adj))) for adj in adjacency_lists)

    return IsingHamiltonian(
        h_field=h_field,
        J_coupling=J_coupling,
        adjacency=adjacency,
        node_count=N,
        lambda_penalty=lambda_penalty,
        utilities=utilities,
    )


def ising_to_oim_parameters(ising: IsingHamiltonian) -> tuple[np.ndarray, np.ndarray]:
    """Map Ising parameters to OIM hardware parameters.

    OIM dynamics (Blueprint §4.6):
        dθᵢ/dt = Kᵢᵢ·sin(2θᵢ) + Σⱼ Kᵢⱼ·sin(θⱼ - θᵢ) + ξᵢ(t)

    Mapping (Blueprint §4.6):
        Kᵢⱼ = -2·Jᵢⱼ     (coupling)
        Iᵢ = -hᵢ        (injection bias current)

    The negative signs are CRITICAL:
    - Conflict edges (Jᵢⱼ > 0) become Kᵢⱼ < 0 (anti-ferromagnetic)
    - High-utility nodes (hᵢ > 0) become Iᵢ < 0 (attractive to phase ≈ 0)

    Args:
        ising: IsingHamiltonian object

    Returns:
        (K_coupling, I_bias) where:
        - K_coupling: N×N coupling matrix for OIM
        - I_bias: N external injection currents
    """
    N = ising.node_count

    # K_ij = -2 * J_ij
    K_coupling = -2.0 * ising.J_coupling

    # I_bias = -h_i (external current / injection strength)
    I_bias = -ising.h_field

    # Validate signs
    # Conflict edges should have K_ij < 0 (anti-ferromagnetic)
    for i, j in zip(*np.where(ising.J_coupling > 0)):
        if i >= j:
            continue  # Skip lower triangle (symmetric matrix)
        if K_coupling[i, j] >= 0:
            raise ValueError(
                f"Coupling K[{i},{j}] = {K_coupling[i,j]} should be negative "
                f"(derived from J[{i},{j}] = {ising.J_coupling[i,j]})"
            )

    return K_coupling, I_bias


def verify_ising_derivation(
    utilities: Sequence[float],
    edges: Sequence[tuple[int, int]],
    lambda_penalty: float,
    verbose: bool = False,
) -> dict:
    """Verify Ising mapping derivation by checking algebraic identities.

    Verifies:
    1. h_k sign: utility contribution is -w_k/2 (negative)
    2. degree term: +λ·deg(k)/4 increases h_k for high-degree nodes
    3. J_ij coupling: always λ/4 (positive)
    4. Anti-ferromagnetic: K_ij = -2·J_ij < 0

    Args:
        utilities: Node weights
        edges: Conflict edges
        lambda_penalty: QUBO penalty
        verbose: Print diagnostic

    Returns:
        Verification result dictionary
    """
    ising = qubo_to_ising(utilities, edges, lambda_penalty)
    K_coupling, I_bias = ising_to_oim_parameters(ising)

    utilities = np.array(utilities)
    N = len(utilities)
    degrees = np.zeros(N, dtype=int)
    for i, j in edges:
        degrees[i] += 1
        degrees[j] += 1

    violations = []

    # Check h_field signs and values
    for k in range(N):
        # Expected: h_k = -w_k/2 + λ*deg(k)/4
        expected = -utilities[k] / 2.0 + (lambda_penalty * degrees[k]) / 4.0
        actual = ising.h_field[k]
        if not np.isclose(actual, expected):
            violations.append(
                f"h[{k}] = {actual}, expected {expected}"
            )

        # Check utility contribution dominates for isolated nodes
        if degrees[k] == 0:
            if ising.h_field[k] >= 0:  # High utility nodes should have h < 0
                if utilities[k] > 0:
                    violations.append(
                        f"h[{k}] = {ising.h_field[k]} should be negative "
                        f"(utility w={utilities[k]})"
                    )

    # Check J_ij coupling values
    for i, j in edges:
        if not np.isclose(ising.J_coupling[i, j], lambda_penalty / 4.0):
            violations.append(
                f"J[{i},{j}] = {ising.J_coupling[i,j]}, "
                f"expected {lambda_penalty / 4.0}"
            )

    # Check K_ij = -2*J_ij mapping
    for i, j in edges:
        expected_K = -2.0 * ising.J_coupling[i, j]
        actual_K = K_coupling[i, j]
        if not np.isclose(actual_K, expected_K):
            violations.append(
                f"K[{i},{j}] = {actual_K}, expected {expected_K}"
            )
        # Anti-ferromagnetic check
        if K_coupling[i, j] >= 0:
            violations.append(
                f"K[{i},{j}] = {K_coupling[i,j]} should be negative "
                f"(anti-ferromagnetic)"
            )

    # Check I_bias = -h_i mapping
    for i in range(N):
        expected_I = -ising.h_field[i]
        actual_I = I_bias[i]
        if not np.isclose(actual_I, expected_I):
            violations.append(
                f"I[{i}] = {actual_I}, expected {expected_I}"
            )

    result = {
        'valid': len(violations) == 0,
        'violations': violations,
        'h_field_stats': {
            'min': float(np.min(ising.h_field)),
            'max': float(np.max(ising.h_field)),
            'mean': float(np.mean(ising.h_field)),
        },
        'J_coupling_stats': {
            'min': float(np.min(ising.J_coupling[ising.J_coupling > 0])),
            'max': float(np.max(ising.J_coupling[ising.J_coupling > 0])),
            'nonzero_count': int(np.count_nonzero(ising.J_coupling)),
        },
        'K_coupling_stats': {
            'min': float(np.min(K_coupling[K_coupling < 0])),
            'max': float(np.max(K_coupling[K_coupling < 0])),
            'all_negative': bool(np.all(K_coupling[K_coupling != 0] < 0)),
        },
    }

    if verbose:
        print("Ising Derivation Verification:")
        print(f"  Valid: {result['valid']}")
        if violations:
            print(f"  Violations ({len(violations)}):")
            for v in violations:
                print(f"    - {v}")
        print(f"  h_field stats: {result['h_field_stats']}")
        print(f"  J_coupling stats: {result['J_coupling_stats']}")
        print(f"  K_coupling stats: {result['K_coupling_stats']}")

    return result


def print_ising_parameters(ising: IsingHamiltonian, precision: int = 4):
    """Pretty-print Ising parameters.

    Args:
        ising: IsingHamiltonian object
        precision: Decimal places
    """
    N = ising.node_count

    print(f"Ising Hamiltonian ({N} spins):")
    print(f"λ = {ising.lambda_penalty}")
    print()

    # External fields
    print("External Fields h_k:")
    print("  k    w_k   deg(k)    h_k")
    print("  " + "-" * 35)
    degrees = np.zeros(N, dtype=int)
    for i, j in zip(*np.where(ising.J_coupling > 0)):
        if i < j:
            degrees[i] += 1
            degrees[j] += 1

    for k in range(N):
        print(f"  {k:2d}  {ising.utilities[k]:6.2f}    {degrees[k]:2d}    "
              f"{ising.h_field[k]:8.4f}")

    # Couplings
    couplings = [(i, j, ising.J_coupling[i, j])
                 for i, j in zip(*np.where(ising.J_coupling > 0))
                 if i < j]
    if couplings:
        print()
        print("Couplings J_ij:")
        print("  (i,j)      J_ij")
        print("  " + "-" * 20)
        for i, j, Jval in sorted(couplings):
            print(f"  ({i},{j})    {Jval:8.4f}")
