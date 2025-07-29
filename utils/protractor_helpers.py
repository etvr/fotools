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
from math import radians, sin

def calculate_triangle_coordinates(self, angle_a: float, radius: float):
  # calculates the coordinates of  the top vertex of the protractor with the given corner 'a' on the origin.
  angle_c = 90.0 - (angle_a / 2.0)
  length_A = sin(radians(angle_a / 2.0)) * radius
  length_C = sin(radians(angle_c)) * radius
  return [length_C, length_A]


def draw_polygon(self, vertices_array, faces_array, name):
  #creates a polygon shape based on an input of vertices and faces.
  mesh = bpy.data.meshes.new("Triangle_Mesh")
  obj = bpy.data.objects.new(name, mesh)
  bpy.context.collection.objects.link(obj)
  edges = []
  mesh_data = mesh.from_pydata(vertices_array, edges, faces_array)
  mesh.update()
  return obj