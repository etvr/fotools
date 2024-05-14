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


#from typing import List
import bpy
from ..utils.protractor_helpers import calculate_triangle_coordinates, draw_polygon

class FOtools_OT_Protractor(bpy.types.Operator):
  
  bl_idname = "mesh.protractor_angle"
  bl_label = "FOtools draw protractor angle"
  bl_description = "creates a polytriangle with a set angle on the world origin"
  bl_options = {"UNDO"}


  @classmethod
  def poll(cls, context):
    return True


  def execute(self, context):
    vertical_protractor_angle = bpy.context.scene.vertical_protractor_angle
    horizontal_protractor_angle = bpy.context.scene.horizontal_protractor_angle
    protractor_radius = bpy.context.scene.protractor_radius
    

    self.draw_horizontal_protractor(horizontal_protractor_angle, protractor_radius )
    self.draw_vertical_protractor(vertical_protractor_angle, protractor_radius )
    return {"FINISHED"}
        
        
  def draw_horizontal_protractor(self, angle, radius):
    print(f" test{angle=} {radius=}")
    vertex_c = calculate_triangle_coordinates(self, angle, radius)
    faces = [(0, 1, 2)] #numbers refer to the index of its vertex in the vert array
    
    verts = [
            (0, 0, 0), 
            (vertex_c[0], (vertex_c[1] * -1), 0), 
            (vertex_c[0], vertex_c[1] , 0)]
    
    protractor_name = f"Angle_{angle}"
    obj = draw_polygon(self, verts, faces, protractor_name)
    return obj
  
  
  def draw_vertical_protractor(self, angle, radius):
    vertex_c = calculate_triangle_coordinates(self, angle, radius)
    faces = [(0, 1, 2)] #numbers refer to the index of its vertex in the vert array
    
    verts = [
            (0, 0, 0), 
            (vertex_c[0], 0, (vertex_c[1] * -1)), 
            (vertex_c[0], 0,vertex_c[1])]
    
    protractor_name = f"Angle_{angle}"
    obj = draw_polygon(self, verts, faces, protractor_name)
    return obj
    
  
  def draw_protractor(self, angle_h, angle_v, radius):
    
    #scalefactor = (1 / v_coord[0]) 
    #vertex_c_h = (vertex_c_h[0] * scalefactor, vertex_c_h[1] * scalefactor)
    
    vertices_h_v = [[],[]]
    faces = [(0, 1, 2)]
    
    if angle_h > 0:
      vertex_c_h = calculate_triangle_coordinates(self, angle, radius)
      scalefactor = (radius / vertex_c_h[0]) 
      vertex_c_h = (vertex_c_h[0] * scalefactor, vertex_c_h[1] * scalefactor)
      vertices_h_v[0] = [
              (0, 0, 0), 
              (vertex_c_h[0], (vertex_c_h[1] * -1), 0), 
              (vertex_c_h[0], vertex_c_h[1] , 0), 
              f"Angle_{angle_h}"]
              
    if angle_v > 0:    
      vertex_c_v = calculate_triangle_coordinates(self, angle, radius)
      scalefactor = (radius / vertex_c_h[0]) 
      vertex_c_v = (vertex_c_v[0] * scalefactor, vertex_c_v[1] * scalefactor)
      vertices_h_v[1] = [
              (0, 0, 0), 
              (vertex_c_v[0], 0, (vertex_c_v[1] * -1)), 
              (vertex_c_v[0], 0,vertex_c_v[1]), 
              f"Angle_{angle_h}"]
    for item in vertices_h_v:
      if  item:
        protractor_name = item[3]
        draw_polygon(self, [item[0],item[1],item[2]], faces, protractor_name)