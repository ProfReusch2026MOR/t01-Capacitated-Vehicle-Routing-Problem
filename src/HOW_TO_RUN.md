# How to Run the Code

This file explains how to run the Python scripts in the `src/` folder for the final Dr. Oetker → Lidl OWL routing project.

The active implementation is based on the final 25-store model with:

* 1 Dr. Oetker depot
* 25 Lidl stores
* 26 total nodes
* 4 heavy trucks with 33-pallet capacity
* 4 medium trucks with 12-pallet capacity
* delivery window from 08:00 to 12:00
* service time formula `s_i = 10 + 2q_i`
* time-dependent traffic multipliers
* scenarios S-99, S-152, and S-170

---

## 1. Install Requirements

From the repository root, install the required Python packages:

`pip install -r src/requirements.txt`

If the requirements file does not work on your system, install the main packages manually:

`pip install ortools pandas numpy matplotlib`

---

## 2. Run the Main OR-Tools Solver

The main solver file is:

`src/DrOetker_Lidl_Optimization.py`

Run it from the repository root with:

`python src/DrOetker_Lidl_Optimization.py`

---

## 3. Change the Scenario

Inside `DrOetker_Lidl_Optimization.py`, change the scenario value:

`CHOSEN_SCENARIO = 99`

Possible values are:

| Scenario value | Meaning                    |      Demand |
| -------------: | -------------------------- | ----------: |
|           `99` | Normal weekday baseline    |  99 pallets |
|          `152` | High-volume surge scenario | 150 pallets |
|          `170` | Fleet stress-test scenario | 174 pallets |

After changing the value, save the file and run the solver again.

---

## 4. Current Documented Scenario Results

The currently documented final results are:

| Scenario | Result                                                                                      |
| -------- | ------------------------------------------------------------------------------------------- |
| S-99     | Feasible, 241 km total distance                                                             |
| S-152    | Feasible, 286 km total distance                                                             |
| S-170    | No feasible hard-window solution found under the implemented model and search configuration |

Important: S-170 should not be described as mathematically “proven infeasible.” The correct statement is that no feasible hard-window solution was found under the implemented constraints, search configuration, and time limit.

---

## 5. Run the Clarke-Wright vs OR-Tools Comparison

The comparison script is:

`src/comparison_cw_vs_ortools.py`

Run it from the repository root with:

`python src/comparison_cw_vs_ortools.py`

The current documented S-99 comparison is:

| Method                |         Total distance |
| --------------------- | ---------------------: |
| Clarke-Wright Savings |               308.1 km |
| OR-Tools GLS          |                 241 km |
| Improvement           | 21.8% shorter distance |

Clarke-Wright is used as a constructive heuristic baseline. OR-Tools with Guided Local Search is used as the stronger routing search method.

OR-Tools GLS should not be described as an exact solver. It provides a high-quality solution found by the implemented search configuration.

---

## 6. Input Files Used by the Scripts

The scripts use the CSV matrix files stored in the same folder:

* `src/distance_matrix.csv`
* `src/time_matrix.csv`

The editable `.ods` versions are stored in the `DATA/` folder for documentation and checking.

---

## 7. Notes for Reproducibility

Run the scripts from the repository root so that the relative file paths work correctly.

The final project documentation should use the same result values as this file, the root `README.md`, and `Results/results.md`.

Outdated result values such as 215 km or 220 km should no longer be used.

