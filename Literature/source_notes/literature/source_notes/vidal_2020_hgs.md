# Vidal (2020) — Hybrid Genetic Search for the CVRP

## Full reference

Vidal, T. (2020). *Hybrid Genetic Search for the CVRP: Open-Source Implementation and SWAP* Neighborhood.*



Vidal’s paper is useful for us because it does more than introduce another routing heuristic. The main point is that good routing methods also need to be understandable and reproducible. In vehicle routing research, many strong algorithms are hard to reuse because the implementation details are either missing, too complex, or not openly available. Vidal addresses this by presenting an open-source Hybrid Genetic Search implementation for the Capacitated Vehicle Routing Problem.

For our project, this matters because our repository has to show more than final route results. If someone only sees a presentation slide with “OR-Tools found this solution,” that is not enough. The data, assumptions, solver settings, and outputs should be visible enough that another person can follow how the result was produced. That is the main lesson we take from this paper.

The paper also helps justify why heuristic methods are still relevant in routing problems. Even though our project does not implement Vidal’s HGS directly, it shows that practical vehicle routing is often solved through carefully designed heuristics rather than only by exact mathematical formulations. This fits our project because we compare a solver-based approach with a heuristic route-construction approach.

There is still a limitation. Vidal’s paper focuses on the CVRP, while our case is richer. We also include time windows, time-dependent travel times, heterogeneous vehicles, and demand scenarios. So we should not present this source as if it directly solves our TDHVRPTW model. It is better used as support for reproducibility, heuristic thinking, and the general difficulty of practical routing problems.
