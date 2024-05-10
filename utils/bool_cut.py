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
from ..utils.aim_towards import aim_object_to


def cut(cutter, cutee):

    # setup objects and add modifiers
    object_name = cutee.name
    cutee.name = f'{object_name}_inside'
    cutee_copy = cutee.copy()
    bpy.context.collection.objects.link(cutee_copy)
    cutee_copy.name = f'{object_name}_outside'
    
    # set up  boolean operation
    mod1 = cutee.modifiers.new('mod1', type='BOOLEAN')
    mod1.object = cutter
    mod1.operation = 'INTERSECT'
    
    mod2 = cutee_copy.modifiers.new('mod2', type='BOOLEAN')
    mod2.object = cutter
    mod2.operation = 'DIFFERENCE'

    # apply boolean operation to the mesh
    bpy.context.view_layer.objects.active = cutee
    bpy.ops.object.modifier_apply(modifier="mod1", single_user=True)
    cleanup_verts(cutee)
    
    bpy.context.view_layer.objects.active = cutee_copy
    bpy.ops.object.modifier_apply(modifier="mod2", single_user=True)
    cleanup_verts(cutee_copy)
    
    # remove cutter object
    bpy.context.view_layer.objects.active = cutter
    bpy.ops.object.delete(use_global=False)
    return [cutee, cutee_copy]

    
def cleanup_verts(obj_to_clean) -> None:
    # - cleanup  works as expected   if the sections of the cutter and cone are equal and  alligned 
    if  obj_to_clean.type != 'MESH':
        print(f"{obj_to_clean} is not a MESH object, please select a object of type MESH and try again")
    else:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.00001)
        bpy.ops.object.mode_set(mode='OBJECT')

def radius_cut(object_to_cut, radius: float, aim_target=None):
    '''
        cut an object with the volume of another
        optional, aim the cutter object to an axis
    '''
    # store 3d cursor location
    original_3dcursor_position = bpy.context.scene.cursor.location
    bpy.context.scene.cursor.location = object_to_cut.location
    
    # create radius cutter object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=64, ring_count=128)
    cutter = bpy.context.active_object
    if aim_target is not None:
        aim_object_to(cutter, aim_target)
    result = cut(cutter, object_to_cut)
    
    # set 3d cursor back to original position
    bpy.context.scene.cursor.location = original_3dcursor_position
    return result