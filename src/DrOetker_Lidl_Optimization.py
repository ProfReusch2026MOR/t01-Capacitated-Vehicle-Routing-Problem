import numpy as np
import pandas as pd
import re
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# ==========================================
# SCENARIO CONFIGURATION MANAGER
# ==========================================
# Change this number to switch scenarios: 99, 152, or 170
CHOSEN_SCENARIO = 99

def load_matrix_completely_safe(file_name):
    """Reads any broken tab/comma/space separated file safely without pandas read_csv parser errors."""
    matrix_data = []
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', line)
            if numbers:
                matrix_data.append([float(num) for num in numbers])

    df = pd.DataFrame(matrix_data).dropna(how='all').dropna(axis=1, how='all')
    if df.shape[0] > 1 and df.shape[1] > 1:
        if df.iloc[0, 0] == 0 and df.iloc[0, 1] == 1:
            df = df.iloc[1:, 1:]
    return df.to_numpy().round().astype(int)


def create_data_model():
    """Stores the data for the problem based on the chosen scenario."""
    data = {}

    print(f"--- INITIALIZING SCENARIO: {CHOSEN_SCENARIO} PALLETS ---")
    data['distance_matrix'] = load_matrix_completely_safe('distance_matrix.csv')
    data['time_matrix'] = load_matrix_completely_safe('time_matrix.csv')

    # 1. PROFILE DICTIONARY SWITCH
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

    # Error checking for typos in setting scenario config
    if CHOSEN_SCENARIO not in scenarios_demands:
        raise ValueError(f"Scenario {CHOSEN_SCENARIO} is not defined! Please pick 99, 152, or 170.")

    data['demands'] = scenarios_demands[CHOSEN_SCENARIO]
    print(f"Verified Combined Network Volume: {sum(data['demands'])} pallets")

    # Fleet Matrix: 4 Heavy Trucks (33) + 4 Medium Trucks (12) = 180 total volume pool
    data['vehicle_capacities'] = [33, 33, 33, 33, 12, 12, 12, 12]
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['depot'] = 0

    # Auto-adjust service time metrics based on demands: s_i = 10 + 2 * q_i
    data['service_times'] = [10 + (2 * q) if q > 0 else 0 for q in data['demands']]

    # Set time dimensions (Depot launch at 07:00 AM)
    data['time_windows'] = [(0, 500) if i == 0 else (60, 300) for i in range(len(data['demands']))]
    data['max_route_time'] = 405

    # Dynamic Slack Allocation: Heuristically increases the waiting buffer as volumes grow tighter
    if CHOSEN_SCENARIO == 99:
        data['slack_allowance'] = 45
    elif CHOSEN_SCENARIO == 152:
        data['slack_allowance'] = 75
    else:  # 170 Pallets
        data['slack_allowance'] = 90  # Massive window tolerance to resolve near 100% capacity bottlenecks

    return data


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

        plan_output = f'Route for Vehicle {vehicle_id} (Capacity {data["vehicle_capacities"][vehicle_id]} pallets):\n'
        plan_output += f'  Depot 0 (LOADED AT DEPOT: {total_route_load} pallets, Depart: 07:00) -> \n'

        route_distance = 0
        current_cargo = total_route_load

        index = solution.Value(routing.NextVar(index))
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            unload_amount = data['demands'][node_index]
            current_cargo -= unload_amount

            time_var = time_dimension.CumulVar(index)
            arrival_min = solution.Value(time_var)
            hour = 7 + (arrival_min // 60)
            minute = arrival_min % 60
            clock_time = f"{int(hour):02d}:{int(minute):02d}"

            plan_output += f'  Node {node_index} (Arrive: {clock_time}, UNLOADED: {unload_amount} pallets, Cargo Remaining: {current_cargo} pallets) -> \n'
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        time_var = time_dimension.CumulVar(index)
        arrival_min = solution.Value(time_var)
        hour = 7 + (arrival_min // 60)
        minute = arrival_min % 60

        plan_output += f'  Depot 0 (Back at: {int(hour):02d}:{int(minute):02d}, Final Cargo: {current_cargo} pallets)\n'
        plan_output += f'Distance of the route: {route_distance} km\n'
        plan_output += f'Total Pallets Transported: {total_route_load} pallets\n'
        plan_output += f'Total Route Time: {arrival_min} mins\n'

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
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        return data['demands'][manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, data['vehicle_capacities'], True, 'Capacity'
    )

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        base_travel_time = data['time_matrix'][from_node][to_node]
        service_time = data['service_times'][from_node]

        try:
            current_time = solution.Value(time_dimension.CumulVar(from_index))
        except:
            current_time = 0

        if current_time < 120:
            traffic_factor = 1.3
        elif current_time < 270:
            traffic_factor = 1.0
        else:
            traffic_factor = 1.1

        return int((base_travel_time * traffic_factor) + service_time)

    time_callback_index = routing.RegisterTransitCallback(time_callback)

    # Injects the dynamically selected scenario slack buffer
    routing.AddDimension(
        time_callback_index, data['slack_allowance'], data['max_route_time'], False, 'Time'
    )

    time_dimension = routing.GetDimensionOrDie('Time')
    for location_idx in range(matrix_size):
        if location_idx == 0:
            continue
        for vehicle_id in range(data['num_vehicles']):
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(data['time_windows'][location_idx][0],
                                                    data['time_windows'][location_idx][1])

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 10  # Extended to 10s to ensure 170-pallet convergence

    global solution
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print(f'No valid schedule path satisfies the combined constraints under the {CHOSEN_SCENARIO}-pallet scenario.')


if __name__ == '__main__':
    main()