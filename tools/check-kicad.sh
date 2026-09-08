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
numbered_review="${repo_root}/tools/number-footprint-review.py"
matrix_check="${repo_root}/tools/check-coupon-matrix.py"
driver_check="${repo_root}/tools/check-coupon-driver.py"

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
    "${led_library_check}" \
    "${numbered_review}" \
    "${matrix_check}" \
    "${driver_check}"
do
    if [[ ! -e "${required_path}" ]]; then
        echo "Required project path is missing: ${required_path}" >&2
        exit 2
    fi
done

python3 "${led_library_check}"
python3 "${matrix_check}"
python3 "${driver_check}"

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
footprint_fab_dir="${check_tmp_dir}/footprints/fabrication"
footprint_copper_dir="${check_tmp_dir}/footprints/copper"
footprint_numbered_dir="${check_tmp_dir}/footprints/numbered"
footprint_paste_dir="${check_tmp_dir}/footprints/paste"
mkdir -p -- "${symbol_svg_dir}" "${footprint_fab_dir}" "${footprint_copper_dir}" "${footprint_numbered_dir}" "${footprint_paste_dir}"

"${kicad_cli}" sym export svg \
    --black-and-white \
    --output "${symbol_svg_dir}" \
    "${symbol_library}"

# Preserve the raw fabrication export; body outlines may cross tiny numbers.
"${kicad_cli}" fp export svg \
    --black-and-white \
    --sketch-pads-on-fab-layers \
    --layers "F.Fab,F.SilkS,F.CrtYd" \
    --output "${footprint_fab_dir}" \
    "${footprint_library}"

# Only this view represents copper; fab outlines are not electrical connections.
"${kicad_cli}" fp export svg \
    --black-and-white \
    --layers "F.Cu" \
    --output "${footprint_copper_dir}" \
    "${footprint_library}"

# Separate paste view exposes the QFN thermal-pad stencil segmentation.
"${kicad_cli}" fp export svg \
    --black-and-white \
    --layers "F.Paste" \
    --output "${footprint_paste_dir}" \
    "${footprint_library}"

for expected_svg in \
    "${symbol_svg_dir}/EAST10105RGBA0_unit1.svg" \
    "${symbol_svg_dir}/QBLP1515A-RGB2A_unit1.svg" \
    "${footprint_fab_dir}/LED_Everlight_EAST10105RGBA0.svg" \
    "${footprint_fab_dir}/LED_QTBrightek_QBLP1515A-RGB2A.svg" \
    "${footprint_copper_dir}/LED_Everlight_EAST10105RGBA0.svg" \
    "${footprint_copper_dir}/LED_QTBrightek_QBLP1515A-RGB2A.svg"
do
    if [[ ! -s "${expected_svg}" ]]; then
        echo "Expected non-empty SVG was not exported: ${expected_svg}" >&2
        exit 1
    fi
done

for symbol_name in TLC59581RTQT ERJ-2RKF3922X ERJ-2RKF1003X GRM155R71C104KA88D PWR_FLAG TestPoint_Pad; do
    if [[ ! -s "${symbol_svg_dir}/${symbol_name}_unit1.svg" ]]; then
        echo "Expected non-empty driver symbol SVG: ${symbol_name}" >&2
        exit 1
    fi
done
for footprint_name in QFN_TI_RTQ0056E_8x8mm_P0.5mm_EP5.7mm R_Panasonic_ERJ2_0402 C_Murata_GRM15_0402; do
    for view_dir in "${footprint_fab_dir}" "${footprint_copper_dir}" "${footprint_paste_dir}"; do
        if [[ ! -s "${view_dir}/${footprint_name}.svg" ]]; then
            echo "Expected non-empty driver footprint SVG: ${view_dir}/${footprint_name}.svg" >&2
            exit 1
        fi
    done
done

# The bare copper probe pad intentionally has no paste aperture.
for view_dir in "${footprint_fab_dir}" "${footprint_copper_dir}"; do
    if [[ ! -s "${view_dir}/TestPoint_Pad_D1.0mm.svg" ]]; then
        echo "Expected non-empty test-pad footprint SVG: ${view_dir}" >&2
        exit 1
    fi
done

for footprint_name in LED_Everlight_EAST10105RGBA0 LED_QTBrightek_QBLP1515A-RGB2A; do
    python3 "${numbered_review}" \
        "${footprint_fab_dir}/${footprint_name}.svg" \
        "${footprint_numbered_dir}/${footprint_name}.svg"
done

"${kicad_cli}" sch erc \
    --severity-all \
    --exit-code-violations \
    --output "${check_tmp_dir}/coupon-erc.rpt" \
    "${schematic_file}"

"${kicad_cli}" sch export netlist \
    --format kicadxml \
    --output "${check_tmp_dir}/coupon-matrix.xml" \
    "${schematic_file}"
python3 "${matrix_check}" --netlist "${check_tmp_dir}/coupon-matrix.xml"
python3 "${driver_check}" --netlist "${check_tmp_dir}/coupon-matrix.xml"

"${kicad_cli}" sch export pdf \
    --black-and-white \
    --output "${check_tmp_dir}/coupon-schematic.pdf" \
    "${schematic_file}"
if [[ ! -s "${check_tmp_dir}/coupon-schematic.pdf" ]]; then
    echo "Expected non-empty schematic PDF was not exported." >&2
    exit 1
fi

echo "KiCad ${kicad_version}: libraries exported, complete matrix/driver connectivity and Coupon Rev A ERC passed."
echo "Matrix/driver draft: row stages, controller and power source remain uncaptured; supply flags are draft boundary assumptions."
if [[ "${keep_check_output}" == yes ]]; then
    echo "Review SVG/PDF output and netlist in: ${check_tmp_dir}"
fi
