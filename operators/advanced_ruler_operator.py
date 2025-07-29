import bpy
import bmesh
from mathutils import Vector
import math
from ..utils import add_material

class FOTOOLS_OT_AdvancedDrawRuler(bpy.types.Operator):
    """Draws an advanced ruler between two selected objects with tick marks and labels."""
    bl_idname = "fotools.advanced_draw_ruler"
    bl_label = "Advanced Draw Ruler"
    bl_options = {'REGISTER', 'UNDO'}

    ruler_thickness: bpy.props.FloatProperty(
        name="Ruler Thickness",
        description="Thickness of the ruler",
        default=0.01,
        min=0.001
    )

    ruler_width: bpy.props.FloatProperty(
        name="Ruler Width",
        description="Width of the ruler",
        default=0.1,
        min=0.01
    )

    tick_interval: bpy.props.FloatProperty(
        name="Tick Interval",
        description="Distance between tick marks",
        default=0.1,
        min=0.01
    )

    font_size: bpy.props.FloatProperty(
        name="Font Size",
        description="Size of the font for labels",
        default=0.035,
        min=0.001
    )

    label_offset_x: bpy.props.FloatProperty(
        name="Label Offset X",
        description="Offset of the labels in the X direction",
        default=-0.00,
    )

    label_offset_y: bpy.props.FloatProperty(
        name="Label Offset Y",
        description="Offset of the labels in the Y direction",
        default=0.02,
    )

    label_offset_z: bpy.props.FloatProperty(
        name="Label Offset Z",
        description="Offset of the labels in the Z direction",
        default=0.00,
    )




    tick_color: bpy.props.FloatVectorProperty(
        name="Tick Color",
        description="Color of the tick marks (RGB)",
        default=(0.0, 0.0, 0.0),  # Black color
        min=0.0,
        max=1.0,
        subtype='COLOR',
        size=3
    )





    def execute(self, context):
        # Get selected objects
        selected_objects = context.selected_objects

        if len(selected_objects) != 2:
            self.report({'ERROR'}, "Select exactly two objects.")
            return {'CANCELLED'}

        obj1, obj2 = selected_objects[0], selected_objects[1]
        start_point = obj1.location
        end_point = obj2.location

        # Calculate ruler length and direction
        ruler_length = (end_point - start_point).length
        ruler_direction = (end_point - start_point).normalized()

        # Create mesh data for the ruler
        mesh = bpy.data.meshes.new("AdvancedRulerMesh")
        obj = bpy.data.objects.new("AdvancedRuler", mesh)
        context.collection.objects.link(obj)

        bm = bmesh.new()



        # Create base ruler vertices (rectangle)
        width = self.ruler_width
        thickness = self.ruler_thickness
        start_normal = Vector((0, 0, 1))  # Upward direction
        start_binormal = ruler_direction.cross(start_normal).normalized()


        v1 = bm.verts.new(start_point - start_binormal * (width / 2) - start_normal * thickness)
        v2 = bm.verts.new(start_point + start_binormal * (width / 2) - start_normal * thickness)
        v3 = bm.verts.new(end_point + start_binormal * (width / 2) - start_normal * thickness)
        v4 = bm.verts.new(end_point - start_binormal * (width / 2) - start_normal * thickness)

        # # Create faces for the ruler
        bm.faces.new((v1, v2, v3, v4))  # Bottom face

        # Update mesh
        bm.to_mesh(mesh)
        bm.free()

        # Create tick marks and labels
        tick_interval = self.tick_interval
        font_size = self.font_size
        num_ticks = int(ruler_length / tick_interval)

        for i in range(0, num_ticks+1):
            tick_position = start_point + ruler_direction * (i * tick_interval)

            # Create mesh data for the tick
            tick_mesh = bpy.data.meshes.new(f"AdvancedRulerTickMesh_{i}")
            tick_obj = bpy.data.objects.new(f"AdvancedRulerTick_{i}", tick_mesh)
            context.collection.objects.link(tick_obj)

            tick_width = self.tick_interval
            tick_start_binormal = ruler_direction.cross(start_normal).normalized()
            tick_offset = thickness/2 + 0.001 #to put it on top of the ruler

            tick_height = width / 3  # Height of the tick
            
            bm_tick = bmesh.new()

            # Create vertices for the tick mark (block), move it on top of the ruler
            tick_v1 = bm_tick.verts.new(tick_position - tick_start_binormal * (width / 2) - start_normal * (thickness/2))
            tick_v2 = bm_tick.verts.new(tick_position + tick_start_binormal * (width / 2) - start_normal * (thickness/2))
            tick_v3 = bm_tick.verts.new(tick_position + tick_start_binormal * tick_height / 2 + start_normal * (thickness/2))
            tick_v4 = bm_tick.verts.new(tick_position - tick_start_binormal * tick_height / 2 + start_normal * (thickness/2))

            tick_position = start_point + ruler_direction * ((i+1) * tick_interval)
            tick_v5 = bm_tick.verts.new(tick_position - tick_start_binormal * (width / 2) - start_normal * (thickness/2))
            tick_v6 = bm_tick.verts.new(tick_position + tick_start_binormal * (width / 2) - start_normal * (thickness/2))
            tick_v7 = bm_tick.verts.new(tick_position + tick_start_binormal * tick_height / 2 + start_normal * (thickness/2))
            tick_v8 = bm_tick.verts.new(tick_position - tick_start_binormal * tick_height / 2 + start_normal * (thickness/2))
     
            bm_tick.faces.new((tick_v1, tick_v2, tick_v6, tick_v5))
            #bm_tick.faces.new((tick_v3, tick_v4, tick_v8, tick_v7))

            
            # Update tick mesh
            bm_tick.to_mesh(tick_mesh)
            bm_tick.free()

            # Assign material to tick mark based on index parity
            if i % 2 == 0:  # Even ticks are white
                tick_mat_name = "Tick_White_Mat"
                tick_mat = bpy.data.materials.get(tick_mat_name) or add_material.newMaterial(name=tick_mat_name)
                tick_mat.diffuse_color = (1.0, 1.0, 1.0, 1)  # White
                tick_obj.data.materials.append(tick_mat)
            else:  # Odd ticks are black
                tick_mat_name = "Tick_Black_Mat"
                tick_mat = bpy.data.materials.get(tick_mat_name) or add_material.newMaterial(name=tick_mat_name)
                tick_mat.diffuse_color = (0.0, 0.0, 0.0, 1)  # Black
                tick_obj.data.materials.append(tick_mat)

            


            # Create text label for the tick 
            # Set text properties (color)
            r, g, b = 0.5, 0.5, 0.5  # Gray color

            text_curve = bpy.data.curves.new(name=f"RulerTickLabel_{i}", type='FONT')
            text_curve.body = f"{i * tick_interval:.1f}"
            text_mat = add_material.newMaterial(name=f"TickLabel_Mat_{i}")
            text_mat.diffuse_color = (r, g, b, 1)
            text_curve.materials.append(text_mat)
            text_curve.size = self.font_size
            text_curve.align_x = 'CENTER'

            tick_position = start_point + ruler_direction * ((i) * tick_interval)

            label_obj = bpy.data.objects.new(name=f"RulerTickLabelObj_{i}", object_data=text_curve)
#           label_obj.location = tick_position + start_normal * (thickness/2 + font_size) # Position label slightly above the ruler
            label_obj.location = tick_position + start_normal * (font_size /2) + Vector((self.label_offset_x, self.label_offset_y, self.label_offset_z))# Position label slightly above the ruler


            label_obj.rotation_euler = Vector((0, 0, math.atan2(ruler_direction.y, ruler_direction.x)))  # Align label with ruler direction

            context.collection.objects.link(label_obj)

        return {'FINISHED'}