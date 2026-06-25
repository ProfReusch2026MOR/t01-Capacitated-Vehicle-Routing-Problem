## Scope and alignment

This literature review supports our final Operations Research project, which is formulated as a Time-Dependent Heterogeneous Fleet Vehicle Routing Problem with Time Windows (TDHVRPTW) for 25 Lidl stores and one depot, resulting in 26 network nodes in total. The main methodological support is based on recent literature from the last decade, while older foundational sources are not discussed in detail and are only used where necessary to identify the historical origin of specific methods or problem classes. This structure was chosen because the earlier repository version contained placeholders and overly general summaries that did not sufficiently justify the final project formulation, the computational approach, or the assumptions used in the model.
*****

## 2.1. Classification within the Operations Research Domain 

This project addresses a combinatorial optimization problem within the field of Rich Vehicle Routing Problems (RVRPs), a class of models introduced in the Operations Research (OR) literature to represent routing problems that extend beyond the assumptions of the classical Vehicle Routing Problem (VRP); unlike traditional VRP (first introduced by Dantzig and Ramser in 1959 in "The Truck Dispatching Problem"), RVRPs incorporate multiple real-world constraints, such as strict delivery time windows, limited vehicle capacities, ergonomic considerations (for example driver-service ergonomic related constraints), multiple depots, customer priorities, and traffic or road restrictions (Cáceres Cruz, et al. 2014). By considering this practical focus, RVRP models enable the development of mathematical formulations and solution algorithms that more accurately reflect real distribution systems, producing solutions that are both operationally feasible and applicable in industrial settings.
Specifically, this project focuses on the Heterogeneous Fleet Vehicle Routing Problem with Time Windows (HFVRPTW), a variant of the RVRP that considers fleets composed of vehicles with different capacities and operational characteristics while satisfying customer time-window constraints. The proposed mathematical model was developed following an extensive review of the relevant OR literature, with particular emphasis on studies addressing heterogeneous fleets and time-constrained routing problems described in the bibliography section.
In high-frequency resupply networks, such as the distribution system analyzed in this present document, ignoring differences in vehicle capacities and urban accessibility constraints may lead to substantial operational inefficiencies like poor vehicle utilization, increased transportation costs, unnecessary trips, violations of delivery time windows, and the assignment of vehicles that are unable to access certain delivery locations due to road regulations, low-emission zones, weight restrictions, or limited urban infrastructure. As a result, the simplifying assumptions of the classical VRP is scarce to represent the operational complexity of modern distribution systems, making richer formulations such as the HFVRPTW a more appropriate modeling framework.

Furthermore, with a mathematical approach, the HFVRPTW is part of a NP-hard formulation according to (Gendreau et al., 1999) since it amalgams two type of sub-combinational problems of exponential scale: 
Bin Packing Problem (BPP): Decide with sub-set of clients and demands are assigned to which sub-set of clients for each demand without exceeding its volumetric or maximum weight capacity (Qk).
Traveling Salesman Problem with Time Windows (TSPTW): Determine the optimal sequence of visit (arc-sequence) for each activated vehicle guaranteeing that the time arrival (tik) is in the correct time interval for each of the nodes of the system. 

## 2.2 Main pillars of this HFVRPTW case study model

Time Windows
The formal integration of temporal variables and restrictive service time windows in vehicle routing was consolidated by Solomon (1987), whose work Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints remains a key reference in OR literature for benchmarking routing algorithms. In his study, Solomon showed that introducing time windows significantly reduces the feasible solution space.  However, even though this reduction might suggest a simpler problem, it actually introduces additional computational difficulty when solving it with exact or heuristic methods. In particular, determining whether a feasible solution exists becomes more complex due to the mismatch between spatial proximity and temporal compatibility: two customers that are geographically close may still be incompatible within the same route if their service time windows do not overlap.
Heterogeneous Fleet and Cost Offsets 

Some authors like Gendreau et al. (1999) and, subsequently, Baldacci et al. (2008) formalized the Heterogeneous Fixed Fleet VRP (HFFVRP) and the Fleet Size and Mix VRP (FSMVRP), respectively. In their work, they showed that the objective function of a realistic OR model cannot be restricted to exclusively minimizing total travel distance alone. Instead, it must capture a fundamental cost trade-off structure.
The authors demonstrated the existence of a mathematical trade-off between fixed and variable costs associated with different vehicle types. For instance, deploying a heavy articulated truck involves a high fixed operational cost (FixedCostₖ), but benefits from a lower variable cost per pallet-kilometer (VariableCostₖ). In contrast, a light rigid vehicle has a significantly lower activation cost, but reaches its capacity limits much earlier, which increases the number of required trips and, consequently, the total variable cost.

Heuristic algorithms
As computational power increased and gained relevance in OR formulations, researchers began to integrate more complex and realistic constraints into routing models. A clear example is Cáceres-Cruz et al. (2014), who mapped the state of the system in RVRPs, concluding that the combination of  HFVRPTW represents one of the most practically relevant frontiers in transportation decision support systems (DSS).
Although their investigations also showed that when these constraints are incorporated into exact mathematical solvers, computational times grow exponentially. This scalability limitation is particularly critical in real-world applications, where decision-making must be performed within short time frames. For this reason, heuristic and metaheuristic algorithms are essential, as they are designed to efficiently explore the solution space and generate high-quality near-optimal solutions in reasonable computational times, especially for instances exceeding 25 to 30 nodes where exact methods often become computationally intractable.
Food Logistics and Retail Context in Germany 

In order to maintain consistency with the real operational conditions of Dr. Oetker and Lidl considered in this study, Holzapfel et al. (2016) analyzed the distribution structures of discount supermarket chains in Germany. Their study showed that the time windows imposed by retailers such as Lidl are typically “hard time windows” (strict delivery time intervals that must be satisfied, otherwise the solution is infeasible) due to the high level of synchronization required at unloading docks (cross-docking operations), as well as German regulations on driving and rest times for professional drivers (Fahrpersonalverordnung – FPersV).

Furthermore, they confirmed that fleet heterogeneity is not merely a modeling assumption but a physical requirement in practice, since certain urban centers restrict the access of trucks exceeding 12 tons during daytime hours. This restriction forces the use of smaller commercial vehicles for last-mile distribution or requires transshipment operations between heavy and light-duty vehicles.

## 2.3. Modeling Approaches in Rich Vehicle Routing

The formulation of the Heterogeneous Fleet Vehicle Routing Problem with Time Windows (HFVRPTW) in the literature generally follows one of three primary mathematical modeling approaches, depending on the specific characteristics of the decision-making process:

Three-Index Formulation (Arc-Based Models): This framework is widely recognized as the standard extension of the classical vehicle routing problem when dealing with non-homogeneous assets (Irnich et al., 2014). This model relies on a binary decision variable $x_{ijk}$, which equals 1 if vehicle $k$ directly traverses the directed arc $(i, j)$ connecting two physical nodes within the spatial network, and 0 otherwise.To couple spatial routing with temporal constraints, this approach incorporates continuous tracking variables, traditionally defined as $t_{ik}$, representing the exact arrival time of vehicle $k$ at node $i$. 
Advantage: The introduction of the vehicle index $k$ forces the decision space to scale quadratically with the number of customers and linearly with the total fleet size, leading to an overall variable complexity of $O(N^2K)$.
Matrix Relaxation Weakness: Subtour elimination constraints and time window integrations are explicitly modeled via extensive Big-M formulations (e.g., $t_{ik} + s_i + \tau_{ij} - M(1 - x_{ijk}) \le t_{jk}$). These linear continuous relaxations are notoriously loose. Consequently, standard commercial mixed-integer linear programming (MILP) solvers struggle to prune the branch-and-bound tree effectively, making this approach computationally impossible for instances scaling beyond 20 to 30 customer nodes. However, it remains highly favored in the literature when exact operational control over specialized vehicle properties on explicit arcs is non-negotiable.

Two-Index Formulation: To mitigate the severe coordinate-space expansion of three-index formulations, modern adaptations frequently collapse individual vehicle tracking by aggregating the heterogeneous fleet into distinct, homogeneous vehicle classes or types (Toth and Vigo, 2014). The principal binary decision variable is reduced to $x_{ij}^m$, which denotes whether any vehicle belonging to class $m$ traverses the arc $(i, j)$.Instead of relying on continuous time variables per vehicle, subtour elimination and capacity utilization are handled implicitly by transforming the routing architecture into a multi-commodity network flow problem. Here, continuous variables represent the flow of physical load units or accumulated elapsed time along the arcs. While this drastically compresses memory requirements and reduces the overall integer variable count to $O(N^2M)$ (where the number of classes $M$ is significantly smaller than the total fleet size $K$), it introduces complex multi-commodity tracking constraints. Furthermore, managing individual vehicle fixed activation costs ($\text{FixedCost}_k$) becomes a complex task if a specific class contains a finite, fixed number of assets rather than an infinite pool, often requiring additional cutting planes to prevent the over-allocation of specialized vehicles.

Set Partitioning Formulation (Route-Based Models): This paradigm fundamentally changes the decision domain by shifting the optimization from arc selections to entire path trajectories. Let $\Omega$ represent the complete pool of all mathematically feasible routes that a heterogeneous vehicle type can execute while completely satisfying capacity limits and hard time windows. The model utilizes a binary decision variable $y_r$, which equals 1 if route $r \in \Omega$ is selected in the final logistics plan, and 0 otherwise. This structure shifts the mathematical complexity from the solver's branch-and-bound tree to the route-generation phase, serving as the foundation for modern exact decomposition methods.

## 2.4 Typical Constraints in Real-World Applications

While the classical Vehicle Routing Problem (VRP) simplifies outbound logistics by assuming unrestricted urban access, homogeneous fleets, and flexible delivery timing, industrial distribution networks must integrate a multi-layered matrix of operational and legal restrictions to simulate reality in the best possible way. The literature classifies these into several categories:

Temporal Constraints: These include Hard Time Windows, where early arrival forces waiting and late arrival causes immediate infeasibility (Bräysy and Gendreau, 2005), and Soft Time Windows, where violations are permitted but penalized financially within the objective function to evaluate cost-service trade-offs (Figliozzi, 2010). More recently, the literature has moved beyond static, deterministic time windows altogether: Ghannam and Gleixner (2023) adapt Hybrid Genetic Search to a dynamic VRPTW in which customer information arrives in batches over the planning horizon, while Serrano, Florio, Minner, Schiffer, and Vidal (2024) develop data-driven prescriptive models for a contextual stochastic VRPTW with uncertain travel times. Although the present project remains static and scenario-based rather than fully dynamic or stochastic, these recent works support treating travel-time variability and scenario-based demand as a deliberate, literature-aligned simplification rather than an omission.

Physical and Infrastructure Compatibility: Vehicles face compatibility constraints based on customer locations and urban regulations (Cáceres-Cruz et al., 2014). Certain retail centers or urban zones restrict access based on maximum weight (e.g., vehicles over 12 tons), vehicle length, or strict emission standards in Low Emission Zones (Holzapfel et al., 2016). Additionally, specific products might require specialized fleet assets, such as refrigerated compartments for perishable food logistics.

Driver and Labor Regulations: Real applications must respect legal frameworks regarding working hours. In Germany and the European Union, this involves strict compliance with driving and rest time allocations regulated by the Fahrpersonalverordnung – FPersV (Holzapfel et al., 2016), which directly impacts route duration constraints and maximum allowable driving shifts (Goel, 2009).

## 2.5 Exact Solver Approaches in the Literature

In modern Operations Research literature, the most prominent exact methods include:

Branch-and-Cut (B&C): An exact methodology where valid inequalities (such as subtour elimination, capacity cuts, or knapsack-like constraints) are dynamically added to tighten the linear programming relaxation, significantly reducing the search space before branching (Pecin et al., 2017).

Branch-and-Price (B&P): A framework that applies Column Generation to the Set Partitioning formulation (Feillet, 2010). Since the number of possible feasible routes is exponential, the algorithm starts with a small subset of routes and solves a pricing sub-problem—usually modeled as a Shortest Path Problem with Resource Constraints (SPPRC)—to dynamically inject profitable routes into the master problem.

Branch-and-Cut-and-Price (BCP): Currently representing the state-of-the-art boundary for exact solvability in heterogeneous routing, this hybridized approach combines the dynamic generation of both columns (routes) and rows (cutting planes), allowing exact solvers to tackle complex instances up to roughly 100 nodes (Baldacci et al., 2008; Pessoa, Sadykov, & Uchoa, 2018).

## 2.6 Heuristic and Approximate Approaches

Because the HFVRPTW belongs to the class of NP-hard formulations, exact solvers often fail to find solutions within reasonable operational timeframes when instances scale past 30–50 nodes (Cáceres-Cruz et al., 2014). To circumvent this, researchers utilize heuristic and metaheuristic frameworks designed to find high-quality, near-optimal solutions efficiently:

Classical Heuristics (Constructive & Improvement)
Modified Savings Frameworks: Modern adaptations of constructive algorithms alter the traditional "routing savings" calculations to dynamically incorporate heterogeneous capacity thresholds and fixed vehicle activation costs simultaneously (Coelho et al., 2016). More recently, Peric, Begovic, and Lesic (2024) extend the classical Clarke and Wright savings procedure with an adaptive-memory metaheuristic for a real-world routing problem that combines heterogeneous vehicles, hard and soft time windows, and time-dependent travel times, reporting average savings of 2.03% in delivery time and 20.98% in total delivery cost relative to prior methods. This confirms that the savings heuristic remains a relevant constructive method in modern, constraint-rich pipelines, provided it is paired with a stronger improvement phase—directly supporting this project's own use of Clarke–Wright as an initial-solution generator ahead of OR-Tools improvement.

Time-Oriented Insertion Heuristics: These algorithms sequentially insert unassigned customers into existing routes based on a weighted combination of spatial minimization and temporal delay minimization tailored for tight windows (Bräysy and Gendreau, 2005).

Metaheuristics (Local Search Frameworks)
Large Neighborhood Search (LNS) and Adaptive LNS (ALNS): Widely considered the gold standard for rich VRP variants (Pisinger and Ropke, 2007). ALNS works by iteratively destroying a portion of the current solution (removing customers using heuristics like random, worst, or radial removal) and rebuilding it using repair heuristics (Ropke and Pisinger, 2006). The algorithm adaptively learns which destroy/repair pairs perform best during the search.

Variable Neighborhood Search (VNS) and Tabu Search: These methods navigate local search spaces by systematically changing neighborhood structures (e.g., swapping nodes between routes) while maintaining memory logs or structures to prevent the algorithm from getting trapped in local optima (Bräysy and Gendreau, 2005).

Hybrid Genetic Algorithms: Population-based metaheuristics that evolve a set of routing solutions over generations using advanced crossover and mutation operators, frequently hybridized with local search techniques to fix time window and capacity violations dynamically (Vidal et al., 2013; Vidal, 2022).

On the question of scale, Accorsi and Vigo (2023) show that a carefully engineered heuristic can solve CVRP instances with up to one million customers in practical time, while Kerscher and Minner (2024) propose a spatial-temporal-demand clustering framework that decomposes large VRPTW instances using similarity measures combining location, timing, and demand rather than spatial proximity alone. Although the present 26-node instance is several orders of magnitude smaller than either study, both works support the broader principle—already embedded in this project's data and scenario design—of treating distance, time windows, and demand jointly rather than as separate, sequentially handled concerns. Finally, Wu et al. (2024) survey neural combinatorial optimization solvers for vehicle routing problems and find that, despite rapid progress, these methods still struggle with generalization, large-scale instances, and fair comparison against conventional OR algorithms; Mozhdehi, Wang, Sun, and Wang (2025) report a deep reinforcement learning approach for a multi-trip, time-dependent VRP with working-hour constraints that outperforms existing baselines on real-world data from two Canadian cities. These recent results motivate this project's choice to remain within the classical OR toolchain (Clarke–Wright and Google OR-Tools) rather than adopt a learning-based solver, while acknowledging that learning-based routing is an active and fast-moving research frontier that may be more appropriate at larger operational scales.

## 2.7 Data Requirements for Model Implementation

To successfully operationalize an HFVRPTW model, a comprehensive dataset of spatial, temporal, fleet, and demand characteristics is required.

Specific Parameters Required for each data Category
*Network & Spatial Data: Latitude/Longitude coordinates of all nodes; asymmetric travel distance matrices; asymmetric travel time matrices (Cáceres-Cruz et al., 2014)
*Demand Data: Deterministic demand volume per customer ($d_i$) measured in pallets, weight, or volume units matching fleet capacities ((Koç et al., 2016).
*Temporal Data:Hard or soft time window intervals ($[e_i, l_i]$) for each customer; service/unloading time required at each node ($s_i$) (Bräysy and Gendreau, 2005).
*Fleet Configurations: Number of available vehicles per category $k$; volumetric/weight capacity ($Q_k$); fixed activation cost ($\text{FixedCost}_k$); variable cost per kilometer ($\text{VariableCost}_k$) (Baldacci et al., 2008). 

## 2.8 Problem Simplifications and Operational Acceptability

To ensure the mathematical model developed in this project remains computationally feasible while still providing highly valuable decisions for the distribution networks of Dr. Oetker and Lidl, certain simplifications to the real-world problem were applied.Following established Operations Research literature, these assumptions are explicitly stated and justified from an operational and structural perspective:

*Deterministic Travel Times and Demand: The model treats travel times between nodes and customer demands as constant, known parameters, omitting real-time traffic stochasticity or sudden demand fluctuations. In high-frequency German retail supply chains, demand is heavily stabilized via advanced Electronic Data Interchange (EDI) systems, meaning order quantities are fixed before routing execution begins (Holzapfel et al., 2016). Furthermore, travel times are calculated using historical averages that incorporate standard urban delays, making a deterministic approximation highly reliable for day-ahead tactical planning (Cáceres-Cruz et al., 2014). In order to simulate traffic congestion, it was applied a security factor according to the OWL region (shown in data collection), this ensures that we can run the model and cover the demand in different traffic scenarios, and also, it gives us the possibility to consider different type of vehicles sizes used depeding on the time of the day. 

Homogeneous Service Times: Unloading and service times ($s_i$) at customer nodes are calculated based on average standard durations rather than fluctuating dynamically based on specific crew sizes or unexpected dock delays. Large retail actors like Lidl operate under highly synchronized cross-docking and logistics standards (Holzapfel et al., 2016). Dock scheduling slots are strictly regimented, forcing service times to conform tightly to planned averages, which justifies treating them as deterministic parameters in the temporal constraints.Single-Period Planning Horizon: The routing optimization is executed for a single operational shift or day, without modeling multi-period vehicle re-allocation over a weekly horizon. High-frequency grocery and food resupply networks, such as those governing perishable or ambient food distribution, operate on a daily turnaround cycle due to product freshness and strict continuous replenishment strategies (Holzapfel et al., 2016). Optimizing on a daily rolling horizon matches the true organizational structure of the dispatching teams without introducing the exponential variable growth of multi-period formulations.

***********
# # Different Authors referred in the project FORMAT: (lastaname, year).

##  Uchoa et al.:
What we learned. Uchoa et al. provide modern benchmark thinking for CVRP instances, and later leading work such as Vidal’s HGS paper explicitly uses the classical Uchoa et al. 2017 instances as a comparison basis. Why it is important. Even if our project is not a benchmark paper, it should still imitate benchmark culture by making instances, assumptions, and outputs reproducible. How it helps our project. It supports the idea that our 26-node case should be documented with transparent matrices, demands, scenarios, and output tables. Gap. Uchoa et al. are benchmark-focused and do not solve our full TDHVRPTW specification directly. 

## Vidal:
What we learned. Vidal’s open-source HGS paper argues that many modern routing studies fail reproducibility because strong methods are hard to reimplement, then provides a simpler open-source HGS implementation for CVRP and shows that it remains highly competitive in solution quality, speed, and conceptual simplicity. Why it is important. This is directly relevant to the feedback because the repository must not rely on presentation claims alone. How it helps our project. It supports building the repository around transparent code, scenario data, and exportable outputs rather than vague algorithm descriptions. It also gives a credible modern heuristic benchmark that can be discussed even if you do not implement HGS yourself. Gap. The paper is specialized to CVRP, so it does not by itself solve the time-dependent and time-window-rich project variant. 

## Máximo, Cordeau, and Nascimento:
This paper studies the Heterogeneous Fleet Vehicle Routing Problem and proposes an adaptive iterated local search heuristic. In the reported experiments, the method outperformed prior metaheuristics on 87% of the instances tested. Why it is important. It is one of the strongest recent direct references for the “HF” part of TDHVRPTW. How it helps our project. It gives academic support for modeling fleet heterogeneity when vehicles have different capacities or cost structures. Even if our current computational version uses a restricted fleet, this paper helps explain why heterogeneous-fleet modeling is relevant in real distribution settings. Gap. It does not directly treat time-dependent travel times or the exact store-specific time-window structure of our case. 

## Ghannam and Gleixner:
This paper adapts Hybrid Genetic Search to the Dynamic Vehicle Routing Problem with Time Windows and reports significantly improved solution quality over the best-performing baseline in the EURO Meets NeurIPS Vehicle Routing Competition setting. Why it is important. It shows that once time and customer information become dynamic, routing methods must explicitly account for arrival timing and evolving information. How it helps our project. Our project is not fully dynamic, but it does use time-dependent travel conditions and scenario-based demand variation, so the paper is useful for discussing why static formulations can become unrealistic. Gap. The paper addresses online/dynamic arrival settings, which are richer than our current offline project implementation. 

## Accorsi and Vigo:
Accorsi and Vigo study extremely large-scale CVRP instances and show that very large routing problems can be solved in practical time with a carefully engineered heuristic. Why it is important. It is a good recent reference for scalability and for the difference between textbook models and high-performance routing implementations. How it helps our project. It supports the methodological point that practical routing studies often rely on heuristics because exact solution approaches become expensive as problem size and constraints grow. Gap. The scale of that study is far above our 26-node instance, so its main value is methodological rather than application-specific. 

## Kerscher and Minner:
 Kerscher and Minner propose a spatial-temporal-demand clustering framework for large-scale VRPTW and show that using similarity measures that account for space, timing, and demand improves over more naive cluster-first route-second approaches based only on spatial information. Why it is important. This is highly relevant because this project already combines location, time windows, and demand scenarios. How it helps our project. It justifies why our literature review must not discuss routing as “distance only.” It strengthens the argument that time windows and demand information should be present already in the data and scenario design. Gap. The paper emphasizes decomposition for large-scale settings and does not focus on a compact, student-scale OR-Tools implementation. 

## Peric, Begovic, and Lesic:
This real-world routing study is particularly close to our project's logic because it combines capacities, time windows, heterogeneous vehicles, soft time windows, multi-trip delivery, and time-dependent routes. The authors construct an initial solution with an extended Clarke–Wright procedure and report average savings of 2.03% in delivery time and 20.98% in total delivery costs compared with prior methods in their setting. Why it is important. It proves that Clarke–Wright is still relevant in modern rich-routing pipelines, but only as one component of a broader heuristic framework. How it helps our project. It is the best paper in this set for explaining why a TDHVRPTW literature section should connect time dependence, fleet structure, and practical heuristics instead of discussing them separately. Gap. Their case is richer than ours, so we should use it as conceptual support, not claim a direct one-to-one implementation match. 

## Serrano, Florio, Minner, Schiffer, and Vidal:
This paper studies a contextual stochastic VRPTW and develops data-driven prescriptive models based on historical information and uncertain travel times, with feature-dependent sample average approximation performing best in many settings. Why it is important. It represents a modern view of uncertainty in routing: not every practical time issue should be hidden inside a deterministic average matrix. How it helps our project. It gives a strong academic bridge between our demand scenarios and a broader literature on routing uncertainty. We can cite it when explaining why scenario analysis is a reasonable compromise when a full stochastic model is outside project scope. Gap. The paper uses richer stochastic modeling and advanced branch-price-and-cut methods that go beyond the complexity intended for our repository. 

## Wu et al.:
This 2024 survey on neural combinatorial optimization for VRPs finds that recent learning-based methods still face serious limitations, including poor generalization, difficulty with large-scale instances, limited ability to cover many variants, and difficulty in fair comparison with conventional OR algorithms. Why it is important. It prevents the literature review from becoming trend-driven or AI-shaped without methodological discipline. How it helps our project. It supports the decision to center the repository on classical OR methods, reproducible heuristics, and official solver documentation rather than trying to imitate fashionable ML papers. Gap. The survey focuses on neural solvers, which are outside the main computational scope of our project. 

## Mozhdehi, Wang, Sun, and Wang:
This paper studies a multi-trip time-dependent VRP with maximum working-hour constraints and proposes a deep reinforcement learning framework that outperforms current baselines on real-world datasets from two Canadian cities. Why it is important. It is a very recent source showing where time-dependent routing research is going when realistic work-hour and trip-structure constraints are combined. How it helps our project. Even if we do not implement this method, it helps justify including working-time and route-duration logic in our data and assumptions section. Gap. It is a learning-based approach for a richer multi-trip setting, so it should be cited as frontier literature, not as the direct computational method of our repository. 

## Computational implementation references
Google OR-Tools documentation
What we learned. The official OR-Tools VRPTW guide shows how to model a routing problem with a time matrix, explicit time windows, a fleet size, and a depot, and how to output timing information for the routes. The routing-options page documents search limits, first-solution strategies including SAVINGS and PATH_CHEAPEST_ARC, and local-search metaheuristics including GUIDED_LOCAL_SEARCH, which the documentation describes as generally the most efficient metaheuristic for vehicle routing. Why it is important. This is the most direct reproducibility source for our solver implementation. How it helps our project. It allows us to document solver choices precisely in the README and report. Gap. Documentation is not a research paper, so it should support the computational section rather than replace the literature review. 

## Final literature position
Based on the reviewed sources, our project is best positioned as a small but realistic TDHVRPTW case study: depot-based delivery, store time windows, scenario-based demand, and reproducible heuristic computation using OR-Tools, with Clarke–Wright used only as a historical or baseline comparison. The main research gap for our project is not inventing a new routing algorithm; it is demonstrating a coherent, transparent, and reproducible applied OR study that uses current literature correctly and does not over-claim more complexity than the code actually supports. Lastly, our older sources such as Dantzig and Ramser, Solomon, and Clarke and Wright are treated only as foundational references for the origin of VRP, VRPTW, and the savings heuristic, while the analytical focus of this review remains on recent literature.


## References 

Accorsi, L., & Vigo, D. (2023). Routing one million customers in a handful of minutes (arXiv:2306.14205). https://arxiv.org/abs/2306.14205

Baldacci, R., Battarra, M., & Vigo, D. (2008). Routing a heterogeneous fleet of vehicles. In B. Golden, S. Raghavan, & E. Wasil (Eds.), The Vehicle Routing Problem: Latest Advances and New Challenges (Operations Research/Computer Science Interfaces, Vol. 43, pp. 3–27). Springer. https://doi.org/10.1007/978-0-387-77778-8_1

Baldacci, R., Mingozzi, A., & Roberti, R. (2012). Recent exact algorithms for solving the vehicle routing problem under capacity and time window constraints. European Journal of Operational Research, 218(1), 1–6. https://doi.org/10.1016/j.ejor.2011.07.037

Bräysy, O., & Gendreau, M. (2005). Vehicle routing problem with time windows, Part I: Route construction and local search heuristics. Transportation Science, 39(1), 104–118. https://doi.org/10.1287/trsc.1030.0056

Cáceres-Cruz, J., Arias, P., Guimarans, D., Riera, D., & Juan, A. A. (2014). Rich vehicle routing problem: Survey. ACM Computing Surveys, 47(2), Article 32. https://doi.org/10.1145/2666003

Coelho, V. N., Grasas, A., Ramalhinho, H., Coelho, I. M., Souza, M. J. F., & Cruz, R. C. (2016). An ILS-based algorithm to solve a large-scale real heterogeneous fleet VRP with multi-trips and docking constraints. European Journal of Operational Research, 250(2), 367–376. https://doi.org/10.1016/j.ejor.2015.09.047

Feillet, D. (2010). A tutorial on column generation and branch-and-price for vehicle routing problems. 4OR: A Quarterly Journal of Operations Research, 8(4), 407–424. https://doi.org/10.1007/s10288-010-0130-z

Figliozzi, M. A. (2010). An iterative route construction and improvement algorithm for the vehicle routing problem with soft time windows. Transportation Research Part C: Emerging Technologies, 18(5), 668–679. https://doi.org/10.1016/j.trc.2009.08.005

Ghannam, M., & Gleixner, A. (2023). Hybrid genetic search for dynamic vehicle routing with time windows (arXiv:2307.11800). https://arxiv.org/abs/2307.11800

Goel, A. (2009). Vehicle scheduling and routing with drivers' working hours. Transportation Science, 43(1), 17–26. https://doi.org/10.1287/trsc.1070.0226

Holzapfel, A., Hübner, A., Kuhn, H., & Sternbeck, M. G. (2016). Delivery pattern and transportation planning in grocery retailing. European Journal of Operational Research, 252(1), 54–68. https://doi.org/10.1016/j.ejor.2015.12.036

Irnich, S., Toth, P., & Vigo, D. (2014). Formulation identifiers for vehicle routing problems. In P. Toth & D. Vigo (Eds.), Vehicle Routing: Problems, Methods, and Applications (2nd ed., pp. 1–35). Society for Industrial and Applied Mathematics. https://doi.org/10.1137/1.9781611973594.ch1

Kerscher, C., & Minner, S. (2024). Spatial-temporal-demand clustering for solving large-scale vehicle routing problems with time windows (arXiv:2402.00041). https://arxiv.org/abs/2402.00041

Koç, Ç., Bektaş, T., Jabali, O., & Laporte, G. (2016). Thirty years of heterogeneous vehicle routing. European Journal of Operational Research, 249(1), 1–21. https://doi.org/10.1016/j.ejor.2015.07.020

Máximo, V. R., Cordeau, J.-F., & Nascimento, M. C. V. (2021). An adaptive iterated local search heuristic for the heterogeneous fleet vehicle routing problem (arXiv:2111.12821). https://arxiv.org/abs/2111.12821

Mozhdehi, A., Wang, Y., Sun, S., & Wang, X. (2025). SED2AM: Solving multi-trip time-dependent vehicle routing problem using deep reinforcement learning (arXiv:2503.04085). https://arxiv.org/abs/2503.04085

Pecin, D., Pessoa, A., Poggi, M., & Uchoa, E. (2017). Improved branch-cut-and-price for capacitated vehicle routing. Mathematical Programming, 161(1), 425–460. https://doi.org/10.1007/s10107-016-1025-5

Peric, N., Begovic, S., & Lesic, V. (2024). Adaptive memory procedure for solving real-world vehicle routing problem (arXiv:2403.04420). https://arxiv.org/abs/2403.04420

Pessoa, A., Sadykov, R., & Uchoa, E. (2018). Enhanced branch-cut-and-price algorithm for heterogeneous fleet vehicle routing problems. European Journal of Operational Research, 270(2), 530–543. https://doi.org/10.1016/j.ejor.2018.04.009

Pisinger, D., & Ropke, S. (2007). A general heuristic for vehicle routing problems. Computers & Operations Research, 34(8), 2403–2435. https://doi.org/10.1016/j.cor.2005.09.012

Ropke, S., & Pisinger, D. (2006). An adaptive large neighborhood search heuristic for the pickup and delivery problem with time windows. Transportation Science, 40(4), 455–472. https://doi.org/10.1287/trsc.1050.0135

Serrano, B., Florio, A. M., Minner, S., Schiffer, M., & Vidal, T. (2024). Contextual stochastic vehicle routing with time windows (arXiv:2402.06968). https://arxiv.org/abs/2402.06968

Toth, P., & Vigo, D. (Eds.). (2014). Vehicle Routing: Problems, Methods, and Applications (2nd ed.). Society for Industrial and Applied Mathematics. https://doi.org/10.1137/1.9781611973594

Uchoa, E., Pecin, D., Pessoa, A., Poggi, M., Vidal, T., & Subramanian, A. (2017). New benchmark instances for the capacitated vehicle routing problem. European Journal of Operational Research, 257(3), 845–858. https://doi.org/10.1016/j.ejor.2016.08.012

Vidal, T. (2022). Hybrid genetic search for the CVRP: Open-source implementation and SWAP* neighborhood. Computers & Operations Research, 140, 105643.

Vidal, T., Crainic, T. G., Gendreau, M., Lahrichi, N., & Rei, W. (2013). A hybrid genetic algorithm for multi-depot and periodic vehicle routing problems. Operations Research, 61(3), 690–707. https://doi.org/10.1287/opre.1120.1148

Wu, X., Wang, D., Wen, L., Xiao, Y., Wu, C., Wu, Y., Yu, C., Maskell, D. L., & Zhou, Y. (2024). Neural combinatorial optimization algorithms for solving vehicle routing problems: A comprehensive survey with perspectives (arXiv:2406.00415). https://arxiv.org/abs/2406.00415
