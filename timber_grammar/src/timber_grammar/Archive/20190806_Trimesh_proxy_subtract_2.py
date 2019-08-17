import compas 
from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas.datastructures import mesh_quads_to_triangles
import trimesh

class Trimesh_proxy_subtract(object):
    """
    this class performs a boolean difference of input meshes
    """
    def _init_(self, beam_mesh, joint_mesh):

        """
        :param beam_mesh:   compas Mesh of beam
        :param joint_mesh:  compas Mesh of joint
        """
        self.beam_mesh = beam_mesh
        self.joint_mesh = joint_mesh
        self.mesh = None

        #Perform initial calculation of the mesh (except when this is an empty object)
        if beam_mesh is not None:  
            self.update_boolean()
        
    def update_boolean(self):
        """Compute the boolean difference operation through trimesh.

        Returns
        -------
        object
            A compas.Mesh

        Note
        __
        The beam_mesh is updated with the new mesh
        """

        #constructing Trimesh from compas mesh
        # tri_beam = mesh_quads_to_triangles(self.beam_mesh)
        # tri_joint = mesh_quads_to_triangles(self.joint_mesh)

        mesh1_v = self.beam_mesh.to_vertices_and_faces()[0]
        mesh1_f = self.beam_mesh.to_vertices_and_faces()[1]  

        mesh2_v = self.joint_mesh.to_vertices_and_faces()[0]
        mesh2_f = self.joint_mesh.to_vertices_and_faces()[1]

        mesh_1 = trimesh.Trimesh(vertices=mesh1_v, faces=mesh1_f, process=False)
        mesh_2 = trimesh.Trimesh(vertices=mesh2_v, faces=mesh2_f, process=False)
        

        with Proxy('trimesh'):     
            boolean_sub = mesh_1.union(mesh_2,'blender')
            boolean_mesh = Mesh.from_vertices_and_faces(boolean_sub.vertices, boolean_sub.faces)
            self.mesh = boolean_mesh

        


if __name__ == '_main_':
    import compas 
    import os
    from compas.geometry import Frame
    from compas.geometry import Box 
    from compas.datastructures import Mesh

    #exporting file 
    HERE = os.path.dirname(_file_)
    DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
    FILE_O = os.path.join(DATA, 'compas_boolean_test_union.json')

    #construct the mesh
    box = Box(Frame.worldXY(),500,100,100)
    box_mesh = Mesh.from_vertices_and_faces(box.vertices, box.faces)

    box_2 = Box(([250,20,20], [300,0,100], [0,100,0]), 100, 50, 80)
    box_mesh_2 = Mesh.from_vertices_and_faces(box_2.vertices, box_2.faces)

    #call function
    mesh = Trimesh_proxy_subtract(box_mesh, box_mesh_2)

    b = mesh.mesh
    # b.to_json(FILE_O, pretty=True)
    print(b)