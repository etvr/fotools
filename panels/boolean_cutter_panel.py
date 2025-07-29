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

class Boolcut_Panel(bpy.types.Panel):
    
    bl_label = "Bool Slice"
    bl_idname = "ETVR_PT_FOtools_Bool_Cut"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category ="FOtools"

    bpy.types.Scene.to_be_cut = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.knife_object = bpy.props.PointerProperty(type=bpy.types.Object)

    @classmethod
    def poll(cls, context):
        # Show panel in both Object Mode and Edit Mode (for meshes)
        return context.mode in {'OBJECT', 'EDIT_MESH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        layout.label(text="Select two mesh objects")
        layout.prop_search(context.scene, "to_be_cut", context.scene, "objects", text="Object to be cut" )
        layout.prop_search( context.scene, "knife_object", context.scene, "objects", text="Cutter Object", )
        layout.separator_spacer()
        layout.operator("mesh.bool_cut", text="Cut Object", icon="ORPHAN_DATA" ) 
        
        '''
        row = layout.row()
        row.label(text="Select two mesh objects")
        row = layout.row()
        row.prop_search(context.scene, "to_be_cut", context.scene, "objects", text="Object to be cut" )
        row = layout.row()
        row.prop_search( context.scene, "knife_object", context.scene, "objects", text="Cutter Object", )
        row.separator_spacer()
        row = layout.row() 
        row.operator("mesh.bool_cut", text="Cut Object", icon="ORPHAN_DATA" ) 
        '''