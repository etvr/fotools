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

FOtools: a set of blender tools to assist in 3D-Forensic analysis Alexander de Bruijn 2024
'''


import bpy

from .panels.Field_of_view_panel import Field_of_view_Panel
from .panels.impact_backprojection_panel import Backprojection_Panel
from .operators.deflectioncone_operator import FOtools_OT_DeflectionCone
from .panels.boolean_cutter_panel import Boolcut_Panel
from .operators.bool_cut_operator import FOtools_OT_Bool_cut
from .panels.geonode_pointcloud_pannel import Geonode_pointcloud_Panel
from .panels.protractor_panel import Protractor_Panel
from .operators.protractor_operator import FOtools_OT_Protractor
from .operators.frustum_operator import FOtools_OT_Frustum

bl_info = {
    "name": "FOtools",
    "description": "3D-forensic Utillities for Blender by ETVR, https://www.politie.nl/informatie/expertteam-visualisatie-en-reconstructie.html",
    "author": "Alexander de Bruijn",
    "version": (0, 1, 2, 2),
    "blender": (3, 3, 1),
    "wiki_url": "www.google.com",
    "tracker_url": "www....com",
    "category": "Generic"
}


classes = [
    Backprojection_Panel,
    FOtools_OT_DeflectionCone,
    Boolcut_Panel,
    FOtools_OT_Bool_cut,
    Field_of_view_Panel,
    Geonode_pointcloud_Panel,
    Protractor_Panel,
    FOtools_OT_Protractor,
    FOtools_OT_Frustum
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

