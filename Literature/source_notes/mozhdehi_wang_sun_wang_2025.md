# Mozhdehi, Wang, Sun and Wang (2025) — Multi-Trip Time-Dependent VRP with Working-Hour Constraints

## Full reference

Mozhdehi, A., Wang, Y., Sun, S., & Wang, X. (2025). *SED2AM: Solving Multi-Trip Time-Dependent Vehicle Routing Problem using Deep Reinforcement Learning.*


This paper is useful as a recent example of where time-dependent vehicle routing research is heading. The authors study a richer routing problem where vehicles can perform multiple trips, travel conditions depend on time, and maximum working-hour constraints also have to be respected. That combination is close to real urban logistics, where a route is not only limited by distance or capacity, but also by the time structure of the working day.

For our project, the most relevant part is not the deep reinforcement learning method itself. We are not using that kind of model. What matters more is the problem setting: time-dependent travel and working-hour limits are treated as important routing constraints. This supports the way our project includes route-duration logic, traffic factors, and delivery-time feasibility instead of only minimizing kilometres.

The paper also helps us explain the boundary of our project. We use a smaller and more explainable OR approach, while this source represents a more advanced research direction. That distinction is useful. It shows that we are aware of newer learning-based methods, but we deliberately keep our implementation focused on transparent optimization and heuristic comparison.

The limitation is that this source is not a direct model template for our repository. It uses deep reinforcement learning and a multi-trip setting, while our implementation is built around OR-Tools, Clarke-Wright logic, fixed demand scenarios, and a 25-store regional case. So we should cite it as frontier literature for time-dependent routing with work-hour constraints, not as the method we actually implemented.
