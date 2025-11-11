#pragma once

#include <igl/iterative_closest_point.h>
#include <igl/read_triangle_mesh.h>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <Eigen/Core>
#include <stdexcept>
#include <string>

std::pair<Eigen::Matrix3d, Eigen::Vector3d> icp_libigl(
    const Eigen::MatrixXd& VA, const Eigen::MatrixXi& FA,
    const Eigen::MatrixXd& VB, const Eigen::MatrixXi& FB,
    int num_samples = 2000, int max_iters = 30);

// Convenience: load two meshes from paths then run ICP
std::pair<Eigen::Matrix3d, Eigen::Vector3d> icp_libigl_from_paths(
    const std::string& path_a, const std::string& path_b,
    int num_samples = 2000, int max_iters = 30);