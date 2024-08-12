import numpy as np
from PIL import Image
import trimesh
from scipy.spatial import Delaunay
from scipy.ndimage import gaussian_filter
import argparse

def main(depth_map_path):
    # Load the depth map
    depth_image = Image.open(depth_map_path)

    # Convert the image to grayscale
    depth_image = depth_image.convert('L')

    # Convert the depth image to a NumPy array
    depth_array = np.array(depth_image)

    # Apply Gaussian filter to smooth the depth map
    depth_array = gaussian_filter(depth_array, sigma=2)

    # Normalize the depth map
    depth_array = depth_array.astype(np.float32)
    depth_array = (depth_array - depth_array.min()) / (depth_array.max() - depth_array.min())

    # Generate 3D point cloud from the depth map
    height, width = depth_array.shape
    xx, yy = np.meshgrid(np.arange(0, width), np.arange(0, height))

    # Flip the Y-axis to correct the upside-down orientation
    yy = height - yy

    # Scale the depth values (adjust as needed)
    zz = depth_array * 1000

    # Combine x, y, z coordinates into a point cloud
    points = np.vstack((xx.flatten(), yy.flatten(), zz.flatten())).T

    # Create the Delaunay triangulation of the 2D grid of points
    tri = Delaunay(np.vstack([xx.flatten(), yy.flatten()]).T)

    # Create a Trimesh object
    mesh = trimesh.Trimesh(vertices=points, faces=tri.simplices)

    # Apply Laplacian smoothing to the mesh
    iterations = 2  # Number of smoothing iterations
    mesh = mesh.smoothed(iterations=iterations)

    # Apply Subdivision Surface Smoothing
    mesh = mesh.subdivide()

    # Export the mesh to an OBJ file or another format
    obj_output_path = depth_map_path.replace('.png', '_model.obj')
    mesh.export(obj_output_path)

    print(f"OBJ file saved as {obj_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a depth map to generate a 3D model.")
    parser.add_argument('--depth_map_path', required=True, help='Path to the depth map image.')
    args = parser.parse_args()
    main(args.depth_map_path)
