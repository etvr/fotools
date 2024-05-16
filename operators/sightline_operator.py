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


class FOtools_OT_Sightlines(bpy.types.Operator):
  
  bl_idname = "mesh.sightline_analsis"
  bl_label = "FOtools sightlines"
  bl_description = "colors all sightlines from a given position"
  bl_options = {"UNDO"}


  @classmethod
  def poll(cls, context):
    return True


  def execute(self, context):
    pass
    return {"FINISHED"}
  
  
  
  '''
  
  set to cycles
  light falloff                                          emission                     light output
                      - linear-------color       - emission--------------surface
  
                      - constant---strength
  
  
 1: bpy.context.scene.render.engine = 'CYCLES'
 2:  bpy.context.scene.cycles.device = 'GPU'
 3: bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
 4: bpy.context.object.data.use_nodes = True
 5:  bpy.ops.node.add_node(use_transform=True, type="ShaderNodeLightFalloff")
 6:
 7: 
 8: bpy.data.lights["Point.001"].node_tree.nodes["Light Falloff"].inputs[0].default_value = 11

  
  '''