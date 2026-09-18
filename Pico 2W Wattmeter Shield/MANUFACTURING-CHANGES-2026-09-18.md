# Manufacturing fixes — 2026-09-18

Completed with KiCad **10.0.1** against the saved project. All 21 component
positions/rotations, all 118 track segments, all 25 vias, all pad geometries and
net assignments, and the board outline are unchanged. No resistor values or
RF routing were altered. No commit, push, supplier message, or order was made.

## Implemented

- U1's placed footprint and local library now declare **SMD**. U1 is present in
  the verified SMD-only placement export.
- J1/J2/J3 are excluded from the schematic BOM; J1 is also excluded from PCB BOM
  and placement output. U3 retains its exclusions. J1/U3 physical pads and holes
  remain. The reusable socket symbol/block carries the same factory exclusions.
- The **Shield purchasing BOM** preset exports and groups by LCSC. C9's value
  is normalized from `0.1µF` to the equivalent `100nF`, grouping it with the
  other C60474 capacitors. BOM and placement reference sets match exactly:
  C1-C9, R1-R8, U1, U2 — 19 front-side components, 13 BOM groups.
- Added the standard `power:PWR_FLAG` and a GND symbol as a separate schematic
  power declaration. Existing symbol positions, wires and junctions are unchanged.
- Retained the five already-selected filled/capped U1 vias and the four 0.65 mm
  square paste windows. Added [selective-via drawing](manufacturing-notes/U1-VIA-TREATMENT.svg)
  and [order notes](manufacturing-notes/ORDER-NOTES.txt).
- Increased thin silkscreen strokes to 0.15 mm. Moved crowded 0402 outline
  graphics to F.Fab; they remain in the project but are not printed on the PCB.
  IC pin-1 marks remain on silkscreen. Added a development ID/date and Pico
  USB/antenna orientation text in unused board space. Existing reference fields
  remain hidden; the [assembly drawing](manufacturing-notes/ASSEMBLY-TOP.svg)
  identifies every populated reference and IC pin 1 without crowding the board.
- Tightened silk clearance to 0.15 mm, minimum text height to 1.0 mm and minimum
  text stroke to 0.15 mm; enabled mask subtraction in saved plot settings.
  No rule severity or exclusion was relaxed.
- Added thermal overrides to U3 GND pads 3, 8, 13, 18, 23, 28, 33 and 38:
  0.20 mm gap, 0.30 mm spoke width. The original solid connections were valid;
  this is a hand-soldering improvement. Local footprint settings preserve it on
  library updates. All other ground connections retain their existing treatment.
- Created four project-local derivatives of standard KiCad footprints for the
  silk edits and updated schematic/board assignments. Copper/paste/mask geometry
  remains unchanged; [provenance and licensing](pico-wattmeter.pretty/LIBRARY-SOURCES.md)
  are recorded. Removed the unused machine-specific EasyEDA library registration.
- Updated the socket, SMA, paste and review notes. Documented the actual
  [GPIO-clock application and input range](INPUT-RANGE.md): 2200 m-2 m,
  approximately 136 kHz-148 MHz, with a provisional 100 mW verification ceiling.
  This ceiling is a design target, not an established calibrated rating.

## Validation

| Check | Result |
| --- | --- |
| ERC, all severities | 0 errors, 0 warnings |
| DRC with zone refill and schematic parity | 0 violations, 0 unconnected pads, 0 footprint errors |
| Saved-zone DRC after final schematic-library changes | Same zero results |
| DRC ignored checks / exclusions | None / none |
| ERC ignored categories | Four existing categories unchanged: single global label, four-way junction, SPICE model issue, footprint-filter mismatch |
| BOM vs. SMD-only placement | Same 19 references; all BOM groups have LCSC identifiers |
| Reusable socket-block BOM | No purchased components, consistent with manual fitting |
| Component/via/track preservation | 21 placements, 118 segments, 25 vias unchanged by parsed source comparison |
| Pad and outline preservation | Geometry, drill sizes, net assignments and outline unchanged |
| U1 manufacturing geometry | Four separate 0.65 mm square paste flashes, no central paste region; exactly five filled/capped vias |
| Visual checks | Full schematic, front and rear board exports, header thermals, assembly map and selective-via drawing inspected |

The first stricter DRC retained in `first-drc.rpt` reported six silk-clearance
warnings and two starved-thermal errors from the initial 0.30 mm header thermal
proposal. Moving the 0402 outline marks to F.Fab and reducing thermal gaps to
0.20 mm resolved those findings. `second-drc.rpt` and `final-drc.rpt` pass; no
failed check was hidden or suppressed.

Evidence and before snapshots are in `generated/manufacturing-fixes-2026-09-18/`.
`validation.json` records preservation checks and manufacturing-output checks.
The saved PCB SHA-256 is
`e854d7cfd099d28c233fb6e8c8c7aefd3871ac11fafe0790f266644e90236ca2`.

The regenerated files, drawings and order notes are packaged in
`production/manufacturing-review-2026-09-18/`. This is a review package for
fabricator/assembler confirmation, not an already approved production order.

## Exact changed-source inventory

Updated existing files:

- `Pico 2W Wattmeter Shield.kicad_pcb`
- `Pico 2W Wattmeter Shield.kicad_sch`
- `Pico 2W Wattmeter Shield.kicad_pro`
- `pico-wattmeter.kicad_sym`
- `fp-lib-table`
- `pico-wattmeter.pretty/QFN-16_L3.0-W3.0-P0.50-TL-EP1.8.kicad_mod`
- `pico-wattmeter.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod`
- `pico-wattmeter.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod`
- `pico-wattmeter.kicad_blocks/Pico_2W_Two_Female_Sockets.kicad_block/Pico_2W_Two_Female_Sockets.kicad_sch`
- `pico-wattmeter.kicad_blocks/Pico_2W_Two_Female_Sockets.kicad_block/Pico_2W_Two_Female_Sockets.json`
- `PICO-HEADERS-AND-NOTCH.md`
- `J1-CONNECTOR-NOTES.md`
- `U1-PASTE-WINDOWS.md`
- `MANUFACTURING-REVIEW-2026-09-18.md`

Added source/documentation files:

- `pico-wattmeter.pretty/C_0402_1005Metric.kicad_mod`
- `pico-wattmeter.pretty/R_0402_1005Metric.kicad_mod`
- `pico-wattmeter.pretty/R_0805_2012Metric.kicad_mod`
- `pico-wattmeter.pretty/TSSOP-10_3x3mm_P0.5mm.kicad_mod`
- `pico-wattmeter.pretty/LIBRARY-SOURCES.md`
- `INPUT-RANGE.md`
- `manufacturing-notes/ORDER-NOTES.txt`
- `manufacturing-notes/ASSEMBLY-TOP.svg`
- `manufacturing-notes/U1-VIA-TREATMENT.svg`
- This change record.

## Remaining external checks

The fabricator must confirm selective epoxy fill/capping on its two-layer
process. The assembler must confirm stencil process, actual supplied parts and
IC orientation. The manually fitted socket MPN/mating height and SMA/Pico stack
have not been physically verified, and no missing 3D models were invented.
RF calibration across the intended bands, Wi-Fi sensitivity and the provisional
input ceiling remain physical validation tasks. These cannot be established by
ERC/DRC or by editing the design files.
