# WsprryPi PCB Designs

KiCad schematics, PCB layouts, and custom footprints for Wsprry Pi.

**Unless a specific board revision has documented validation, treat these designs
as untested and not ready for production.** Included PDFs are reference exports;
the KiCad source files are authoritative.

## Projects

| Project | Purpose | Reference schematic |
| --- | --- | --- |
| [Synth Universal](Wsprry-Pi-Synth-Univ/README.md) | Si5351-synthesized transmission board | [PDF](Wsprry-Pi-Synth-Univ/Wsprry-Pi-Synth-Univ.pdf) |
| [GPIO Universal](Wsprry-Pi-GPIO-Univ/README.md) | Traditional GPIO transmission board | [PDF](Wsprry-Pi-GPIO-Univ/Wsprry-Pi-GPIO-Univ.pdf) |
| [LPF](Wsprry-Pi-LPF/README.md) | Low-pass filter board | [PDF](Wsprry-Pi-LPF/Wsprry-Pi-LPF.pdf) |
| [Pico 2W Shield Template](Pico%202W%20Shield%20Template/README.md) | Reusable Pico 2 W shield outline, header interface, and antenna notch | KiCad 10 starter project |

## Standalone library assets

[Pico 2 W library assets](pico-2w-libs/README.md) contains standalone symbols, footprints, and a STEP model. Read its compatibility and provenance limitations before use; the shield projects use their own local libraries.

## Opening a project

Clone [WsprryPi/WsprryPi-PCB-Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs)
and open the desired project's `.kicad_pro` file in KiCad. The checked-in
Synth, GPIO, and LPF schematics and boards identify KiCad 9.0 as their generator.
The Pico 2W Shield Template was prepared with KiCad 10.0.1. Record the KiCad
version used for any edits, and review format upgrades before committing them.

Each project keeps its own local libraries and library tables. Paths use
`${KIPRJMOD}`, which refers to that project's directory. Preserve this structure
when copying a project. No shared library outside the repository is required by
the project library tables.

### Known missing assets

The custom footprint libraries are included, but these symbol-library paths are
currently referenced by the project tables and absent from the repository:

| Project | Missing path relative to the project |
| --- | --- |
| Synth Universal | `libraries/symbols/Wsprry-Pi.kicad_sym` |
| GPIO Universal | `libraries/symbols/Wsprry-Pi.kicad_sym` |
| LPF | `libraries/symbols/New_Library.kicad_sym` |
| LPF | `libraries/symbols/Wsprry-Pi-LPF.kicad_sym` |

The existing schematics contain embedded symbol definitions, but the absent
libraries still need to be restored or their references deliberately resolved
for library editing and updates. Changing `.gitignore` does not recover them.

Some custom footprints also reference absent STEP models in each project's
`EASYEDA_MODELS` directory: the large through-hole capacitor, and, in the Synth
and GPIO projects, the pushbutton and through-hole SMA connector. These affect
3D visualization. Standard model references use `${KICAD9_3DMODEL_DIR}` and rely
on the installed KiCad model libraries.

## What belongs in Git

Track schematics, boards, project settings, custom rules, symbol and footprint
libraries, library tables, reusable 3D models, and intentional documentation or
design calculations. The LPF workbook and reference PDFs belong in the repository.
Retain legacy cache or rescue libraries when a design depends on them.

KiCad local preferences, locks, caches, automatic backup folders, and `.history`
are ignored. Put regenerable fabrication and analysis output in a project's
`production/`, `fabrication/`, or `generated/` directory. These directories are
ignored; reviewed evidence and documentation should live outside them. Attach
release manufacturing packages to the corresponding GitHub release, identifying
the source commit, board revision, KiCad version, and validation status.

File extensions such as `.kicad_sym`, `.step`, `.csv`, `.xml`, `.pdf`, and `.zip`
are deliberately not ignored globally. See [`.gitignore`](.gitignore) and
[KiCad's file documentation](https://docs.kicad.org/9.0/en/kicad/kicad.html#_kicad_files_and_folders)
for the distinction between design assets and local state.

## Contributions and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for change and validation guidance. Report
problems through [GitHub Issues](https://github.com/WsprryPi/WsprryPi-PCB-Designs/issues).
Agent guidance starts in [AGENTS.md](AGENTS.md); [CLAUDE.md](CLAUDE.md) points to
the same instructions.

The repository includes the [MIT license](LICENSE.md). Preserve any third-party
copyright and license notices when adding or modifying library assets.
