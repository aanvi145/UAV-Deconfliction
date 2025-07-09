# main.py
import json
from typing import List

from data_models import Mission, SimulatedDrone, Waypoint3D
from deconfliction_service import check_for_conflicts
from visualization import plot_trajectories

def load_simulated_drones(filepath: str) -> List[SimulatedDrone]:
    """Loads simulated drone data from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return [
        SimulatedDrone(
            drone_id=d['drone_id'],
            trajectory=[tuple(point) for point in d['trajectory']]
        )
        for d in data['simulated_drones']
    ]

def run_scenario(scenario_name: str, mission: Mission, sim_drones: List[SimulatedDrone]):
    """Runs a single deconfliction scenario and prints/plots the results."""
    print(f"\n--- RUNNING SCENARIO: {scenario_name} ---")
    
    # System parameters
    SAFETY_BUFFER = 25.0  # meters
    TIME_STEP = 1.0       # seconds

    result = check_for_conflicts(mission, sim_drones, SAFETY_BUFFER, TIME_STEP)
    
    print(f"Deconfliction Status: {result['status'].upper()}")
    if result['status'] == "conflict detected":
        print("Conflict Details:")
        for conflict in result['details']:
            print(f"  - {conflict}")
        plot_trajectories(
            f"Visualization for {scenario_name}",
            mission,
            sim_drones,
            result['details']
        )
    else:
        print(f"Details: {result['details']}")
        plot_trajectories(
            f"Visualization for {scenario_name}",
            mission,
            sim_drones
        )

if __name__ == "__main__":
    # Load the shared airspace data
    simulated_drones = load_simulated_drones("scenarios.json")

    # --- SCENARIO 1: A mission that should be conflict-free ---
    mission_clear = Mission(
        waypoints=[(0, 0, 150), (1000, 1000, 150)],
        start_time=0.0,
        end_time=120.0
    )
    run_scenario("Conflict-Free Mission", mission_clear, simulated_drones)

    # --- SCENARIO 2: A mission designed to conflict with drone 'Alpha-1' ---
    # This path crosses Alpha-1's path at roughly the same time.
    mission_conflict_alpha = Mission(
        waypoints=[(500, 0, 110), (500, 1000, 110)],
        start_time=0.0,
        end_time=100.0
    )
    run_scenario("Conflict with Alpha-1", mission_conflict_alpha, simulated_drones)

    # --- SCENARIO 3: A mission designed to conflict with drone 'Bravo-2' ---
    # This path crosses Bravo-2's path.
    mission_conflict_bravo = Mission(
        waypoints=[(100, 100, 115), (900, 900, 115)],
        start_time=30.0,
        end_time=110.0
    )
    run_scenario("Conflict with Bravo-2", mission_conflict_bravo, simulated_drones)