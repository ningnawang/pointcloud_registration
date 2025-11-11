from .context import *

class TestApproximateMesh(unittest.TestCase):
    def test_more_eigenvectors_means_better(self):
        """ Test that using more eigenvectors gives a better approximation
        """
        eig_nums = np.linspace(10, 100, 10, dtype=int)
        test_mesh_paths = ["data/bunny.obj"]
        for mesh_path in test_mesh_paths:
            V, F = gpy.read_mesh(mesh_path)
            V_approx_list = []
            for k in eig_nums:
                V_approx = meshapprox.approximate_mesh(V, F, k=k)
                V_approx_list.append(V_approx)
            # check that the approximations get better as the number of eigenvalues grows
            for i in range(len(eig_nums)-1):
                err1 = np.linalg.norm(V - V_approx_list[i])
                err2 = np.linalg.norm(V - V_approx_list[i+1])
                self.assertTrue(err2 < err1)
    def test_something_else(self):
        pass