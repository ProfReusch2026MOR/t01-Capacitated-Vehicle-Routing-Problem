# Data Model for the CVRP / TDHVRPTW Project

## 1. Project Scope

The final project uses a Dr. Oetker depot in Bielefeld and Lidl stores in the OWL region. The routing problem is modeled as a Time-Dependent Heterogeneous Vehicle Routing Problem with Time Windows.

The active final baseline is:

- 1 depot
- 25 Lidl stores
- 26 nodes total
- customer set `C = {1, ..., 25}`

Older 11-store, 24-store, and 28-store drafts are archived and should not be used as the active baseline.

## 2. Sets

| Symbol | Meaning |
|---|---|
| `V` | Set of all nodes, including depot and customers |
| `C` | Set of customer nodes |
| `K` | Set of available vehicles |
| `K_heavy` | Set of heavy trucks |
| `K_medium` | Set of medium trucks |

## 3. Customer Table

| Column | Data type | Unit | Meaning |
|---|---|---|---|
| `customer_id` | integer | - | Unique ID of each Lidl store |
| `name` | text | - | Store name or short address |
| `latitude` | float | degrees | Store latitude |
| `longitude` | float | degrees | Store longitude |
| `demand_pallets` | integer | pallets | Estimated delivery demand |
| `service_time_min` | integer | minutes | Time needed at the store |
| `time_window_start` | time | HH:MM | Earliest allowed delivery |
| `time_window_end` | time | HH:MM | Latest allowed delivery |
| `demand_class` | text | low/medium/high | Demand category |

## 4. Depot Information

| Column | Data type | Unit | Meaning |
|---|---|---|---|
| `depot_id` | integer | - | Depot node ID, usually 0 |
| `name` | text | - | Dr. Oetker depot |
| `address` | text | - | Depot address |
| `latitude` | float | degrees | Depot latitude |
| `longitude` | float | degrees | Depot longitude |
| `route_start` | time | HH:MM | Vehicle departure time |
| `route_end` | time | HH:MM | Latest route return time |

## 5. Vehicle Table

| Column | Data type | Unit | Meaning |
|---|---|---|---|
| `vehicle_id` | integer | - | Unique vehicle ID |
| `vehicle_type` | text | - | Heavy, medium, or low-capacity vehicle |
| `capacity_pallets` | integer | pallets | Maximum pallet load |
| `max_route_duration_min` | integer | minutes | Maximum allowed route time |
| `fixed_cost_eur` | float | euros | Optional fixed vehicle cost |
| `cost_per_km` | float | euros/km | Distance-based transport cost |

## 6. Distance and Travel-Time Matrix

The route model needs a complete matrix between every pair of nodes, not only depot-to-store distances.

| Column | Data type | Unit | Meaning |
|---|---|---|---|
| `from_node` | integer | - | Start node |
| `to_node` | integer | - | Destination node |
| `distance_km` | float | km | Driving distance |
| `travel_time_min` | float | minutes | Baseline travel time |

## 7. Service Time Formula

Service time is demand-dependent:

`s_i = 10 + 2 * q_i`

where:

- `s_i` = service time at customer `i` in minutes
- `q_i` = demand at customer `i` in pallets
- `10` minutes = fixed handling and paperwork time
- `2` minutes per pallet = unloading time

## 8. Main Decision Variables

| Math symbol | Meaning |
|---|---|
| `x_ijk` | 1 if vehicle `k` travels directly from node `i` to node `j`, otherwise 0 |
| `T_ik` | arrival time of vehicle `k` at node `i` |
| `y_k` | 1 if vehicle `k` is used, otherwise 0 |

## 9. Main Parameters

| Symbol | Meaning |
|---|---|
| `c_ij` | distance between node `i` and node `j` |
| `t_ij` | baseline travel time between node `i` and node `j` |
| `q_i` | demand at customer `i` |
| `s_i` | service time at customer `i` |
| `Q_k` | capacity of vehicle `k` |
| `M` | large Big-M constant for time constraints |

## 10. Data Source Types

| Data | Source type |
|---|---|
| Depot location | Real |
| Lidl store addresses | Real |
| Demand values | Estimated |
| Service times | Formula-based |
| Distance matrix | Computed / Google Maps-based |
| Time windows | Assumed but realistic |
| Vehicle capacities | Literature / logistics assumptions |
