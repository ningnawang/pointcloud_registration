import open3d as o3d
from context import *
from open3d_utils import print_rt_from_transform, load_mesh_as_point_cloud, load_mesh_subset_as_point_cloud

def preprocess_point_cloud(pcd, voxel_size):
    pcd_down = pcd.voxel_down_sample(voxel_size)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2.0,
                                             max_nn=30))
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 5.0,
                                             max_nn=100))
    return (pcd_down, pcd_fpfh)


# To run:
#  python open3d_registration_fgr.py ../data/mask.obj ../data/max_planck_face.obj
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Global point cloud registration example with RANSAC')
    parser.add_argument("mesh_source", type=str, help="Path to source mesh A")
    parser.add_argument("mesh_target", type=str, help="Path to target mesh B")
    parser.add_argument(
        "--samples",
        type=int,
        default=10000,
        help="Number of sampled points from mesh A per iteration (default 10000)",
    )
    parser.add_argument('--voxel_size',
                        type=float,
                        default=0.01,
                        help='voxel size in meter used to downsample inputs')
    parser.add_argument(
        '--distance_multiplier',
        type=float,
        default=1.5,
        help='multipler used to compute distance threshold'
        'between correspondences.'
        'Threshold is computed by voxel_size * distance_multiplier.')
    parser.add_argument('--max_iterations',
                        type=int,
                        default=64,
                        help='number of max FGR iterations')
    parser.add_argument(
        '--max_tuples',
        type=int,
        default=1000,
        help='max number of accepted tuples for correspondence filtering')

    args = parser.parse_args()


    voxel_size = args.voxel_size
    distance_threshold = args.distance_multiplier * voxel_size

    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
    print('Reading inputs')
    src = load_mesh_as_point_cloud(args.mesh_source, n_points=args.samples)
    # dst = load_mesh_as_point_cloud(args.mesh_target, n_points=args.samples)
    dst = load_mesh_subset_as_point_cloud(args.mesh_target, n_points=args.samples)

    print('Downsampling inputs')
    src_down, src_fpfh = preprocess_point_cloud(src, voxel_size)
    dst_down, dst_fpfh = preprocess_point_cloud(dst, voxel_size)

    print('Running FGR')
    result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        src_down, dst_down, src_fpfh, dst_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold,
            iteration_number=args.max_iterations,
            maximum_tuple_count=args.max_tuples))

    print("Transformation is:")
    print(result.transformation, "\n")
    print_rt_from_transform(result.transformation)

    src.paint_uniform_color([1, 0, 0])
    dst.paint_uniform_color([0, 1, 0])
    o3d.visualization.draw([src.transform(result.transformation), dst])