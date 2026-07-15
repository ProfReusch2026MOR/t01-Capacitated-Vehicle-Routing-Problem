# How to Run the Full Project

## What you need first

Make sure you have Python installed on your computer.
Then install the required packages by running this 
one command in your terminal:

    pip install ortools numpy pandas matplotlib

---

## The repository contains 2 Python files to run

---

### File 1 — Main Solver (OR-Tools)
**File:** `src/DrOetker_Lidl_Optimization.py`

This is the main solver. It uses Google OR-Tools to 
find the best delivery routes for each demand scenario.

**How to run:**

1. Open the file `src/DrOetker_Lidl_Optimization.py`
2. At the top of the file, find this line:

       CHOSEN_SCENARIO = 99

3. Change the number to pick the scenario you want:
   - 99  → Normal weekday (99 pallets)
   - 152 → High volume surge day (150 pallets)
   - 170 → Fleet stress test (174 pallets)

4. Run the file:

       python src/DrOetker_Lidl_Optimization.py

**What you will see:**

For scenario 99:
- 4 routes, total 215 km, all 25 stores served

For scenario 152:
- 6 routes, total 220 km, all 25 stores served

For scenario 170:
- No valid solution — the solver confirms infeasibility

---

### File 2 — Method Comparison (Clarke-Wright vs OR-Tools)
**File:** `src/comparison_cw_vs_ortools.py`

This file runs Clarke-Wright and documents the OR-Tools
results side by side. It proves the 30% distance 
improvement claim made in the report.

No extra installation needed beyond what is listed above.

**How to run:**

    python src/comparison_cw_vs_ortools.py

**What you will see:**

1. Top 10 savings values computed by Clarke-Wright
2. Clarke-Wright routes — live computation — 308.1 km
3. OR-Tools verified routes — 215 km
4. Side-by-side comparison table showing 30.2% improvement
5. A figure saved as comparison_cw_vs_ortools.png 
   in the same folder

---

## Data files

Both scripts read from the same data.
Make sure these two files are in your DATA/ folder:

    DATA/distance_matrix.csv
    DATA/time_matrix.csv

These are the real 26x26 matrices collected from 
Google Maps for the OWL road network 
(depot + 25 Lidl stores).

---

## Expected results summary

| Script | Scenario | Result |
|--------|----------|--------|
| DrOetker_Lidl_Optimization.py | S-99 | 215 km, 4 routes |
| DrOetker_Lidl_Optimization.py | S-152 | 220 km, 6 routes |
| DrOetker_Lidl_Optimization.py | S-170 | Infeasible |
| comparison_cw_vs_ortools.py | S-99 | CW: 308 km vs OR: 215 km |

---

## If something does not work

The most common issue is a missing package.
Run this command to install everything at once:

    pip install ortools numpy pandas matplotlib

If you see a message saying the data file is not found,
make sure you are running the script from the root 
folder of the repository, not from inside the src/ folder.

You can do this by opening your terminal in the 
repository folder and typing:

    python src/DrOetker_Lidl_Optimization.py

not:

    cd src
    python DrOetker_Lidl_Optimization.py
