# Relay-Switched LPF

Independent KiCad reconstruction of the **QRP Labs Ultimate relay-switched LPF carrier, PCB Rev. 5**. Open [Relay-Switched LPF.kicad_pro](Relay-Switched%20LPF.kicad_pro). The editable [schematic](Relay-Switched%20LPF.kicad_sch), [PCB](Relay-Switched%20LPF.kicad_pcb), and [schematic PDF](Relay-Switched%20LPF.pdf) belong to this project.

**Engineering reconstruction, drawing revision v0.0.1; not qualified for fabrication or use.** The published circuit is reconstructed, and a new two-layer layout is provided inside an 80 × 37 mm outline. This is not an original QRP Labs CAD release, an exact trace copy, or a verified mechanical replacement. Read [VALIDATION.md](VALIDATION.md) for actual checks and remaining findings before ordering anything.

## What is included

- Five Panasonic TX2-5V DPDT relay channels, five 1N4148 flyback diodes, and ten four-position LPF sockets.
- An underside 2 × 5 host socket, active-low band controls, separate coil-supply link, five output selectors, a final-filter input selector, and an optional output-ground bypass.
- Five individual antenna solder-terminal pairs, a final-output terminal pair, and alternative generic vertical and edge SMA pad groups.
- Independent [symbol library](relay-switched-lpf.kicad_sym), [footprint library](relay-switched-lpf.pretty/), and `${KIPRJMOD}` library tables. No references to other repository projects or machine-specific library locations.
- [Project-local 3D models](relay-switched-lpf.3dshapes/README.md) for the carrier components, optional SMA connectors, and default fitted wire links; the four mounting-hole footprints are also local.
- [Reconstruction generator](design/generate.py), [routing script](design/route.py), and [connectivity audit](design/audit.py). These are reproducibility tools; the saved native CAD files remain authoritative after hand edits.
- Ten four-pin LPF connectors use the standard KiCad boxed `Conn_01x04` appearance, adapted in the project-local `LPF_IN`/`LPF_OUT` symbols; see [attribution and license](KICAD-LIBRARY-LICENSE.md#four-pin-connector-symbols).
- A visibly wired schematic arranged like the published diagram: relay coils and flyback diodes above the shared RF input bus, five filter columns, and a shared output bus below. Relay units A/B/C are the coil/input pole/output pole of the same physical relay. [Redraw tool](design/redraw_schematic.py) updates the schematic and its local symbol graphics without writing the PCB.

The plug-in filter circuits, band-dependent inductors/capacitors, Ultimate3S transmitter, sixth relay/filter on that transmitter, GPIO drivers, enclosure, and spacers are external. No arbitrary filter bands or component values have been selected.

## Default circuit and assembly

Install the highest-frequency LPF in **slot 1**, on the right. Energizing one of relays 2–5 selects its filter, whose output feeds slot 1 through the common `RFO` bus. Energizing relay 1 feeds its filter directly from `RFI`. With no carrier relay energized, an external filter-0 signal on `RFO` can still pass through slot 1. Filters 2–5 have both RF terminals grounded when their relays are at rest.

The saved PCB represents **unbridged wire-link pads**. Fit these six separate wire links for the default LPF configuration:

| Link | Fit | Function |
| --- | --- | --- |
| W1 | 1–2 | Connect `+5V` to `RELAY_VPLUS` |
| W2 | **Open** | Slot-1 relay output selector; final output already comes directly from LPF1 |
| W3, W4, W5, W6 | Each 1–2 | Connect relays 2–5 to `RFO` |
| W7 | 1–2 | Feed relay-1 normally closed input from `RFO` |
| W8 | **Open** | Preserve isolated final output return |
| W9 | **Open** | Optional LPF1-output to relay-1 second-pole COM link |

W2–W6 each use pin 1 for the relay's output NO contact, pin 2 for `RFO`, and pin 3 for the corresponding individual `ANTn` terminal. W7 pins 1/2/3 are `RFO` / `FINAL_NC` / `GND`. W8 pins 1/2 are `GND` / `GND_OUT`. W9 pins 1/2 are `LPF1_OUT` / `FINAL_RELAY_COM`; it represents the separately accessible RF pads by relay 1 in the source circuit. The second pole of relay 1 is not in the default RF path. Link designators and pad ordering are assigned by this reconstruction, not original QRP Labs designators. An unfitted selector pad still has a routed net; it is intentionally not shorted by copper.

`GND_OUT` joins X1/X2 returns, J26 pin 2, and slot-1 output-socket pins 3/4. It remains separate from main `GND`; slot-1 output-socket pins 1/2 carry RF. Do not bridge these returns through mounting hardware, coax shields, or test equipment without considering the intended filter return path. W8 represents the original optional ground-bridge pad pairs as one two-terminal link, not a default connection.

The circuit retains alternate output selection pads, but this revision has only been audited against the default LPF configuration. Alternate BPF or separate-antenna assembly requires a separate connection review. The SMA groups are permanently connected to `LPF1_OUT`, not `RFO`; those nets are distinct.

## Host and module pin maps

J1 is on **B.Cu**, opposite the relays. In a component-side/top view, with slot 5 on the left and slot 1 on the right, J1's odd-numbered column is on the left, and its even-numbered column is on the right. Read each row from the input-socket edge toward the output-socket edge:

| Left pin | Net | Right pin | Net |
| --- | --- | --- | --- |
| 1 | +5V | 2 | BAND5_N |
| 3 | BAND3_N | 4 | BAND4_N |
| 5 | BAND1_N | 6 | BAND2_N |
| 7 | GND | 8 | RFI |
| 9 | GND | 10 | RFO |

This numeric convention is assigned to the published labeled pad arrangement. Confirm the mating host's numbering and orientation; do not infer compatibility from a generic 2 × 5 socket name. In top view, J1 pin 1 is at board coordinate (2.54, 8.26) mm, with 2.54 mm row/column pitch.

Band controls sink the relay-coil current. The nominal 5 V, 140 mW coil corresponds to approximately 28 mA. Use a suitable external sink driver for Raspberry Pi/Pico GPIO; the carrier contains no transistor or level shifter. Energize **at most one** band input at a time and mute RF during switching. Keep the flyback cathode supply and linked coil supply on the same 5 V rail in the default assembly.

| Item | Pin assignments |
| --- | --- |
| RLn | 1 coil+, 12 coil−; 8 NO/input bus, 9 COM/filter input, 10 NC; 5 NO/output selector, 4 COM/filter output for slots 2–5 (separate FINAL_RELAY_COM for slot 1), 3 NC/main ground |
| Dn | 1 cathode/+5V; 2 anode/BANDn_N |
| J2/J4/J6/J8/J10 | LPF1/2/3/4/5 input: pins 1/2 GND; pins 3/4 signal |
| J3/J5/J7/J9/J11 | LPF1/2/3/4/5 output: pins 1/2 signal; pins 3/4 GND except LPF1 pins 3/4 use GND_OUT |
| J21–J25 | ANT1–ANT5: pin 1 RF, pin 2 main GND |
| J26, X1, X2 | Pin 1 final RF output, pin 2 isolated GND_OUT; repeated X1/X2 pin 2 pads are intentional |

Input sockets run pin 1 left to pin 4 right in top view. Output sockets run pin 4 left to pin 1 right. Match module IN/OUT markings. There is no guaranteed RF power, frequency range, insertion loss, or isolation rating for the reconstructed layout.

## Geometry, population, and model limits

| Feature | Implemented geometry | Evidence / limit |
| --- | --- | --- |
| Outline | 80 × 37 mm, two layers, four tangent R3 mm corner fillets | Overall published size retained; radius selected for this reconstruction, not a measured original-board radius |
| Filter sockets | 2.54 mm pitch; 33.02 mm input/output row spacing; 13.97 mm slot spacing | Pitch-based reconstruction of the placement/trace drawings; confirm on real modules |
| Mounts | Four 3.2 mm NPTH holes at (3,3), (77,3), (3,34), (77,34) mm | **Inferred**, not dimensioned in the manual; must be measured against host/spacers |
| Relays | 15 × 7.4 mm body; 5.08 mm pin-row separation, 5.08/2.54/2.54 mm longitudinal pin spacing; 1 mm drills | Standard TX2 terminal pattern reconstructed from available pin/dimension evidence; verify actual supplied surplus relay |
| Diodes | DO-35 axial, 7.62 mm lead pitch | New footprint choice, not a measured original lead bend |
| Wire links / terminals | Bare 1.8 mm pads, 1 mm holes, 2.54 mm pitch | Layout adaptation; not plastic headers |
| X1 | Generic vertical SMA, central signal and four returns at ±2.54 mm; center (75.819, 23) mm | CAD edge and courtyard checks pass; no selected manufacturer/order code or verified physical fit |
| X2 | Generic double-sided edge SMA land pattern; footprint origin (78.5, 12) mm, with RF and isolated-return layer transitions | CAD clearance/connectivity checks pass; no selected connector or qualified board thickness |
| Routing | New 0.30 mm two-layer traces with ground and isolated-return fills | Not an exact original trace geometry or controlled-impedance stackup |

The terminal and link locations have been adjusted within the published outline to make the reconstruction routable. Consequently, mating compatibility is not established by matching the board's outer dimensions. X1 is an alternative to X2/J26; using a short coax pigtail on the output pads avoids assuming a generic SMA fits underneath a filter. Review vertical clearances to the plug-in filters and the original warning about vertical SMA interference.

The output-area DRC repair moves RL1 left 0.762 mm and X1 left 0.381 mm from their initial placements, preserving socket/mounting coordinates. Nearby RFI, LPF1 input, and relay-1 COM traces are rerouted. Two 0.65/0.30 mm vias join X2's RF lands and its isolated output return between copper layers. The latest hand edit extends both main-ground pours across the board, with clearance around the separate output-return pads and traces. Two dedicated return vias and short traces now connect X2’s front/back ground lands. KiCad 10.0.6 reports zero rule violations, unconnected items, or schematic-parity findings; see [current validation](VALIDATION.md#output-return-layer-repair--2026-11-13). Physical connector fit and RF qualification remain open.

The 3D viewer now uses seven local STEP/VRML assets across 29 model instances: the 21 normal carrier components, both optional SMA alternatives, and six fitted wire links. The socket and diode STEP files are unmodified KiCad assets; the relay, SMA, and wire models are documented original nominal previews. No unrelated relay/connector model is silently substituted. Bare terminals, open links, and mounting holes have no invented part bodies. See [model coverage and limits](relay-switched-lpf.3dshapes/README.md) and [KiCad asset terms](KICAD-LIBRARY-LICENSE.md).

Twenty-one normal carrier components are needed before wire links: five relays, five diodes, ten four-way sockets, and one ten-way underside socket. SMA hardware is optional; filter modules, six default wire links, and mounting hardware are separate assembly items. The two SMA previews are alternatives, not an instruction to assemble both. See [BOM.csv](BOM.csv).

All 42 saved board footprints, including the four mounting holes, resolve to eleven project-local footprint definitions. The six fitted wire links use model-bearing variants whose pad geometry is identical to the bare versions. Every schematic symbol is in the independent local symbol library. Keep the entire project folder, including `.pretty` and `.3dshapes`, together when copying it.

## Letter sheets and shared title-block fields

The schematic fits on one **US Letter landscape sheet, 11 × 8.5 inches**, matching the selected ANSI A page setting in both editors. The compact symbols use a standard 25 mil schematic connection grid. The PCB drawing-sheet size is the same; its actual board geometry is unchanged by this page-format work.

Edit shared values under **Schematic Setup or Board Setup → Project → Text Variables**. Both title blocks refer to the same project variables, so set these values once rather than replacing their `${DOC_...}` references in Page Settings:

| Project variable | Shared field | Current value |
| --- | --- | --- |
| `DOC_TITLE` | Title | Relay-Switched LPF |
| `DOC_DATE` | Date | 11/13/2026 |
| `DOC_REVISION` | Revision | v0.0.1 |
| `DOC_COMPANY` | Company / author | Lee Bussy [AA0NT] |
| `DOC_COMMENT1`–`DOC_COMMENT4` | Comments 1–4 | Empty |
| `DOC_COMMENT5`–`DOC_COMMENT9` | Additional optional comment placeholders | Define shared variables if used |

These are native [KiCad project text variables](https://docs.kicad.org/10.0/en/eeschema/eeschema.html), stored in the `.kicad_pro` file and usable by both editors. The date is an explicit shared value, not an automatic clock. [Shared-field setup tool](design/shared_fields.py) installs the references while retaining existing project values; the redraw and full-generation tools preserve those values on later runs. The filenames and sheet numbers remain editor-specific.

## Rebuilding and checking

Creation and checks use **KiCad 10.0.6**. The generators overwrite this project's CAD; save hand edits before regenerating. Run `design/generate.py` and then `design/route.py` using a Python installation with KiCad's `pcbnew`, wxPython, and NumPy. On macOS, the bundled KiCad Python requires access to the logged-in display session. Routing refuses an already routed board.

The full generator invokes `design/redraw_schematic.py` after creating the initial circuit. To rebuild only the schematic presentation from the saved references and connection map, run `python3 design/redraw_schematic.py`; this uses only Python's standard library. Re-export the PDF and rerun ERC and the connectivity audit afterward. Net labels are retained for names, host connections, and ground references; the filter and relay interconnections are drawn as wires.

The full generator also invokes [design/finish_mechanics.py](design/finish_mechanics.py), which assigns the local models and fitted-link variants, localizes mounting holes, and applies R3 corners. Its imported models are bundled local files, not downloads from installed libraries. [generate_previews.py](relay-switched-lpf.3dshapes/generate_previews.py) reproduces the four original nominal VRML assets. Normal KiCad software/Python dependencies remain necessary for CAD operations.

From this folder, using `kicad-cli` on PATH:

```bash
mkdir -p generated
kicad-cli sch erc --severity-all --exit-code-violations -o generated/erc.rpt 'Relay-Switched LPF.kicad_sch'
kicad-cli sch export netlist --format kicadxml -o generated/connectivity.xml 'Relay-Switched LPF.kicad_sch'
python3 design/audit.py
kicad-cli pcb drc --severity-all --schematic-parity --exit-code-violations --format json -o generated/drc.json 'Relay-Switched LPF.kicad_pcb'
```

The latest checked PCB has zero errors, warnings, unconnected items, or schematic-parity issues; no findings are excluded. Any later regeneration or edit requires fresh checks; the generators retain the repaired placements and reserve the X2 layer transitions before routing. Generated reports/previews are ignored; [VALIDATION.md](VALIDATION.md) records results against source hashes. Do not substitute successful exports, connectivity checks, routing, or 3D renders for physical or RF validation.

## Sources and rights

Accessed 2026-11-13:

- [QRP Labs Ultimate relay-switched LPF page](https://qrp-labs.com/ultimatelpf.html): product identity, documented revisions, connector options, and alternate configurations.
- [QRP Labs Rev. 5 assembly manual](https://qrp-labs.com/images/ultimatelpf/assembly_ulpf2.pdf), document version 8, 06-Jan-2022: pp. 1–2 parts and operation; p. 3 trace drawing; p. 4 circuit; pp. 5–7 placement, default links, and assembly. The body text's `RX2` spelling conflicts with the `TX2-5V` parts list and circuit; the reconstruction follows the latter.
- [QRP Labs plug-in LPF page](https://qrp-labs.com/lpfkit): external filter-module family, not a source of selected filters for this project.
- [Panasonic TX2-5V manufacturer page](https://na.industrial.panasonic.com/products/relays-contactors/mechanical-signal-relays/series/11597/model/12070): single-side-stable, 5 V, 140 mW, 2 Form C part identity. The 2 A resistive contact rating is not treated as an RF rating.

QRP Labs' circuit, manual, photographs, and product names retain their owners' rights. The original board artwork, manual PDF, and photographs are **not redistributed** here; no QRP Labs CAD license has been established, and the source design is not represented as repository-owned MIT work. Newly drawn documentation, library geometry, nominal previews, and generator code use the repository [MIT license](../LICENSE.md). Three unmodified KiCad STEP assets retain their [original library license and attribution](KICAD-LIBRARY-LICENSE.md). The four-pin connector artwork is adapted from KiCad `Connector_Generic:Conn_01x04` under its library license and exception; other symbol and footprint artwork is original. This project is unaffiliated with QRP Labs.
