#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
build_dir="$repo_root/firmware/build/host"
cxx="${CXX:-c++}"
mkdir -p "$build_dir"
"$cxx" -std=c++17 -Wall -Wextra -Wpedantic -Werror \
  -fsanitize=address,undefined -fno-omit-frame-pointer -g \
  -I "$repo_root/firmware/core/include" \
  "$repo_root/firmware/core/color_transform.cpp" \
  "$repo_root/firmware/tests/color_transform_test.cpp" \
  -o "$build_dir/color_transform_test"
"$build_dir/color_transform_test"
