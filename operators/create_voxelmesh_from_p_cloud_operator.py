'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

FOtools: a set of blender tools to assist in 3D-Forensic analysis Alexander de Bruijn 2022
'''

import bpy
import numpy as np
from mathutils import Vector


class FOtools_OT_CreateVoxelMeshFromCloud(bpy.types.Operator):
    bl_idname = "mesh.create_voxel_mesh_from_cloud"
    bl_label = "Create Voxel Mesh from Point Cloud"   
    bl_description = "Create a voxel mesh from a point cloud"
    bl_options = {"UNDO"}
    
    
    @classmethod
    def poll(cls, context):
     return True

    
    def execute(self, context):
        #TODO: voxelsize must be passed by the panel ui
        VOXEL_SIZE = 1.0  
        #TODO:  should be passed from the pannel, or panel ui uld pass active object
        points = get_point_cloud_coordinates()
        create_voxel_grid(points, VOXEL_SIZE)
        return {"FINISHED"}
    
    
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

