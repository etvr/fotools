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
import bpy.utils.previews


class Backprojection_Panel(bpy.types.Panel):
    bl_label = "Trajectory Cone"
    bl_idname = "ETVR_PT_FOTools_Backprojection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category ="FOtools"

    bpy.types.Scene.impact_point = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.secondary_point = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.deflection_angle = bpy.props.FloatProperty( name="Cone deflection", description="Total uncertainty in degrees", min=0, max=360, default=5,)
    bpy.types.Scene.minimal_distance = bpy.props.FloatProperty( name="Min distance", description="Minimal distance in meters", min=0, max=5, default=0.25, )
    bpy.types.Scene.maximal_distance = bpy.props.FloatProperty( name="Max distance", description="Maximal_distance in meters", min=0, max=20, default=0.8, )
    bpy.types.Scene.total_length = bpy.props.FloatProperty( name="Total length", description="Total length in degrees ", min=1, max=50, default=10, )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        self.layout.prop_search(context.scene, "impact_point", context.scene, "objects", text="Impact Point" )
        self.layout.prop_search( context.scene, "secondary_point", context.scene, "objects", text="Secondary Point", )
        self.layout.separator_spacer()
        self.layout.prop(context.scene, "deflection_angle")
        self.layout.prop(context.scene, "minimal_distance")
        self.layout.prop(context.scene, "maximal_distance")
        self.layout.prop(context.scene, "total_length")
        self.layout.separator_spacer()
        self.layout.operator("mesh.deflection_cone", text="Create Deflection Cone", icon="CONE" )