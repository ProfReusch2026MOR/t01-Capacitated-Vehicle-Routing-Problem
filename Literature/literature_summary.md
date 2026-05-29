# Literature Summary

This file summarizes books, articles, and research sources related to our Operations Research project on the Capacitated Vehicle Routing Problem.

## Purpose

The literature is used to support the theoretical background, model formulation, assumptions, and possible solution approaches for our delivery routing project.

Our project is based on a vehicle routing problem where deliveries start from a depot and serve multiple customer locations while respecting capacity, time, and operational constraints.

## Main Literature Areas

### 1. Vehicle Routing Problem

The Vehicle Routing Problem is the general problem class behind our project. It deals with planning routes for vehicles that start from a depot, visit customers, and return to the depot.

Relevant sources:

- Dantzig, G. B., & Ramser, J. H. (1959). The Truck Dispatching Problem.
- Laporte, G. (2009). Fifty Years of Vehicle Routing.
- Toth, P., & Vigo, D. (2014). Vehicle Routing: Problems, Methods, and Applications.

### 2. Capacitated Vehicle Routing Problem

The Capacitated Vehicle Routing Problem adds vehicle capacity restrictions. This is directly relevant to our project because customer demand is measured in pallets and vehicles have limited pallet capacity.

Relevant sources:

- Toth, P., & Vigo, D. (2014). Vehicle Routing: Problems, Methods, and Applications.
- Uchoa et al. New Benchmark Instances for the Capacitated Vehicle Routing Problem.
- Accorsi et al. A fast and scalable heuristic for large-scale capacitated vehicle routing problems.

### 3. Vehicle Routing Problem with Time Windows

The Vehicle Routing Problem with Time Windows considers delivery time intervals. This is relevant because our project uses delivery time windows for Lidl stores.

Relevant sources:

- Solomon, M. M. (1987). Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints.
- Kallehauge, B. Vehicle Routing Problem with Time Windows.

### 4. Time-Dependent Vehicle Routing

Time-dependent vehicle routing considers that travel time can change depending on the time of day. This is relevant because our model includes congestion multipliers for different time intervals.

Relevant sources:

- Adamo et al. (2024). A review of recent advances in time-dependent vehicle routing.
- Wu et al. (2023). Research on the Time-Dependent Vehicle Routing Problem in Urban Cold Chain Logistics.

### 5. Heuristics and Practical Solution Methods

Vehicle routing problems become difficult as the number of customers increases. Therefore, practical projects often use heuristics, metaheuristics, or approximate solution methods.

Relevant sources:

- Laporte, Røpke, & Vidal (2014). Heuristics for the Vehicle Routing Problem.
- Accorsi et al. A fast and scalable heuristic for large-scale capacitated vehicle routing problems.

## Relevance for Our Project

The literature supports our project in the following way:

- It justifies why our project belongs to the Vehicle Routing Problem family.
- It supports the use of vehicle capacity constraints.
- It supports the use of customer time windows.
- It supports the use of time-dependent travel times or congestion factors.
- It explains why exact optimization can become difficult for larger instances.
- It provides a basis for later using heuristics or solver-based methods.

## Current Status

This literature folder is currently being built. The next step is to add detailed source notes and a structured reference list.