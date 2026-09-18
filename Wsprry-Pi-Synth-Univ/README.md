# Wsprry Pi Synth Board

Si5351-synthesized transmission board.

## Project files

Open [Wsprry-Pi-Synth-Univ.kicad_pro](Wsprry-Pi-Synth-Univ.kicad_pro) in KiCad 10.0.1 or newer. The [schematic PDF](Wsprry-Pi-Synth-Univ.pdf) is a reference export; the KiCad sources are authoritative.

The [project libraries](libraries/README.md) contain every symbol and footprint used by the design, plus available 3D models. Keep the `libraries/` folder and library tables with the project; their `${KIPRJMOD}` paths resolve within this directory. Library documentation covers connector options, model limitations, sources, and licenses.

## Assembly

**Resolve C11 before ordering:** the schematic and PCB specify 100 µF, but the `C178565` purchasing fields select [Panasonic EEEFK1V470P, 47 µF / 35 V](https://www.lcsc.com/product-detail/C178565.html). The local symbol default describes the 47 µF part.

J83 is a through-hole BWSMA-KWE-Z001 connector ([LCSC C496551](https://www.lcsc.com/product-detail/C496551.html)), with signal on pin 5 and ground on pins 1–4. The local Adafruit 1865 edge-launch option uses signal pin 1 and ground pin 2; using it requires schematic pin mapping and PCB routing changes.

## Validation

The validation baseline is source revision `bc5cba8`, checked with KiCad 10.0.1. Run ERC and DRC again after design edits and before producing manufacturing files.

- ERC: no errors and 2 unconnected-wire-endpoint warnings.
- DRC: zero violations, unconnected pads, or footprint errors.

The project settings include ignored ERC/DRC categories. These checks do not establish assembly fit or electrical/RF performance. Treat the design as untested until revision-specific physical validation is documented. See the [repository conventions](../README.md) and [validation requirements](../CONTRIBUTING.md).

## Design considerations

[Optional GPS frequency calibration for Pi and Pico](GPS-FREQUENCY-CALIBRATION.md) records the selected LS7366R counter and a proposed common 3.3 V circuit for Pi and Pico. It describes CLK2 measurement against GPS PPS, SPI capture readout, benefits, standalone operation and holdover, and an optional external GPSDO reference. The circuit has not been implemented or physically validated.
