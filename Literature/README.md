

## Team

| Full name     | GitHub username |
|---|---|
| [Full Name 1] | [@github-emmanuelezenwata-1] |
| [Full Name 2] | [@github-Abde03-2] |
| [Full Name 3] | [@github-jmwema1990-3] |
| [Full Name 4] | [@github-MarkoG0205-4] |
| [Full Name 5] | [@github-barbaracalderonavila-collab-5] |
> Use full legal/academic names only. Do not use nicknames.

## Project title

Time-Dependent Heterogeneous Fleet Vehicle Routing Problem with Time Windows for Lidl Store Deliveries

## Final project scope

This repository contains the full material for our Operations Research project on a **TDHVRPTW** case with **25 Lidl stores plus 1 depot (26 nodes total)**.

The project combines:
- delivery routing from one depot to multiple Lidl stores
- store-specific demand assumptions
- delivery time windows
- time-dependent travel times / congestion effects
- scenario-based analysis
- reproducible computational results

## Repository contents

- `data/`
  - coordinates
  - distance matrix
  - travel-time matrix
  - demand scenarios
  - time-window data
- `src/`
  - data preparation scripts
  - solver scripts
  - output generation scripts
- `outputs/`
  - route outputs by scenario
  - summary tables
  - solver logs
- `literature/`
  - `literature_review.md`
  - `sources.bib`
  - source notes
- `reports/`
  - final project report
  - updated OR project file
- `figures/`
  - route plots, charts, and report figures

## Reproducibility

### Software

- Python version: to be documented after the solver scripts are uploaded
- Main packages: `[insert packages]`
- Solver/library: Google OR-Tools Routing Solver
- Operating system used for final tests: `[insert OS]`

### Installation

```bash
git clone [repository-url]
cd [repository-folder]
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
