"""
Hardware performance profiles for comparing neuromorphic vs classical computing.
Includes OIM, Intel Loihi, and multiple CPU architectures.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import math


@dataclass(frozen=True)
class HardwareProfile:
    """Base class for hardware performance specifications."""
    name: str
    description: str
    energy_per_solve_mJ: float  # millijoules for one solve
    latency_ms: float  # milliseconds per solve
    power_W: float  # instantaneous power consumption (watts)

    def energy_per_quality_point(self, quality: float) -> float:
        """Energy efficiency: energy cost per unit quality gained."""
        if quality <= 0:
            return float('inf')
        return self.energy_per_solve_mJ / quality


@dataclass(frozen=True)
class OIMHardware(HardwareProfile):
    """Oscillator Ising Machine (neuromorphic) hardware profile."""
    oscillator_count: int = 100
    clock_freq_GHz: float = 2.0
    settling_time_us: float = 100.0
    coupling_overhead_us: float = 10.0
    voltage_V: float = 0.8
    capacitance_pF: float = 1.0

    @classmethod
    def from_node_count(cls, node_count: int) -> OIMHardware:
        """Create OIM profile scaled to problem size."""
        oscillator_count = max(128, (node_count + 31) // 32 * 32)  # Round to 32

        # Latency increases with problem size (settling time scales ~O(log N))
        settling_time = 100.0 + 20.0 * math.log2(max(1, node_count / 10))

        # Energy: P = α·C·V²·f (capacitive) + leakage
        # Assume ~1-2 mW per 100 oscillators
        capacitive_energy = 0.5 * oscillator_count * (settling_time / 1000)  # mJ
        leakage_energy = 0.1 * oscillator_count * (settling_time / 1000)  # mJ
        total_energy = capacitive_energy + leakage_energy

        # Power during active solve: V²·f·C·N
        active_power = 1.5 * (oscillator_count / 100) if oscillator_count > 0 else 1.5

        # Latency: settling + coupling overhead
        total_latency = settling_time + (oscillator_count / 10)  # μs

        return cls(
            name=f"OIM_{node_count}nodes",
            description=f"Oscillator Ising Machine for {node_count}-node problems",
            energy_per_solve_mJ=total_energy,
            latency_ms=total_latency / 1000,  # convert to ms
            power_W=active_power,
            oscillator_count=oscillator_count,
            settling_time_us=settling_time,
        )


@dataclass(frozen=True)
class LoihiHardware(HardwareProfile):
    """Intel Loihi neuromorphic processor (reference profile)."""
    core_count: int = 128
    neuron_per_core: int = 1000
    clock_freq_MHz: float = 1.0  # Neuromorphic clock

    @classmethod
    def default(cls) -> LoihiHardware:
        """Standard Loihi chip specifications (from Davies et al. 2018)."""
        return cls(
            name="Intel_Loihi",
            description="Intel Loihi neuromorphic processor (128 cores, 128k neurons)",
            energy_per_solve_mJ=85.0,  # ~85 mJ for ~128ms solve (100mW active @ 128ms)
            latency_ms=128.0,  # 128 timesteps @ 1MHz = 128 ms
            power_W=0.085,  # ~85 mW average during solve
            core_count=128,
            neuron_per_core=1000,
        )


@dataclass(frozen=True)
class CPUHardware(HardwareProfile):
    """Classical CPU hardware profiles."""
    tdp_W: float  # Thermal Design Power
    gips: float  # Giga-Instructions Per Second
    ipc: float = 2.0  # Instructions per clock cycle

    @classmethod
    def laptop_i7(cls) -> CPUHardware:
        """Intel Core i7 (11th gen, laptop)."""
        return cls(
            name="Intel_i7_11gen",
            description="Intel Core i7-1185G7 (4 cores, ~45W TDP)",
            energy_per_solve_mJ=45.0,  # 45W × 1s average (worst case if problem takes ~1s)
            latency_ms=500.0,  # ILP/BnB typically 100-1000ms for thesis-scale MWIS
            power_W=45.0,
            tdp_W=45.0,
            gips=20.0,
        )

    @classmethod
    def server_xeon(cls) -> CPUHardware:
        """Intel Xeon E5-2690 (server grade)."""
        return cls(
            name="Intel_Xeon_E5",
            description="Intel Xeon E5-2690v2 (10 cores, ~130W TDP)",
            energy_per_solve_mJ=10.0,  # Faster solver (10ms) on server CPU
            latency_ms=10.0,  # Server CPU ~10-20ms for small MWIS
            power_W=130.0,
            tdp_W=130.0,
            gips=80.0,
        )

    @classmethod
    def arm_jetson(cls) -> CPUHardware:
        """NVIDIA Jetson Orin Nano (ARM-based edge device)."""
        return cls(
            name="NVIDIA_Jetson_Orin",
            description="NVIDIA Jetson Orin Nano (12-core ARM, ~15W TDP)",
            energy_per_solve_mJ=7.5,  # 15W × 500ms (slower but energy-efficient)
            latency_ms=500.0,  # ARM slower at MWIS solving
            power_W=15.0,
            tdp_W=15.0,
            gips=50.0,
        )


def get_default_hardware_profiles() -> dict[str, HardwareProfile]:
    """Return standard hardware profile comparison set."""
    return {
        "oim_30": OIMHardware.from_node_count(30),
        "oim_100": OIMHardware.from_node_count(100),
        "loihi": LoihiHardware.default(),
        "cpu_laptop_i7": CPUHardware.laptop_i7(),
        "cpu_server_xeon": CPUHardware.server_xeon(),
        "cpu_arm_jetson": CPUHardware.arm_jetson(),
    }


def compare_hardware_for_problem(
    node_count: int,
    solver_runtimes_ms: dict[str, float],
) -> dict[str, dict[str, float]]:
    """
    Compare hardware profiles for a specific problem.

    Args:
        node_count: MWIS problem size
        solver_runtimes_ms: {solver_name: runtime_ms} for classical solvers

    Returns:
        {hardware_name: {"energy_mJ": ..., "latency_ms": ..., "power_W": ...}}
    """
    profiles = {
        "OIM": OIMHardware.from_node_count(node_count),
        "Loihi": LoihiHardware.default(),
        "CPU i7 (ILP)": CPUHardware.laptop_i7(),
        "CPU i7 (BnB)": CPUHardware.laptop_i7(),
        "Xeon (ILP)": CPUHardware.server_xeon(),
        "Xeon (BnB)": CPUHardware.server_xeon(),
        "Jetson (ILP)": CPUHardware.arm_jetson(),
        "Jetson (BnB)": CPUHardware.arm_jetson(),
    }

    # Scale CPU energy based on actual solver runtime
    def scale_cpu_profile(base_profile: CPUHardware, actual_runtime_ms: float) -> dict:
        # Energy = Power × Time
        energy = (base_profile.power_W * actual_runtime_ms) / 1000  # convert ms to s, then J to mJ
        return {
            "energy_mJ": energy,
            "latency_ms": actual_runtime_ms,
            "power_W": base_profile.power_W,
            "efficiency_mJ_per_quality": "TBD",
        }

    results = {}

    # OIM is problem-size dependent
    oim = profiles["OIM"]
    results["OIM"] = {
        "energy_mJ": oim.energy_per_solve_mJ,
        "latency_ms": oim.latency_ms,
        "power_W": oim.power_W,
        "efficiency_mJ_per_quality": "high",
    }

    # Loihi is constant regardless
    loihi = profiles["Loihi"]
    results["Loihi"] = {
        "energy_mJ": loihi.energy_per_solve_mJ,
        "latency_ms": loihi.latency_ms,
        "power_W": loihi.power_W,
        "efficiency_mJ_per_quality": "medium",
    }

    # CPUs scale by actual solver time
    cpu_variants = ["CPU i7 (ILP)", "CPU i7 (BnB)", "Xeon (ILP)", "Xeon (BnB)", "Jetson (ILP)", "Jetson (BnB)"]
    for variant in cpu_variants:
        if "ILP" in variant:
            solver_time = solver_runtimes_ms.get("ilp_mwis", 5000.0)
        else:  # BnB
            solver_time = solver_runtimes_ms.get("branch_and_bound_mwis", 1000.0)

        if "i7" in variant:
            profile = profiles["CPU i7 (ILP)"]
        elif "Xeon" in variant:
            profile = profiles["Xeon (ILP)"]
        else:
            profile = profiles["Jetson (ILP)"]

        results[variant] = scale_cpu_profile(profile, solver_time)

    return results
