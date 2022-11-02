'''
Copyright (C) 2022 Alexander de Bruijn

Created by Alexander de Bruijn 2022

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

class Field_of_view_Panel(bpy.types.Panel):
    bl_label = "Field of view"
    bl_idname = "ETVR_PT_FOtools_Field_of_view"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category ="FOtools"
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        row = layout.row()
        row.label(text="Visualizes the FOV from a given point.")
