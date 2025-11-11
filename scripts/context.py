# These are the imports we're going to use in all scripts.
import sys, os, platform
import numpy as np
# import gpytoolbox as gpy
# from scipy.sparse.linalg import eigsh
# import polyscope as ps
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# import meshapprox
# import utility

# Get the operating system name and version
os_name = platform.system()
if os_name == "Darwin":
    # Get the macOS version
    os_version = platform.mac_ver()[0]
    # print("macOS version:", os_version)

    # Check if the macOS version is less than 14
    if os_version and os_version < "14":
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build-studio')))
    else:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build')))
else:
    # For non-macOS systems
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../build')))
import pc_align_bindings as pc_align
