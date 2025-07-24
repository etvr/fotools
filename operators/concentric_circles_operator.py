'''
Created by Alexander de Bruijn 2025,


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

FOtools: a set of blender tools to assist in 3D-Forensic analysis
This file contains the operator to create concentric circles.
'''

import bpy
from math import radians

class FOTOOLS_OT_concentric_circles(bpy.types.Operator):
    """Create 10 concentric circles around the active object"""
    bl_idname = "fotools.create_concentric_circles"
    bl_label = "Create Concentric Circles"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # This operator should only be active in Object Mode with an active object
        return context.active_object is not None and context.mode == 'OBJECT'

    def execute(self, context):
        target_obj = context.active_object
        if not target_obj:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

        center_location = target_obj.location
        
        # Create a parent empty to group the circles and labels
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=center_location)
        parent_empty = context.active_object
        parent_empty.name = "Concentric_Circles_Group"

        num_circles = 10
        start_radius = 1.0
        radius_step = 1.0

        for i in range(num_circles):
            radius = start_radius + (i * radius_step)

            # Create the circle
            bpy.ops.mesh.primitive_circle_add(
                vertices=64, 
                radius=radius, 
                fill_type='NOTHING', 
                align='WORLD', 
                location=center_location
            )
            circle_obj = context.active_object
            circle_obj.name = f"Circle_Radius_{int(radius)}"
            circle_obj.parent = parent_empty

            # Create the label
            label_location = (center_location.x + radius, center_location.y, center_location.z)
            bpy.ops.object.text_add(location=label_location)
            label_obj = context.active_object
            label_obj.name = f"Label_Radius_{int(radius)}"
            label_obj.data.body = str(int(radius))
            label_obj.data.align_x = 'CENTER'
            label_obj.data.align_y = 'CENTER'
            label_obj.rotation_euler.x = radians(90) # Rotate to be flat on XY plane
            label_obj.parent = parent_empty

        # Restore original selection
        context.view_layer.objects.active = target_obj
        target_obj.select_set(True)
        parent_empty.select_set(False)

        self.report({'INFO'}, f"Created {num_circles} concentric circles around '{target_obj.name}'")
        return {'FINISHED'}