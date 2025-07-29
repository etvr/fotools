import bpy

class FOTOOLS_PT_fit_panel(bpy.types.Panel):
    """Creates a Panel in the Viewport N panel"""
    bl_label = "Fit Primitives"
    bl_idname = "FOTOOLS_PT_fit"
    bl_space_type = 'VIEW_3D'
    bl_category = "FOtools"
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT' and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout

        obj = context.active_object

        layout.label(text="Fit to Selection:")
        layout.label(text="APPLY ALL TRANSFORMS BEFORE FITTING")

        # Plane fitting
        layout.operator("fotools.fit_plane")

        # Line fitting
        layout.operator("fotools.fit_line")

        # Sphere fitting
        layout.operator("fotools.fit_sphere")

        # Cylinder fitting
        layout.operator("fotools.fit_cylinder")

        # Circle fitting with segments property
        layout.row().operator("fotools.fit_circle").segments = 32  # Default segments value


def register():
    bpy.utils.register_class(FOTOOLS_PT_fit_panel)


def unregister():
    bpy.utils.unregister_class(FOTOOLS_PT_fit_panel)