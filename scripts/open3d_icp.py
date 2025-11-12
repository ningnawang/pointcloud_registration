import open3d as o3d
import copy
from context import *
from open3d_utils import print_rt_from_transform, load_mesh_as_point_cloud


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw([source_temp, target_temp])

def point_to_point_icp(source, target, threshold):
    print("Apply point-to-point ICP")
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source, target, threshold, 
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint())
    print(reg_p2p)
    print("Transformation is:")
    print(reg_p2p.transformation, "\n")
    print_rt_from_transform(reg_p2p.transformation)
    # draw_registration_result(source, target, reg_p2p.transformation)

def point_to_plane_icp(source, target, threshold):
    print("Apply point-to-plane ICP")
    reg_p2l = o3d.pipelines.registration.registration_icp(
        source, target, threshold,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPlane())
    print(reg_p2l)
    print("Transformation is:")
    print(reg_p2l.transformation, "\n")
    print_rt_from_transform(reg_p2l.transformation)
    draw_registration_result(source, target, reg_p2l.transformation)

# To run:
# python open3d_icp.py ../data/mask.obj ../data/max_planck_face.obj
def main():
    parser = argparse.ArgumentParser(
        description="Rigidly align mesh A to mesh B using open3d"
    )
    parser.add_argument("mesh_source", type=str, help="Path to source mesh A")
    parser.add_argument("mesh_target", type=str, help="Path to target mesh B")
    parser.add_argument(
        "--samples",
        type=int,
        default=10000,
        help="Number of sampled points from mesh A per iteration (default 10000)",
    )
    args = parser.parse_args()

    source = load_mesh_as_point_cloud(args.mesh_source, n_points=args.samples)
    target = load_mesh_as_point_cloud(args.mesh_target, n_points=args.samples)
    threshold = 5000

    print("Initial alignment")
    evaluation = o3d.pipelines.registration.evaluate_registration(
        source, target, threshold)
    print(evaluation, "\n")

    # point_to_point_icp(source, target, threshold)
    point_to_plane_icp(source, target, threshold)


# To run:
# python open3d_icp.py ../data/mask.obj ../data/max_planck_face.obj
if __name__ == "__main__":
    main()
