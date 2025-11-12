#!/usr/bin/env python3
import igl


def rigid_alignment_numpy(X, P):
    """
    Compute best-fit rigid transform (rotation R, translation t)
    that aligns points X to P: minimize || R*X_i + t - P_i ||^2
    """
    X_mean = X.mean(axis=0)
    P_mean = P.mean(axis=0)

    X_centered = X - X_mean
    P_centered = P - P_mean

    H = X_centered.T @ P_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # Handle reflection
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    t = P_mean - X_mean @ R
    return R, t


def rigid_align_meshes(path_a: str, path_b: str, iters: int = 10):
    # Load meshes
    VA, FA = igl.read_triangle_mesh(path_a)
    VB, FB = igl.read_triangle_mesh(path_b)

    # Target face normals for potential use with igl.rigid_alignment
    Z = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)
    FN = igl.per_face_normals(VB, FB, Z)

    X = VA.copy()
    R_total = np.eye(3)
    t_total = np.zeros((1, 3))

    use_igl_rigid = hasattr(igl, "rigid_alignment")
    if not use_igl_rigid:
        print("igl has no rigid_alignment(), fall back.")

    for _ in range(max(1, iters)):
        # Closest points on mesh B for each vertex of current X
        sqrD, I, C = igl.point_mesh_squared_distance(X, VB, FB)
        if use_igl_rigid:
            # Use libigl binding if available
            Ncorr = FN[I, :]
            R_step, t_step = igl.rigid_alignment(X, C, Ncorr)
        else:
            # Fallback to NumPy Kabsch
            R_step, t_step = rigid_alignment_numpy(X, C)

        # Compose transform and update X
        R_total = R_total @ R_step
        t_total = t_total @ R_step + t_step
        X = X @ R_step + t_step

    return R_total, t_total


def main():
    parser = argparse.ArgumentParser(
        description="Rigid align mesh A to mesh B and print R, t"
    )
    parser.add_argument("mesh_a", type=str, help="Path to source mesh A")
    parser.add_argument("mesh_b", type=str, help="Path to target mesh B")
    parser.add_argument("iters", type=int, nargs="?", default=10,
                        help="ICP iterations, default 10")
    args = parser.parse_args()

    R, t = rigid_align_meshes(args.mesh_a, args.mesh_b, args.iters)

    np.set_printoptions(precision=6, suppress=True)
    print("Rotation R (3x3):")
    print(R)
    print("\nTranslation t (1x3):")
    print(t)


if __name__ == "__main__":
    main()
