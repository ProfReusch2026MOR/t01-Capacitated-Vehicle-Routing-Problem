# Uchoa et al. (2017) — Benchmark Instances for the CVRP

## Full reference

Uchoa, E., Pecin, D., Pessoa, A., Poggi, M., Vidal, T., & Subramanian, A. (2017). *New benchmark instances for the Capacitated Vehicle Routing Problem.*


This source is useful to us because it represents the benchmark culture behind modern CVRP research. Uchoa et al. do not focus on one company case or one small routing example. Instead, they provide structured benchmark instances that allow algorithms to be compared more fairly.

That matters for our project because our repository should also be understandable from the outside. We are not creating a benchmark paper, but the same idea still applies: the data should not be hidden inside vague explanations. If we say that our model has 25 Lidl stores, one depot, three demand scenarios, distance matrices, time matrices, and solver outputs, then those elements should be documented clearly enough for another person to inspect them.

For our project, this source mainly supports reproducibility and data transparency. It reminds us that a routing result is only convincing if the instance behind it is clear. That means store nodes, demand values, vehicle capacities, time windows, and scenario definitions should be visible in the repository, not only mentioned in the report.

The source also helps us avoid a common weakness in student projects: using assumptions without showing the structure behind them. Even if some of our data is estimated, the instance should still be organized and traceable. That is the practical lesson we take from this benchmark literature.

The limitation is that Uchoa et al. focus on the CVRP, not on our full TDHVRPTW setting. Their work does not directly include time-dependent travel, heterogeneous fleets, or Lidl-specific time-window assumptions. So we use this source mainly for benchmark thinking, reproducibility, and clear instance documentation.
