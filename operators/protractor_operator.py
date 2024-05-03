"""
Created by Alexander de Bruijn 2024

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

FOtools: a set of blender tools to assist in 3D-Forensic analysis


calculates the coordinates of  the top vertex of the protractor angle with the given corner at the origin,
              c                  given angle a 
            /|                  vertex a = [0, 0] at the origin
          /  |                  vertex c = [sin(90 - angle a)*radius, sin(angle a)*radius]
        /    |                  vertex b = [vertex c[0], 0]
    B/      |A
    /        |                  A            B         C 
  /-------|                 ----- = ----- = -----  
a       C      b            	sin(a)    sin(b)   sin(c)
"""
from typing import List
import bpy
from math import sin
from mathutils import Vector

class FOtools_OT_Protractor(bpy.types.Operator):
  
    bl_idname = "mesh.protractor_angle"
    bl_label = "FOtools create protractor"
    bl_description = "creates an polytriangle with an set angle on the world origin point"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
      protractor_angle = bpy.context.scene.protractor_angle
      protractor_radius = bpy.context.scene.protractor_radius
  
      protractor_mesh = self.draw_protractor(protractor_angle, protractor_radius )
      return {"FINISHED"}
    
    
    def calculate_triangle_coordinates(self, angle_a: float, radius: float) -> Vector: 
     # calculates the coordinates of  the top vertex of the protractor with the given corner 'a' on the origin.
      angle_c = 90 - angle_a
      length_A = sin(angle_a) * radius
      length_C = sin(angle_c) * radius
      return [length_C, length_A]
    
    
    def draw_protractor(self, angle, radius):
      mesh = bpy.data.meshes.new("Triangle_Mesh")
      protractor_name = f"hoek_{angle}"
      
      vertex_c_coordinates = self.calculate_triangle_coordinates(protractor_angle, protractor_radius)
      
      #creer mesh-object
      obj = bpy.data.objects.new(protractor_name, mesh)
      bpy.context.collection.objects.link(obj)
      
      # define geometry data
      faces = [(0, 1, 2)]
      edges = []
      verts = [(0, 0, 0), (0, vertex_c_coordinates[0], 0), (0,  vertex_c_coordinates[0],  vertex_c_coordinates[1])]
      
      #draw geometry
      mesh_data = mesh.from_pydata(verts, edges, faces)
      mesh.update()
