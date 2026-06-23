# Serrano, Florio, Minner, Schiffer and Vidal (2024) — Contextual Stochastic VRPTW

## Full reference

Serrano, B., Florio, A. M., Minner, S., Schiffer, M., & Vidal, T. (2024). *Contextual Stochastic Vehicle Routing with Time Windows.*


This paper is useful because it shows how modern vehicle routing research deals with uncertainty. The authors focus on a VRPTW setting where travel times are not treated as perfectly fixed. Instead, historical and contextual information is used to make better routing decisions when travel times are uncertain.

For our project, this is relevant because our model also contains uncertainty, even if we do not model it in the same advanced way. We work with demand scenarios and time-dependent traffic assumptions. That is a simpler approach, but the logic is similar: real delivery planning cannot rely only on one fixed “average” situation.

The paper also helps explain why scenario analysis makes sense in our repository. Since we do not have enough data or time to build a full stochastic optimization model, we use baseline, high-volume, and stress-test scenarios as a practical compromise. This allows us to test how the routing system behaves under different demand levels without pretending that one single demand estimate is perfectly true.

Another useful point is that the paper links routing decisions with travel-time uncertainty. In our case, this supports the use of congestion factors and time-dependent travel assumptions. Even though our implementation is much simpler, the source gives academic support to the idea that travel time should not always be treated as constant.

The limitation is clear. Serrano et al. use more advanced stochastic and data-driven methods than we can realistically implement in this course project. We therefore use the paper to support the reasoning behind uncertainty and scenario design, not as a direct model template.
