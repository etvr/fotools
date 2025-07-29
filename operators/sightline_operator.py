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


# from typing import List
import bpy


class FOtools_OT_Sightlines(bpy.types.Operator):
  
  bl_idname = "mesh.sightline_analsis"
  bl_label = "FOtools sightlines"
  bl_description = "colors all sightlines from a given position"
  bl_options = {"UNDO"}


  @classmethod
  def poll(cls, context):
      return context.mode in {'OBJECT', 'EDIT_MESH'}


  def execute(self, context):
    fov_color = bpy.context.scene.fov_color
    self.draw_sightlines_fov(fov_color)
    return {"FINISHED"}
  
  def draw_sightlines_fov(self, fov_color):
    
    #setup renderer
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.preview_samples = 8
    bpy.context.scene.cycles.max_bounces = 0
    bpy.context.scene.cycles.use_preview_denoising = False
    
    #create pointlight
    bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    mylight  = bpy.context.active_object.data
    mylight.color = [fov_color[0], fov_color[1], fov_color[2]]
    
    #create shadernetwork
    mylight.use_nodes = True
    emission_node = mylight.node_tree.nodes["Emission"]
    falloff_node = mylight.node_tree.nodes.new(type="ShaderNodeLightFalloff")
    falloff_node.inputs[0].default_value = 5
    mylight.node_tree.links.new( falloff_node.outputs[1], emission_node.inputs[1] )
    mylight.node_tree.links.new( falloff_node.outputs[2], emission_node.inputs[0] )