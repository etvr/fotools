# https://vividfax.github.io/2021/01/14/blender-materials.html
# create a new material. The function takes a string as the name for the new material.

import bpy

def newMaterial(id):
    mat = bpy.data.materials.get(id)
    if mat is None:
        mat = bpy.data.materials.new(name=id)
    mat.use_nodes = True
    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()
    return mat


# add a shader to the material. Input the type of shader (i.e. diffuse, emission, glossy) and the rgb colour.
def newShader(id, type, r, g, b):
    mat = newMaterial(id)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')
    if type == "diffuse":
        shader = nodes.new(type='ShaderNodeBsdfDiffuse')
        nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)
    elif type == "emission":
        shader = nodes.new(type='ShaderNodeEmission')
        nodes["Emission"].inputs[0].default_value = (r, g, b, 1)
        nodes["Emission"].inputs[1].default_value = 1
    elif type == "glossy":
        shader = nodes.new(type='ShaderNodeBsdfGlossy')
        nodes["Glossy BSDF"].inputs[0].default_value = (r, g, b, 1)
        nodes["Glossy BSDF"].inputs[1].default_value = 0
    links.new(shader.outputs[0], output.inputs[0])
    return mat


# create the object, assign the material and call the function.
def drawObjectdemo():
    mat = newShader("Shader1", "diffuse", 1, 1, 1)
    bpy.ops.mesh.primitive_cube_add(size=2, align='WORLD', location=(0, 0, 0))
    bpy.context.active_object.data.materials.append(mat)


if __name__ == '__main__':
    drawObjectdemo()