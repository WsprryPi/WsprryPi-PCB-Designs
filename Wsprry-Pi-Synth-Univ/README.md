# Wsprry Pi Synth Board

This design is for the Si5351-synthesized transmission board.

Open [Wsprry-Pi-Synth-Univ.kicad_pro](Wsprry-Pi-Synth-Univ.kicad_pro) in KiCad.
The [schematic PDF](Wsprry-Pi-Synth-Univ.pdf) is a reference export.

The project uses its own custom footprint library under
`libraries/footprints/Wsprry-Pi.pretty`. Its referenced
`libraries/symbols/Wsprry-Pi.kicad_sym` library is currently missing.

Treat this design as untested unless a specific revision has documented
validation. See the [repository README](../README.md) for KiCad version details,
other missing assets, and repository conventions.

## Design considerations

[Optional GPS frequency calibration for Pi and Pico](GPS-FREQUENCY-CALIBRATION.md)
describes a proposed CLK2 feedback circuit for measuring TCXO error against GPS
PPS, its benefits, standalone operation and holdover, and an optional external
GPSDO reference. This proposal has not been implemented or physically validated.
