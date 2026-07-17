# CVRP — Dr. Oetker to Lidl Stores (OWL Region)

## Project Overview

This repository contains the Operations Research group 
project for Team 01. The project analyzes a capacitated 
vehicle routing problem for deliveries from the Dr. Oetker 
depot in Bielefeld to Lidl stores in the OWL region.

The goal is to structure the delivery problem, collect and 
prepare input data, formulate a mathematical routing model, 
and compute high-quality delivery routes using two methods: the
Clarke-Wright Savings Algorithm and Google OR-Tools with
Guided Local Search.

The model used is a Time-Dependent Heterogeneous Vehicle 
Routing Problem with Time Windows (TDHVRPTW). 
Travel times are adjusted using simplified time-dependent
congestion multipliers μ(t) based on the departure time at
each node:
- 07:00 to 09:00 → ×1.3 (morning rush hour)
- 09:00 to 11:30 → ×1.0 (free flow baseline)
- 11:30 to 12:00 → ×1.1 (lunch surge)

The traffic multipliers are simplified planning assumptions and are documented in detail in `Docs/traffic_data_method.md`.
---

## Decision Question

Which delivery routes should the available vehicles use to 
serve all Lidl stores while minimizing transportation effort 
and respecting operational constraints such as vehicle 
capacity, service times, delivery time windows, traffic 
buffers, and maximum route duration?

---

## Repository Structure

* `DATA/` contains collected and prepared data files, including the editable distance and time matrices.
* `Docs/` contains project explanations, assumptions, model documentation, traffic-method documentation, and solver-comparison documentation.
* `Figures/` contains route figures, comparison figures, and the Google TrafficLayer screenshot.
* `Literature/` contains literature review files, source notes, references, and BibTeX entries.
* `Mathematics formular/` contains the mathematical formulation documents.
* `Presentation/` contains presentation material.
* `Results/` contains documented scenario results and method-comparison results.
* `src/` contains the executable Python scripts, CSV input matrices, package requirements, and run instructions:
  - `DrOetker_Lidl_Optimization.py` — main OR-Tools solver
  - `comparison_cw_vs_ortools.py` — Clarke-Wright vs OR-Tools comparison
  - `HOW_TO_RUN.md` — detailed run instructions
* `Archive/` contains older conceptual project files that are kept for transparency but are not part of the active final implementation.
* `CONTRIBUTIONS.pdf` documents the team contribution overview.

---

## How to Run

1. Install the required packages:

       pip install -r src/requirements.txt

   If this does not work on your system, install the main packages manually:

       pip install ortools numpy pandas matplotlib

2. Make sure these two CSV files are in the `src/` folder together with the Python scripts:

       distance_matrix.csv
       time_matrix.csv

3. Open the main solver file:

       src/DrOetker_Lidl_Optimization.py

4. Set the scenario you want to test at the top of the file:

       CHOSEN_SCENARIO = 99    # change to 152 or 170

5. Run the file from the repository root:

       python src/DrOetker_Lidl_Optimization.py

The output will print the routes, arrival times at each store, distances, and total pallets delivered for every truck used in that scenario.

To run the Clarke-Wright vs OR-Tools comparison:

       python src/comparison_cw_vs_ortools.py

Detailed run instructions are provided in:

       src/HOW_TO_RUN.md

## Problem Setup

* Depot: Dr. Oetker, Bielefeld (node 0)
* Customers: 25 Lidl stores across the OWL region 
  (nodes 1 to 25)
* Fleet: 4 heavy trucks (33 pallets each) and 
  4 medium trucks (12 pallets each)
* Total fleet capacity: 180 pallets
* Departure time: 07:00 every morning
* Delivery window: stores must be served between 
  08:00 and 12:00 (hard time windows)
* Maximum route duration: 405 minutes per truck
* Service time at each store: s = 10 + 2 × demand (min)
* Traffic model: simplified time-dependent congestion
  multipliers μ(t) applied to baseline travel times

---

## Main Model Components

* Decision variable x_ijk (binary): 1 if vehicle k 
  travels from node i to node j, 0 otherwise
* Decision variable T_ik (continuous): arrival time 
  of vehicle k at node i in minutes from midnight
* Customer demand measured in pallets
* Heterogeneous vehicle capacity per truck type
* Service times based on demand: s_i = 10 + 2 × q_i
* Hard delivery time windows (08:00 to 12:00)
* Maximum route duration (405 minutes)
* Distance-based objective function minimising total 
  kilometres driven across all routes

---

## Three Demand Scenarios

| Scenario | Description | Total Pallets |
|----------|-------------|---------------|
| S-99 | Normal weekday baseline | 99 pallets |
| S-152 | High volume surge day | 150 pallets |
| S-170 | Maximum fleet stress test | 174 pallets |

---

## Results

The solver was run for all three scenarios using Google
OR-Tools with Guided Local Search, the implemented search
configuration, and simplified time-dependent traffic multipliers.

| Scenario | Pallets | Total Distance | Trucks Used | Feasible |
|----------|---------|----------------|-------------|----------|
| S-99 | 99 | 241 km | 4 Heavy | Yes |
| S-152 | 150 | 286 km | 4 Heavy + 2 Medium | Yes |
| S-170 | 174 | — | — | No |

### Scenario S-99 — Route Summary

| Truck | Load | Distance | Route Time | Stores Visited |
|-------|------|----------|------------|----------------|
| V0 | 29/33p | 55 km | 310 min | L11→L18→L15→L10→L05→L06→L07 |
| V1 | 26/33p | 82 km | 330 min | L09→L21→L23→L24→L25→L22→L02 |
| V2 | 27/33p | 86 km | 328 min | L20→L19→L17→L14→L16→L12→L13 |
| V3 | 17/33p | 18 km | 189 min | L03→L04→L01→L08 |

All 25 stores served. All routes completed within constraints.

### Scenario S-152 — Route Summary

| Truck | Type | Load | Distance | Route Time | Stores Visited |
|-------|------|------|----------|------------|----------------|
| V0 | Heavy | 33/33p | 92 km | 313 min | L15→L16→L14→L17→L20→L19 |
| V1 | Heavy | 33/33p | 30 km | 245 min | L05→L06→L07→L04→L03 |
| V2 | Heavy | 28/33p | 80 km | 284 min | L22→L25→L24→L23→L21 |
| V3 | Heavy | 32/33p | 59 km | 273 min | L10→L13→L12→L18→L11 |
| V4 | Medium | 12/12p | 14 km | 130 min | L02→L09 |
| V6 | Medium | 12/12p | 11 km | 131 min | L01→L08 |

All 25 stores served. All routes completed within constraints.

### Scenario S-170 — No feasible hard-window solution found

No feasible solution was found under the implemented hard-window model, search configuration, and time limit.

The fleet has enough nominal volume capacity:

`174 / 180 pallets = 96.7%`

However, the combination of higher service times, morning congestion, the hard 08:00–12:00 delivery window, and the maximum route-duration constraint prevented the implemented solver from constructing a feasible schedule under the current assumptions.

Scenario summaries and method-comparison results are documented
in the `Results/` folder.

---

## Method Comparison: Clarke-Wright vs OR-Tools

Both methods applied to Scenario S-99 (99 pallets):

| Method | Total Distance | Time | Interpretation |
|--------|---------------|------|----------------|
| Clarke-Wright Savings | 308.1 km | < 1 ms | Constructive heuristic baseline |
| OR-Tools GLS | 241 km | < 30 sec | Stronger search result, no formal optimality proof |
| Improvement | 21.8% shorter | — | — |

Full comparison output available by running:
python src/comparison_cw_vs_ortools.py

---

## Project Progress

* Distance matrix and time matrix collected from 
  Google Maps and added to DATA/
* Demand estimation research completed and documented
* Mathematical formulation report completed
* Simplified time-dependent traffic model implemented
* Python solver implemented using OR-Tools GLS
* Clarke-Wright comparison implemented and documented
* All three scenarios tested and results documented
* Figures and route maps generated
* Final report written
* Presentation completed
* Model justification with full academic citations added

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

Braekers, K., Ramaekers, K. and Van Nieuwenhuyse, I. (2016).
The vehicle routing problem: State of the art classification
and review. Computers and Industrial Engineering, 99, 300-313.
https://doi.org/10.1016/j.cie.2015.12.007

Gendreau, M., Ghiani, G. and Guerriero, E. (2015).
Time-dependent routing problems: A review.
Computers and Operations Research, 64, 189-197.
https://doi.org/10.1016/j.cor.2015.06.001

Lahyani, R., Khemakhem, M. and Semet, F. (2015).
Rich vehicle routing problems: From a taxonomy to a
definition. European Journal of Operational Research,
241(1), 1-14.
https://doi.org/10.1016/j.ejor.2014.07.048

Vidal, T., Laporte, G. and Matl, P. (2020). A concise guide
to existing and emerging vehicle routing problem variants.
Networks, 75(4), 349-360.
https://doi.org/10.1002/net.21901

Mor, A. and Speranza, M.G. (2022). Vehicle routing problems
over time: a survey. Annals of Operations Research,
314, 255-275.
https://doi.org/10.1007/s10479-021-04times

Shaheen, S. and Cohen, A. (2020). Shared mobility policy
playbook. Transportation Sustainability Research Center,
University of California Berkeley.
https://doi.org/10.7922/G2DN43J3

Caceres-Cruz, J., Arias, P., Guimarans, D., Riera, D. and
Juan, A.A. (2015). Rich vehicle routing problem:
Survey. ACM Computing Surveys, 47(2), Article 32.
https://doi.org/10.1145/2666003

Perron, L. and Furnon, V. (2023). OR-Tools. Google LLC.
https://developers.google.com/optimization

Google Maps Platform (2024). Distance Matrix API.
https://developers.google.com/maps/documentation/distance-matrix
