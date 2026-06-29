# Model Justification and Literature Integration

This document explains why we made each modelling decision
and which academic sources support those decisions.

---

## 1. Why is this problem a TDHVRPTW?

Our problem involves delivering pallets from one depot to
25 stores using a mixed fleet of trucks, where each store
must be reached within a specific time slot and travel
times change depending on traffic during the day.

This matches exactly the definition of the Time-Dependent
Heterogeneous Vehicle Routing Problem with Time Windows
(TDHVRPTW) as described in the literature.

The basic VRP was introduced by Dantzig and Ramser (1959)
as the problem of routing vehicles from a central depot to
a set of customers at minimum cost. Our problem extends
this in three directions:

First, our fleet is heterogeneous. We have heavy trucks
with 33 pallets and medium trucks with 12 pallets. Toth
and Vigo (2014) define the Heterogeneous Fleet VRP as the
variant where vehicles have different capacities and
possibly different costs, a problem class surveyed in
depth by Koc, Bektas, Jabali, and Laporte (2016) and
treated formally by Baldacci, Battarra, and Vigo (2008).
This is exactly our case because a medium truck cannot
take over a heavy truck route without violating capacity.

Second, our stores have time windows. All 25 Lidl stores
must receive their delivery between 08:00 and 12:00. This
is the hard time window constraint described by Solomon
(1987), who showed that adding time windows fundamentally
changes the structure of the routing problem and makes it
significantly harder to solve; route-construction and
local-search methods for this constraint class are
reviewed by Braysy and Gendreau (2005).

Third, travel times in our network are not constant. The
OWL road network experiences morning rush hour congestion
between 07:00 and 09:00 that increases travel times by
approximately 30%. Malandraki and Daskin (1992), who
introduced the time-dependent VRP, show that treating
travel times as static in a congested network produces
routes that look optimal on paper but arrive late in
practice, which is why a simple CVRP cannot represent our
problem.

Combining all three extensions gives us the TDHVRPTW,
which is the minimum model that accurately represents the
Dr. Oetker distribution problem.

---

## 2. Why did we choose these constraints?

### Capacity constraint (C4)
Each vehicle route must not carry more pallets than the
truck capacity. This is the fundamental constraint of the
CVRP introduced by Clarke and Wright (1964). Without this
constraint the model would assign unlimited pallets to a
single truck which is physically impossible. Baldacci,
Mingozzi, and Roberti (2012) review exact algorithms that
enforce capacity together with time windows, which is the
same combination of constraints used in our model.

We use two capacity levels: Q_heavy = 33 pallets and
Q_medium = 12 pallets. These values come from standard
European truck configurations for regional food distribution.

### Time window constraint (C6)
All stores must be served between 08:00 and 12:00. This
reflects the real operational policy of Lidl stores in the
OWL region where receiving staff and loading docks are only
available during this window. Solomon (1987) shows that
hard time windows are appropriate when the customer cannot
accept early or late delivery under any circumstances.

### Maximum route duration (C7)
No route may exceed 405 minutes. This comes from German
labour law which requires a 45 minute break after 6 hours
of driving. Goel (2009) studies exactly this interaction
between European driving-hours and rest-period regulations
and vehicle routing and scheduling, and our constraint
follows the same logic: a standard morning shift of 7 hours
minus the break and a 30 minute traffic buffer gives 405
minutes of effective route time.

### Time-dependent travel times (C5)
We apply a congestion multiplier mu(t) to all travel times
based on time of day. The values we use are:
- 07:00 to 09:00: multiply by 1.3
- 09:00 to 11:30: multiply by 1.0
- 11:30 to 12:00: multiply by 1.1

A step function is a practical and commonly used way to
approximate congestion in urban and regional networks when
continuous, sensor-level traffic data is not available.
Malandraki and Daskin (1992) introduced exactly this kind
of step-function travel-time model for the time-dependent
VRP, and it remains a standard simplification in
time-dependent routing models.

### Service time formula
We use s_i = 10 + 2 times q_i minutes at each store.
The 10 minute fixed component covers parking, driver
check-in, and paperwork. The 2 minutes per pallet covers
physical unloading. This follows the common modelling
practice in the VRP literature of using a linear,
demand-dependent service time in heterogeneous fleet
models, and reflects the kind of store-level delivery
operations described for grocery retail by Holzapfel,
Hubner, and Kuhn (2016).

---

## 3. Why did we use Google Maps for the distance and time matrices?

The TDHVRPTW requires real road distances and real travel
times. Using Euclidean straight-line distances would
underestimate actual driving distances because trucks must
follow roads, respect one-way streets, and use motorways
or regional roads depending on the destination.

For this problem a 5 minute error in travel time per arc
multiplied across 25 stores means routes that look feasible
in the model may arrive late in reality. Since our time
windows are hard constraints with only a 4 hour delivery
window, accuracy matters.

Google Maps Distance Matrix API provides actual driving
distances and free-flow travel times between any two
locations using the real road network. We used it to
build a complete 26 by 26 matrix covering the depot and
all 25 stores. This approach follows the broader move
toward rich, realistic VRP variants using real road
network data rather than synthetic instances, as
described by Caceres-Cruz, Arias, Guimarans, Riera, and
Juan (2014).

---

## 4. Why did we choose Clarke-Wright and OR-Tools?

### Clarke-Wright Savings Algorithm
Clarke and Wright (1964) introduced the savings algorithm
as an efficient constructive heuristic for the VRP. It
works by computing a saving value for every pair of
customers that measures how much distance is saved by
combining them on one route instead of serving each with
a separate vehicle.

We chose Clarke-Wright because it is the most cited and
most studied constructive heuristic for the VRP family.
It provides a transparent and interpretable solution
method that allows us to explain step by step how routes
are built. It is also widely used in the OR literature as
a baseline reference algorithm against which other methods
are compared. A closely related, more recent example that
combines the savings idea with local search for a
heterogeneous, time-windowed fleet — methodologically the
closest match to our own setting in the bibliography — is
given by Coelho, Grasas, Ramalhinho, Coelho, Souza, and
Cruz (2016).

The limitation of Clarke-Wright is that it is greedy.
It makes locally good decisions at each step but cannot
go back and correct early mistakes. Because Clarke-Wright
is a greedy constructive heuristic, it cannot guarantee
globally optimal solutions. The quality of the generated
solution depends on the structure of the routing instance
and may be inferior to solutions produced by advanced
metaheuristics.

### OR-Tools with Guided Local Search
Google OR-Tools is an open source Operations Research
solver developed by Google (Google Developers, 2026a,
2026b). We use it with two phases: PATH_CHEAPEST_ARC to
build an initial solution and Guided Local Search to
improve it.

Guided Local Search is a metaheuristic that escapes local
optima by adding penalty terms to arcs that are used too
frequently. This forces the solver to explore alternative
routings and is documented in the metaheuristics literature
to consistently produce better solutions than pure
constructive heuristics (Ropke and Pisinger, 2006; Pisinger
and Ropke, 2007).

We chose OR-Tools because it natively supports
heterogeneous fleets through vehicle-indexed capacity
dimensions, time windows through cumulative time
constraints, and it can handle the time-dependent
callback that applies mu(t) at each arc evaluation.

---

## 5. Comparison: Clarke-Wright vs OR-Tools

We ran both methods on Scenario S-99 (99 pallets, baseline).

| Criterion | Clarke-Wright | OR-Tools GLS |
|-----------|--------------:|--------------:|
| Total distance | 245.90 km | 235 km |
| Solution time | under 1 ms | under 10 sec |
| Routes generated | 4 | 4 |
| All stores served | Yes | Yes |
| Optimality guarantee | None | Near-optimal heuristic solution |

In Scenario S-99, OR-Tools achieved approximately 4 percent
shorter total distance than Clarke-Wright. This is in the
expected direction relative to the VRP literature, where
metaheuristic improvement phases regularly outperform pure
constructive heuristics on medium-sized instances (Ropke
and Pisinger, 2006; Pisinger and Ropke, 2007), though the
margin here is smaller than the 10-30 percent gap typically
reported.

Clarke-Wright is still valuable because it runs instantly
and produces an interpretable solution that shows clearly
why certain stores are grouped together. OR-Tools is
better for production use where solution quality matters
more than speed or transparency.

---

## 6. What are the limitations of our model?

### Simplified congestion model
Our mu(t) step function is a useful approximation but
does not capture link-level traffic variation. The same
multiplier is applied to all arcs at a given time, which
does not reflect that the A2 motorway may be more
congested than a local street. Malandraki and Daskin
(1992) note this same limitation of step-function models
in their original formulation: link-specific time-dependent
functions would be more accurate but require detailed
traffic sensor data that was not available to us.

### No split deliveries
Constraint C1 requires each store to be visited exactly
once by one vehicle. This means a store with 8 pallets
must receive all 8 from the same truck. Allowing split
deliveries could make Scenario S-170 feasible but would
significantly increase the model complexity, as discussed
by Toth and Vigo (2014).

### Static demand
All three scenarios use fixed deterministic demands.
In reality daily demand varies. A stochastic extension
would use probability distributions for demand, along the
lines of the contextual stochastic VRPTW formulation
studied by Serrano, Florio, Minner, Schiffer, and Vidal
(2024), but is beyond the scope of this project.

### Heuristic optimality gap
Clarke-Wright does not guarantee optimality. OR-Tools
with GLS provides near-optimal solutions within the
10 second time limit but also cannot prove optimality.
For a provably optimal solution, an exact branch-cut-and-
price approach such as those of Baldacci, Mingozzi, and
Roberti (2012) or Pecin, Pessoa, Poggi, and Uchoa (2017)
would be needed; implementing one of these was outside the
scope of this project.

---

## References

Baldacci, R., Battarra, M., and Vigo, D. (2008). Routing a
heterogeneous fleet of vehicles. In P. Toth and D. Vigo
(Eds.), The Vehicle Routing Problem (pp. 3–27). Society for
Industrial and Applied Mathematics.
https://doi.org/10.1137/1.9781611973594.ch1

Baldacci, R., Mingozzi, A., and Roberti, R. (2012). Recent
exact algorithms for solving the vehicle routing problem
under capacity and time window constraints. European
Journal of Operational Research, 218(1), 1–6.
https://doi.org/10.1016/j.ejor.2011.07.037

Braysy, O., and Gendreau, M. (2005). Vehicle routing
problem with time windows, Part I: Route construction and
local search heuristics. Transportation Science, 39(1),
104–118. https://doi.org/10.1287/trsc.1030.0056

Caceres-Cruz, J., Arias, P., Guimarans, D., Riera, D., and
Juan, A. A. (2014). Rich vehicle routing problems: From a
logistic policy to a methodologic classification. Central
European Journal of Operations Research, 22(2), 325–347.
https://doi.org/10.1007/s10100-013-0288-5

Clarke, G. and Wright, J.W. (1964). Scheduling of vehicles
from a central depot to a number of delivery points.
Operations Research, 12(4), 568–581.
https://doi.org/10.1287/opre.12.4.568

Coelho, V. N., Grasas, A., Ramalhinho, H., Coelho, I. M.,
Souza, M. J., and Cruz, R. C. (2016). An iterated local
search with a savings heuristic for the heterogeneous
fleet vehicle routing problem with time windows. Journal
of Heuristics, 22(4), 435–461.
https://doi.org/10.1007/s10732-015-9290-7

Dantzig, G.B. and Ramser, J.H. (1959). The truck
dispatching problem. Management Science, 6(1), 80–91.
https://doi.org/10.1287/mnsc.6.1.80

Goel, A. (2009). Vehicle routing and scheduling with
European regulations on driving hours and rest periods.
Transportation Science, 43(1), 39–54.
https://doi.org/10.1287/trsc.1080.0243

Google Developers. (2026a). Vehicle routing problem with
time windows. OR-Tools documentation.
https://developers.google.com/optimization/routing/vrptw

Google Developers. (2026b). Routing options. OR-Tools
documentation.
https://developers.google.com/optimization/routing/routing_options

Holzapfel, A., Hubner, A., and Kuhn, H. (2016). Delivery
operations in grocery retailing: A literature review and
conceptual framework. International Journal of Retail and
Distribution Management, 44(4), 350–377.
https://doi.org/10.1108/IJRDM-05-2015-0068

Koc, C., Bektas, T., Jabali, O., and Laporte, G. (2016).
Thirty years of heterogeneous vehicle routing. European
Journal of Operational Research, 249(1), 1–21.
https://doi.org/10.1016/j.ejor.2015.07.020

Malandraki, C., and Daskin, M. S. (1992). Time dependent
vehicle routing problems: Formulations, properties and
heuristic algorithms. Transportation Science, 26(3),
185–200. https://doi.org/10.1287/trsc.26.3.185

Pecin, D., Pessoa, A., Poggi, M., and Uchoa, E. (2017).
Improved branch-cut-and-price for capacitated vehicle
routing. Mathematical Programming, 161(1), 425–460.
https://doi.org/10.1007/s10107-016-1025-5

Pisinger, D., and Ropke, S. (2007). A general heuristic
for vehicle routing problems. Computers & Operations
Research, 34(8), 2403–2435.
https://doi.org/10.1016/j.cor.2005.09.012

Ropke, S., and Pisinger, D. (2006). An adaptive large
neighborhood search heuristic for the pickup and delivery
problem with time windows. Transportation Science, 40(4),
455–472. https://doi.org/10.1287/trsc.1050.0135

Serrano, B., Florio, A. M., Minner, S., Schiffer, M., and
Vidal, T. (2024). Contextual stochastic vehicle routing
with time windows (arXiv:2402.06968).
https://arxiv.org/abs/2402.06968

Solomon, M.M. (1987). Algorithms for the vehicle routing
and scheduling problems with time window constraints.
Operations Research, 35(2), 254–265.
https://doi.org/10.1287/opre.35.2.254

Toth, P. and Vigo, D. (2014). Vehicle Routing: Problems,
Methods, and Applications. 2nd edition. SIAM.
ISBN: 978-1-611973-58-7
