import bpy


def aim_object_to(object_to_aim, aim_target):
    con = object_to_aim.constraints.new(type="TRACK_TO")
    con.target = aim_target
    object_to_aim.constraints.apply(constraint=con.name)

# DEBUG CODE
    # print(f"{con=}")
    # print(f"{con.name=}")
    # print(f"{aim_target=}")
    # print(f"{object_to_aim=}/n/n")
# EO DEBUG CODE

    # bpy.ops.constraint.apply(constraint=con.name)
    #bpy.ops.constraint.apply(constraint="Track To", owner='OBJECT')


# def example_apply:
#     for obj in bpy.context.selected_objects:

#     # loop over the constraints in each object
#     for con in obj.constraints[:]:
#         # get the constraint you want to apply
#         if con.type == "COPY_TRANSFORMS":

#             # apply it using the constraint name.
#             bpy.ops.constraint.apply(constraint=con.name)
'''    
----
target_obj = bpy.data.objects['Cube']
camera_obj = bpy.data.objects['Camera']
 
constraint = camera_obj.constraints.new(type='TRACK_TO')
constraint.target = target_obj
----
----
import bpy

o = bpy.context.object
constraint = o.constraints.new('COPY_LOCATION')

#constraint properties
constraint.show_expanded = False
constraint.mute = True
----
'''
