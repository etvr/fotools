'''
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
'''

import bpy

class Protractor_Panel(bpy.types.Panel):
    bl_label = "Protractor tool"
    bl_idname = "ETVR_PT_FO_protractor_tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "FOtools"

    bpy.types.Scene.protractor_angle = bpy.props.FloatProperty( name="Angle Degree", description=" Angle for the to be drawn polygon", min=0, max=360, default=45,)
    bpy.types.Scene.protractor_radius = bpy.props.FloatProperty( name="Protractor Radius", description=" Radius of the drawn polygon", min=0, max=100, default=1,)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        self.layout.prop(context.scene, "protractor_angle")
        self.layout.prop(context.scene, "protracor_radius")
        self.layout.operator("mesh.protractor_angle", text="Create Protractor Angle", icon="CONE")

