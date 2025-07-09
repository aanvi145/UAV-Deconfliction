# visualization.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from typing import List, Optional

from data_models import Mission, SimulatedDrone, Conflict
from path_utils import generate_primary_trajectory, interpolate_position_at_time

def plot_trajectories(
    title: str,
    primary_mission: Mission,
    simulated_drones: List[SimulatedDrone],
    conflicts: Optional[List[Conflict]] = None
):
    """
    Generates a 3D plot of all drone trajectories and highlights conflicts.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title, fontsize=16)

    # 1. Plot Primary Mission
    primary_trajectory = generate_primary_trajectory(primary_mission)
    p_x = [p[0] for p in primary_trajectory]
    p_y = [p[1] for p in primary_trajectory]
    p_z = [p[2] for p in primary_trajectory]
    ax.plot(p_x, p_y, p_z, label='Primary Mission Path', color='blue', linewidth=3, zorder=10)
    
    # Plot waypoints
    wp_x = [wp[0] for wp in primary_mission.waypoints]
    wp_y = [wp[1] for wp in primary_mission.waypoints]
    wp_z = [wp[2] for wp in primary_mission.waypoints]
    ax.scatter(wp_x, wp_y, wp_z, color='blue', s=100, marker='o', label='Primary Waypoints', zorder=11)

    # 2. Plot Simulated Drones
    colors = plt.cm.get_cmap('viridis', len(simulated_drones))
    for i, drone in enumerate(simulated_drones):
        s_x = [p[0] for p in drone.trajectory]
        s_y = [p[1] for p in drone.trajectory]
        s_z = [p[2] for p in drone.trajectory]
        ax.plot(s_x, s_y, s_z, label=f'Drone {drone.drone_id} Path', color=colors(i), linestyle='--')

    # 3. Plot Conflicts if they exist
    if conflicts:
        for conflict in conflicts:
            loc = conflict.location
            ax.scatter(loc[0], loc[1], loc[2], color='red', s=200, marker='X', 
                       zorder=12)
        
        # Avoid duplicate labels for conflicts in the legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        # Customize the conflict label to be generic
        if f'Conflict @ T={conflicts[0].time:.1f}s' in by_label:
            conflict_handle = by_label[f'Conflict @ T={conflicts[0].time:.1f}s']
            del by_label[f'Conflict @ T={conflicts[0].time:.1f}s']
            by_label['Conflict Point'] = conflict_handle
        ax.legend(by_label.values(), by_label.keys())
    else:
        ax.legend()

    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (altitude in meters)')  # type: ignore
    plt.show()