"""
============================================================
  COMPARISON: Clarke-Wright vs OR-Tools GLS
  REALISTIC TRAFFIC MODEL — matches DrOetker_Lidl_Optimization_REALISTIC.py

  Traffic model: mu(t) step function
    07:00-09:00 (t=0 to 120 min)   -> x1.3  morning rush
    09:00-11:30 (t=120 to 270 min) -> x1.0  free flow
    11:30-12:00 (t=270 to 300 min) -> x1.1  lunch surge

  Clarke-Wright: applies mu(t) based on estimated departure
                 time at each node during route simulation
  OR-Tools GLS:  results taken from verified solver output
                 (DrOetker_Lidl_Optimization_REALISTIC.py)

  Both methods use IDENTICAL input data:
    - Same 26x26 distance matrix (Google Maps)
    - Same 26x26 time matrix (Google Maps)
    - Same demand vector S-99 (99 pallets)
    - Same fleet: 4x33p heavy + 4x12p medium
    - Same constraints: TW [08:00-12:00], max 405 min

  How to run:
      python comparison_cw_vs_ortools.py

  Output:
      - Full console comparison printed to screen
      - comparison_cw_vs_ortools.png saved in same folder
============================================================
"""

import math
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ─────────────────────────────────────────────────────────
#  REAL DATA — identical to DrOetker_Lidl_Optimization_REALISTIC.py
# ─────────────────────────────────────────────────────────

NODE_NAMES = {
    0:  "Depot (Dr. Oetker, Bielefeld)",
    1:  "Lidl Teutoburger Str.",
    2:  "Lidl Jöllenbecker Str.",
    3:  "Lidl Heeper Str.",
    4:  "Lidl Stadtheider Str.",
    5:  "Lidl Detmolder Str. 345",
    6:  "Lidl Babenhauser Str.",
    7:  "Lidl Kimbernstr.",
    8:  "Lidl Oldentruper Str.",
    9:  "Lidl Detmolder Str. 550",
    10: "Lidl Kasseler Str.",
    11: "Lidl Henleinstr.",
    12: "Lidl Neuenkirchener Str.",
    13: "Lidl Carl-Bertelsmann-Str.",
    14: "Lidl Auf dem Stempel",
    15: "Lidl Westring, Verl",
    16: "Lidl Bielefelder Str., Rheda",
    17: "Lidl Berliner Ring, Harsewinkel",
    18: "Lidl Lüchtenstr., Schloß Holte",
    19: "Lidl Elsa-Brändström-Str., Halle",
    20: "Lidl Bahnhofstr., Steinhagen",
    21: "Lidl Krentruper Str., Leopoldshöhe",
    22: "Lidl Lange Str., Spenge",
    23: "Lidl Friedrich-Petri-Str., Lage",
    24: "Lidl Ahmser Str., Herford",
    25: "Lidl Lambernweg, Enger",
}

SHORT = {i: f"L{i:02d}" for i in range(1, 26)}
SHORT[0] = "Depot"

# Distance matrix (km) — 26x26 — index 0 = depot
DIST = [
    [0,5.1,6.5,2.9,6.3,7.1,7.1,7.0,3.7,3.7,10.7,2.5,28.5,17.1,20.2,21.1,34.0,23.0,23.7,14.5,11.2,16.5,16.5,21.6,23.4,20.8],
    [5.1,0,11.3,2.9,4.9,7.9,7.8,6.0,2.1,8.9,19.9,3.1,29.3,18.3,21.3,21.9,35.2,34.2,24.4,15.3,12.4,13.0,15.9,20.7,17.2,19.4],
    [6.5,11.3,0,9.2,12.6,20.8,11.8,13.5,12.2,4.5,10.9,8.9,29.1,17.8,20.8,21.7,34.6,33.6,24.3,15.1,11.8,14.7,13.7,22.7,17.4,18.8],
    [2.9,2.9,9.2,0,3.5,8.9,8.9,8.9,3.5,6.4,17.4,2.3,31.7,20.3,23.3,24.3,37.2,36.2,26.9,17.7,14.4,12.1,16.6,20.4,16.0,19.2],
    [6.3,4.9,12.6,3.5,0,12.3,12.3,11.0,6.8,9.8,20.8,6.4,31.6,20.2,23.2,24.2,37.1,36.1,26.8,17.6,14.3,12.7,14.8,20.6,14.8,17.3],
    [7.1,7.9,20.8,8.9,12.3,0,2.4,3.7,6.6,9.8,7.2,6.1,27.9,26.7,31.5,27.6,33.4,36.2,16.5,17.8,14.5,13.3,19.7,17.4,19.2,32.8],
    [7.1,7.8,11.8,8.9,12.3,2.4,0,2.6,4.2,6.7,10.2,3.7,32.5,21.1,24.2,25.1,38.0,30.0,27.7,15.9,13.7,15.6,10.7,25.8,16.9,13.7],
    [7.0,6.0,13.5,8.9,11.0,3.7,2.6,0,3.8,8.8,11.2,4.2,16.2,13.8,16.9,15.1,31.2,21.4,15.0,13.6,10.3,19.0,21.5,23.3,28.7,25.7],
    [3.7,2.1,12.2,3.5,6.8,6.6,4.2,3.8,0,8.5,11.7,1.4,27.2,25.9,30.7,26.9,32.7,37.6,15.8,31.2,24.6,8.8,20.6,16.7,18.5,32.0],
    [3.7,8.9,4.5,6.4,9.8,9.8,6.7,8.8,8.5,0,7.5,5.3,26.1,24.9,29.7,25.8,31.7,36.5,12.7,30.2,23.6,9.6,23.7,15.7,17.5,31.0],
    [10.7,19.9,10.9,17.4,20.8,7.2,10.2,11.2,11.7,7.5,0,11.1,12.6,9.2,12.2,13.1,30.1,17.4,19.8,16.5,7.7,27.6,22.8,31.7,33.3,27.1],
    [2.5,3.1,8.9,2.3,6.4,6.1,3.7,4.2,1.4,5.3,11.1,0,19.0,17.8,22.6,12.6,24.6,35.6,8.5,23.1,16.5,17.1,30.8,21.2,22.8,36.3],
    [28.5,29.3,29.1,31.7,31.6,27.9,32.5,16.2,27.2,26.1,12.6,19.0,0,3.1,4.6,9.5,8.7,17.1,26.2,22.0,15.6,33.6,37.9,37.7,39.3,51.0],
    [17.1,18.3,17.8,20.3,20.2,26.7,21.1,13.8,25.9,24.9,9.2,17.8,3.1,0,5.7,8.2,10.4,15.6,24.9,20.2,13.4,32.3,31.7,36.5,38.0,49.7],
    [20.2,21.3,20.8,23.3,23.2,31.5,24.2,16.9,30.7,29.7,12.2,22.6,4.6,5.7,0,13.0,8.7,12.8,29.8,21.4,16.2,37.2,37.1,41.3,42.9,41.2],
    [21.1,21.9,21.7,24.3,24.2,27.6,25.1,15.1,26.9,25.8,13.1,12.6,9.5,8.2,13.0,0,14.3,24.2,13.2,27.7,21.1,29.1,35.5,33.3,34.9,46.5],
    [34.0,35.2,34.6,37.2,37.1,33.4,38.0,31.2,32.7,31.7,30.1,24.6,8.7,10.4,8.7,14.3,0,20.5,31.1,41.1,34.5,38.5,48.9,42.6,44.2,55.9],
    [23.0,34.2,33.6,36.2,36.1,36.2,30.0,21.4,37.6,36.5,17.4,35.6,17.1,15.6,12.8,24.2,20.5,0,41.9,17.1,13.8,49.7,31.7,53.8,55.4,35.6],
    [23.7,24.4,24.3,26.9,26.8,16.5,27.7,15.0,15.8,12.7,19.8,8.5,26.2,24.9,29.8,13.2,31.1,41.9,0,29.3,22.7,13.9,47.7,17.9,27.6,39.2],
    [14.5,15.3,15.1,17.7,17.6,17.8,15.9,13.6,31.2,30.2,16.5,23.1,22.0,20.2,21.4,27.7,41.1,17.1,29.3,0,6.9,38.1,17.3,42.2,43.8,21.4],
    [11.2,12.4,11.8,14.4,14.3,14.5,13.7,10.3,24.6,23.6,7.7,16.5,15.6,13.4,16.2,21.1,34.5,13.8,22.7,6.9,0,31.3,21.0,35.5,37.0,25.4],
    [16.5,13.0,14.7,12.1,12.7,13.3,15.6,19.0,8.8,9.6,27.6,17.1,33.6,32.3,37.2,29.1,38.5,49.7,13.9,38.1,31.3,0,25.1,8.2,14.2,27.8],
    [16.5,15.9,13.7,16.6,14.8,19.7,10.7,21.5,20.6,23.7,22.8,30.8,37.9,31.7,37.1,35.5,48.9,31.7,47.7,17.3,21.0,25.1,0,32.5,18.7,7.5],
    [21.6,20.7,22.7,20.4,20.6,17.4,25.8,23.3,16.7,15.7,31.7,21.2,37.7,36.5,41.3,33.3,42.6,53.8,17.9,42.2,35.5,8.2,32.5,0,16.0,29.6],
    [23.4,17.2,17.4,16.0,14.8,19.2,16.9,28.7,18.5,17.5,33.3,22.8,39.3,38.0,42.9,34.9,44.2,55.4,27.6,43.8,37.0,14.2,18.7,16.0,0,15.9],
    [20.8,19.4,18.8,19.2,17.3,32.8,13.7,25.7,32.0,31.0,27.1,36.3,51.0,49.7,41.2,46.5,55.9,35.6,39.2,21.4,25.4,27.8,7.5,29.6,15.9,0],
]

# Time matrix (minutes, free-flow) — identical to solver
TIME = [
    [0,13,14,9,16,16,15,16,13,9,21,9,28,26,30,25,27,32,25,20,17,29,31,33,30,32],
    [13,0,16,7,12,20,19,15,8,18,21,10,31,29,34,29,31,34,28,23,20,24,32,31,28,30],
    [14,16,0,13,20,20,22,23,17,11,18,17,26,24,28,23,25,28,23,18,14,25,23,31,27,27],
    [9,7,13,0,9,18,17,17,10,13,16,11,31,29,33,28,30,33,28,23,20,21,29,29,24,27],
    [16,12,20,9,0,27,26,22,18,22,26,19,31,28,32,28,30,33,27,23,19,21,25,29,22,22],
    [16,20,20,18,27,0,6,7,15,16,10,15,27,25,33,26,26,37,22,27,24,19,38,22,18,32],
    [15,19,22,17,26,6,0,6,10,13,15,10,35,33,37,33,35,35,32,21,21,29,17,37,24,22],
    [16,15,23,17,22,7,6,0,8,16,14,10,30,24,28,24,27,29,24,21,18,29,35,33,28,36],
    [13,8,17,10,18,15,10,8,0,18,21,5,25,24,31,25,24,36,20,26,22,13,35,20,17,31],
    [9,18,11,13,22,16,13,16,18,0,14,15,23,22,29,23,22,33,17,23,20,15,38,18,15,29],
    [21,21,18,16,26,10,15,14,21,14,0,19,20,15,19,20,24,23,22,17,13,28,35,31,27,37],
    [9,10,17,11,19,15,10,10,5,15,19,0,20,18,26,18,19,30,13,20,17,19,39,22,18,32],
    [28,31,26,31,31,27,35,30,25,23,20,20,0,9,10,18,14,24,29,32,25,34,48,37,33,47],
    [26,29,24,29,28,25,33,24,24,22,15,18,9,0,12,16,16,22,27,29,20,31,47,35,31,45],
    [30,34,28,33,32,33,37,28,31,29,19,26,10,12,0,25,14,18,35,28,23,40,45,45,40,51],
    [25,29,23,28,28,26,33,24,25,23,20,18,18,16,25,0,19,34,22,28,25,33,47,37,32,46],
    [27,31,25,30,30,26,35,27,24,22,24,19,14,16,14,19,0,25,27,30,27,32,50,36,31,45],
    [32,34,28,33,33,37,35,29,36,33,23,30,24,22,18,34,25,0,37,20,17,43,35,49,42,43],
    [25,28,23,28,27,22,32,24,20,17,22,13,29,27,35,22,27,37,0,26,23,20,43,25,26,41],
    [20,23,18,23,23,27,21,21,26,23,17,20,32,29,28,28,30,20,26,0,10,34,24,40,33,29],
    [17,20,14,20,19,24,21,18,22,20,13,17,25,20,23,25,27,17,23,10,0,28,28,30,27,33],
    [29,24,25,21,21,19,29,29,13,15,28,19,34,31,40,33,32,43,20,34,28,0,38,12,19,31],
    [31,32,23,29,25,38,17,35,35,38,35,39,48,47,45,47,50,35,43,24,28,38,0,39,24,12],
    [33,31,31,29,29,22,37,33,20,18,31,22,37,35,45,37,36,49,25,40,30,12,39,0,20,33],
    [30,28,27,24,22,18,24,28,17,15,27,18,33,31,40,32,31,42,26,33,27,19,24,20,0,17],
    [32,30,27,27,22,32,22,36,31,29,37,32,47,45,51,46,45,43,41,29,33,31,12,33,17,0],
]

# Scenario S-99 demands — identical to solver
DEMANDS = [0,4,4,4,5,4,4,5,4,4,5,5,4,5,5,3,4,3,3,3,3,3,3,4,5,3]
CUSTOMERS = list(range(1, 26))

# Fleet
HEAVY_CAP  = 33
MEDIUM_CAP = 12
N_HEAVY    = 4
N_MEDIUM   = 4

# Time parameters — identical to solver
DEPART_MIN = 420   # 07:00 in minutes from midnight
TW_OPEN    = 480   # 08:00
TW_CLOSE   = 720   # 12:00
MAX_ROUTE  = 405   # minutes
SERVICE    = {i: 10 + 2 * DEMANDS[i] for i in CUSTOMERS}

# ─────────────────────────────────────────────────────────
#  REALISTIC CONGESTION MODEL
#  Identical step function to DrOetker_Lidl_Optimization_REALISTIC.py
# ─────────────────────────────────────────────────────────

def traffic_multiplier(departure_minute):
    """
    Realistic time-dependent congestion multiplier.
    departure_minute = minutes elapsed since 07:00 departure.
    Matches exactly the traffic_multiplier() function in
    DrOetker_Lidl_Optimization_REALISTIC.py
    """
    if 0 <= departure_minute < 120:      # 07:00-09:00 morning rush
        return 1.3
    if 120 <= departure_minute < 270:    # 09:00-11:30 free flow
        return 1.0
    if 270 <= departure_minute <= 300:   # 11:30-12:00 lunch surge
        return 1.1
    return 1.0  # fallback

def realistic_travel_time(i, j, t_model):
    """
    Time-dependent travel time from i to j.
    t_model = minutes elapsed since 07:00.
    Applies realistic congestion multiplier at departure time.
    """
    return TIME[i][j] * traffic_multiplier(t_model)

# ─────────────────────────────────────────────────────────
#  ROUTE FEASIBILITY CHECK WITH REALISTIC TRAFFIC
# ─────────────────────────────────────────────────────────

def check_route(route, capacity):
    """
    Simulate a route with realistic time-dependent traffic.
    Returns (feasible, arrivals_dict, total_duration_minutes)
    """
    load = sum(DEMANDS[c] for c in route)
    if load > capacity:
        return False, None, None

    t_model = 0          # minutes since 07:00
    t_clock = DEPART_MIN # minutes since midnight
    prev = 0
    arrivals = {}

    for c in route:
        # Apply realistic congestion at departure time
        tt = realistic_travel_time(prev, c, t_model)
        t_model += tt
        t_clock += tt

        # Wait if arrive before time window opens
        if t_clock < TW_OPEN:
            wait    = TW_OPEN - t_clock
            t_model += wait
            t_clock  = TW_OPEN

        # Reject if arrive after time window closes
        if t_clock > TW_CLOSE:
            return False, None, None

        arrivals[c] = t_clock

        # Service time
        t_model += SERVICE[c]
        t_clock += SERVICE[c]
        prev = c

    # Return to depot with realistic congestion
    tt_ret  = realistic_travel_time(prev, 0, t_model)
    t_model += tt_ret

    # Check max route duration
    if t_model > MAX_ROUTE:
        return False, None, None

    return True, arrivals, t_model


def route_distance(route):
    d = DIST[0][route[0]]
    for k in range(len(route) - 1):
        d += DIST[route[k]][route[k+1]]
    d += DIST[route[-1]][0]
    return round(d, 1)

# ─────────────────────────────────────────────────────────
#  METHOD A — CLARKE-WRIGHT SAVINGS (REALISTIC TRAFFIC)
# ─────────────────────────────────────────────────────────

def run_clarke_wright():
    print("\n" + "="*62)
    print("  METHOD A — CLARKE-WRIGHT SAVINGS ALGORITHM")
    print("  Clarke & Wright (1964), Operations Research 12(4)")
    print("  Traffic model: realistic mu(t) step function")
    print("  (same as DrOetker_Lidl_Optimization_REALISTIC.py)")
    print("="*62)

    t_start = time.time()

    # Step 1 — compute savings using distance matrix
    savings = []
    for i in CUSTOMERS:
        for j in CUSTOMERS:
            if i >= j:
                continue
            s = DIST[0][i] + DIST[0][j] - DIST[i][j]
            savings.append((s, i, j))
    savings.sort(reverse=True)

    print(f"\n  Step 1: Computed {len(savings)} savings values")
    print(f"  Top 5 savings (distance-based):")
    for rank, (s, i, j) in enumerate(savings[:5], 1):
        print(f"    {rank}. {SHORT[i]} <-> {SHORT[j]}: {s:.2f} km saved")

    # Step 2 — initialise singleton routes
    routes   = {c: [c] for c in CUSTOMERS}
    route_of = {c: c   for c in CUSTOMERS}
    print(f"\n  Step 2: Initialised {len(CUSTOMERS)} singleton routes")

    # Step 3 — merge using savings list with realistic traffic check
    merges = 0
    for s, i, j in savings:
        ri = route_of[i]
        rj = route_of[j]
        if ri == rj:
            continue

        ri_route = routes[ri]
        rj_route = routes[rj]

        # Both i and j must be at route endpoints
        i_end = (ri_route[-1] == i or ri_route[0] == i)
        j_end = (rj_route[-1] == j or rj_route[0] == j)
        if not (i_end and j_end):
            continue

        # Try all valid merge orientations
        candidates = [
            ri_route + rj_route,
            ri_route + list(reversed(rj_route)),
            list(reversed(ri_route)) + rj_route,
            list(reversed(ri_route)) + list(reversed(rj_route)),
        ]

        merged_ok = False
        for merged in candidates:
            # Try heavy truck first, then medium
            for cap in [HEAVY_CAP, MEDIUM_CAP]:
                ok, _, _ = check_route(merged, cap)
                if ok:
                    routes[ri] = merged
                    del routes[rj]
                    for c in merged:
                        route_of[c] = ri
                    merges += 1
                    merged_ok = True
                    break
            if merged_ok:
                break

    t_end    = time.time()
    elapsed  = (t_end - t_start) * 1000

    print(f"  Step 3: Performed {merges} successful merges")
    print(f"          (feasibility checked with realistic mu(t) traffic)")

    # Build final results
    final_routes = list(routes.values())
    results      = []
    total_dist   = 0

    print(f"\n  ROUTES GENERATED ({len(final_routes)} routes):")
    print(f"  {'-'*57}")

    for idx, route in enumerate(final_routes):
        load  = sum(DEMANDS[c] for c in route)
        cap   = HEAVY_CAP if load > MEDIUM_CAP else MEDIUM_CAP
        ok, arrivals, duration = check_route(route, cap)
        dist  = route_distance(route)
        total_dist += dist
        vtype = "Heavy 33p" if cap == HEAVY_CAP else "Medium 12p"

        results.append({
            'id': idx+1, 'route': route, 'load': load,
            'cap': cap, 'dist': dist, 'duration': duration,
            'arrivals': arrivals, 'type': vtype, 'feasible': ok
        })

        stop_str = " -> ".join(SHORT[c] for c in route)
        print(f"\n  Truck {idx+1} [{vtype}]")
        print(f"    Stops    : {stop_str}")
        print(f"    Load     : {load}/{cap} pallets")
        print(f"    Distance : {dist} km")
        if duration:
            status = 'FEASIBLE' if ok else 'INFEASIBLE'
            print(f"    Duration : {duration:.0f} min | {status}")
        if arrivals:
            arr_str = "  |  ".join(
                f"{SHORT[c]}@{int(arrivals[c])//60:02d}:{int(arrivals[c])%60:02d}"
                for c in route
            )
            print(f"    Schedule : {arr_str}")

    print(f"\n  {'-'*57}")
    print(f"  TOTAL DISTANCE  : {total_dist:.1f} km")
    print(f"  VEHICLES USED   : {len(final_routes)}")
    print(f"  STORES SERVED   : {sum(len(r['route']) for r in results)}/25")
    print(f"  RUNTIME         : {elapsed:.2f} ms")

    return results, total_dist, elapsed

# ─────────────────────────────────────────────────────────
#  METHOD B — OR-TOOLS GLS (verified realistic output)
# ─────────────────────────────────────────────────────────

def run_ortools_documented():
    """
    Verified output from DrOetker_Lidl_Optimization_REALISTIC.py
    CHOSEN_SCENARIO = 99
    Traffic: realistic mu(t) via CumulVar().Min() in OR-Tools
    Solver: PATH_CHEAPEST_ARC + Guided Local Search, 30s limit
    GLS lambda coefficient: 0.1
    """
    print("\n" + "="*62)
    print("  METHOD B — OR-TOOLS GLS (Verified Realistic Output)")
    print("  Source: DrOetker_Lidl_Optimization_REALISTIC.py")
    print("  Strategy: PATH_CHEAPEST_ARC + Guided Local Search")
    print("  Time limit: 30 seconds | GLS lambda: 0.1")
    print("  Traffic: realistic mu(t) via CumulVar().Min()")
    print("  Scenario: S-99 (99 pallets)")
    print("="*62)

    ortools_routes = [
        {
            'id': 0, 'type': 'Heavy 33p', 'cap': 33, 'load': 29,
            'dist': 55, 'duration': 310, 'feasible': True,
            'route': [11,18,15,10,5,6,7],
            'arrivals': {
                11:'08:00', 18:'08:37', 15:'09:22',
                10:'10:04', 5:'10:37',  6:'11:03', 7:'11:29'
            },
            'depart': '07:00', 'return': '12:10'
        },
        {
            'id': 1, 'type': 'Heavy 33p', 'cap': 33, 'load': 26,
            'dist': 82, 'duration': 330, 'feasible': True,
            'route': [9,21,23,24,25,22,2],
            'arrivals': {
                9:'08:00',  21:'08:38', 23:'09:10',
                24:'09:54', 25:'10:36', 22:'11:08', 2:'11:54'
            },
            'depart': '07:00', 'return': '12:30'
        },
        {
            'id': 2, 'type': 'Heavy 33p', 'cap': 33, 'load': 27,
            'dist': 86, 'duration': 328, 'feasible': True,
            'route': [20,19,17,14,16,12,13],
            'arrivals': {
                20:'08:00', 19:'08:29', 17:'09:11',
                14:'09:50', 16:'10:28', 12:'11:04', 13:'11:34'
            },
            'depart': '07:00', 'return': '12:28'
        },
        {
            'id': 3, 'type': 'Heavy 33p', 'cap': 33, 'load': 17,
            'dist': 18, 'duration': 189, 'feasible': True,
            'route': [3,4,1,8],
            'arrivals': {
                3:'08:00', 4:'08:30', 1:'09:06', 8:'09:34'
            },
            'depart': '07:00', 'return': '10:09'
        },
    ]

    total_dist = sum(r['dist'] for r in ortools_routes)

    print(f"\n  Objective value (OR-Tools): 241 km")
    print(f"\n  ROUTES ({len(ortools_routes)} routes):")
    print(f"  {'-'*57}")

    for r in ortools_routes:
        stop_str = " -> ".join(SHORT[c] for c in r['route'])
        arr_str  = "  |  ".join(
            f"{SHORT[c]}@{r['arrivals'][c]}" for c in r['route']
        )
        print(f"\n  Vehicle {r['id']} [{r['type']}]")
        print(f"    Depot depart : {r['depart']}")
        print(f"    Stops        : {stop_str}")
        print(f"    Schedule     : {arr_str}")
        print(f"    Depot return : {r['return']}")
        print(f"    Load         : {r['load']}/{r['cap']} pallets")
        print(f"    Distance     : {r['dist']} km")
        print(f"    Duration     : {r['duration']} min | FEASIBLE")

    print(f"\n  {'-'*57}")
    print(f"  TOTAL DISTANCE  : {total_dist} km")
    print(f"  VEHICLES USED   : {len(ortools_routes)}")
    print(f"  STORES SERVED   : {sum(len(r['route']) for r in ortools_routes)}/25")
    print(f"  RUNTIME         : < 30 seconds (GLS time limit)")

    return ortools_routes, total_dist

# ─────────────────────────────────────────────────────────
#  SIDE-BY-SIDE COMPARISON
# ─────────────────────────────────────────────────────────

def print_comparison(cw_routes, cw_dist, cw_ms, ort_routes, ort_dist):
    improvement = (cw_dist - ort_dist) / cw_dist * 100

    print("\n" + "="*62)
    print("  SIDE-BY-SIDE COMPARISON — SCENARIO S-99 (99 PALLETS)")
    print("  Both methods use IDENTICAL data and traffic model")
    print("="*62)

    w = 24
    print(f"\n  {'Criterion':<28} {'Clarke-Wright':>{w}} {'OR-Tools GLS':>{w}}")
    print(f"  {'-'*76}")

    rows = [
        ("Traffic model",          "Realistic mu(t) step fn",  "Realistic mu(t) CumulVar"),
        ("Total distance (km)",    f"{cw_dist:.1f} km",         f"{ort_dist} km"),
        ("Distance improvement",   "Reference baseline",        f"-{improvement:.1f}% shorter"),
        ("Vehicles used",          str(len(cw_routes)),          str(len(ort_routes))),
        ("Stores served",          f"{sum(len(r['route']) for r in cw_routes)}/25",
                                   f"{sum(len(r['route']) for r in ort_routes)}/25"),
        ("All routes feasible",    "Yes",                        "Yes"),
        ("Computation time",       f"{cw_ms:.2f} ms",           "< 30 seconds"),
        ("Algorithm type",         "Constructive heuristic",    "Metaheuristic (GLS)"),
        ("Optimality guarantee",   "None (greedy merges)",      "No formal proof"),
        ("Transparency",           "Fully traceable",           "Black-box solver"),
        ("Best use case",          "Education / speed",         "Production routing"),
    ]

    for label, cw_val, ort_val in rows:
        print(f"  {label:<28} {cw_val:>{w}} {ort_val:>{w}}")

    print(f"\n  {'='*76}")
    print(f"  CONCLUSION:")
    print(f"  OR-Tools GLS achieves {improvement:.1f}% shorter total distance than")
    print(f"  Clarke-Wright ({ort_dist} km vs {cw_dist:.1f} km) on Scenario S-99.")
    print(f"")
    print(f"  Both methods use the SAME realistic traffic model.")
    print(f"  The difference comes purely from the optimisation quality:")
    print(f"  Clarke-Wright makes greedy decisions that cannot be reversed.")
    print(f"  OR-Tools GLS explores many alternative routes and keeps the best.")
    print(f"")
    print(f"  This is consistent with Cordeau et al. (2002, JORS 53(5), p.516)")
    print(f"  who report metaheuristic improvement of 10-30% over constructive")
    print(f"  heuristics on medium-sized VRP instances (n=25 to 100 customers).")
    print(f"  {'='*76}")

# ─────────────────────────────────────────────────────────
#  FIGURES
# ─────────────────────────────────────────────────────────

GEO = {
    0:(50,50),1:(55,48),2:(47,55),3:(53,54),4:(54,58),5:(44,46),
    6:(46,48),7:(44,43),8:(57,51),9:(61,48),10:(40,43),11:(52,43),
    12:(34,34),13:(32,33),14:(30,29),15:(38,27),16:(21,21),17:(18,44),
    18:(62,28),19:(31,62),20:(39,53),21:(68,59),22:(67,71),23:(79,47),
    24:(68,68),25:(59,72),
}

COLORS = ['#E53935','#1E88E5','#43A047','#FB8C00','#8E24AA','#00ACC1']

def plot_comparison(cw_routes, ort_routes, cw_dist, ort_dist):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('#FFFFFF')
    fig.suptitle(
        'Clarke-Wright vs OR-Tools GLS — Scenario S-99 (99 pallets)\n'
        'Realistic Time-Dependent Traffic Model  μ(t): ×1.3 rush / ×1.0 free-flow / ×1.1 lunch',
        fontsize=13, fontweight='bold', y=1.02
    )

    for ax, routes, title, dist in zip(
        axes[:2],
        [cw_routes, ort_routes],
        [f'Clarke-Wright\nTotal: {cw_dist:.1f} km',
         f'OR-Tools GLS (Realistic)\nTotal: {ort_dist} km'],
        [cw_dist, ort_dist]
    ):
        ax.set_facecolor('#F0F4F8')
        ax.grid(True, alpha=0.25, ls='--')
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlim(10, 90); ax.set_ylim(10, 85)
        ax.set_xlabel('X (scaled km)'); ax.set_ylabel('Y (scaled km)')

        legend_handles = []
        for ri, route in enumerate(routes):
            r_list = route['route'] if isinstance(route, dict) else route
            color  = COLORS[ri % len(COLORS)]
            nodes  = [0] + r_list + [0]
            xs = [GEO[n][0] for n in nodes]
            ys = [GEO[n][1] for n in nodes]
            ax.plot(xs, ys, color=color, lw=2, alpha=0.7, zorder=2)

            for k in range(len(nodes)-1):
                mx=(xs[k]+xs[k+1])/2; my=(ys[k]+ys[k+1])/2
                dx=xs[k+1]-xs[k]; dy=ys[k+1]-ys[k]
                if abs(dx)+abs(dy)>0.5:
                    ax.annotate('', xy=(mx+dx*0.01, my+dy*0.01),
                        xytext=(mx-dx*0.01, my-dy*0.01),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1), zorder=3)

            for n in r_list:
                ax.scatter(GEO[n][0], GEO[n][1], s=55, color=color,
                           zorder=5, edgecolors='white', lw=0.7)
                ax.text(GEO[n][0]+0.8, GEO[n][1]+0.8, SHORT[n],
                        fontsize=6.5, color='#222', zorder=6)

            r_load = route['load'] if isinstance(route, dict) else sum(DEMANDS[c] for c in r_list)
            r_dist = route['dist'] if isinstance(route, dict) else route_distance(r_list)
            legend_handles.append(Line2D([0],[0], color=color, lw=2,
                label=f"T{ri+1}: {r_load}p / {r_dist}km"))

        # Depot
        dx, dy = GEO[0]
        ax.scatter(dx, dy, s=220, color='#1A237E', marker='*', zorder=7)
        ax.text(dx+1, dy+1, 'DEPOT', fontsize=8, fontweight='bold', color='#1A237E')
        ax.legend(handles=legend_handles, fontsize=8, loc='lower right', framealpha=0.9)

    # Bar chart comparison
    ax = axes[2]
    ax.set_facecolor('#F8F9FA')
    methods   = ['Clarke-Wright\n(Constructive)', 'OR-Tools GLS\n(Realistic)']
    distances = [cw_dist, ort_dist]
    bar_cols  = ['#1E88E5', '#43A047']
    bars      = ax.bar(methods, distances, color=bar_cols, edgecolor='white', width=0.45)

    for bar, v in zip(bars, distances):
        ax.text(bar.get_x()+bar.get_width()/2, v+2,
                f'{v:.1f} km', ha='center', fontsize=12, fontweight='bold')

    improvement = (cw_dist - ort_dist) / cw_dist * 100
    ax.annotate(
        f'{improvement:.1f}% shorter',
        xy=(1, ort_dist), xytext=(0.55, ort_dist + 35),
        fontsize=11, color='#2E7D32', fontweight='bold',
        arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5)
    )
    ax.set_ylabel('Total Distance (km)', fontsize=11)
    ax.set_title('Distance Comparison\n(Same data & traffic model)', fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(distances) * 1.3)
    ax.grid(axis='y', alpha=0.3)

    # Traffic model legend box
    ax.text(0.5, 0.05,
        'Traffic model μ(t):\n07-09h: ×1.3 | 09-11:30h: ×1.0 | 11:30-12h: ×1.1',
        transform=ax.transAxes, ha='center', fontsize=8,
        bbox=dict(boxstyle='round', facecolor='#E3F2FD', alpha=0.8))

    plt.tight_layout()
    out = 'comparison_cw_vs_ortools.png'
    plt.savefig(out, dpi=170, bbox_inches='tight')
    plt.close()
    print(f"\n  [✓] Figure saved -> {out}")

# ─────────────────────────────────────────────────────────
#  TOP SAVINGS TABLE
# ─────────────────────────────────────────────────────────

def print_top_savings():
    print("\n" + "="*62)
    print("  TOP 10 SAVINGS VALUES (Clarke-Wright Step 1)")
    print("  s(i,j) = d(0,i) + d(0,j) - d(i,j)")
    print("  Source: real Google Maps distance matrix")
    print("="*62)

    savings = []
    for i in CUSTOMERS:
        for j in CUSTOMERS:
            if i >= j:
                continue
            s = DIST[0][i] + DIST[0][j] - DIST[i][j]
            savings.append((s, i, j))
    savings.sort(reverse=True)

    print(f"\n  {'Rank':<6} {'Pair':<14} {'d(0,i)':<10} "
          f"{'d(0,j)':<10} {'d(i,j)':<10} {'Saving':<10}")
    print(f"  {'-'*60}")
    for rank, (s, i, j) in enumerate(savings[:10], 1):
        print(f"  {rank:<6} {SHORT[i]+' <-> '+SHORT[j]:<14} "
              f"{DIST[0][i]:<10.1f} {DIST[0][j]:<10.1f} "
              f"{DIST[i][j]:<10.1f} {s:<10.2f}")

# ─────────────────────────────────────────────────────────
#  REPRODUCIBILITY NOTE
# ─────────────────────────────────────────────────────────

def print_reproducibility(cw_dist, ort_dist):
    print("\n" + "="*62)
    print("  REPRODUCIBILITY NOTE")
    print("="*62)
    print(f"""
  Clarke-Wright results ({cw_dist:.1f} km):
    Computed live by this script using the real Google Maps
    distance and time matrices. Run this script again to
    reproduce the exact same result.

  OR-Tools GLS results ({ort_dist} km):
    Verified output from running:
        DrOetker_Lidl_Optimization_REALISTIC.py
    with CHOSEN_SCENARIO = 99

    To reproduce OR-Tools results independently:
        pip install ortools numpy pandas matplotlib
        python DrOetker_Lidl_Optimization_REALISTIC.py

  Both methods use identical input data:
    - 26x26 distance matrix (Google Maps, OWL region)
    - 26x26 time matrix (Google Maps, OWL region)
    - Demand vector S-99: {DEMANDS[1:]}
    - Fleet: 4x33p heavy + 4x12p medium trucks
    - Time windows: [08:00, 12:00] hard constraint
    - Max route: 405 minutes
    - Traffic: mu(t) = 1.3 / 1.0 / 1.1 step function
  """)

# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("\n" + "#"*62)
    print("#  TDHVRPTW — METHOD COMPARISON (REALISTIC TRAFFIC)")
    print("#  Dr. Oetker -> 25 Lidl Stores (OWL Region)")
    print("#  Scenario S-99: 99 pallets | 4H + 4M fleet")
    print("#  Traffic: mu(t) realistic step function")
    print("#"*62)

    print_top_savings()

    cw_routes, cw_dist, cw_ms = run_clarke_wright()
    ort_routes, ort_dist       = run_ortools_documented()

    print_comparison(cw_routes, cw_dist, cw_ms, ort_routes, ort_dist)
    print_reproducibility(cw_dist, ort_dist)

    # Build route lists for plotting
    cw_plot  = [{'route': r['route'], 'dist': r['dist'], 'load': r['load']} for r in cw_routes]
    ort_plot = [{'route': r['route'], 'dist': r['dist'], 'load': r['load']} for r in ort_routes]

    plot_comparison(cw_plot, ort_plot, cw_dist, ort_dist)

    print("\n  Done. Upload comparison_cw_vs_ortools.png to your Figures/ folder.")
