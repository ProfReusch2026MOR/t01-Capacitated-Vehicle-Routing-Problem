# Traffic Data Method

## 1. Purpose

Traffic is included because travel time in urban and regional delivery is not constant. A route that is short in distance can still be slow if it passes through congested roads.

## 2. Google Maps TrafficLayer

Google Maps TrafficLayer is used to visually inspect traffic conditions in the Bielefeld / OWL region during the morning delivery period.

The professor suggested this source because it can show traffic conditions directly on a map. In our project, it is used as visual support for the traffic assumptions in the routing model.

## 3. From Traffic Observation to Model Parameter

The routing model uses a baseline travel-time matrix. To include traffic effects, baseline travel times are multiplied by time-dependent congestion factors.

| Time period | Traffic assumption | Multiplier |
|---|---|---:|
| 07:00–09:00 | Morning peak traffic | 1.3 |
| 09:00–11:30 | Normal traffic | 1.0 |
| 11:30–12:00 | Slight lunch-period increase | 1.1 |

The model calculates:

`actual_travel_time(i, j, t) = baseline_travel_time(i, j) * traffic_multiplier(t)`

## 4. Connection to the Routing Model

The travel-time matrix provides the baseline travel time between all node pairs. The congestion multiplier changes the travel time depending on when the vehicle starts a route segment.

This makes the model time-dependent and more realistic than a pure distance-based CVRP.

## 5. Limitation

The Google Maps TrafficLayer is used as visual evidence and not as exact historical traffic data for every road segment. The traffic model is therefore simplified.

However, the simplification is documented and allows the project to include realistic traffic effects while keeping the model understandable and solvable.
