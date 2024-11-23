import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
import csv


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


def export_planes_to_csv(planes, output_file="planes.csv"):
    """
    Export plane equations and Z-intercepts to a CSV file.
    """
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["A", "B", "C", "D", "Z-Intercept"])
        writer.writerows(planes)
    print(f"Planes exported to {output_file}")


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
stl_file = 'Spyro_Gem.stl'
main(stl_file)
