"""Leaky Integrate-and-Fire (LIF) neuron model.

Physics:
    tau * dV/dt = -V + R*(I_ext + sum_j W_ij * S_j(t))

Where:
    tau   = 20 ms   membrane time constant
    V_th  = 1.0     firing threshold
    V_rest= 0.0     reset potential
    R     = 1.0     membrane resistance
    tau_ref = 2 ms  refractory period
"""
from __future__ import annotations


class LIFNeuron:
    """Single LIF neuron with refractory period."""

    def __init__(
        self,
        neuron_id: int,
        tau_ms: float = 20.0,
        v_th: float = 1.0,
        v_rest: float = 0.0,
        r_mem: float = 1.0,
        tau_ref_ms: float = 2.0,
    ) -> None:
        self.neuron_id = neuron_id
        self.tau_ms = tau_ms
        self.v_th = v_th
        self.v_rest = v_rest
        self.r_mem = r_mem
        self.tau_ref_ms = tau_ref_ms

        # State
        self.v: float = v_rest
        self.refractory_remaining_ms: float = 0.0
        self.spike_times_ms: list[float] = []

    def step(self, t_ms: float, dt_ms: float, i_total: float) -> bool:
        """Advance neuron by dt_ms. Returns True if spike fired."""
        fired = False

        if self.refractory_remaining_ms > 0.0:
            self.refractory_remaining_ms -= dt_ms
            if self.refractory_remaining_ms < 0.0:
                self.refractory_remaining_ms = 0.0
        else:
            # Euler integration: dV = dt/tau * (-V + R*I)
            dv = (dt_ms / self.tau_ms) * (-self.v + self.r_mem * i_total)
            self.v += dv

            if self.v >= self.v_th:
                fired = True
                self.spike_times_ms.append(t_ms)
                self.v = self.v_rest
                self.refractory_remaining_ms = self.tau_ref_ms

        return fired

    def reset(self) -> None:
        """Reset to initial state."""
        self.v = self.v_rest
        self.refractory_remaining_ms = 0.0
        self.spike_times_ms = []
