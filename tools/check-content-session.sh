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
sources=("$repo_root/firmware/core/asset_reader.cpp" "$repo_root/firmware/core/asset_playback.cpp"
  "$repo_root/firmware/core/color_transform.cpp" "$repo_root/firmware/core/mode_button.cpp"
  "$repo_root/firmware/core/content_session.cpp")
"$cxx" "${flags[@]}" "${sources[@]}" "$repo_root/firmware/tests/content_session_test.cpp" -o "$build_dir/content_session_test"
"$build_dir/content_session_test"
"$cxx" "${flags[@]}" "${sources[@]}" "$repo_root/firmware/tests/content_session_cli.cpp" -o "$build_dir/content_session"
python3 "$repo_root/firmware/tests/test_content_session.py" --session "$build_dir/content_session"
