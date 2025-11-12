from context import *
import open3d as o3d

def print_rt_from_transform(T):
    """
    Given a 4x4 transformation matrix T,
    print the rotation (3x3) and translation (3x1) components.
    """
    T = np.asarray(T)
    if T.shape != (4, 4):
        raise ValueError(f"Expected a 4x4 matrix, got shape {T.shape}")

    R = T[:3, :3]
    t = T[:3, 3]

    print("Rotation matrix (R):")
    print(np.array2string(R, precision=6, suppress_small=True))
    print("\nTranslation vector (t):")
    print(np.array2string(t, precision=6, suppress_small=True))

def load_mesh_as_point_cloud(path: str, n_points: int = 200000) -> o3d.geometry.PointCloud:
    """Load a mesh and sample a dense point cloud on its surface."""
    mesh = o3d.io.read_triangle_mesh(path)
    if mesh.is_empty():
        raise ValueError(f"Failed to load mesh: {path}")
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()
    # Poisson disk sampling gives better coverage than uniform
    pcd = mesh.sample_points_poisson_disk(number_of_points=n_points, init_factor=5)
    return pcd
