# Computational Results — TDHVRPTW Realistic Solver Output

All results produced by:
src/DrOetker_Lidl_Optimization.py

Solver: Google OR-Tools
Strategy: PATH_CHEAPEST_ARC initialisation + Guided Local Search
Time limit: 30 seconds per scenario
Traffic model: Time-dependent μ(t) = 1.3 (07-09h) / 1.0 (09-11:30h) / 1.1 (11:30-12h)
Fleet: 4 Heavy trucks (33 pallets) + 4 Medium trucks (12 pallets)

---

## SCENARIO S-99 — Normal Weekday Baseline

Total demand: 99 pallets
Objective value: 241 km
Vehicles used: 4 Heavy trucks
All 25 stores served: Yes
All routes feasible: Yes

| Vehicle | Type | Load | Distance | Route Time | Departure | Return |
|---------|------|------|----------|------------|-----------|--------|
| V0 | Heavy 33p | 29/33p | 55 km | 310 min | 07:00 | 12:10 |
| V1 | Heavy 33p | 26/33p | 82 km | 330 min | 07:00 | 12:30 |
| V2 | Heavy 33p | 27/33p | 86 km | 328 min | 07:00 | 12:28 |
| V3 | Heavy 33p | 17/33p | 18 km | 189 min | 07:00 | 10:09 |
| TOTAL | — | 99/99p | 241 km | — | — | — |

### Route V0 — Heavy Truck (33 pallets)
Depot 07:00 → L11@08:00 (5p) → L18@08:37 (3p) → L15@09:22 (3p)
→ L10@10:04 (5p) → L05@10:37 (4p) → L06@11:03 (4p) → L07@11:29 (5p)
→ Depot 12:10 | Load: 29/33p | Distance: 55 km | Time: 310 min

### Route V1 — Heavy Truck (33 pallets)
Depot 07:00 → L09@08:00 (4p) → L21@08:38 (3p) → L23@09:10 (4p)
→ L24@09:54 (5p) → L25@10:36 (3p) → L22@11:08 (3p) → L02@11:54 (4p)
→ Depot 12:30 | Load: 26/33p | Distance: 82 km | Time: 330 min

### Route V2 — Heavy Truck (33 pallets)
Depot 07:00 → L20@08:00 (3p) → L19@08:29 (3p) → L17@09:11 (3p)
→ L14@09:50 (5p) → L16@10:28 (4p) → L12@11:04 (4p) → L13@11:34 (5p)
→ Depot 12:28 | Load: 27/33p | Distance: 86 km | Time: 328 min

### Route V3 — Heavy Truck (33 pallets)
Depot 07:00 → L03@08:00 (4p) → L04@08:30 (5p) → L01@09:06 (4p)
→ L08@09:34 (4p) → Depot 10:09 | Load: 17/33p | Distance: 18 km | Time: 189 min

---

## SCENARIO S-152 — High Volume Surge Day

Total demand: 150 pallets
Objective value: 286 km
Vehicles used: 4 Heavy + 2 Medium trucks
All 25 stores served: Yes
All routes feasible: Yes

| Vehicle | Type | Load | Distance | Route Time | Departure | Return |
|---------|------|------|----------|------------|-----------|--------|
| V0 | Heavy 33p | 33/33p | 92 km | 313 min | 07:00 | 12:13 |
| V1 | Heavy 33p | 33/33p | 30 km | 245 min | 07:00 | 11:05 |
| V2 | Heavy 33p | 28/33p | 80 km | 284 min | 07:00 | 11:44 |
| V3 | Heavy 33p | 32/33p | 59 km | 273 min | 07:00 | 11:33 |
| V4 | Medium 12p | 12/12p | 14 km | 130 min | 07:00 | 09:10 |
| V6 | Medium 12p | 12/12p | 11 km | 131 min | 07:00 | 09:11 |
| TOTAL | — | 150/150p | 286 km | — | — | — |

### Route V0 — Heavy Truck (33 pallets)
Depot 07:00 → L15@08:00 (5p) → L16@08:45 (6p) → L14@09:25 (7p)
→ L17@10:12 (5p) → L20@10:54 (5p) → L19@11:27 (5p)
→ Depot 12:13 | Load: 33/33p | Distance: 92 km | Time: 313 min

### Route V1 — Heavy Truck (33 pallets)
Depot 07:00 → L05@08:00 (6p) → L06@08:30 (6p) → L07@09:00 (7p)
→ L04@09:53 (7p) → L03@10:29 (7p)
→ Depot 11:05 | Load: 33/33p | Distance: 30 km | Time: 245 min

### Route V2 — Heavy Truck (33 pallets)
Depot 07:00 → L22@08:00 (5p) → L25@08:36 (5p) → L24@09:18 (7p)
→ L23@10:08 (6p) → L21@10:46 (5p)
→ Depot 11:44 | Load: 28/33p | Distance: 80 km | Time: 284 min

### Route V3 — Heavy Truck (33 pallets)
Depot 07:00 → L10@08:00 (7p) → L13@08:44 (7p) → L12@09:20 (6p)
→ L18@10:20 (5p) → L11@10:57 (7p)
→ Depot 11:33 | Load: 32/33p | Distance: 59 km | Time: 273 min

### Route V4 — Medium Truck (12 pallets)
Depot 07:00 → L02@08:00 (6p) → L09@08:36 (6p)
→ Depot 09:10 | Load: 12/12p | Distance: 14 km | Time: 130 min

### Route V6 — Medium Truck (12 pallets)
Depot 07:00 → L01@08:00 (6p) → L08@08:32 (6p)
→ Depot 09:11 | Load: 12/12p | Distance: 11 km | Time: 131 min

---

## SCENARIO S-170 — Fleet Stress Test

Total demand: 174 pallets
Result: No feasible hard-window solution found

Solver output:
"No valid schedule path satisfies the combined
constraints under the 170-pallet scenario."

The fleet has enough nominal volume capacity:
174 pallets demand vs 180 pallets fleet capacity = 96.7%

However, the implemented solver did not find a valid schedule under the current hard time-window, traffic, service-time, fleet-capacity, and route-duration assumptions. The main limiting factor is time feasibility rather than pure pallet capacity. Reasons:

| Driver | Explanation |
|--------|-------------|
| Time window (C6) | Hard 08:00-12:00 window. Stores with 8p demand need 26 min service each |
| Peak congestion | μ=1.3 on all first legs erodes effective window by 15-25 min |
| Service inflation | Average 23.9 min per stop vs 17.9 min in S-99 (+34%) |
| Route limit (C7) | 405 min max minus 90 min slack = 315 min active routing |

To make S-170 feasible:
- Add a 5th heavy truck, or
- Extend time window to 07:00-13:00, or
- Allow split deliveries

---

## Cross-Scenario Summary

| Scenario | Demand | Distance | Vehicles | Heavy Used | Medium Used | Feasible |
|----------|--------|----------|----------|------------|-------------|----------|
| S-99 | 99p | 241 km | 4 | 4 | 0 | Yes |
| S-152 | 150p | 286 km | 6 | 4 | 2 | Yes |
| S-170 | 174p | — | — | — | — | No feasible hard-window solution found |

---

## Method Comparison: Clarke-Wright vs OR-Tools GLS

Both methods are compared on Scenario S-99 with identical input data.

Clarke-Wright Savings is used as a constructive heuristic baseline. OR-Tools with `PATH_CHEAPEST_ARC` and `GUIDED_LOCAL_SEARCH` is used as the stronger routing search method.

| Method | Distance | Time | Interpretation |
|--------|----------|------|----------------|
| Clarke-Wright Savings | 308.1 km | < 1 ms | Constructive heuristic baseline |
| OR-Tools GLS | 241 km | < 30 sec | Stronger search result, no formal optimality proof |
| Improvement | 21.8% shorter | — | — |

The 21.8% improvement is consistent with findings in
Cordeau et al. (2002, JORS 53(5), p.516) who report
metaheuristic improvement of 10-30% over constructive
heuristics on medium VRP instances.

## S-170 Constraint Diagnosis

The S-170 scenario was used as a stress test to identify which part of the model becomes binding under high demand.

The result suggests that the feasibility problem is not caused by total pallet capacity alone. The fleet has 180 pallets of nominal capacity, while S-170 requires 174 pallets. The critical issue is the interaction between:

- high service times caused by larger pallet volumes,
- the hard 08:00–12:00 delivery window,
- morning traffic multipliers,
- the 405-minute maximum route-duration limit,
- and the limited number of available vehicles.

A soft-time-window formulation was considered as a possible extension. In such a model, late deliveries would be allowed but penalized in the objective function. This would help test whether a small amount of lateness could make the stress scenario operationally feasible.

This extension is not part of the main final result unless a separate solver output is documented. Therefore, the current final interpretation remains:

> No feasible hard-window solution was found for S-170 under the implemented model, search configuration, and time limit.

Possible operational responses include:

- adding vehicle capacity,
- extending the delivery window,
- reducing route-duration buffers,
- allowing split deliveries,
- or introducing soft time windows with calibrated lateness penalties.
