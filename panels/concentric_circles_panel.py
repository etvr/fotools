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

FOtools: a set of blender tools to assist in 3D-Forensic analysis Alexander de Bruijn 2025
'''

import bpy

class FOTOOLS_PT_concentric_circles(bpy.types.Panel):
    """Creates a Panel in the FO-Tools Tab"""
    bl_label = "Concentric Circles"
    bl_idname = "FOTOOLS_PT_concentric_circles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FO-Tools"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select an object as the center:")
        layout.operator("fotools.create_concentric_circles", text="Create Circles", icon="MESH_CIRCLE")