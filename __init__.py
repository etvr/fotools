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

from .panels.sightline_pannel import Sightline_analysis_pannel
from .panels.geonode_pointcloud_pannel import Geonode_pointcloud_Panel
from .panels.impact_backprojection_panel import Backprojection_Panel
from .panels.boolean_cutter_panel import Boolcut_Panel
from .panels.protractor_panel import Protractor_Panel
from .operators.deflectioncone_operator import FOtools_OT_DeflectionCone
from .operators.bool_cut_operator import FOtools_OT_Bool_cut
from .operators.protractor_operator import FOtools_OT_Protractor
from .operators.frustum_operator import FOtools_OT_Frustum
from .operators.geonode_operator import FOtools_OT_GeonodePointcloud
from .operators.sightline_operator import FOtools_OT_Sightlines
from .operators.clean_voxel_mesh_operator import MESH_OT_remove_close_faces
from .operators.create_voxelmesh_from_p_cloud_operator import FOtools_OT_CreateVoxelMeshFromCloud
from .operators.import_ply_file_operator import FOtools_OT_ImportPLY


# bl_info = {
#     "name": "FOtools",
#     "description": "3D-forensic Utillities for Blender by ETVR, https://www.politie.nl/informatie/expertteam-visualisatie-en-reconstructie.html",
#     "author": "Alexander de Bruijn",
#     "version": (0, 2, 1),
#     "blender": (4, 4, 0),
#     "wiki_url": "https://github.com/etvr/fotools",
#     "tracker_url": "https://github.com/etvr/fotools",
#     "category": "Generic"
# }


classes = [
    Backprojection_Panel,
    FOtools_OT_DeflectionCone,
    Boolcut_Panel,
    FOtools_OT_Bool_cut,
    Protractor_Panel,
    FOtools_OT_Protractor,
    FOtools_OT_Frustum,
    Sightline_analysis_pannel,
    FOtools_OT_Sightlines,
    Geonode_pointcloud_Panel,
    FOtools_OT_GeonodePointcloud,
    MESH_OT_remove_close_faces,
    FOtools_OT_CreateVoxelMeshFromCloud,
    FOtools_OT_ImportPLY
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
