# Accorsi and Vigo (2021) — Large-Scale Capacitated Vehicle Routing

## Full reference

Accorsi, L., & Vigo, D. (2021). *A Fast and Scalable Heuristic for the Solution of Large-Scale Capacitated Vehicle Routing Problems.*


This source is useful because it looks at vehicle routing from a scalability perspective. Accorsi and Vigo focus on very large CVRP instances and show that practical routing does not only depend on having a mathematically correct model. The algorithm also has to run in a reasonable time, otherwise it is not very useful for real planning.

That point matters for our project, even though our own instance is much smaller. We only work with 25 Lidl stores and one depot, so our case is not a large-scale benchmark problem. Still, the same general issue appears: as soon as routing problems include more customers, vehicle limits, time windows, or traffic assumptions, the solution space grows quickly. A method that works nicely on paper can become difficult to use once the model becomes richer.

For our project, this paper helps support the use of heuristic thinking. We compare a solver-based approach with a Clarke-Wright-style heuristic, and this source gives background for why practical routing studies often do not rely on exact optimization alone. Fast heuristics are not just shortcuts; in many routing settings, they are part of how usable solutions are actually produced.

The source also helps us explain scalability as a limitation. Our 26-node network is manageable, but the same model would become harder if the number of stores increased, if several depots were added, or if demand changed throughout the day. Accorsi and Vigo’s work gives us a good reason to discuss that limitation honestly.

The limitation of the source is that it focuses on CVRP and very large benchmark-style instances. It does not directly model our full TDHVRPTW case with hard store time windows, time-dependent travel, heterogeneous vehicles, and scenario-based demand. So we use it mainly to support the discussion of scalability and heuristic methods.
