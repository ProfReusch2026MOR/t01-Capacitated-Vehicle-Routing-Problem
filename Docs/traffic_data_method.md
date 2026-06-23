# Traffic Data Method

## Purpose

This document explains how traffic information is considered in the routing model.

The professor suggested using the Google Maps TrafficLayer example to show how traffic conditions can be visualized. In this project, the TrafficLayer is used as visual support for the time-dependent travel assumptions in the model. It does not directly solve the vehicle routing problem and it does not generate the full travel-time matrix by itself.

## Why traffic matters

The delivery routes in this project start in the morning. Around Bielefeld and the surrounding OWL region, travel times can change during the day because of commuter traffic, city traffic, and congestion on larger roads.

For this reason, it would be too simple to treat every travel time as fully constant. A route that looks short by distance may still become problematic if the vehicle travels during a busy time period. This is especially relevant because the model also uses hard delivery time windows and a maximum route duration.

## Role of Google TrafficLayer

Google TrafficLayer displays traffic conditions on a Google map. In our project, it is used to visualize that traffic conditions are not the same everywhere in the network.

The screenshot used for this task is saved as:

`Figures/google_traffic_layer_bielefeld.png`

It shows the Bielefeld / OWL area with the traffic overlay activated. The screenshot supports the idea that travel time should be treated as time-dependent, especially during the morning delivery period.

At the same time, the TrafficLayer should not be overinterpreted. It is not used as an exact historical traffic dataset for every road segment. It is also not used to calculate the optimized routes directly. The solver works with a baseline travel-time matrix and then applies simplified time-dependent multipliers.

## Traffic multipliers used in the model

The model uses a baseline travel-time matrix between all relevant nodes. To account for traffic, the baseline travel time is multiplied by a time-dependent congestion factor.

| Time period | Traffic assumption           | Multiplier |
| ----------- | ---------------------------- | ---------: |
| 07:00–09:00 | Morning peak traffic         |        1.3 |
| 09:00–11:30 | Normal traffic               |        1.0 |
| 11:30–12:00 | Slight lunch-period increase |        1.1 |

The model uses the following idea:

`actual_travel_time(i, j, t) = baseline_travel_time(i, j) × traffic_multiplier(t)`

where:

* `i` is the origin node
* `j` is the destination node
* `t` is the departure time from node `i`
* `baseline_travel_time(i, j)` is the travel time before the congestion adjustment
* `traffic_multiplier(t)` is the multiplier assigned to the relevant time period

## Connection to the travel-time matrix

The travel-time matrix gives the baseline travel time between the depot and the Lidl stores, and between store pairs. The traffic multiplier is applied on top of this matrix.

This means the matrix provides the base travel-time structure, while the traffic model changes the effective travel time depending on the time of day.

For example, if a baseline travel time is 20 minutes and the vehicle travels during the 07:00–09:00 morning peak, the adjusted travel time becomes:

`20 × 1.3 = 26 minutes`

The same baseline connection would remain 20 minutes during the normal 09:00–11:30 period.

## Connection to the TDHVRPTW model

This is what makes the routing model time-dependent. In a basic CVRP, travel times are usually fixed. In this project, the travel time of an arc can change depending on when the vehicle starts that arc.

This matters because the routes must satisfy several restrictions at the same time: store demand, vehicle capacity, service time, delivery time windows, and maximum route duration. Traffic affects the timing of the route and can therefore make a route infeasible even if the distance and capacity look acceptable.

## What we can claim

We can claim that Google TrafficLayer was used to visualize traffic conditions in the Bielefeld / OWL delivery region and to support the reasoning behind time-dependent travel-time assumptions.

We should not claim that Google TrafficLayer directly calculated the optimized route, the full distance matrix, or exact historical travel times for every road segment.

## Limitations

The traffic approach is simplified. It does not use live traffic values for every single road segment during the solver run. It also does not reconstruct historical traffic data for the exact delivery day.

Instead, the model uses a transparent traffic scenario: baseline travel times are adjusted by fixed multipliers for different time periods. This is less precise than a full traffic-data model, but it is understandable, reproducible, and suitable for the scope of this university project.

## Related files

| File                                         | Purpose                                                         |
| -------------------------------------------- | --------------------------------------------------------------- |
| `Figures/google_traffic_layer_bielefeld.png` | Screenshot of the Google traffic overlay around Bielefeld / OWL |
| `docs/traffic_data_method.md`                | Explanation of how traffic is considered in the model           |
