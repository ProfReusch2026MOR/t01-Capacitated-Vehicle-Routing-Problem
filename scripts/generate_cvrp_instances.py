import csv
import math
import random
from pathlib import Path

def generate_instance(n_customers, n_vehicles, seed, spread, path):
    random.seed(seed)
    rows = []

    rows.append({
        "node_id": 0,
        "node_type": "depot",
        "x_coord": 50.0,
        "y_coord": 50.0,
        "demand_pallets": 0,
        "service_time_min": 0,
        "time_window_start": "06:30",
        "time_window_end": "17:00",
        "demand_class": "depot",
        "vehicle_count": n_vehicles,
        "vehicle_capacity_pallets": 33
    })

    for i in range(1, n_customers + 1):
        angle = random.random() * 2 * math.pi
        radius = random.uniform(5, spread)
        x = round(50 + math.cos(angle) * radius + random.uniform(-3, 3), 2)
        y = round(50 + math.sin(angle) * radius + random.uniform(-3, 3), 2)

        demand = random.choice([3, 4, 4, 5, 5])
        if demand <= 3:
            demand_class = "low"
        elif demand == 4:
            demand_class = "medium"
        else:
            demand_class = "high"

        service_time = 10 + 2 * demand

        rows.append({
            "node_id": i,
            "node_type": "customer",
            "x_coord": x,
            "y_coord": y,
            "demand_pallets": demand,
            "service_time_min": service_time,
            "time_window_start": "08:00",
            "time_window_end": "12:00",
            "demand_class": demand_class,
            "vehicle_count": n_vehicles,
            "vehicle_capacity_pallets": 33
        })

    with open(path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "node_id",
            "node_type",
            "x_coord",
            "y_coord",
            "demand_pallets",
            "service_time_min",
            "time_window_start",
            "time_window_end",
            "demand_class",
            "vehicle_count",
            "vehicle_capacity_pallets",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    output_dir = Path("DATA")
    output_dir.mkdir(exist_ok=True)

    generate_instance(10, 2, 42, 20, output_dir / "cvrp_small.csv")
    generate_instance(40, 5, 43, 45, output_dir / "cvrp_medium.csv")
    generate_instance(100, 12, 44, 90, output_dir / "cvrp_large.csv")

    print("Generated CVRP instances in DATA/")
