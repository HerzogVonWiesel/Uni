cmake_minimum_required(VERSION 3.16)
project(hdp_concurrent_linked_list)
set(CMAKE_CXX_STANDARD 17)

include(FetchContent)

# For this test task, we provide all tests and benchmarks, so we need to build them too.
option(CI_BUILD "Set to ON for complete build in CI." ON)

if(NOT CMAKE_BUILD_TYPE)
    message(STATUS "No build type specified. Defaulting to Debug.
                    Use cmake `-DCMAKE_BUILD_TYPE=Release ..` to build an optimized version.")
endif()

if (CMAKE_BUILD_TYPE MATCHES Release)
    message(STATUS "Building an optimized release version.")
    add_compile_options(-O3)
    if (CI_BUILD)
        # message(STATUS "Adding -march=native in CI")
        # We cannot set this generally, as it does not work on all architectures.
        # You can change this if you like to see if it works (will not work in Apple M1).
        # add_compile_options(-march=native)
    endif()
endif()

set(LINKED_LINK_SOURCES
        src/linked_list.cpp
        src/linked_list.hpp
        src/node.hpp
        )

add_library(linked_list ${LINKED_LINK_SOURCES})
target_include_directories(linked_list INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_compile_options(linked_list PUBLIC -pthread)
target_link_libraries(linked_list PUBLIC pthread)

enable_testing()
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG release-1.11.0
)

set(BUILD_GMOCK ON CACHE BOOL "" FORCE)
set(BUILD_GTEST ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(basic_test test/basic.cpp)
add_test(basic_test basic_test)
target_link_libraries(basic_test linked_list gtest gmock)


if (${CI_BUILD})
    # Build advanced tests in CI only
    add_executable(advanced_test test/advanced.cpp)
    add_test(advanced_test advanced_test)
    target_link_libraries(advanced_test linked_list gtest gmock)

    # Build benchmark in CI only
    FetchContent_Declare(
            google_benchmark
            GIT_REPOSITORY https://github.com/google/benchmark.git
            GIT_TAG v1.6.1
    )
    set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "Suppressing benchmark's tests" FORCE)
    FetchContent_MakeAvailable(google_benchmark)

    add_executable(hdp_benchmark test/benchmark.cpp)
    target_link_libraries(hdp_benchmark linked_list benchmark pthread)
endif()
