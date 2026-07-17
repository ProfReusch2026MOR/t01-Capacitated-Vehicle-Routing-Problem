# Source Code — Dr. Oetker to Lidl Stores Routing Model

This folder contains the executable Python files, input CSV matrices, and run instructions for the computational part of the Team 01 Operations Research project.

The implemented model is a Time-Dependent Heterogeneous Vehicle Routing Problem with Time Windows (TDHVRPTW). It models deliveries from the Dr. Oetker depot in Bielefeld to 25 Lidl stores in the OWL region.

The current implementation uses:

* 1 depot
* 25 Lidl stores
* 26 total nodes
* 4 heavy trucks with 33-pallet capacity
* 4 medium trucks with 12-pallet capacity
* service time formula `s_i = 10 + 2q_i`
* hard delivery time window from 08:00 to 12:00
* maximum route duration of 405 minutes
* time-dependent traffic multipliers
* three demand scenarios: S-99, S-152, and S-170

---

## Active Files in This Folder

| File                                  | Purpose                                                                                                               |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `DrOetker_Lidl_Optimization.py` | Main OR-Tools routing implementation for the three demand scenarios                                                   |
| `comparison_cw_vs_ortools.py`         | Clarke-Wright Savings baseline and comparison with the OR-Tools result for Scenario S-99                              |
| `distance_matrix.csv`                 | 26×26 road-distance matrix used by the Python scripts                                                                 |
| `time_matrix.csv`                     | 26×26 baseline travel-time matrix used by the Python scripts                                                          |
| `requirements.txt`                    | Python package requirements                                                                                           |
| `HOW_TO_RUN.md`                       | Step-by-step run instructions                                                                                         |
| `comparison_cw_vs_ortools (1).png`    | Visual comparison figure generated for the Clarke-Wright vs OR-Tools comparison                                       |
| `model justifications corrected.md`   | Supporting model-justification draft; the final documentation should be checked against the current implemented model |

---

## Main Solver

The main solver file is:

`DrOetker_Lidl_Optimization.py`

It uses Google OR-Tools with:

* `PATH_CHEAPEST_ARC` as the first solution strategy
* `GUIDED_LOCAL_SEARCH` as the local search metaheuristic
* a 30-second search time limit
* route constraints for capacity, time windows, service time, and maximum route duration

The scenario can be changed inside the script by editing:

`CHOSEN_SCENARIO = 99`

Possible values are:

| Scenario | Meaning                    |      Demand |
| -------- | -------------------------- | ----------: |
| `99`     | Normal weekday baseline    |  99 pallets |
| `152`    | High-volume surge day      | 150 pallets |
| `170`    | Fleet stress-test scenario | 174 pallets |

---

## Implemented Model Setup

| Element                | Current implementation           |
| ---------------------- | -------------------------------- |
| Depot                  | Dr. Oetker, Bielefeld            |
| Customers              | 25 Lidl stores                   |
| Nodes                  | 26 total nodes                   |
| Fleet                  | 4 heavy trucks + 4 medium trucks |
| Heavy capacity         | 33 pallets                       |
| Medium capacity        | 12 pallets                       |
| Total fleet capacity   | 180 pallets                      |
| Departure time         | 07:00                            |
| Delivery window        | 08:00–12:00                      |
| Maximum route duration | 405 minutes                      |
| Service time           | `s_i = 10 + 2q_i`                |
| Objective              | Minimize total driven distance   |

---

## Traffic Model

The implementation uses time-dependent traffic multipliers:

| Time period | Assumption                   | Multiplier |
| ----------- | ---------------------------- | ---------: |
| 07:00–09:00 | Morning peak traffic         |        1.3 |
| 09:00–11:30 | Normal traffic               |        1.0 |
| 11:30–12:00 | Slight lunch-period increase |        1.1 |

These multipliers are implemented as planning assumptions. They are documented more fully in:

`../Docs/traffic_data_method.md`

---

## Current Scenario Results

The current documented results are:

| Scenario | Pallets | Total distance | Vehicles used               | Status                                 |
| -------- | ------: | -------------: | --------------------------- | -------------------------------------- |
| S-99     |      99 |         241 km | 4 heavy vehicles            | Feasible                               |
| S-152    |     150 |         286 km | 4 heavy + 2 medium vehicles | Feasible                               |
| S-170    |     174 |              — | —                           | No feasible hard-window solution found |

Important: The S-170 result should be described carefully. The implemented OR-Tools search did not find a feasible solution under the current hard time-window, service-time, fleet-capacity, traffic, and route-duration assumptions. This should not be overstated as a formal mathematical proof of infeasibility.

---

## Method Comparison

The comparison script is:

`comparison_cw_vs_ortools.py`

It compares:

| Method                | Role                            |
| --------------------- | ------------------------------- |
| Clarke-Wright Savings | Constructive heuristic baseline |
| OR-Tools GLS          | Stronger routing search method  |

For Scenario S-99, the current documented comparison is:

| Method                |         Total distance |
| --------------------- | ---------------------: |
| Clarke-Wright Savings |               308.1 km |
| OR-Tools GLS          |                 241 km |
| Improvement           | 21.8% shorter distance |

OR-Tools with Guided Local Search should not be described as a formal exact solver. It provides a high-quality solution found under the configured search strategy and time limit.

---

## How to Run

Install the required packages from the repository root:

`pip install -r src/requirements.txt`

Run the main solver:

`python src/DrOetker_Lidl_Optimization.py`

Run the Clarke-Wright vs OR-Tools comparison:

`python src/comparison_cw_vs_ortools.py`

More detailed instructions are provided in:

`HOW_TO_RUN.md`

---

## Input Files

The Python scripts use the CSV matrices stored in this folder:

* `distance_matrix.csv`
* `time_matrix.csv`

The editable `.ods` versions are stored in the `DATA/` folder for documentation and checking.

---

## Reproducibility Notes

This folder should contain the files needed to run the computational part of the project.

The current implementation is based on the final 25-store model. Older file names, obsolete scenario values, and outdated claims such as 215 km or 220 km should not be used anymore.

The final documentation of data assumptions, traffic assumptions, limitations, results, figures, and literature support is stored in the repository folders:

* `DATA/`
* `Docs/`
* `Results/`
* `Figures/`
* `Literature/`
