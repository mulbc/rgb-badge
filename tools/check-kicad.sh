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
    "${footprint_library}"
do
    if [[ ! -e "${required_path}" ]]; then
        echo "Required project path is missing: ${required_path}" >&2
        exit 2
    fi
done

kicad_version="$("${kicad_cli}" version)"

case "${kicad_version}" in
    10.0.*)
        ;;
    *)
        echo "Expected stable KiCad 10.0.x; found ${kicad_version}." >&2
        exit 2
        ;;
esac

check_tmp_dir="$(mktemp -d)"
trap 'rm -rf -- "${check_tmp_dir}"' EXIT

"${kicad_cli}" sch erc \
    --severity-all \
    --exit-code-violations \
    --output "${check_tmp_dir}/coupon-erc.rpt" \
    "${schematic_file}"

echo "KiCad ${kicad_version}: Coupon Rev A schematic loaded and ERC passed."
