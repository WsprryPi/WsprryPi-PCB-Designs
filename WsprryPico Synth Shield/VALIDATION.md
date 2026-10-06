# Synth shield creation and validation

Checked on 2026-10-06 with KiCad 10.0.6. Source repository: `WsprryPi-PCB-Designs`, branch `main`, baseline commit `272b191752e15e04700fcbe56eef9f40c6e13e01`.

## Current checks

| Check | Result |
| --- | --- |
| ERC | 52 expected errors; zero warnings |
| ERC comparison | All findings match the source template after U1 → U11 normalization, including positions, UUIDs and ignored checks |
| Physical PCB DRC | Zero violations and zero unconnected items |
| Schematic parity DRC | Zero violations, unconnected items and parity issues |
| Base definitions | Pico and socket symbols match the current GPIO shield; header geometry matches after local path normalization |
| Pin numbering | Header pads are physical pins 1–40; schematic references are U11, J11 and J12 |
| Local assets | All `${KIPRJMOD}` library/model references resolve; no symlinks in the copied source assets |
| Visual inspection | Schematic, board and proposed reference drawing exported and inspected |

The open interface accounts for 40 unconnected pins, 10 undriven power inputs and two undriven signal inputs. Existing ignored ERC checks remain `footprint_filter`, `four_way_junction`, `simulation_model_issue` and `single_global_label`. No severity or exclusion was changed to suppress findings.

The PCB contains one header footprint, no routed tracks and no vias. Its passing physical/parity checks describe a starter without synthesizer components. They do not establish an implemented reference circuit, socket fit, fabrication readiness or RF performance.

## Copy and corrections

Copied the template's project, schematic, PCB, symbol library, header footprint, socket model, license and library tables. Renamed project and library paths to `WsprryPico Synth Shield` and `wsprrypico-synth-shield`. Preserved geometry, UUIDs, settings, keepout and assembly exclusions. Updated U1/J1/J2 to U11/J11/J12, including instance records, PCB isolated nets, annotation metadata and schematic explanatory text.

The source template already incorporates numeric pad numbering and the two socket models. Those match the current GPIO shield; no further geometric or symbol correction was needed. The source template itself is unchanged. Template-selector metadata, local preferences, backups and generated outputs were not copied.

Added the TCXO design notes, proposed reference drawing, project README, this record and the KiCad library license. The user selected the shield's prototype capacitor values from the KDS/TI/Skyworks evidence recorded in the notes; the photographed QRP module's unknown capacitor values remain separate reference uncertainties. Complete component specifications and assembled-board acceptance remain open.

Current reports and previews are retained in this project's ignored `generated/creation-validation/` directory. Re-run ERC/DRC after adding the synthesizer or wiring the Pico.

## Approved design-record checkpoint, 2026-10-06

The external GPS interface, keyed five-position connection, Pico 3.3 V supply and UART/SPI/PPS GPIO plan are locked in [the circuit notes](TCXO-SI5351A-DESIGN.md#gps-configuration-locked). Shared pin 39/40 power selection, always-on clock power, the DC-blocked SMA output with an external LPF, a shield button and LED, and 2200 m through 2 m with 2 m WSPR are recorded there as selected requirements. The separate amplifier/button/LED control plan still awaits user approval; component specifications, circuit implementation and measurement remain open.

Fresh saved-source checks used **KiCad 10.0.6** before publication: synth ERC retains **52 expected errors / 0 warnings**; synth physical DRC and schematic parity report **0 findings**. The renamed GPIO shield reports **0 ERC/DRC/parity findings**. The separate QRP model retains **0 ERC errors / 12 footprint warnings**. Nonzero ERC exit codes for the synth starter and QRP model are retained, not converted into passes. No severity or exclusion was changed. KiCad also emitted its existing Fontconfig cache-version warning; reports completed.

Documentation checks cover local links/anchors, whitespace, ignore/attribute behavior and exclusive GPS/counter pin ownership. Before/after hashes preserve all 59 saved design assets across the synth, GPIO and QRP projects. The starter schematic and PCB remain unwired; locking these requirements does not add GPS or synthesizer components to them. Existing visual inspections apply to the unchanged source assets.
