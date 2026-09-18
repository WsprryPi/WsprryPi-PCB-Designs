# Wsprry Pi GPIO Board

GPIO transmission board.

The proposed GPIO-driven broadband-amplifier architecture, development blocks,
selected requirements, and open decisions are maintained in
[BROADBAND-AMPLIFIER-DESIGN.md](BROADBAND-AMPLIFIER-DESIGN.md). That document
defines design targets and does not establish implemented or validated hardware.

## Project files

Open [WsprryPi-GPIO-Univ.kicad_pro](WsprryPi-GPIO-Univ.kicad_pro) in KiCad 10.0.1 or newer. The [schematic PDF](WsprryPi-GPIO-Univ.pdf) is a reference export; the KiCad sources are authoritative.

The [project libraries](libraries/README.md) contain every symbol and footprint used by the design, plus available 3D models. Keep the `libraries/` folder and library tables with the project; their `${KIPRJMOD}` paths resolve within this directory. Library documentation covers connector options, model limitations, sources, and licenses.

## Assembly

C11 is [Panasonic EEEFK1V470P, 47 µF / 35 V](https://www.lcsc.com/product-detail/C178565.html), matching the `C178565` purchasing field, schematic value, and PCB value. Its local footprint uses KiCad's generic `CP_Elec_6.3x5.8` STEP model for visualization; verify the selected part and assembled height mechanically rather than treating the model as physical-fit evidence.

J83 is the locally stored Adafruit 1865 edge-launch SMA connector, with signal on pin 1 and ground on pin 2. It is hand-soldered and excluded from the BOM and position files. The nearby RF route was revised and the conflicting local fence vias were removed; the surrounding ground-via fence remains in place.

Headers J11, J21, J81, and J82 remain part of the electrical design but are excluded from the BOM. Treat them as separately supplied assembly hardware.

## Validation

The renamed design was checked with KiCad 10.0.1. Equivalent checks against a
pre-rename snapshot produced the same findings.

- ERC: no errors and 1 `isolated_pin_label` warning for `GPIO_CLK`.
- DRC: 2 locally overridden `track_dangling` warnings, on `/5V` and
  `/FINAL_OUT`; zero unconnected pads and zero schematic-parity issues.
- Neither report listed ignored checks.

Run ERC and DRC again after later design edits and before producing
manufacturing files. These checks do not establish assembly fit or
electrical/RF performance. Treat the design as untested until revision-specific
physical validation is documented. See the
[repository conventions](../README.md) and
[validation requirements](../CONTRIBUTING.md).
