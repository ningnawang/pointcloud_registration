
#pragma once
#include <pointmatcher/PointMatcher.h>

#include <random>

// -------------------------------
// Result container
// -------------------------------
struct SimilarityResult {
  Eigen::Matrix3d R;  // rotation
  Eigen::Vector3d t;  // translation
  double s;           // uniform scale
  Eigen::Matrix3d S;  // scale matrix = s * I
  Eigen::Matrix4d T;  // 4x4 homogeneous, maps B -> A
};

// -------------------------------
// ICP over meshes given as matrices
// -------------------------------
bool icp_libpointmatcher(const Eigen::MatrixXd& VA,
                         const Eigen::MatrixXi& FA,  // mesh A
                         const Eigen::MatrixXd& VB,
                         const Eigen::MatrixXi& FB,  // mesh B
                         SimilarityResult& out, int n_samples = 20000,
                         int max_iter = 100, double trim_ratio = 0.85);