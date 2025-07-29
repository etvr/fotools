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

class FOtools_OT_GeonodePointcloud(bpy.types.Operator):
    bl_idname ="mesh.pointcloud_as_geonode"
    bl_label = "FOtools, draw a pointcloud as geonodes"
    bl_description = "converts an imported PLY pointcloud to a geonode mesh with a color shader network"
    bl_options = {"UNDO"}
    
    @classmethod
    def poll(cls, context):
     return True

    
    def execute(self, context):
        MESH_POINT_SIZE = 0.02
        self.create_material("pointcloud_mat")
        self.create_geo_nodes("pointcloud_mat", MESH_POINT_SIZE)
        self.adjust_render_settings()
        return {"FINISHED"}
    
    def adjust_render_settings(self):
        bpy.ops.object.shade_smooth()
        bpy.context.space_data.shading.type = 'MATERIAL'


    def create_material(self, name):
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]
        
        #add col as given attribute Name
        attribute_node=material.node_tree.nodes.new(type="ShaderNodeAttribute")
        attribute_node.attribute_name = "Col"
        material.node_tree.links.new(attribute_node.outputs["Color"], principled_bsdf_node.inputs["Base Color"])
        return material


    def create_node(self, node_tree, type_name, node_x_location, node_location_step_x=0):
        """Creates a node of a given type, and sets/updates the location of the node on the X axis.
        Returning the node object and the next location on the X axis for the next node.
        """
        node_obj = node_tree.nodes.new(type=type_name)
        node_obj.location.x = node_x_location
        node_x_location += node_location_step_x
        return node_obj, node_x_location


    def create_geo_nodes(self, name, mesh_point_size):
        node_x_location = 0
        node_location_step_x = 200

        pointcloud_object = bpy.context.active_object
        bpy.ops.node.new_geometry_nodes_modifier()
        geo_node_tree = bpy.data.node_groups["Geometry Nodes"]
        in_node = geo_node_tree.nodes['Group Input']
        out_node = geo_node_tree.nodes["Group Output"]
        
        mesh_to_points_node,node_x_location = self.create_node(geo_node_tree,"GeometryNodeMeshToPoints",node_x_location, node_location_step_x)
        mesh_to_points_node.inputs[3].default_value = mesh_point_size
        set_material_node, node_x_location = self.create_node(geo_node_tree,"GeometryNodeSetMaterial",node_x_location, node_location_step_x)
        set_material_node.inputs[2].default_value = bpy.data.materials[name]
        out_node.location.x =node_x_location
        
        geo_node_tree.links.new(in_node.outputs["Geometry"], mesh_to_points_node.inputs["Mesh"])
        geo_node_tree.links.new(mesh_to_points_node.outputs["Points"], set_material_node.inputs['Geometry'])
        geo_node_tree.links.new(set_material_node.outputs['Geometry'], out_node.inputs['Geometry'])