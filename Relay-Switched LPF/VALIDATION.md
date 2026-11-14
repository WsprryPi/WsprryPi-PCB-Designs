# Relay-Switched LPF validation

Recorded **2026-11-13**, repository branch `main`, using **KiCad 10.0.6** on macOS. This is an independently drawn reconstruction of the QRP Labs Rev. 5 circuit with a new layout, not a released or physically verified copy. Existing unrelated working-tree changes were preserved. The repository commit records this saved source revision.

Updated after the output-area PCB repair and the earlier schematic presentation redraw. The coil, input pole, and output pole of each relay remain separate A/B/C units, with visible wires, shared supply/RF buses, paired filter pins, and junction dots. Component references, electrical pin membership, and PCB association UUIDs were preserved. The current PCB has corrected connector/relay placement, locally rerouted traces, and explicit layer connections for the RF output and isolated return.

Latest update: four **R3 mm corner fillets**, a complete local-footprint audit, and **29 local 3D model assignments** have been applied. The 80 × 37 mm outside dimensions, mounting centers, component positions, pad geometry/UUIDs, and all tracks/vias are preserved. Letter sheet settings and native shared `DOC_*` title-block variables remain in place.

## Flyback cathodes on the relay supply — 2026-11-13

Moved **D1–D5 pin 1 (cathode)** from host `+5V` to `RELAY_VPLUS` in the saved schematic and PCB. The cathodes and relay coil-positive pins now share W1 pin 2. The only host `+5V` members are J1 pin 1 and W1 pin 1. With W1 open, an external regulated 5 V supply can feed W1 pin 2 and main `GND`; `/GND_OUT` remains separate. Fit W1 for the existing shared-supply configuration. This intentionally adapts the original circuit; physical/sequencing qualification remains open.

The schematic diode branches now join the coil-supply bus. On the PCB, all 29 existing front-layer cathode-chain segments were retained geometrically and reassigned to `/RELAY_VPLUS`. Four old back-layer segments linking the cathode chain to W1 pin 1 were removed and replaced with two 0.30 mm back-layer segments from D5 pin 1 at (58.89,55.8) through (59.94,56.85) to W1 pin 2 at (59.94,58.4) mm in sheet coordinates. All footprint placements, pad geometry, and footprint/pad UUIDs are preserved; only the five diode pad net assignments change. Project settings are unchanged.

Zone refill exposed one isolated, unrouted `GND` via at sheet coordinate (62.9,63.38) mm, UUID `f4eddd31-dbbf-4520-8888-0793ce630fa5`. It produced one dangling-via warning and one unconnected finding. The unused via was removed; no routed connection depended on it. No rule or exclusion was changed.

KiCad **10.0.6** final ERC and DRC after refill/save, with all severities and schematic parity, report **zero findings**, exit **0**. The independent connectivity audit passes **140 pins/33 nets**, PCB membership, and all default switching paths. Explicit supply-net assertions confirm the host rail has exactly two pins, while the relay rail has W1 pin 2, all five coil-positive pins, and all five cathodes. Generator defaults, schematic redraw wiring, connection map, and independent expected-pin audit are updated; full regeneration was not run over hand edits.

The schematic PDF and top/bottom copper exports were regenerated, rendered, and visually inspected. Python syntax, local Markdown links, file attributes/ignore behavior, and whitespace checks pass. Reports: `generated/erc-flyback-supply.rpt`, `generated/drc-flyback-supply.json`; visuals: `generated/flyback-schematic-detail.png`, `generated/flyback-board-top.svg`, and `generated/flyback-board-bottom.svg`; pre-edit snapshots: `generated/before-flyback-supply/`. No hardware or RF tests were performed.

## User-saved SMA placement and project state — 2026-11-13

Recorded the remaining user-saved schematic/project edits after the ground-symbol commit. X1 and X2 are repositioned with revised label placement and equivalent signal/shield wire branches. X2 was recreated in the editor and has a new schematic UUID. Pin/net membership and existing SMA footprint fields are unchanged. KiCad also normalized native schematic formatting, field ordering, and explicit body-style settings; embedded symbol definitions are unchanged. The project records `used_designators` as `X2,#PWR1`.

KiCad **10.0.6** ERC and DRC with all severities and schematic parity report **zero findings**, exit **0**. The independent audit passes **140 pins/33 nets**, PCB membership, default switching paths, and local dependencies. The PCB is unchanged from commit `0772d46`; no physical board geometry was edited. The native schematic is authoritative; the redraw helper's earlier placement defaults were not run over or synchronized with these user edits.

The maintained one-page Letter schematic PDF was regenerated and visually inspected against the saved source. Local Markdown links and whitespace checks pass. Reports: `generated/erc-user-save.rpt`, `generated/drc-user-save.json`; preview: `generated/schematic-user-save.png`. Hardware, physical connector fit, and RF qualification remain open.

## Project-local triangular grounds — 2026-11-13

Copied the user's W8 `power:GND` symbol into the independent library as `relay-switched-lpf:GND`, preserving its standard full-size triangular artwork and global power behavior. Replaced all 16 former two-bar drawn ground markings; W8 now also references the local definition. One redundant W7 marker at an already connected input-ground junction was removed. There are **17 local GND instances**, including the ground used with the new host-ground ERC flag. J1's textual ground pin labels remain labels. `/GND_OUT` is unchanged and remains separate.

The user-saved schematic/project edits were preserved. The schematic's global main net is `GND`; the PCB changes only the former `/GND` net-name references to `GND`. A byte comparison verifies no other PCB change: copper fills, tracks, vias, footprints, pads, outline, UUIDs, and rule settings are unchanged. The project file is byte-identical to the pre-edit user version. Exact exported component/pin net membership is unchanged from the user-saved input schematic.

Added a project-local standard `PWR_FLAG` on main ground to assert the externally supplied host return. The input schematic's single `power_pin_not_driven` ERC error is resolved. Two intermediate off-grid flag warnings were corrected by placing the flag/ground on the unchanged connection grid. No check was excluded or threshold relaxed. The redundant W7 marking and nearby RL1C property text were adjusted for legibility.

KiCad **10.0.6** final ERC and DRC with all severities and schematic parity report **zero findings**, exit **0**. The independent audit passes **140 pins/33 nets**, PCB membership, default switching paths, and local library dependencies. Local/embedded ground and flag symbols and the redraw helper are synchronized; a full redraw was not run over the user-edited schematic. The refreshed one-page Letter PDF was rendered and visually inspected. Local Markdown links, Python syntax, attributes/ignore behavior, and `git diff --check` pass. Reports: `generated/erc-ground-symbols.rpt`, `generated/drc-ground-symbols.json`; preview: `generated/schematic-ground-symbols.png`; pre-edit snapshot: `generated/before-ground-symbols/`. Hardware/RF qualification remains open.

## Coaxial arc geometry correction — 2026-11-13

Corrected the two shield-arc midpoints in local/embedded `Conn_Coaxial` definitions. The earlier scale helper transformed arc endpoints but omitted `mid`, distorting the shield into a flattened lens. `scale_local` now scales midpoints too. The corrected helper reproduces the saved symbol geometry exactly. A source comparison against `3a55c9c` confirms only these midpoint coordinates change in the schematic and symbol library; all connections, pin endpoints, placed-symbol identities/properties, and PCB remain unchanged.

KiCad **10.0.6** ERC and DRC/parity with all severities report **zero findings**, exit **0**. The PDF was regenerated and an enlarged X1/X2 detail rendered and inspected: both now show the standard round coaxial shield outline. Reports: `generated/erc-coax-arcs.rpt`, `generated/drc-coax-arcs.json`; corrected detail: `generated/coax-arcs-detail.png`. Whitespace and helper syntax checks pass. Hardware/RF qualification remains open.

## X1/X2 coaxial symbols — 2026-11-13

X1 and X2 now use project-local `Conn_Coaxial`, adapted from KiCad 10.0.6 `Connector:Conn_Coaxial`. The standard center-contact/shield graphics and passive pin names/numbers are retained, translated and scaled for the compact sheet. Local/embedded definitions and the redraw helper agree. Their labels are positioned clear of the coaxial graphics. The two shield wire branches and their junctions are repositioned to the downward shield pins; pin 1 remains at the original signal endpoint.

Both retain pin 1 on `/LPF1_OUT` and pin 2 on `/GND_OUT`. Footprint fields, values, references, instance/pin UUIDs, and all other placed symbols are preserved. The PCB is byte-identical to commit `8fc9521`, retaining the existing distinct vertical/edge SMA footprints and routing.

KiCad **10.0.6** ERC and DRC with all severities and schematic parity report **zero findings**, exit **0**. The independent audit passes all **140 pins/33 nets**, PCB membership, and default switching paths. The refreshed one-page Letter PDF and enlarged connector detail were rendered and visually inspected. Helper syntax, local Markdown links, and whitespace checks pass. Reports: `generated/erc-coax.rpt`, `generated/drc-coax.json`; visual detail: `generated/coax-detail.png`. Physical connector fit and RF qualification remain open.

## J1 boxed connector symbol — 2026-11-13

J1's project-local `Port_10` now uses the matching boxed connector body and ten contact marks, adapted from KiCad `Conn_01x10`. Local/embedded definitions and the redraw helper agree. Only this symbol definition changes in the saved schematic: all placed symbols, properties, UUIDs, wiring, labels, pin endpoints/numbers/electrical types, and PCB footprint assignments remain unchanged. The PCB is byte-identical to commit `c896664`; J1 retains its underside 2 × 5 host socket footprint.

KiCad **10.0.6** ERC and DRC with all severities and schematic parity report **zero findings**, exit **0**. The independent 140-pin/33-net connectivity and default switching-path audit passes. The updated one-page Letter schematic PDF was rendered and visually inspected. Helper syntax, local Markdown links, and whitespace checks pass. Reports: `generated/erc-j1.rpt`, `generated/drc-j1.json`; preview: `generated/schematic-j1.png`. Hardware and RF qualification remain open.

## W1–W9 boxed connector symbols — 2026-11-13

All nine wire jumpers now use boxed connector body/contact graphics: `Link2` for W1/W8/W9, `Selector3` for W2–W6, and `InputSelector3` for W7. Pin endpoints, numbers, passive electrical types, references, values, instance/pin UUIDs, and PCB footprint assignments are preserved. The PCB is byte-identical to commit `f3a92e7`; default fitted/open links are unchanged.

Small schematic-only layout changes keep wires outside the new bodies: the RFO bus and selector branches are repositioned, W7's ground marking is shifted, W9's COM wire is jogged, and nearby labels/W8/W9 property text are moved. Local and embedded symbol definitions and the redraw helper agree. No full redraw was run over the saved schematic.

KiCad **10.0.6** ERC and DRC with all severities and schematic parity finish with **zero findings**, exit **0**. The independent audit passes for all **140 pins/33 nets**, PCB membership, and default switching paths. An intermediate ERC warning identified a dangling RFO bus tail; the unused tail was removed, with no exclusion or threshold changes. The refreshed one-page Letter schematic PDF was rendered and visually inspected. Python syntax, local Markdown links, and whitespace checks pass. Reports: `generated/erc-wire-symbols.rpt`, `generated/drc-wire-symbols.json`; preview: `generated/schematic-wire-symbols.png`. Hardware and RF qualification remain open.

## J21–J26 connector appearance — 2026-11-13

All six antenna/output connectors J21–J26 now use the standard KiCad `Conn_01x02` boxed connector appearance. Project-local `AntennaConnector2` serves J21–J25; `OutputConnector2` serves J26 with its existing orientation and compact pin spacing. The library, embedded definitions, and redraw helper agree. No full redraw was run.

A structured comparison against commit `f58de32` confirms that exactly J21–J26 change library IDs. All instance UUIDs, properties, pin UUIDs, footprint assignments, pin endpoints/electrical types, wires, labels, and other placed symbols remain unchanged. The PCB is byte-identical to that commit.

KiCad **10.0.6** ERC and DRC with all severities and schematic parity report **zero findings**, exit **0**. The independent 140-pin/33-net membership and switching-path audit passes. The updated schematic PDF was rendered and visually inspected. Local Markdown links and `git diff --check` pass. Reports: `generated/erc-j21-j26.rpt`, `generated/drc-j21-j26.json`; preview: `generated/schematic-j21-j26.png`. Hardware and RF qualification remain open.

## Output-return layer repair — 2026-11-13

The two remaining `/GND_OUT` connections are repaired with two 0.60/0.30 mm through vias and three 0.20 mm traces at X2. The upper via is at board coordinate (74.98, 9) mm, connecting the existing bottom return trace to the front upper ground land. The lower via is at (75.5, 14) mm, with front/back diagonal traces to (76.5, 15) mm, joining the lower lands and existing return routing. Both vias are inland of the SMA lands. `/GND_OUT` remains separate from `/GND`.

KiCad **10.0.6**, after zone refill and save, reports **0 rule violations, 0 unconnected items, and 0 schematic-parity findings**, exit **0**, with `--severity-all --schematic-parity --exit-code-violations`. No thresholds, ignored-check settings, or exclusions were changed. This supersedes the two unresolved-connection results in the earlier entries below.

A structured comparison with the pre-edit snapshot confirms every existing non-zone UUID-bearing object is unchanged, including all original tracks/vias, footprints, pads, and outline objects; exactly two vias and three segments were added, all on `/GND_OUT`. The existing zones were refilled. Top/bottom copper exports were rendered and visually inspected. The independent pin/net, PCB membership, and default switching-path audit passes. The schematic is unchanged; its previous clean ERC result remains applicable, and ERC was not rerun for this board-only repair.

Changed source files: native PCB, README, and this validation record. The reconstruction generator was not run or changed. Report: `generated/drc-ground-out-repair.json`; visual exports: `generated/ground-out-repair-top.svg` and `generated/ground-out-repair-bottom.svg`; pre-edit board: `generated/before-ground-out-repair/`. Hardware, physical connector fit, and RF qualification remain open.

## Four-pin connector symbol update — 2026-11-13

All ten LPF socket symbols (J2–J11) now use the boxed body and contact marks of standard KiCad `Connector_Generic:Conn_01x04`, adapted to the existing compact schematic through the project-local `LPF_IN`/`LPF_OUT` definitions. See [asset attribution](KICAD-LIBRARY-LICENSE.md#four-pin-connector-symbols). The local library, schematic cache, and redraw helper agree. No full redraw or PCB edit was performed.

A structured before/after comparison confirms that only these two embedded definitions changed: all symbol instances, UUIDs, properties, pin endpoints/numbers, footprints, wires, labels, and junctions are identical. KiCad **10.0.6** ERC reports **0 errors and 0 warnings**, exit **0**. The independent connectivity audit passes for **140 pins, 33 nets**, all default switching paths, and PCB pad membership. Current DRC reports **0 rule violations, 2 unresolved `/GND_OUT` connections, and 0 schematic-parity findings**, exit **5**. No rule or exclusion settings were changed.

The maintained schematic PDF was regenerated, rendered, and visually inspected: one US Letter landscape page (792 × 612 points), with clear connector symbols and labels. Redraw helper syntax, local Markdown links, and whitespace checks pass. Reports: `generated/erc-connector-symbols.rpt`, `generated/drc-connector-symbols.json`, and `generated/schematic-connector-symbols.png`. Pre-edit schematic/library/helper/PDF copies are in `generated/before-connector-symbols/`. Hardware/RF qualification remains open.

## Full-board ground-pour update — 2026-11-13

Both existing `/GND` zone outlines now cover the full 80 × 37 mm board on F.Cu and B.Cu. The input board already had no `/GND_OUT` zones; none were restored. Clearance still separates `/GND` from `/GND_OUT` pads and tracks. Disconnected copper islands are now always removed, rather than retained above the previous 10 mm² cutoff. Edge, track, pad, and hole clearances are unchanged.

KiCad **10.0.6** refilled and saved the board. DRC with `--severity-all --schematic-parity --exit-code-violations` reports **0 geometric/rule violations, 2 unconnected items, and 0 schematic-parity findings**; exit **5**. The unresolved connections involve X2's `/GND_OUT` lands and the front/back output-return traces. No findings were excluded or downgraded. These current results supersede the previous clean-board claims below. Schematic ERC was not rerun for this copper-zone-only edit.

The top and bottom copper SVG exports were rendered and visually inspected. A byte comparison confirms that all source before the zone definitions—including footprints, tracks/vias, outline, net assignments, and board settings—is unchanged from the pre-edit snapshot. Only the native PCB and this validation/README documentation were edited; the reconstruction generator was not run or changed. Its older zone defaults are not synchronized with this hand edit.

Reports and previews: `generated/drc-full-ground.json`, `generated/full-ground-top.svg`, and `generated/full-ground-bottom.svg`. The pre-edit board is preserved in `generated/before-full-ground-pours/`. Hardware and RF validation remain unperformed.

## Results

| Check | Result |
| --- | --- |
| Schematic ERC, `--severity-all --exit-code-violations` | **0 violations**, exit 0 |
| Independent schematic connectivity audit | **Pass:** 140 unique component pins across 38 electrical items, 48 symbol units, and 33 nets |
| PCB-to-exported-schematic net membership | **Pass:** every numbered pad agrees; duplicate connector-return pads are consistent |
| Default switching-path topology | **Pass:** band 0 uses LPF1; band 1 uses LPF1; bands 2–5 use their selected filter followed by LPF1; selected RF paths do not connect to either ground net in the carrier |
| PCB DRC, `--severity-all --schematic-parity --exit-code-violations` | **0 rule violations, 0 unconnected items, 0 parity findings**, exit 0; see latest update above |
| Unconnected PCB items in the currently saved board | **0** |
| Schematic parity findings | **0** |
| Local library/model dependencies | **Pass:** all schematic symbols local; 42 board footprints resolve to eleven local definitions; 29 assigned model instances resolve to seven local STEP/VRML files |
| Rounded outline | **Pass:** four retained straight segments shortened tangentially and joined by four R3 mm arcs; closed outline, unchanged 80 × 37 mm extents and mounting centers |
| Holes, track clearance, and thermal relief | No remaining findings in the final DRC run |
| Letter page size | Both schematic and PCB proof exports are **one 792 × 612 point page**, exactly 11 × 8.5 inches |
| Shared-field expansion | Both sheet exports show the retained common title, author, date, and revision. Temporary export overrides `DOC_REVISION=SYNC-CHECK` and `DOC_COMMENT1=SHARED-CHECK` render on both sheets; saved project values remain unchanged. |
| Visual review | Top isometric, bottom isometric, and direct top 3D renders inspected for corner shape, all five diodes/relays, ten filter sockets, underside host socket, default wire links, and both generic SMA alternatives. Updated Letter schematic PDF regenerated and inspected. |
| Markdown links, whitespace, and file attributes | Local project/root-index links checked; `git diff --check` passed; KiCad sources remain LF text and PDF remains binary |
| Ignore behavior | `generated/` reports ignored; native design/library files are trackable |
| Mechanical / assembly / RF / hardware | **Not performed** |

No DRC findings are excluded, and no severities or thresholds were weakened to obtain these results. Normal KiCad defaults otherwise remain in the project. The default net-class clearance is 0.20 mm, board-edge clearance is 0.50 mm, and minimum hole spacing is 0.25 mm. The saved board contains 0.20 mm and 0.30 mm tracks and 0.60/0.30 mm and 0.65/0.30 mm vias; the latest return repair uses 0.20 mm tracks and 0.60/0.30 mm vias. These are layout choices, not a controlled-impedance stackup or an RF performance specification.

The schematic is a passive carrier model; ERC does not establish a real controller, power source, compatible driver, LPF module, or correctly assembled wire link. The switching-path audit models each LPF as an ideal two-port connection to check topology; it does not simulate its frequency response or its internal ground path.

## Current checks and prior warnings

Five B.Silkscreen warnings were recorded at the earlier Letter-sheet review. They are absent from the latest saved board and latest full DRC run. The current model/fillet work preserves the input board's silkscreen text and positions; it does not claim to have repaired those earlier legend overlaps. No warning has been excluded or downgraded.

The compact schematic uses a standard 25 mil connection grid, with resized project-local symbol graphics and matching embedded definitions. The loaded project had reverted to 50 mil; restoring the documented 25 mil grid clears its off-grid warnings while retaining the off-grid check. ERC and the independent pin/net audit verify all electrical connections. W9's hidden PCB value was synchronized with the existing schematic value to clear one pre-existing parity warning. Shared fields live in `.kicad_pro` `text_variables`; editing `DOC_*` there or in either editor's Project Text Variables updates both title blocks. A direct replacement of a title-block placeholder would remove that field's shared reference.

## Fillets, local libraries, and 3D coverage

The four corner arcs have centers at board coordinates (3,3), (77,3), (77,34), and (3,34) mm, with 3 mm radii. The radius is a reconstruction choice, not an original-board measurement. Existing mounting-hole centers remain fixed, leaving 1.4 mm nominal board material between each 3.2 mm drill and its concentric corner arc. Copper was refilled against the new outline; no routing or clearance threshold was changed.

Every board footprint now has a project-local library ID, including H1–H4. W1/W3–W7 use fitted-link variants with the same pad geometry as the bare versions; only model population and library association differ. Schematic footprint fields match these variants, and the pin/net audit still passes. The mounting holes are board-only source footprints, excluded from component BOM/positions as before.

Model coverage is 21 required carrier parts, two alternative SMA previews, and six default wire links. Bare terminals, open links, and unselected mounting hardware do not have invented component bodies. The three KiCad STEP assets are bundled locally with original notices and SHA-256 provenance. Four original nominal VRML assets cover the TX2 relay, generic SMA options, and wire links. All model references use `${KIPRJMOD}` and resolve locally. See [coverage, provenance, and model limits](relay-switched-lpf.3dshapes/README.md) and [imported asset terms](KICAD-LIBRARY-LICENSE.md).

No installed global 3D library is needed to view the saved assembly or rerun the mechanical finishing step. The model generator reproduces original previews from source; imported STEP files remain bundled assets. The main generator invokes the finishing step so later regeneration retains rounded corners and local model assignments. Full regeneration was not run over the hand-edited board; the native saved PCB was checked directly.

## Output-area repair

The pre-repair PCB hash was `8e8afe96f3d8336100d26c4c1dbdd11778bdf1ac1a15f80c8484e526cf7f2e3b`. Its three geometric errors and two unconnected findings were resolved as follows:

| Previous count | Finding | Repair |
| --- | --- | --- |
| 2 | `copper_edge_clearance`, X1 | Move X1 left 0.381 mm, to board coordinate (75.819, 23) mm. Right-hand pad copper now has 0.541 mm nominal edge clearance, exceeding the unchanged 0.50 mm rule. |
| 1 | `courtyards_overlap`, RL1/X1 | Move RL1 left 0.762 mm, to board coordinate (67.818, 18.62) mm. The original library courtyard shapes now clear one another; no body/courtyard shrink was used. RFI, LPF1 input, and relay-1 COM branches were locally rerouted around the moved pads. |
| 1 | X2 RF layer connection | Add a 0.65 mm / 0.30 mm through via at board coordinate (75, 12) mm, with 0.30 mm copper connections to both RF lands. The via is inland of the SMA solder land. |
| 1 | Isolated-return layer connection | Add a 0.65 mm / 0.30 mm through via at board coordinate (78, 10.5) mm, tied to X2's upper ground land on both layers. Refill the GND_OUT planes; retain separation from main GND. |

The filter-socket and mounting-hole positions, footprint-library pad sizes, and electrical nets remain unchanged. X2 retains its existing (78.5, 12) mm footprint origin. The local rerouting adds further layer transitions where needed to avoid other copper; all hole, pad, track, thermal, and copper-clearance checks pass. Later Letter-sheet work changed schematic presentation; the current mechanical step changes the outline corners and models while preserving positions and copper routing.

A before/after source comparison confirms that only RL1 and X1 changed footprint positions; every footprint/pad UUID, local pad geometry, other placement, and outline segment was retained. The board now has 18 vias versus 10 before repair: two dedicated X2 transitions and six transitions in the three locally rerouted branches. Generator placement defaults and pre-routing X2 transitions were synchronized and syntax-checked. Full regeneration was not run over the saved board; the final checks above apply to the repaired native PCB.

**ERC and current DRC pass; hardware qualification remains open.** No exact SMA manufacturer/order code, connector/board-thickness fit, host/mounting fit, or RF performance has been established. The original manual's vertical-SMA/filter interference warning still requires a physical clearance review. The new nominal previews do not resolve these physical uncertainties.

## Source and geometry audit

The circuit was read from p. 4 of the [Rev. 5 manual](https://qrp-labs.com/images/ultimatelpf/assembly_ulpf2.pdf), with p. 3 trace and pp. 5–7 assembly drawings used to cross-check physical orientation. The paired LPF signal pads are included: input pins 3/4 and output pins 1/2. Slot-1 output ground is pins 3/4 on the separate `GND_OUT` net. Relay-1 COM pin 4 has its own accessible RF node, represented by optional W9, and is not silently wired into the default final-output path.

The 80 × 37 mm outline is published. The 33.02 mm socket-row spacing, 13.97 mm slot spacing, mounting centers, and connector coordinates are pitch/drawing-derived and **not measured from original hardware**. The board has new routing, adjusted link/terminal positions, an assigned standard numeric host convention, consolidated optional ground-bridge pads, and generic output-connector geometry. It does not claim original Gerber or host-mating equivalence.

The independent enumeration in [design/audit.py](design/audit.py) checks the exported XML and saved PCB rather than comparing only generator data with itself. [design/connections.json](design/connections.json) is an additional machine-readable design map; it is not the audit's expected-data input. Pin membership and all six default switching-path checks still pass after the PCB repair. DRC separately confirms that actual copper has no unconnected items or shorted nets.

## Source identification

SHA-256 hashes of the checked source revision:

| File | SHA-256 |
| --- | --- |
| `Relay-Switched LPF.kicad_sch` | `8d29a67e48bcef2ccf27a937c9127061c5367abe47d48cc13f11de34d477377c` |
| `Relay-Switched LPF.kicad_pcb` | `80c827c9e3a5d6f1692aad18a382a7e781d30d935223cb6ca27f263bc11ce477` |
| `relay-switched-lpf.kicad_sym` | `60824d9e999deb88c2240adb61f15bfa4871622dbde0935b79be750b3041e995` |

Recheck after any source edit. Final pre-commit reports `erc-precommit.rpt`, `drc-precommit.json`, `connectivity.xml`, earlier reports, and visual exports reside in ignored `generated/`. The final KiCad 10.0.6 ERC and DRC/parity checks passed with zero findings; the independent connectivity audit also passed. The maintained schematic PDF is an intentional reference export; the native schematic is authoritative.

## Remaining qualification

1. Select the intended output connector and verify its land pattern, board thickness, assembly requirements, and fabrication compatibility. Generic connector previews are not verified part selections.
2. Measure real LPF modules, the mating host header, mounting centers, board outline/corners, spacer height, and relay-to-module vertical clearances. The inferred mounting pattern is not a fit guarantee.
3. Verify relay terminal numbering, the actual surplus relay type, header mirroring, diode polarity, six fitted links, and ground isolation by inspection and unpowered continuity measurements.
4. Test 5 V coil voltage/current, driver compatibility, all selected/rest states, and muted switching with the actual host.
5. Measure insertion loss, return loss, filter response, harmonic attenuation, channel isolation, heating, and power handling over the intended bands on the exact assembled revision and fixture. No such performance has been inferred from clean ERC, connected copper, or a successful export.

No push, release, fabrication package, device installation, or hardware operation was performed.
