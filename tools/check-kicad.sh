#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(CDPATH= cd -- "${script_dir}/.." && pwd)"
project_dir="${repo_root}/hardware/coupon/rev-a"
project_file="${project_dir}/rgb-badge-coupon.kicad_pro"
schematic_file="${project_dir}/rgb-badge-coupon.kicad_sch"
symbol_library="${project_dir}/symbols/rgb-badge-coupon.kicad_sym"
footprint_library="${project_dir}/footprints/rgb-badge-coupon.pretty"
led_library_check="${repo_root}/tools/check-led-libraries.py"

if [[ -n "${RGB_BADGE_KICAD_CLI:-}" ]]; then
    kicad_cli="${RGB_BADGE_KICAD_CLI}"
elif [[ -x "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" ]]; then
    kicad_cli="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
elif command -v kicad-cli >/dev/null 2>&1; then
    kicad_cli="$(command -v kicad-cli)"
else
    echo "KiCad CLI not found. Install stable KiCad 10.0.x or set RGB_BADGE_KICAD_CLI." >&2
    exit 2
fi

for required_path in \
    "${project_file}" \
    "${schematic_file}" \
    "${project_dir}/sym-lib-table" \
    "${project_dir}/fp-lib-table" \
    "${symbol_library}" \
    "${footprint_library}" \
    "${led_library_check}"
do
    if [[ ! -e "${required_path}" ]]; then
        echo "Required project path is missing: ${required_path}" >&2
        exit 2
    fi
done

python3 "${led_library_check}"

kicad_version="$("${kicad_cli}" version)"

case "${kicad_version}" in
    10.0.*)
        ;;
    *)
        echo "Expected stable KiCad 10.0.x; found ${kicad_version}." >&2
        exit 2
        ;;
esac

if [[ -n "${RGB_BADGE_KICAD_CHECK_OUTPUT:-}" ]]; then
    check_tmp_dir="${RGB_BADGE_KICAD_CHECK_OUTPUT}"
    if [[ -e "${check_tmp_dir}" ]]; then
        echo "RGB_BADGE_KICAD_CHECK_OUTPUT must name a path that does not exist: ${check_tmp_dir}" >&2
        exit 2
    fi
    mkdir -p -- "${check_tmp_dir}"
    keep_check_output=yes
else
    check_tmp_dir="$(mktemp -d)"
    keep_check_output=no
    trap 'rm -rf -- "${check_tmp_dir}"' EXIT
fi

symbol_svg_dir="${check_tmp_dir}/symbols"
footprint_svg_dir="${check_tmp_dir}/footprints"
mkdir -p -- "${symbol_svg_dir}" "${footprint_svg_dir}"

"${kicad_cli}" sym export svg \
    --black-and-white \
    --output "${symbol_svg_dir}" \
    "${symbol_library}"

"${kicad_cli}" fp export svg \
    --black-and-white \
    --sketch-pads-on-fab-layers \
    --layers "F.Cu,F.Mask,F.Paste,F.SilkS,F.Fab,F.CrtYd" \
    --output "${footprint_svg_dir}" \
    "${footprint_library}"

symbol_svg_count="$(find "${symbol_svg_dir}" -type f -name '*.svg' | wc -l | tr -d '[:space:]')"
footprint_svg_count="$(find "${footprint_svg_dir}" -type f -name '*.svg' | wc -l | tr -d '[:space:]')"
if (( symbol_svg_count < 2 )); then
    echo "Expected at least 2 exported symbol SVGs; found ${symbol_svg_count}." >&2
    exit 1
fi
if (( footprint_svg_count < 2 )); then
    echo "Expected exported SVGs for both LED footprints; found ${footprint_svg_count}." >&2
    exit 1
fi

"${kicad_cli}" sch erc \
    --severity-all \
    --exit-code-violations \
    --output "${check_tmp_dir}/coupon-erc.rpt" \
    "${schematic_file}"

echo "KiCad ${kicad_version}: LED libraries loaded/exported and Coupon Rev A ERC passed."
if [[ "${keep_check_output}" == yes ]]; then
    echo "Review SVG output in: ${check_tmp_dir}"
fi
