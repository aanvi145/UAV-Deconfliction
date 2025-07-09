# UAV Strategic Deconfliction System

This project implements a strategic deconfliction system to verify if a primary drone's planned mission is safe to execute in a shared airspace populated by other drones. The system performs 4D (3D space + time) conflict checking.

## Project Structure

- `main.py`: The main script to run predefined scenarios.
- `deconfliction_service.py`: Contains the core logic for checking for spatiotemporal conflicts.
- `path_utils.py`: Helper functions for geometric calculations (distance, interpolation).
- `data_models.py`: Defines the data classes (`Mission`, `Conflict`, etc.) for clear and robust data handling.
- `visualization.py`: Handles the 3D plotting of trajectories and conflicts using Matplotlib.
- `scenarios.json`: A data file defining the flight paths of other drones in the airspace.
- `requirements.txt`: Required Python packages.

## Assumptions Made

- **Drone Speed**: The primary drone travels at a constant speed, calculated to complete its mission exactly between `T_start` and `T_end`.
- **Path**: All drones travel in straight lines between waypoints.
- **Safety Buffer**: A conflict is defined as two drones coming within **25 meters** of each other. #Human edit, an even smaller buffer zone would make sense proportionally based on the drone but for this case it is 25 meters
- **Conflict Checking**: The simulation checks for conflicts at **1-second intervals**.
- **Units**: All spatial coordinates are in **meters**, and time is in **seconds**.

## How to Run

1.  **Set up the environment**:
    ```bash
    # It's recommended to use a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt #for numpy and matplotlib, assuming not already installed
    ```

3.  **Run the simulation**:
    ```bash
    python main.py
    ```

This will execute several predefined scenarios (both conflict-free and with conflicts) and display the results in the console. For each scenario, a 3D plot will be generated to visually represent the drone paths and any detected conflicts.