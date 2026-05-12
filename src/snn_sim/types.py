"""Types for SNN simulation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SpikeRecord:
    """Record of spikes from one neuron."""
    neuron_id: int
    spike_times_ms: list[float] = field(default_factory=list)

    @property
    def spike_count(self) -> int:
        return len(self.spike_times_ms)


@dataclass
class SNNSimResult:
    """Full simulation result."""
    n_neurons: int
    sim_time_ms: float
    dt_ms: float
    voltage_traces: list[list[float]]   # [neuron][timestep]
    spike_records: list[SpikeRecord]
    time_axis_ms: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)
