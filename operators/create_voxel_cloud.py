'''
import bpy
import numpy as np
from mathutils import Vector

def get_point_cloud_coordinates():
    # Get the active object (assumed to be your point cloud)
    obj = bpy.context.active_object
    
    # Get world space coordinates of all vertices
    coords = [obj.matrix_world @ Vector(v.co) for v in obj.data.vertices]
    return np.array(coords)

def create_voxel_grid(points, voxel_size):
    # Calculate grid bounds
    min_bounds = np.floor(points.min(axis=0) / voxel_size) * voxel_size
    max_bounds = np.ceil(points.max(axis=0) / voxel_size) * voxel_size
    
    # Create dictionary to store occupied voxels
    voxels = {}
    
    # Assign points to voxels
    for point in points:
        # Calculate voxel indices
        voxel_coord = tuple(np.floor((point - min_bounds) / voxel_size))
        voxels[voxel_coord] = True
    
    # Create cube mesh for each voxel
    for voxel_coord in voxels:
        # Calculate world space position
        position = min_bounds + (np.array(voxel_coord) * voxel_size)
        
        # Add cube
        bpy.ops.mesh.primitive_cube_add(size=voxel_size, location=position)
        
        # Optional: Add material or modify cube properties here

# Set your desired voxel size
VOXEL_SIZE = 1.0  # Adjust this value to change voxel size

# Get point cloud coordinates
points = get_point_cloud_coordinates()

# Create voxel grid
create_voxel_grid(points, VOXEL_SIZE)
'''