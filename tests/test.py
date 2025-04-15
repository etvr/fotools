import unittest
import bpy
import bmesh
from mathutils import Vector
import math

class TestFaceRemoval(unittest.TestCase):
    def setUp(self):
        # Create a new mesh object for testing
        mesh = bpy.data.meshes.new(name="Test Mesh")
        self.obj = bpy.data.objects.new("Test Object", mesh)
        bpy.context.scene.collection.objects.link(self.obj)
        bpy.context.view_layer.objects.active = self.obj
        
    def tearDown(self):
        # Clean up test objects
        bpy.data.objects.remove(self.obj, do_unlink=True)
        
    def test_close_parallel_faces(self):
        # Create two close parallel faces
        bm = bmesh.new()
        
        # First face
        v1 = bm.verts.new((0, 0, 0))
        v2 = bm.verts.new((1, 0, 0))
        v3 = bm.verts.new((1, 1, 0))
        v4 = bm.verts.new((0, 1, 0))
        
        # Second face slightly above
        v5 = bm.verts.new((0, 0, 0.0005))
        v6 = bm.verts.new((1, 0, 0.0005))
        v7 = bm.verts.new((1, 1, 0.0005))
        v8 = bm.verts.new((0, 1, 0.0005))
        
        face1 = bm.faces.new((v1, v2, v3, v4))
        face2 = bm.faces.new((v5, v6, v7, v8))
        
        bm.to_mesh(self.obj.data)
        bm.free()
        
        # Run the operator
        bpy.ops.mesh.remove_close_faces()
        
        # Check if faces were removed
        self.assertEqual(len(self.obj.data.polygons), 0)
        
    def test_distant_faces(self):
        # Create two faces far apart
        bm = bmesh.new()
        
        # First face
        v1 = bm.verts.new((0, 0, 0))
        v2 = bm.verts.new((1, 0, 0))
        v3 = bm.verts.new((1, 1, 0))
        v4 = bm.verts.new((0, 1, 0))
        
        # Second face far above
        v5 = bm.verts.new((0, 0, 1))
        v6 = bm.verts.new((1, 0, 1))
        v7 = bm.verts.new((1, 1, 1))
        v8 = bm.verts.new((0, 1, 1))
        
        face1 = bm.faces.new((v1, v2, v3, v4))
        face2 = bm.faces.new((v5, v6, v7, v8))
        
        bm.to_mesh(self.obj.data)
        bm.free()
        
        # Run the operator
        bpy.ops.mesh.remove_close_faces()
        
        # Check if faces were preserved
        self.assertEqual(len(self.obj.data.polygons), 2)
        
    def test_perpendicular_faces(self):
        # Create two close but perpendicular faces
        bm = bmesh.new()
        
        # Horizontal face
        v1 = bm.verts.new((0, 0, 0))
        v2 = bm.verts.new((1, 0, 0))
        v3 = bm.verts.new((1, 1, 0))
        v4 = bm.verts.new((0, 1, 0))
        
        # Vertical face
        v5 = bm.verts.new((0, 0, 0))
        v6 = bm.verts.new((0, 0, 1))
        v7 = bm.verts.new((1, 0, 1))
        v8 = bm.verts.new((1, 0, 0))
        
        face1 = bm.faces.new((v1, v2, v3, v4))
        face2 = bm.faces.new((v5, v6, v7, v8))
        
        bm.to_mesh(self.obj.data)
        bm.free()
        
        # Run the operator
        bpy.ops.mesh.remove_close_faces()
        
        # Check if faces were preserved
        self.assertEqual(len(self.obj.data.polygons), 2)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFaceRemoval)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_tests()