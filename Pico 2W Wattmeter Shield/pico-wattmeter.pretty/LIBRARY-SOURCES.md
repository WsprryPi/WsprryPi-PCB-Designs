# Footprint sources and licenses

## KiCad footprints

`C_0402_1005Metric`, `R_0402_1005Metric`, `R_0805_2012Metric`, and `TSSOP-10_3x3mm_P0.5mm` are derived from the KiCad 10.0.1 standard libraries: `Capacitor_SMD.pretty`, `Resistor_SMD.pretty`, and `Package_SO.pretty`. Their copper pads, mask/paste apertures, pitch, bodies, courtyards, and 3D-model references follow those sources. Local graphics use 0.15 mm silkscreen strokes; 0402 outline marks are on `F.Fab`.

Copyright KiCad Library Contributors. These footprints use [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). The exception permits use in electronic designs without imposing the library license on the resulting design. [Upstream footprint libraries](https://gitlab.com/kicad/libraries/kicad-footprints).

## Adafruit SMA connector

`SMA_Adafruit_1865_EdgeMount.kicad_mod` is derived from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). The footprint contains Adafruit attribution and its source URL. See [J1 connector geometry](../J1-CONNECTOR-NOTES.md).

## Logo

[Wsprry_Pi_Synth_Logo.kicad_mod](Wsprry_Pi_Synth_Logo.kicad_mod) contains the repository's Synth board artwork: two filled polygons in a 4.405354 × 5.584516 mm outline. Both polygons belong to one unlocked footprint, so the logo moves as a unit.

The footprint has a placement courtyard and hidden reference/value fields, with no copper pads or soldermask openings. It is excluded from the BOM and placement files. The board has independent front and back instances, with the rear artwork mirrored for viewing from that side.

## Other library assets

Other imported footprints retain their source metadata. The repository's general MIT license does not replace third-party license terms. The [U1 STEP model](../pico-wattmeter.3dshapes/README.md) has its own KiCad library attribution and license.
