if(TARGET pointmatcher)
    return()
endif()

include(FetchContent)
FetchContent_Declare(
    libpointmatcher
    GIT_REPOSITORY https://github.com/norlab-ulaval/libpointmatcher.git
    GIT_TAG 1.4.4
)
FetchContent_MakeAvailable(libpointmatcher)



