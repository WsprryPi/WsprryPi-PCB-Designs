# U1 exposed-pad paste windows

Updated 2026-09-18 using KiCad 10.0.1.

U1's ADL5904 exposed pad retains its continuous 1.8 × 1.8 mm GND copper
and full solder-mask opening. Four separate square apertures on `F.Paste`
replace the full-pad paste opening. This is a stencil-layout change with
four ground-via relocations; assembly and RF performance remain untested.

## Geometry

All coordinates below are relative to U1's center, in millimetres.

| Feature | Geometry |
| --- | --- |
| Copper pad 17 | 1.8 × 1.8, centered at (0, 0), GND |
| Paste windows | Four 0.65 × 0.65 squares |
| Window centers | (−0.55, −0.55), (+0.55, −0.55), (+0.55, +0.55), (−0.55, +0.55) |
| Total paste aperture area | 1.69 mm², or 52.16% of the copper pad area |
| Horizontal and vertical stencil bridges | 0.45 |
| Paste inset from the paddle's outside edge | 0.025 |
| Via centers | (0, 0), (−0.60, 0), (+0.60, 0), (0, −0.60), (0, +0.60) |
| Via copper diameter / drill | 0.60 / 0.30, unchanged |
| Minimum nominal aperture-to-hole-edge clearance | 0.075 |

The four outer ground vias were moved from their previous corner positions
into a cross. The center via, all five via UUIDs, net assignments, sizes, and
drills were preserved. All via annuli remain within the paddle copper.
The center-to-outer via drill-edge spacing is 0.30 mm.

The imported footprint also contained a separate, filled 1.2 × 1.2 mm
`F.Paste` polygon over the paddle. It was removed from both the library and
board footprint; retaining it would bridge the new windows. The perimeter-pad
paste features were left unchanged.

## Grounding and assembly

Pad 17 remains on `F.Cu` and `F.Mask`, connected to GND. The four new pads
are unnumbered, paste-only apertures with no copper or net. The vias connect
the paddle to the existing back ground plane through their plated barrels.
The five board-level paddle vias now explicitly specify filling and copper
capping, with front/back tenting disabled. Their locations remain the cross
pattern below U1; the current center is (133.081114, 89.499999) mm.
The full paddle mask opening and four paste windows are unchanged. All other
vias retain their existing treatment. These CAD flags must be accompanied by
[order notes](manufacturing-notes/ORDER-NOTES.txt) and the
[selective-via drawing](manufacturing-notes/U1-VIA-TREATMENT.svg).
The original validation section below records the earlier, pre-fill/cap edit.

The square windows provide a straightforward stencil pattern while keeping
initial paste deposits clear of the nominal drill openings. Without the specified physical fill/cap process, molten solder
can still enter the holes during reflow. The 0.075 mm clearance is a CAD
dimension, not a guarantee after drilling and stencil-registration tolerances.
Have the assembler assess stencil thickness, paste release, coverage, and
the actual via treatment. Do not replace these windows with an automatic
full-pad stencil opening when ordering assembly.

[Analog Devices AN-772](https://www.analog.com/en/resources/app-notes/an-772.html)
describes windowed stencil apertures, typical 50–80% coverage, and the
interaction between coverage and via treatment. That general guidance does
not qualify this board's assembly process. KiCad documents paste-only
[SMD Aperture pads](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#editing_pad_properties).

## Files and reuse

- [PCB](Pico%202W%20Wattmeter%20Shield.kicad_pcb): pad-17 paste membership,
  four new paste apertures, removal of the redundant center paste polygon,
  and relocation of four existing GND vias.
- [Local footprint](pico-wattmeter.pretty/QFN-16_L3.0-W3.0-P0.50-TL-EP1.8.kicad_mod):
  matching paste-only changes, so a library update retains the pattern.
- This note.

The vias remain board-level objects, as before. When reusing the footprint,
place any exposed-pad vias to suit the paste windows; the footprint does not
automatically create or reposition them.

## Validation

- KiCad 10.0.1 DRC with in-memory zone refill, schematic parity, and all
  severities: 0 violations, 0 unconnected pads, 0 footprint/parity errors.
  No DRC exclusions or ignored categories.
- ERC before and after: the same existing `power_pin_not_driven` error on
  U1 pin 11 (GND), with 0 warnings. The four existing ignored ERC categories
  are unchanged. This paste edit does not resolve that schematic issue.
- Native KiCad board/library loading verifies 17 numbered electrical pads
  plus four unnumbered paste-only apertures. Loading through the headless
  Python API also emits a wxApp initialization diagnostic; CLI exports and
  the full DRC completed successfully.
- Exact source comparisons preserve all 126 tracks, 25 via identities and
  sizes, 21 footprint placements, other pads/graphics, zones, and board
  settings. Only the four documented via positions changed. The schematic
  and project settings are byte-for-byte unchanged.
- Exported `F.Paste` Gerber verified to contain exactly four 0.65 mm square
  windows over the paddle, with no residual center paste region.
- Visually inspected the native KiCad copper/paste export with all five
  drill holes. Exported drill coordinates match the relocated vias.
- Markdown local links and `git diff --check` passed. No source file was
  ignored; regenerable validation outputs are ignored as intended.

Source snapshots, diffs, geometry checks, reports, Gerbers, drill output, and
the detail image are in `generated/windowed-paste-2026-09-18/`. These are
review outputs, not a released manufacturing package. No commit or push
was performed.
