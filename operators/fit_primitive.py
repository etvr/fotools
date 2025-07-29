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

try:
    from scipy.optimize import least_squares
    scipy_available = True
except ImportError:
    scipy_available = False

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

        # Calculate residual error (Root Mean Square of distances to the plane)
        distances = np.abs(np.dot(points_centered, normal_vec))
        rms_error = np.sqrt(np.mean(distances**2))
        print(f"Fit Plane RMS Error: {rms_error:.6f}")

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=centroid)

        new_plane = context.active_object
        rot_quat = Vector(normal_vec).to_track_quat('Z', 'Y')
        new_plane.rotation_euler = rot_quat.to_euler()

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT') 

        self.report({'INFO'}, f"Fitted plane to {len(world_coords)} vertices. RMS Error: {rms_error:.4f}")
        return {'FINISHED'}


class FOTOOLS_OT_fit_sphere(bpy.types.Operator):
    """
    Best-fit a sphere to the selected vertices.
    Uses non-linear least squares (if scipy is available) for accuracy,
    otherwise falls back to a simple average method.
    """
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

        # A unique sphere requires at least 4 non-coplanar points.
        if len(world_coords) < 4:
            self.report({'WARNING'}, "Need at least 4 vertices to fit a sphere.")
            return {'CANCELLED'}

        points = np.array([v.to_tuple() for v in world_coords])

        if scipy_available:
            # --- More accurate method using non-linear least squares ---
            def sphere_residuals(params, points_data):
                """Calculates residuals for sphere fitting (distance from surface)."""
                center, radius = params[:3], params[3]
                return np.linalg.norm(points_data - center, axis=1) - radius

            # Initial guess using the simple centroid/average radius method
            initial_centroid = np.mean(points, axis=0)
            initial_radius = np.mean(np.linalg.norm(points - initial_centroid, axis=1))
            initial_guess = np.append(initial_centroid, initial_radius)

            # Perform the optimization with bounds to ensure radius > 0
            res = least_squares(
                sphere_residuals,
                initial_guess,
                args=(points,),
                jac='3-point',
                bounds=([-np.inf, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, np.inf])
            )

            center_pos_np = res.x[:3]
            radius = res.x[3]
            centroid = Vector(center_pos_np)
            fit_method_msg = "Non-linear least squares"
        else:
            # --- Simpler, less accurate fallback method ---
            self.report({'WARNING'}, "Scipy not found, using simple average. For better accuracy, install scipy.")
            print("FOTOOLS: Scipy not found, using simple average for sphere fit. For better accuracy, please install the 'scipy' python module.")
            centroid_vec = sum(world_coords, Vector()) / len(world_coords)
            radius = sum((v - centroid_vec).length for v in world_coords) / len(world_coords)
            centroid = centroid_vec
            fit_method_msg = "Simple average"

        if radius < 1e-6:
            self.report({'WARNING'}, "Cannot create sphere with zero radius.")
            return {'CANCELLED'}

        # Calculate residual error (RMS of distance from sphere surface)
        centroid_np = np.array(centroid.to_tuple())
        distances_from_center = np.linalg.norm(points - centroid_np, axis=1)
        errors = distances_from_center - radius
        rms_error = np.sqrt(np.mean(errors**2))
        print(f"Fit Sphere ({fit_method_msg}) RMS Error: {rms_error:.6f}")

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, enter_editmode=False, align='WORLD', location=centroid)

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted sphere to {len(world_coords)} vertices. RMS Error: {rms_error:.4f}")
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

        # The axis of the cylinder is the eigenvector with the largest eigenvalue.
        # Eigenvectors from eigh are already normalized.
        axis_vec_np = eigenvectors[:, np.argmax(eigenvalues)]

        # Project points onto the axis to find the height and center offset.
        projections = np.dot(points_centered, axis_vec_np)
        min_proj, max_proj = np.min(projections), np.max(projections)
        height = max_proj - min_proj
        
        # The center of the cylinder is the centroid offset by the average projection.
        center_offset = (min_proj + max_proj) / 2.0
        center_pos_np = centroid_np + center_offset * axis_vec_np

        # Calculate radius by finding the average distance from the axis.
        projections_on_axis = np.outer(projections, axis_vec_np)
        vectors_from_axis = points_centered - projections_on_axis
        radii = np.linalg.norm(vectors_from_axis, axis=1)
        radius = np.mean(radii)

        # Calculate residual error (RMS of radial distance from cylinder surface)
        # This measures how much the points deviate from a constant radius.
        errors = radii - radius
        rms_error = np.sqrt(np.mean(errors**2))
        print(f"Fit Cylinder RMS Error: {rms_error:.6f}")

        if radius < 1e-6 or height < 1e-6:
            self.report({'WARNING'}, "Cannot create cylinder with zero radius or height.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=height, enter_editmode=False, align='WORLD', location=center_pos_np)

        new_cyl = context.active_object
        rot_quat = Vector(axis_vec_np).to_track_quat('Z', 'Y')
        new_cyl.rotation_euler = rot_quat.to_euler()

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted cylinder to {len(world_coords)} vertices. RMS Error: {rms_error:.4f}")
        return {'FINISHED'}


class FOTOOLS_OT_fit_circle(bpy.types.Operator):
    """
    Best-fit a circle to the selected vertices.
    This operator uses Principal Component Analysis (PCA) to find the best-fit plane
    for the selected points, then projects the points onto that plane.
    A 2D circle is then fitted to these projected points using a least-squares method.
    """
    bl_idname = "fotools.fit_circle"
    bl_label = "Fit Circle"
    bl_options = {'REGISTER', 'UNDO'}

    segments: bpy.props.IntProperty(
        name="Segments",
        description="Number of segments for the circle",
        default=32,
        min=3
    )

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
            self.report({'WARNING'}, "Need at least 3 vertices to fit a circle.")
            return {'CANCELLED'}

        points = np.array([v.to_tuple() for v in world_coords])

        # 1. Fit a plane to the points (PCA) to find the circle's orientation
        centroid = np.mean(points, axis=0)
        points_centered = points - centroid
        covariance_matrix = np.cov(points_centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

        # Sort eigenvectors by eigenvalues to find plane vectors
        sort_indices = np.argsort(eigenvalues)
        normal_vec = eigenvectors[:, sort_indices[0]]  # Smallest eigenvalue -> plane normal
        plane_v1 = eigenvectors[:, sort_indices[2]]    # Largest eigenvalue -> plane axis 1
        plane_v2 = eigenvectors[:, sort_indices[1]]    # Middle eigenvalue -> plane axis 2

        # 1a. Calculate residual error for the plane fit (deviation from the plane)
        plane_distances = np.abs(np.dot(points_centered, normal_vec))
        plane_rms_error = np.sqrt(np.mean(plane_distances**2))
        print(f"Fit Circle - Plane Fit RMS Error: {plane_rms_error:.6f}")

        # 2. Project points onto the plane and convert to a 2D system
        coords_2d_x = np.dot(points_centered, plane_v1)
        coords_2d_y = np.dot(points_centered, plane_v2)

        # 3. Fit a 2D circle using least squares
        # (x-a)^2 + (y-b)^2 = R^2  =>  2ax + 2by + (R^2-a^2-b^2) = x^2+y^2
        A = np.array([coords_2d_x, coords_2d_y, np.ones(len(coords_2d_x))]).T
        b = coords_2d_x**2 + coords_2d_y**2

        # Solve for c = [2a, 2b, R^2-a^2-b^2]
        c, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        center_x_2d = c[0] / 2
        center_y_2d = c[1] / 2

        # 4. Calculate the radius
        radius_sq = c[2] + center_x_2d**2 + center_y_2d**2
        circle_radius = np.sqrt(radius_sq)

        # 4a. Calculate residual error for the circle fit
        # This measures the deviation of the projected 2D points from the fitted circle.
        distances_from_center = np.sqrt((coords_2d_x - center_x_2d)**2 + (coords_2d_y - center_y_2d)**2)
        errors = distances_from_center - circle_radius
        circle_rms_error = np.sqrt(np.mean(errors**2))
        print(f"Fit Circle - Circle Fit RMS Error: {circle_rms_error:.6f}")

        # 5. Convert the 2D center back to 3D world coordinates
        circle_center_world = centroid + center_x_2d * plane_v1 + center_y_2d * plane_v2

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_circle_add(vertices=self.segments, radius=circle_radius, enter_editmode=False, align='WORLD', location=circle_center_world)
        circle_object = context.active_object
        circle_object.name = "Fitted_Circle"

        # Orient the circle to align with the fitted plane
        rot_quat = Vector(normal_vec).to_track_quat('Z', 'Y')
        circle_object.rotation_euler = rot_quat.to_euler()

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted circle to {len(world_coords)} vertices. Plane RMS: {plane_rms_error:.4f}, Circle RMS: {circle_rms_error:.4f}")
        return {'FINISHED'}


class FOTOOLS_OT_fit_line(bpy.types.Operator):
    """Create a best fit line through selected vertices"""
    bl_idname = "fotools.fit_line"
    bl_label = "Fit Line"
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
            self.report({'WARNING'}, "Not enough vertices selected (need at least 2)")
            return {'CANCELLED'}

        points = np.array([v.to_tuple() for v in world_coords])

        # Calculate centroid
        centroid = np.mean(points, axis=0)

        # Calculate direction using Principal Component Analysis (PCA)
        # First, center the data
        centered_coords = points - centroid

        # Calculate covariance matrix
        cov_matrix = np.cov(centered_coords.T)

        # Calculate eigenvectors and eigenvalues
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

        # Sort eigenvectors by eigenvalues in descending order
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Principal direction is the eigenvector with the largest eigenvalue
        principal_direction = Vector(eigenvectors[:, 0])
        principal_direction.normalize()

        # Calculate residual error (RMS of perpendicular distance to the line)
        principal_direction_np = np.array(principal_direction)
        cross_products = np.cross(centered_coords, principal_direction_np)
        distances_sq = np.sum(cross_products**2, axis=1)
        rms_error = np.sqrt(np.mean(distances_sq))
        print(f"Fit Line RMS Error: {rms_error:.6f}")

        # Find the extent of the vertices along the principal direction
        projections = [Vector(p - centroid).dot(principal_direction) for p in points]
        min_proj = min(projections)
        max_proj = max(projections)

        bpy.ops.object.mode_set(mode='OBJECT')

        # Create a new mesh for the line
        line_mesh = bpy.data.meshes.new("BestFitLine")
        line_obj = bpy.data.objects.new("BestFitLine", line_mesh)

        # Link the object to the scene
        context.collection.objects.link(line_obj)

        # Create the line vertices
        start_point = Vector(centroid) + principal_direction * min_proj
        end_point = Vector(centroid) + principal_direction * max_proj

        # Create the line mesh
        line_verts = [start_point, end_point]
        line_edges = [(0, 1)]
        line_mesh.from_pydata(line_verts, line_edges, [])
        line_mesh.update()

        # Restore original selection
        original_obj = context.scene.objects.get(original_obj_name)
        context.view_layer.objects.active = original_obj
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, f"Fitted line to {len(world_coords)} vertices. RMS Error: {rms_error:.4f}")
        return {'FINISHED'}