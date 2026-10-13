# U40 exposed pad and via treatment

U40 is the front-side ADL5904. It has a continuous 1.8 × 1.8 mm ground land with a full F.Mask opening, four paste-only stencil apertures, and five GND through vias connected to the B.Cu ground plane. Two additional DECL through vias are centered on R40 pad 1 and C48 pad 1. All seven request selective filling and capping.

## Geometry

Coordinates are relative to U40's center, in millimetres.

| Feature | Geometry |
| --- | --- |
| Copper pad 17 | 1.8 × 1.8, centered at (0, 0), GND |
| Paste windows | Four 0.65 × 0.65 squares |
| Window centers | (−0.55, −0.55), (+0.55, −0.55), (+0.55, +0.55), (−0.55, +0.55) |
| Total paste aperture area | 1.69 mm²; 52.16% of the copper land area |
| Horizontal and vertical stencil bridges | 0.45 |
| Paste inset from the land edge | 0.025 |
| Via centers | (0, 0), (−0.60, 0), (+0.60, 0), (0, −0.60), (0, +0.60) |
| Via copper diameter / drill | 0.60 / 0.25 |
| Nominal annular-ring width | 0.175 |
| Minimum nominal aperture-to-drill-edge clearance | 0.100 |
| Center-to-outer via drill-edge spacing | 0.35 |

The four paste apertures are unnumbered pads on F.Paste in the placed board footprint with no copper or net. Pad 17 has no full-size paste aperture. All five via annuli lie within the ground land.

## Fabrication and assembly

Fill only the five U40 exposed-pad vias and the two DECL vias with nonconductive epoxy, planarize them, and copper-cap them to IPC-4761 Type VII. Keep their F-side caps solderable within the component-pad openings and cover their B-side pads with soldermask. All seven have filling and capping enabled, front tenting disabled, and back tenting enabled. Front/back ink plugging and additional covering are disabled. Ordinary vias default to tenting on both sides with filling/capping disabled; component through-holes remain open. The ordinary ground vias at (135.680, 94.690) mm and (136.590, 94.670) mm have 0.15 mm nominal drill-to-opening clearance beside C45 and C47. Drill and mask registration tolerances are separate from these nominal dimensions.

These are plated through vias connecting F.Cu to B.Cu. Filling/capping changes the hole treatment, not the layer span. Blind, buried, and microvias remain disallowed on this two-copper-layer board.

| Additional selected via | Net | PCB editor center (X, Y), mm | Copper / drill, mm |
| --- | --- | --- | --- |
| R40 pad 1 | Net-(U40-DECL) | (135.679, 91.280) | 0.60 / 0.25 |
| C48 pad 1 | Net-(U40-DECL) | (138.805, 94.360) | 0.60 / 0.25 |

Both DECL via centers exactly match their solder-pad centers. The front trace terminates at the R40 via center. The back DECL route contains a 0.046 mm segment joining that center to its diagonal toward C48. R40's via annulus extends slightly beyond the resistor land; preserve the combined solderable opening and check it in the fabrication preview.

Supply the [order notes](manufacturing-notes/ORDER-NOTES.txt) and [selective-via drawing](manufacturing-notes/U1-VIA-TREATMENT.svg) to the fabricator. The 0.25 mm drill is unique to these seven vias in the current source. Specify epoxy filling, planarization, and copper capping for all seven 0.25 mm via holes, using the coordinate drawing to cross-check their identity. Leave the five ordinary 0.20 mm vias, ten ordinary 0.30 mm vias, and two ordinary 0.40 mm vias unfilled. CAD flags do not select or confirm the factory's process. Supplier acceptance of selective epoxy filling/copper capping on this two-layer, 1.6 mm board is unconfirmed. [JLCPCB's via-covering guidance](https://jlcpcb.com/help/article/pcb-via-covering) describes the process and selected-hole instructions.

Preserve the four paste windows. The assembler must confirm stencil thickness, paste release, and reflow conditions. Back-side tenting is not a substitute for filling and capping. Nominal aperture clearances do not include drilling and stencil-registration tolerances.

[Analog Devices AN-772](https://www.analog.com/en/resources/app-notes/an-772.html) describes windowed stencil apertures and via treatment. KiCad documents paste-only [SMD aperture pads](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#editing_pad_properties).

## Footprint reuse

The reusable [local QFN footprint](pico-wattmeter.pretty/QFN-16_L3.0-W3.0-P0.50-TL-EP1.8.kicad_mod) and U40 are both front-sided. The footprint contains the copper land and paste windows. The vias remain board objects; recreate them when reusing the footprint on another board. Move U40 and its containing group together and keep the selected vias aligned with U40 pad 17, R40 pad 1, and C48 pad 1.

## Available via settings

| Copper diameter / drill | Annular ring | Use |
| --- | --- | --- |
| 0.50 / 0.20 mm | 0.15 mm | Compact ordinary through via |
| 0.60 / 0.25 mm | 0.175 mm | Seven selected filled/capped through vias |
| 0.60 / 0.30 mm | 0.15 mm | Default ordinary through via |
| 0.80 / 0.40 mm | 0.20 mm | Larger ordinary through via |

The zero-valued preset entry selects netclass defaults. The Default netclass uses 0.60 / 0.30 mm ordinary through vias.

Board minima are 0.50 mm via diameter, 0.20 mm drill, 0.10 mm via annular ring, and 0.25 mm hole-to-hole clearance. U40's smallest drill-edge gap is 0.35 mm. A custom rule disallows micro, blind, and buried vias on this two-copper-layer board. Unused microvia-size fields do not enable those types. The selected through-via dimensions are within [JLCPCB's published drilling capabilities](https://jlcpcb.com/capabilities/pcb-); supplier confirmation of the selective filling process remains separate.
