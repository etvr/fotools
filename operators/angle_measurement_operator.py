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
import math
import mathutils

class FOTOOLS_OT_MeasureAngle(bpy.types.Operator):
    """Measure the angle between three selected objects, with the active object as the vertex"""
    bl_idname = "fotools.measure_angle"
    bl_label = "Measure Angle Between 3 Objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # This operator requires three selected objects, one of which is active.
        return context.active_object is not None and len(context.selected_objects) == 3

    def execute(self, context):
        selected_objs = context.selected_objects
        active_obj = context.active_object

        # The active object is the vertex of the angle.
        # The other two selected objects are the endpoints of the vectors.
        other_objs = [obj for obj in selected_objs if obj != active_obj]

        p_vertex = active_obj.location
        p_end1 = other_objs[0].location
        p_end2 = other_objs[1].location

        # Create vectors from the vertex to the endpoints.
        vec1 = p_end1 - p_vertex
        vec2 = p_end2 - p_vertex

        # Calculate the angle between the two vectors.
        angle_rad = vec1.angle(vec2)
        angle_deg = math.degrees(angle_rad)

        # --- Create Visual Representation ---

        # 1. Create an empty object to act as the parent for the measurement visuals.
        # This makes it easy to move, hide, or delete the entire measurement.
        angle_measurement_empty = bpy.data.objects.new("AngleMeasurement", None)
        angle_measurement_empty.location = p_vertex
        context.collection.objects.link(angle_measurement_empty)

        # 2. Create the lines representing the angle.
        mesh_data = bpy.data.meshes.new(name="AngleLines")
        # Vertices are defined relative to the parent empty's location.
        verts = [vec1, mathutils.Vector((0,0,0)), vec2]
        edges = [[0, 1], [1, 2]]
        mesh_data.from_pydata(verts, edges, [])
        mesh_data.update()

        line_obj = bpy.data.objects.new("AngleLines", mesh_data)
        context.collection.objects.link(line_obj)
        line_obj.parent = angle_measurement_empty

        # 3. Create the angle arc visual
        plane_normal = vec1.cross(vec2)
        if plane_normal.length > 1e-6:
            plane_normal.normalize()

            # Use a radius that is a fraction of the vector lengths
            arc_radius = (vec1.length + vec2.length) / 16.0
            num_segments = 32

            arc_verts = [mathutils.Vector((0,0,0))] # Center vertex
            start_arc_vec = vec1.normalized() * arc_radius

            # Generate vertices by rotating the start vector around the plane normal
            for i in range(num_segments + 1):
                angle_step = i * (angle_rad / num_segments)
                rot_mat = mathutils.Matrix.Rotation(angle_step, 4, plane_normal)
                new_vert = rot_mat @ start_arc_vec
                arc_verts.append(new_vert)

            # Create faces for the arc fan
            arc_faces = []
            # The first vertex in arc_verts is the center, so we start faces from index 1
            for i in range(1, num_segments + 1):
                arc_faces.append((0, i, i + 1))

            arc_mesh_data = bpy.data.meshes.new(name="AngleArc")
            arc_mesh_data.from_pydata(arc_verts, [], arc_faces)
            arc_mesh_data.update()

            arc_obj = bpy.data.objects.new("AngleArc", arc_mesh_data)
            context.collection.objects.link(arc_obj)
            arc_obj.parent = angle_measurement_empty

        # 4. Create the text label for the angle.
        # Position the label midway between the two vectors.
        label_pos_vec_dir = (vec1.normalized() + vec2.normalized())
        
        # Handle the case where vectors are opposite, to avoid a zero-length direction vector.
        if label_pos_vec_dir.length < 1e-6:
            # Create a perpendicular vector to place the label.
            label_pos_vec_dir = vec1.cross(mathutils.Vector((0,0,1)))
            if label_pos_vec_dir.length < 1e-6: # if vec1 is aligned with Z
                 label_pos_vec_dir = vec1.cross(mathutils.Vector((0,1,0)))

        label_pos_vec_dir.normalize()

        # Place label at 1/8 of the average length of the vectors.
        label_dist = (vec1.length + vec2.length) / 8.0
        label_pos = label_pos_vec_dir * label_dist

        text_curve = bpy.data.curves.new(name="AngleLabelCurve", type='FONT')
        text_curve.body = f"{angle_deg:.2f}°"
        text_curve.align_x = 'CENTER'
        text_curve.align_y = 'CENTER'
        text_curve.size = context.scene.fotools_angle_label_size

        label_obj = bpy.data.objects.new(name="AngleLabel", object_data=text_curve)
        label_obj.location = label_pos
        
        # Orient the label to be flat on the plane of the angle.
        plane_normal = vec1.cross(vec2)
        if plane_normal.length > 1e-6:
            rot_quat = plane_normal.to_track_quat('Z', 'Y')
            label_obj.rotation_euler = rot_quat.to_euler()

        context.collection.objects.link(label_obj)
        label_obj.parent = angle_measurement_empty

        self.report({'INFO'}, f"Measured Angle: {angle_deg:.2f} degrees")

        return {'FINISHED'}
