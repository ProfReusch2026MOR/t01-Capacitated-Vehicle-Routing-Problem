# Solver vs Heuristic Comparison

## 1. Purpose

The project compares an exact optimization approach with a heuristic approach.

The exact solver is useful for small instances because it can prove optimality. The heuristic is useful for larger instances because exact solving becomes slow or may hit a time limit.

## 2. Methods Compared

| Method | Description |
|---|---|
| Exact solver | MILP / ILP formulation solved with a solver such as CBC, PuLP, or Gurobi |
| Clarke-Wright Savings Heuristic | Constructive heuristic that merges routes based on distance savings while checking feasibility |

## 3. Comparison Table

| Instance | Customers | Method | Objective value | Runtime | Feasible? | Comment |
|---|---:|---|---:|---:|---|---|
| Small | 10 | Exact solver | TBD | TBD | TBD | Should solve to optimality |
| Small | 10 | Clarke-Wright | TBD | TBD | TBD | Compare with exact optimum |
| Medium | 40 | Exact solver | TBD | TBD | TBD | Runtime or MIP gap may become visible |
| Medium | 40 | Clarke-Wright | TBD | TBD | TBD | Expected to be faster |
| Large | 100 | Exact solver | TBD | TBD | TBD | May hit time limit |
| Large | 100 | Clarke-Wright | TBD | TBD | TBD | Practical feasible solution expected |

## 4. Evaluation Criteria

The methods are compared using:

- total distance
- total travel time
- route feasibility
- capacity utilization
- time-window compliance
- runtime
- optimality gap, where available

## 5. Interpretation

A solver is preferred when the instance is small enough and an optimality proof is required. A heuristic is preferred when the instance is large, the solver becomes too slow, or a fast feasible solution is more important than proving optimality.

## 6. Current Status

The table currently contains placeholders. It should be filled after computational experiments are run.
