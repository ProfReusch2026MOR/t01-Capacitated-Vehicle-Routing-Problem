# Literature Review for CVRP / VRPTW Project

## Purpose

This literature review supports the mathematical model for the Dr. Oetker to Lidl delivery project. The project is formulated as a Vehicle Routing Problem with capacity and time-window constraints.

## Source Summary Table

| Topic | Source | Main idea | How it supports our project |
|---|---|---|---|
| CVRP | [Add source here] | CVRP models routes with vehicle capacity limits. | Supports our capacity constraints and depot-store-depot route structure. |
| VRPTW | [Add source here] | VRPTW extends VRP with customer time windows and service times. | Supports our delivery time windows and service time assumptions. |
| Heterogeneous Fleet VRP | [Add source here] | Different vehicle types can have different capacities and costs. | Supports possible use of trucks with different pallet capacity. |
| Heuristics for VRP | [Add source here] | Heuristics are used when exact optimization becomes difficult. | Supports our clustering/simple route construction approach. |
| Logistics / food distribution | [Add source here] | Retail logistics requires reliable routing under time and capacity limits. | Supports the real-world motivation of the Dr. Oetker and Lidl case. |

## Link to Mathematical Model

Our project follows the standard OR structure: decision variables, objective function, and constraints. In the course material, OR problems are defined by choices, a clear goal, and rules that limit the decision. :contentReference[oaicite:1]{index=1}

For our project:

- Decision variables: whether vehicle k travels from location i to location j.
- Objective: minimize total transportation cost.
- Constraints: vehicle capacity, customer demand, service times, time windows, route duration, and depot return.

This also matches the course model-formulation logic, where OR models transform real-world problems into variables, constraints, parameters, and an objective function. :contentReference[oaicite:2]{index=2}

## Reference Documentation

All references should be listed consistently in the bibliography section of the report. If a source is used for a specific formula, definition, or assumption, the report should mention it directly in the relevant section.