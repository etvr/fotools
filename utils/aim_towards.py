import bpy


def aim_object_to(object_to_aim, aim_target):
    con = object_to_aim.constraints.new(type="TRACK_TO")
    con.target = aim_target
    bpy.ops.constraint.apply(constraint=con.name, owner='OBJECT', report=False)
