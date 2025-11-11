import numpy as np
import gpytoolbox as gpy
from scipy.sparse.linalg import eigsh

def approximate_mesh(V, F, k=100):
    """
    Approximate a mesh using the first k eigenvectors of its Laplacian.

    Parameters:
    V : (n, 3) array
        Vertex positions of the mesh.
    F : (m, 3) array
        Face indices of the mesh.
    k : int
        Number of eigenvectors to use for approximation.

    Returns:
    V_approx : (n, 3) array
        Approximated vertex positions.
    """
    # compute the Laplacian
    L = gpy.cotangent_laplacian(V, F)

    # find the first k eigenvalues and eigenvectors of the Laplacian
    eigenvalues, eigenvectors = eigsh(L, k=k, which='SM')

    # project vertex positions onto the eigenvectors
    V_approx = eigenvectors @ (eigenvectors.T @ V)

    return V_approx