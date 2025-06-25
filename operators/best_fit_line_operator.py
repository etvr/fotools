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
import bmesh
import numpy as np
from mathutils import Vector

class Best_Fit_Line_Operator(bpy.types.Operator):
    """Create a best fit line through selected vertices"""
    bl_idname = "mesh.best_fit_line"
    bl_label = "Best Fit Line"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        create_best_fit_line()
        return {'FINISHED'}
    
    def create_best_fit_line():
        # Get the active object
        obj = bpy.context.active_object
        
        if obj is None or obj.type != 'MESH':
            print("No active mesh object selected")
            return
            
        # Get a BMesh representation
        bm = bmesh.from_edit_mesh(obj.data)
        
        # Get selected vertices
        selected_verts = [v for v in bm.verts if v.select]
        
        if len(selected_verts) < 2:
            print("Not enough vertices selected (need at least 2)")
            return
        
        # Get coordinates of selected vertices
        coords = np.array([v.co for v in selected_verts])
        
        # Calculate centroid
        centroid = np.mean(coords, axis=0)
        
        # Calculate direction using Principal Component Analysis (PCA)
        # First, center the data
        centered_coords = coords - centroid
        
        # Calculate covariance matrix
        cov_matrix = np.cov(centered_coords.T)
        
        # Calculate eigenvectors and eigenvalues
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Sort eigenvectors by eigenvalues in descending order
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Principal direction is the eigenvector with the largest eigenvalue
        principal_direction = Vector(eigenvectors[:, 0])
        principal_direction.normalize()
        
        # Find the extent of the vertices along the principal direction
        projections = [Vector(p - centroid).dot(principal_direction) for p in coords]
        min_proj = min(projections)
        max_proj = max(projections)
        
        # Create a new mesh for the line
        line_mesh = bpy.data.meshes.new("BestFitLine")
        line_obj = bpy.data.objects.new("BestFitLine", line_mesh)
        
        # Link the object to the scene
        bpy.context.collection.objects.link(line_obj)
        
        # Create the line vertices
        start_point = Vector(centroid) + principal_direction * min_proj
        end_point = Vector(centroid) + principal_direction * max_proj
        
        # Create the line mesh
        line_verts = [start_point, end_point]
        line_edges = [(0, 1)]
        line_mesh.from_pydata(line_verts, line_edges, [])
        line_mesh.update()
        
        print("Best fit line created")
        return line_obj