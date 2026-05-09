"""
Tests for hardware profiling module.
Verifies hardware specifications and energy/latency calculations.
"""
import pytest
from src.oim_sim.hardware import (
    OIMHardware,
    LoihiHardware,
    CPUHardware,
    get_default_hardware_profiles,
    compare_hardware_for_problem,
)


def test_oim_hardware_profiles():
    """Test OIM hardware profile generation for various sizes."""
    for node_count in [10, 30, 100, 500]:
        profile = OIMHardware.from_node_count(node_count)
        assert profile.name == f"OIM_{node_count}nodes"
        assert profile.energy_per_solve_mJ > 0
        assert profile.latency_ms > 0
        assert profile.power_W > 0


def test_oim_latency_scales_with_size():
    """Test that OIM latency increases with problem size (sublinearly)."""
    latency_10 = OIMHardware.from_node_count(10).latency_ms
    latency_100 = OIMHardware.from_node_count(100).latency_ms
    latency_1000 = OIMHardware.from_node_count(1000).latency_ms

    assert latency_10 < latency_100 < latency_1000, \
        "OIM latency should increase with problem size"

    # Check sublinear scaling: latency should not increase linearly
    # Linear would be: latency_1000/latency_10 = 100 (10x -> 1000x)
    # Sublinear should be much less, e.g., 2-5x
    total_ratio = latency_1000 / latency_10
    assert total_ratio < 100, \
        f"OIM latency should scale sublinearly, got {total_ratio}x increase from 10 to 1000 nodes"


def test_loihi_hardware_profile():
    """Test Loihi hardware profile specification."""
    loihi = LoihiHardware.default()
    assert loihi.name == "Intel_Loihi"
    assert loihi.latency_ms == 128.0  # Fixed: 128 timesteps @ 1MHz
    assert loihi.power_W == 0.085  # ~85 mW


def test_cpu_hardware_profiles():
    """Test CPU hardware profile specifications."""
    i7 = CPUHardware.laptop_i7()
    xeon = CPUHardware.server_xeon()
    jetson = CPUHardware.arm_jetson()

    assert i7.power_W == 45.0
    assert xeon.power_W == 130.0
    assert jetson.power_W == 15.0

    # Xeon should be faster than laptop i7
    assert xeon.latency_ms < i7.latency_ms


def test_default_hardware_profiles():
    """Test that default hardware profiles are available."""
    profiles = get_default_hardware_profiles()
    assert len(profiles) >= 6, "Should have at least 6 default profiles"
    assert "oim_30" in profiles
    assert "loihi" in profiles
    assert "cpu_laptop_i7" in profiles
    assert "cpu_server_xeon" in profiles
    assert "cpu_arm_jetson" in profiles


def test_energy_efficiency_calculation():
    """Test energy efficiency (energy per quality point)."""
    profile = OIMHardware.from_node_count(50)
    quality = 10.0

    efficiency = profile.energy_per_quality_point(quality)
    assert efficiency > 0
    assert efficiency == profile.energy_per_solve_mJ / quality


def test_energy_efficiency_zero_quality():
    """Test that zero quality returns infinite efficiency."""
    profile = OIMHardware.from_node_count(50)
    efficiency = profile.energy_per_quality_point(0.0)
    assert efficiency == float('inf')


def test_compare_hardware_for_problem():
    """Test hardware comparison for a specific problem."""
    solver_runtimes = {
        "ilp_mwis": 500.0,
        "branch_and_bound_mwis": 100.0,
    }

    comparison = compare_hardware_for_problem(
        node_count=30,
        solver_runtimes_ms=solver_runtimes,
    )

    assert "OIM" in comparison
    assert "Loihi" in comparison
    assert "CPU i7 (ILP)" in comparison

    # Check OIM should be faster and more efficient than Loihi
    assert comparison["OIM"]["latency_ms"] < comparison["Loihi"]["latency_ms"], \
        "OIM should be faster than Loihi for real-time robotics"


def test_hardware_profiles_immutable():
    """Test that hardware profiles are frozen dataclasses."""
    profile = OIMHardware.from_node_count(50)
    with pytest.raises(AttributeError):
        profile.power_W = 999.0  # Should not be modifiable


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
