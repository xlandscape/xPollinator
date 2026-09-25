"""Write the parameters of a GAP preset into one or more xPollinator .xrun files.

Usage:
    python scripts/apply_gap.py <gap_id> <file.xrun> [<file.xrun> ...]
    python scripts/apply_gap.py --list

GAP presets live in model/variant/gaps.json. Each preset bundles the exposure parameters of a
crop use (application rate, residue concentrations, application window, exposure period) with the
toxicity endpoints of the substance (LD50s, slopes, DT50, RUD). The script inserts or replaces the
corresponding <Parameter> elements in the .xrun files and records the preset id in a <GAP> element.
Existing elements that are not part of the preset are left untouched.
"""
import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GAPS_FILE = os.path.join(REPO_ROOT, "model", "variant", "gaps.json")


def load_gaps(path: str = GAPS_FILE) -> dict:
    with open(path, encoding="utf-8") as fh:
        catalog = json.load(fh)
    return {gap["id"]: gap for gap in catalog["gaps"]}


def gap_params(gap_id: str, path: str = GAPS_FILE) -> dict:
    """Return the .xrun parameters of a preset as a dict of strings, including the GAP id itself."""
    gaps = load_gaps(path)
    if gap_id not in gaps:
        raise KeyError(f"Unknown GAP '{gap_id}'. Available: {', '.join(sorted(gaps))}")
    params = {"GAP": gap_id}
    params.update({key: _format(value) for key, value in gaps[gap_id]["params"].items()})
    return params


def _format(value) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def apply_to_xrun(xrun_path: str, params: dict) -> None:
    tree = ET.parse(xrun_path)
    root = tree.getroot()
    for key, value in params.items():
        element = root.find(key)
        if element is None:
            element = ET.SubElement(root, key)
        element.text = value
    ET.indent(root, space="  ")
    with open(xrun_path, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fh.write(ET.tostring(root, encoding="unicode"))
        fh.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("gap_id", nargs="?", help="Preset id from model/variant/gaps.json")
    parser.add_argument("xrun", nargs="*", help=".xrun files to update in place")
    parser.add_argument("--list", action="store_true", help="List available presets and exit")
    args = parser.parse_args()

    if args.list or not args.gap_id:
        for gap_id, gap in load_gaps().items():
            print(f"{gap_id:32s} {gap['label']}")
        return 0
    if not args.xrun:
        parser.error("no .xrun files given")

    params = gap_params(args.gap_id)
    for xrun_path in args.xrun:
        apply_to_xrun(xrun_path, params)
        print(f"updated: {xrun_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
