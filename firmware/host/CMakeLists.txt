# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.20)
project(rgb_badge_host LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
option(RGB_BADGE_SANITIZERS "Enable fail-fast address/undefined host sanitizers" ON)

if(NOT CMAKE_CXX_COMPILER_ID MATCHES "^(GNU|Clang|AppleClang)$")
  message(FATAL_ERROR "Host verification currently supports GNU and Clang-family compilers")
endif()
get_filename_component(REPO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../.." ABSOLUTE)

add_library(rgb_badge_host_options INTERFACE)
target_compile_options(rgb_badge_host_options INTERFACE -Wall -Wextra -Wpedantic -Werror)
if(RGB_BADGE_SANITIZERS)
  target_compile_options(rgb_badge_host_options INTERFACE
    -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer)
  target_link_options(rgb_badge_host_options INTERFACE
    -fsanitize=address,undefined -fno-sanitize-recover=all)
endif()

add_library(rgb_badge_core STATIC
  ../core/color_transform.cpp ../core/asset_reader.cpp ../core/asset_playback.cpp
  ../core/mode_button.cpp ../core/content_session.cpp)
target_include_directories(rgb_badge_core PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/../core/include")
target_compile_features(rgb_badge_core PUBLIC cxx_std_17)
target_compile_options(rgb_badge_core PRIVATE -fno-exceptions -fno-rtti)
target_link_libraries(rgb_badge_core PUBLIC rgb_badge_host_options)

add_executable(rgbb-inspect rgbb_inspect.cpp)
target_link_libraries(rgbb-inspect PRIVATE rgb_badge_core)

include(CTest)
if(BUILD_TESTING)
  find_package(Python3 3.9 REQUIRED COMPONENTS Interpreter)
  foreach(unit IN ITEMS color_transform asset_reader asset_playback mode_button content_session)
    add_executable(${unit}_test "../tests/${unit}_test.cpp")
    target_link_libraries(${unit}_test PRIVATE rgb_badge_core)
    add_test(NAME ${unit} COMMAND ${unit}_test)
  endforeach()
  foreach(adapter IN ITEMS asset_decode asset_playback content_session)
    add_executable(${adapter} "../tests/${adapter}_cli.cpp")
    target_link_libraries(${adapter} PRIVATE rgb_badge_core)
  endforeach()
  add_test(NAME asset_pipeline COMMAND "${Python3_EXECUTABLE}"
    "${REPO_ROOT}/firmware/tests/test_asset_pipeline.py" --decoder "$<TARGET_FILE:asset_decode>")
  add_test(NAME playback_pipeline COMMAND "${Python3_EXECUTABLE}"
    "${REPO_ROOT}/firmware/tests/test_asset_playback.py" --player "$<TARGET_FILE:asset_playback>")
  add_test(NAME session_pipeline COMMAND "${Python3_EXECUTABLE}"
    "${REPO_ROOT}/firmware/tests/test_content_session.py" --session "$<TARGET_FILE:content_session>")
  add_test(NAME asset_inspection COMMAND "${Python3_EXECUTABLE}"
    "${REPO_ROOT}/firmware/tests/test_asset_inspection.py" --inspector "$<TARGET_FILE:rgbb-inspect>")
  foreach(version IN ITEMS 1 2)
    add_test(NAME capacity_v${version} COMMAND "${CMAKE_COMMAND}"
      "-DPYTHON_EXECUTABLE=${Python3_EXECUTABLE}" "-DREPO_ROOT=${REPO_ROOT}"
      "-DOUTPUT_DIR=${CMAKE_CURRENT_BINARY_DIR}" "-DVERSION=${version}"
      -P "${CMAKE_CURRENT_SOURCE_DIR}/check_capacity.cmake")
  endforeach()
  get_property(host_tests DIRECTORY PROPERTY TESTS)
  set_tests_properties(${host_tests} PROPERTIES TIMEOUT 180)
endif()
