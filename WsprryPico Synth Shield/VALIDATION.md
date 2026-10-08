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

## JP41 solder-pad drawing, 2026-10-07

Replaced the PowerSelector rectangle with a three-pad solder-jumper graphic in the local library and schematic cache. USB/pin 40 is shown normally closed to the center pad through the marked cuttable link; VSYS/pin 39 is shown open. The assigned local footprint already contains the exposed 0.35 mm wide, 0.50 mm long copper neck between pads 1–2 and the alternate open 2–3 solder gap, so no footprint geometry change was necessary.

The working schematic already contained user edits at the start of this change. A saved pre-edit snapshot and exact replacement audit confirm that only the PowerSelector graphic and pin-name display changed; all existing wiring, pin definitions, component instances and UUIDs are preserved. The PCB, footprints, project settings and unrelated files remain byte-for-byte unchanged.

KiCad **10.0.6** checks:

- ERC before and after: **167 errors / 16 warnings**, exit 5; finding lists are identical. These comprise 136 unconnected pins, 16 undriven power inputs, 15 undriven signal inputs, 15 isolated pin labels and one dangling no-connect flag. They remain unresolved; no rules or exclusions were changed.
- Physical PCB DRC: **0 violations / 0 unconnected items**. Schematic parity: **73 findings**, combined exit 5, reflecting the current unsynchronized schematic and interface-only PCB.
- Native SVG export succeeded; the rendered JP41 detail was visually inspected for its default bridge, alternate gap, labels and clearance.
- Local Markdown links, whitespace, source ignore/attribute behavior and file-preservation checks pass. Reports, original snapshots and the visual preview are in ignored `generated/jp41-solder-selector/`.

KiCad's existing Fontconfig cache warning remains in the logs. These checks verify the drawing change and saved-source state, not current capacity, fabrication readiness or RF performance. PCB synchronization and circuit completion remain pending.

## Standard JP41 symbol replacement, 2026-10-07

Superseding the custom drawing above, JP41 now uses **wsprrypico-synth-shield:SolderJumper_3_Bridged12**, imported from KiCad 10.0.6's installed `Jumper.kicad_sym`. The stock graphical units and all pin definitions match exactly. The local copy assigns the existing cuttable footprint/filter and excludes position output; its KiCad license attribution is recorded in [SYMBOL-SOURCES.md](SYMBOL-SOURCES.md). The obsolete PowerSelector symbol was removed from the library and schematic cache. JP41 retains its instance/pin UUIDs, location, assigned footprint and assembly exclusions. Its pins were unconnected before replacement, so the shorter standard pin geometry requires no wire changes. All other component instances and existing wires/labels are preserved.

KiCad **10.0.6** ERC remains **167 errors / 16 warnings**, exit 5, with the same finding categories and counts before and after replacement. Physical DRC reports **0 violations / 0 unconnected items**; parity remains **50 missing footprints and 23 net conflicts**, combined exit 5. These unsynchronized-design findings remain unresolved. The native SVG export and rendered JP41 detail were visually inspected. The PCB, footprint geometry and rules are unchanged; no exclusions were added. The existing Fontconfig warning remains in the logs.

Stock-symbol comparison, instance/wiring preservation, local documentation links, whitespace and source ignore/attribute checks pass. Reports, the pre-edit snapshot and preview are in ignored `generated/jp41-standard-jumper/`. Changes are uncommitted; circuit completion, PCB synchronization and physical qualification remain pending.

## Footprint audit and control GPIO decisions, 2026-10-07

All **51 physical schematic instances** have project-local footprint assignments resolving to **19 distinct footprint files**, all present in `wsprrypico-synth-shield.pretty`. The footprint table retains `${KIPRJMOD}`. J11/J12 intentionally have no separate footprint and are off-board purchasing descriptions; U11 supplies the combined socket pad rows. This verifies footprint availability, not PCB population, 3D-model completeness or physical qualification.

The user approved **GP6 / physical 9 AMP_EN**, **GP14 / physical 19 BUTTON_N**, and **GP15 / physical 20 LED_DRIVE**. The local U11 symbol pin mapping and exclusive role allocation were checked. Current decision documents now mark these pins approved; historical checkpoints above retain their original approval status. Button action and LED behavior remain open.

Only decision/provenance documentation changed in this step. Before/after hashes preserve every KiCad design asset and all unrelated tracked files, including the user's existing schematic and project-setting edits. Local Markdown links/anchors, whitespace and ignore/attribute checks pass. ERC/DRC were not rerun for this documentation-only decision update; earlier results remain historical saved-source checkpoints. The read-only footprint audit is retained in ignored `generated/control-pin-decisions/`.


## 2026-10-07 QLG3 socket and 70-series net labels

Replaced J71's selected JST PH footprint with a project-local **1x5 female 2.54 mm socket on the shield top**, accepting **QLG3 male pins fitted on the underside**. Pins are 1 PICO_3V3, 2 backup supply tied to PICO_3V3, 3 GPS_PPS_RAW, 4 GPS_TX, 5 GND. Added TP71, a local 2 mm copper pad for GPS_RX command hand wiring. Socket/pad are excluded from assembly BOM and positions; the generic socket STEP model is copied locally. Exact mating parts/heights, QLG3 mounting geometry, connector orientation relative to the board edge and SMA clearances are not physically qualified.

Labeled every 70-series pin; intentionally unused U71 fCKO/DFLAG and U72 NC receive no-connect markers. GPS_PPS_RAW passes through R75 to GPS_PPS (Pico GP16 and inverter input); COUNTER_INDEX_N reaches U71 INDEX. SYNTH_CLK2 passes through R74 to COUNTER_CLK. Original symbol/pin UUIDs and all original symbol positions are preserved. Existing user wiring is preserved. PCB/project files are byte-for-byte unchanged. The user explicitly retained the 70-series block below the A3 printable area. Visual inspection used a temporary taller-page copy; the saved project's paper size/placement are unchanged. Ordinary A3 exports omit the block.

Checks with **KiCad 10.0.6**:

| Check | Result |
| --- | --- |
| ERC before | 57 errors / 9 warnings |
| ERC after | **3 errors / 0 warnings**: undriven power declarations for VSYS, GND and AMP_5V_IN; no exclusions or severities changed |
| Actual exported netlist | Every 70-series pin checked against the specified pin/net map; Pico UART/PPS associations and socket order agree |
| Physical DRC, unchanged board | **0 violations / 0 unconnected items**; does not validate the pending circuitry |
| Schematic/PCB parity | **Blocked: kicad-cli aborts with exit 134 on two attempts**, without a completed report; not a pass. PCB still contains only the Pico interface |
| Library and assembly metadata | J71/TP71 local assets resolve; both exclude BOM/positions. 53 unique inventory entries; 44 SMT entries unchanged |
| Visual review | Labeled 70-series reviewed using a temporary taller sheet; original block location retained |

Reports and review image are in ignored `generated/qlg3-interface/`. Counter INDEX pulse/capture behavior, receiver power sequencing, socket mating and RF coupling remain hardware/firmware acceptance work. A clear physical DRC on the unsynchronized board is not fabrication or RF qualification.

## QLG3 reusable part — 2026-10-07

KiCad **10.0.6** exported the new module symbol and host footprint to SVG; both were visually inspected, along with a native colored 3D render. The isolated mechanical fixture passed DRC: **0 violations, 0 unconnected pads, 0 footprint errors**, no ignored checks, with unchanged project rules. The sandboxed DRC process initially aborted in macOS application registration; the approved native run succeeded. The first completed run found reference text on the temporary fixture edge; enlarging that temporary board resolved it. No design rules were relaxed.

The active schematic ERC remains **3 errors / 0 warnings**, all existing undriven power inputs: U11 pin 39, #PWR01 pin 1, U41 pin 1. This library-only addition preserves the active schematic and PCB byte-for-byte. It does not resolve earlier whole-design parity limitations or qualify assembly fit. Hans's XY, five-pin mapping and standard connector geometry are distinguished from photo-based mechanical estimates in [the module documentation](qlg3-model/README.md). Preview and native reports are in ignored `generated/qlg3-part/`.

### Corrected assembly orientation

The QLG3 part now places E108 and SMA above the daughterboard, with the male mating header underneath on the opposite face. The host footprint is reflected consistently from Hans's source view: X′=X, Y′=18.0975−Y. Pads 1–5 retain their signals and X positions, with KiCad Y=−2.69875 mm. Regenerated STEP/VRML solids and inspected the corrected native 3D render. KiCad 10.0.6 isolated fixture DRC again reports **0 violations / 0 unconnected items**. Active schematic and PCB hashes remain unchanged; electrical symbol pin mapping is unchanged, so no new ERC run was required for this mechanical correction.

### QLG3 hardware-only keepouts

KiCad 10.0.6: corrected footprint fixture **0 DRC violations**; an 0603 component at module X=12, Y=9 mm under the open area also **0 violations**. Three deliberately misplaced components at the socket and both mounting centers each trigger the matching named `items_not_allowed` rule. That negative fixture reports **27 expected collision findings total**, including the three keepout errors, copper/hole clearances and courtyard/silkscreen collisions. No checks were ignored and no rules were weakened. Updated native footprint SVG inspected. The footprint uses three F.Cu component-only keepouts and two valid, closed hardware courtyard contours; all five pad numbers/positions and the two hole centers are unchanged. The active schematic and PCB remain unchanged. This verifies placement restrictions, not component height or final post/socket fit.

## J71 plain header and complete QLG3 model assignment

J71 now displays `QLG3 GPS Receiver` and selects `wsprrypico-synth-shield:QLG3_GPS_UndersideHeader`. Removed stale keyed/JST/2.0 mm and C157993 supplier fields; specified plain unkeyed 1×5 0.1-inch (2.54 mm) socket/header hardware. Updated the local and cached connector footprint filters together. All instance/pin UUIDs, positions, BOM/position exclusions and electrical connectivity are preserved. Before/after exported netlists have identical net-to-pin membership throughout the schematic.

KiCad **10.0.6** ERC remains **3 errors, 0 warnings** (U11 VSYS, GND power input, U41 IN undriven). Native schematic detail and 3D render inspected. An isolated preview loads its footprint from J71's actual exported assignment and displays the complete receiver/SMA/header/post assembly; its DRC reports **0 violations / 0 unconnected items**. The active PCB remains byte-for-byte unchanged; J71 receives this assembly when transferred/placed from the schematic. Reports and previews are under ignored `generated/j71-qlg3/`. Existing physical-fit limitations remain.

Native export exclusion check: KiCad 10.0.6 BOM export from the active schematic and CSV position export from the isolated J71 preview both omit **J71**. The check used its explicit BOM/position exclusion flags, without a blanket through-hole filter. J71 remains on-board, with its complete QLG3 model. Both native exports ran outside the sandbox at the user's request.

## QLG3/J71 focused part commit — 2026-10-07

This commit includes the QLG3 symbol/footprint, local STEP/VRML models, standard connector model inputs, generator, Hans's dimension drawing, J71 properties and related part documentation. It deliberately preserves the previously committed unwired schematic baseline; separate in-progress wiring, control changes, TP71 placement, capacitor renumbering and PCB/project edits remain outside the commit.

**KiCad 10.0.6, exact staged snapshot:** ERC reports **217 errors / 0 warnings**, exactly matching every finding in the pre-commit HEAD baseline. These are retained baseline findings, not a passing ERC result. The separately wired working checkout's 3-error result does not apply to this snapshot. The staged native BOM omits J71. The J71 assembly preview passed DRC with **0 violations / 0 unconnected items**, and native placement export omitted J71 without filtering all through-hole parts. Named keepout probes reject all three hardware areas while an 0603 probe beneath the free module area passes. Native symbol, footprint, schematic detail and 3D visuals were inspected; the staged schematic was also exported successfully.

J71's five pins, exclusions and baseline placement are preserved; only part properties, footprint filters and the corrected header pin-order annotation change in the staged schematic. The active PCB is untouched. Generic post/socket fit, underside component height, approximate body geometry and RF qualification remain open. Documentation links and staged whitespace checks pass. Native tools run outside the sandbox as requested.


## Synth shield primary-side flip — 2026-10-07

At the user's request, flipped the complete starter board about its horizontal centerline (Y = 89.775 mm). U11's Pico sockets and associated silkscreen/courtyard/models are now on **B.Cu**, leaving **F.Cu** as the primary synth-component side. Flipped the nine board-level outline items together with U11's embedded antenna-notch edges and both-layer antenna keepout. Board dimensions, pad numbers, net associations, UUIDs, locks, assembly exclusions and project-relative model references are preserved. The library footprint is unchanged; back-side orientation belongs to the placed U11 instance.

**KiCad 10.0.6:** native physical DRC **0 violations / 0 unconnected items**. Schematic parity completes with **75 existing starter-board differences** (51 missing footprints and 24 net conflicts), matching the pre-flip audit. The latest user-saved schematic now reports **0 ERC errors / 0 warnings**; this operation did not edit the schematic. The former three undriven-power errors are absent from that saved source. No rule severities or exclusions were changed by this operation. The existing native Fontconfig cache warning did not prevent completion.

Inspected native front and back 3D renders: both socket bodies are beneath the primary face, and the open antenna notch remains aligned. Verified all 40 pad identities/net assignments, outline UUIDs, and the locked U11 instance after saving/reloading. Source format version remains 20260206 / generator 10.0. Only the active synth PCB, README and this validation note were edited for this change; independent pre-existing user changes remain intact. A before-copy, transform checks, native reports and renders are in ignored `generated/primary-side-flip/`. No commit or push was requested.

## QLG3 single-post variant — 2026-10-07

Saved the user's current placement before replacing only J71's mounting variant. All non-J71 board objects remain byte-for-byte identical to that saved baseline. Its five numbered pads, net assignments, pad UUIDs, position/orientation and assembly exclusions are unchanged. The schematic change is limited to J71's footprint assignment and the matching connector footprint filter; the independent module symbol is added to the local library. Original two-post assets remain available.

KiCad 10.0.6: ERC 0 findings before/after; schematic parity 0 before/after. DRC physical findings 17 → 1; unconnected items 124 → 124. The remaining finding is the existing J71 F.SilkS rectangle/Edge.Cuts clearance warning. The independent single-post footprint fixture has 0 DRC findings and 0 unconnected items. The removed mounting hole was overlapping Pico pads 1/2; its associated collision findings are eliminated without moving the module or changing rules. Native footprint and 3D previews were inspected. Reports are in ignored `generated/qlg3-single-post/` at the repository root. Physical single-post support remains unqualified.

## J61 board-edge SMA restoration — 2026-10-07

Replaced the BAT Wireless through-hole J61 with the existing `SMA_Adafruit_1865_EdgeMount` and its local illustrative VRML model, copied from the GPIO shield. Updated only J61's schematic/PCB assignment and supplier fields, plus purchasing/provenance documentation. The existing QLG3 single-post work and every non-J61 schematic/PCB object are preserved. J61's footprint UUID, origin, electrical pad UUIDs and net assignments are retained: pad 1 TX_OUT, four pad-2 lands GND. All five pads are now surface lands, with no drilled holes or paste; BOM/position exclusions remain set.

KiCad 10.0.6: schematic ERC 0 findings; PCB/schematic parity 0 findings; 124 unrouted connections unchanged. Current board DRC has 2 findings: the existing J71 silkscreen/edge clearance warning and a J61/U31 courtyard overlap in the off-board staging area caused by the larger edge-launch outline. The footprint origin remains at (172.255, 140.775) mm, pending placement at the actual board edge. No routing, other component placement or rules were changed to conceal this finding. The isolated 1.6 mm board-edge fixture passes DRC with 0 findings / 0 unconnected items, and its native 3D render was inspected. Documentation links and whitespace checks pass. Physical connector fit and RF performance remain unqualified. Evidence: repository-root ignored `generated/j61-edge-sma/`.
