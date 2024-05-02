"""
Created by Alexander de Bruijn 2024

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
"""
import bpy
from typing import List

import math


class FOtools_OT_Bool_cut(bpy.types.Operator):
    bl_idname = "mesh.protractor"
    bl_label = "FOtools create protractor"
    bl_description = (
        "creates an polytriangle with an set angle on the world origin point"
    )
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        parmA = "something"
        parmB = "something else"
        self.operator(parmA, parmB)
        return {"FINISHED"}

    def operator(self, parmA, ParmB): 
        pass
    
    def calculate_ triangle_coordinates(radius, angle) -> List[float, float]:
        '''
                    c
                  /|
                /  |
              /    |
          B/      |A
          /        |
        /-------|
    a       C      b       
    
                    68
                  /|
                /  |
              /    |
        1  /      | 0.3746
          /        |
        /-------|
22  0.9272    90       
    
    
        apply sine rule?
        - radius can be assumed as 1 and scaled after drawing the polygon, apply transform afterward. this way we can skip a multiplication
       
        so givn  that 
        B = : "radius" ex: 1
        b = 90 deg'
        a = "angle" a set function argument ex: 22
        
        then 
        c = (180 - b - a)
        A = math.sin( a ) * B
        C = math.sine( c ) * B
        ''