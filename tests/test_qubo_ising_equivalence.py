"""
Regression tests for QUBO ↔ Ising equivalence.

Tests that:
1. λ/4 coefficient produces exact energy equivalence.
2. λ/2 coefficient fails with predictable residuals.
3. Optimal solutions agree across formulations when λ > max(w_i + w_j).
4. Real MRTA instances verify correctly.
"""

import pytest
import numpy as np
from pathlib import Path
from itertools import product

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "experiments"))

from oim_sim.solvers.exact import solve_exact_bruteforce
from mrta.ising_map import qubo_to_ising
from oim_sim.types import MWISProblem


def compute_qubo_unconstrained(x, utilities, edges, lambda_penalty):
    """Compute Q(x) = -Σ w_k x_k + λ Σ x_i x_j."""
    q = -np.sum(utilities * x)
    for i, j in edges:
        q += lambda_penalty * x[i] * x[j]
    return q


def compute_ising_energy(s, h_field, J_coupling, const=0.0):
    """Compute H(s) = Σ h_k s_k + Σ J_ij s_i s_j + const."""
    h_energy = np.sum(h_field * s)
    j_energy = 0.5 * np.sum(J_coupling * np.outer(s, s))
    return h_energy + j_energy + const


def compute_constant_shift(utilities, edges, lambda_penalty):
    """Constant term in QUBO → Ising substitution."""
    return -np.sum(utilities) / 2 + lambda_penalty * len(edges) / 4


class TestQuboToIsingEquivalence:
    """Test QUBO ↔ Ising equivalence with λ/4."""

    @pytest.mark.parametrize(
        "name,utilities,edges,lambda_penalty",
        [
            # Triangle
            (
                "triangle",
                [1.0, 1.0, 1.0],
                [(0, 1), (1, 2), (0, 2)],
                2.5,
            ),
            # 4-cycle
            (
                "4cycle",
                [1.0, 2.0, 1.0, 2.0],
                [(0, 1), (1, 2), (2, 3), (3, 0)],
                3.5,
            ),
            # Star
            (
                "star",
                [5.0, 1.0, 1.0, 1.0, 1.0],
                [(0, 1), (0, 2), (0, 3), (0, 4)],
                6.0,
            ),
            # Complete graph K_4
            (
                "k4",
                [1.0, 2.0, 1.5, 0.5],
                [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
                4.0,
            ),
        ],
    )
    def test_energy_equivalence_lambda4(self, name, utilities, edges, lambda_penalty):
        """Test that Q(x) = H_λ/4(s) + const for all assignments."""
        utilities = np.array(utilities)
        n = len(utilities)

        # Compute Ising parameters with λ/4
        ising = qubo_to_ising(utilities, edges, lambda_penalty)
        h_field = ising.h_field
        J_coupling = ising.J_coupling
        const = compute_constant_shift(utilities, edges, lambda_penalty)

        # Brute force enumeration
        for x_tuple in product([0, 1], repeat=n):
            x = np.array(x_tuple, dtype=np.float64)
            s = 2 * x - 1

            q = compute_qubo_unconstrained(x, utilities, edges, lambda_penalty)
            h = compute_ising_energy(s, h_field, J_coupling, const)

            # Energy equivalence: max error should be < 1e-10
            residual = abs(q - h)
            assert residual < 1e-10, (
                f"Energy mismatch in {name}: "
                f"Q(x)={q:.6e}, H(s)={h:.6e}, residual={residual:.6e}"
            )

    @pytest.mark.parametrize(
        "name,utilities,edges,lambda_penalty",
        [
            ("triangle", [1.0, 1.0, 1.0], [(0, 1), (1, 2), (0, 2)], 2.5),
            ("4cycle", [1.0, 2.0, 1.0, 2.0], [(0, 1), (1, 2), (2, 3), (3, 0)], 3.5),
            ("star", [5.0, 1.0, 1.0, 1.0, 1.0], [(0, 1), (0, 2), (0, 3), (0, 4)], 6.0),
        ],
    )
    def test_lambda2_fails_systematically(self, name, utilities, edges, lambda_penalty):
        """Test that λ/2 fails with large, systematic residuals."""
        utilities = np.array(utilities)
        n = len(utilities)
        const = compute_constant_shift(utilities, edges, lambda_penalty)

        # Compute degree of each node
        degrees = np.zeros(n, dtype=int)
        for i, j in edges:
            degrees[i] += 1
            degrees[j] += 1

        # Build incorrect λ/2 parameters
        h_field_lambda2 = -utilities / 2 + lambda_penalty * degrees / 2
        J_coupling_lambda2 = np.zeros((n, n))
        for i, j in edges:
            J_coupling_lambda2[i, j] = lambda_penalty / 2
            J_coupling_lambda2[j, i] = lambda_penalty / 2

        # Check that λ/2 produces non-zero residuals
        residuals = []
        for x_tuple in product([0, 1], repeat=n):
            x = np.array(x_tuple, dtype=np.float64)
            s = 2 * x - 1

            q = compute_qubo_unconstrained(x, utilities, edges, lambda_penalty)
            h_lambda2 = compute_ising_energy(s, h_field_lambda2, J_coupling_lambda2, const)

            actual = abs(q - h_lambda2)
            residuals.append(actual)

        # λ/2 should produce significant residuals (> 1.0)
        max_residual = max(residuals)
        assert max_residual > 1.0, (
            f"λ/2 should fail but max residual is only {max_residual}"
        )

    @pytest.mark.parametrize(
        "name,utilities,edges,lambda_penalty",
        [
            ("triangle", [1.0, 1.0, 1.0], [(0, 1), (1, 2), (0, 2)], 2.5),
            ("4cycle", [1.0, 2.0, 1.0, 2.0], [(0, 1), (1, 2), (2, 3), (3, 0)], 3.5),
            ("star", [5.0, 1.0, 1.0, 1.0, 1.0], [(0, 1), (0, 2), (0, 3), (0, 4)], 6.0),
        ],
    )
    def test_argmin_agreement(self, name, utilities, edges, lambda_penalty):
        """Test that argmin(Q) = argmin(H_λ/4) when λ is sufficiently large."""
        utilities = np.array(utilities)
        n = len(utilities)

        # Compute Ising parameters
        ising = qubo_to_ising(utilities, edges, lambda_penalty)
        h_field = ising.h_field
        J_coupling = ising.J_coupling
        const = compute_constant_shift(utilities, edges, lambda_penalty)

        # Find argmin for Q and H
        argmin_q = None
        argmin_h = None
        min_q = np.inf
        min_h = np.inf

        for x_tuple in product([0, 1], repeat=n):
            x = np.array(x_tuple, dtype=np.float64)
            s = 2 * x - 1

            q = compute_qubo_unconstrained(x, utilities, edges, lambda_penalty)
            h = compute_ising_energy(s, h_field, J_coupling, const)

            if q < min_q:
                min_q = q
                argmin_q = x_tuple

            if h < min_h:
                min_h = h
                argmin_h = x_tuple

        assert argmin_q == argmin_h, (
            f"argmin mismatch in {name}: "
            f"argmin(Q)={argmin_q}, argmin(H)={argmin_h}"
        )


class TestHandshakeLemma:
    """Test the critical handshake identity used in the derivation."""

    def test_handshake_identity_triangle(self):
        """Test that Σ_E (s_i + s_j) = Σ_k deg(k) s_k for a triangle."""
        edges = [(0, 1), (1, 2), (0, 2)]
        degrees = np.array([2, 2, 2])

        for s_tuple in product([-1, 1], repeat=3):
            s = np.array(s_tuple)

            # LHS: sum over edges
            lhs = sum(s[i] + s[j] for i, j in edges)

            # RHS: sum with degrees
            rhs = np.sum(degrees * s)

            assert lhs == rhs, (
                f"Handshake lemma fails for s={s}: "
                f"Σ_E (s_i + s_j)={lhs}, Σ deg(k)s_k={rhs}"
            )

    def test_handshake_identity_4cycle(self):
        """Test the lemma on a 4-cycle."""
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        degrees = np.array([2, 2, 2, 2])

        for s_tuple in product([-1, 1], repeat=4):
            s = np.array(s_tuple)

            lhs = sum(s[i] + s[j] for i, j in edges)
            rhs = np.sum(degrees * s)

            assert lhs == rhs


class TestRealWorldInstances:
    """Test on real MRTA instances (synthetic real)."""

    def test_3r2t_factory_instance(self):
        """Test a mock 3R2T factory task allocation scenario."""
        # Factory floor: 12 tasks, some conflicts
        utilities = np.array([2.5, 1.8, 3.2, 1.5, 2.1, 1.9, 2.8, 2.3, 1.6, 2.0, 2.5, 1.7])
        edges = [
            (0, 1), (0, 3), (1, 2), (1, 4), (2, 5), (3, 6), (3, 7),
            (4, 8), (5, 9), (6, 10), (7, 11), (8, 10), (9, 11),
        ]
        lambda_min = np.max(utilities) * 2
        lambda_penalty = lambda_min * 1.1

        # Test energy equivalence
        ising = qubo_to_ising(utilities, edges, lambda_penalty)
        h_field = ising.h_field
        J_coupling = ising.J_coupling
        const = compute_constant_shift(utilities, edges, lambda_penalty)

        n = len(utilities)
        max_residual = 0.0

        # Sample some assignments (full enumeration is 2^12 = 4096, manageable)
        for x_tuple in product([0, 1], repeat=min(n, 12)):
            x = np.array(list(x_tuple) + [0] * (n - min(n, 12)), dtype=np.float64)
            s = 2 * x - 1

            q = compute_qubo_unconstrained(x, utilities, edges, lambda_penalty)
            h = compute_ising_energy(s, h_field, J_coupling, const)

            residual = abs(q - h)
            max_residual = max(max_residual, residual)

            if residual > 1e-10:
                assert residual < 1e-10, f"Residual {residual} too large"

        # At least some should be exact
        assert max_residual < 1e-9


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
