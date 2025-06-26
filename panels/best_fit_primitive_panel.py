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

class FOTOOLS_PT_fit_panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport for fitting primitives"""
    bl_label = "Fit Primitives"
    bl_idname = "FOTOOLS_PT_fit_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOtools '

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.label(text="Fit to Selection:")
#       layout.operator("mesh.best_fit_line", text="Create Best Fit Line", icon="CURVE_BEZCURVE")

        layout.operator("fotools.fit_plane", text="create best fit plane")
        layout.operator("fotools.fit_sphere", text="create best fit plane")
        layout.operator("fotools.fit_cylinder", text="create best fit plane")
        #layout.operator("fotools.fit_box", text="create best fit box")
        #layout.operator("fotools.fit_cone", text="create best fit cone")
        #layout.operator("fotools.fit_torus", text="create best fit torus")
        #layout.operator("fotools.fit_line", text="create best fit line")
        #layout.operator("fotools.fit_circle", text="create best fit circle")
        #layout.operator("fotools.fit_3pcircle", text="create best fit 3pcircle")
        #layout.operator("fotools.fit_bwtarget", text="create best fit bw target")
 