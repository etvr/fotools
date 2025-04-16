import bpy
from bpy_extras.io_utils import ImportHelper


class FOtools_OT_ImportPLY(bpy.types.Operator, ImportHelper):
    bl_idname = "fotools.import_ply_pointcloud"
    bl_label = "Import PLY"
    bl_description = "Import a PLY pointcloud file"
    
    filename_ext = ".ply"
    filter_glob: bpy.props.StringProperty( default="*.ply", options={'HIDDEN'})
    def execute(self, context):
        bpy.ops.wm.ply_import(filepath=self.filepath)
        return {'FINISHED'}