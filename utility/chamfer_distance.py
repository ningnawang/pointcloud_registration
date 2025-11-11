import gpytoolbox as gpy
import numpy as np

def chamfer_distance(v1,f1,v2,f2,n=1000000):
    P1 = gpy.random_points_on_mesh(v1,f1,n)
    P2 = gpy.random_points_on_mesh(v2,f2,n)
    d1 = gpy.squared_distance(P1,P2,use_aabb=True,use_cpp=True)[0]
    d2 = gpy.squared_distance(P2,P1,use_aabb=True,use_cpp=True)[0]
    return np.sqrt(np.mean(d1)) + np.sqrt(np.mean(d2))