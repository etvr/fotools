# 1: apply modifiers on voxel objects
# 2: select all cubes and join them together into a singel mesh object
# 3: find oposite faces ( overlap, close together, equal size)
# 4: delete all these faces
# 5: merge all vertices that are very close together or overlap
# 6: add a decimate modifier in PLANAR mode
# 7: apply the modifier




# import bpy
# import bmesh
# from mathutils import Vector
# import math

# def find_and_remove_close_faces():
#     active_object = bpy.context.active_object
#     if active_object is None or active_object.type != 'MESH':
#         print("Please select a mesh object")
#         return
    
#     DISTANCE_THRESHOLD = 0.001  # Distance threshold for considering faces as "close"
    
#     bm = bmesh.new()
#     bm.from_mesh(active_object.data)
#     bm.faces.ensure_lookup_table()
    
#     # Calculate face centers and normals
#     face_data = []
#     for face in bm.faces:
#         face_center = face.calc_center_median()
#         face_normal = face.normal
#         face_data.append((face, face_center, face_normal))
    
#     # Find close face pairs
#     faces_to_remove = set()
    
#     for i, (face1, center1, normal1) in enumerate(face_data):
#         for j, (face2, center2, normal2) in enumerate(face_data[i+1:], i+1):
#             # Skip if either face is already marked for removal
#             if face1 in faces_to_remove or face2 in faces_to_remove:
#                 continue
#             face_center_distance = (center1 - center2).length
#             normal_angle_between = math.degrees(normal1.angle(normal2))
#             # Check if faces are close and parallel/anti-parallel
#             if face_center_distance < DISTANCE_THRESHOLD and (normal_angle_between < 10 or normal_angle_between > 170):
#                 faces_to_remove.add(face1)
#                 faces_to_remove.add(face2)
    
#     bmesh.ops.delete(bm, geom=list(faces_to_remove), context='FACES')
#     bm.to_mesh(active_object.data)
#     active_object.data.update()
#     bm.free()
    
#     print(f"Removed {len(faces_to_remove)} faces")

# Register operator
# class MESH_OT_remove_close_faces(bpy.types.Operator):
#     bl_idname = "mesh.remove_close_faces"
#     bl_label = "Remove Close Faces"
#     bl_description = "Remove planar pairs of faces that are very close together"
#     bl_options = {'REGISTER', 'UNDO'}
    
#     def execute(self, context):
#         find_and_remove_close_faces()
#         return {'FINISHED'}

# def register():
#     bpy.utils.register_class(MESH_OT_remove_close_faces)

# def unregister():
#     bpy.utils.unregister_class(MESH_OT_remove_close_faces)

# if __name__ == "__main__":
#     register()
