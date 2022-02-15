cmake_minimum_required(VERSION 3.18)

project(mypackage VERSION "0.1" LANGUAGES CXX)

option(SKBUILD "Should be ON of being build by skbuild, 
and OFF of being build by regular cmake" OFF)

option(BUILD_PYTHON "ON if building python interface" ON)
  
option(USE_CPM "ON if to use CMake Package Manager" ON)

if (NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)
endif()

if (USE_CPM)
  include(cmake/CPM.cmake)
  CPMAddPackage(
    NAME xtl
    VERSION 0.7.4
    GITHUB_REPOSITORY "xtensor-stack/xtl"
    GIT_TAG "0.7.4"
    EXCLUDE_FROM_ALL ON
  )
  CPMAddPackage(
    NAME xtensor
    VERSION 0.24.0
    GITHUB_REPOSITORY "xtensor-stack/xtensor"
    GIT_TAG "0.24.0"
    EXCLUDE_FROM_ALL ON
  )
else ()
  find_package(xtl REQUIRED)
  find_package(xtensor REQUIRED)
endif ()

add_library(example src/example.cpp)
target_link_libraries(example PUBLIC xtensor)

add_subdirectory(test)

if (BUILD_PYTHON)
  
  if (NOT SKBUILD)
    set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/")
  endif()

  find_package(NumPy REQUIRED)
  if (USE_CPM)
    CPMAddPackage(
      NAME pybind11
      VERSION 2.9.1
      GITHUB_REPOSITORY "pybind/pybind11"
      GIT_TAG "v2.9.1"
      EXCLUDE_FROM_ALL ON
    )
    CPMAddPackage(
      NAME xtensor-python
      VERSION 0.26.0
      GITHUB_REPOSITORY "xtensor-stack/xtensor-python"
      GIT_TAG "0.26.0"
      EXCLUDE_FROM_ALL ON
    )
  else ()
    find_package(pybind11 REQUIRED)
    find_package(xtensor-python REQUIRED)
  endif ()

  pybind11_add_module(_example MODULE mypackage/wrapper.cpp)
  target_link_libraries(_example PUBLIC xtensor-python pybind11::module example)
  target_include_directories(_example PUBLIC ${NumPy_INCLUDE_DIRS} src)

  if (SKBUILD)
    install(TARGETS _example DESTINATION mypackage)
  else()
    install(TARGETS _example DESTINATION ${CMAKE_SOURCE_DIR}/mypackage)
  endif()
  
endif()

