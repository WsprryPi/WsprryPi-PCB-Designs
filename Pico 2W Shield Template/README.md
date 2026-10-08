# Pico 2W Shield Template

A KiCad 10 project template for Raspberry Pi Pico 2 W shield designs. It contains the header interface, board outline, antenna notch, and local libraries. The schematic is unwired; the board has no tracks, vias, or copper pours.

## Board-side and USB reference update — 2026-10-07

The Pico sockets are now on B.Cu; use F.Cu as the primary component side in derived shields. The entire board was reflected about its horizontal centerline, including components, tracks, vias, zones, outline, markings and antenna clearance. Relative placement, pad numbers/net assignments, routed lengths and widths, UUIDs, locks and assembly exclusions were preserved. The USB label is centered in its Dwgs.User reference box in both the placed interface and the independent local header library. The library footprint remains front-sided; the board instance determines the mounting side.

KiCad **10.0.6**: after refilling copper, **0 DRC violations, 0 unconnected items and 0 schematic-parity findings**. ERC remains **52 expected unwired-interface errors / 0 warnings**; the schematic and project settings are byte-for-byte unchanged. Preservation checks cover 1 footprints, 40 pads, 0 tracks/vias and 0 board zones. A complete inverse-flip comparison reproduced the original board properties apart from KiCad's invalidated fill-cache flag; final saved routing and pin/net geometry were checked again after refill. Native 3D views were inspected. Existing ERC ignored-check categories remain unchanged; no new suppressions or weakened rules were introduced.

## Create a new shield

1. In KiCad's project manager, open **Preferences → Configure Paths…**.
2. Set `KICAD_USER_TEMPLATE_DIR` to the parent directory containing this template folder: the `WsprryPi PCB Designs` repository root. Alternatively, copy the entire template folder into your existing user-template directory.
3. Choose **File → New Project…**, select **Pico 2W Shield Template**, and give the project its own name and directory. Reopen the project manager if its template list has not refreshed.
4. Add your circuit, wire the required Pico pins, and mark unused pins with no-connect flags.
5. Run **Tools → Update PCB from Schematic…**, place the components, route the board, add and fill copper zones, and run ERC and DRC.

Each new project has independent copies of the design files and libraries. Template edits do not update existing shields. New designs define their own ground, analog-ground, and power connections.

## Mechanical interface

| Item | Geometry |
| --- | --- |
| Header rows | Two 1×20 rows, 2.54 mm pitch, 17.78 mm between row centers |
| Pads | 1.508 × 1.508 mm square pads; 1.00 mm drills |
| Board | 53.33 × 22.85 mm outer envelope; 1.6 mm thickness; two copper layers |
| Outer corners | Nominal 1 mm radius |
| Antenna opening | 14 mm wide × 9 mm deep, open to the right edge |
| Keepout | Both copper layers; tracks, vias, pads, copper pours, and footprints prohibited |

U1 is the combined 40-pad header footprint. It and the nine board-level outline segments/arcs are locked. Three `Edge.Cuts` segments inside U1 form the antenna notch and join the board perimeter. Keep these endpoints joined when resizing the shield; moving U1 alone breaks the outline.

## Header previews and manufacturing outputs

U1 represents the electrical Pico interface and is excluded from the purchasing BOM and placement output. Its footprint carries two local female 1×20, 2.54 mm socket models aligned with the pad rows, so both headers appear in KiCad's 3D viewer and rendered previews. The models do not add components to manufacturing outputs.

J1 and J2 are pinless, schematic-only socket descriptions with optional purchasing fields. They are excluded from the BOM, board, and placement output by default and create no additional PCB footprints. The schematic's **Shield purchasing BOM** preset respects these exclusions; the unwired template therefore exports no component rows.

The socket models are generic visual aids, not a selected manufacturer's part or a fit qualification. Manufacturer and MPN fields are blank. Select compatible lead dimensions, body width, and mating height before assembly. If a future shield requires socket procurement, explicitly enable J1/J2 BOM inclusion and enter the selected part on both symbols. Configure manufacturing outputs to match the parts the factory will fit.

## Local libraries and files

Both library tables use the `pico-wattmeter` nickname and `${KIPRJMOD}` paths. All required libraries and socket 3D models are inside this directory.

- [Project settings](Pico%202W%20Shield%20Template.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](Pico%202W%20Shield%20Template.kicad_sch): U1 interface and excluded J1/J2 socket descriptions.
- [PCB](Pico%202W%20Shield%20Template.kicad_pcb): header interface, outline, and antenna keepout.
- [Symbol library](pico-wattmeter.kicad_sym): Pico interface and socket definitions.
- [Header footprint](pico-shield.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod).
- [Socket model and third-party terms](pico-shield.3dshapes/README.md).
- [Symbol table](sym-lib-table) and [footprint table](fp-lib-table): local library registration.
- [Template description](meta/info.html) and [preview](meta/board.png): template selector assets.
- [License](LICENSE.md): included with new projects.

KiCad renames the three project design files for the chosen project name and omits `meta` from the new project. Library filenames remain unchanged. Keep temporary exports and local preferences out of the template folder because other non-hidden files can be copied into new projects.

Git ignores `jlcpcb/`, generated exports, fabrication packages, backups, caches, and editor state. Design sources, local libraries, template metadata, and documentation belong in Git.

## Validation and limits

The unwired interface produces expected ERC findings: 40 unconnected pins, 10 undriven power inputs, and two undriven signal inputs. Connect required pins and mark only unused pins with no-connect flags when developing a circuit. ERC ignores `footprint_filter`, `four_way_junction`, `simulation_model_issue`, and `single_global_label`.

The header-preview update was checked with KiCad 10.0.6: DRC reported zero violations and zero unconnected items; ERC retained the same 52 findings above. The **Shield purchasing BOM** and CSV placement exports contained no component rows. The 3D render was visually checked for both socket rows and is used as the template-selector preview. PCB and footprint geometry, connectivity, UUIDs, and exclusion attributes were unchanged by the model additions.

Run ERC and DRC after developing the circuit or changing the mechanical interface. This template has no verified physical assembly, socket fit, fabrication, or RF performance.

## Sources and license

The interface derives from the Pico 2W Wattmeter Shield in [WsprryPi PCB Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs). See [LICENSE.md](LICENSE.md).

- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)
- [Raspberry Pi Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf)
