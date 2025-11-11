import numpy as np
import gpytoolbox as gpy
from scipy.sparse.linalg import eigsh
import polyscope as ps
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import meshapprox
import utility