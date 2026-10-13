"""Add the BEEHAVE weather/season parameters to existing .xrun files.

Usage:
    python scripts/update_xrun_weather.py <file.xrun> [<file.xrun> ...]

Since the SETAC 2026 changes, mc.xml requires SunshineHours and
SeasonHoPoMoRepX1..5 in every .xrun file. This script copies the values of
those elements from template.xrun into each given file, inserting them after
the <BeeHaveWeather> (or <BeeHaveWeatherFile>) element. Elements that already
exist are left untouched, as is the rest of the file (comments and formatting
are preserved).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE = os.path.join(REPO_ROOT, "template.xrun")
WEATHER_KEYS = [
    "SunshineHours",
    "SeasonHoPoMoRepX1",
    "SeasonHoPoMoRepX2",
    "SeasonHoPoMoRepX3",
    "SeasonHoPoMoRepX4",
    "SeasonHoPoMoRepX5",
]


def template_weather_params(template: str = TEMPLATE) -> dict[str, str]:
    """Return the weather/season parameters of template.xrun as {tag: text}."""
    root = ET.parse(template).getroot()
    params = {}
    for key in WEATHER_KEYS:
        el = root.find(key)
        if el is None or not (el.text or "").strip():
            raise ValueError(f"{template} has no <{key}> element")
        params[key] = el.text
    return params


def update_xrun(path: str, params: dict[str, str]) -> list[str]:
    """Insert missing weather elements into one .xrun file; return the added tags."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    missing = [key for key in WEATHER_KEYS if not re.search(rf"<{key}>", text)]
    if not missing:
        return []
    anchor = re.search(r"^([ \t]*)<BeeHaveWeatherFile>.*?</BeeHaveWeatherFile>[ \t]*\r?\n", text, flags=re.M | re.S)
    if anchor is None:
        anchor = re.search(r"^([ \t]*)<BeeHaveWeather>.*?</BeeHaveWeather>[ \t]*\r?\n", text, flags=re.M | re.S)
    if anchor is None:
        anchor = re.search(r"^([ \t]*)<BeeHaveMapCenterPointY>.*?</BeeHaveMapCenterPointY>[ \t]*\r?\n", text, flags=re.M | re.S)
    if anchor is None:
        raise ValueError(f"{path}: no BeeHaveWeather/BeeHaveWeatherFile/BeeHaveMapCenterPointY element to anchor on")
    indent = anchor.group(1)
    newline = "\r\n" if "\r\n" in text else "\n"
    block = ""
    for key in missing:
        value = params[key]
        if key == "SunshineHours":
            # keep the template's multi-line layout, re-indented for this file
            lines = [line.strip() for line in value.strip().splitlines() if line.strip()]
            value = newline + "".join(f"{indent}  {line}{newline}" for line in lines) + indent
        block += f"{indent}<{key}>{value}</{key}>{newline}"
    text = text[: anchor.end()] + block + text[anchor.end():]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("xrun", nargs="+", help=".xrun files to update in place")
    parser.add_argument("--template", default=TEMPLATE, help="template.xrun to copy the values from")
    args = parser.parse_args()
    params = template_weather_params(args.template)
    for path in args.xrun:
        added = update_xrun(path, params)
        print(f"{path}: {'added ' + ', '.join(added) if added else 'already complete'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
