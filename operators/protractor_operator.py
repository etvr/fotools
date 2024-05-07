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
#from typing import List
import bpy
from ..utils.protractor_helpers import calculate_triangle_coordinates, draw_polygon

class FOtools_OT_Protractor(bpy.types.Operator):
  
  
  bl_idname = "mesh.protractor_angle"
  bl_label = "FOtools create protractor"
  bl_description = "creates a polytriangle with a set angle on the world origin"
  bl_options = {"UNDO"}


  @classmethod
  def poll(cls, context):
    return True


  def execute(self, context):
    vertical_protractor_angle = bpy.context.scene.vertical_protractor_angle
    horizontal_protractor_angle = bpy.context.scene.horizontal_protractor_angle
    protractor_radius = bpy.context.scene.protractor_radius
    protractor_horizontal_mesh = self.draw_horizontal_protractor(horizontal_protractor_angle, protractor_radius )
    protractor_vertical_mesh = self.draw_vertical_protractor(vertical_protractor_angle, protractor_radius )
    frustum_mesh = self.draw_frustum(horizontal_protractor_angle, vertical_protractor_angle, protractor_radius)
    return {"FINISHED"}


  # def calculate_triangle_coordinates(self, angle_a: float, radius: float):
  #   # calculates the coordinates of  the top vertex of the protractor with the given corner 'a' on the origin.
  #   angle_c = 90.0 - (angle_a / 2.0)
  #   length_A = sin(radians(angle_a / 2.0)) * radius
  #   length_C = sin(radians(angle_c)) * radius
  #   #print (f"{length_C=}, {length_A=}, {angle_a=}, {radius=}")
  #   return [length_C, length_A]


  # def draw_polygon(self, vertices_array, faces_array, name):
  #   #creates a polygon shape based on an input of vertices and faces.
  #   mesh = bpy.data.meshes.new("Triangle_Mesh")
  #   obj = bpy.data.objects.new(name, mesh)
  #   bpy.context.collection.objects.link(obj)
  #   edges = []
  #   mesh_data = mesh.from_pydata(vertices_array, edges, faces_array)
  #   mesh.update()
  #   return obj
        
        
  def draw_horizontal_protractor(self, angle, radius):
    vertex_c = calculate_triangle_coordinates(angle, radius)
    faces = [(0, 1, 2)] #numbers refer to the index of its vertex in the vert array
    verts = [(0, 0, 0), (vertex_c[0], (vertex_c[1] * -1), 0), (vertex_c[0], vertex_c[1] , 0)]
    protractor_name = f"Angle_{angle}"
    obj = draw_polygon(verts, faces, protractor_name)
    return obj
  
  
  def draw_vertical_protractor(self, angle, radius):
    vertex_c = calculate_triangle_coordinates(angle, radius)
    faces = [(0, 1, 2)] #numbers refer to the index of its vertex in the vert array
    verts = [(0, 0, 0), (vertex_c[0], 0, (vertex_c[1] * -1)), (vertex_c[0], 0,vertex_c[1])]
    protractor_name = f"Angle_{angle}"
    obj = draw_polygon(verts, faces, protractor_name)
    return obj
  
  
  def draw_frustum(self, h_angle, v_angle, radius):
    h_coord  = calculate_triangle_coordinates(v_angle, radius)
    v_coord  = calculate_triangle_coordinates(h_angle,   radius)
    scalefactor = (h_coord[0] / v_coord[0]) 
    v_coord = (v_coord[0] * scalefactor, v_coord[1] * scalefactor)
    # define coordinates arra
    verts = [(0, 0, 0), 
             (h_coord[0], v_coord[1]*-1, h_coord[1] ), 
             (h_coord[0], v_coord[1]*-1, h_coord[1] * -1), 
             (h_coord[0], v_coord[1], h_coord[1] * -1), 
             (h_coord[0], v_coord[1], h_coord[1])]
    faces = [(0, 1, 4), (0, 4, 3), (0, 3, 2), (0, 1, 2)] 
    frustum_name = f"Frustum_{h_angle}_x_{v_angle}"
    obj = draw_polygon(verts, faces, frustum_name)  
    return obj
  
