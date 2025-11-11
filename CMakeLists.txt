cmake_minimum_required(VERSION 3.5)

project(Bindings
	DESCRIPTION
		"Python bindings"
)

# allow duplicate custom targets defined in subprojects
# so that 'embree' and 'nanoflann' can both create target "uninstall"
set_property(GLOBAL PROPERTY ALLOW_DUPLICATE_CUSTOM_TARGETS TRUE)

# To make macOS with M3 chip happy
if (APPLE)
	# set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "Target specific architectures for macOS" FORCE)
	set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Target specific architectures for macOS" FORCE)
	# set(CMAKE_OSX_ARCHITECTURES "x86_64" CACHE STRING "Target specific architectures for macOS" FORCE)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
set(EXT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/ext")
set(UTILS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/utility")

#https://stackoverflow.com/q/46724267
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-march=native" COMPILER_SUPPORTS_MARCH_NATIVE)
if(COMPILER_SUPPORTS_MARCH_NATIVE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()

include(libigl)
# igl_include(glfw)
# igl_include(embree)

# # required by libpointmatcher
# include(libnabo)
# include(yaml-cpp)
# include(libpointmatcher)
# find_package(Boost REQUIRED)

include(pybind11)

# All libraries to link
set(PROJ_LIBS 
		igl::core 
		pybind11::module 
		Eigen3::Eigen 
		# pointmatcher
		${GL_LIBS}
)

# add src/cpp
add_library(cpp_src
	STATIC
	# Headers
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/non_rigid_alignment.h"
	"${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/icp_libigl.h"
	# Source
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/non_rigid_alignment.cpp"
	"${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/icp_libigl.cpp"
	)
target_link_libraries(cpp_src "${PROJ_LIBS}")
set_property(TARGET cpp_src PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
set_target_properties(cpp_src PROPERTIES LINKER_LANGUAGE CXX)

# src/cpp bindings
pybind11_add_module(pc_align_bindings
	"${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/icp_bindings.cpp"
)
target_link_libraries(pc_align_bindings PRIVATE cpp_src "${PROJ_LIBS}")
set_property(TARGET pc_align_bindings PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)