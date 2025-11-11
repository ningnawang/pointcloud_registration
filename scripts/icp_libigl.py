#!/usr/bin/env python3
import argparse
import igl
import numpy as np
from context import *

def main():
    parser = argparse.ArgumentParser(
        description="Rigidly align mesh A to mesh B using libigl::iterative_closest_point()"
    )
    parser.add_argument("mesh_a", type=str, help="Path to source mesh A")
    parser.add_argument("mesh_b", type=str, help="Path to target mesh B")
    parser.add_argument(
        "--samples",
        type=int,
        default=2000,
        help="Number of sampled points from mesh A per iteration (default 2000)",
    )
    parser.add_argument(
        "--iters",
        type=int,
        default=30,
        help="Maximum number of ICP iterations (default 30)",
    )
    args = parser.parse_args()

    R, t = pc_align.icp_libigl_from_paths(
        args.mesh_a, args.mesh_b, args.samples, args.iters
    )

    np.set_printoptions(precision=6, suppress=True)
    print("Rotation matrix R (3x3):")
    print(R)
    print("\nTranslation vector t (1x3):")
    print(t)


if __name__ == "__main__":
    main()
