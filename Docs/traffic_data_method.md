# Traffic Data Method

## Purpose

The project includes traffic because travel time in urban and regional delivery is not constant. A route that is short in distance can still be slow if it passes through congested roads.

## Google Maps TrafficLayer

Google Maps TrafficLayer was used to visually inspect traffic conditions in the Bielefeld / OWL region during the morning delivery period. This supports the assumption that travel times are higher during peak traffic.

## From Traffic Observation to Model Parameter

The routing model uses a baseline travel-time matrix. To include traffic effects, the baseline travel times are multiplied by time-dependent congestion factors.

| Time period | Traffic assumption | Multiplier |
|---|---|---:|
| 07:00–09:00 | Morning peak traffic | 1.3 |
| 09:00–11:30 | Normal traffic | 1.0 |
| 11:30–12:00 | Slight lunch-period increase | 1.1 |

The model therefore calculates:

actual_travel_time(i,j,t) = baseline_travel_time(i,j) × traffic_multiplier(t)

## Limitation

The Google Maps TrafficLayer was used as visual evidence and not as exact historical traffic data for every road segment. The traffic model is therefore simplified. However, the simplification is documented and allows the model to include realistic traffic effects while remaining understandable and solvable.