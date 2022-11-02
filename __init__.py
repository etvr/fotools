'''
Copyright (C) 2022 Alexander de Bruijn 

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

from . panels.Field_of_view_panel import Field_of_view_Panel
from . panels.impact_backprojection_panel import Backprojection_Panel
from . operators.deflectioncone_operator import FOtools_OT_DeflectionCone
from . panels.boolean_cutter_panel import Boolcut_Panel
from . operators.bool_cut_operator import FOtools_OT_Bool_cut


bl_info = {
    "name": "FOtools",
    "description": "3D-forensic Utillities for Blender by ETVR, https://www.politie.nl/informatie/expertteam-visualisatie-en-reconstructie.html",
    "author": "Alexander de Bruijn",
    "version": (0, 1, 2, 2),
    "blender": (3, 3, 1),
    "wiki_url": "NOT YET",
    "tracker_url": "NOT YET",
    "category": "Generic"
}


classes = [
    Backprojection_Panel, 
    FOtools_OT_DeflectionCone, 
    Boolcut_Panel, 
    FOtools_OT_Bool_cut,
    Field_of_view_Panel
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()


# TODO: add logo and version to panel
# TODO: custom icons
# TODO: place humanoid male and female figure
# TODO: find the standard addon license in the snippets file
# TODO: field of view highlighter/ /checker
# TODO: add edge to mesh line function
# TODO: selector for: back-projection, foreward-projection, both, line-between.
# TODO: if the angle ==0, draw a 9mm cylinder or a cone with a 1st and 2nd radius that is 9mm
# TODO: ricochet lijn tool met verstelbare mirror lijn
# TODO: the impactpoint radius is now a point, this is not realistic, van be fixed my pulling impact pivot back towards a given cone radius
# TODO: add a offset value for a perpendicular pivotpoint
# TODO: basic pointcloud importer?
# TODO: groundplane extractor ?
# TODO: resampling, voxel, spatial ?
# TODO: basic dicom importer
# TODO: adjustable wedge tool
# TODO: Cloudcompare achtige path animatie tool
# TODO: click on plane and set an object with a give "height" allong the face normal
# TODO: toggle radius cutter,
# TODO: make cone and radius sphere density increas as the length grow longer.
# TODO: preferences panel---- think materials, diameters
# TODO: checkbox to retain tracking of the cone to secondary point
# TODO: implement color selector panel
# TODO: mesh cleaning tools
# TODO: REFACTOR CLEANUP out of bool_cut_operator
# DONE: implement boolcut pannel
# DONE: create red, yelow, blue materials on startup
# DONE: assign materials to the cone  sections
# DONE: Sync vertices of the uvsphere to  the vertices of the cone in the init script.
# DONE: a 32*16 uv-sphere over 10M can have a deviation aprox. 10CM due to the polygonal structure of the curved surface
# DONE: optimaliseer cutter segmenten tov cutee cone
# DONE: its probably better to aim the cone after cleanup
# DONE: cleanup expects the vertices to be exactly alligned.