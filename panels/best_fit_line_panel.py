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

class BestFitLinePanel(bpy.types.Panel):
    bl_label = "Best Fit Line"
    bl_idname = "ETVR_PT_FOTools_BestFitLine"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "edit_mesh"
    bl_category = "FOtools"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.operator("mesh.best_fit_line", text="Create Best Fit Line", icon="CURVE_BEZCURVE")
        layout.separator_spacer()
        layout.label(text="Select vertices to create a best fit line.")