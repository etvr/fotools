'''
the script takes a HOROS roi file andplaces blender spheres on the extracted coordinates
'''

import bpy

# setup
#TODO: native fileselection dialog

roi_file_path = "C:\\Users\\alexander\\OneDrive\\Desktop\\Test ETVR\\rois.txt"
split_string_line = "3D Pos:"
split_string_coordinates = "mm"
sphereradius =5
coordinatelist = []

# store 3d cursor original location
original_3dcursor_position = bpy.context.scene.cursor.location

# read data
roi_file = open(roi_file_path, "rb")
txt = str(roi_file.readline())

# split the data
buffer = txt.split(split_string_line)
buffer.pop(0)

#clean up the coordinates
for item in buffer:
    coordinate_buffer = item.split(split_string_coordinates)
    coordinatelist.append((coordinate_buffer[0][3:-1], coordinate_buffer[1][3:-1], coordinate_buffer[1][3:-1]))
    
# create the roi spheres
for item in coordinatelist:
    print(item)
    roi_location = float(item[0]), float(item[1]), float(item[2])
    bpy.context.scene.cursor.location = roi_location
    bpy.ops.mesh.primitive_uv_sphere_add(radius=sphereradius, segments=32, ring_count=64)
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', radius=sphereradius*2)


# set 3d cursor back to original position
bpy.context.scene.cursor.location = original_3dcursor_position