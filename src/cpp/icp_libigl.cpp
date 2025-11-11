#include "icp_libigl.h"

// Core: return (R, t) with t as Eigen::Vector3d (column)
std::pair<Eigen::Matrix3d, Eigen::Vector3d> icp_libigl(
    const Eigen::MatrixXd& VA, const Eigen::MatrixXi& FA,
    const Eigen::MatrixXd& VB, const Eigen::MatrixXi& FB, int num_samples,
    int max_iters) {
  if (VA.cols() != 3 || VB.cols() != 3) {
    throw std::runtime_error("Meshes must have V.cols()==3");
  }
  if (FA.cols() != 3 || FB.cols() != 3) {
    throw std::runtime_error("Triangle meshes required (F.cols()==3)");
  }

  Eigen::Matrix3d R;
  Eigen::RowVector3d t_row;
  igl::iterative_closest_point(VA, FA, VB, FB, num_samples, max_iters, R,
                               t_row);

  Eigen::Vector3d t = t_row.transpose();  // return column vector for pybind11
  return {R, t};
}

std::pair<Eigen::Matrix3d, Eigen::Vector3d> icp_libigl_from_paths(
    const std::string& path_a, const std::string& path_b, int num_samples,
    int max_iters) {
  Eigen::MatrixXd VA, VB;
  Eigen::MatrixXi FA, FB;
  if (!igl::read_triangle_mesh(path_a, VA, FA)) {
    throw std::runtime_error("Failed to read mesh A: " + path_a);
  }
  if (!igl::read_triangle_mesh(path_b, VB, FB)) {
    throw std::runtime_error("Failed to read mesh B: " + path_b);
  }
  return icp_libigl(VA, FA, VB, FB, num_samples, max_iters);
}
