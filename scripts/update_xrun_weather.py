"""Add the BEEHAVE weather/season parameters to existing .xrun files.

Usage:
    python scripts/update_xrun_weather.py <file.xrun> [<file.xrun> ...]

Since the SETAC 2026 changes, mc.xml requires SunshineHours and
SeasonHoPoMoRepX1..5 in every .xrun file. This script inserts the missing
elements after <BeeHaveWeather> (or <BeeHaveWeatherFile>), leaving the rest of
the file (comments, formatting) untouched.

SunshineHours comes from the scenario when it provides one: the file
<Project>/weather/sunshine_hours.txt (365 numbers, '#' comments allowed).
Otherwise, and for the season parameters, the values of template.xrun are used.
With --replace an existing <SunshineHours> is overwritten by the scenario series.
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


SCENARIO_SUNSHINE_FILE = os.path.join("weather", "sunshine_hours.txt")


def read_sunshine_file(path: str) -> list[str]:
    """Parse a sunshine-hours file: whitespace/comma separated numbers, '#' comments, optional [ ]."""
    values = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].replace("[", " ").replace("]", " ").replace(",", " ")
            values.extend(line.split())
    for value in values:
        float(value)  # raises ValueError on garbage
    if len(values) != 365:
        raise ValueError(f"{path}: expected 365 sunshine values, found {len(values)}")
    return values


def scenario_sunshine_hours(project: str, repo_root: str = REPO_ROOT) -> str | None:
    """Return the scenario's sunshine series as a space-separated string, or None if it has none."""
    if not project:
        return None
    folder = project if os.path.isabs(project) else os.path.join(repo_root, project)
    path = os.path.join(folder, SCENARIO_SUNSHINE_FILE)
    if not os.path.isfile(path):
        return None
    return " ".join(read_sunshine_file(path))


def _project_of(text: str) -> str | None:
    m = re.search(r"<Project>\s*(.*?)\s*</Project>", text, flags=re.S)
    return m.group(1) if m else None


def update_xrun(path: str, params: dict[str, str], replace: bool = False) -> list[str]:
    """Insert missing weather elements into one .xrun file; return the added/replaced tags."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    params = dict(params)
    scenario_series = scenario_sunshine_hours(_project_of(text) or "")
    if scenario_series:
        params["SunshineHours"] = scenario_series
    replaced = []
    if replace and scenario_series and re.search(r"<SunshineHours>", text):
        text = re.sub(r"<SunshineHours>.*?</SunshineHours>", "<SunshineHours>\x00</SunshineHours>", text, count=1, flags=re.S)
        replaced.append("SunshineHours")
    missing = [key for key in WEATHER_KEYS if not re.search(rf"<{key}>", text)]
    if not missing and not replaced:
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
    if replaced:
        lines = [line.strip() for line in params["SunshineHours"].split()]
        value = newline + "".join(f"{indent}  {' '.join(lines[i:i + 20])}{newline}" for i in range(0, len(lines), 20)) + indent
        text = text.replace("\x00", value, 1)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return replaced + missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("xrun", nargs="+", help=".xrun files to update in place")
    parser.add_argument("--template", default=TEMPLATE, help="template.xrun to copy the values from")
    parser.add_argument("--replace", action="store_true",
                        help="overwrite an existing <SunshineHours> with the scenario's weather/sunshine_hours.txt")
    args = parser.parse_args()
    params = template_weather_params(args.template)
    for path in args.xrun:
        added = update_xrun(path, params, replace=args.replace)
        print(f"{path}: {'updated ' + ', '.join(added) if added else 'already complete'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
