// icp_bindings.cpp
#include <pybind11/pybind11.h>

#include <Eigen/Core>

#include "icp_libigl.h"
// #include "non_rigid_alignment.h"

namespace py = pybind11;

#include <pybind11/pybind11.h>
namespace py = pybind11;

PYBIND11_MODULE(pc_align_bindings, m) {
  m.doc() = "ICP wrapper over libigl::iterative_closest_point";

  m.def("icp_libigl", &icp_libigl, py::arg("VA"), py::arg("FA"), py::arg("VB"),
        py::arg("FB"), py::arg("num_samples") = 2000,
        py::arg("max_iters") = 30);

  m.def("icp_libigl_from_paths", &icp_libigl_from_paths, py::arg("mesh_a_path"),
        py::arg("mesh_b_path"), py::arg("num_samples") = 2000,
        py::arg("max_iters") = 30);

  //   m.def(
  //       "icp_libpointmatcher",
  //       [](const Eigen::MatrixXd& VA, const Eigen::MatrixXi& FA,
  //          const Eigen::MatrixXd& VB, const Eigen::MatrixXi& FB, int
  //          n_samples, int max_iter, double trim_ratio) {
  //         SimilarityResult res;
  //         bool ok = icp_libpointmatcher(VA, FA, VB, FB, res, n_samples,
  //         max_iter,
  //                                       trim_ratio);
  //         if (!ok) {
  //           throw std::runtime_error(
  //               "ICP registration failed or invalid mesh input");
  //         }

  //         return py::dict("R"_a = res.R, "t"_a = res.t, "s"_a = res.s,
  //                         "S"_a = res.S, "T"_a = res.T);
  //       },
  //       py::arg("VA"), py::arg("FA"), py::arg("VB"), py::arg("FB"),
  //       py::arg("n_samples") = 20000, py::arg("max_iter") = 100,
  //       py::arg("trim_ratio") = 0.85);
}
