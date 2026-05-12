"""SNN-based MRTA solver using LIF neurons.

Each coalition node i maps to a LIF neuron.
- External drive I_ext_i = utility of coalition node i  (normalised to [0, 2])
- Inhibitory weight W_ij = -lambda for conflict edges
- Winning allocation = neurons with highest spike count forming independent set
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

import numpy as np

from .lif_neuron import LIFNeuron
from .types import SNNSimResult, SpikeRecord

# Problems with more nodes than this use the numpy-vectorised fast path
_NP_THRESHOLD = 40


@dataclass(frozen=True)
class SNNConfig:
    sim_time_ms: float = 200.0
    dt_ms: float = 0.1
    tau_ms: float = 20.0
    v_th: float = 1.0
    v_rest: float = 0.0
    r_mem: float = 1.0
    tau_ref_ms: float = 2.0
    inhibitory_weight: float = -2.0   # W_ij for conflict edges
    noise_amp: float = 0.05
    restarts: int = 5
    seed: int | None = None


@dataclass
class SNNResult:
    selected: list[int]
    utility: float
    feasible: bool
    runtime_ms: float
    spike_counts: list[int]
    sim_result: SNNSimResult | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def _select_from_spikes(
    spike_counts: list[int],
    adjacency: list[set[int]],
    utilities: list[float],
) -> list[int]:
    """Greedy MWIS extraction from spike counts.

    Sort neurons by spike count (descending), greedily add if no conflict.
    """
    order = sorted(range(len(spike_counts)), key=lambda i: spike_counts[i], reverse=True)
    selected: set[int] = set()
    for i in order:
        if spike_counts[i] == 0:
            continue
        if not any(j in selected for j in adjacency[i]):
            selected.add(i)
    return sorted(selected)


class SNNSolver:
    """LIF-SNN solver for MWIS/MRTA."""

    def __init__(self, cfg: SNNConfig | None = None) -> None:
        self.cfg = cfg or SNNConfig()

    def simulate(
        self,
        utilities: list[float],
        adjacency: list[set[int]],
        lambda_penalty: float,
        rng: random.Random | None = None,
        record_traces: bool = True,
    ) -> SNNSimResult:
        """Run one SNN simulation. Returns full trace data."""
        cfg = self.cfg
        n = len(utilities)
        if rng is None:
            rng = random.Random(cfg.seed)

        neurons = [
            LIFNeuron(
                neuron_id=i,
                tau_ms=cfg.tau_ms,
                v_th=cfg.v_th,
                v_rest=cfg.v_rest,
                r_mem=cfg.r_mem,
                tau_ref_ms=cfg.tau_ref_ms,
            )
            for i in range(n)
        ]

        n_steps = int(cfg.sim_time_ms / cfg.dt_ms)
        time_axis = [step * cfg.dt_ms for step in range(n_steps)]

        # Pre-build inhibitory weights
        # W_ij = inhibitory_weight if conflict, 0 otherwise
        inhibit_w = cfg.inhibitory_weight

        # voltage traces: only record every 10 steps to save memory
        record_every = max(1, n_steps // 1000)
        voltage_traces: list[list[float]] = [[] for _ in range(n)]
        recorded_times: list[float] = []

        # Track last spike for synaptic current (exponential kernel, decay 5ms)
        last_spike_t = [-9999.0] * n
        syn_decay = 5.0  # ms

        for step in range(n_steps):
            t = step * cfg.dt_ms

            # Compute synaptic currents from recent spikes
            syn_currents = [0.0] * n
            for j in range(n):
                if last_spike_t[j] > -9999.0:
                    age = t - last_spike_t[j]
                    if age < 5 * syn_decay:
                        s_j = rng.gauss(1.0, 0.1) * (age / cfg.dt_ms < 1.0 and 1.0 or 0.0)
                        # Use binary spike: 1 if just fired last step
                        pass  # handled below

            # Determine which neurons fired last step (for synaptic current)
            fired_last = [False] * n

            for i in range(n):
                if last_spike_t[i] >= t - cfg.dt_ms - 1e-9:
                    fired_last[i] = True

            # Compute total input current for each neuron
            for i in range(n):
                i_ext = utilities[i]
                i_syn = 0.0
                for j in range(n):
                    if fired_last[j] and j != i:
                        if i in adjacency[j]:
                            i_syn += inhibit_w
                i_noise = rng.gauss(0, cfg.noise_amp)
                i_total = i_ext + i_syn + i_noise

                fired = neurons[i].step(t, cfg.dt_ms, i_total)
                if fired:
                    last_spike_t[i] = t

            if record_traces and step % record_every == 0:
                recorded_times.append(t)
                for i in range(n):
                    voltage_traces[i].append(neurons[i].v)

        spike_records = [
            SpikeRecord(neuron_id=i, spike_times_ms=list(neurons[i].spike_times_ms))
            for i in range(n)
        ]

        return SNNSimResult(
            n_neurons=n,
            sim_time_ms=cfg.sim_time_ms,
            dt_ms=cfg.dt_ms,
            voltage_traces=voltage_traces,
            spike_records=spike_records,
            time_axis_ms=recorded_times,
        )

    def _simulate_numpy(
        self,
        utilities: list[float],
        adjacency: list[set[int]],
        lambda_penalty: float,
        rng: random.Random,
    ) -> "SNNSimResult":
        """Numpy-vectorised LIF simulation for large graphs.

        Uses Euler integration with dense inhibitory matrix.
        Same dynamics as the scalar path, but O(n²) via numpy matmul
        rather than Python double-loops.
        """
        cfg = self.cfg
        n = len(utilities)
        nprng = np.random.default_rng(rng.randint(0, 2**31))

        # Build inhibitory weight matrix
        W = np.zeros((n, n), dtype=np.float64)
        for i in range(n):
            for j in adjacency[i]:
                W[i, j] = cfg.inhibitory_weight

        i_ext = np.array(utilities, dtype=np.float64)
        n_steps = int(cfg.sim_time_ms / cfg.dt_ms)

        v = np.zeros(n, dtype=np.float64)
        refractory = np.zeros(n, dtype=np.float64)
        spike_counts = np.zeros(n, dtype=np.int32)
        fired = np.zeros(n, dtype=bool)

        # For SNNSimResult compat, build minimal spike records
        spike_times: list[list[float]] = [[] for _ in range(n)]
        record_every = max(1, n_steps // 500)
        voltage_traces: list[list[float]] = [[] for _ in range(n)]
        recorded_times: list[float] = []

        for step in range(n_steps):
            t = step * cfg.dt_ms
            refractory -= cfg.dt_ms
            refractory = np.maximum(refractory, 0.0)

            i_syn = W @ fired.astype(np.float64)
            i_noise = nprng.normal(0.0, cfg.noise_amp, n)
            i_total = i_ext + i_syn + i_noise

            active = refractory <= 0.0
            dv = (cfg.dt_ms / cfg.tau_ms) * (-v + cfg.r_mem * i_total)
            v = np.where(active, v + dv, v)

            fired = active & (v >= cfg.v_th)
            spike_counts += fired.astype(np.int32)
            for i in np.where(fired)[0]:
                spike_times[i].append(t)
            v = np.where(fired, cfg.v_rest, v)
            refractory = np.where(fired, cfg.tau_ref_ms, refractory)

            if step % record_every == 0:
                recorded_times.append(t)
                for i in range(n):
                    voltage_traces[i].append(float(v[i]))

        spike_records = [
            SpikeRecord(neuron_id=i, spike_times_ms=spike_times[i])
            for i in range(n)
        ]
        # Attach spike_counts as attribute for fast retrieval
        result = SNNSimResult(
            n_neurons=n,
            sim_time_ms=cfg.sim_time_ms,
            dt_ms=cfg.dt_ms,
            voltage_traces=voltage_traces,
            spike_records=spike_records,
            time_axis_ms=recorded_times,
        )
        # Store counts directly so solve() doesn't recount
        result._np_spike_counts = spike_counts.tolist()  # type: ignore[attr-defined]
        return result

    def solve(
        self,
        utilities: list[float],
        adjacency: list[set[int]],
        lambda_penalty: float,
    ) -> SNNResult:
        """Run multiple SNN restarts, return best result."""
        cfg = self.cfg
        rng = random.Random(cfg.seed)

        # Scale utilities so the maximum drive is 1.5× the firing threshold,
        # ensuring neurons actually spike regardless of raw utility magnitude.
        max_util = max(utilities) if utilities else 1.0
        if max_util > 0:
            scale = (cfg.v_th / cfg.r_mem) * 1.5 / max_util
            scaled_utilities = [u * scale for u in utilities]
        else:
            scaled_utilities = utilities

        use_numpy = len(utilities) > _NP_THRESHOLD

        t0 = perf_counter()
        best_utility = -1.0
        best_selected: list[int] = []
        best_spike_counts: list[int] = []
        best_sim: SNNSimResult | None = None

        for restart in range(cfg.restarts):
            if use_numpy:
                sim = self._simulate_numpy(scaled_utilities, adjacency, lambda_penalty, rng=rng)
                spike_counts = getattr(sim, "_np_spike_counts", [sr.spike_count for sr in sim.spike_records])
            else:
                sim = self.simulate(scaled_utilities, adjacency, lambda_penalty, rng=rng)
                spike_counts = [sr.spike_count for sr in sim.spike_records]
            selected = _select_from_spikes(spike_counts, adjacency, utilities)
            util = sum(utilities[i] for i in selected)

            if util > best_utility:
                best_utility = util
                best_selected = selected
                best_spike_counts = spike_counts
                best_sim = sim

        runtime_ms = (perf_counter() - t0) * 1000.0

        # Check feasibility (independent set)
        chosen = set(best_selected)
        feasible = all(
            not any(j in chosen for j in adjacency[i])
            for i in best_selected
        )

        return SNNResult(
            selected=best_selected,
            utility=best_utility,
            feasible=feasible,
            runtime_ms=runtime_ms,
            spike_counts=best_spike_counts,
            sim_result=best_sim,
            metadata={"restarts": cfg.restarts},
        )
