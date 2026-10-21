#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
build_dir="$repo_root/firmware/build/host"
cxx="${CXX:-c++}"
mkdir -p "$build_dir"
flags=(-std=c++17 -Wall -Wextra -Wpedantic -Werror
  -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -g
  -I "$repo_root/firmware/core/include")
sources=("$repo_root/firmware/core/asset_reader.cpp" "$repo_root/firmware/core/asset_playback.cpp")
"$cxx" "${flags[@]}" "${sources[@]}" "$repo_root/firmware/tests/asset_playback_test.cpp" -o "$build_dir/asset_playback_test"
"$build_dir/asset_playback_test"
"$cxx" "${flags[@]}" "${sources[@]}" "$repo_root/firmware/tests/asset_playback_cli.cpp" -o "$build_dir/asset_playback"
python3 "$repo_root/firmware/tests/test_asset_playback.py" --player "$build_dir/asset_playback"
