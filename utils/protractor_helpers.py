  import bpy
  from math import radians, sin
  
  def calculate_triangle_coordinates(self, angle_a: float, radius: float):
    # calculates the coordinates of  the top vertex of the protractor with the given corner 'a' on the origin.
    angle_c = 90.0 - (angle_a / 2.0)
    length_A = sin(radians(angle_a / 2.0)) * radius
    length_C = sin(radians(angle_c)) * radius
    #print (f"{length_C=}, {length_A=}, {angle_a=}, {radius=}")
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