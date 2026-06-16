# Model Simplifications

The real Dr. Oetker and Lidl logistics system is more complex than our model. We simplify the real problem in order to create a solvable Operations Research model.

## Main Simplifications

- Store-level demand is estimated because real internal delivery data is not public.
- All products are converted into homogeneous Euro pallet units.
- Each customer must be visited exactly once.
- Split deliveries are not allowed.
- Traffic is represented by simplified time-dependent multipliers.
- Vehicle loading order and detailed warehouse processes are not modeled.
- The model focuses on one planning day, not a full weekly delivery schedule.
- All pallets are treated as equal loading units.
- Service time is estimated with a linear formula.

## Why These Simplifications Are Acceptable

The goal of the project is not to reproduce the complete Lidl supply chain. The goal is to build a transparent routing model that can compare routes, vehicle use, time feasibility, and operational cost.

The simplifications allow us to focus on the core Operations Research structure:

- decision variables
- objective function
- capacity constraints
- time-window constraints
- route feasibility
- solver and heuristic comparison

## Possible Impact

The results should be interpreted as decision-support results, not as exact operational schedules. If real internal demand data, real historical traffic data, and vehicle-specific restrictions became available, the model could be updated and re-optimized.
