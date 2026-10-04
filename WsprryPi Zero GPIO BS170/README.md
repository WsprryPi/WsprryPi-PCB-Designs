# WsprryPi Zero GPIO BS170

This is a separate KiCad project in the same Git repository. It was copied from `WsprryPi Zero GPIO` as a starting point, with its own project files, project-local symbol and footprint libraries, and `${KIPRJMOD}` model paths. The saved schematic and PCB contain the single-BS170 RF stage, switched 5 V supply, adjustable gate bias, and LPF interface. The block-renumbering change preserves their existing wiring and layout.

A KiCad 10 project initialized from the `RPi Zero HAT Template` for WsprryPi GPIO development. It provides the Raspberry Pi Zero-size uHAT geometry, a complete 40-pin GPIO interface, a selectable underside socket model, a socket purchasing item, and independent local libraries.

The schematic retains the load-switch circuit, GPIO selection header, LPF interface, and edge-launch SMA output. The RF path uses the 30-, 40-, and 50-Series sections, supplied by the 20-Series switched 5 V circuit. The design intentionally omits an identification EEPROM and leaves ID_SD and ID_SC unused. The copied two-layer board has not been fabricated or physically qualified.

**Cost redesign in progress:** the two-transformer LTC6432-15 implementation is too expensive and is no longer the forward design choice. See the [single-BS170 redesign proposal](BS170-REDESIGN-PROPOSAL.md) for the lower-cost candidate and its band-dependent power limits. The hand-wound FT37-43 choke is selected, and all physical schematic parts now have local footprints. Completion of RF wiring, PCB implementation, sourcing, and physical/RF qualification remain open.

The copied 5 V LTC6432-15 circuit, its original RF estimate, and first-pass BOM are recorded in [BASELINE-AMPLIFIER-DESIGN.md](BASELINE-AMPLIFIER-DESIGN.md). Those details document the copied baseline and do not define the proposed BS170 circuit.

> **Order status: Not ready for order.** The BS170 schematic is partially wired, and the saved PCB remains the cost-rejected baseline. The new circuit, physical parts, layout, and electrical/RF performance have not been qualified. Do not submit the saved board for fabrication or assembly as the lower-cost design.

## Develop this HAT project

1. Open `WsprryPi Zero GPIO BS170.kicad_pro` in KiCad 10 and review the saved schematic and routed board together.
2. Wire the placed parts using the [BS170 redesign proposal](BS170-REDESIGN-PROPOSAL.md) as the circuit direction. Resolve its circuit, power, sourcing, and compliance decisions before preparing an order package.
3. After any design change, update the PCB from the schematic as needed, refill copper zones, and rerun ERC and DRC before reviewing the resulting diff.

This project has independent copies of the design files, symbol library, footprint library, and STEP model. Changes here do not update `RPi Zero HAT Template`, and later template changes do not update this project.

## Schematic block numbering

The schematic is arranged as five boxed functional sections. Circuit parts within those blocks use reference numbers from their section's decade; the prefix distinguishes component types, so a suffix may be reused across types. On 2026-10-04, the switched supply moved from 50-Series to 20-Series, the GPIO input and gate bias from 20-Series to 30-Series, the BS170 amplifier and drain feed from 30-Series to 40-Series, and the output coupling/LPF interface from 40-Series to 50-Series. The corresponding 20 component references were changed together in the schematic and PCB. Wiring, values, UUIDs, placement, routing, and design settings were preserved.

| Series | Functional block | References |
| --- | --- | --- |
| 10 | Raspberry Pi HAT interface, GPIO indicator, GPIO-selection header, socket purchasing item, and shutdown button | `U11`, `D11`, `R11`, `J11`, `J12`, `SW11` |
| 20 | TPS22918 switched 5 V amplifier supply | `U21`, `C21`, `C22`, `C23`, `R21`, `R22` |
| 30 | GPIO AC coupling, damping, adjustable gate bias, pull-down, and bias bypass | `C31`, `R31`, `RV31`, `R32`, `R33`, `C32` |
| 40 | BS170 amplifier, drain RF choke, supply bypassing, and 0 Ω link | `Q41`, `L41`, `C41`, `C42`, `R41` |
| 50 | Output DC blocking, SMA, and paired LPF female-header interface | `C51`, `J51`, `J52` |

J51 is the hand-soldered edge-launch output connector, and U11 now carries the underside socket 3D model directly; the optional H1 library footprint is retained. J12 permits GPIO4 or GPIO20 to be jumpered onto `GPIO_RF`. GPIO23 is the active-high `AMP_EN` control, and SW11 grounds GPIO26 for software to detect. GPIO drive-strength selection remains coarse and experimental rather than a calibrated power control.

### Placed RF parts awaiting wiring

| Reference | Starting value | Intended function |
| --- | --- | --- |
| C31 | 100 nF | GPIO DC block |
| R31 | 22 Ω | Gate-drive damping |
| RV31 | 5 kΩ | Adjustable gate bias; Bourns TC33X-2-502E, pin 2 wiper |
| R32 | 4.7 kΩ | Bias feed to gate |
| R33 | 100 kΩ | Gate pull-down |
| C32 | 100 nF | Bias-wiper bypass |
| Q41 | BS170 | RF transistor; pins 1/2/3 = drain/gate/source |
| L41 | 25T FT37-43 | Selected hand-wound drain choke; approximately 220 µH nominal at low frequency |
| C41 | 100 nF | Local switched-supply bypass |
| C42 | 1 µF | Local switched-supply decoupling |
| C51 | 100 nF | Drain DC block before `TX_OUT` |

These are starting values for circuit review and prototyping, not qualified full-range RF values. RV31 and L41 now have project-local footprints. All 24 physical schematic parts have assignments that resolve locally; J11 remains a schematic-only purchasing item, and power symbols intentionally have no footprints. The existing 10-, 20-, and LPF-interface parts do not need to be placed again.

### Selected hand-wound choke and trimmer

On 2026-10-01, the user selected **25 turns on a hand-wound FT37-43 core** for L41. Each pass through the core center counts as one turn. The schematic value is `25T FT37-43`. The [Amidon core specification](https://www.amidoncorp.com/ft-37-43/) gives nominal A_L = 350 nH/turn², so 25 turns estimates 218.75 µH at low frequency. RF impedance under drain current and performance at 137 kHz and 144 MHz remain measurement requirements. The winding follows the [QRP Labs Ultimate3S assembly manual](https://www.qrp-labs.com/images/ultimate3s/assembly.pdf); its [LF modifications](https://www.qrp-labs.com/ultimate3/u3mods.html) also document a different R10/N30 core for improved LF output.

L41 uses the local `L_Toroid_FT37-43_Vertical_P5.08mm` footprint, adapted from KiCad's generic 10 × 5 mm vertical toroid pattern. On 2026-10-01, the user selected upright mounting. The hand-formed leads use 5.08 mm pad-center spacing, with 2.4 mm pads and 1.2 mm drills; pad 1 connects to `SW_5V` and pad 2 to `PA_DRAIN`. The fabrication outline depicts the bare core's 9.525 × 3.175 mm board projection; `Dwgs.User` marks an 11 × 5 mm maximum wound-body projection. The courtyard reserves 11.5 × 7.98 mm including the lead pads. Reserve up to 11 mm wound-body height plus the mounting gap. Start with approximately 0.32 mm (AWG 28) enamelled wire, form the leads to the footprint pitch, and strip/tin them before hand soldering. Wound fit, stability, height clearance, and RF behavior require physical verification.

RV31 retains 5 kΩ and selects Bourns `TC33X-2-502E`, `LCSC_PART` C719177, with the local `Potentiometer_Bourns_TC33X_Vertical` footprint. Pin/pad 2 is the wiper; pins 1/3 are the CCW/CW resistance ends. L41 now has a project-local illustrative 25-turn upright VRML model; RV31 now has a project-local illustrative 3D model; see [library sources and model gaps](LIBRARY-SOURCES.md#selected-choke-and-trimmer-footprints).

## Mechanical interface

Coordinates below use the upper-left corner of the 65 × 30 mm board envelope as `(0, 0)`.

| Item | Geometry |
| --- | --- |
| Board envelope | 65 × 30 mm; 1.6 mm thickness; two copper layers |
| Outer corners | 3 mm radius |
| Mounting holes | Four 2.75 mm non-plated holes at `(3.5, 3.5)`, `(61.5, 3.5)`, `(3.5, 26.5)`, and `(61.5, 26.5)` mm |
| Mounting-hole spacing | 58 × 23 mm centers |
| Mounting-hole land | 6.2 mm clear diameter, open solder mask and electrically isolated |
| GPIO interface | Full 2×20 connector, 2.54 mm pitch; pin 1 at `(8.37, 7.31)` mm and pin 2 at `(8.37, 4.77)` mm |
| GPIO extent | Pin columns run from X = 8.37 mm through X = 56.63 mm |
| PoE clearance | Locked 5 × 5 mm underside component-placement keepout at X = 59–64 mm, Y = 7.14–12.14 mm |

U11 combines the 40 GPIO pads and four mechanical holes in one locked footprint. GPIO row orientation follows Raspberry Pi HAT numbering: pin 1 is in the board-interior row and pin 2 is in the board-edge row. The 65 × 30 mm through-hole-header outline is also locked. The connector has an underside courtyard, and the mounting pads enforce the specified copper clearance and solder-mask opening.

The official uHAT drawing allows a 65 × 30.5 mm envelope for an SMT-style through-hole connector arrangement. This project uses a normal through-hole socket and therefore uses the 65 × 30 mm outline.

## Identification and compliance status

This project follows the Raspberry Pi Zero/uHAT mechanical geometry but intentionally omits the identification EEPROM. ID_SD and ID_SC remain unused and must not be repurposed by this design. Because the identification subsystem is omitted, this project does not claim HAT+ compliance.

- Verify STANDBY compatibility: 5 V may be present while 3.3 V is unpowered, and rail sequencing cannot be assumed.
- Select a full 2×20 socket and spacers that provide adequate board-to-board clearance; verify connector, spacer, and component height on every supported Raspberry Pi model.
- Do not back-power the Raspberry Pi unless the design implements the HAT+ power requirements and safe power-path behavior.
- Verify GPIO boot states, contention protection, markings, documentation, and every model-specific mechanical clearance used by the finished design.

## Purchasing BOM

### L41 hand assembly

L41 stays **included on the board and in the netlist**, while its schematic instance and local footprint exclude it from automated BOM and position output. Purchase an FT37-43 core and enamelled wire separately, wind 25 turns, and hand solder it. These exclusions keep the hand-wound assembly out of the JLCPCB component list without removing its electrical pins. RV31 records Bourns TC33X-2-502E and C719177; stock and assembled pricing require checking before ordering.

### J52 LPF sockets and assembly exports

`J52` represents two physical 1×4 LPF socket headers in one grouped symbol and footprint. Keep **Exclude from board unchecked**, **Exclude from BOM checked**, and **Exclude from position files checked**. Its eight pins must remain in the PCB netlist. Both the schematic instance and existing PCB footprint exclude the grouped item from automated BOM and placement output, so it does not become a single assembly item in the JLCPCB BOM. Purchase and fit the two socket headers separately; they are omitted from the exported purchasing BOM as well.

### Retained interface purchasing notes

U11 represents the electrical and mechanical interface and is excluded from the purchasing BOM and placement output. J11 is a pinless, schematic-only purchasing symbol for one female 2×20, 2.54 mm socket header; it is excluded from the PCB so schematic-parity DRC does not require a footprint.

The schematic's **Amplifier purchasing BOM** preset exports the parts included in the automated purchasing BOM. The current command-line preset export omits the `LCSC_PART` column; explicitly include that field when preparing a supplier-ordering CSV. The explicit-field export was checked to include RV31's C719177 and omit L41/J52. `LCSC_PART` is the canonical supplier-ordering property; the legacy `LCSC` field is not used. U11 remains excluded as a non-purchasing interface representation. J11 appears as one row with deliberately blank manufacturer, MPN, and `LCSC_PART` fields because mating height and supported Raspberry Pi models must be chosen for the finished design. Enter the selected socket part before fabrication. J51 is a required hand-soldered SMA connector but is intentionally excluded from BOM and placement output. J12 is also excluded from BOM and placement output by design, while remaining placed for routing and 3D visualization.

The schematic BOM now includes the placed BS170-stage parts and the selected RV31 trimmer. L41 is a manually wound part and is excluded from the automated BOM. Footprints are assigned, but remaining sourcing fields must be completed before ordering. The copied PCB BOM still describes the rejected baseline and must not be used for BS170 assembly.

## Local libraries and files

Both library tables use the `wsprrypi-zero-gpio-bs170` nickname and `${KIPRJMOD}` paths. All required project libraries are inside this directory.

### New symbols for the BS170 circuit

The following project-local symbols are placed in the schematic:

| Reference | Local symbol | Footprint / value |
| --- | --- | --- |
| Q41 | `wsprrypi-zero-gpio-bs170:BS170` | Local `TO-92_Inline`, with local STEP model; pins 1/2/3 are drain/gate/source |
| RV31 | `wsprrypi-zero-gpio-bs170:R_Potentiometer_US` | 5 kΩ Bourns TC33X-2-502E; local `Potentiometer_Bourns_TC33X_Vertical`; pin 2 is the wiper |
| L41 | `wsprrypi-zero-gpio-bs170:L` | 25 turns on FT37-43; local `L_Toroid_FT37-43_Vertical_P5.08mm`; upright, manually wound and fitted |

These are independent copies from the installed KiCad 10.0.6 libraries; see [sources and pin mapping](LIBRARY-SOURCES.md#bs170-redesign-additions). The existing resistor and capacitor symbols provide the other eight new parts.

### Copied baseline assets

U11 directly carries the female 2×20 socket model on the underside. J52 carries two 1×4 socket models on top. Both remain excluded from BOM and position output, with electrical pads intact. The optional H1 model-only footprint remains in the library for compatibility; do not place it over U11, which would duplicate the socket. J11 remains the purchasing item.

The local library includes the grouped 2×4 connector `LPF_HeaderPair_Female_2x1x04_P2.54mm_S33.02mm`. Its two 1×4 socket centers are exactly 33.020 mm apart, matching paired J1 on the `WsprryPi LPF` board. J52 is one eight-pin symbol with a single rectangular body, styled like the matching LPF-board symbol. Pins 1–4 are the amplifier-side row; pins 5–8 are the filtered-output row. Pins 1, 4, 5, and 8 are `GND`; pins 2 and 3 are `RF_IN` (the amplifier’s `TX_OUT` net); pins 6 and 7 are `RF_OUT` (the `FINAL_OUT` net). Its inter-header rule area prohibits tracks, pads, and footprints on `F.Cu`, while allowing stitching vias and copper pours. The bottom-layer ground pour remains allowed beneath the LPF. This project-local footprint was adjusted from the Zero HAT template's older 32.020 mm, two-copper-layer definition.

J12 uses the local `Conn_01x03` symbol and `PinHeader_1x03_P2.54mm_Vertical` male through-hole footprint. It is placed and routed with pin 1 on GPIO4, pin 2 on `GPIO_RF`, and pin 3 on GPIO20. The symbol and footprint are excluded from BOM and position output, and the footprint references a project-local STEP model for 3D visualization.

J51 uses the `SMA_Adafruit_1865` symbol and `SMA_Adafruit_1865_EdgeMount` footprint copied from `WsprryPi-GPIO-Univ`. This is the Adafruit 1865 standard-polarity female edge-launch SMA for a 1.6 mm board: pin 1 is signal, pin 2 is ground, the origin is the board seating edge on the signal centerline, and copper extends 0.500–4.064 mm into the board. It is placed and routed, hand-soldered, excluded from BOM and position output, and has no attached 3D model.

The same project-local library retains the following baseline and interface assets:

- `LTC6432-15`, whose local master and copied PCB U31 metadata select `LTC6432AIUF-15#PBF` and `LCSC_PART` C689344, with the Analog Devices UF24 4 × 4 mm QFN exposed-pad footprint and thermal vias; it is removed from the schematic;
- unplaced `YA9308-AEC` with a custom footprint built from Coilcraft's recommended land pattern;
- `WBC2-1TLC`, retained on T21 and T41 in the copied PCB but removed from the schematic, with `LCSC_PART` C19191658 and a separate custom footprint built from Coilcraft's WBC recommended land pattern;
- `TPS22918` with the KiCad SOT-23-6 footprint;
- local `R_0603`, `C_0603`, and `C_0805` symbols with local 0603 and 0805 KiCad footprints, plus the retained `C_1206_3216Metric` baseline footprint; the new RF resistors and C31/C32/C41/C51 use 0603, while C42 uses 0805; `R_0603` uses the compact US zigzag graphic;
- local `R_US` and `LED` symbols supporting the placed R11 and D11 indicator circuit, with local 0603 footprints and an LED STEP model;
- a project-local `GND` power symbol used by every placed ground-symbol instance;
- the placed `SKRPANE010` momentary tactile switch SW11 for `LCSC_PART` C470426, with an Alps SKRP manufacturer-land-pattern footprint and local STEP model;
- the placed, BOM- and position-output-excluded J12 `Conn_01x03` symbol with a 2.54 mm male through-hole header footprint and local STEP model; and
- the placed, hand-soldered J51 `SMA_Adafruit_1865` symbol with its BOM- and position-output-excluded `SMA_Adafruit_1865_EdgeMount` footprint.

Manufacturer, MPN, `LCSC_PART`, data-sheet, description, and local-footprint fields are embedded in the device symbols where applicable. See [local library sources and licensing](LIBRARY-SOURCES.md) before modifying or redistributing the imported assets.

- [Project settings](WsprryPi%20Zero%20GPIO%20BS170.kicad_pro): copied rules, defaults, and BOM preset.
- [Schematic](WsprryPi%20Zero%20GPIO%20BS170.kicad_sch): partially wired BS170-stage parts with assigned footprints, retained power-control circuit, GPIO interface, and LPF interface.
- [PCB](WsprryPi%20Zero%20GPIO%20BS170.kicad_pcb): copied placed and routed two-layer baseline with the locked Zero-size outline, interface footprint, mounting-hole lands, PoE keepout, and LPF keepout.
- [Fabrication notes](FABRICATION-NOTES.md): process notes for the copied U31 baseline only; reassess after the BS170 layout replaces it.
- [Symbol library](wsprrypi-zero-gpio-bs170.kicad_sym): GPIO interface, socket purchasing symbol, and paired LPF female-header connector symbol.
- [Interface footprint](wsprrypi-zero-gpio-bs170.pretty/Raspberry_Pi_Zero_HAT_Interface.kicad_mod).
- [Selectable 2×20 socket footprint](wsprrypi-zero-gpio-bs170.pretty/Raspberry_Pi_HAT_2x20_Socket_3D.kicad_mod): board-only 3D representation used by H1.
- [Paired LPF female-header footprint](wsprrypi-zero-gpio-bs170.pretty/LPF_HeaderPair_Female_2x1x04_P2.54mm_S33.02mm.kicad_mod): exact current LPF-board spacing plus an F.Cu inter-header copper and placement keepout.
- [Local library sources and licensing](LIBRARY-SOURCES.md): imported-footprint provenance, custom-part data sources, license, and validation limits.
- [Local STEP models](wsprrypi-zero-gpio-bs170.3dshapes/README.md) for the BS170 TO-92 package, 2×20 socket, 1×3 male header, 0603 LED, and SKRPANE010 tactile switch.
- [License](LICENSE.md): repository-owned project terms.

The local-library filenames and nickname are unique to this project. Keep generated exports, backups, caches, and local preference files out of this directory.

## Validation and limits

For the 2026-10-04 block renumbering, KiCad **10.0.6** was run outside the sandbox on the saved working-tree sources before and after the change. ERC reported **0 errors and 0 warnings** in both runs. Command-line DRC with in-memory zone refill reported **0 rule violations, 0 unconnected items, and 34 schematic-parity warnings** in both runs; the findings match after reference substitution. A separate native PCB-editor check, with the matching schematic loaded and zone refill/parity enabled, reported **0 rule violations, 0 unconnected items, and 0 parity findings**. Both reports are retained; the CLI/native parity discrepancy remains explicit. Before/after netlists have identical pin connections after reference substitution. Schematic and PCB source comparisons confirm that all other drawing objects and UUIDs are unchanged, and the affected schematic and board were visually inspected.

The historical records below retain their original component references and describe earlier source states.

### Historical validation records

The saved schematic has unwired 20-series parts, and the PCB remains the cost-rejected implementation. Both are not ready for order. Production decisions and physical/RF qualification remain open. J41, J12, and SW11 are placed; J41 and J12 retain their intentional BOM and placement-output exclusions. U11 and every other previously placed schematic symbol retain their UUIDs.

At project creation, KiCad 10.0.6 schematic ERC reported 0 violations, and standard command-line PCB DRC reported 0 violations and 0 unconnected items. These baseline results predate removal of the amplifier stages from the schematic. A separate command-line DRC attempt with schematic parity enabled aborted, so schematic-to-PCB parity was not verified by that run. These checks do not establish physical assembly, connector fit, Raspberry Pi model compatibility, electrical performance, thermal behavior, or RF performance.

After the schematic cleanup and J42 exclusion correction, before adding the BS170 parts, KiCad 10.0.6 ERC reported 0 errors and 1 warning: `GPIO_RF` connected only to J12. The exported netlist included all eight J42 pins: 1/4/5/8 on `GND`, 2/3 on `FINAL_OUT`, and 6/7 on `TX_OUT`. The purchasing BOM and PCB placement exports omitted J42; comparison with the preceding BOM showed only the J42 row removed. The J42 correction changed only its schematic BOM/board flags; the saved PCB was byte-for-byte unchanged.

After the BS170 library additions, KiCad 10.0.6 successfully exported all 20 project-local symbols and all 17 project-local footprints. The new BS170, trimmer, inductor, and TO-92 footprint were visually inspected from those exports. The pre-placement schematic had 0 ERC errors and the one expected `GPIO_RF` warning.

On 2026-10-01, eleven RF parts were placed without wiring, net labels, or no-connect flags. The placement-stage KiCad 10.0.6 ERC reported **25 errors and 1 warning**: 24 unconnected new pins, the undriven Q31 gate, and the existing isolated `GPIO_RF` label. The saved schematic was exported to PDF and visually inspected for placement and readable labels. All existing symbols, wires, junctions, labels, and no-connect markers were preserved; the PCB, project settings, and local library files were unchanged by placement. No PCB DRC was rerun because the PCB was not edited. The current schematic and PCB do not represent the same RF circuit.

After the user wired the 30- and 40-series sections, the footprint-assignment update on 2026-10-01 imported two local footprints and assigned L31/RV21. KiCad 10.0.6 ERC before and after the update reported the same **14 errors and 2 warnings**: 13 unconnected 20-series pins, the undriven Q31 gate, and isolated `GPIO_RF`/`GATE` labels. All 24 physical schematic parts resolve locally. The new footprints and updated schematic were exported and visually inspected; the trimmer lands and numbering were compared with the Bourns drawing. Exported netlist connectivity and all symbol/pin UUIDs, wires, junctions, labels, and no-connect markers were unchanged. L31 remains in the netlist while excluded from automated BOM/position output. The PCB, project settings, library tables, and existing footprint assets were byte-for-byte unchanged. No PCB DRC was rerun because the PCB was not edited. The schematic and PCB still represent different RF circuits.

For the user-selected upright L31 revision on 2026-10-01, KiCad 10.0.6 ERC reported **0 errors and 0 warnings** before and after the footprint assignment. The new vertical footprint and saved schematic were exported and visually inspected. All schematic connections, drawing objects, and UUIDs were preserved; only the L31/master footprint and description properties changed. The exported netlists have identical connectivity, and the new pads preserve 1 = `SW_5V`, 2 = `PA_DRAIN`. The user's currently saved PCB, project settings, and existing library assets were unchanged by this revision. L31 on that PCB still references the horizontal footprint; update it from the schematic to adopt upright mounting. No PCB DRC was rerun because this revision did not edit the board. Wound dimensions, mounting stability, and height clearance remain physical checks.

Existing ignored ERC checks were retained: global labels appearing only once, four-way junctions, SPICE model issues, and assigned footprints not matching footprint filters. No new exclusions or severity changes were added during placement or the upright-footprint revision.

These exports, ERC, historical DRC, and visual inspection do not establish land-pattern suitability for a particular assembly process, solderability, thermal performance, RF performance, or production readiness.

## Sources and license

The board geometry follows Raspberry Pi's official uHAT mechanical drawing and Raspberry Pi Zero 2 W mechanical drawing. Electrical and compliance notes follow the current HAT+ specification.

The 2×20 socket STEP model derives from the KiCad standard 3D model library and retains the KiCad library license described in the adjacent model notice. The repository MIT license does not replace those third-party terms.

- [Raspberry Pi uHAT mechanical drawing](https://github.com/raspberrypi/hats/blob/master/uhat-board-mechanical.pdf)
- [Raspberry Pi Zero 2 W mechanical drawing](https://pip.raspberrypi.com/documents/RP-008358-DS)
- [Raspberry Pi HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf)
- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)

See [LICENSE.md](LICENSE.md).

## RV31 and J51 3D visualization

`TC33X_Preview.wrl` and `SMA_Adafruit_1865_Preview.wrl` are original repository-MIT-licensed models attached to both the local footprint masters and the saved PCB through `${KIPRJMOD}`. The trimmer follows the footprint fabrication outline (3.8 × 3.0 mm), with an illustrative 1.6 mm height and adjustment disk. The SMA follows its existing fabrication outline: 6.5 mm flange, 6.1 mm barrel diameter, 9.5 mm forward reach, and 3.9 mm rear fingers straddling the 1.6 mm board. Heights, threads, internal details, and tolerances are simplified assumptions; these are visualizations, not supplier CAD or clearance qualification. The SMA points outward along footprint +Y; terminal fingers align with its pads. Placement, copper, connectivity, and settings are preserved.

The original visualization meshes can be regenerated with `python3 wsprrypi-zero-gpio-bs170.3dshapes/generate_rv31_j51.py` from the project directory. KiCad 10.0.6 DRC before and after model attachment reported 0 violations and 0 unconnected items without refilling or saving zones; both models were visually inspected in a 3D render.

### J52 header spacing

J52 uses 33.02 mm (1.300 inch) between the two socket-row centerlines, with 2.54 mm pin pitch. The left row remains at X = 123.976736 mm and the right row is at X = 156.996736 mm. The right row and adjacent ground stitching were adjusted toward J51; eight conflicting redundant stitching vias were removed and the ground-pour boundary was extended. Pin assignments are unchanged.

At the header-spacing checkpoint, KiCad 10.0.6 ERC reported zero violations. DRC with in-memory zone refill reported two copper-sliver warnings and two then-unconnected output items (J52 pads 6/7 and J51). These are historical results; the current renumbering checks are recorded above. Saved zone fills must be refreshed in KiCad before manufacturing. This spacing change does not qualify mechanical mating or RF performance.
