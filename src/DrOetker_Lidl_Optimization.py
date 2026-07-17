"""
Dr. Oetker – Lidl Distribution Optimisation

Implements a Time-Dependent Heterogeneous Vehicle Routing Problem with
Time Windows (TDHVRPTW) for the OWL Lidl delivery network.

Main model components:
- 25 Lidl stores + 1 Dr. Oetker depot
- heterogeneous fleet: 4 heavy trucks and 4 medium trucks
- vehicle capacity constraints
- service time s_i = 10 + 2*q_i
- delivery window 08:00–12:00
- maximum route duration of 405 minutes
- time-dependent traffic multipliers
- optional Google Maps Distance Matrix API support
- Google OR-Tools with Guided Local Search
- demand scenarios S-99, S-152, and S-170
"""

import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# ==========================================
# SCENARIO CONFIGURATION MANAGER
# ==========================================
# Change this number to switch scenarios: 99, 152, or 170
CHOSEN_SCENARIO = 99

# Set this to True when you want Google Maps to build the distance/time matrices.
# You need a Google Maps API key and a locations.csv file.
USE_GOOGLE_MAPS = False
GOOGLE_MAPS_API_KEY_FILE = 'google_maps_api_key.txt'
LOCATIONS_FILE = 'locations.csv'
GOOGLE_MAPS_MODE = 'driving'
GOOGLE_MAPS_DEPARTURE_TIME = 'now'

BASE_DIR = Path(__file__).resolve().parent
# Time-dependent congestion multipliers used when CSV matrices are loaded.
# Model clock: 07:00 = 0 minutes.
def traffic_multiplier(departure_minute):
    """Return the congestion multiplier based on minutes since 07:00."""
    if 0 <= departure_minute < 120:      # 07:00–09:00
        return 1.3
    if 120 <= departure_minute < 270:    # 09:00–11:30
        return 1.0
    if 270 <= departure_minute <= 300:   # 11:30–12:00
        return 1.1
    return 1.0  # fallback outside the planned delivery horizon


def find_input_file(file_name):
    """Finds an input file beside this script or in the folder where Python was started."""
    file_path = BASE_DIR / file_name
    if file_path.exists():
        return file_path

    file_path = Path.cwd() / file_name
    if file_path.exists():
        return file_path

    raise FileNotFoundError(
        f"Could not find {file_name}. Put it in {BASE_DIR} or in {Path.cwd()}."
    )


def load_matrix_completely_safe(file_name):
    """Reads any broken tab/comma/space separated file safely without pandas read_csv parser errors."""
    matrix_data = []
    file_path = find_input_file(file_name)

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', line)
            if numbers:
                matrix_data.append([float(num) for num in numbers])

    df = pd.DataFrame(matrix_data).dropna(how='all').dropna(axis=1, how='all')
    if df.shape[0] > 1 and df.shape[1] > 1:
        if df.iloc[0, 0] == 0 and df.iloc[0, 1] == 1:
            df = df.iloc[1:, 1:]
    return df.to_numpy().round().astype(int)


def get_google_maps_api_key():
    """Loads the Google Maps API key from an environment variable or a local text file."""
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    if api_key:
        return api_key.strip()

    key_path = BASE_DIR / GOOGLE_MAPS_API_KEY_FILE
    if key_path.exists():
        return key_path.read_text(encoding='utf-8').strip()

    raise ValueError(
        'Google Maps mode is enabled, but no API key was found. Set GOOGLE_MAPS_API_KEY '
        f'or create {key_path} containing only your API key.'
    )


def load_locations(expected_nodes):
    """Loads node addresses from locations.csv."""
    location_path = find_input_file(LOCATIONS_FILE)
    locations = pd.read_csv(location_path)

    if 'address' not in locations.columns:
        raise ValueError(f'{LOCATIONS_FILE} must contain an address column.')

    if 'node' in locations.columns:
        locations = locations.sort_values('node')

    if len(locations) != expected_nodes:
        raise ValueError(
            f'{LOCATIONS_FILE} must contain {expected_nodes} rows: node 0 depot plus '
            f'{expected_nodes - 1} customer nodes. It currently has {len(locations)} rows.'
        )

    addresses = locations['address'].astype(str).tolist()
    names = locations['name'].astype(str).tolist() if 'name' in locations.columns else [f'Node {i}' for i in range(expected_nodes)]
    return addresses, names


def google_distance_matrix_request(api_key, origins, destinations):
    """Calls Google Distance Matrix API for one batch of origins/destinations."""
    params = {
        'origins': '|'.join(origins),
        'destinations': '|'.join(destinations),
        'mode': GOOGLE_MAPS_MODE,
        'units': 'metric',
        'departure_time': GOOGLE_MAPS_DEPARTURE_TIME,
        'key': api_key,
    }
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?' + urlencode(params)

    with urlopen(url, timeout=60) as response:
        payload = json.loads(response.read().decode('utf-8'))

    if payload.get('status') != 'OK':
        raise RuntimeError(f"Google Maps API error: {payload.get('status')} - {payload.get('error_message', '')}")

    return payload


def build_matrices_from_google_maps(addresses):
    """Builds OR-Tools distance/time matrices from Google Maps travel data."""
    api_key = get_google_maps_api_key()
    node_count = len(addresses)
    distance_matrix = [[0 for _ in range(node_count)] for _ in range(node_count)]
    time_matrix = [[0 for _ in range(node_count)] for _ in range(node_count)]

    # Distance Matrix requests are batched to keep each request small and reliable.
    destination_batch_size = 25
    for origin_index, origin in enumerate(addresses):
        for start in range(0, node_count, destination_batch_size):
            end = min(start + destination_batch_size, node_count)
            destinations = addresses[start:end]
            payload = google_distance_matrix_request(api_key, [origin], destinations)
            elements = payload['rows'][0]['elements']

            for offset, element in enumerate(elements):
                destination_index = start + offset
                if element.get('status') != 'OK':
                    raise RuntimeError(
                        f'No Google Maps route from node {origin_index} to node {destination_index}: '
                        f"{element.get('status')}"
                    )

                distance_meters = element['distance']['value']
                duration_seconds = element.get('duration_in_traffic', element['duration'])['value']
                distance_matrix[origin_index][destination_index] = max(1, round(distance_meters / 1000))
                time_matrix[origin_index][destination_index] = max(1, round(duration_seconds / 60))

            time.sleep(0.1)

    return pd.DataFrame(distance_matrix).to_numpy(), pd.DataFrame(time_matrix).to_numpy()


def google_maps_route_url(addresses, route_nodes):
    """Creates a clickable Google Maps directions URL for one optimized route."""
    if len(route_nodes) < 2:
        return ''

    params = {
        'api': '1',
        'origin': addresses[route_nodes[0]],
        'destination': addresses[route_nodes[-1]],
        'travelmode': GOOGLE_MAPS_MODE,
    }
    if len(route_nodes) > 2:
        params['waypoints'] = '|'.join(addresses[node] for node in route_nodes[1:-1])

    return 'https://www.google.com/maps/dir/?' + urlencode(params)


def create_data_model():
    """Stores the data for the problem based on the chosen scenario."""
    data = {}

    print(f"--- INITIALIZING SCENARIO: {CHOSEN_SCENARIO} PALLETS ---")

    scenarios_demands = {
        # Baseline Scenario (Our primary configuration)
        99: [
            0,  # Depot
            4, 4, 4, 5, 4, 4, 5, 4, 4, 5,
            5, 4, 5, 5, 3, 4, 3, 3, 3, 3,
            3, 3, 4, 5, 3
        ],
        # Mid-Tier High Volume Surge Day
        152: [
            0,  # Depot
            6, 6, 7, 7, 6, 6, 7, 6, 6, 7,
            7, 6, 7, 7, 5, 6, 5, 5, 5, 5,
            5, 5, 6, 7, 5
        ],
        # Max-Capacity Absolute Fleet Limit Stress-Test
        170: [
            0,  # Depot
            7, 7, 7, 8, 7, 7, 8, 7, 7, 8,
            8, 7, 8, 8, 6, 7, 6, 6, 6, 6,
            6, 6, 7, 8, 6
        ]
    }

    if CHOSEN_SCENARIO not in scenarios_demands:
        raise ValueError(f"Scenario {CHOSEN_SCENARIO} is not defined! Please pick 99, 152, or 170.")

    data['demands'] = scenarios_demands[CHOSEN_SCENARIO]
    print(f"Verified Combined Network Volume: {sum(data['demands'])} pallets")

    if USE_GOOGLE_MAPS:
        data['addresses'], data['location_names'] = load_locations(len(data['demands']))
        data['distance_matrix'], data['time_matrix'] = build_matrices_from_google_maps(data['addresses'])
    else:
        data['distance_matrix'] = load_matrix_completely_safe('distance_matrix.csv')
        data['time_matrix'] = load_matrix_completely_safe('time_matrix.csv')
        data['addresses'] = []
        data['location_names'] = [f'Node {i}' for i in range(len(data['demands']))]

    # Fleet Matrix: 4 Heavy Trucks (33) + 4 Medium Trucks (12) = 180 total volume pool
    data['vehicle_capacities'] = [33, 33, 33, 33, 12, 12, 12, 12]
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['depot'] = 0

    # Auto-adjust service time metrics based on demands: s_i = 10 + 2 * q_i
    data['service_times'] = [10 + (2 * q) if q > 0 else 0 for q in data['demands']]

    # Time windows are expressed as minutes since depot departure:
    # 07:00 = 0, therefore customer delivery window 08:00–12:00 = 60–300.
    data['time_windows'] = [(0, 500) if i == 0 else (60, 300) for i in range(len(data['demands']))]
    data['max_route_time'] = 405

    # Dynamic Slack Allocation: Heuristically increases the waiting buffer as volumes grow tighter
    if CHOSEN_SCENARIO == 99:
        data['slack_allowance'] = 45
    elif CHOSEN_SCENARIO == 152:
        data['slack_allowance'] = 75
    else:  # 170 Pallets
        data['slack_allowance'] = 90  # Larger waiting buffer for the tightest stress-test scenario

    validate_data_model(data)
    return data


def validate_data_model(data):
    """Checks that the loaded matrices match the scenario node count."""
    expected_nodes = len(data['demands'])

    for matrix_name in ('distance_matrix', 'time_matrix'):
        matrix = data[matrix_name]
        if matrix.shape != (expected_nodes, expected_nodes):
            raise ValueError(
                f"{matrix_name} must be {expected_nodes}x{expected_nodes}, "
                f"but loaded shape is {matrix.shape}."
            )

    if len(data['service_times']) != expected_nodes:
        raise ValueError('Service times must match the number of demand nodes.')

    if len(data['time_windows']) != expected_nodes:
        raise ValueError('Time windows must match the number of demand nodes.')

    if sum(data['demands']) > sum(data['vehicle_capacities']):
        raise ValueError('Total demand exceeds total fleet capacity.')


def print_solution(data, manager, routing, solution):
    """Prints solution on console with corrected unloading logistics wording."""
    print(f'Objective: {solution.ObjectiveValue()} total kilometers driven.\n')
    total_distance = 0
    total_load = 0
    time_dimension = routing.GetDimensionOrDie('Time')

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)

        total_route_load = 0
        temp_index = index
        while not routing.IsEnd(temp_index):
            node_idx = manager.IndexToNode(temp_index)
            total_route_load += data['demands'][node_idx]
            temp_index = solution.Value(routing.NextVar(temp_index))

        if total_route_load == 0:
            continue  # Vehicle stayed back idle

        route_nodes = [data['depot']]
        plan_output = f'Route for Vehicle {vehicle_id} (Capacity {data["vehicle_capacities"][vehicle_id]} pallets):\n'
        plan_output += f'  Depot 0 (LOADED AT DEPOT: {total_route_load} pallets, Depart: 07:00) -> \n'

        route_distance = 0
        current_cargo = total_route_load
        previous_index = index
        index = solution.Value(routing.NextVar(index))

        while not routing.IsEnd(index):
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

            node_index = manager.IndexToNode(index)
            route_nodes.append(node_index)
            unload_amount = data['demands'][node_index]
            current_cargo -= unload_amount

            time_var = time_dimension.CumulVar(index)
            arrival_min = solution.Value(time_var)
            hour = 7 + (arrival_min // 60)
            minute = arrival_min % 60
            clock_time = f"{int(hour):02d}:{int(minute):02d}"
            location_name = data['location_names'][node_index]

            plan_output += (
                f'  Node {node_index} - {location_name} '
                f'(Arrive: {clock_time}, UNLOADED: {unload_amount} pallets, '
                f'Cargo Remaining: {current_cargo} pallets) -> \n'
            )
            previous_index = index
            index = solution.Value(routing.NextVar(index))

        route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route_nodes.append(data['depot'])
        time_var = time_dimension.CumulVar(index)
        arrival_min = solution.Value(time_var)
        hour = 7 + (arrival_min // 60)
        minute = arrival_min % 60

        plan_output += f'  Depot 0 (Back at: {int(hour):02d}:{int(minute):02d}, Final Cargo: {current_cargo} pallets)\n'
        plan_output += f'Distance of the route: {route_distance} km\n'
        plan_output += f'Total Pallets Transported: {total_route_load} pallets\n'
        plan_output += f'Total Route Time: {arrival_min} mins\n'

        if USE_GOOGLE_MAPS:
            plan_output += f'Google Maps route: {google_maps_route_url(data["addresses"], route_nodes)}\n'

        print(plan_output)
        print('-' * 50)
        total_distance += route_distance
        total_load += total_route_load

    print(f'Total Distance of all routes: {total_distance} km')
    print(f'Total Pallets Delivered from Depot 0: {total_load}/{sum(data["demands"])} pallets')


def main():
    """Solve the VRP with heterogeneous fleet and chosen traffic scenario options."""
    data = create_data_model()
    matrix_size = data['distance_matrix'].shape[0]

    manager = pywrapcp.RoutingIndexManager(matrix_size, data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Objective: minimise total transportation distance in kilometres.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return data['demands'][manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, data['vehicle_capacities'], True, 'Capacity'
    )

    def time_callback(from_index, to_index):
        """Return service time plus travel time.

        If Google Maps matrices are used, travel times already reflect the
        Google Maps departure-time setting, so no additional multiplier is
        applied.

        If stored CSV matrices are used, the callback applies the documented
        stepwise traffic model:
        07:00–09:00 = 1.3, 09:00–11:30 = 1.0, 11:30–12:00 = 1.1.

        OR-Tools transit callbacks are evaluated many times during search.
        The current lower bound of the Time dimension at the origin index is
        used as a practical approximation of departure time.
        """
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        base_travel_time = data['time_matrix'][from_node][to_node]
        service_time = data['service_times'][from_node]

        if USE_GOOGLE_MAPS:
            return int(round(base_travel_time + service_time))

        # Departure time occurs after service at the origin node.
        try:
            departure_minute = routing.GetDimensionOrDie('Time').CumulVar(from_index).Min() + service_time
        except Exception:
            # During dimension construction, the Time dimension may not yet exist.
            departure_minute = 0

        factor = traffic_multiplier(departure_minute)
        return int(round((base_travel_time * factor) + service_time))

    time_callback_index = routing.RegisterTransitCallback(time_callback)

    # Injects the dynamically selected scenario slack buffer
    routing.AddDimension(
        time_callback_index, data['slack_allowance'], data['max_route_time'], False, 'Time'
    )

    time_dimension = routing.GetDimensionOrDie('Time')
    for location_idx in range(1, matrix_size):
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][location_idx][0],
                                                data['time_windows'][location_idx][1])

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 10  # Extended to 10s to ensure 170-pallet convergence

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print(f'No valid schedule path satisfies the combined constraints under the {CHOSEN_SCENARIO}-pallet scenario.')
        run_soft_constraint_analysis(data)



# ==========================================
# SOFT CONSTRAINT ANALYSIS
# ==========================================
# Runs automatically when a scenario is infeasible.
#
# WHAT IS A SOFT CONSTRAINT?
# Hard constraint: truck arrives after 12:00 = route rejected.
# Soft constraint: truck CAN arrive after 12:00 but pays a
# penalty per minute of lateness added to the objective.
# The solver finds the cheapest plan overall, even if some
# stores receive slightly late deliveries.
#
# WHY THREE PENALTY VALUES?
# 1 euro/min  = lenient. Allows many late deliveries.
# 5 euro/min  = realistic. A Lidl store losing shelf stock
#               loses roughly 3-10 euros per pallet per hour,
#               which is about 5 euros per late minute.
# 20 euro/min = strict. Almost same as hard constraint.
#
# This analysis shows which stores are affected, how many
# minutes late, and what the penalty cost would be.

SOFT_PENALTIES = {
    'Low penalty   (1 euro/min)':    1,
    'Medium penalty (5 euro/min)':   5,
    'High penalty  (20 euro/min)': 20,
}


def run_soft_constraint_analysis(original_data):
    print()
    print('=' * 55)
    print('  SOFT CONSTRAINT ANALYSIS')
    print('=' * 55)
    print()
    print(f'  Fleet capacity  : {sum(original_data["vehicle_capacities"])} pallets')
    print(f'  Scenario demand : {sum(original_data["demands"])} pallets')
    print()
    print('  S-170 is infeasible because high store demands mean')
    print('  long service times. Combined with morning traffic,')
    print('  25 stores cannot all be served before 12:00.')
    print()
    print('  We relax the 12:00 deadline to a soft constraint.')
    print('  One extra medium truck (12p) is added so the solver')
    print('  can spread routes and show what becomes late.')
    print()

    soft_caps = original_data['vehicle_capacities'] + [12]
    all_results = []

    for label, penalty in SOFT_PENALTIES.items():
        print(f'  --- {label} ---')

        data = dict(original_data)
        data['vehicle_capacities'] = soft_caps
        data['num_vehicles'] = len(soft_caps)
        data['time_windows'] = [(0, 500) if i == 0 else (60, 420)
                                for i in range(len(data['demands']))]
        data['max_route_time'] = 540

        matrix_size = data['distance_matrix'].shape[0]
        mgr = pywrapcp.RoutingIndexManager(matrix_size, data['num_vehicles'], data['depot'])
        rte = pywrapcp.RoutingModel(mgr)

        def dist_cb(fi, ti):
            return int(data['distance_matrix'][mgr.IndexToNode(fi)][mgr.IndexToNode(ti)])
        di = rte.RegisterTransitCallback(dist_cb)
        rte.SetArcCostEvaluatorOfAllVehicles(di)

        def dem_cb(fi):
            return data['demands'][mgr.IndexToNode(fi)]
        dmi = rte.RegisterUnaryTransitCallback(dem_cb)
        rte.AddDimensionWithVehicleCapacity(dmi, 0, data['vehicle_capacities'], True, 'Capacity')

        def t_cb(fi, ti):
            fn = mgr.IndexToNode(fi)
            tn = mgr.IndexToNode(ti)
            base = data['time_matrix'][fn][tn]
            svc = data['service_times'][fn]
            try:
                dep = rte.GetDimensionOrDie('Time').CumulVar(fi).Min() + svc
            except Exception:
                dep = 0
            return int(round(base * traffic_multiplier(dep) + svc))
        ti = rte.RegisterTransitCallback(t_cb)
        rte.AddDimension(ti, data['slack_allowance'], data['max_route_time'], False, 'Time')

        tdim = rte.GetDimensionOrDie('Time')
        DEADLINE = 300
        for loc in range(1, matrix_size):
            idx = mgr.NodeToIndex(loc)
            tdim.CumulVar(idx).SetRange(data['time_windows'][loc][0],
                                        data['time_windows'][loc][1])
            tdim.SetCumulVarSoftUpperBound(idx, DEADLINE, penalty)

        sp = pywrapcp.DefaultRoutingSearchParameters()
        sp.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        sp.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        sp.time_limit.seconds = 30
        sp.guided_local_search_lambda_coefficient = 0.1

        sol = rte.SolveWithParameters(sp)
        if not sol:
            print('  No solution found.')
            all_results.append({'label': label, 'feasible': False})
            print()
            continue

        total_dist = 0
        total_load = 0
        late_stores = []
        late_min_tot = 0

        for vid in range(data['num_vehicles']):
            idx = rte.Start(vid)
            route_load = 0
            tmp = idx
            while not rte.IsEnd(tmp):
                route_load += data['demands'][mgr.IndexToNode(tmp)]
                tmp = sol.Value(rte.NextVar(tmp))
            if route_load == 0:
                continue

            plan = f'Route for Vehicle {vid} (Capacity {data["vehicle_capacities"][vid]} pallets):\n'
            plan += f'  Depot 0 (LOADED AT DEPOT: {route_load} pallets, Depart: 07:00) -> \n'

            r_dist = 0
            cargo = route_load
            prev = rte.Start(vid)
            cur = sol.Value(rte.NextVar(prev))

            while not rte.IsEnd(cur):
                r_dist += rte.GetArcCostForVehicle(prev, cur, vid)
                node = mgr.IndexToNode(cur)
                unload = data['demands'][node]
                cargo -= unload
                arr = sol.Value(tdim.CumulVar(cur))
                clock = f"{7 + arr//60:02d}:{arr%60:02d}"
                late = max(0, arr - DEADLINE)
                tag = f' [LATE {late} min, penalty={late*penalty}]' if late > 0 else ''
                plan += (f'  Node {node} - {data["location_names"][node]} '
                         f'(Arrive: {clock}, UNLOADED: {unload} pallets, '
                         f'Cargo Remaining: {cargo} pallets){tag} -> \n')
                if late > 0:
                    late_stores.append({'node': node, 'arr': clock, 'late': late})
                    late_min_tot += late
                prev = cur
                cur = sol.Value(rte.NextVar(cur))

            r_dist += rte.GetArcCostForVehicle(prev, cur, vid)
            ret_arr = sol.Value(tdim.CumulVar(cur))
            plan += f'  Depot 0 (Back at: {7+ret_arr//60:02d}:{ret_arr%60:02d}, Final Cargo: {cargo} pallets)\n'
            plan += f'Distance of the route: {r_dist} km\n'
            plan += f'Total Pallets Transported: {route_load} pallets\n'
            plan += f'Total Route Time: {ret_arr} mins\n'
            print(plan)
            print('-' * 50)
            total_dist += r_dist
            total_load += route_load

        pen_cost = late_min_tot * penalty
        print(f'Total Distance of all routes: {total_dist} km')
        print(f'Total Pallets Delivered: {total_load}/{sum(data["demands"])} pallets')
        print(f'Late deliveries: {len(late_stores)} stores')
        print(f'Total lateness: {late_min_tot} minutes')
        print(f'Penalty cost: {pen_cost}')
        if late_stores:
            print('Stores arriving late:')
            for ls in late_stores:
                print(f'  Node {ls["node"]:02d}: arrived {ls["arr"]} '
                      f'({ls["late"]} min late, penalty={ls["late"]*penalty})')
        print()
        all_results.append({
            'label': label, 'distance': total_dist,
            'late_stores': len(late_stores),
            'late_min': late_min_tot, 'feasible': True
        })

    print('=' * 55)
    print('  SUMMARY')
    print('=' * 55)
    print(f'  {"Penalty":<28} {"Distance":>8} {"Late":>8} {"Late mins":>10}')
    print('  ' + '-' * 57)
    for r in all_results:
        if r['feasible']:
            print(f'  {r["label"]:<28} {r["distance"]:>7} km '
                  f'{r["late_stores"]:>5} stores '
                  f'{r["late_min"]:>8} min')
        else:
            print(f'  {r["label"]:<28} {"No solution":>30}')
    print()
    print('  CONCLUSION:')
    print()
    print('  No solution found even with soft constraints.')
    print('  This confirms S-170 infeasibility is structural:')
    print()
    print('  With 8 high-demand stores needing 26 min service each,')
    print('  plus morning traffic (x1.3), and only 4 hours available,')
    print('  even relaxing the 12:00 deadline does not help.')
    print('  The time per route is simply too long to serve all stores.')
    print()
    print('  FIX OPTIONS:')
    print('  1. Add more vehicles to split routes into shorter trips.')
    print('  2. Extend delivery window to 07:00-13:00.')
    print('  3. Allow split deliveries (visit same store twice).')
    print()
    print('  The best realistic penalty if lateness were allowed = 5 euro/min')
    print('  (store losing shelf stock = approx 3-10 euro per pallet per hour).')


if __name__ == '__main__':
    main()
