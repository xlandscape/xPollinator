# Changelog

This list contains all additions, changes and fixes for xPollinator.

## [Unreleased]

### Added

- GAP presets in `model/variant/gaps.json`: each preset bundles the exposure parameters of a crop use with the toxicity
  endpoints of the substance. Includes the legacy `default` parameterisation and thiacloprid on apple for EU and US
  application rates.
- `scripts/apply_gap.py` writes a preset into existing `.xrun` files; `scripts/run_batch.py` accepts a `gap` manifest
  key.
- BeeHaveEcotox inputs `ResidueUnitDose`, `PlantDT50`, `ForagerOralLD50`, `ForagerOralSlope`, `ForagerContactLD50`,
  `ForagerContactSlope`, `LarvaeOralLD50` and `LarvaeOralSlope`. They replace the values that were hard-coded in the
  BehaviorSpace template and the per-patch RUD of 21 in `Sources.txt`.

### Changed

- All pesticide exposure and toxicity inputs of the BeeHave component in `model/variant/mc.xml` are now `.xrun`
  parameters. `.xrun` files therefore need the parameter block found in `template.xrun` (or run
  `scripts/apply_gap.py <gap_id> <file.xrun>`).

### Fixed

- Unit of the BeeHaveEcotox inputs `ContactToxicityMean` and `ContactToxicityStd` corrected from µg/bee to kg/ha. The
  value is the application rate written to `ETOX_PPPContact_patch`; BEEHAVEecotox derives the contact dose per bee from
  it as rate × RUD × 0.1 g (RUD fixed at 21).

## [0.1.4] - 2026-02-12

### Added

### Changed

- Updated Landscape Model core to version 1.18.1;
- Updated BeeHaveEcotox component to new development version

## [0.1.3] - 2025-12-03

### Added

### Changed

- scenario section

### Fixed

## [0.1.2] - 2025-12-03

### Added

### Changed

- draft documentation

### Fixed

## [0.1.1] - 2025-12-03

### Added

- workflow for conversion of mkdocs-base md-files to html

### Changed

### Fixed

## [0.1] - 2025-12-03

### Added

- initial release
- CHANGELOG.md

### Changed

### Fixed
