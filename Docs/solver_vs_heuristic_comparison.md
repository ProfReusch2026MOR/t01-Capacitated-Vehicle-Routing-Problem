# Solver vs. Heuristic Comparison

This document explains the comparison between the constructive heuristic baseline and the stronger routing search method used in the final Dr. Oetker → Lidl OWL routing project.

The implemented project is a Time-Dependent Heterogeneous Vehicle Routing Problem with Time Windows (TDHVRPTW). It includes one Dr. Oetker depot, 25 Lidl stores, two vehicle capacity classes, service times, hard delivery time windows, maximum route-duration constraints, and time-dependent traffic multipliers.

---

## Purpose of the Comparison

The purpose of the comparison is to show the difference between:

1. a simple and transparent constructive heuristic, and
2. a stronger solver-based routing search method.

The comparison is not used to prove mathematical optimality. It is used to evaluate solution quality, computational behavior, and practical usefulness for the routing case.

---

## Method 1: Clarke-Wright Savings Heuristic

The Clarke-Wright Savings Algorithm is used as the heuristic baseline.

It starts from the idea that each customer could be served individually from the depot. It then calculates possible distance savings from combining customers into shared routes.

The savings value for combining two customers `i` and `j` is:

`s(i,j) = c(0,i) + c(0,j) - c(i,j)`

where:

* `c(0,i)` is the distance from the depot to customer `i`,
* `c(0,j)` is the distance from the depot to customer `j`,
* `c(i,j)` is the distance between both customers.

A high savings value means that combining both customers in the same route may reduce total driving distance.

### Strengths

* easy to understand
* fast to compute
* transparent baseline
* useful for comparison against a stronger routing method

### Limitations

* greedy construction logic
* no formal optimality guarantee
* weaker handling of complex time-window and route-duration interactions
* may produce longer routes than a stronger search method

---

## Method 2: Google OR-Tools with Guided Local Search

The stronger routing method uses Google OR-Tools.

The implementation uses:

* `PATH_CHEAPEST_ARC` as the initial solution strategy
* `GUIDED_LOCAL_SEARCH` as the local search metaheuristic
* a fixed search time limit
* capacity constraints
* time-window constraints
* service-time calculations
* route-duration constraints
* time-dependent travel-time multipliers

OR-Tools searches for improved route combinations after constructing an initial solution. This makes it stronger than the Clarke-Wright baseline for the final routing problem.

Important: OR-Tools with Guided Local Search is not treated as a formal exact solver in this project. The result is described as a high-quality solution found under the implemented search configuration and time limit.

---

## Scenario Used for Direct Comparison

The direct method comparison is performed on Scenario S-99.

Scenario S-99 represents the baseline weekday demand case:

| Scenario | Total demand | Demand classes                                     |
| -------- | -----------: | -------------------------------------------------- |
| S-99     |   99 pallets | Low: 3 pallets, Medium: 4 pallets, High: 5 pallets |

This scenario is suitable for comparison because it is feasible under the implemented model and provides a stable baseline for evaluating route quality.

---

## Comparison Result

| Method                | Role                            | Total distance |
| --------------------- | ------------------------------- | -------------: |
| Clarke-Wright Savings | Constructive heuristic baseline |       308.1 km |
| OR-Tools GLS          | Stronger routing search method  |         241 km |

The OR-Tools GLS result is:

`308.1 km - 241 km = 67.1 km`

shorter than the Clarke-Wright result.

The relative improvement is:

`67.1 / 308.1 = 21.8%`

Therefore, in Scenario S-99, OR-Tools GLS produced a route plan with approximately 21.8% less total driving distance than the Clarke-Wright Savings baseline.

---

## Interpretation

The comparison shows the expected trade-off between both approaches.

Clarke-Wright is fast, simple, and transparent. It is useful as a benchmark because it gives a reasonable first routing solution with limited computational effort.

OR-Tools GLS is more powerful for this project because it can search for improved route structures while respecting the implemented operational constraints. In the S-99 comparison, this produced a substantially shorter total distance.

The result supports the use of OR-Tools GLS as the main routing method for the final decision-support analysis.

---

## Important Methodological Limitation

The comparison does not prove that the OR-Tools solution is globally optimal.

The project does not use an exact MILP proof, optimality gap, or mathematical lower bound for the final OR-Tools result. Therefore, the correct interpretation is:

> OR-Tools GLS found a better solution than the Clarke-Wright baseline under the implemented model and search configuration.

The correct wording is not:

> OR-Tools proved the optimal solution.

---

## Final Conclusion

The Clarke-Wright Savings Algorithm provides a useful transparent benchmark, while OR-Tools with Guided Local Search provides the stronger final routing result.

For the implemented S-99 baseline case, OR-Tools reduced total driving distance from 308.1 km to 241 km, corresponding to a 21.8% improvement over the Clarke-Wright baseline.

This comparison strengthens the project because it shows not only one routing result, but also why the final solver-based approach is preferable to a simpler constructive heuristic.
