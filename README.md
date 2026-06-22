# CVRP — Dr. Oetker to Lidl Stores (OWL Region)

## Project Overview

This repository contains the Operations Research group 
project for Team 01. The project analyzes a capacitated 
vehicle routing problem for deliveries from the Dr. Oetker 
depot in Bielefeld to Lidl stores in the OWL region.

The goal is to structure the delivery problem, collect and 
prepare input data, formulate a mathematical routing model, 
and solve optimal delivery routes using two methods: the 
Clarke-Wright Savings Algorithm and Google OR-Tools with 
Guided Local Search.

---

## Decision Question

Which delivery routes should the available vehicles use to 
serve all Lidl stores while minimizing transportation effort 
and respecting operational constraints such as vehicle 
capacity, service times, delivery time windows, traffic 
buffers, and maximum route duration?

---

## Repository Structure

* `DATA/` contains collected and prepared data files, 
  including distance and time matrices collected from 
  Google Maps Distance Matrix API.
* `Math formulation report/` contains the mathematical 
  model formulation (ILP with objective function and 
  8 constraints).
* `Final report/` contains the full written project report.
* `docs/` contains project explanations, assumptions, 
  and short documentation files.
* `Notebooks/` contains Jupyter notebooks for data 
  exploration, model testing, and result analysis.
* `src/` contains the main Python solver script: 
  DrOetker_Lidl_Optimization.py
* `Results/` contains solver outputs, route summaries, 
  and figures for all 3 scenarios.
* `Figures/` contains route maps, Gantt charts, load 
  charts and comparison graphs.
* `Presentation/` contains presentation material.
* `Literature/` contains sources and literature notes 
  with full academic citations.
* `Project_management/` contains contribution logs, 
  task overview, and meeting notes.

---

## How to Run

1. Install the required packages:

   pip install ortools numpy pandas matplotlib

2. Open the main solver file:

   src/DrOetker_Lidl_Optimization.py

3. Set the scenario you want to test at the top of the file:

   CHOSEN_SCENARIO = 99    # change to 152 or 170

4. Run the file:

   python src/DrOetker_Lidl_Optimization.py

The output will print the routes, arrival times at each 
store, distances, and total pallets delivered for every 
truck used in that scenario.

---

## Problem Setup

* Depot: Dr. Oetker, Bielefeld (node 0)
* Customers: 25 Lidl stores across the OWL region 
  (nodes 1 to 25)
* Fleet: 4 heavy trucks (33 pallets each) and 
  4 medium trucks (12 pallets each)
* Departure time: 07:00 every morning
* Delivery window: stores must be served between 
  08:00 and 12:00
* Maximum route duration: 405 minutes per truck
* Service time at each store: s = 10 + 2 × demand 
  (in minutes)
* Traffic model: travel times are multiplied by a 
  congestion factor depending on time of day:
  - 07:00 to 09:00 → ×1.3 (morning rush hour)
  - 09:00 to 11:30 → ×1.0 (free flow)
  - 11:30 to 12:00 → ×1.1 (lunch surge)

---

## Main Model Components

The project uses typical Operations Research elements:

* Decision variables for vehicle movements between 
  locations (binary variable x_ijk) and arrival times 
  at each node (continuous variable T_ik)
* Customer demand measured in pallets
* Vehicle capacity restrictions per truck type
* Service times at stores based on demand
* Delivery time windows (08:00 to 12:00)
* Maximum route duration (405 minutes)
* Distance-based objective function to minimise total 
  kilometres driven

---

## Three Demand Scenarios

We tested three situations to stress-test the fleet:

| Scenario | Description | Total Pallets |
|----------|-------------|---------------|
| S-99 | Normal weekday baseline | 99 pallets |
| S-152 | High volume surge day | 150 pallets |
| S-170 | Maximum fleet stress test | 174 pallets |

Each scenario uses a different demand per store:
* S-99: low stores get 3p, medium 4p, high 5p
* S-152: low stores get 5p, medium 6p, high 7p
* S-170: low stores get 6p, medium 7p, high 8p

---

## Results

The solver was run for all three scenarios using Google 
OR-Tools with Guided Local Search (10 second time limit).

| Scenario | Pallets | Total Distance | Trucks Used | Feasible |
|----------|---------|----------------|-------------|----------|
| S-99 | 99 | 215 km | 4 heavy | Yes |
| S-152 | 150 | 220 km | 4 heavy + 2 medium | Yes |
| S-170 | 174 | — | — | No |

### Scenario S-99 — Route Summary

| Truck | Load | Distance | Route Time | Stores Visited |
|-------|------|----------|------------|----------------|
| V0 | 32/33p | 49 km | 317 min | L04→L01→L08→L06→L05→L10→L20→L19 |
| V1 | 26/33p | 86 km | 342 min | L11→L18→L21→L23→L24→L25→L22 |
| V2 | 29/33p | 64 km | 329 min | L17→L14→L16→L12→L13→L15→L07 |
| V3 | 12/33p | 16 km | 162 min | L03→L09→L02 |

All 25 stores served. All routes completed on time.

### Scenario S-152 — Route Summary

| Truck | Type | Load | Distance | Route Time | Stores Visited |
|-------|------|------|----------|------------|----------------|
| V0 | Heavy | 33/33p | 71 km | 312 min | L15→L16→L14→L17→L20→L19 |
| V1 | Heavy | 33/33p | 23 km | 240 min | L05→L06→L07→L04→L03 |
| V2 | Heavy | 28/33p | 64 km | 281 min | L22→L25→L24→L23→L21 |
| V3 | Heavy | 32/33p | 48 km | 268 min | L10→L13→L12→L18→L11 |
| V4 | Medium | 12/12p | 8 km | 129 min | L02→L09 |
| V6 | Medium | 12/12p | 6 km | 130 min | L01→L08 |

All 25 stores served. All routes completed on time.

### Scenario S-170 — Infeasible

The solver could not find a valid solution.

The fleet had enough physical space (174 pallets demand 
vs 180 pallets total capacity = 96.7% utilisation). 
However the problem was time, not space. Each store 
needed more unloading time because of higher demand, 
and all trucks depart into morning rush hour traffic 
which slows down the first legs by 30%. Combined with 
the hard 08:00 to 12:00 delivery window and the 405 
minute shift limit, no valid schedule could be built.

To make this scenario work the company would need to 
either add a 5th heavy truck, extend the delivery 
window, or allow split deliveries.

Full console outputs for all three scenarios are saved 
in the Results/ folder.

---

## Project Progress

* Distance matrix and time matrix collected from 
  Google Maps and added to DATA/
* Demand estimation research completed and documented
* Mathematical formulation report completed (ILP model 
  with 8 constraints)
* Python solver implemented using OR-Tools and 
  Clarke-Wright heuristic
* All three scenarios solved and results documented
* Figures and route maps generated
* Final report written
* Presentation completed

---

## Team Workflow

The repository is used as the central workspace for:

* storing project files
* documenting assumptions
* tracking individual contributions
* organizing tasks through GitHub Issues
* reviewing work through commits and pull requests

---

## References

Clarke, G. and Wright, J.W. (1964). Scheduling of 
vehicles from a central depot to a number of delivery 
points. Operations Research, 12(4), 568–581.
https://doi.org/10.1287/opre.12.4.568

Dantzig, G.B. and Ramser, J.H. (1959). The truck 
dispatching problem. Management Science, 6(1), 80–91.
https://doi.org/10.1287/mnsc.6.1.80

Toth, P. and Vigo, D. (2014). Vehicle Routing: Problems, 
Methods, and Applications. 2nd edition. SIAM.
ISBN: 978-1-611973-58-7

Malandraki, C. and Daskin, M.S. (1992). Time dependent 
vehicle routing problems: Formulations, properties and 
heuristic algorithms. Transportation Science, 26(3), 
185–200.
https://doi.org/10.1287/trsc.26.3.185

Solomon, M.M. (1987). Algorithms for the vehicle routing 
and scheduling problems with time window constraints. 
Operations Research, 35(2), 254–265.
https://doi.org/10.1287/opre.35.2.254

Gendreau, M., Ghiani, G. and Guerriero, E. (2015). 
Time-dependent routing problems: A review. Computers 
and Operations Research, 64, 189–197.
https://doi.org/10.1016/j.cor.2015.06.001

Perron, L. and Furnon, V. (2023). OR-Tools. Google LLC.
https://developers.google.com/optimization

Google Maps Platform (2024). Distance Matrix API.
https://developers.google.com/maps/documentation/
distance-matrix
