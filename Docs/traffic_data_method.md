# Traffic Data Method

## Purpose

This document explains how traffic information is considered in the routing model.

The professor suggested using the Google Maps TrafficLayer example to show how traffic conditions can be visualized. In this project, the TrafficLayer is used as visual support for the time-dependent travel assumptions in the model. It does not directly solve the vehicle routing problem and it does not generate the full travel-time matrix by itself.

The routing model still works with a baseline travel-time matrix. Traffic is represented by simplified time-dependent multipliers that adjust the baseline travel times depending on the departure time of each route segment.

---

## Why Traffic Matters

The delivery routes in this project start in the morning. Around Bielefeld and the surrounding OWL region, travel times can change during the day because of commuter traffic, city traffic, and congestion on larger roads.

For this reason, it would be too simple to treat every travel time as fully constant. A route that looks short by distance may still become problematic if the vehicle travels during a busy time period.

This is especially relevant because the model also uses:

- hard delivery time windows,
- service times at each store,
- vehicle-capacity constraints,
- and a maximum route duration.

Traffic therefore affects whether a route is feasible in time, not only how long the route distance is.

---

## Role of Google TrafficLayer

Google TrafficLayer displays traffic conditions on a Google map. In this project, it is used to visualize that traffic conditions are not the same everywhere in the delivery network.

The screenshot used for this task is saved as:

`Figures/google_traffic_layer_bielefeld.png`

It shows the Bielefeld / OWL area with the traffic overlay activated. The screenshot supports the modelling idea that travel time should be treated as time-dependent, especially during the morning delivery period.

At the same time, the TrafficLayer should not be overinterpreted. It is not used as an exact historical traffic dataset for every road segment. It is also not used to calculate the optimized routes directly. The solver works with a baseline travel-time matrix and then applies simplified time-dependent multipliers.

---

## Traffic Multipliers Used in the Model

The model uses a baseline travel-time matrix between all relevant nodes. To account for traffic, the baseline travel time is multiplied by a time-dependent congestion factor.

| Time period | Traffic assumption | Multiplier |
|---|---|---:|
| 07:00–09:00 | Morning peak traffic | 1.3 |
| 09:00–11:30 | Normal mid-morning traffic | 1.0 |
| 11:30–12:00 | Slight late-morning increase | 1.1 |

The model uses the following idea:

`actual_travel_time(i, j, t) = baseline_travel_time(i, j) × traffic_multiplier(t)`

where:

- `i` is the origin node,
- `j` is the destination node,
- `t` is the departure time from node `i`,
- `baseline_travel_time(i, j)` is the travel time before the congestion adjustment,
- `traffic_multiplier(t)` is the multiplier assigned to the relevant time period.

---

## Justification of the Traffic Multipliers

The traffic multipliers are simplified planning assumptions. They are not presented as exact measured traffic values for every road segment.

The rationale behind the multipliers is based on typical urban and regional traffic patterns during the delivery window.

The highest multiplier is assigned to the 07:00–09:00 period because this period overlaps with morning commuter traffic. Since the vehicles depart from the Dr. Oetker depot at 07:00, many early route segments can be affected by this peak period. Therefore, the model applies a congestion multiplier of 1.3 during this period.

The 09:00–11:30 period is treated as the baseline mid-morning period. After the morning peak, traffic conditions are assumed to be closer to normal operating conditions. Therefore, the multiplier is set to 1.0.

The 11:30–12:00 period receives a smaller increase of 1.1. This represents a conservative planning buffer for possible late-morning delays, for example from urban traffic lights, local congestion, reduced speeds, or local road-network effects.

The broader conceptual framework of the project considered congestion multiplier ranges such as:

| Traffic situation | Conceptual multiplier range |
|---|---:|
| Peak traffic | approximately 1.25–1.35 |
| Standard daytime operation | approximately 1.0–1.15 |
| Free-flow traffic | close to 1.0 |

The final implementation uses a simplified three-period version of this idea because the project focuses on deterministic scenario-based routing rather than real-time traffic prediction.

These multipliers make the model more realistic than using one constant travel-time matrix for the whole morning, while still keeping the model transparent, reproducible, and suitable for the scope of this university project.

---

## Connection to the Travel-Time Matrix

The travel-time matrix gives the baseline travel time between the depot and the Lidl stores, and between store pairs. The traffic multiplier is applied on top of this matrix.

This means the matrix provides the base travel-time structure, while the traffic model changes the effective travel time depending on the time of day.

For example, if a baseline travel time is 20 minutes and the vehicle travels during the 07:00–09:00 morning peak, the adjusted travel time becomes:

`20 × 1.3 = 26 minutes`

The same baseline connection would remain 20 minutes during the normal 09:00–11:30 period.

---

## Connection to the TDHVRPTW Model

This is what makes the routing model time-dependent. In a basic CVRP, travel times are usually fixed. In this project, the travel time of an arc can change depending on when the vehicle starts that arc.

This matters because the routes must satisfy several restrictions at the same time:

- store demand,
- vehicle capacity,
- service time,
- delivery time windows,
- maximum route duration,
- and time-dependent travel times.

Traffic affects the timing of the route and can therefore make a route infeasible even if the distance and capacity look acceptable.

---

## What We Can Claim

We can claim that Google TrafficLayer was used to visualize traffic conditions in the Bielefeld / OWL delivery region and to support the reasoning behind time-dependent travel-time assumptions.

We can also claim that the model uses simplified time-dependent traffic multipliers to represent different traffic conditions during the morning delivery window.

We should not claim that Google TrafficLayer directly calculated:

- the optimized routes,
- the full distance matrix,
- the full travel-time matrix,
- exact historical travel times for every road segment,
- or real-time traffic during the solver run.

---

## Limitations

The traffic approach is simplified. It does not use live traffic values for every single road segment during the solver run. It also does not reconstruct historical traffic data for the exact delivery day.

Instead, the model uses a transparent traffic scenario: baseline travel times are adjusted by fixed multipliers for different time periods.

This is less precise than a full traffic-data model, but it is understandable, reproducible, and suitable for the scope of this university project.

A stronger empirical method would be to collect repeated travel-time observations for the same origin-destination pairs at different departure times using a routing API or repeated map-based travel-time checks.

For each time period, the multiplier could then be calculated as:

`traffic multiplier = observed travel time / baseline travel time`

The average multiplier for each time block could then replace the current assumed values.

Because this project uses fixed multipliers, the final results should be interpreted as scenario-based planning results rather than exact real-time route predictions.

---

## Related Files

| File | Purpose |
|---|---|
| `Figures/google_traffic_layer_bielefeld.png` | Screenshot of the Google traffic overlay around Bielefeld / OWL |
| `DATA/time matrix.ods` | Editable baseline travel-time matrix |
| `src/time_matrix.csv` | CSV travel-time matrix used by the Python scripts |
| `src/DrOetker_Lidl_Optimization_fixed.py` | Python implementation where the time-dependent traffic multipliers are applied |
| `Docs/traffic_data_method.md` | Explanation of how traffic is considered in the model |
