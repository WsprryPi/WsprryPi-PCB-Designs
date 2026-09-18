# Wsprry Pi Synth Board

This design is for the Si5351-synthesized transmission board.

Open [Wsprry-Pi-Synth-Univ.kicad_pro](Wsprry-Pi-Synth-Univ.kicad_pro) in KiCad. The [schematic PDF](Wsprry-Pi-Synth-Univ.pdf) is a reference export.

The project uses its own custom footprint library under `libraries/footprints/Wsprry-Pi.pretty`. Its referenced `libraries/symbols/Wsprry-Pi.kicad_sym` library is currently missing.

Treat this design as untested unless a specific revision has documented validation. See the [repository README](../README.md) for KiCad version details, other missing assets, and repository conventions.

## Design considerations

[Optional GPS frequency calibration for Pi and Pico](GPS-FREQUENCY-CALIBRATION.md) records the selected LS7366R counter and a proposed common 3.3 V circuit for Pi and Pico. It describes CLK2 measurement against GPS PPS, SPI capture readout, benefits, standalone operation and holdover, and an optional external GPSDO reference. The circuit has not been implemented or physically validated.
