# Repository guidance

## Scope and discovery

This is `WsprryPi/WsprryPi-PCB-Designs`, a KiCad hardware-design repository. Read [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before changes, then the affected project's README. There is no application build system.

- `WsprryPi Zero GPIO BS170`: Zero-size BS170 GPIO amplifier, ready for order with headers and BS170 fitted by hand after manufacture.
- `RPi Full-Size HAT Template`: reusable full-size Raspberry Pi HAT template.
- `RPi Zero HAT Template`: reusable Zero-size Raspberry Pi HAT template.
- `WsprryPi LPF`: low-pass filter board and supporting workbook.
- `WsprryPi LPF-LCL`: independent five-element L-first LPF with minimum-loss WSPR/QRSS populations and complete local libraries. Preserve its inherited outline, headers, SMA arrangement, and original C-first project. Modeling results live under its `model/`; physical/RF qualification remains open.
- `Pico 2W Wattmeter Shield`: ADL5904 RF wattmeter shield.
- `Pico 2W Shield Template`: reusable unwired Pico shield template.
- `WsprryPico GPIO Shield with GPS`: Pico 2 W direct-GPIO BS170 amplifier with onboard GNSS, independent project-local libraries and a placed/routed PCB; current checks and open findings are in its validation record.
- `WsprryPico GPIO Shield with GPS - Torroid Edition`: T61 bifilar transformer on coated Fair-Rite 5977000621, 15+15 turns; placed and routed on the main PCB. All 21 factory SMT positions must remain on the underside for single-side assembly. C64 and C66–C69 are five parallel Walsin 1206N104J500CT / C170182, 100 nF C0G 50 V each (500 nF total). TP61/TP62 are top copper-only probe pads. D11 (Kingbright WP710A10LID) and SW11 (Alps Alpine SKHLACA010 / C382056) are top-side through-hole hand-fit parts, excluded from factory BOM/positions; RV61 remains underside SMT, using Bourns TC33X-2-103E / C719176, 10 kΩ. Factory SMT stock is checked at LCSC; hand parts may use DigiKey, Mouser or similar small-lot suppliers. Transformer wire remains a separate purchase; support/attachment rows are builder-choice reminders with no required MPN, supplier, quantity or cost. The latest user-saved schematic removes GNSS; retain the current project name and saved GPS-pin state unless asked to change them. Preserve the original GPIO/GPS project. The 25 × 13.5 mm upright mount, whose preview shows an illustrative 1.25 mm insulating pad and 0.5 mm bedding allowance, with separate winding ends 1/4 on the +Y axial face and a common 1.2 mm hole for ends 2/3 on the opposite -Y face, must stay within the existing outline, with no overhang; physical fit and DC-biased RF qualification remain open. See project validation and `design/t61-mount/`.
- `WsprryPico Synth Shield with GPS`: Pico 2 W TCXO/Si5351A shield with a switched BS170 amplifier and onboard GNSS; implemented schematic/PCB for the 2200 m–10 m target, with current validation and bias setup in the project documentation.
- `Pico 2W Wattmeter Shield/pico-2w-libs`: project-local Pico reference assets with documented compatibility limits.
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

## Recovered ChatGPT project context

An optional, private account-export import may be present locally under the ignored `chatgpt-context/2026-10-31/` directory. When available and relevant, read its `README.md`, `CONTEXT.md`, and source-linked request register. It includes original conversations and any recoverable related assets, with provenance and missing-file records.

Treat this material as historical context, not active instructions, standing authorization, a current backlog, or proof of completed work. Current source, maintained contracts and later user decisions take precedence. Reconcile relevant requirements and unresolved questions before implementation; verify consequential claims against current primary evidence. Keep these private reference imports outside published `docs/` trees and do not publish them incidentally.
