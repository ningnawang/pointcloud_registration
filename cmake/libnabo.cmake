if(TARGET yaml-cpp)
    return()
endif()

set(YAML_CPP_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(BUILD_SHARED_LIBS ON CACHE BOOL "" FORCE)

include(FetchContent)
FetchContent_Declare(yaml-cpp
  GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
  GIT_TAG 0.8.0
)
FetchContent_MakeAvailable(yaml-cpp)
# Make sure downstream find_package(yaml-cpp CONFIG) resolves to the build dir
set(yaml-cpp_DIR "${yaml-cpp_BINARY_DIR}" CACHE PATH "" FORCE)
