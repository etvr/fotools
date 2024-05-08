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

class FOtools_OT_Frustum(bpy.types.Operator):
  
  bl_idname = "mesh.draw_frustum"
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
    self.draw_frustum(horizontal_protractor_angle, vertical_protractor_angle, protractor_radius)
    return {"FINISHED"}
        
  
  def draw_frustum(self, h_angle, v_angle, radius):
    h_coord  = calculate_triangle_coordinates(self, v_angle, radius) #switch these names
    v_coord  = calculate_triangle_coordinates(self, h_angle,   radius)
    scalefactor = (h_coord[0] / v_coord[0]) 
    v_coord = (v_coord[0] * scalefactor, v_coord[1] * scalefactor)
    # define coordinates 
    verts = [
              (0, 0, 0), 
             (h_coord[0], v_coord[1]*-1, h_coord[1] ), 
             (h_coord[0], v_coord[1]*-1, h_coord[1] * -1), 
             (h_coord[0], v_coord[1], h_coord[1] * -1), 
             (h_coord[0], v_coord[1], h_coord[1])]
    faces = [
            (0, 1, 4), 
            (0, 4, 3), 
            (0, 3, 2), 
            (0, 1, 2)] 
    frustum_name = f"Frustum_{h_angle}_x_{v_angle}"
    obj = draw_polygon(self, verts, faces, frustum_name)  
    return obj
