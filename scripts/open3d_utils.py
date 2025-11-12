from context import *
import open3d as o3d
import plydata

def load_ply(file_name):
    ply_data = PlyData.read(file_name)
    vertices = ply_data["vertex"]
    vertices = np.vstack([vertices["x"], vertices["y"], vertices["z"]]).T
    data = {"vertices": vertices}

    faces = np.vstack(ply_data["face"]["vertex_indices"])
    data["faces"] = faces

    try:
        vertex_quality = np.vstack(ply_data["vertex"]["quality"])
        vertex_selection = np.float32(vertex_quality > 0)
        data["vertex_selection"] = vertex_selection
    except ValueError:
        data["vertex_selection"] = None
        print("The ply file %s does not contain quality property for vertex selection." % file_name)

    try:
        face_quality = np.vstack(ply_data["face"]["quality"])
        face_selection = np.float32(face_quality > 0)
        data["face_selection"] = face_selection
    except ValueError:
        data["face_selection"] = None
        print("The ply file %s does not contain quality property for face selection." % file_name)

    return data


def extract_selected_mesh(data):
    vertices = data["vertices"]
    faces = data["faces"]
    vsel = data["vertex_selection"]
    fsel = data["face_selection"]

    if fsel is not None:
        selected_faces = faces[fsel[:, 0] > 0]
        selected_vertices_idx = np.unique(selected_faces.flatten())
        selected_vertices = vertices[selected_vertices_idx]
        # Remap indices for Open3D
        index_map = np.zeros(len(vertices), dtype=int)
        index_map[selected_vertices_idx] = np.arange(len(selected_vertices))
        remapped_faces = np.array([[index_map[i] for i in f] for f in selected_faces])
        mesh = o3d.geometry.TriangleMesh(
            o3d.utility.Vector3dVector(selected_vertices),
            o3d.utility.Vector3iVector(remapped_faces),
        )
    elif vsel is not None:
        selected_vertices = vertices[vsel[:, 0] > 0]
        mask = np.isin(faces, np.where(vsel[:, 0] > 0)[0]).all(axis=1)
        remapped_faces = faces[mask]
        selected_vertices_idx = np.unique(remapped_faces.flatten())
        selected_vertices = vertices[selected_vertices_idx]
        index_map = np.zeros(len(vertices), dtype=int)
        index_map[selected_vertices_idx] = np.arange(len(selected_vertices))
        remapped_faces = np.array([[index_map[i] for i in f] for f in remapped_faces])
        mesh = o3d.geometry.TriangleMesh(
            o3d.utility.Vector3dVector(selected_vertices),
            o3d.utility.Vector3iVector(remapped_faces),
        )
    else:
        print("No selection annotation found, using full mesh.")
        mesh = o3d.geometry.TriangleMesh(
            o3d.utility.Vector3dVector(vertices),
            o3d.utility.Vector3iVector(faces),
        )

    return mesh


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


def load_mesh_subset_as_point_cloud(
    path: str,
    n_points: int = 50000,
    voxel_size: float | None = None,
    estimate_normals: bool = True,
) -> tuple[o3d.geometry.PointCloud, o3d.geometry.TriangleMesh]:

    ext = os.path.splitext(path)[1].lower()
    if ext == ".ply":
        data = load_ply(path)                     
        mesh = extract_selected_mesh(data)        
    else:
        mesh = o3d.io.read_triangle_mesh(path)

    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()
    if not mesh.has_triangle_normals():
        mesh.compute_triangle_normals()

    pcd = mesh.sample_points_poisson_disk(n_points)

    return pcd

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
