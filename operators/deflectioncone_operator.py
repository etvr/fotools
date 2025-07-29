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

from math import tan, radians
from mathutils import Vector, Matrix
from typing import List
from ..utils.add_material import newShader
from ..utils.bool_cut import radius_cut
from ..utils.aim_towards import aim_object_to


class FOtools_OT_DeflectionCone(bpy.types.Operator):
    bl_idname = "mesh.deflection_cone"
    bl_label = "FOtools Deflectioncone"
    bl_description = "Creates a cone with an user-given angle and length along the extension of two objects"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def create_section_materials(self):
        mat_red = newShader("fotools_red", "diffuse", 1, 0, 0)
        mat_yellow = newShader("fotools_yellow", "diffuse", 1, 1, 0)
        mat_blue = newShader("fotools_blue", "diffuse", 0, 0, 1)
        return (mat_red, mat_yellow, mat_blue)

    def add_deflection_cone(
            self, cone_deflection_degrees: float,
            cone_length_meters: float,
            radius_min: float,
            radius_max: float,
            impact_point: object,
            secondary_point: object
    ) -> object:

        if (cone_deflection_degrees != 0):
            deflection_radius_size = self.calculate_deflection_radius(
                cone_deflection_degrees,
                cone_length_meters
            )
            bpy.ops.mesh.primitive_cone_add(
                radius1=deflection_radius_size,
                radius2=0,
                vertices=64,
                depth=cone_length_meters,
                align="WORLD",
                end_fill_type="TRIFAN",
                enter_editmode=False,
                scale=(1, 1, 1),
                location=(impact_point.location)
            )
            deflectioncone = bpy.context.active_object
        else:
            #draw a straight line
            bpy.ops.mesh.primitive_cone_add(
                radius1=0.009,
                radius2=0.009,
                depth=cone_length_meters,
                align="WORLD",
                end_fill_type="TRIFAN",
                enter_editmode=False,
                scale=(1, 1, 1),
                location=(impact_point.location)
            )
            deflectioncone = bpy.context.active_object
            
        aim_object_to(deflectioncone, secondary_point)   
        self.set_origin(bpy.context.object,self.get_cone_top_vertex_coordinate())
        deflectioncone.location = secondary_point.location
        return deflectioncone

    def get_vertex_world_coordinates(self, obj) -> List[Vector]:
        # multiply local vertex coordinate with object world matrix to get world coordinates
        world_coords = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
        return world_coords

    def get_cone_top_vertex_coordinate(self) -> Vector:
        #for a cone  the first vertex refers to the top coordinates
        active_selection = bpy.context.active_object
        cone_world_coordinates = self.get_vertex_world_coordinates(
            active_selection)
        return cone_world_coordinates[-1]

    def set_origin(self, object, global_origin=Vector()) -> None:
        mw = object.matrix_world
        o = mw.inverted() @ Vector(global_origin)
        object.data.transform(Matrix.Translation(-o))

    def calculate_deflection_radius(self, degrees: float, length: float) -> float:
        deflection_radius = length * tan(radians(degrees)/2.0)
        return deflection_radius

    def execute(self, context):
        min_distance = bpy.context.scene.minimal_distance
        max_distance = bpy.context.scene.maximal_distance
        cone_length = bpy.context.scene.total_length
        deflection_angle = bpy.context.scene.deflection_angle
        impact_point = bpy.context.scene.impact_point
        secondary_point = bpy.context.scene.secondary_point
        fotools_materials = self.create_section_materials()
        deflectioncone = self.add_deflection_cone(
            deflection_angle, 
            cone_length,
            min_distance, 
            max_distance, 
            impact_point, 
            secondary_point
            )
        
        #outside minimal radius
        intermediate_results = radius_cut(deflectioncone, min_distance, secondary_point)
        outside_min_radius_cone = intermediate_results[0]
        outside_min_radius_cone.name = f'Cone_outside_minimal_radius'
        outside_min_radius_cone.data.materials.append(fotools_materials[1])
        
        #outside maximal radius
        intermediate_results = radius_cut(intermediate_results[1], max_distance, secondary_point)
        outside_max_radius_cone = intermediate_results[1]
        outside_max_radius_cone.name = f'Cone_outside_max_radius'
        outside_max_radius_cone.data.materials.append(fotools_materials[1])
        
        #inside radius
        inside_min_max_radius_cone = intermediate_results[0]
        inside_min_max_radius_cone.name = f'Cone_inside_radius'
        inside_min_max_radius_cone.data.materials.append(fotools_materials[0])

        return {"FINISHED"}