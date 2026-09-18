# Footprint provenance

C_0402_1005Metric, R_0402_1005Metric, R_0805_2012Metric and
TSSOP-10_3x3mm_P0.5mm were copied from the standard footprint libraries shipped
with KiCad 10.0.1 on 2026-09-18. Original geometry, descriptions, generators and
3D-model references are retained. Local changes increase silkscreen strokes to
0.15 mm; the crowded 0402 outline marks are moved to F.Fab. No copper pad,
mask/paste aperture, pitch, body or courtyard geometry was changed.

Copyright KiCad Library Contributors. These derived library assets remain under
[CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/),
not the repository's general MIT license. The exception permits use in electronic
designs without imposing the library license on the resulting board design.
Original sources: [KiCad footprints](https://gitlab.com/kicad/libraries/kicad-footprints),
Capacitor_SMD.pretty, Resistor_SMD.pretty and Package_SO.pretty.

Existing Adafruit attribution in SMA_Adafruit_1865_EdgeMount.kicad_mod remains
unchanged. Other pre-existing imported footprints retain their original metadata.

## Wsprry Pi Synth logo

[Wsprry_Pi_Synth_Logo.kicad_mod](Wsprry_Pi_Synth_Logo.kicad_mod) is a local copy
of the two filled F.SilkS polygons in
[the Synth Universal PCB](../../Wsprry-Pi-Synth-Univ/Wsprry-Pi-Synth-Univ.kicad_pcb),
copied on 2026-09-18. The original 2,369 vertices and 4.405354 x 5.584516 mm size
are retained; only the origin is recentered. The source PCB SHA-256 at extraction
was `87db9ae849700e83f1e3ae7403d8ba3c0a0fdbcaaf566431da3428efbb8afbdc`.
The artwork comes from this repository, not the KiCad standard libraries above.

The reusable footprint adds a rectangular placement courtyard and hidden
reference/value fields, with no copper, pads, or soldermask openings. It is a
board-only graphic excluded from the BOM and placement files. The wattmeter
instance, LOGO1, is centered at (152.78, 93.30) mm on F.SilkS, below the existing
power-range text. Existing components and front board text were not moved or changed.

The front logo polygon locks are cleared, including in the reusable library.
LOGO2 is a back-silkscreen copy directly opposite LOGO1, at the same board
coordinates. KiCad native flipping mirrors the artwork for reading from the
back. Both polygons remain contained in one footprint per side, so each logo
moves as a whole. The range text is also copied to B.SilkS at (152.78, 86.27) mm
with mirrored text. Front and back logos remain independent of the text.

KiCad 10.0.1 DRC with schematic parity reports zero errors and four warnings:
the existing front text height/stroke warnings and the same warnings on its
back copy (0.9 mm height / 0.1125 mm stroke versus 1.0 mm / 0.15 mm project
minimums). No rules or exclusions were changed. The native mirrored back
export was visually inspected; existing electrical geometry is unchanged.
