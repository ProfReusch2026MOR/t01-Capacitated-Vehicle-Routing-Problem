# T01 Capacitated Vehicle Routing Problem

## Project Overview

This repository contains the Operations Research group project for Team 01.  
The project analyzes a capacitated vehicle routing problem for deliveries from the Dr. Oetker depot in Bielefeld to Lidl stores in the OWL region.

The goal is to structure the delivery problem, collect and prepare input data, formulate a mathematical routing model, and later solve or evaluate possible delivery routes.

## Decision Question

Which delivery routes should the available vehicles use to serve all Lidl stores while minimizing transportation effort and respecting operational constraints such as vehicle capacity, service times, delivery time windows, traffic buffers, and maximum route duration?

## Current Repository Structure

- `DATA/` contains collected and prepared data files, including distance and time matrices.
- `Math formulation report/` contains the mathematical model formulation.
- `Final report/` contains material for the final written project report.
- `docs/` contains project explanations, assumptions, and short documentation files.
- `notebooks/` contains Jupyter notebooks for data exploration, model testing, and result analysis.
- `src/` contains Python scripts for data preparation, solving, or visualization.
- `results/` contains solver outputs, route summaries, and figures.
- `presentation/` contains presentation material.
- `literature/` contains sources and literature notes.
- `project_management/` contains contribution logs, task overview, and meeting notes.

## Current Progress

- Initial data folder created.
- Distance matrix and time matrix added.
- Demand estimation research added.
- Mathematical formulation report added.
- Repository structure is being cleaned and extended.

## Main Model Components

The project uses typical Operations Research elements:

- decision variables for vehicle movements between locations
- customer demand measured in pallets
- vehicle capacity restrictions
- service times at stores
- delivery time windows
- maximum route duration
- distance or time based objective function

## Team Workflow

The repository is used as the central workspace for:

- storing project files
- documenting assumptions
- tracking individual contributions
- organizing tasks through GitHub Issues
- reviewing work through commits and pull requests