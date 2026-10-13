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

For each hive, one untreated .xrun file plus one per treatment is generated, sharing the same
RandomSeed so treatment sampling is reproducible. SimID = <hive_id>_<untreated|treated>.
Each .xrun file specifies the NumberMC outer Monte Carlo count (default 1 for backward compatibility).
Optional manifest keys "sunshine_hours" (365 values) and "season_hopomo" (X1..X5) override the
weather/season defaults taken from template.xrun.

Treatments: by default one treated variant ("treated") with the manifest's "gap" (default: "default")
and "treated_min_applications"/"treated_max_applications". A manifest may instead list several:

    "treatments": [
      {"id": "treated",      "gap": "default",                  "min_applications": 0, "max_applications": 3},
      {"id": "thiacloprid",  "gap": "thiacloprid_apple_EU_120", "min_applications": 1, "max_applications": 1}
    ]

Each yields <hive>_<id>.xrun with SimID/RunLabel "<hive>_<id>"; the untreated run uses the manifest's
"gap" (toxicity parameters are still required) with zero applications. The <GAP> element in the .xrun
file identifies the preset of a run after import. --parallel N runs N simulations at a time.
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
from update_xrun_weather import WEATHER_KEYS, scenario_sunshine_hours, template_weather_params  # noqa: E402


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUNDLED_PYTHON = os.path.join(REPO_ROOT, "model", "core", "bin", "python-3.9.7-amd64", "python.exe")
INIT_PY = os.path.join(REPO_ROOT, "model", "core", "init.py")


def weather_params(manifest: dict) -> dict:
    """SunshineHours and SeasonHoPoMoRepX1..5 for the .xrun file.

    SunshineHours defaults to the scenario's weather/sunshine_hours.txt when present,
    otherwise to template.xrun (Rothamsted 2009); the season defaults come from
    template.xrun. A manifest may override them with "sunshine_hours" (365 numbers,
    list or space-separated string) and "season_hopomo" (five numbers X1..X5).
    """
    params = template_weather_params()
    scenario_series = scenario_sunshine_hours(manifest.get("scenario", ""))
    if scenario_series:
        params["SunshineHours"] = scenario_series
    sunshine = manifest.get("sunshine_hours")
    if sunshine is not None:
        values = sunshine.split() if isinstance(sunshine, str) else [str(v) for v in sunshine]
        if len(values) != 365:
            raise ValueError(f"sunshine_hours must contain 365 values, got {len(values)}")
        params["SunshineHours"] = " ".join(values)
    season = manifest.get("season_hopomo")
    if season is not None:
        if len(season) != 5:
            raise ValueError("season_hopomo must contain five values (X1..X5)")
        for i, value in enumerate(season, start=1):
            params[f"SeasonHoPoMoRepX{i}"] = str(value)
    return {key: params[key] for key in WEATHER_KEYS}


UNTREATED = {"id": "untreated", "min_applications": 0, "max_applications": 0}


def treatments_of(manifest: dict) -> list[dict]:
    """Treated variants of a manifest (see module docstring); validated, with the gap filled in."""
    default_gap = manifest.get("gap", "default")
    treatments = manifest.get("treatments")
    if not treatments:
        treatments = [{
            "id": "treated",
            "gap": default_gap,
            "min_applications": manifest.get("treated_min_applications", 0),
            "max_applications": manifest.get("treated_max_applications", 0),
        }]
    seen = set()
    result = []
    for t in treatments:
        t = dict(t)
        t.setdefault("gap", default_gap)
        if not t.get("id") or t["id"] in seen or t["id"] == "untreated":
            raise ValueError(f"treatment ids must be unique and not 'untreated': {t.get('id')!r}")
        if int(t.get("max_applications", 0)) < 1:
            raise ValueError(f"treatment {t['id']!r} needs max_applications >= 1")
        if int(t.get("min_applications", 0)) > int(t["max_applications"]):
            raise ValueError(f"treatment {t['id']!r}: min_applications > max_applications")
        seen.add(t["id"])
        result.append(t)
    return result


def build_xrun(manifest: dict, hive: dict, treatment: dict, output_dir: str) -> str:
    """Write <hive>_<treatment id>.xrun; `treatment` is UNTREATED or an entry of treatments_of()."""
    sim_id = f"{hive['id']}_{treatment['id']}"
    min_apps = int(treatment.get("min_applications", 0))
    max_apps = int(treatment.get("max_applications", 0))
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
    fields.update(gap_params(treatment.get("gap") or manifest.get("gap", "default")))
    fields.update(weather_params(manifest))
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
    parser.add_argument("--parallel", type=int, default=1, metavar="N",
                        help="run N simulations concurrently (each needs ~2 GB for NetLogo); default 1")
    parser.add_argument("--only", metavar="SUBSTR", action="append",
                        help="only run simulations whose SimID contains SUBSTR (repeatable)")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as fh:
        manifest = json.load(fh)

    manifest_dir = os.path.dirname(os.path.abspath(args.manifest))
    output_dir = os.path.join(manifest_dir, "batch_runs")
    os.makedirs(output_dir, exist_ok=True)

    variants = [UNTREATED] + treatments_of(manifest)
    xrun_paths: list[tuple[str, str]] = []
    for hive in manifest["hives"]:
        for treatment in variants:
            path = build_xrun(manifest, hive, treatment, output_dir)
            sim_id = f"{hive['id']}_{treatment['id']}"
            if args.only and not any(s in sim_id for s in args.only):
                continue
            xrun_paths.append((sim_id, path))
            print(f"generated: {path}")

    if args.dry_run:
        return 0

    for sim_id, _ in xrun_paths:
        if os.path.isdir(os.path.join(REPO_ROOT, "run", sim_id)):
            print(f"run/{sim_id} already exists; delete it first (SimIDs must be unique)", file=sys.stderr)
            return 2

    return run_all(xrun_paths, max(1, args.parallel))


def run_all(xrun_paths: list[tuple[str, str]], parallel: int) -> int:
    """Run the simulations, `parallel` at a time; log each to batch_runs/<SimID>.log. Returns exit code."""
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def run_one(sim_id: str, xrun_path: str) -> tuple[str, int, float]:
        started = time.time()
        log_path = os.path.splitext(xrun_path)[0] + ".log"
        with open(log_path, "w", encoding="utf-8") as log:
            result = subprocess.run(
                [BUNDLED_PYTHON, "-u", INIT_PY, xrun_path],
                cwd=REPO_ROOT, stdout=log, stderr=subprocess.STDOUT, check=False,
            )
        return sim_id, result.returncode, time.time() - started

    failed = 0
    print(f"\n=== running {len(xrun_paths)} simulation(s), {parallel} at a time ===", flush=True)
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        futures = [pool.submit(run_one, sim_id, path) for sim_id, path in xrun_paths]
        for future in as_completed(futures):
            sim_id, code, seconds = future.result()
            status = "ok" if code == 0 else f"FAILED (exit {code})"
            print(f"{sim_id}: {status} after {seconds / 60:.1f} min", flush=True)
            failed += code != 0
    if failed:
        print(f"{failed} simulation(s) failed; see batch_runs/<SimID>.log", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
