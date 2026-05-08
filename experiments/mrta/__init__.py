"""Coalition Multi-Robot Task Allocation (CMRTA) Experiments

Modules:
- oim_simulate: OIM dynamics solver with correct signs (Blueprint §4.6)
- qubo_formulate: QUBO matrix assembly from MWIS (Blueprint §4.4)
- ising_map: QUBO to Ising parameter mapping (Blueprint §4.5)
"""

from .oim_simulate import (
    OIMConfig,
    OIMContext,
    solve_oim_dynamics,
    oim_dynamics_step,
)

from .qubo_formulate import (
    QUBOMatrix,
    assemble_qubo_matrix,
    evaluate_qubo,
    verify_qubo_signs,
    verify_penalty_bound,
)

from .ising_map import (
    IsingHamiltonian,
    qubo_to_ising,
    ising_to_oim_parameters,
    verify_ising_derivation,
)

__all__ = [
    # OIM
    'OIMConfig',
    'OIMContext',
    'solve_oim_dynamics',
    'oim_dynamics_step',
    # QUBO
    'QUBOMatrix',
    'assemble_qubo_matrix',
    'evaluate_qubo',
    'verify_qubo_signs',
    'verify_penalty_bound',
    # Ising
    'IsingHamiltonian',
    'qubo_to_ising',
    'ising_to_oim_parameters',
    'verify_ising_derivation',
]
