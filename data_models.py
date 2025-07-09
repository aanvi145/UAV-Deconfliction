# data_models.py
from dataclasses import dataclass, field
from typing import List, Tuple

# Using floats for coordinates and time for precision
Waypoint3D = Tuple[float, float, float]
TrajectoryPoint = Tuple[float, float, float, float] # (x, y, z, time)

@dataclass
class Mission:
    """Represents the primary drone's mission."""
    waypoints: List[Waypoint3D]
    start_time: float
    end_time: float

@dataclass
class SimulatedDrone:
    """Represents a simulated drone with a pre-defined trajectory."""
    drone_id: str
    # Trajectory is a list of (x, y, z, time) points, sorted by time
    trajectory: List[TrajectoryPoint]

@dataclass
class Conflict:
    """Represents a detected conflict."""
    time: float
    location: Waypoint3D
    drone_ids: Tuple[str, str]

    def __repr__(self) -> str:
        return (f"Conflict at T={self.time:.2f}s "
                f"near location {tuple(round(c, 2) for c in self.location)} "
                f"between drones {self.drone_ids[0]} and {self.drone_ids[1]}")