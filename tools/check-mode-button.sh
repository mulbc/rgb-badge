#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
build_dir="$repo_root/firmware/build/host"
cxx="${CXX:-c++}"
mkdir -p "$build_dir"
"$cxx" -std=c++17 -Wall -Wextra -Wpedantic -Werror \
  -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -g \
  -I "$repo_root/firmware/core/include" \
  "$repo_root/firmware/core/mode_button.cpp" \
  "$repo_root/firmware/tests/mode_button_test.cpp" \
  -o "$build_dir/mode_button_test"
"$build_dir/mode_button_test"
