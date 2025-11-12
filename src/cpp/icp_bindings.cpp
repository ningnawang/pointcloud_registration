// icp_bindings.cpp
#include <pybind11/pybind11.h>

#include <Eigen/Core>

#include "icp_libigl.h"

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
}
