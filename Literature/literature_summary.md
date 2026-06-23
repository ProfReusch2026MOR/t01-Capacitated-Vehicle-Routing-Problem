# Literature Summary

This file gives a short overview of the main literature areas used in the project. The detailed discussion is written in `literature_review.md`, while the individual source notes are stored in `source_notes/`.

The project is not a simple CVRP anymore. It is modeled as a Time-Dependent Heterogeneous Fleet Vehicle Routing Problem with Time Windows (TDHVRPTW). Because of that, the literature has to support more than just vehicle capacity. It also has to support time windows, different vehicle types, demand scenarios, traffic effects, heuristics, and reproducible computational work.

## Main literature areas

### Vehicle routing and benchmark structure

The basic problem belongs to the Vehicle Routing Problem family. More recent CVRP benchmark literature is useful because it shows how routing instances should be documented: nodes, demand, vehicle capacities, matrices, and outputs should be clear enough that another person can understand and reproduce the case.

For our project, this mainly supports the way we document the 25 Lidl stores, the depot, the demand scenarios, and the distance and time matrices.

### Heterogeneous fleet routing

Our model includes vehicles with different capacities. Literature on heterogeneous fleet routing supports this part of the model because real delivery fleets are rarely made of identical vehicles. Vehicle type can affect capacity, cost, flexibility, and route feasibility.

This is relevant for the Dr. Oetker/Lidl case because the routing decision is not only about store order. It also involves deciding which type of truck can serve which part of the demand efficiently.

### Time windows and time-dependent travel

The project uses delivery time windows and congestion-based travel-time assumptions. Literature on VRPTW, dynamic VRPTW, and time-dependent routing helps justify why timing cannot be treated as an afterthought.

A route that is short by distance is not automatically feasible. It also has to respect store delivery windows, service times, and route-duration limits.

### Heuristics and scalability

The project compares a solver-based approach with heuristic routing logic. Recent heuristic literature supports this decision because practical VRP variants can become difficult quickly once additional constraints are added.

Even though our case has only 25 stores, the same principle applies: if more stores, depots, scenarios, or constraints were added, the model would become harder to solve and interpret. This is why heuristic methods are still relevant.

### Uncertainty and scenarios

The project uses different demand scenarios instead of relying on one fixed demand estimate. Literature on stochastic and contextual VRPTW supports this idea at a higher methodological level.

We do not build a full stochastic optimization model, but scenario analysis gives us a practical way to test whether the routing system remains feasible under different demand levels.

### Neural and frontier methods

Some recent literature studies neural or reinforcement-learning approaches for vehicle routing. These papers are useful as background, but they are not the computational basis of our project.

For this project, explainability and reproducibility are more important than using a fashionable method that we cannot properly implement or defend. Therefore, neural routing methods are mentioned only as a research direction, not as part of the implemented solution.

## Role in the project

The literature supports four main parts of the project:

* defining the correct routing problem class
* justifying the model assumptions and constraints
* explaining why both solver-based and heuristic methods are discussed
* showing the limits of our student-scale implementation

The main purpose is not to collect many sources, but to connect each source to a clear part of the model or repository.
