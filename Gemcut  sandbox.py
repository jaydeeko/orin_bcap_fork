import time
import csv
from bCAPClient.bcapclient import BCAPClient

def read_planes_from_csv(file_path="planes.csv"):
    """
    Read plane data from a CSV file.
    Each row contains A, B, C, D, Z-Intercept, Azimuth (deg), and Pitch (deg).
    """
    planes = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                A = float(row["A"])
                B = float(row["B"])
                C = float(row["C"])
                D = float(row["D"])
                azimuth = float(row["Azimuth (deg)"])
                pitch = float(row["Pitch (deg)"])
                planes.append((A, B, C, D, azimuth, pitch))
            except (KeyError, ValueError) as e:
                print(f"Skipping invalid row: {row} due to error: {e}")
    return planes

# Define connection parameters
HOST = "169.254.183.80"  # Replace with the robot's IP address
PORT = 5007  # Standard port for BCAP
TIMEOUT = 2000  # Timeout in milliseconds

# Robot parameters
robot_name = "vp6242a"  # Name of the robot in the controller
move_speed = "Speed=100"  # Movement speed

try:
    # Initialize BCAP client and connect to the controller
    client = BCAPClient(HOST, PORT, TIMEOUT)
    client.service_start()
    controller_handle = client.controller_connect("", "CaoProv.DENSO.VRC", "localhost", "")
    robot_handle = client.controller_getrobot(controller_handle, robot_name, "")
    client.robot_execute(robot_handle, "Motor", [1, 0])
    client.robot_execute(robot_handle, "TakeArm")
    time.sleep(1)
    client.robot_change(robot_handle, "Tool1")

    # Read planes from CSV
    planes = read_planes_from_csv("planes.csv")

    print(f"Read {len(planes)} planes from planes.csv. Starting loop...")

    for plane in planes:
        A, B, C, D, azimuth, pitch = plane
        print(f"Processing plane: A={A}, B={B}, C={C}, D={D}, Azimuth={azimuth}, Pitch={pitch}")

        # Define a position based on the plane's Z-intercept, azimuth, and pitch
        Z = -D / C if C != 0 else 0  # Calculate Z-intercept
        facet = [0, 0, Z, pitch, azimuth, 0]  # Example facet position

        # Move to position
        Pose = [facet, "CP", "@E"]
        client.robot_move(robot_handle, 2, Pose, move_speed)

        # Example additional operations (e.g., grinding cuts)
        adjusted_facet = [facet[0], facet[1] + 30, facet[2] - 50, facet[3], facet[4], facet[5]]
        Pose = [adjusted_facet, "CP", "@E"]
        client.robot_move(robot_handle, 2, Pose, move_speed)

    # Close robot connection
    client.robot_execute(robot_handle, "GiveArm")
    client.robot_release(robot_handle)
    client.controller_disconnect(controller_handle)

finally:
    # Stop the BCAP service
    client.service_stop()
