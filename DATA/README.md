# CVRP Dataset Description

This folder contains three generated CVRP instances for computational experiments in the Dr. Oetker → Lidl routing project.

## Files

| File | Customers | Vehicles | Purpose |
|---|---:|---:|---|
| `cvrp_small.csv` | 10 | 2 | Small test instance that an exact solver should solve easily |
| `cvrp_medium.csv` | 40 | 5 | Medium instance for comparing solver runtime and heuristic quality |
| `cvrp_large.csv` | 100 | 12 | Large stress-test instance where exact solving should become difficult |

## Columns

| Column | Meaning |
|---|---|
| `node_id` | Unique node number |
| `node_type` | `depot` or `customer` |
| `x_coord` | Artificial x-coordinate in kilometres |
| `y_coord` | Artificial y-coordinate in kilometres |
| `demand_pallets` | Customer demand in Euro pallets |
| `service_time_min` | Service time in minutes |
| `time_window_start` | Earliest allowed delivery time |
| `time_window_end` | Latest allowed delivery time |
| `demand_class` | Low, medium, or high demand |

## Assumptions

The depot is node 0. Customer demand is measured in Euro pallets. Service time is calculated with:

`s_i = 10 + 2 * q_i`

where `q_i` is the demand of customer `i` in pallets.

The generated instances are not real store data. They are artificial benchmark instances used to test model scalability and compare exact solvers with the Clarke-Wright heuristic.
