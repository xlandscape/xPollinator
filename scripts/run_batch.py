"""Generate and run xPollinator .xrun files for a batch of hive locations x treatment on/off.

Usage:
    python scripts/run_batch.py <manifest.json> [--dry-run]

Manifest (JSON):
    {
      "scenario": "scenario/Tarn-et-Garonne-small",
      "simulation_start": "2021-01-01",
            "simulation_end":   "2026-12-31",
            "timesteps": 2190,
      "replicates": 10,
            "weather": "Berlin (2000-2006)",
      "number_mc_runs": 1,
      "treated_min_applications": 1,
      "treated_max_applications": 5,
      "gap": "thiacloprid_apple_EU_120",
      "hives": [
        {"id": "hive01", "x": 127406.94, "y": 5482559.85, "random_seed": 42},
        {"id": "hive02", "x": 130000.0,  "y": 5485000.0,  "random_seed": 43}
      ]
    }

For each hive, two .xrun files are generated (untreated/treated) sharing the same
RandomSeed so treatment sampling is reproducible. SimID = <hive_id>_<untreated|treated>.
Each .xrun file specifies the NumberMC outer Monte Carlo count (default 1 for backward compatibility).
The optional "gap" key selects a preset from model/variant/gaps.json (default "default"); its exposure
and toxicity parameters are written into every .xrun file, treated and untreated alike.

The generated .xrun files are written to batch_runs/ next to the manifest and executed
sequentially via the bundled Python + init.py.
"""
import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apply_gap import gap_params  # noqa: E402


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUNDLED_PYTHON = os.path.join(REPO_ROOT, "model", "core", "bin", "python-3.9.7-amd64", "python.exe")
INIT_PY = os.path.join(REPO_ROOT, "model", "core", "init.py")


def build_xrun(manifest: dict, hive: dict, treated: bool, output_dir: str) -> str:
    suffix = "treated" if treated else "untreated"
    sim_id = f"{hive['id']}_{suffix}"
    if treated:
        min_apps = manifest["treated_min_applications"]
        max_apps = manifest["treated_max_applications"]
    else:
        min_apps = 0
        max_apps = 0
    root = ET.Element("Parameters")
    project_path = manifest["scenario"]
    if not os.path.isabs(project_path):
        project_path = os.path.join(REPO_ROOT, project_path)
    fields = {
        "SimID": sim_id,
        "Project": project_path,
        "SimulationStart": manifest["simulation_start"],
        "SimulationEnd": manifest["simulation_end"],
        "NumberBeeHaveTimesteps": str(manifest["timesteps"]),
        "BeeHaveMapCenterPointX": str(hive["x"]),
        "BeeHaveMapCenterPointY": str(hive["y"]),
        "NumberBeeHaveReplicates": str(manifest["replicates"]),
        "BeeHaveRandomSeed": str(hive["random_seed"]),
        "BeeHaveWeather": manifest.get("weather", "Rothamsted (2009)"),
        "MinNumberApplications": str(min_apps),
        "MaxNumberApplications": str(max_apps),
        "NumberMC": str(manifest.get("number_mc_runs", 1)),
        "RunLabel": sim_id,
        "HiveGroupId": hive["id"],
    }
    fields.update(gap_params(manifest.get("gap", "default")))
    weather_file = manifest.get("weather_file")
    if weather_file:
        if not os.path.isabs(weather_file):
            weather_file = os.path.join(REPO_ROOT, weather_file)
        fields["BeeHaveWeatherFile"] = weather_file
    for tag, text in fields.items():
        el = ET.SubElement(root, tag)
        el.text = text
    ET.indent(root, space="  ")
    path = os.path.join(output_dir, f"{sim_id}.xrun")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifest", help="Path to JSON manifest")
    parser.add_argument("--dry-run", action="store_true", help="Generate .xrun files but do not execute")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as fh:
        manifest = json.load(fh)

    manifest_dir = os.path.dirname(os.path.abspath(args.manifest))
    output_dir = os.path.join(manifest_dir, "batch_runs")
    os.makedirs(output_dir, exist_ok=True)

    xrun_paths: list[tuple[str, str]] = []
    for hive in manifest["hives"]:
        for treated in (False, True):
            path = build_xrun(manifest, hive, treated, output_dir)
            xrun_paths.append((f"{hive['id']}_{'treated' if treated else 'untreated'}", path))
            print(f"generated: {path}")

    if args.dry_run:
        return 0

    for sim_id, xrun_path in xrun_paths:
        print(f"\n=== running {sim_id} ===")
        result = subprocess.run(
            [BUNDLED_PYTHON, "-u", INIT_PY, xrun_path],
            cwd=REPO_ROOT,
            check=False,
        )
        if result.returncode != 0:
            print(f"run {sim_id} failed (exit {result.returncode})", file=sys.stderr)
            return result.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
