# WsprryPi Zero GPIO

A KiCad 10 project initialized from the `RPi Zero HAT` template for WsprryPi GPIO development. It provides the Raspberry Pi Zero-size uHAT geometry, a complete 40-pin GPIO interface, a selectable underside socket model, a socket purchasing item, and independent local libraries.

The schematic and routed two-layer PCB contain the first implementation pass of the 5 V RF amplifier, load-switch circuit, GPIO selection header, LPF interface, and edge-launch SMA output. The design intentionally omits an identification EEPROM and leaves ID_SD and ID_SC unused. Placement and routing are saved, but the board has not been fabricated or physically qualified.

The selected 5 V LTC6432-15 amplifier architecture, expected RF level, first-pass BOM, and remaining implementation decisions are recorded in [AMPLIFIER-DESIGN.md](AMPLIFIER-DESIGN.md). It is a new design and does not inherit the earlier 1 W amplifier requirements.

> **Order status: Not ready for order.** The selected architecture requires two Coilcraft `YA9308-AEC` transformers. They are not available through the normal JLCPCB/LCSC public parts inventory, and no normally stocked substitute has been qualified for the required impedance ratio, center-tapped output bias, current capacity, frequency span, and available board area. Do not submit this design for fabrication or assembly until the exact transformers have an accepted procurement path, or the circuit is redesigned around a separately qualified replacement.

## Develop this HAT project

1. Open `WsprryPi Zero GPIO.kicad_pro` in KiCad 10 and review the saved schematic and routed board together.
2. Resolve the `YA9308-AEC` sourcing blocker and the remaining provisional component and compliance decisions recorded in `AMPLIFIER-DESIGN.md`.
3. After any design change, update the PCB from the schematic as needed, refill copper zones, and rerun ERC and DRC before reviewing the resulting diff.

This project has independent copies of the design files, symbol library, footprint library, and STEP model. Changes here do not update `RPi Zero HAT`, and later template changes do not update this project.

## Schematic block numbering

The schematic is arranged as five boxed functional sections. Circuit parts within those blocks use reference numbers from their section's decade; the prefix distinguishes component types, so a suffix may be reused across types. A few interface and board-only parts retain special references as documented below. Connections within each section are drawn conventionally with wires and explicit branch junctions; net labels are reserved primarily for interfaces between sections and ground references.

| Series | Functional block | References |
| --- | --- | --- |
| 10 | Raspberry Pi HAT interface, GPIO indicator, GPIO-selection header, and socket purchasing item | `U10`, `D11`, `R11`, `J11`, `J12` |
| 20 | GPIO damping, DC blocking, boot-state pull-down, and input transformer | `R20`, `C21`, `R21`, `T22` |
| 30 | LTC6432-15 amplifier, coupling, feedback, noise filtering, and bypassing | `C30`–`C37`, `U32` |
| 40 | Output transformer and grouped J81/J82 LPF interface | `T40`, `J41` |
| 50 | TPS22918 switched 5 V amplifier supply | `U50`, `C51`, `R52`, `C53`, `R54`, `C55` |

J1 is the hand-soldered edge-launch output connector, and H1 is the board-only 3D socket representation; those references sit outside the functional-decade annotation convention. SW11 is the software shutdown-request button in the 10-series. J12 permits GPIO4 or GPIO20 to be jumpered onto `GPIO_RF`. GPIO23 is the active-high `AMP_EN` control, and SW11 grounds GPIO26 for software to detect. GPIO drive-strength selection remains coarse and experimental rather than a calibrated power control.

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

U10 combines the 40 GPIO pads and four mechanical holes in one locked footprint. GPIO row orientation follows Raspberry Pi HAT numbering: pin 1 is in the board-interior row and pin 2 is in the board-edge row. The 65 × 30 mm through-hole-header outline is also locked. The connector has an underside courtyard, and the mounting pads enforce the specified copper clearance and solder-mask opening.

The official uHAT drawing allows a 65 × 30.5 mm envelope for an SMT-style through-hole connector arrangement. This project uses a normal through-hole socket and therefore uses the 65 × 30 mm outline.

## Identification and compliance status

This project follows the Raspberry Pi Zero/uHAT mechanical geometry but intentionally omits the identification EEPROM. ID_SD and ID_SC remain unused and must not be repurposed by this design. Because the identification subsystem is omitted, this project does not claim HAT+ compliance.

- Verify STANDBY compatibility: 5 V may be present while 3.3 V is unpowered, and rail sequencing cannot be assumed.
- Select a full 2×20 socket and spacers that provide adequate board-to-board clearance; verify connector, spacer, and component height on every supported Raspberry Pi model.
- Do not back-power the Raspberry Pi unless the design implements the HAT+ power requirements and safe power-path behavior.
- Verify GPIO boot states, contention protection, markings, documentation, and every model-specific mechanical clearance used by the finished design.

## Purchasing BOM

U10 represents the electrical and mechanical interface and is excluded from the purchasing BOM and placement output. J11 is a pinless, schematic-only purchasing symbol for one female 2×20, 2.54 mm socket header; it is excluded from the PCB so schematic-parity DRC does not require a footprint.

The schematic's **Amplifier purchasing BOM** preset exports all parts included in the automated purchasing BOM, including the canonical `LCSC_PART` supplier-ordering field; the legacy `LCSC` field is not used. U10 remains excluded as a non-purchasing interface representation. J11 appears as one row with deliberately blank manufacturer, MPN, and `LCSC_PART` fields because mating height and supported Raspberry Pi models must be chosen for the finished design. Enter the selected socket part before fabrication. J1 is a required hand-soldered SMA connector but is intentionally excluded from BOM and placement output. J12 is also excluded from BOM and placement output by design, while remaining placed for routing and 3D visualization.

The exported BOM is for design review and costing only. It is not an order-ready BOM while the two required `YA9308-AEC` transformers lack an accepted assembly-sourcing path.

## Local libraries and files

Both library tables use the `wsprrypi-zero-gpio` nickname and `${KIPRJMOD}` paths. All required project libraries are inside this directory.

H1 is a separate, selectable footprint that shows the female 2×20 HAT socket on the underside of the board. Delete H1 when the 3D socket is not wanted, or place `wsprrypi-zero-gpio:Raspberry_Pi_HAT_2x20_Socket_3D` to add it back. H1 has no electrical pads and is exempt from the courtyard requirement because it overlays the same physical socket already represented by U10's authoritative underside courtyard. U10 remains the authoritative electrical and mechanical interface, and J11 remains the purchasing item.

The local library includes the grouped 2×4 connector `Dual_PinSocket_1x04_P2.54mm_J81_J82`. Its two 1×4 socket centers are exactly 31.880 mm apart, matching J1/J2 on the current `Wsprry-Pi-LPF` board. Symbol/footprint pins 1–4 correspond to J81 pins 1–4; pins 5–8 correspond to J82 pins 1–4. Its 29.22 × 11.20 mm inter-header rule area prohibits tracks, vias, pads, copper pours, and footprints on `F.Cu` while intentionally allowing the bottom-layer ground pour beneath the LPF. This project-local footprint was adjusted from the Zero HAT template's older 32.020 mm, two-copper-layer definition.

J12 uses the local `Conn_01x03` symbol and `PinHeader_1x03_P2.54mm_Vertical` male through-hole footprint. It is placed and routed with pin 1 on GPIO4, pin 2 on `GPIO_RF`, and pin 3 on GPIO20. The symbol and footprint are excluded from BOM and position output, and the footprint references a project-local STEP model for 3D visualization.

J1 uses the `SMA_Adafruit_1865` symbol and `SMA_Adafruit_1865_EdgeMount` footprint copied from `WsprryPi-GPIO-Univ`. This is the Adafruit 1865 standard-polarity female edge-launch SMA for a 1.6 mm board: pin 1 is signal, pin 2 is ground, the origin is the board seating edge on the signal centerline, and copper extends 0.500–4.064 mm into the board. It is placed and routed, hand-soldered, excluded from BOM and position output, and has no attached 3D model.

The same project-local library now contains symbols and assigned footprints for the proposed BOM:

- `LTC6432-15`, whose local master and placed U32 metadata select `LTC6432AIUF-15#PBF` and `LCSC_PART` C689344, with the Analog Devices UF24 4 × 4 mm QFN exposed-pad footprint and thermal vias;
- `YA9308-AEC` with a custom footprint built from Coilcraft's recommended land pattern;
- `TPS22918` with the KiCad SOT-23-6 footprint;
- local `R_0603`, `C_0603`, and `C_0805` symbols with local 0603 and 0805 KiCad footprints, plus the project-local `C_1206_3216Metric` footprint assigned in the schematic to C21, C31, C32, C37, and C38; the shared `C_0805` symbol's filter permits both local capacitor footprints while retaining 0805 as its default; `R_0603` uses the compact US zigzag graphic; and
- local `R_US` and `LED` symbols supporting the placed R11 and D11 indicator circuit, with local 0603 footprints and an LED STEP model;
- a project-local `GND` power symbol used by every placed ground-symbol instance;
- the placed `SKRPANE010` momentary tactile switch SW11 for `LCSC_PART` C470426, with an Alps SKRP manufacturer-land-pattern footprint and local STEP model;
- the placed, BOM- and position-output-excluded J12 `Conn_01x03` symbol with a 2.54 mm male through-hole header footprint and local STEP model; and
- the placed, hand-soldered J1 `SMA_Adafruit_1865` symbol with its BOM- and position-output-excluded `SMA_Adafruit_1865_EdgeMount` footprint.

Manufacturer, MPN, `LCSC_PART`, data-sheet, description, and local-footprint fields are embedded in the device symbols where applicable. See [local library sources and licensing](LIBRARY-SOURCES.md) before modifying or redistributing the imported assets.

- [Project settings](WsprryPi%20Zero%20GPIO.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](WsprryPi%20Zero%20GPIO.kicad_sch): proposed five-block amplifier, power-control, and LPF-interface circuit.
- [PCB](WsprryPi%20Zero%20GPIO.kicad_pcb): placed and routed two-layer board with the locked Zero-size outline, interface footprint, mounting-hole lands, PoE keepout, and LPF keepout.
- [Symbol library](wsprrypi-zero-gpio.kicad_sym): GPIO interface, socket purchasing symbol, and grouped J81/J82 connector symbol.
- [Interface footprint](wsprrypi-zero-gpio.pretty/Raspberry_Pi_Zero_HAT_Interface.kicad_mod).
- [Selectable 2×20 socket footprint](wsprrypi-zero-gpio.pretty/Raspberry_Pi_HAT_2x20_Socket_3D.kicad_mod): board-only 3D representation used by H1.
- [Grouped 2×4 J81/J82 footprint](wsprrypi-zero-gpio.pretty/Dual_PinSocket_1x04_P2.54mm_J81_J82.kicad_mod): exact current LPF-board spacing plus an F.Cu inter-header copper and placement keepout.
- [Local library sources and licensing](LIBRARY-SOURCES.md): imported-footprint provenance, custom-part data sources, license, and validation limits.
- [Local STEP models](wsprrypi-zero-gpio.3dshapes/README.md) for the 2×20 socket, 1×3 male header, 0603 LED, and SKRPANE010 tactile switch.
- [License](LICENSE.md): repository-owned project terms.

The local-library filenames and nickname are unique to this project. Keep generated exports, backups, caches, and local preference files out of this directory.

## Validation and limits

The current schematic and board remain active work and are not ready for order because of the unresolved `YA9308-AEC` sourcing requirement and the remaining production-readiness decisions in `AMPLIFIER-DESIGN.md`. J1, J12, and SW11 are placed; J1 and J12 retain their intentional BOM and placement-output exclusions. The HAT interface footprint keeps its original schematic UUID, so U10 remains associated with the PCB interface when the board is updated from the schematic.

KiCad 10.0.6 schematic ERC reports 0 errors and 0 warnings. KiCad 10.0.6 command-line PCB DRC reports 0 violations, 0 unconnected pads, and 0 footprint errors. These checks do not establish physical assembly, connector fit, Raspberry Pi model compatibility, electrical performance, thermal behavior, or RF performance.

KiCad 10.0.6 successfully exported all 15 project-local symbols and all 15 project-local footprints. The resistor, capacitor, LED, ground, SMA, SKRPANE010, and 1×3 header assets, four device symbols, and two custom RF footprints were visually inspected from those exports. Library inspection, ERC, DRC, routing, and 3D rendering do not establish land-pattern suitability for a particular assembly process, solderability, thermal performance, RF performance, or production readiness.

## Sources and license

The board geometry follows Raspberry Pi's official uHAT mechanical drawing and Raspberry Pi Zero 2 W mechanical drawing. Electrical and compliance notes follow the current HAT+ specification.

The 2×20 socket STEP model derives from the KiCad standard 3D model library and retains the KiCad library license described in the adjacent model notice. The repository MIT license does not replace those third-party terms.

- [Raspberry Pi uHAT mechanical drawing](https://github.com/raspberrypi/hats/blob/master/uhat-board-mechanical.pdf)
- [Raspberry Pi Zero 2 W mechanical drawing](https://pip.raspberrypi.com/documents/RP-008358-DS)
- [Raspberry Pi HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf)
- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)

See [LICENSE.md](LICENSE.md).
