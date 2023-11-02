'''
Created by Alexander de Bruijn 2022

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

FOtools: a set of blender tools to assist in 3D-Forensic analysis
'''
import bpy

def newMaterial(name):
    mat = bpy.data.materials.get(name)

    if mat is None:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True

    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()

    return mat

def newShader(name, type, r, g, b):
    mat = newMaterial(name)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    output = nodes.new(type="ShaderNodeOutputMaterial")

    if type == "diffuse":
        shader = nodes.new(type="ShaderNodeBsdfDiffuse")
        nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)

    elif type == "emission":
        shader = nodes.new(type="ShaderNodeEmission")
        nodes["Emission"].inputs[0].default_value = (r, g, b, 1)
        nodes["Emission"].inputs[1].default_value = 1

    elif type == "glossy":
        shader = nodes.new(type="ShaderNodeBsdfGlossy")
        nodes["Glossy BSDF"].inputs[0].default_value = (r, g, b, 1)
        nodes["Glossy BSDF"].inputs[1].default_value = 0

    links.new(shader.outputs[0], output.inputs[0])
    return mat
