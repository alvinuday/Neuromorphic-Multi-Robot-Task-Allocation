# OIM-MRTA Benchmark Results

## Setup
- Solvers: kuramoto_oim, simulated_annealing, greedy_mwis, random_restarts
- Coalition bound: k=2
- Exact optimum: brute-force MWIS when node count <= 22

## Case Results
| Case | Nodes | Solver | Utility | Feasible | Runtime (ms) | Approx ratio |
|---|---:|---|---:|:---:|---:|---:|
| N3_M2_S7 | 5 | greedy_mwis | 2.826 | Y | 0.02 | 1.000 |
| N3_M2_S7 | 5 | simulated_annealing | 2.826 | Y | 46.03 | 1.000 |
| N3_M2_S7 | 5 | kuramoto_oim | 0.000 | Y | 84.82 | 0.000 |
| N3_M2_S7 | 5 | random_restarts | 2.826 | Y | 1.97 | 1.000 |
| N4_M2_S8 | 20 | greedy_mwis | 10.832 | Y | 0.04 | 1.000 |
| N4_M2_S8 | 20 | simulated_annealing | 10.832 | Y | 62.97 | 1.000 |
| N4_M2_S8 | 20 | kuramoto_oim | 0.000 | Y | 1231.59 | 0.000 |
| N4_M2_S8 | 20 | random_restarts | 10.832 | Y | 4.54 | 1.000 |
| N4_M3_S9 | 23 | greedy_mwis | 14.587 | Y | 0.02 | n/a |
| N4_M3_S9 | 23 | simulated_annealing | 14.587 | Y | 70.88 | n/a |
| N4_M3_S9 | 23 | kuramoto_oim | 0.000 | Y | 1125.09 | n/a |
| N4_M3_S9 | 23 | random_restarts | 14.587 | Y | 18.08 | n/a |
| N5_M2_S10 | 21 | greedy_mwis | 3.246 | Y | 0.02 | 1.000 |
| N5_M2_S10 | 21 | simulated_annealing | 3.246 | Y | 60.79 | 1.000 |
| N5_M2_S10 | 21 | kuramoto_oim | 0.000 | Y | 1057.96 | 0.000 |
| N5_M2_S10 | 21 | random_restarts | 3.246 | Y | 2.74 | 1.000 |
| N6_M3_S21 | 46 | greedy_mwis | 13.946 | Y | 0.04 | n/a |
| N6_M3_S21 | 46 | simulated_annealing | 7.856 | Y | 101.31 | n/a |
| N6_M3_S21 | 46 | kuramoto_oim | 0.000 | Y | 3855.82 | n/a |
| N6_M3_S21 | 46 | random_restarts | 13.946 | Y | 6.52 | n/a |
| N8_M4_S31 | 76 | greedy_mwis | 16.571 | Y | 0.09 | n/a |
| N8_M4_S31 | 76 | simulated_annealing | 16.205 | Y | 266.83 | n/a |
| N8_M4_S31 | 76 | kuramoto_oim | 6.862 | Y | 11528.61 | n/a |
| N8_M4_S31 | 76 | random_restarts | 14.322 | Y | 10.09 | n/a |

## Aggregate Summary
| Solver | Avg utility | Avg runtime (ms) | Feasibility rate | Avg approx ratio |
|---|---:|---:|---:|---:|
| greedy_mwis | 10.334 | 0.04 | 1.000 | 1.000 |
| kuramoto_oim | 1.144 | 3147.31 | 1.000 | 0.000 |
| random_restarts | 9.960 | 7.32 | 1.000 | 1.000 |
| simulated_annealing | 9.258 | 101.47 | 1.000 | 1.000 |
