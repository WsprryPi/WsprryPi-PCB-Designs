# WsprryPico Shield

A standalone KiCad 10 project copied from the [Pico 2W Shield Template](../Pico%202W%20Shield%20Template/README.md). It contains the header interface, board outline, antenna notch, and independent local libraries. The schematic is unwired; the board has no tracks, vias, or copper pours.

## Develop this shield

1. Open [WsprryPico Shield.kicad_pro](WsprryPico%20Shield.kicad_pro) in KiCad.
2. Add your circuit, wire the required Pico pins, and mark unused pins with no-connect flags.
3. Run **Tools → Update PCB from Schematic…**, place the components, route the board, add and fill copper zones, and run ERC and DRC.

This project has independent copies of all required design files and libraries. It has no symlinks or library dependencies on the source template or Wattmeter Shield. Template edits do not update this shield. Define its ground, analog-ground, and power connections as development proceeds.

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

J1 and J2 are pinless, schematic-only socket descriptions with optional purchasing fields. They are excluded from the BOM, board, and placement output by default and create no additional PCB footprints. The schematic's **Shield purchasing BOM** preset respects these exclusions; the unwired starter therefore exports no component rows.

The socket models are generic visual aids, not a selected manufacturer's part or a fit qualification. Manufacturer and MPN fields are blank. Select compatible lead dimensions, body width, and mating height before assembly. If a future shield requires socket procurement, explicitly enable J1/J2 BOM inclusion and enter the selected part on both symbols. Configure manufacturing outputs to match the parts the factory will fit.

## Local libraries and files

Both library tables use the `wsprrypico-shield` nickname and `${KIPRJMOD}` paths. All schematic library IDs, footprint assignments, and project library pins use that nickname. The PCB and local footprint reference the copied socket model through `${KIPRJMOD}/wsprrypico-shield.3dshapes/`. All required libraries and socket 3D models are inside this directory.

- [Project settings](WsprryPico%20Shield.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](WsprryPico%20Shield.kicad_sch): U1 interface and excluded J1/J2 socket descriptions.
- [PCB](WsprryPico%20Shield.kicad_pcb): header interface, outline, and antenna keepout.
- [Symbol library](wsprrypico-shield.kicad_sym): Pico interface and socket definitions.
- [Header footprint](wsprrypico-shield.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod).
- [Socket model and third-party terms](wsprrypico-shield.3dshapes/README.md).
- [Symbol table](sym-lib-table) and [footprint table](fp-lib-table): local library registration.
- [License](LICENSE.md): preserved from the source template.

The three project design files and their internal project/sheet names use `WsprryPico Shield`. The copied libraries use the distinct `wsprrypico-shield` name. Template-selector metadata, local preferences, locks, backups, and generated outputs were not copied.

Git ignores `jlcpcb/`, generated exports, fabrication packages, backups, caches, and editor state. Design sources, local libraries, and documentation belong in Git.

## Validation and limits

The unwired interface produces expected ERC findings: 40 unconnected pins, 10 undriven power inputs, and two undriven signal inputs. Connect required pins and mark only unused pins with no-connect flags when developing a circuit. ERC ignores `footprint_filter`, `four_way_junction`, `simulation_model_issue`, and `single_global_label`.

Creation of this independent project was checked with KiCad 10.0.6: DRC reported zero violations and zero unconnected items; ERC retained the same 52 findings above. The **Shield purchasing BOM** and CSV placement exports contained no component rows. The 3D render was visually checked for both socket rows. Symbol and footprint exports and reference-path checks verified the copied local assets. Project renaming and library repointing preserved PCB and footprint geometry, connectivity, UUIDs, and exclusion attributes.

Run ERC and DRC after developing the circuit or changing the mechanical interface. This shield has no verified physical assembly, socket fit, fabrication, or RF performance.

## Sources and license

This project was copied from the Pico 2W Shield Template, whose interface derives from the Pico 2W Wattmeter Shield in [WsprryPi PCB Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs). See [LICENSE.md](LICENSE.md) and the [socket model terms](wsprrypico-shield.3dshapes/README.md).

- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)
- [Raspberry Pi Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf)
