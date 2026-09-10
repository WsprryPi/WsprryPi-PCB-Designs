# Contributing

Keep changes focused on the affected KiCad project and describe the resulting
electrical, mechanical, or documentation change. Include the project name, board
revision, source commit, and KiCad version when reporting a problem or proposing
a design change.

## Design files and libraries

- Open the project's `.kicad_pro` file and retain its project-relative library
  paths. Include any new custom symbols, footprints, and required model assets.
- Preserve the separate project folders. Synth and GPIO currently carry identical
  custom footprint libraries; if changing a shared footprint, explain whether
  both projects need the update.
- Preserve KiCad's native file formatting. Review application-driven format or
  settings changes separately from intentional design edits.
- Keep source assets and intentional reference PDFs or calculations in Git.
  Write disposable exports into `production/`, `fabrication/`, or `generated/`.
  Do not commit local preferences, locks, backups, or `.history`.
- Record the source and license of imported symbols, footprints, models, and
  documentation. Preserve existing third-party notices.

## Validation

For schematic or board changes, run the applicable electrical rule check (ERC)
and design rule check (DRC), inspect the affected layout, and report the KiCad
version and results. Retain unresolved violations and explain any existing
exclusions; do not silently weaken rules to obtain a passing report.

Missing libraries and model assets are listed in the [README](README.md). State
which checks are blocked by missing assets and which were actually completed.
If a reference PDF is affected, regenerate it and visually compare it with the
source before including it in the change.

Software checks do not establish assembly, pin compatibility, electrical, or RF
performance. Describe physical validation separately, tied to the exact board
revision, assembly, configuration, and measurement setup. Keep designs marked
untested until supporting evidence is recorded.

For documentation or repository configuration changes, check local links,
run `git diff --check`, and verify ignore rules with `git check-ignore` when they
change. There is no application build or automated hardware qualification suite
in this repository.

## Pull requests

Explain the problem, the resulting behavior, the files or boards affected, and
the validation performed. Include remaining limitations and useful schematic or
layout images for design changes. Distinguish proposed work from verified results.
