#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reject every KiCad ERC violation except the staged USB boundary pair."""

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


SUMMARY = re.compile(r"\*\* ERC messages: (\d+)  Errors (\d+)  Warnings (\d+)")
HEADER = re.compile(r"^\[([^]]+)\]: (.+)$")
SHEET = re.compile(r"^\*\*\*\*\* Sheet (.+)$")
LOCATION = re.compile(r"^\s*@\(([^)]+)\): (.+)$")


@dataclass(frozen=True)
class Violation:
    sheet: str
    rule: str
    message: str
    severity: str
    location: str
    item: str


EXPECTED_USB_BOUNDARIES = {
    Violation("/", "isolated_pin_label", "Label connected to only one pin", "warning",
              "350.52 mm, 66.04 mm", "Global Label 'USB_D-'"),
    Violation("/", "isolated_pin_label", "Label connected to only one pin", "warning",
              "350.52 mm, 81.28 mm", "Global Label 'USB_D+'"),
}


def parse_report(text: str) -> tuple[tuple[int, int, int], list[Violation]]:
    summary_match = SUMMARY.search(text)
    if not summary_match:
        raise ValueError("ERC report has no parseable summary")

    current_sheet = ""
    records: list[Violation] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        sheet_match = SHEET.match(lines[index])
        if sheet_match:
            current_sheet = sheet_match.group(1)
            index += 1
            continue
        header_match = HEADER.match(lines[index])
        if not header_match:
            index += 1
            continue

        rule, message = header_match.groups()
        severity = location = item = ""
        index += 1
        while index < len(lines) and not HEADER.match(lines[index]) and not SHEET.match(lines[index]):
            stripped = lines[index].strip()
            if stripped.startswith(";"):
                severity = stripped.removeprefix(";").strip()
            location_match = LOCATION.match(lines[index])
            if location_match:
                location, item = location_match.groups()
            index += 1
        records.append(Violation(current_sheet, rule, message, severity, location, item))

    return tuple(map(int, summary_match.groups())), records


def check_report(path: Path) -> str:
    summary, records = parse_report(path.read_text(encoding="utf-8"))
    total, errors, warnings = summary
    if total != len(records):
        raise ValueError(f"ERC summary says {total} messages but {len(records)} were parsed")
    if errors != sum(record.severity == "error" for record in records):
        raise ValueError("ERC error count does not match the parsed records")
    if warnings != sum(record.severity == "warning" for record in records):
        raise ValueError("ERC warning count does not match the parsed records")

    actual = set(records)
    if not actual:
        return "ERC report check passed: 0 violations."
    if actual == EXPECTED_USB_BOUNDARIES and errors == 0 and warnings == 2:
        return ("ERC report check passed with 2 temporary USB-boundary warnings: "
                "USB_D- and USB_D+ are intentionally awaiting the power/input sheet.")

    details = "\n".join(f"- {record}" for record in records)
    raise ValueError("Unexpected ERC violation set:\n" + details)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        print(check_report(args.report))
    except (OSError, ValueError) as error:
        raise SystemExit(f"ERC report check failed: {error}") from error


if __name__ == "__main__":
    main()
