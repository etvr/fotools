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

class Sightline_analysis_pannel(bpy.types.Panel):
    bl_label = "Project Sightline"
    bl_idname = "ETVR_PT_FOtools_Sightline_analysis"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "objectmode"
    bl_category ="FOtools"
    
    bpy.types.Scene.fov_color = bpy.props.FloatVectorProperty(
                                 name = "FOV Color",
                                 subtype = "COLOR",
                                 size = 4,
                                 min = 0.0,
                                 max = 1.0,
                                 default = (1.0,1.0,1.0,1.0))
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        row = layout.row()
        row.label(text="Visualizes the FOV from a given point.")
        self.layout.prop(context.scene, "fov_color")
        layout.separator_spacer()
        layout.operator("mesh.sightline_analsis", text="Create Viewpoint", icon="HIDE_OFF" ) 
  
