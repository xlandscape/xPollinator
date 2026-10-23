"""Check .xrun files for every parameter the model configuration needs.

Usage:
    python scripts/check_xrun.py <file.xrun> [<file.xrun> ...]

Collects the $(...) macros of model/variant/mc.xml and experiment.xml plus the parameters
core requires itself (ExperimentID, LandscapeScenario since core 1.19) and reports, per file,
the ones that are missing. A missing macro is not an error at parse time: core leaves the
literal "$(Name)" in the configuration, and the run fails later. Exit code 1 if any file
is incomplete. Fix incomplete files with scripts/update_xrun_weather.py or scripts/apply_gap.py.
"""
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "model", "core"))
import base  # noqa: E402

CORE_REQUIRED = {"ExperimentID", "LandscapeScenario"}
# read only when BeeHaveWeather is "Weather File"; BeeView-server omits it otherwise
OPTIONAL = {"BeeHaveWeatherFile"}


def required_parameters() -> set:
    macros = set(CORE_REQUIRED)
    for name in ("mc.xml", "experiment.xml"):
        with open(os.path.join(REPO_ROOT, "model", "variant", name), encoding="utf-8") as fh:
            macros |= set(re.findall(r"\$\(([A-Za-z][A-Za-z0-9]*)\)", fh.read()))
    return macros - OPTIONAL


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    required = required_parameters()
    print(f"{len(required)} required parameters (mc.xml, experiment.xml, core)")
    incomplete = 0
    for path in sys.argv[1:]:
        params = base.UserParameters(path).params
        missing = sorted(k for k in required if k not in params)
        incomplete += bool(missing)
        print(f"{os.path.basename(path):40s} {'OK' if not missing else 'missing ' + ', '.join(missing)}")
    return 1 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
