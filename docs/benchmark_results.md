# OIM-MRTA Benchmark Results

## Setup
- Solvers: `kuramoto_oim`, `simulated_annealing`, `greedy_mwis`, `random_restarts`
- Coalition bound: k in {1, 2} depending on instance
- Instances: 6 random MRTA cases (N=3..8 robots, M=2..4 tasks)
- Exact optimum: brute-force MWIS when node count <= 22
- Kuramoto model: annealed subharmonic injection locking with conflict couplings

## Case Results
| Case | Nodes | Solver | Utility | Feasible | Runtime (ms) | Approx ratio |
|---|---:|---|---:|:---:|---:|---:|
| N3_M2_S7 | 8 | greedy_mwis | 1.878 | Y | 0.05 | 0.881 |
| N3_M2_S7 | 8 | simulated_annealing | 2.132 | Y | 124.13 | 1.000 |
| N3_M2_S7 | 8 | kuramoto_oim | 1.878 | Y | 253.06 | 0.881 |
| N3_M2_S7 | 8 | random_restarts | 2.132 | Y | 30.96 | 1.000 |
| N4_M2_S8 | 12 | greedy_mwis | 4.643 | Y | 0.05 | 1.000 |
| N4_M2_S8 | 12 | simulated_annealing | 4.643 | Y | 219.89 | 1.000 |
| N4_M2_S8 | 12 | kuramoto_oim | 4.406 | Y | 145.99 | 0.949 |
| N4_M2_S8 | 12 | random_restarts | 4.643 | Y | 23.33 | 1.000 |
| N4_M3_S9 | 5 | greedy_mwis | 9.685 | Y | 0.01 | 1.000 |
| N4_M3_S9 | 5 | simulated_annealing | 9.685 | Y | 82.31 | 1.000 |
| N4_M3_S9 | 5 | kuramoto_oim | 8.950 | Y | 34.90 | 0.924 |
| N4_M3_S9 | 5 | random_restarts | 9.685 | Y | 9.51 | 1.000 |
| N5_M2_S10 | 3 | greedy_mwis | 10.721 | Y | 0.01 | 1.000 |
| N5_M2_S10 | 3 | simulated_annealing | 10.721 | Y | 67.33 | 1.000 |
| N5_M2_S10 | 3 | kuramoto_oim | 3.433 | Y | 15.92 | 0.320 |
| N5_M2_S10 | 3 | random_restarts | 10.721 | Y | 9.02 | 1.000 |
| N6_M3_S21 | 49 | greedy_mwis | 11.167 | Y | 0.33 | n/a |
| N6_M3_S21 | 49 | simulated_annealing | 11.167 | Y | 417.05 | n/a |
| N6_M3_S21 | 49 | kuramoto_oim | 9.465 | Y | 1976.51 | n/a |
| N6_M3_S21 | 49 | random_restarts | 11.167 | Y | 104.99 | n/a |
| N8_M4_S31 | 96 | greedy_mwis | 13.371 | Y | 0.60 | n/a |
| N8_M4_S31 | 96 | simulated_annealing | 13.505 | Y | 1169.90 | n/a |
| N8_M4_S31 | 96 | kuramoto_oim | 9.477 | Y | 7516.91 | n/a |
| N8_M4_S31 | 96 | random_restarts | 13.509 | Y | 270.96 | n/a |

## Aggregate Summary
| Solver | Avg utility | Avg runtime (ms) | Feasibility rate | Avg approx ratio |
|---|---:|---:|---:|---:|
| greedy_mwis | 8.578 | 0.17 | 1.000 | 0.970 |
| kuramoto_oim | 6.268 | 1657.21 | 1.000 | 0.769 |
| random_restarts | 8.643 | 74.80 | 1.000 | 1.000 |
| simulated_annealing | 8.642 | 346.77 | 1.000 | 1.000 |

## Reference Papers Used
- Bhowmik et al., Spintronics-Based Neuromorphic and Ising Computing, EDTM 2024, DOI:10.1109/EDTM58488.2024.10511458
- Garg et al. with Debanjan Bhowmik, Phase-Binarized Dipole-Coupled SHNOs as Ising Machines, NANO 2024, DOI:10.1109/NANO61778.2024.10628871
- Bhowmik et al., Improved time complexity for spintronic oscillator Ising machines (Kuramoto Max-Cut study), Nanotechnology 2024, DOI:10.1088/1361-6528/ad6f18


## Kuramoto Parameter Sweep (Auto-Appended)
Generated: 2026-04-20 14:18:42 UTC

Objective: maximize average approximation ratio on exact-solvable cases (first 4 scenarios).
Grid combinations evaluated: 128

### Best Tuned Parameters
- restarts=8, steps=280, dt=0.035, kinj_min=0.15, kinj_max=3.4, coupling_gain=1.0, bias_gain=0.55, noise_amp=0.04
- objective avg_ratio=0.854, avg_utility=5.310, avg_runtime_ms=41.07

### Top 5 Sweep Configurations
| Rank | restarts | steps | dt | kinj_min | kinj_max | coupling_gain | bias_gain | noise_amp | avg_ratio | avg_utility | avg_runtime_ms |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 8 | 280 | 0.035 | 0.15 | 3.4 | 1.0 | 0.55 | 0.04 | 0.854 | 5.310 | 41.07 |
| 2 | 8 | 280 | 0.04 | 0.15 | 3.4 | 1.0 | 0.55 | 0.08 | 0.854 | 5.310 | 41.21 |
| 3 | 8 | 280 | 0.035 | 0.15 | 3.4 | 1.0 | 0.55 | 0.08 | 0.854 | 5.310 | 42.68 |
| 4 | 8 | 280 | 0.04 | 0.15 | 3.4 | 1.0 | 0.55 | 0.04 | 0.854 | 5.310 | 42.98 |
| 5 | 8 | 360 | 0.035 | 0.15 | 3.4 | 1.0 | 0.55 | 0.04 | 0.854 | 5.310 | 53.36 |

### Default vs Tuned Kuramoto (All 6 Cases)
| Case | Nodes | Optimum utility | Default utility | Tuned utility | Default ratio | Tuned ratio | Default runtime (ms) | Tuned runtime (ms) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| N3_M2_S7 | 8 | 2.132 | 1.878 | 2.132 | 0.881 | 1.000 | 60.41 | 45.10 |
| N4_M2_S8 | 12 | 4.643 | 4.406 | 4.406 | 0.949 | 0.949 | 115.00 | 92.02 |
| N4_M3_S9 | 5 | 9.685 | 8.950 | 9.685 | 0.924 | 1.000 | 23.91 | 19.17 |
| N5_M2_S10 | 3 | 10.721 | 3.433 | 5.017 | 0.320 | 0.468 | 11.67 | 9.82 |
| N6_M3_S21 | 49 | n/a | 9.465 | 9.511 | n/a | n/a | 1832.38 | 1180.91 |
| N8_M4_S31 | 96 | n/a | 9.477 | 13.374 | n/a | n/a | 5743.88 | 4506.86 |

### Aggregate (Default vs Tuned Kuramoto)
| Variant | Avg utility | Avg runtime (ms) | Feasibility rate | Avg approx ratio (exact-solvable subset) |
|---|---:|---:|---:|---:|
| default_kuramoto | 6.268 | 1297.88 | 1.000 | 0.769 |
| tuned_kuramoto | 7.354 | 975.65 | 1.000 | 0.854 |

Ground-truth JS export: docs/js_groundtruth_cases.json
Sweep raw JSON: docs/kuramoto_sweep_results.json
