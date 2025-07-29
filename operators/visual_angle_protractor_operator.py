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

bl_info = {
    "name": "Add Protractor",
    "author": "Alexander de Bruijn",
    "version": (2, 1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Add > Mesh > Protractor",
    "description": "Adds a new protractor mesh with degree labels",
    "warning": "",
    "doc_url": "https://github.com/etvr/fotools",
    "category": "Add Mesh",
}

import bpy
import math
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatProperty, IntProperty, BoolProperty


class OBJECT_OT_add_angle_protractor(bpy.types.Operator, AddObjectHelper):
    """Create a new Protractor object"""
    bl_idname = "mesh.add_protractor"
    bl_label = "Add Protractor"
    bl_options = {'REGISTER', 'UNDO'}

    outer_radius: FloatProperty(
        name="Radius",
        description="Outer radius of the protractor",
        default=0.5,
        min=0.1,
        unit='LENGTH'
    )

    width: FloatProperty(
        name="Width",
        description="Width of the protractor arc",
        default=0.1,
        min=0.01,
        unit='LENGTH'
    )

    arc_resolution: IntProperty(
        name="Resolution",
        description="Number of segments for the 180-degree arc. Higher is smoother",
        default=90,
        min=2,
        max=360
    )

    add_ticks: BoolProperty(
        name="Add Tick Marks",
        description="Create tick marks on the protractor mesh",
        default=True
    )

    major_tick_length: FloatProperty(
        name="Major Tick Length",
        description="Length of the major (10 degree) tick marks, extending from the inner edge",
        default=0.008,
        min=0.0,
        unit='LENGTH'
    )

    medium_tick_length: FloatProperty(
        name="Medium Tick Length",
        description="Length of the medium (5 degree) tick marks",
        default=0.05,
        min=0.0,
        unit='LENGTH'
    )

    minor_tick_length: FloatProperty(
        name="Minor Tick Length",
        description="Length of the minor (1 degree) tick marks",
        default=0.02,
        min=0.0,
        unit='LENGTH'
    )

    tick_width: FloatProperty(
        name="Tick Width",
        description="The width (thickness) of the tick marks",
        default=0.002,
        min=0.001,
        unit='LENGTH'
    )

    add_labels: BoolProperty(
        name="Add Labels",
        description="Create text objects for degree labels",
        default=True
    )

    label_size: FloatProperty(
        name="Label Size",
        description="The size of the text labels",
        default=0.05,
        min=0.01,
        unit='LENGTH'
    )

    label_offset: FloatProperty(
        name="Label Offset",
        description="Distance of the labels from the outer edge",
        default=0.05,
        min=0,
        unit='LENGTH'
    )

    def draw(self, context):
        """Custom layout for the operator properties."""
        layout = self.layout
        layout.use_property_split = True

        layout.label(text="Arc Shape:")
        col = layout.column(align=True)
        col.prop(self, "outer_radius")
        col.prop(self, "width")
        col.prop(self, "arc_resolution")

        layout.separator()
        layout.prop(self, "add_ticks")
        if self.add_ticks:
            box = layout.box()
            col = box.column(align=True)
            col.prop(self, "major_tick_length")
            col.prop(self, "medium_tick_length")
            col.prop(self, "minor_tick_length")
            #col.prop(self, "tick_width")

        layout.separator()
        layout.prop(self, "add_labels")
        if self.add_labels:
            box = layout.box()
            col = box.column(align=True)
            col.prop(self, "label_size")
            col.prop(self, "label_offset")

    def execute(self, context):

        inner_radius = self.outer_radius - self.width
        verts = []
        faces = []

        # Generate vertices for the arc
        for i in range(self.arc_resolution + 1):
            angle_rad = math.pi * i / self.arc_resolution
            cos_angle = math.cos(angle_rad)
            sin_angle = math.sin(angle_rad)

            # Outer vertex
            verts.append((self.outer_radius * cos_angle, self.outer_radius * sin_angle, 0.0))
            # Inner vertex
            verts.append((inner_radius * cos_angle, inner_radius * sin_angle, 0.0))

        # Generate faces for the arc
        for i in range(self.arc_resolution):
            v_outer_curr = 2 * i
            v_inner_curr = 2 * i + 1
            v_outer_next = 2 * (i + 1)
            v_inner_next = 2 * (i + 1) + 1

            faces.append((v_inner_curr, v_outer_curr, v_outer_next, v_inner_next))

        # Generate tick marks
        if self.add_ticks and inner_radius > 0:
            for angle_deg in range(1, 180):  # Ticks from 1 to 179 degrees
                tick_len = 0
                if angle_deg % 10 == 0:
                    tick_len = self.major_tick_length
                elif angle_deg % 5 == 0:
                    tick_len = self.medium_tick_length
                else:
                    tick_len = self.minor_tick_length

                if tick_len <= 0:
                    continue

                # Ensure tick does not go past the center
                tick_len = min(tick_len, inner_radius)

                angle_rad = math.radians(angle_deg)
                # Calculate angular width of the tick using arc length formula: theta = s / r
                angle_offset = (self.tick_width / 2) / inner_radius

                angle_left = angle_rad - angle_offset
                angle_right = angle_rad + angle_offset

                cos_l, sin_l = math.cos(angle_left), math.sin(angle_left)
                cos_r, sin_r = math.cos(angle_right), math.sin(angle_right)

                base_idx = len(verts)
                verts.append((inner_radius * cos_l, inner_radius * sin_l, 0))
                verts.append((inner_radius * cos_r, inner_radius * sin_r, 0))
                verts.append(((inner_radius - tick_len) * cos_r, (inner_radius - tick_len) * sin_r, 0))
                verts.append(((inner_radius - tick_len) * cos_l, (inner_radius - tick_len) * sin_l, 0))
                faces.append((base_idx, base_idx + 1, base_idx + 2, base_idx + 3))

        mesh = bpy.data.meshes.new(name="Protractor")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        protractor_obj = object_data_add(context, mesh, operator=self)

        if self.add_labels:
            label_radius = self.outer_radius + self.label_offset

            for angle_deg in range(0, 181, 10):
                angle_rad = math.radians(angle_deg)

                text_curve = bpy.data.curves.new(name=f"LabelCurve_{angle_deg}", type='FONT')
                text_curve.body = str(angle_deg)
                text_curve.align_x = 'CENTER'
                text_curve.align_y = 'CENTER'
                text_curve.size = self.label_size

                label_obj = bpy.data.objects.new(name=f"Label_{angle_deg}", object_data=text_curve)
                label_obj.location.x = label_radius * math.cos(angle_rad)
                label_obj.location.y = label_radius * math.sin(angle_rad)
                label_obj.rotation_euler.z = angle_rad

                label_obj.parent = protractor_obj
                context.collection.objects.link(label_obj)

        return {'FINISHED'}

def add_visual_protractor_button(self, context):
    """Adds the operator to the Add > Mesh menu."""
    self.layout.operator(OBJECT_OT_add_angle_protractor.bl_idname, text="Protractor", icon='MOD_CURVE')