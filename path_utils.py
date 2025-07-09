# path_utils.py
import numpy as np
from typing import List
from data_models import Mission, TrajectoryPoint, Waypoint3D

def calculate_distance(p1: Waypoint3D, p2: Waypoint3D) -> float:
    """Calculates the Euclidean distance between two 3D points."""
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))

def calculate_total_distance(waypoints: List[Waypoint3D]) -> float:
    """Calculates the total path length over a series of waypoints."""
    total_dist = 0.0
    for i in range(len(waypoints) - 1):
        total_dist += calculate_distance(waypoints[i], waypoints[i+1])
    return total_dist

def generate_primary_trajectory(mission: Mission) -> List[TrajectoryPoint]:
    """
    Generates a full spatiotemporal trajectory for the primary drone based on its mission.
    Assumes constant speed to complete the mission exactly in the given time window.
    """
    total_dist = calculate_total_distance(mission.waypoints)
    mission_duration = mission.end_time - mission.start_time
    
    if mission_duration <= 0:
        raise ValueError("Mission end time must be after start time.")
    if total_dist == 0:
        # If the drone doesn't move, its trajectory is just the start point over time
        stationary_trajectory: List[TrajectoryPoint] = []
        for t in np.arange(mission.start_time, mission.end_time, 1.0):
            stationary_trajectory.append((mission.waypoints[0][0], mission.waypoints[0][1], mission.waypoints[0][2], float(t)))
        return stationary_trajectory

    speed = total_dist / mission_duration
    
    trajectory: List[TrajectoryPoint] = []
    current_time = mission.start_time
    
    for i in range(len(mission.waypoints) - 1):
        p1 = mission.waypoints[i]
        p2 = mission.waypoints[i+1]
        segment_dist = calculate_distance(p1, p2)
        segment_duration = segment_dist / speed
        
        # Add the start point of the segment
        trajectory.append((p1[0], p1[1], p1[2], current_time))
        
        current_time += segment_duration

    # Add the final waypoint at the mission end time
    last_wp = mission.waypoints[-1]
    trajectory.append((last_wp[0], last_wp[1], last_wp[2], mission.end_time))
    
    return trajectory

def interpolate_position_at_time(trajectory: List[TrajectoryPoint], time: float) -> Waypoint3D | None:
    """
    Finds the 3D position of a drone at a specific time by interpolating its trajectory.
    Returns None if the time is outside the trajectory's time range.
    """
    # Find the two trajectory points that bracket the given time
    p1 = None
    p2 = None
    for point in trajectory:
        if point[3] <= time:
            p1 = point
        if point[3] >= time:
            p2 = point
            break
    
    # If time is outside the trajectory's bounds or there's no movement
    if p1 is None or p2 is None:
        return None # Not active at this time
    
    if p1 == p2:
        return (p1[0], p1[1], p1[2])

    # Linear interpolation
    p1_pos, p1_time = np.array(p1[:3]), p1[3]
    p2_pos, p2_time = np.array(p2[:3]), p2[3]
    
    time_diff = p2_time - p1_time
    if time_diff == 0:
        return tuple(p1_pos)

    fraction = (time - p1_time) / time_diff
    interpolated_pos = p1_pos + fraction * (p2_pos - p1_pos)
    
    return tuple(interpolated_pos)