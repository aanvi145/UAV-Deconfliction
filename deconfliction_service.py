# deconfliction_service.py
from typing import List, Dict, Any
import numpy as np

from data_models import Mission, SimulatedDrone, Conflict
from path_utils import generate_primary_trajectory, interpolate_position_at_time, calculate_distance

PRIMARY_DRONE_ID = "Primary-Mission"

def check_for_conflicts(
    primary_mission: Mission,
    simulated_drones: List[SimulatedDrone],
    safety_buffer: float,
    time_step: float = 1.0
) -> Dict[str, Any]:
    """
    Checks a primary drone mission for spatiotemporal conflicts against other drones.

    Args:
        primary_mission: The mission to be checked.
        simulated_drones: A list of other drones in the airspace.
        safety_buffer: The minimum required distance between drones (in meters).
        time_step: The interval (in seconds) at which to check for conflicts.

    Returns:
        A dictionary containing the status ("clear" or "conflict detected") and
        a list of detailed conflict information.
    """
    try:
        primary_trajectory = generate_primary_trajectory(primary_mission)
    except ValueError as e:
        return {"status": "error", "details": str(e)}

    conflicts: List[Conflict] = []
    
    # Iterate through the mission time window at the specified time step
    for t in np.arange(primary_mission.start_time, primary_mission.end_time, time_step):
        primary_pos = interpolate_position_at_time(primary_trajectory, float(t))
        if primary_pos is None:
            continue

        # Check against each simulated drone
        for sim_drone in simulated_drones:
            sim_pos = interpolate_position_at_time(sim_drone.trajectory, float(t))
            if sim_pos is None:
                # This simulated drone is not active at this time, so no conflict is possible
                continue

            distance = calculate_distance(primary_pos, sim_pos)
            
            if distance < safety_buffer:
                conflict = Conflict(
                    time=float(t),
                    location=primary_pos,
                    drone_ids=(PRIMARY_DRONE_ID, sim_drone.drone_id)
                )
                conflicts.append(conflict)

    if not conflicts:
        return {"status": "clear", "details": "No conflicts detected."}
    else:
        # Simple de-duplication: group conflicts that are very close in time
        # This is a basic approach; more sophisticated clustering could be used.
        deduped_conflicts = []
        if conflicts:
            conflicts.sort(key=lambda c: c.time)
            last_conflict = conflicts[0]
            for i in range(1, len(conflicts)):
                # If a new conflict is with the same drone and very close in time, skip it
                if (conflicts[i].drone_ids == last_conflict.drone_ids and 
                    conflicts[i].time - last_conflict.time < 5.0): # 5s grouping window
                    continue
                deduped_conflicts.append(last_conflict)
                last_conflict = conflicts[i]
            deduped_conflicts.append(last_conflict)

        return {"status": "conflict detected", "details": deduped_conflicts}