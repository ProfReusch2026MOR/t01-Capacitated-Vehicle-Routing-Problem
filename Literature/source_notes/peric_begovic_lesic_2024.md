# Peric, Begovic and Lesic (2024) — Adaptive Memory Procedure for a Real-World Vehicle Routing Problem

## Full reference

Peric, N., Begovic, S., & Lesic, V. (2024). *Adaptive Memory Procedure for Solving Real-world Vehicle Routing Problem.*


This paper is one of the closest sources to our project because it does not treat vehicle routing as a clean textbook problem. The authors work with a real-world routing case where several constraints appear at the same time: vehicle capacities, time windows, heterogeneous vehicles, soft time windows, multi-trip delivery, crew-related limits, split deliveries, and time-dependent routes. That makes the paper useful for us, because our own project also moves beyond a simple CVRP.

One important point is that the authors still use Clarke-Wright as part of the solution process. They do not present it as a complete modern solution by itself, but they use an extended Clarke-Wright procedure to build an initial solution before improving it with a broader heuristic framework. This is useful for our project because we also use Clarke-Wright as a practical heuristic reference, not as the only or final answer to the routing problem.

The paper also helps us explain why rich routing problems become difficult quickly. Once time windows, vehicle differences, route timing, and operational constraints are combined, the problem is no longer only about finding the shortest distance. The route has to be feasible in several different ways at the same time.

For our project, this source supports the connection between time-dependent travel, heterogeneous fleets, and heuristic methods. It gives us a stronger reason to discuss these elements together instead of treating them as separate details. The reported savings in the study also show that even small improvements in routing time or route structure can lead to meaningful cost reductions in practice.

There is still a difference between this paper and our project. Their industrial case is richer and more complex than our student-scale implementation. We should therefore use it as conceptual and methodological support, not as if we copied their full model. Our project remains smaller, with 25 stores, one depot, defined demand scenarios, and a solver/heuristic comparison built for the course repository.
