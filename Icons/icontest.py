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

FOtools: a set of blender tools to assist in 3D-Forensic analysis Alexander de Bruijn 2024
'''

import os

import bpy
import bpy.utils.previews
from bpy.types import Panel


preview_collections = {}
dir = os.path.dirname(bpy.data.filepath)

pcoll = bpy.utils.previews.new()

for entry in os.scandir(dir):
    if entry.name.endswith(".png"):
        name = os.path.splitext(entry.name)[0]
        pcoll.load(name.upper(), entry.path, "IMAGE")


class VIEW3D_PT_test(Panel):
    bl_label = "TEST"
    bl_category = "TEST"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "use_gravity", text="Enable Layout")

        col = layout.column()
        col.enabled = scene.use_gravity
        col.operator("object.duplicate_move", text="Custom Icon", icon_value=pcoll["ICON"].icon_id)
        col.operator("object.duplicate_move", text="Built-in Icon", icon="OUTPUT")


bpy.utils.register_class(VIEW3D_PT_test)


#https://blender.stackexchange.com/questions/32335/how-to-implement-custom-icons-for-my-script-addon
'''
bl_info = {
    "name": "Custom Icon Test",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Tools",
    "description": "Test custom icons",
    "warning": "",
    "doc_url": "",
    "category": "Testing",
}

import os
import bpy
import bpy.utils.previews

class CUSTOM_PT_myPanel(bpy.types.Panel):
    bl_label = "My Icon Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        global custom_icons
        self.layout.label(text="Blender SE", icon_value=custom_icons["custom_icon"].icon_id)

# global variable to store icons in
custom_icons = None

def register():
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    addon_path =  os.path.dirname(__file__)
    icons_dir = os.path.join(addon_path, "icons")
    
    custom_icons.load("custom_icon", os.path.join(icons_dir, "icon.png"), 'IMAGE')
    bpy.utils.register_class(CUSTOM_PT_myPanel)

def unregister():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    bpy.utils.unregister_class(CUSTOM_PT_myPanel)

if __name__ == "__main__":
    # Test run
    # edit to folder containing your icons folder
    __file__ = "/home/user/Desktop/"
    # The path of this text (if saved)
    #__file__ = bpy.context.space_data.text.filepath
    # The path of this blend file (if saved)
    #__file__ = bpy.data.filepath
    register()


'''