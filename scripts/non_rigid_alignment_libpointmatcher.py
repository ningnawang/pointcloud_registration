from context import *

meshA = trimesh.load_mesh("meshA.obj", process=False)
meshB = trimesh.load_mesh("meshB.obj", process=False)

VA = np.asarray(meshA.vertices, dtype=np.float64)
FA = np.asarray(meshA.faces, dtype=np.int32)
VB = np.asarray(meshB.vertices, dtype=np.float64)
FB = np.asarray(meshB.faces, dtype=np.int32)

res = icp_similarity.icp_libpointmatcher(VA, FA, VB, FB,
                                                    n_samples=20000,
                                                    max_iter=100,
                                                    trim_ratio=0.85)
print("Scale:", res["s"])
print("Rotation:\n", res["R"])
print("Translation:", res["t"])
