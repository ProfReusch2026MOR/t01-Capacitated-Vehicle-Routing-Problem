# Kerscher and Minner (2024) — Spatial-Temporal-Demand Clustering for VRPTW

## Full reference

Kerscher, C., & Minner, S. (2024). *Spatial-temporal-demand clustering for solving large-scale vehicle routing problems with time windows.*


Kerscher and Minner are useful for our project because they look at routing from more than just a distance perspective. Their paper argues that when customers are grouped only by location, important information can be lost. Two stores may be close to each other, but if their time windows or demand levels do not fit well together, putting them on the same route can still be a bad decision.

This connects well to our project. Our case does not only involve store locations. We also have pallet demand, delivery time windows, and different demand scenarios. So the paper gives us a good reason to avoid describing the problem as if it were only about finding the shortest path between Lidl stores.

The main lesson is that routing data should be treated as a combination of spatial, temporal, and demand-related information. In our case, this means the coordinates, travel-time matrix, time-window assumptions, and pallet demand scenarios all matter together. A route that looks efficient by distance may still fail once unloading time or store timing is included.

For the repository, this source supports the way we document our data. It helps justify why we should show not only store coordinates, but also demand values, scenario assumptions, and timing constraints. That makes the model easier to understand and more defensible.

The limitation is that the paper is aimed at large-scale routing and decomposition methods. Our case is much smaller, with 25 stores and one depot. We are not implementing their clustering framework directly. Instead, we use the paper to support the idea that time and demand should already be considered during data preparation and interpretation, not only after the solver produces routes.
