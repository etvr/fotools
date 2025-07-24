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

class FOTOOLS_PT_AngleMeasurementPanel(bpy.types.Panel):
    """Creates a Panel in the FOTools Tab"""
    bl_label = "Angle Measurement"
    bl_idname = "FOTOOLS_PT_angle_measurement"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOTools'

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Select 3 objects.")
        col.label(text="Active object is the vertex.")
        
        # The operator button will be automatically greyed out
        # if its poll() method returns False.
        col.operator("fotools.measure_angle", text="Measure Angle", icon='CON_TRACKTO')