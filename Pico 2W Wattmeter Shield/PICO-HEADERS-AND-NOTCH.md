# Pico female socket BOM and antenna notch

Updated 2026-09-17 with KiCad 10.0.1.

The PCB keeps the combined `Raspberry_Pi_Pico_2W_Header` footprint: two rows of
20 plated holes, 2.54 mm pitch, 17.78 mm row spacing, 1.00 mm drills, and
1.508 × 1.508 mm pads. Pin numbering, hole/pad geometry, courtyards, component
placement and routing are unchanged. Ground thermal settings were updated as below.

## Bill of materials

J1, J2, J3 and U3 are excluded from the factory assembly BOM. J1 and U3
are excluded from position files. J2/J3 remain pinless schematic-only symbols
recording the two female 1x20, 2.54 mm socket headers fitted by hand. Their
physical rows remain represented by the U3 footprint. The Pico module itself
is also outside the factory assembly scope.

The **Shield purchasing BOM** preset includes the LCSC part identifier and
contains C1-C9, R1-R8, U1 and U2: 19 components. Exact socket manufacturer,
part number and mating height remain to be selected for manual installation.

Eight U3 GND pads (3, 8, 13, 18, 23, 28, 33 and 38) now use thermal reliefs,
with 0.20 mm gap and 0.30 mm spoke width. Pad geometry and placement remain
unchanged. See [manufacturing changes](MANUFACTURING-CHANGES-2026-09-18.md)
for current validation; the original validation below is historical.

## Reuse

The project-local design block is
`pico-wattmeter:Pico_2W_Two_Female_Sockets`. It contains the Pico interface symbol
with the combined footprint assignment and both BOM-only socket symbols.
Application-specific wiring and no-connect flags are intentionally omitted.

In the Schematic Editor, open **View → Panels → Design Blocks**, select the
`pico-wattmeter` library, and place `Pico_2W_Two_Female_Sockets`. Wire the Pico
interface as required and use Update PCB from Schematic. The reusable block also excludes both sockets from the factory BOM.
Enable their BOM inclusion explicitly if a future assembly order should buy them. Placing the bare
Pico symbol or footprint alone does not add the socket procurement symbols.

The block is registered through `${KIPRJMOD}` in `design-block-lib-table`.
To reuse it in another project, make the accompanying symbol, footprint, and
design-block libraries available there under the same `pico-wattmeter` nickname.
There is no machine-specific path in the new registration.

## Antenna opening

The old `Antenna Cutout` was a rule area on `Edge.Cuts`; it did not remove board
material. The header footprint now carries three real `Edge.Cuts` lines defining
a nominal **14 mm-wide × 9 mm-deep open notch**. Its local endpoints are
(-7.89, 26.65) and (6.11, 26.65) mm, with its inner edge at y = 17.65 mm.

On this PCB, the opening occupies x = 164.46–173.46 mm and
y = 82.69–96.69 mm. The former straight right edge was split at those endpoints
and joined to the footprint's notch, forming one closed board perimeter.
The board retains all header holes. The former rule area was moved to F.Cu and
B.Cu and renamed `Pico antenna keepout`; it still forbids tracks, vias, pads,
copper pours, and footprints in that region. Copper was refilled around the
new physical edge.

When this footprint is placed on another board, **join its two notch endpoints
to that board's outer outline**. A footprint cannot automatically trim the
receiving board's edge. Do not leave a straight edge across the notch mouth or
add a fourth closing side at that edge. If the footprint is moved on this board,
update the attached outline segments too. Confirm the fabricator's internal
corner radius when preparing fabrication; physical fit and RF performance are
not validated by these CAD checks.

The geometry follows the antenna clearance area in the
[Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf).
See also KiCad's
[footprint graphics](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#footprint_graphics_and_text),
[BOM documentation](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#generating_a_bill_of_materials),
and [design blocks](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#design_blocks).

## Changed source files

- [Schematic](Pico%202W%20Wattmeter%20Shield.kicad_sch): embedded socket definition,
  J2/J3 procurement symbols and note, U3 BOM/placement attributes.
- [PCB](Pico%202W%20Wattmeter%20Shield.kicad_pcb): U3 notch/keepout and attributes,
  split right edge, regenerated copper fills and teardrops.
- [Project](Pico%202W%20Wattmeter%20Shield.kicad_pro): purchasing BOM preset/settings.
- [Symbol library](pico-wattmeter.kicad_sym): reusable pinless female socket symbol.
- [Header footprint](pico-wattmeter.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod):
  reusable notch, copper keepout, BOM/placement exclusion attributes.
- [Design-block registration](design-block-lib-table).
- [Design-block schematic](pico-wattmeter.kicad_blocks/Pico_2W_Two_Female_Sockets.kicad_block/Pico_2W_Two_Female_Sockets.kicad_sch).
- [Design-block metadata](pico-wattmeter.kicad_blocks/Pico_2W_Two_Female_Sockets.kicad_block/Pico_2W_Two_Female_Sockets.json).
- This note.

## Validation

- KiCad 10.0.1 ERC: 0 errors and 0 warnings.
- DRC: 0 violations, 0 unconnected items, and 0 schematic parity issues.
- All 89 placed pads, 84 track segments, and 13 vias are unchanged, including
  their UUIDs and teardrop settings. All 40 library pads and existing library
  graphics/field UUIDs were preserved.
- Schematic wires, junctions, labels, and no-connect flags are unchanged.
- Board/DRC settings and ERC configuration are unchanged. ERC retains its four
  pre-existing ignored check categories; no DRC exclusions were added.
- Native BOM export verified J2/J3 quantity 2 and U3 omitted. The reusable block
  also parsed/exported successfully and produced a two-socket BOM.
- Visually inspected the complete notch, both copper sides, and the socket
  entries below the Pico schematic symbol. No physical or RF test was performed.

Regenerable reports, BOMs, source snapshots/differences/hashes, and visual exports
are in `generated/headers-notch-2026-09-17/`. No commit or push was performed.
