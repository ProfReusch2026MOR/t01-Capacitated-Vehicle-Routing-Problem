# Literature Review

## Purpose of the Literature Review

The purpose of this literature review is to connect our project to established Operations Research research on vehicle routing.

Our project is based on a Capacitated Vehicle Routing Problem with additional operational constraints such as delivery time windows, heterogeneous vehicle capacities, service times, and time-dependent travel times. The literature helps us justify why these model components are relevant and how similar routing problems are usually formulated and solved.

## Main Literature Areas

### 1. Vehicle Routing Problem

The Vehicle Routing Problem is the general problem class behind our project. It deals with planning routes for vehicles that start from a depot, visit customers, and return to the depot. The objective is usually to minimize total distance, total time, total cost, or another operational performance measure.

### 2. Capacitated Vehicle Routing Problem

The Capacitated Vehicle Routing Problem adds vehicle capacity constraints. This is directly relevant because our project models Lidl store demand in pallets and uses trucks with limited pallet capacity.

### 3. Vehicle Routing Problem with Time Windows

The Vehicle Routing Problem with Time Windows considers that customers can only be served within defined time intervals. This is relevant because our model assumes a delivery time window for the Lidl stores.

### 4. Heterogeneous Fleet Routing

Our project does not assume that all vehicles are identical. Instead, the mathematical formulation distinguishes between heavy trucks and medium trucks with different capacity limits. This connects the project to heterogeneous vehicle routing problems.

### 5. Time-Dependent Vehicle Routing

Travel times in real distribution systems are not always constant. Traffic conditions can change during the day. Our model reflects this by using congestion multipliers for different time periods.

### 6. Heuristics and Solver-Based Approaches

Vehicle routing problems become difficult as the number of customers and constraints increases. Therefore, both exact methods and heuristic approaches are relevant. Exact methods are useful for small or structured instances, while heuristics can provide good feasible solutions when the model becomes too large or complex.

## Relevance for Our Project

The literature supports our project in the following ways:

- It helps define the project as a vehicle routing problem.
- It justifies capacity constraints based on pallet demand.
- It supports the use of time windows and route duration limits.
- It supports the distinction between different vehicle types.
- It explains why routing problems are computationally difficult.
- It motivates the possible use of heuristics or solver-based methods.

## Literature Gaps and Open Points

- More literature is needed on time-dependent vehicle routing.
- More literature is needed on heterogeneous vehicle routing.
- More practical sources are needed for food and retail distribution.
- More sources are needed to justify cost parameters and traffic assumptions.
- The final report should clearly separate real input data from assumptions.