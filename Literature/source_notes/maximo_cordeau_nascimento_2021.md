# Máximo, Cordeau and Nascimento (2021) — Adaptive Iterated Local Search for the HFVRP

## Full reference

Máximo, V. R., Cordeau, J.-F., & Nascimento, M. C. V. (2021). *An Adaptive Iterated Local Search Heuristic for the Heterogeneous Fleet Vehicle Routing Problem.*


This paper is mainly useful for the heterogeneous-fleet part of our project. The authors focus on the Heterogeneous Fleet Vehicle Routing Problem, where vehicles are not all identical. That is important because in real distribution systems, trucks can differ in capacity, operating cost, and practical suitability for certain routes. A model that treats every vehicle as the same can become too simple for realistic logistics planning.

The paper proposes an adaptive iterated local search heuristic. The important lesson for us is not the full technical detail of the algorithm, but the reason why such a method is needed. When vehicle types differ, the routing problem becomes harder because the model has to decide not only the order of customers, but also which kind of vehicle should serve which group of customers. That adds another layer to the routing decision.

For our project, this supports the decision to describe the case as a heterogeneous fleet routing problem instead of only a basic CVRP. Even if our computational model uses a simplified fleet structure, the source helps justify why vehicle capacity and vehicle type should be part of the model. In a Dr. Oetker to Lidl delivery setting, this is realistic because larger vehicles may be efficient for consolidated loads, while smaller or medium vehicles may be more flexible in regional or urban delivery situations.

The limitation is that this paper does not directly include the full structure of our case. It focuses on heterogeneous fleet routing, but not on the complete combination of time-dependent travel times, hard store time windows, and our specific demand scenarios. So we use it mainly to support the fleet-design part of the model, not the entire TDHVRPTW formulation.
