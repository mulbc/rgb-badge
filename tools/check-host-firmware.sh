#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
build_dir="$repo_root/firmware/build/cmake-host"
cxx="${CXX:-c++}"
cmake -S "$repo_root/firmware/host" -B "$build_dir" \
  -DCMAKE_CXX_COMPILER="$cxx" -DCMAKE_BUILD_TYPE=Debug \
  -DBUILD_TESTING=ON -DRGB_BADGE_SANITIZERS=ON
cmake --build "$build_dir" --parallel 2
ctest --test-dir "$build_dir" --output-on-failure --parallel 2
