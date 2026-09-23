# RPi Zero HAT

A KiCad 10 project template for Raspberry Pi Zero-size HAT+ designs. It is electrically and functionally identical to the `RPi Full-Size Hat` template: the schematic exposes the complete 40-pin GPIO interface, the project includes a selectable underside socket model and a socket purchasing item, and the local libraries carry the same reusable symbols and footprints. The mechanical envelope is the official through-hole-connector Raspberry Pi uHAT size.

The schematic is intentionally unwired, and the board has no tracks, vias, or copper pours. A derived design must add its HAT+ identification EEPROM and application circuit.

## Create a new HAT project

1. In KiCad's project manager, open **Preferences → Configure Paths…**.
2. Set `KICAD_USER_TEMPLATE_DIR` to the parent directory containing this template folder: the `Wsprry Pi PCB Designs` repository root. Alternatively, copy this entire folder into an existing user-template directory.
3. Choose **File → New Project…**, select **RPi Zero HAT**, and give the project its own name and directory. Reopen the project manager if its template list has not refreshed.
4. Add the required identification EEPROM and application circuit. Connect only the GPIOs the design uses; mark genuinely unused pins with no-connect flags.
5. Run **Tools → Update PCB from Schematic…**, place the added components, route the board, add and fill copper zones, and run ERC and DRC.

Each new project has independent copies of the design files and libraries. Template edits do not update existing HAT projects.

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

U1 combines the 40 GPIO pads and four mechanical holes in one locked footprint. GPIO row orientation follows Raspberry Pi HAT numbering: pin 1 is in the board-interior row and pin 2 is in the board-edge row. The 65 × 30 mm through-hole-header outline is also locked. The connector has an underside courtyard, and the mounting pads enforce the specified copper clearance and solder-mask opening.

The official uHAT drawing allows a 65 × 30.5 mm envelope for an SMT-style through-hole connector arrangement. This template uses a normal through-hole socket and therefore uses the 65 × 30 mm outline.

## HAT+ compliance responsibilities

This template follows the Raspberry Pi Zero/uHAT mechanical geometry and provides a HAT+ capable starting point, but a derived board is not automatically a compliant HAT+. Before using the HAT+ name or mark for a finished product:

- Add a suitable 3.3 V, 16-bit-addressed ID EEPROM on ID_SD and ID_SC with the required 3.9 kΩ pull-ups, whole-array write protection, a valid programmed identity, and a Device Tree overlay name.
- Keep ID_SD and ID_SC exclusive to the identification EEPROM circuit.
- Verify STANDBY compatibility: 5 V may be present while 3.3 V is unpowered, and rail sequencing cannot be assumed.
- Select a full 2×20 socket and spacers that provide adequate board-to-board clearance; verify connector, spacer, and component height on every supported Raspberry Pi model.
- Do not back-power the Raspberry Pi unless the design implements the HAT+ power requirements and safe power-path behavior.
- Verify GPIO boot states, contention protection, markings, documentation, and every model-specific mechanical clearance used by the finished design.

## Purchasing BOM

U1 represents the electrical and mechanical interface and is excluded from the purchasing BOM and placement output. J1 is a pinless, schematic-only purchasing symbol for one female 2×20, 2.54 mm socket header.

The schematic's **HAT socket purchasing BOM** preset exports J1 as one row. Manufacturer and MPN fields are deliberately blank because mating height and supported Raspberry Pi models must be chosen for the finished design. Enter the selected part before fabrication.

## Local libraries and files

Both library tables use the `zero-hat` nickname and `${KIPRJMOD}` paths. All required template libraries are inside this directory.

H1 is a separate, selectable footprint that shows the female 2×20 HAT socket on the underside of the board. Delete H1 when the 3D socket is not wanted, or place `zero-hat:Raspberry_Pi_HAT_2x20_Socket_3D` to add it back. H1 has no electrical pads; U1 remains the authoritative electrical and mechanical interface, and J1 remains the purchasing item.

The local library also copies the grouped 2×4 connector from the full-size template as `Dual_PinSocket_1x04_P2.54mm_J81_J82`. It represents two 1×4 sockets whose centers are exactly 32.020 mm apart. Symbol/footprint pins 1–4 correspond to J81 pins 1–4; pins 5–8 correspond to J82 pins 1–4. Its 29.36 × 11.20 mm inter-header rule area prohibits tracks, vias, pads, copper pours, and footprints on both copper layers while leaving the two connector strips routable.

- [Project settings](RPi%20Zero%20HAT.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](RPi%20Zero%20HAT.kicad_sch): U1 GPIO interface and J1 procurement symbol.
- [PCB](RPi%20Zero%20HAT.kicad_pcb): locked Zero-size outline, interface footprint, mounting-hole lands, and PoE keepout.
- [Symbol library](zero-hat.kicad_sym): GPIO interface, socket purchasing symbol, and grouped J81/J82 connector symbol.
- [Interface footprint](zero-hat.pretty/Raspberry_Pi_Zero_HAT_Interface.kicad_mod).
- [Selectable 2×20 socket footprint](zero-hat.pretty/Raspberry_Pi_HAT_2x20_Socket_3D.kicad_mod): board-only 3D representation used by H1.
- [Grouped 2×4 J81/J82 footprint](zero-hat.pretty/Dual_PinSocket_1x04_P2.54mm_J81_J82.kicad_mod): exact source spacing plus inter-header copper and placement keepout.
- [2×20 socket STEP model](zero-hat.3dshapes/PinSocket_2x20_P2.54mm_Vertical.step) and [model notice](zero-hat.3dshapes/README.md).
- [Template description](meta/info.html) and [preview](meta/board.png): template selector assets.
- [License](LICENSE.md): included with new projects.

KiCad renames the three project design files for the chosen project name and omits `meta` from the new project. Library filenames remain unchanged. Keep generated exports, backups, caches, and local preference files out of this folder because other non-hidden files may be copied into new projects.

## Validation and limits

The template was checked with KiCad 10.0.6. ERC reports the expected 34 errors for this intentionally unwired template: 31 unconnected interface pins plus 3 undriven power-input pins, with no warnings. Native PCB Editor DRC reports no errors, one expected warning because the selectable model-only H1 footprint has no courtyard, and 9 expected unrouted items for the shared 3V3, 5V, and GND header pads. The authoritative physical socket courtyard is part of U1.

Run ERC and DRC after adding the ID EEPROM, application circuit, routing, and copper. This template has no verified physical assembly, connector fit, HAT+ identity data, Raspberry Pi model compatibility, electrical performance, or RF performance.

## Sources and license

The board geometry follows Raspberry Pi's official uHAT mechanical drawing and Raspberry Pi Zero 2 W mechanical drawing. Electrical and compliance notes follow the current HAT+ specification.

The 2×20 socket STEP model derives from the KiCad standard 3D model library and retains the KiCad library license described in the adjacent model notice. The repository MIT license does not replace those third-party terms.

- [Raspberry Pi uHAT mechanical drawing](https://github.com/raspberrypi/hats/blob/master/uhat-board-mechanical.pdf)
- [Raspberry Pi Zero 2 W mechanical drawing](https://pip.raspberrypi.com/documents/RP-008358-DS)
- [Raspberry Pi HAT+ specification](https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf)
- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)

See [LICENSE.md](LICENSE.md).
