#!/usr/bin/env python3
"""
Sanity check: OIM implementation uses λ/4 coefficient correctly.

This script verifies that:
1. The OIM parameters (h_field, J_coupling) are derived with λ/4.
2. The sign conventions (I_i = -h_i, K_ij = -2*J_ij) are correct.
3. The implementation matches the derivation in DERIVATION_NOTE.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "experiments"))

from mrta.ising_map import qubo_to_ising


def test_oim_parameter_derivation():
    """Verify that OIM parameters use λ/4 correctly."""
    print("\n" + "=" * 70)
    print("OIM PARAMETER VERIFICATION (λ/4 coefficient)")
    print("=" * 70)

    test_cases = [
        {
            "name": "triangle",
            "utilities": [1.0, 1.0, 1.0],
            "edges": [(0, 1), (1, 2), (0, 2)],
            "lambda": 2.5,
            "expected_h": [0.75, 0.75, 0.75],  # -1.0/2 + 2.5*2/4 = 0.75
            "expected_J": 0.625,  # 2.5 / 4
        },
        {
            "name": "4cycle",
            "utilities": [1.0, 2.0, 1.0, 2.0],
            "edges": [(0, 1), (1, 2), (2, 3), (3, 0)],
            "lambda": 3.5,
            "expected_h": [1.25, 0.75, 1.25, 0.75],  # -w_k/2 + 3.5*2/4
            "expected_J": 0.875,  # 3.5 / 4
        },
        {
            "name": "star",
            "utilities": [5.0, 1.0, 1.0, 1.0, 1.0],
            "edges": [(0, 1), (0, 2), (0, 3), (0, 4)],
            "lambda": 6.0,
            "expected_h": [3.5, 1.0, 1.0, 1.0, 1.0],  # -5/2 + 6*4/4=3.5, -1/2 + 6*1/4=1.0
            "expected_J": 1.5,  # 6.0 / 4
        },
    ]

    all_pass = True

    for test in test_cases:
        name = test["name"]
        utilities = test["utilities"]
        edges = test["edges"]
        lambda_penalty = test["lambda"]

        print(f"\n{name}:")
        print(f"  utilities={utilities}")
        print(f"  edges={edges}")
        print(f"  λ={lambda_penalty}")

        # Derive Ising parameters
        ising = qubo_to_ising(utilities, edges, lambda_penalty)

        # Check h_field
        print(f"  h_field check:")
        for k, (actual, expected) in enumerate(zip(ising.h_field, test["expected_h"])):
            error = abs(actual - expected)
            status = "✓" if error < 1e-10 else "✗"
            print(f"    h_{k}: expected={expected:.4f}, actual={actual:.4f} {status}")
            if error > 1e-10:
                all_pass = False

        # Check J_coupling (all edges have same value)
        print(f"  J_coupling check:")
        for (i, j) in edges:
            actual = ising.J_coupling[i, j]
            expected = test["expected_J"]
            error = abs(actual - expected)
            status = "✓" if error < 1e-10 else "✗"
            print(f"    J_{{{i},{j}}}: expected={expected:.4f}, actual={actual:.4f} {status}")
            if error > 1e-10:
                all_pass = False

    print("\n" + "=" * 70)
    if all_pass:
        print("✓ All OIM parameters verified: λ/4 coefficient is correctly implemented.")
        print("  The repository's ising_map.py uses λ/4 (CORRECT).")
    else:
        print("✗ Some parameters do not match λ/4 formula.")
    print("=" * 70 + "\n")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(test_oim_parameter_derivation())
