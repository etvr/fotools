'''
Created by Alexander de Bruijn 2025,

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

FOtools: a set of blender tools to assist in 3D-Forensic analysis
This file contains operators to fit primitive shapes to vertex selections.
'''
import bpy
import bmesh
import numpy as np
from mathutils import Vector

def get_selected_world_verts(context):
    """
    Gets the selected vertices from the active edit-mode mesh and returns
    their coordinates in world space.
    """
    obj = context.edit_object
    if not obj or obj.type != 'MESH':
        return None, "Active object is not a mesh."

    bm = bmesh.from_edit_mesh(obj.data)
    selected_verts = [v for v in bm.verts if v.select]

    if not selected_verts:
        return None, "No vertices selected."

    world_matrix = obj.matrix_world
    world_coords = [world_matrix @ v.co for v in selected_verts]

    return world_coords, None


class FOTOOLS_OT_fit_plane(bpy.types.Operator):
    """Best-fit a plane to the selected vertices using PCA"""
    bl_idname = "fotools.fit_plane"
    bl_label = "Fit Plane"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'EDIT' and context.active_object.type == 'MESH'

    def execute(self, context):
        original_obj_name = context.edit_object.name
        world_coords, error_msg = get_selected_world_verts(context)
        if error_msg:
            self.report({'WARNING'}, error_msg)
            return {'CANCELLED'}

        if len(world_coords) < 3:
            self.report({'WARNING'}, "Need at least 3 vertices to fit a plane.")
            return {'CANCELLED'}

        points = np.array([v.to_tuple() for v in world_coords])
        centroid = np.mean(points, axis=0)
        points_centered = points - centroid
        covariance_matrix = np.cov(points_centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

        # The normal of the plane is the eigenvector with the smallest eigenvalue
        normal_vec = eigenvectors[:, np.argmin(eigenvalues)]

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=centroid)

        new_plane = context.active_object
        rot_quat = Vector(normal_vec).to_track_quat('Z', 'Y')
        new_plane.rotation_euler = rot_quat.to_euler()

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted plane to {len(world_coords)} vertices.")
        return {'FINISHED'}


class FOTOOLS_OT_fit_sphere(bpy.types.Operator):
    """Best-fit a sphere to the selected vertices"""
    bl_idname = "fotools.fit_sphere"
    bl_label = "Fit Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'EDIT' and context.active_object.type == 'MESH'

    def execute(self, context):
        original_obj_name = context.edit_object.name
        world_coords, error_msg = get_selected_world_verts(context)
        if error_msg:
            self.report({'WARNING'}, error_msg)
            return {'CANCELLED'}

        if len(world_coords) < 2:
            self.report({'WARNING'}, "Need at least 2 vertices to fit a sphere.")
            return {'CANCELLED'}

        centroid = sum(world_coords, Vector()) / len(world_coords)
        radius = sum((v - centroid).length for v in world_coords) / len(world_coords)

        if radius < 1e-6:
            self.report({'WARNING'}, "Cannot create sphere with zero radius.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, align='WORLD', location=centroid)

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted sphere to {len(world_coords)} vertices.")
        return {'FINISHED'}


class FOTOOLS_OT_fit_cylinder(bpy.types.Operator):
    """Best-fit a cylinder to the selected vertices using PCA"""
    bl_idname = "fotools.fit_cylinder"
    bl_label = "Fit Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'EDIT' and context.active_object.type == 'MESH'

    def execute(self, context):
        original_obj_name = context.edit_object.name
        world_coords, error_msg = get_selected_world_verts(context)
        if error_msg:
            self.report({'WARNING'}, error_msg)
            return {'CANCELLED'}

        if len(world_coords) < 3:
            self.report({'WARNING'}, "Need at least 3 vertices to fit a cylinder.")
            return {'CANCELLED'}

        points = np.array([v.to_tuple() for v in world_coords])
        centroid_np = np.mean(points, axis=0)
        points_centered = points - centroid_np
        covariance_matrix = np.cov(points_centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

        # The axis of the cylinder is the eigenvector with the largest eigenvalue
        axis_vec = Vector(eigenvectors[:, np.argmax(eigenvalues)]).normalized()

        # Calculate radius by finding the average distance from the axis
        radii = [np.linalg.norm(p - p.dot(axis_vec) * axis_vec) for p in points_centered]
        radius = np.mean(radii)

        # Calculate height and center by projecting points onto the axis
        projections = [p.dot(axis_vec) for p in points_centered]
        min_proj, max_proj = min(projections), max(projections)
        height = max_proj - min_proj
        center_offset = (min_proj + max_proj) / 2.0
        center_pos = Vector(centroid_np) + center_offset * axis_vec

        if radius < 1e-6 or height < 1e-6:
            self.report({'WARNING'}, "Cannot create cylinder with zero radius or height.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, enter_editmode=False, align='WORLD', location=center_pos)

        new_cyl = context.active_object
        rot_quat = axis_vec.to_track_quat('Z', 'Y')
        new_cyl.rotation_euler = rot_quat.to_euler()

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted cylinder to {len(world_coords)} vertices.")
        return {'FINISHED'}


# class FOTOOLS_PT_fit_panel(bpy.types.Panel):
#     """Creates a Panel in the 3D Viewport for fitting primitives"""
#     bl_label = "Fit Primitives"
#     bl_idname = "FOTOOLS_PT_fit_panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'FOtools '

#     def draw(self, context):
#         layout = self.layout
#         col = layout.column(align=True)
#         col.label(text="Fit to Selection:")
#         col.operator(FOTOOLS_OT_fit_plane.bl_idname)
#         col.operator(FOTOOLS_OT_fit_sphere.bl_idname)
#         col.operator(FOTOOLS_OT_fit_cylinder.bl_idname)


# classes = (
#     FOTOOLS_OT_fit_plane,
#     FOTOOLS_OT_fit_sphere,
#     FOTOOLS_OT_fit_cylinder,
#     FOTOOLS_PT_fit_panel,
# )

# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)

# def unregister():
#     for cls in reversed(classes):
#         bpy.utils.unregister_class(cls)