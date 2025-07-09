# Reflection & Justification Document

## Design Decisions and Architecture

The system is designed with a modular architecture to separate concerns, enhancing maintainability and testability. This is chosen for easy access to updgrade each file, reduce confusion, easier to debug and handle edge cases:
- **Data Models (`data_models.py`)**: Using Python's `dataclasses` provides type safety and self-documenting code structures, preventing common errors associated with managing raw tuples or dictionaries.
- **Core Logic (`deconfliction_service.py`)**: The main service is decoupled from data loading and visualization. It accepts structured data and returns a structured result, making it a pure, testable function.
- **Utilities (`path_utils.py`)**: Geometric and interpolation logic is isolated. If we wanted to switch from linear to curved path interpolation, the changes would be localized to this file.
- **Configuration (`scenarios.json`)**: Externalizing the simulated drone data into a JSON file allows for easy testing of new scenarios without altering the core codebase. This is hardcoded like mentioned in the assignment. 
- **Setting up (`main.py`)**: This orchestrates the entire simulation and is responsible for calling the correct services to visualize, print results, and load the data. 

The conflict detection algorithm works by discretizing time. It steps through the primary mission's time window and, at each step, calculates the position of every drone to check for buffer violations. This is a straightforward and effective method for the scale of this problem.

## AI Integration

This system was mostly designed through AI prompt engineering and refined through Cursor involved AI and simple debugging. Most mistakes were syntax errors and easy fixes by a human. The safety buffer value was decreased for a more realistic scenario. AI refined the code and handled the test cases by itself to provide more accurate code the first time for the system. Environment and dependencies installations were done on the human end. 

## Scaling to Tens of Thousands of Drones

The current implementation is suitable for a small number of drones but would not scale to tens of thousands of commercial drones in real-time due to its computational complexity. The current algorithm is roughly `O(T * N)`, where `T` is the number of time steps and `N` is the number of simulated drones. For a large system, this is too slow. We want it to be more efficient.

## Handling Edge Cases
This code handles multiple edge cases
-**start_time after end_time**
    -ValueError is raised to prevent simulation from running with invalid values
**Same start and end waypoints**
    -There could be a case where the start and end way points would be the same, resulting in a distance of 0 which is checked for in the code. If this is true, a trajectory of constant position over changing time is created so there is no division by 0 error. 
**Drone position check before start or after end time (ie. Drone not flying)**
    -interpolate_position_at_time function returns None and in the main.py script, it is checked once more and skips that drone if that if detected through the for loop.
**Vertical Movement (drone only ascends or descends)**
    -Euclidean distance formula handles this through dz in the eq (sqrt (dx^2 + dy^2 + dz^3)) and will still have a calculated distance cross checked with the safety buffer, above or below the drone.

Here is an outline of the necessary architectural changes and enhancements:

### 1. Algorithmic Enhancements & Data Structures
- **Spatial Indexing**: Instead of checking against every single drone, we can use spatial data structures to quickly query for drones within a certain area.
  - **k-d Trees or Octrees**: These structures partition the 3D space. To check for conflicts for our primary drone at position `P`, we would only need to query the tree for other drones in the vicinity of `P`, drastically reducing the number of distance calculations. The tree would need to be updated as drones move, but for strategic deconfliction (pre-flight checks), we can build a 4D (x, y, z, t) tree once.
- **Collision Detection Algorithms**: Move from discrete time-stepping to continuous collision detection. Instead of checking points in time, we can treat trajectories as 4D line segments ("tubes" with the safety buffer radius) and mathematically check for intersections. This is more complex but far more accurate and efficient as it avoids missing conflicts that might occur between time steps.

### 2. Architectural Changes for Real-Time and Scale
- **Distributed Computing**: A single machine cannot handle the load. We need a distributed system.
  - **Airspace Partitioning (Geofencing)**: Divide the airspace into geographic cells (e.g., using a grid system like S2 or H3). Each cell's deconfliction can be managed by a separate computational node/service. 

### 3. Interactive UI
- **Editable Inputs**: For a more realistic and useful system, users should be able to input on the command line, just the starting time and speed of multiple drones to see possible collision or even pull from an existing database rather than cross checking a hard-coded database.

