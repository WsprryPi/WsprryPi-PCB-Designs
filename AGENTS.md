# Repository guidance

## Scope and discovery

This is `WsprryPi/WsprryPi-PCB-Designs`, a KiCad hardware-design repository. Read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before changes, then the affected project's README. There is no application build system.

- `Wsprry-Pi-Synth-Univ`: Si5351 transmission board.
- `WsprryPi-GPIO-Univ`: GPIO transmission board.
- `Wsprry-Pi-LPF`: low-pass filter board and supporting workbook.
- `Pico 2W Wattmeter Shield`: ADL5904 RF wattmeter shield.
- `Pico 2W Shield Template`: reusable unwired Pico shield template.
- `pico-2w-libs`: standalone Pico library assets with documented compatibility limits.
- `design`: proposed circuits and engineering requirements.

## Working rules

- Confirm the repository root, branch, and working-tree state. Preserve existing user changes and keep work within the requested project and task.
- Keep each project's library folder and `${KIPRJMOD}` paths intact. Do not consolidate libraries or introduce machine-specific paths without a request.
- Treat `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `.kicad_sym`, `.kicad_mod`, custom rules, library tables, and reusable models as source assets. Respect `.gitignore`; do not blanket-ignore source libraries or 3D models.
- Missing symbol libraries and local STEP models are documented in README.md. Do not silently replace missing definitions. Update the documentation when their status changes.
- Preserve KiCad formatting, UUIDs, connectivity, layout, and design settings unless the task calls for changing them. Avoid incidental version migrations.
- Keep documentation and repository-metadata tasks free of design-file changes. Preserve third-party attribution and the existing license.

## Validation and reporting

For repository metadata or documentation, validate local Markdown links, `git diff --check`, and relevant `git check-ignore` / `git check-attr` behavior. For design changes, run applicable ERC/DRC checks and visually inspect the affected schematic or board. Report the exact KiCad version, checks, results, and blockers. Do not substitute a successful parse or export for ERC/DRC or physical validation.

Keep failed checks and unresolved exclusions visible. Do not relax thresholds to manufacture a pass. Hardware or RF claims require evidence tied to the exact board revision, assembly, configuration, and measurement setup.

Before committing, inspect the diff and stage only the intended changes. Report the files changed, validation performed, commit if created, and remaining work. Push only when requested. Keep local agent state in ignored tool directories; maintain shared repository instructions here instead of duplicating them.
