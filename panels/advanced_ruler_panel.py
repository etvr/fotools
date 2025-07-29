import bpy
 
class FOTOOLS_PT_AdvancedRulerPanel(bpy.types.Panel):
    """Creates a panel for the advanced ruler tool."""
    bl_label = "Draw Ruler"
    bl_idname = "FOTOOLS_PT_advanced_ruler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FOtools'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Operator properties
        col.prop(context.scene, "advanced_ruler_thickness", text="Thickness")
        col.prop(context.scene, "advanced_ruler_width", text="Width")
        col.prop(context.scene, "advanced_ruler_tick_interval", text="Tick Interval")
        col.prop(context.scene, "advanced_ruler_font_size", text="Font Size")

        # Draw Ruler Button
        col.operator("fotools.advanced_draw_ruler", text="Draw Ruler")

# Register scene properties for the panel
bpy.types.Scene.advanced_ruler_thickness = bpy.props.FloatProperty(
    name="Ruler Thickness",
    description="Thickness of the ruler",
    default=0.01,
    min=0.001
)

bpy.types.Scene.advanced_ruler_width = bpy.props.FloatProperty(
    name="Ruler Width",
    description="Width of the ruler",
    default=0.1,
    min=0.01
)

bpy.types.Scene.advanced_ruler_tick_interval = bpy.props.FloatProperty(
    name="Tick Interval",
    description="Distance between tick marks",
    default=0.1,
    min=0.01
)

bpy.types.Scene.advanced_ruler_font_size = bpy.props.FloatProperty(
    name="Font Size",
    description="Size of the font for labels",
    default=0.05,
    min=0.01
)