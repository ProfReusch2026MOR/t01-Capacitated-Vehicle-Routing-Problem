Introduction

This report describes the mathematical model we built to solve the daily delivery problem between the Dr. Oetker depot in Bielefeld and 25 Lidl stores in the OWL region. The model is classified as a Time-Dependent Heterogeneous Vehicle Routing Problem with Time Windows, or TDHVRPTW. We chose this model because our problem has three features that simpler models do not handle: trucks of different sizes, strict delivery time slots for each store, and travel times that change depending on the time of day due to traffic.

The network we work with has 26 locations in total. Node 0 is the depot at Lutterstraße 14, Bielefeld. Nodes 1 to 25 are the Lidl stores we need to deliver to. The distances and travel times between all locations come from real road data collected through the Google Maps Distance Matrix API, giving us a complete 26 by 26 matrix.

We test three demand situations in this project. The first is a normal working day with 99 pallets to deliver. The second is a busier day with 150 pallets. The third is a stress test with 174 pallets, which we designed to find the limits of the current fleet. The mathematical structure is the same for all three situations. Only the demand values change.
 
1. Model Parameters

Before writing the equations, we need to define the key values and rules the model works with. These come directly from the operational data we collected.

The Network
We have 26 nodes in total. Node 0 is the Dr. Oetker depot in Bielefeld, which is where all trucks start and finish their day. Nodes 1 through 25 are the Lidl stores spread across the OWL region. The full set of nodes is written as V = {0, 1, 2, ..., 25}. When we talk about customer nodes only, without the depot, we use the set S = {1, 2, ..., 25}.

Distances and Travel Times
For every pair of locations i and j, we have two values. The first is c_ij, which is the road distance in kilometres between them. The second is t_ij, which is the baseline free-flow driving time in minutes. We collected both of these from the Google Maps API, so they reflect real roads rather than straight-line estimates.

Store Demands
Each Lidl store has a demand value q_i, measured in Euro pallets. In the baseline scenario S-99, stores are grouped into three demand levels: low (3 pallets), medium (4 pallets), and high (5 pallets). Across all 25 stores, the total in S-99 is 99 pallets. The depot has no demand, so q_0 = 0.

Service Time at Each Store
When a truck arrives at a store, it needs time to unload and complete the paperwork. We calculate this time using a simple formula that depends on how many pallets are being delivered:
sᵢ  =  10  +  2 × qᵢ   (minutes)
The 10 minutes is a fixed base that covers parking, signing in, and the administrative process. The 2 minutes per pallet covers the physical unloading. So a store receiving 4 pallets gets 18 minutes of service time, and a store receiving 5 pallets gets 20 minutes.

Delivery Time Window
All stores must receive their delivery between 08:00 and 12:00. In the model we express time in minutes past midnight, so the window is [480, 720]. If a truck arrives before 08:00, it waits until the store opens. If a truck cannot reach a store before 12:00, that route is not feasible.

Maximum Route Length
No truck is allowed to be out for more than 405 minutes. We calculated this from a standard 480-minute morning shift, minus a mandatory 45-minute rest break, minus a 30-minute buffer for unexpected delays. All truck types follow this same limit.

Waiting Slack
Because trucks leave at 07:00 and stores only open at 08:00, trucks that reach their first stop early have to wait. We set a scenario-specific waiting allowance to handle this. For S-99 it is 45 minutes, for S-152 it is 75 minutes, and for S-170 it is 90 minutes. This does not change the delivery window itself. It just allows the solver to accept routes where a truck arrives early at a stop and waits, rather than rejecting them entirely.
 
2. The Fleet

We have two types of trucks available. Together they form the heterogeneous fleet K. The fleet is split into two groups:

K  =  K_heavy  ∪  K_medium

Truck Type	Capacity Qᵏ	Number Available	Used For
Heavy trucks (K_heavy)	33 pallets	4 trucks	Large delivery clusters, high-demand routes
Medium trucks (K_medium)	12 pallets	4 trucks	Urban areas, small-demand stores, short loops

This gives us a total fleet capacity of 180 pallets across all 8 trucks. Each truck has its own capacity limit Q_k, which depends on which group it belongs to. A heavy truck can carry up to 33 pallets per route. A medium truck can carry up to 12.
 
3. Traffic Model

One of the key features of our model is that travel times are not fixed. They depend on what time of day the truck is driving. We use a step function called μ(t) to multiply the baseline travel times based on the time elapsed since 07:00 departure.

Actual travel time(i → j, t)  =  tᵢⱼ  ×  μ(t)

The function μ(t) takes three values depending on the time:

Time of Day	Minutes from 07:00	μ(t)	What It Means
07:00 – 09:00	0 to 120	1.3	Roads are 30% slower due to morning rush hour on the A2 and B61
09:00 – 11:30	120 to 270	1.0	Normal speed, no significant congestion
11:30 – 12:00	270 to 300	1.1	A small slowdown as lunch traffic starts to build

This means all trucks departing at 07:00 face heavier traffic on their first stops. Once the clock passes 09:00, routes run at normal speed. The reason we included this is straightforward: if we assumed constant travel times, the model would produce schedules that look fine on paper but would regularly arrive late in reality.

3a. Demand Scenarios
We test the model under three different demand levels to understand how the system behaves as pressure increases:

Scenario	What It Represents	Total Pallets	Result
S-99	A normal weekday delivery run	99 pallets	✓ Works
S-152	A busy day, like before a holiday	150 pallets	✓ Works
S-170	A stress test at near-maximum load	174 pallets	✗ Not feasible

The mathematical model is exactly the same for all three scenarios. The only thing that changes is q_i, the demand at each store. We designed S-170 on purpose to push the system past its limits and see where it breaks. The result of that test is not a failure of the model — it is the model correctly telling us that 174 pallets cannot be delivered within the given time window with the current fleet.
 
4. Variables and Notation

The table below lists all the symbols used in the equations that follow.

Symbol	What It Represents
V	All 26 nodes: V = {0, 1, ..., 25}
S	Store nodes only: S = {1, 2, ..., 25}
K	The full fleet: K = K_heavy ∪ K_medium
Qᵏ	Carrying capacity of vehicle k (33p for heavy, 12p for medium)
qᵢ	Number of pallets that store i needs delivered
cᵢⱼ	Road distance between nodes i and j (km)
tᵢⱼ	Baseline free-flow travel time between i and j (minutes)
sᵢ	Time spent at store i = 10 + 2 × qᵢ (minutes)
[eᵢ, lᵢ]	Delivery window at store i: [480, 720] minutes past midnight
T_max	Maximum route duration: 405 minutes
μ(t)	Congestion multiplier applied to travel time at time t
xᵢⱼᵏ	1 if vehicle k drives from node i to node j, 0 if not
Tᵢᵏ	The time vehicle k arrives at node i (minutes past midnight)
Wᵢᵏ	How long vehicle k waits at node i before the store opens
εᵏ	Maximum allowed waiting time per scenario (45 / 75 / 90 min)
M	A very large number (99,999) used in the Big-M method

The two decision variables are x_ijk and T_ik. These are the unknowns the solver must find. x_ijk is binary — it is either 0 or 1. T_ik is continuous — it can take any non-negative value. All other symbols are known parameters that we set before running the solver.
 
5. Objective Function

The goal of the model is simple: minimise the total kilometres driven by all trucks across all routes.
Minimise  Z  =  Σ k∈K  Σ i∈V  Σ j∈V  cᵢⱼ · xᵢⱼᵏ
This formula adds up the distances of all arcs that are actually used. When x_ijk = 1, the distance c_ij for that arc is counted. When x_ijk = 0, the arc is not used and adds nothing. Minimising Z pushes the solver to find routes that are as short as possible while still satisfying all the constraints below.

We chose distance rather than cost as the objective because it is the most direct measure of routing efficiency and it avoids the need to estimate or assume fuel prices, which can vary. Travel time considerations are handled through the constraints rather than the objective.
 
6. Constraints

The constraints are the rules the solver must respect when finding routes. There are nine of them. Together they make sure the routes are physically possible, operationally valid, and legally compliant.

C1 — Every store must be visited exactly once
Σ k∈K  Σ j∈V  xᵢⱼᵏ  =  1     for all i in {1, ..., 25}
This is one of the most fundamental rules. Each Lidl store gets exactly one delivery, from exactly one truck. If we used ≥ 1 instead of = 1, the solver could send two trucks to the same store, which is not how real deliveries work. Setting it to exactly 1 avoids this.

C2 — What goes in must come out
Σ j∈V  xᵢⱼᵏ  −  Σ j∈V  xⱼᵢᵏ  =  0     for all i in V, for all k in K
If a truck enters a node, it must also leave it. This applies to every node including the depot. This constraint keeps routes connected and prevents the solver from building paths that start or end inside a store.

C3 — Each truck leaves the depot at most once
Σ j∈S  x₀ⱼᵏ  ≤  1     for all k in K
A truck can only depart from the depot once per day. Trucks that are not needed stay at the depot and are never activated. The ≤ 1 allows for this possibility, unlike = 1 which would force every truck to be used.

C4 — Each truck returns to the depot at most once
Σ i∈S  xᵢ₀ᵏ  ≤  1     for all k in K
After finishing its deliveries, each truck returns to the depot exactly once. Combined with C3, this ensures every active truck makes a single round trip from and back to node 0.

C5 — Trucks cannot carry more than they can hold
Σ i∈S  qᵢ (Σ j∈V  xᵢⱼᵏ)  ≤  Qᵏ     for all k in K
This adds up all the pallets assigned to a truck's route and checks that the total does not exceed what that truck can carry. For heavy trucks this limit is 33 pallets. For medium trucks it is 12 pallets. Because each truck has its own Q_k value, this constraint automatically handles the different sizes without any extra logic.

C6 — Arrival times must flow forward correctly with traffic
Tᵢᵏ + sᵢ + [μ(Tᵢᵏ + sᵢ) × tᵢⱼ]  −  M(1 − xᵢⱼᵏ)  ≤  Tⱼᵏ
This is the most technical constraint in the model. It does two things at once.

First, it makes sure arrival times move forward correctly along the route. When a truck leaves node i, its arrival at node j must account for the time already spent at i (the arrival time T_ik), the service time s_i, and the travel time from i to j adjusted for traffic using μ(t).

Second, it eliminates subtours. A subtour is a loop that is disconnected from the depot, for example a small circular route between three stores that never visits the depot. Because arrival times can only increase along the route, and the depot is the only starting point, any loop that does not connect back to the depot would require arrival times to go backwards at some point, which this constraint prevents.

The M term in the formula is the Big-M technique. M is a very large number (99,999). When an arc is not used (x_ijk = 0), the term −M(1 − 0) = −M makes the left side so small that the constraint is automatically satisfied regardless of the arrival times. When the arc is used (x_ijk = 1), the M term disappears and the constraint is active.

C7 — Stores must be visited during their opening hours
480  ≤  Tᵢᵏ  ≤  720     for all i in {1, ..., 25}, for all k in K
Every truck must arrive at a store between 08:00 (minute 480) and 12:00 (minute 720). If a truck arrives before 08:00 it waits, which is allowed. If it cannot reach a store before 12:00, that route is infeasible and the solver must find another combination.

C8 — Waiting time at stores is bounded
This constraint was not in the original formulation. We added it here to fully document the model.

0  ≤  Wᵢᵏ  ≤  εᵏ     for all i in {1, ..., 25}, for all k in K
When a truck arrives at a store before 08:00, it has to wait. W_ik is the waiting time of truck k at store i. We set a maximum waiting limit ε_k per scenario: 45 minutes for S-99, 75 minutes for S-152, and 90 minutes for S-170. Without this constraint, the solver would reject routes where trucks arrive early, even though those routes are perfectly valid in practice. The limit also prevents the solver from accepting solutions where trucks are parked waiting for an unreasonably long time.

C9 — Variable types
xᵢⱼᵏ  ∈  {0, 1}     and     Tᵢᵏ  ≥  0
x_ijk must be a binary integer — either a truck uses an arc or it does not, there is no in-between. T_ik is a continuous variable that can take any non-negative real value. Because of the binary variables, this problem is classified as a Mixed-Integer Linear Programme (MILP), which is why a specialised solver like OR-Tools is needed rather than a simple linear programme solver.
 
7. Model Summary

Below is the complete model in one place for reference.

Minimise  Z  =  Σ k∈K  Σ i∈V  Σ j∈V  cᵢⱼ · xᵢⱼᵏ

Subject to:

Ref	Constraint	What It Enforces
C1	Σ k,j x_ijk = 1  ∀i∈S	Each store visited by exactly one truck
C2	Σj x_ijk − Σj x_jik = 0  ∀i,k	Every truck that enters a node must leave it
C3	Σj x_0jk ≤ 1  ∀k	Each truck departs the depot at most once
C4	Σi x_i0k ≤ 1  ∀k	Each truck returns to the depot at most once
C5	Σi qi(Σj x_ijk) ≤ Qk  ∀k	Load on each truck stays within its capacity
C6	T_ik+s_i+μ(T_ik+s_i)·t_ij−M(1−x_ijk) ≤ T_jk	Arrival times advance correctly with traffic
C7	480 ≤ T_ik ≤ 720  ∀i∈S	Stores visited within 08:00–12:00
C8*	0 ≤ W_ik ≤ εk  ∀i∈S	Early arrivals can wait up to the slack limit
C9	x_ijk ∈ {0,1},  T_ik ≥ 0	Variable domains

* C8 is an addition to the original formulation.

Network: 26 nodes — 1 depot (Node 0) + 25 Lidl stores (Nodes 1–25)
Fleet: 4 heavy trucks (33p each) + 4 medium trucks (12p each) = 180p total capacity
Decision variables: x_ijk ∈ {0,1} for routing, T_ik ≥ 0 for arrival times
 
Conclusion

This document describes the full mathematical model we use for the Dr. Oetker delivery problem. The model has nine constraints covering every operational requirement: which stores get visited, how trucks move through the network, how much they can carry, when they arrive, how long they can drive, and how traffic affects their journey.

Compared to the original formulation PDF, we added two things. The first is the three-scenario framework (S-99, S-152, S-170), which was being tested in the code but not documented in the equations. The second is Constraint C8, which covers the waiting slack parameter that was already in the solver but had not been formally written down. Everything else in the original formulation was already correct and has been kept exactly as it was.

The model is implemented in Python using Google OR-Tools with Guided Local Search, as described in the project solver file DrOetker_Lidl_Optimization_REALISTIC.py. The results for all three scenarios are documented in the Results folder of the repository 

