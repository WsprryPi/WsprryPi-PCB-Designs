# GPIO shield rename and validation

Renamed on 2026-10-06 using KiCad 10.0.6 for checks. Repository branch: `main`; source commit: `272b191752e15e04700fcbe56eef9f40c6e13e01`.

The current schematic is wired and its PCB is placed and routed. The old README's import descriptions have been labeled historical. The rename preserves the current circuit and layout; it does not restore the earlier unwired starter.

## Checks and preservation

| Check | Before | Renamed candidate |
| --- | --- | --- |
| ERC findings | 0 | 0 |
| Physical DRC violations | 0 | 0 |
| Physical DRC unconnected items | 0 | 0 |
| Schematic parity issues | Not run in the baseline | 0 |

All 37 original tracked files other than the main README were compared byte-for-byte after the intended project/library-name substitutions. UUIDs, pin connectivity, component values, placement, tracks, vias, zones, design rules and assembly exclusions are preserved. Assets without name/path changes retain identical bytes. The main README also adds the current checkpoint and identifies obsolete import descriptions as historical.

ERC retains the existing ignored checks: `footprint_filter`, `four_way_junction`, `simulation_model_issue` and `single_global_label`. DRC has no ignored checks in the current reports. Schematic and board exports were visually inspected. No physical or RF validation was performed.

## Renamed artifacts

- Project directory: `WsprryPico Shield` → `WsprryPico GPIO Shield`.
- Project basenames: `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, and the existing ignored `.kicad_prl`.
- Local library basename: `wsprrypico-shield.kicad_sym` → `wsprrypico-gpio-shield.kicad_sym`.
- Library directories: `.pretty` and `.3dshapes` now use `wsprrypico-gpio-shield`.
- Existing backup directory basename follows the project rename; historical archive contents remain intact.

The complete directory move preserves ignored backups, generated evidence and JLCPCB state. Historical file contents are not rewritten as current evidence.

## Edited references

Updated active project and library names in the project settings, schematic, PCB, symbol/footprint tables, symbol library, local model README and the following footprint files:

- `ALPS_SKRP_4.2x3.2mm.kicad_mod`
- `LED_0603_1608Metric.kicad_mod`
- `LPF_HeaderPair_Female_2x1x04_P2.54mm_S33.02mm.kicad_mod`
- `L_Toroid_FT37-43_Vertical_P5.08mm.kicad_mod`
- `PinHeader_1x02_P2.54mm_Vertical.kicad_mod`
- `PinHeader_1x03_P2.54mm_Vertical.kicad_mod`
- `Potentiometer_Bourns_TC33X_Vertical.kicad_mod`
- `Raspberry_Pi_Pico_2W_Header.kicad_mod`
- `SMA_Adafruit_1865_EdgeMount.kicad_mod`
- `TO-92_Inline.kicad_mod`

These changes only repoint project-local paths. `${KIPRJMOD}` remains intact. Other footprints, models, generator scripts and license files moved without content changes.

Repository `README.md` and `AGENTS.md` identify the renamed GPIO project and new synth starter. Reports and previews are retained under this project's ignored `generated/rename-validation/` directory.
