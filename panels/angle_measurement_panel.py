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
    bl_label = "Draw Angle Measuremnet"
    bl_idname = "FOTOOLS_PT_angle_measurement"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOtools'

    # Define property on the scene so it's persistent and accessible
    bpy.types.Scene.fotools_angle_label_size = bpy.props.FloatProperty(
        name="Label Size",
        description="Size of the angle measurement text label",
        default=0.1,
        min=0.001,
        unit='LENGTH'
    )

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        col = layout.column(align=True)
        col.label(text="Select 3 objects.")
        col.label(text="Active object is the vertex.")
        
        # The operator button will be automatically greyed out
        # if its poll() method returns False.
        col.operator("fotools.measure_angle", text="Measure Angle", icon='CON_TRACKTO')
        col.prop(scene, "fotools_angle_label_size")