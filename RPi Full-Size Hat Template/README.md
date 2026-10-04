# RPi Full-Size Hat

A KiCad 10 project template for full-size Raspberry Pi HAT designs. It provides the official classic full-size HAT board geometry, the complete 40-pin GPIO interface, recommended display/camera flex openings, mounting-hole clear lands, local libraries, and a socket-header purchasing item. The schematic is intentionally unwired, and the board has no tracks, vias, or copper pours.

## Create a new HAT project

1. In KiCad's project manager, open **Preferences → Configure Paths…**.
2. Set `KICAD_USER_TEMPLATE_DIR` to the parent directory containing this template folder: the `Wsprry Pi PCB Designs` repository root. Alternatively, copy this entire folder into your existing user-template directory.
3. Choose **File → New Project…**, select **RPi Full-Size Hat**, and give the project its own name and directory. Reopen the project manager if its template list has not refreshed.
4. Add the required identification EEPROM and application circuit. Connect only the GPIOs the design uses; mark genuinely unused pins with no-connect flags.
5. Run **Tools → Update PCB from Schematic…**, place the added components, route the board, add and fill copper zones, and run ERC and DRC.

Each new project has independent copies of the design files and libraries. Template edits do not update existing HAT projects.

## Mechanical interface

| Item | Geometry |
| --- | --- |
| Board envelope | 65 × 56.5 mm; 1.6 mm thickness; two copper layers |
| Outer corners | 3 mm radius |
| Mounting holes | Four 2.75 mm non-plated holes on 58 × 49 mm centers |
| Mounting-hole land | 6.2 mm clear diameter, open solder mask and electrically isolated |
| GPIO interface | Full 2×20 connector, 2.54 mm pitch |
| Display opening | 5 mm-deep × 17 mm-high edge cutout with 1 mm radii |
| Camera opening | 2 mm-wide × 17 mm-long internal slot |

U1 combines the 40 GPIO pads and four mechanical holes in one locked footprint. GPIO row orientation follows Raspberry Pi HAT numbering: pin 1 is in the board-interior row and pin 2 is in the board-edge row. The board-level perimeter and flex openings are also locked. Unlock those objects only when deliberately changing the mechanical interface.

## HAT compliance responsibilities

This template follows the classic Raspberry Pi full-size HAT mechanical drawing, but a derived board is not automatically a compliant HAT. Before calling a finished design a Raspberry Pi HAT, complete and verify all applicable requirements:

- Connect ID_SD and ID_SC only to the required identification EEPROM circuit. If they are not used for an EEPROM, leave them unconnected.
- Add a compatible 3.3 V, 16-bit-addressed ID EEPROM, the required 3.9 kΩ pull-ups, write-protect provisions, a valid programmed identity, GPIO map, and device-tree information.
- Select a full 2×20 socket and spacers that provide at least the required board separation; verify connector, spacer, and component height on the exact Raspberry Pi model.
- Do not back-power the Raspberry Pi unless the design implements the required current capacity and safe power-path behavior.
- Protect against GPIO contention and boot-state hazards required by the HAT guidance.
- Check PoE-header, Active Cooler, camera/display, and other model-specific mechanical clearances against the exact Raspberry Pi model.

The original HAT specification is deprecated for new products in favor of HAT+, but the classic 65 × 56.5 mm outline remains a useful full-size mechanical starting point. A new product should also satisfy the current HAT+ electrical, EEPROM, marking, spacing, and documentation requirements that apply to its class.

## Purchasing BOM

U1 represents the electrical and mechanical interface and is excluded from the purchasing BOM and placement output. J1 is a pinless, schematic-only purchasing symbol for one female 2×20, 2.54 mm socket header; it is excluded from the PCB so schematic-parity DRC does not require a footprint.

The schematic's **HAT socket purchasing BOM** preset exports J1 as one row. Manufacturer and MPN fields are deliberately blank because mating height and supported Raspberry Pi models must be chosen for the finished design. Enter the selected part before fabrication.

## Local libraries and files

Both library tables use the `full-size-hat` nickname and `${KIPRJMOD}` paths. All required template libraries are inside this directory. H1 is a separate, selectable footprint that shows the female 2×20 HAT socket on the underside of the board. Delete H1 when the 3D socket is not wanted, or place `full-size-hat:Raspberry_Pi_HAT_2x20_Socket_3D` to add it back. H1 has no electrical pads and is exempt from the courtyard requirement because it overlays the same physical socket already represented by U1's authoritative underside courtyard. U1 remains the authoritative electrical and mechanical interface, and J1 remains the purchasing item.

The local library also includes `Dual_PinSocket_1x04_P2.54mm_J81_J82`, a single eight-pin symbol and footprint derived from J81 and J82 in `Wsprry-Pi-Synth-Univ`. Its two 1×4 socket centers are exactly 32.020 mm apart. Symbol/footprint pins 1–4 correspond to J81 pins 1–4; pins 5–8 correspond to J82 pins 1–4. The footprint origin is the midpoint between the two header centers. Its 29.36 × 11.20 mm rule area spans the complete underside between the two connector bodies and prohibits tracks, vias, pads, copper pours, and footprints on both copper layers. The two connector strips remain outside that rule area so their own through-hole pads do not violate it and their nets can route outward. This grouped 1×4 footprint intentionally has no 3D model.

- [Project settings](RPi%20Full-Size%20Hat.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](RPi%20Full-Size%20Hat.kicad_sch): U1 GPIO interface and J1 procurement symbol.
- [PCB](RPi%20Full-Size%20Hat.kicad_pcb): locked interface footprint, outline, mounting holes, and flex openings.
- [Symbol library](full-size-hat.kicad_sym): GPIO interface, socket purchasing symbol, and grouped J81/J82 connector symbol.
- [Interface footprint](full-size-hat.pretty/Raspberry_Pi_HAT_Interface.kicad_mod).
- [Selectable 2×20 socket footprint](full-size-hat.pretty/Raspberry_Pi_HAT_2x20_Socket_3D.kicad_mod): board-only 3D representation used by H1.
- [Grouped J81/J82 footprint](full-size-hat.pretty/Dual_PinSocket_1x04_P2.54mm_J81_J82.kicad_mod): exact source spacing plus inter-header copper and placement keepout.
- [2×20 socket STEP model](full-size-hat.3dshapes/PinSocket_2x20_P2.54mm_Vertical.step) and [model notice](full-size-hat.3dshapes/README.md).
- [Template description](meta/info.html) and [preview](meta/board.png): template selector assets.
- [License](LICENSE.md): included with new projects.

KiCad renames the three project design files for the chosen project name and omits `meta` from the new project. Library filenames remain unchanged. Keep generated exports, backups, caches, and local preference files out of this folder because other non-hidden files may be copied into new projects.

## Validation and limits

The unwired interface produces 34 expected ERC findings: 31 visible pins are unconnected and the three visible power inputs are undriven. The PCB has zero DRC rule violations and nine expected unrouted items for the shared 3V3, 5V, and GND header pads. The selectable, model-only H1 footprint is explicitly exempt from the missing-courtyard check because its physical socket courtyard remains in U1. Connect required pins, route the shared rails, and mark only genuinely unused pins with no-connect flags when developing a design.

Run ERC and DRC after adding the ID EEPROM, application circuit, routing, and copper. This template has no verified physical assembly, connector fit, HAT identity data, Raspberry Pi model compatibility, electrical performance, or RF performance.

## Sources and license

The geometry follows Raspberry Pi's official full-size HAT mechanical drawing. Electrical and compliance notes follow the official HAT design guidance and current HAT+ specification.

The 2×20 socket STEP model derives from the KiCad standard 3D model library and retains the KiCad library license described in the adjacent model notice. The repository MIT license does not replace those third-party terms.

- [Raspberry Pi HAT repository and design guide](https://github.com/raspberrypi/hats)
- [Full-size HAT mechanical drawing](https://github.com/raspberrypi/hats/blob/master/hat-board-mechanical.pdf)
- [Raspberry Pi HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf)
- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)

See [LICENSE.md](LICENSE.md).
