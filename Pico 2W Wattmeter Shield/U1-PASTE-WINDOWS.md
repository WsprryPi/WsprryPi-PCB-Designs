# U1 exposed pad and via treatment

U1 has a continuous 1.8 × 1.8 mm ground land with a full front soldermask opening, four paste-only stencil apertures, and five ground vias. The plated via barrels connect the land to the rear ground plane.

## Geometry

Coordinates are relative to U1's center, in millimetres.

| Feature | Geometry |
| --- | --- |
| Copper pad 17 | 1.8 × 1.8, centered at (0, 0), GND |
| Paste windows | Four 0.65 × 0.65 squares |
| Window centers | (−0.55, −0.55), (+0.55, −0.55), (+0.55, +0.55), (−0.55, +0.55) |
| Total paste aperture area | 1.69 mm²; 52.16% of the copper land area |
| Horizontal and vertical stencil bridges | 0.45 |
| Paste inset from the land edge | 0.025 |
| Via centers | (0, 0), (−0.60, 0), (+0.60, 0), (0, −0.60), (0, +0.60) |
| Via copper diameter / drill | 0.60 / 0.30 |
| Minimum nominal aperture-to-drill-edge clearance | 0.075 |
| Center-to-outer via drill-edge spacing | 0.30 |

The four paste apertures are unnumbered pads on `F.Paste` with no copper or net. Pad 17 has no full-size paste aperture. All five via annuli lie within the ground land.

## Fabrication and assembly

Fill only these five vias with nonconductive epoxy, planarize them, and copper-cap them to IPC-4761 Type VII. Keep the front caps solderable within the ground-land opening and cover the rear via pads with soldermask. The board specifies filling and capping, front tenting disabled, and back tenting enabled.

Supply the [order notes](manufacturing-notes/ORDER-NOTES.txt) and [selective-via drawing](manufacturing-notes/U1-VIA-TREATMENT.svg) to the fabricator. There are other 0.30 mm vias on the board; do not specify filling by drill diameter alone. CAD flags do not select or confirm the factory's process.

Preserve the four paste windows. The assembler must confirm stencil thickness, paste release, and reflow conditions. Soldermask on the rear is not a substitute for filling and capping. Nominal aperture clearances do not include drilling and stencil-registration tolerances.

[Analog Devices AN-772](https://www.analog.com/en/resources/app-notes/an-772.html) describes windowed stencil apertures and via treatment. KiCad documents paste-only [SMD aperture pads](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#editing_pad_properties).

## Footprint reuse

The [local U1 footprint](pico-wattmeter.pretty/QFN-16_L3.0-W3.0-P0.50-TL-EP1.8.kicad_mod) contains the copper land and paste windows. The vias are board objects, not part of the footprint; place and configure them separately when reusing it.
