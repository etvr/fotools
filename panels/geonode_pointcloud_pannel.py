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


class Geonode_pointcloud_Panel(bpy.types.Panel):
    bl_label = "PLY-pointcloud to Geonodes"
    bl_idname = "ETVR_PT_FOtools_geonode_pointcloud"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "objectmode"
    bl_category ="FOtools"
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        row = layout.row()
        row.label(text="import a pointcloud .PLY file and make sure it is selected.  Pointsize is settable in the geometry node editor on the top level of the ply object,")
        self.layout.separator_spacer()
        self.layout.operator("fotools.import_ply_pointcloud", text="Import PLY File", icon="FILEBROWSER")
        self.layout.operator("mesh.pointcloud_as_geonode", text="Create pointcloud as geonodes", icon="HIDE_OFF")
