#include "non_rigid_alignment.h"

// -------------------------------
// Surface sampling (uniform by area)
// -------------------------------
inline Eigen::MatrixXd sample_mesh_surface(const Eigen::MatrixXd& V,
                                           const Eigen::MatrixXi& F,
                                           int n_samples,
                                           std::mt19937_64* rng_in = nullptr) {
  using Vec3 = Eigen::Vector3d;
  const int Tn = F.rows();

  // per-triangle areas and CDF
  Eigen::VectorXd area(Tn);
  for (int f = 0; f < Tn; ++f) {
    const Vec3 a = V.row(F(f, 0));
    const Vec3 b = V.row(F(f, 1));
    const Vec3 c = V.row(F(f, 2));
    area(f) = 0.5 * ((b - a).cross(c - a)).norm();
  }
  const double total = area.sum();
  Eigen::VectorXd cdf = area;
  for (int i = 1; i < Tn; ++i) cdf(i) += cdf(i - 1);
  if (total > 0) cdf.array() /= total;

  std::random_device rd;
  std::mt19937_64 rng = rng_in ? *rng_in : std::mt19937_64(rd());
  std::uniform_real_distribution<double> U(0.0, 1.0);

  Eigen::MatrixXd P(n_samples, 3);
  for (int k = 0; k < n_samples; ++k) {
    // triangle index by inverse CDF
    const double u = U(rng);
    const int f =
        int(std::lower_bound(cdf.data(), cdf.data() + Tn, u) - cdf.data());
    const Vec3 a = V.row(F(f, 0));
    const Vec3 b = V.row(F(f, 1));
    const Vec3 c = V.row(F(f, 2));
    // barycentric sampling
    const double r1 = std::sqrt(U(rng));
    const double r2 = U(rng);
    const Vec3 p = (1.0 - r1) * a + r1 * ((1.0 - r2) * b + r2 * c);
    P.row(k) = p.transpose();
  }
  return P;
}

// -------------------------------
// Convert Nx3 points to DataPoints (homogeneous, column-major)
// -------------------------------
inline auto points_to_datapoints(const Eigen::MatrixXd& P) {
  using PM = PointMatcher<double>;
  using DP = PM::DataPoints;
  const int N = static_cast<int>(P.rows());
  Eigen::MatrixXd feats(4, N);
  feats.topRows<3>() = P.transpose();
  feats.row(3).setOnes();
  return DP(feats);
}

bool icp_libpointmatcher(const Eigen::MatrixXd& VA,
                         const Eigen::MatrixXi& FA,  // mesh A
                         const Eigen::MatrixXd& VB,
                         const Eigen::MatrixXi& FB,  // mesh B
                         SimilarityResult& out, int n_samples = 20000,
                         int max_iter = 100, double trim_ratio = 0.85) {
  using PM = PointMatcher<double>;
  using DP = PM::DataPoints;

  if (VA.rows() == 0 || FA.rows() == 0 || VB.rows() == 0 || FB.rows() == 0)
    return false;

  // 1) sample surfaces
  const Eigen::MatrixXd A_pts = sample_mesh_surface(VA, FA, n_samples);
  const Eigen::MatrixXd B_pts = sample_mesh_surface(VB, FB, n_samples);

  // 2) wrap as DataPoints
  DP ref = points_to_datapoints(A_pts);  // target
  DP src = points_to_datapoints(B_pts);  // source

  // 3) build ICP pipeline
  PM::ICP icp;

  // optional: light filtering on both clouds
  {
    auto* mindist_r = PM::get().DataPointsFilterRegistrar.create(
        "MinDistDataPointsFilter", {{"minDist", "1e-9"}});
    auto* random_r = PM::get().DataPointsFilterRegistrar.create(
        "RandomSamplingDataPointsFilter", {{"prob", "0.5"}});
    icp.readingDataPointsFilters.push_back(mindist_r);
    icp.readingDataPointsFilters.push_back(random_r);

    auto* mindist_t = PM::get().DataPointsFilterRegistrar.create(
        "MinDistDataPointsFilter", {{"minDist", "1e-9"}});
    auto* random_t = PM::get().DataPointsFilterRegistrar.create(
        "RandomSamplingDataPointsFilter", {{"prob", "0.5"}});
    icp.referenceDataPointsFilters.push_back(mindist_t);
    icp.referenceDataPointsFilters.push_back(random_t);
  }

  // matcher
  icp.matcher = PM::get().MatcherRegistrar.create(
      "KDTreeMatcher", {{"knn", "1"}, {"epsilon", "0.0"}});

  // outlier filter
  icp.outlierFilters.push_back(PM::get().OutlierFilterRegistrar.create(
      "TrimmedDistOutlierFilter", {{"ratio", std::to_string(trim_ratio)}}));

  // similarity error minimizer
  icp.errorMinimizer = PM::get().ErrorMinimizerRegistrar.create(
      "PointToPointSimilarityErrorMinimizer");

  // stopping
  icp.transformationCheckers.push_back(
      PM::get().TransformationCheckerRegistrar.create(
          "CounterTransformationChecker",
          {{"maxIterationCount", std::to_string(max_iter)}}));
  icp.transformationCheckers.push_back(
      PM::get().TransformationCheckerRegistrar.create(
          "DifferentialTransformationChecker", {{"minDiffRotErr", "1e-6"},
                                                {"minDiffTransErr", "1e-6"},
                                                {"smoothLength", "4"}}));

  // apply similarity transforms
  icp.transformations.push_back(
      PM::get().TransformationRegistrar.create("SimilarityTransformation"));

  // 4) run ICP: T maps B -> A
  const PM::TransformationParameters Tpm = icp(src, ref);  // 4x4
  const Eigen::Matrix4d T = Tpm.cast<double>();

  // 5) decompose T into s, R, t with T(0:3,0:3) = s * R
  Eigen::Matrix3d A = T.topLeftCorner<3, 3>();
  Eigen::Vector3d t = T.topRightCorner<3, 1>();

  const double s = (A.col(0).norm() + A.col(1).norm() + A.col(2).norm()) / 3.0;
  Eigen::Matrix3d R = (s != 0.0) ? (A / s) : A;

  // small orthogonalization for numerical stability
  Eigen::JacobiSVD<Eigen::Matrix3d> svd(
      R, Eigen::ComputeFullU | Eigen::ComputeFullV);
  R = svd.matrixU() * svd.matrixV().transpose();
  double s_fixed = s;
  if (R.determinant() < 0.0) {
    Eigen::Matrix3d U = svd.matrixU();
    U.col(2) *= -1.0;
    R = U * svd.matrixV().transpose();
    s_fixed *= -1.0;
  }

  // 6) fill output
  out.R = R;
  out.t = t;
  out.s = s_fixed;
  out.S = Eigen::Matrix3d::Identity() * s_fixed;
  out.T.setIdentity();
  out.T.topLeftCorner<3, 3>() = out.S * out.R;
  out.T.topRightCorner<3, 1>() = out.t;

  return true;
}
