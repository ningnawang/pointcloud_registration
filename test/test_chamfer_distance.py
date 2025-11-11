from .context import *

class TestChamferDistance(unittest.TestCase):
    def test_same_mesh_gives_zero(self):
        V1, F1 = gpy.read_mesh("data/bunny.obj")
        V2, F2 = gpy.read_mesh("data/bunny.obj")
        cd = utility.chamfer_distance(V1,F1,V2,F2)
        self.assertAlmostEqual(cd, 0.0, places=2)
    def test_same_mesh_converges_to_zero(self):
        V1, F1 = gpy.read_mesh("data/bunny.obj")
        V2, F2 = gpy.read_mesh("data/bunny.obj")
        cds = []
        ns = [10000, 100000, 1000000, 10000000]
        for n in ns:
            cd = utility.chamfer_distance(V1,F1,V2,F2,n=n)
            cds.append(cd)
            print("Chamfer distance with n=%d: %f" % (n, cd))
        # check that the chamfer distances decrease
        for i in range(len(cds)-1):
            self.assertTrue(cds[i+1] < cds[i])
    def test_something_else(self):
        pass
            