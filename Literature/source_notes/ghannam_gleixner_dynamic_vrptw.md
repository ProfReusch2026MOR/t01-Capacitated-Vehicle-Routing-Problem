# Ghannam and Gleixner (2023) — Dynamic Vehicle Routing with Time Windows

## Full reference

Ghannam, M., & Gleixner, A. (2023). *Hybrid Genetic Search for Dynamic Vehicle Routing with Time Windows.*


This source is useful because it shows what happens when routing is no longer treated as a fully fixed problem. In the Dynamic Vehicle Routing Problem with Time Windows, customer information can arrive over time, and routes may need to be adjusted while the planning process is already running. That is more complex than our project, but it is still relevant because it highlights how important timing becomes once routing decisions are linked to real operations.

For our project, the main connection is not the dynamic customer-arrival part. Our model is still planned offline. However, we do include time-dependent travel assumptions and delivery time windows, so the paper helps us explain why timing cannot be treated as a small detail. A route is only useful if the vehicle arrives at the right place within the allowed time interval.

The paper is also helpful because it uses Hybrid Genetic Search in a richer VRPTW setting. This connects with the broader literature showing that practical routing often needs heuristics or metaheuristics, especially when time-related constraints are added. In our case, we do not implement HGS, but the source still supports the idea that solver results should be compared with heuristic logic rather than discussed in isolation.

The limitation is that Ghannam and Gleixner study an online dynamic problem, while our project uses fixed scenarios and a known set of 25 stores. We should therefore not present this paper as a direct model template. It is better used to show how recent routing research handles time windows and changing information, and why our simpler offline approach is only one limited version of a broader problem class.
