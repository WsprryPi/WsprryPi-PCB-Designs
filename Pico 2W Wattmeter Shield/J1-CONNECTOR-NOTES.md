# J1 — Adafruit 1865 SMA connector

Updated 2026-09-17 using KiCad 10.0.1. J1 now specifies the
[Adafruit 1865](https://www.adafruit.com/product/1865), a standard-polarity SMA
female edge-launch connector for a 1.6 mm PCB. The project board thickness is
1.6 mm. Assembly fit and RF performance remain physically untested.

## Current assembly scope

J1 is excluded from the schematic and PCB BOM and from machine placement.
It remains physically present and is fitted by hand. See
[order notes](manufacturing-notes/ORDER-NOTES.txt).

## Source and geometry

The local footprint is an adaptation of `SMA_EDGELAUNCH` in the
[Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library),
which Adafruit identifies for this product. That library is public domain;
Adafruit attribution and its source URL are retained in the footprint description.
The [connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf)
provides the nominal body and contact dimensions used for the fabrication outline.
The barrel outline is simplified and is not a 3D model.

| Feature | Implemented geometry |
| --- | --- |
| Signal | Pad 1, front copper/mask, 1.27 mm wide |
| Ground | Four pads numbered 2, two on each board face, 1.524 mm wide |
| Ground pad centers | ±2.54 mm from the signal centerline; 5.08 mm separation |
| Land extent from seating edge | 0.500 to 4.064 mm; length 3.564 mm |
| Footprint origin | Connector seating edge, on the signal centerline |
| J1 placement | (120.130, 89.688) mm, rotation −90° |
| Soldering | Hand solder; no stencil-paste apertures, following Adafruit's library |

The supplier's original lands begin at the board edge and are 4.064 mm long.
This adaptation trims their edge-facing ends by 0.5 mm to retain the project's
existing copper-to-edge clearance requirement, without changing their inboard
ends. At least 3.3 mm of nominal contact length overlaps exposed copper.
The body seating edge now coincides with the actual left board edge.

The drawing's ground-leg centers are ±2.75 mm (5.50 mm apart), whereas the
supplier's published land centers are ±2.54 mm. These are different measurements:
the supplier's wider 1.524 mm lands cover the nominal 1.0 mm legs. For example,
one land spans 1.778–3.302 mm and its leg spans 2.250–3.250 mm from the centerline.
This replaces the old 1.27 mm lands centered at ±2.1463 mm, which did not fully
cover those legs.

## Files and preservation

- Added [SMA_Adafruit_1865_EdgeMount.kicad_mod](pico-wattmeter.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod).
- Updated J1's footprint assignment, datasheet, description, `Manufacturer`
  (`Adafruit`), and `MPN` (`1865`) in
  [the schematic](Pico%202W%20Wattmeter%20Shield.kicad_sch).
- Replaced J1's pad geometry and fabrication/courtyard graphics and moved its
  seating origin to the board edge in
  [the PCB](Pico%202W%20Wattmeter%20Shield.kicad_pcb).
- Added this note. The old generic `SMA_EDGE` library footprint remains available.

J1 retains its `RF In` value, symbol and pad UUIDs, signal/ground numbering,
electrical connectivity, and pad teardrop settings. All other footprints,
84 track segments, 13 vias, board outline, authored zone boundaries/settings,
project rules, symbol library, and library tables were preserved. KiCad refilled
the zones and regenerated teardrops for the revised pads; generated polygon and
priority changes elsewhere are refill output, not routing edits.

## Validation

- KiCad 10.0.1 ERC: 0 errors and 0 warnings.
- DRC, including schematic parity: 0 violations, 0 unconnected items, and
  0 schematic parity issues.
- No rule thresholds or exclusions changed. ERC retains its four pre-existing
  ignored check categories; DRC has no ignored checks or exclusions.
- Visually inspected front/back copper and the nominal contact outlines at the
  board edge. The contacts land on their assigned exposed pads and existing
  traces remain connected.
- This is a drawing/library-based replacement, not a physical fit test or RF
  qualification. No commit or push was performed.

Reports, source snapshots/hashes, differences, supplier-library snapshot, and
visual exports are retained in `generated/adafruit-1865-2026-09-17/`.
The retrieved Adafruit library SHA-256 is
`3d2af8aa33f0629a2b5c75b7fac3f5a1775724983b71f44c05028fa264d0e99e`.
