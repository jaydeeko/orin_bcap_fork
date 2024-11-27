import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
import math
import csv

indexwheelreal= 360/96


def extract_plane_equations(stl_mesh):
    """
    Extract plane equations (Ax + By + Cz + D = 0) and Z-intercepts from the STL mesh.
    """
    planes = []
    for i in range(len(stl_mesh.vectors)):
        v1, v2, v3 = stl_mesh.vectors[i]
        # Calculate the normal vector (A, B, C)
        normal = np.cross(v2 - v1, v3 - v1)
        normal = normal / np.linalg.norm(normal)

        # Calculate D using one vertex
        D = -np.dot(normal, v1)

        # Calculate Z-intercept (set x=0, y=0, solve for z)
        if normal[2] != 0:  # Avoid division by zero
            z_intercept = -D / normal[2]
        else:
            z_intercept = None  # Parallel to the Z-axis

        planes.append((*normal, D, z_intercept))
    return planes


def visualize_endpoints(stl_mesh):
    """
    Visualize endpoints (vertices) in 3D.
    """
    vertices = np.vstack(stl_mesh.vectors)
    x, y, z = vertices.T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='blue', s=1)
    ax.set_title('STL Endpoints Visualization')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()





def calculate_rotation_and_pitch(A, B, C, D, indexwheel=3.75):
    """
        Calculate the shortest distance from the plane to the Z-axis (Girdle Z).
        :param A: X-coefficient of the plane equation
        :param B: Y-coefficient of the plane equation
        :param C: Z-coefficient of the plane equation
        :param D: Constant term of the plane equation
        :return: Girdle Z (shortest distance from plane to Z-axis) or None if C != 0
        """


    # Calculate the azimuth (angle around Z-axis) of the normal vector projected onto the XY-plane
    azimuth = math.degrees(math.atan2(B, A))  # Angle in degrees
    if azimuth < 0:
        azimuth += 360  # Ensure the azimuth is within [0, 360)

    # Convert azimuth to index
    index = azimuth / indexwheel

    # Calculate pitch (angle between the normal vector and the XY-plane)
    pitch = math.degrees(math.atan2(C, math.sqrt(A ** 2 + B ** 2)))


    #Girdle condition
    if C == 0:
        # Calculate shortest distance to the Z-axis
        GirdleZ =abs(D) / math.sqrt(A ** 2 + B ** 2)
    else:
        GirdleZ = "N/A"
    return round(index), pitch, GirdleZ


def export_planes_to_csv(planes, output_file="planes.csv", indexwheel=3.75):
    """
    Export plane equations, Z-intercepts, rotation around Z-axis, pitch, and Girdle Z to a CSV file.
    The output is aligned, formatted for readability, and removes duplicate rows.
    :param planes: List of planes, each represented as [A, B, C, D]
    :param output_file: Name of the output CSV file
    :param indexwheel: Conversion factor for index calculation
    """

    def format_value(value, width=10):
        """Format values for better readability and alignment."""
        if value is None:
            return "N/A".rjust(width)
        elif isinstance(value, float):
            return f"{value:.3f}".rjust(width)
        return str(value).rjust(width)

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Define column headers with alignment
        headers = ["Z-Intercept", "Index", "Pitch", "GirdleZ"]
        formatted_headers = [header.center(12) for header in headers]
        writer.writerow(formatted_headers)

        rows = set()  # Use a set to track unique rows
        for plane in planes:
            A, B, C, D = plane[:4]

            # Calculate Z-intercept (if C != 0)
            z_intercept = round(-D / C, 3) if C != 0 else None

            # Calculate index, pitch, and Girdle Z
            index, pitch, girdlez = calculate_rotation_and_pitch(A, B, C, D, indexwheel)
            index = round(index, 3)
            pitch = round(pitch, 3)

            if girdlez!="N/A":
                girdlez = round(girdlez, 3)
                print("Rounding")

            # Create a tuple of values to ensure uniqueness
            row = (
                format_value(z_intercept),
                format_value(index),
                format_value(pitch),
                format_value(girdlez),
            )

            rows.add(row)  # Add the formatted row to the set to remove duplicates

        # Write unique rows to the CSV
        for row in sorted(rows):  # Optional: Sort rows for consistent output
            writer.writerow(row)
    print(f"Planes exported to {output_file}, duplicates removed.")


def main(stl_file):
    # Load the STL file
    stl_mesh = mesh.Mesh.from_file(stl_file)

    # Visualize endpoints
    visualize_endpoints(stl_mesh)

    # Extract plane equations and Z-intercepts
    planes = extract_plane_equations(stl_mesh)

    # Export planes to a CSV file
    export_planes_to_csv(planes)


# Replace 'your_file.stl' with your STL file path
stl_file = 'Simple Example.stl'
main(stl_file)
