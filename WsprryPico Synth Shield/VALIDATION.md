# Synth shield creation and validation

Checked on 2026-10-06 with KiCad 10.0.6. Source repository: `WsprryPi-PCB-Designs`, branch `main`, baseline commit `272b191752e15e04700fcbe56eef9f40c6e13e01`.

## Creation checks (historical)

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

Creation reports and previews are retained in this project's ignored `generated/creation-validation/` directory. Re-run ERC/DRC after adding the synthesizer or wiring the Pico.

## Approved design-record checkpoint, 2026-10-06

The external GPS interface, keyed five-position connection, Pico 3.3 V supply and UART/SPI/PPS GPIO plan are locked in [the circuit notes](TCXO-SI5351A-DESIGN.md#gps-configuration-locked). Shared pin 39/40 power selection, always-on clock power, the DC-blocked SMA output with an external LPF, a shield button and LED, and 2200 m through 2 m with 2 m WSPR are recorded there as selected requirements. The separate amplifier/button/LED control plan still awaits user approval; component specifications, circuit implementation and measurement remain open.

Fresh saved-source checks used **KiCad 10.0.6** before publication: synth ERC retains **52 expected errors / 0 warnings**; synth physical DRC and schematic parity report **0 findings**. The renamed GPIO shield reports **0 ERC/DRC/parity findings**. The separate QRP model retains **0 ERC errors / 12 footprint warnings**. Nonzero ERC exit codes for the synth starter and QRP model are retained, not converted into passes. No severity or exclusion was changed. KiCad also emitted its existing Fontconfig cache-version warning; reports completed.

Documentation checks cover local links/anchors, whitespace, ignore/attribute behavior and exclusive GPS/counter pin ownership. Before/after hashes preserve all 59 saved design assets across the synth, GPIO and QRP projects. The starter schematic and PCB remain unwired; locking these requirements does not add GPS or synthesizer components to them. Existing visual inspections apply to the unchanged source assets.

## Prototype parts and footprint checkpoint, 2026-10-06

Work starts from `main` at `e73a0492b9daf962ce656422591bd520e0be96ef`. [PARTS.md](PARTS.md) and [PARTS.csv](PARTS.csv) record 52 reserved positions, with 51 prototype selections and one unresolved FT37-43 sourcing conflict. [ASSEMBLY-BOM-PREVIEW.csv](ASSEMBLY-BOM-PREVIEW.csv) contains 44 SMT positions. All headers, the SMA and hand-wound inductors are excluded from both assembly BOM and position output. BS170 remains a manual fitting; selector/jumper copper features have no assembly purchasing rows. No production position file has been generated.

Added 18 project-local footprints and the copied illustrative choke model. [LIBRARY-SOURCES.md](LIBRARY-SOURCES.md) records their provenance, dimensions, adaptations, license terms and model gaps. The active schematic, PCB, project settings, symbol library, existing header footprint and socket STEP are byte-for-byte unchanged; three unrelated pre-existing dirty files are also preserved, verified by nine before/after SHA-256 hashes.

Fresh checks use **KiCad 10.0.6**:

| Check | Result / scope |
| --- | --- |
| Starter ERC | **52 errors / 0 warnings**, exit 5; expected open-interface findings remain visible |
| Starter physical DRC and schematic parity | **0 violations / 0 unconnected items / 0 parity findings**, exit 0 |
| Isolated fixture containing all 18 new footprints | **0 violations / 0 unconnected items**, exit 0; geometry only, no functional circuit or routing |
| Inventory and assembly filter | 52 unique references; 44 SMT rows match the preview exactly; headers/SMA have both exclusions; all listed footprints exist |
| Referenced 3D models | 14 references resolve; Bourns TC33X and BAT WIRELESS SMA stock STEP files are missing and documented; custom TCXO/button/selector solids remain unassigned |
| Visual inspection | Manufacturer drawings for KDS, Bourns, XUNPU, JST, Pico sockets, LS7366R package and SMA inspected; final exported footprint gallery inspected, including selector labels/cut point |

The first completed fixture DRC reported **15 findings**: eight generic MSOP pad-clearance errors and seven silkscreen/text warnings. The Si5351 footprint was adapted to Skyworks' recommended 0.30 mm pad width, 1.40 mm length and 4.40 mm row centers, and the affected reference/selector text was corrected. The final pass retains the project's existing rules, severities and exclusions; no threshold was relaxed. The manufacturer's approximately 0.08 mm mask web still requires fabrication-process confirmation.

An earlier sandboxed fixture DRC aborted while initializing native macOS application services. Re-running with approved native access completed; its reports supersede that tool abort. An attempted Python/wx fixture workflow also failed to initialize native screen access, so fixture construction used the saved native text format instead. KiCad's existing Fontconfig warning and a transient CLI lock-removal warning did not prevent completed reports. These failures are not counted as passes.

Reports, the isolated fixture and visual preview remain in ignored `generated/parts-validation/`. Local documentation links/anchors, whitespace, source ignore/attribute behavior and preservation checks are included in this checkpoint. Supplier counts are dated page snapshots, sometimes cached, rather than reserved inventory or assembler-availability guarantees.

The circuit is still unimplemented in the active KiCad schematic and PCB. Choke sourcing and the proposed GP6/GP14/GP15 control plan await the user's choices. External receiver compatibility, placement/fit, capacitor bias behavior, power sequencing, PPS capture, synthesis and full-band RF acceptance remain open. A clean footprint fixture and starter DRC do not establish a fabrication-ready or RF-qualified shield.

## Hand-wound inductor assembly exclusion, 2026-10-06

The user extended the no-BOM/no-position rule to every hand-wound inductor. L61 is marked manual in the engineering inventory; its existing `no`/`no` export fields and local footprint's `exclude_from_bom` / `exclude_from_pos_files` attributes are retained. The 44-row SMT preview is unchanged. Future schematic instances must also use `in_bom no`. Only documentation and the inventory assembly/notes fields changed; all KiCad source assets and models are byte-for-byte unchanged. Local links, CSV exclusions, ignore/attribute behavior and whitespace checks pass. Existing KiCad 10.0.6 results above remain applicable; ERC/DRC were not rerun for this documentation/inventory update. L61 sourcing remains separate and unresolved.

## Decade-series symbol placement, 2026-10-06

Placed **53 component symbols** in eight titled 10–80-series boxes using the GPIO Pico schematic's style. This comprises the existing U11/J11/J12 interface and all 50 additional component references from the engineering inventory. The sheet is intentionally A3 to leave room for wiring. [SYMBOL-SOURCES.md](SYMBOL-SOURCES.md) records the placement groups and 17 added standalone local definitions; the two existing library definitions and their schematic cache entries are preserved.

All placed inventory symbols carry their selected value, technology/dielectric, rating, tolerance, manufacturer, MPN, supplier code/link, assembly method and selection status. The 51 physical symbol pin-number sets match their selected local footprint pad-number sets, including U11's 40-pad interface. J11/J12 remain pinless, off-board purchasing descriptions with no duplicate footprints. All references are unique and belong to their numbered boxes; electrical pins are on the 1.27 mm connection grid. Supplier metadata was consolidated so each instance property appears once.

No wires, labels, junctions or no-connect flags were added. The existing symbol/pin UUIDs, project settings, library tables, PCB, footprints and model files are preserved. The 44 SMT BOM/position inclusions match the inventory. Headers, SMA, hand-wound choke, manual BS170 and copper features retain their assembly exclusions. L61 sourcing and control GPIO/behavior choices remain open.

Fresh saved-source checks use **KiCad 10.0.6**:

| Check | Result |
| --- | --- |
| ERC | **217 errors / 0 warnings**, exit 5: 176 unconnected-pin, 24 undriven-power-input and 17 undriven-signal-input findings |
| Physical PCB DRC | **0 violations / 0 unconnected items**; unchanged interface-only PCB |
| Schematic/PCB parity | **50 missing-footprint findings**, combined DRC/parity exit 5; PCB synchronization intentionally pending |
| Pin/pad and metadata audit | 53 symbols; 19 local definitions; 51 physical pin/pad sets match; 44 SMT assembly inclusions; existing interface UUIDs/definitions preserved |
| Native exports | SVG, one-page PDF and XML netlist complete; netlist has all 53 references and no nets joining distinct component references |
| Visual review | Full schematic preview inspected for box membership, reference/value readability, selector labeling, pin display and drawing-sheet clearance |

The initial candidate export failed to load; cached symbol identifiers and text-justification syntax were corrected before the successful native checks. The first completed ERC also reported seven off-grid warnings; those instances were snapped to the existing grid, leaving the 217 unwired-circuit errors visible. Copied passive/connector footprint filters were corrected to match the selected local assets. No project severities, ignored checks or exclusion thresholds were changed. The original four template ERC ignored checks remain unchanged.

The sandboxed parity DRC aborted with exit 134. Its rerun with approved native macOS access completed and produced the results above. KiCad's existing Fontconfig warning remains in the command logs. Reports, the before-checkpoint snapshot, audit, SVG/PDF and preview are retained in ignored `generated/symbol-placement/`. Local links/anchors, source ignore/attribute behavior, whitespace and preservation checks pass.

This completes symbol placement and annotation. Circuit wiring, PCB synchronization, component placement/routing and electrical/physical/RF acceptance remain pending. The earlier 52-error ERC and clear parity describe the historical three-symbol starter, not this placed-symbol checkpoint.
