# Wsprry Pi GPIO Board

GPIO transmission board.

## Project files

Open [Wsprry-Pi-GPIO-Univ.kicad_pro](Wsprry-Pi-GPIO-Univ.kicad_pro) in KiCad 10.0.1 or newer. The [schematic PDF](Wsprry-Pi-GPIO-Univ.pdf) is a reference export; the KiCad sources are authoritative.

The [project libraries](libraries/README.md) contain every symbol and footprint used by the design, plus available 3D models. Keep the `libraries/` folder and library tables with the project; their `${KIPRJMOD}` paths resolve within this directory. Library documentation covers connector options, model limitations, sources, and licenses.

## Assembly

C11 is [Panasonic EEEFK1V470P, 47 µF / 35 V](https://www.lcsc.com/product-detail/C178565.html), matching the `C178565` purchasing field, schematic value, and PCB value. Its local footprint uses KiCad's generic `CP_Elec_6.3x5.8` STEP model for visualization; verify the selected part and assembled height mechanically rather than treating the model as physical-fit evidence.

J83 is the locally stored Adafruit 1865 edge-launch SMA connector, with signal on pin 1 and ground on pin 2. It is hand-soldered and excluded from the BOM and position files. The nearby RF route was revised and the conflicting local fence vias were removed; the surrounding ground-via fence remains in place.

Headers J11, J21, J81, and J82 remain part of the electrical design but are excluded from the BOM. Treat them as separately supplied assembly hardware.

## Validation

The design was checked with KiCad 10.0.1 after the edge-connector and 3D-model changes. Run ERC and DRC again after later design edits and before producing manufacturing files.

- ERC: no errors and 1 unconnected-wire-endpoint warning.
- DRC: zero violations, unconnected pads, or schematic-parity errors.

The macOS `kicad-cli pcb drc` launcher aborted in KiCad's UI-registration path during this review, so the reported DRC result comes from the native PCB Editor with zone refill and schematic parity enabled. Board parsing, STEP export, and 3D rendering completed successfully.

The project settings include ignored ERC/DRC categories. These checks do not establish assembly fit or electrical/RF performance. Treat the design as untested until revision-specific physical validation is documented. See the [repository conventions](../README.md) and [validation requirements](../CONTRIBUTING.md).
