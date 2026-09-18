# Pico 2W Shield Template

A KiCad 10 project template for Raspberry Pi Pico 2 W shield designs. It contains the header interface, board outline, antenna notch, and local libraries. The schematic is unwired; the board has no tracks, vias, or copper pours.

## Create a new shield

1. In KiCad's project manager, open **Preferences → Configure Paths…**.
2. Set `KICAD_USER_TEMPLATE_DIR` to the parent directory containing this template folder: the `Wsprry Pi PCB Designs` repository root. Alternatively, copy the entire template folder into your existing user-template directory.
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

## Purchasing BOM

U1 represents the electrical Pico interface and is excluded from the purchasing BOM and placement output. J1 and J2 are pinless, schematic-only purchasing symbols for two female 1×20, 2.54 mm socket headers. They create no additional PCB footprints.

The schematic's **Shield purchasing BOM** preset exports one grouped row: `J1,J2`, quantity `2`, value `Socket_1x20_P2.54mm`. A PCB-only export omits these socket procurement items. Enable U1's BOM inclusion if the assembly order includes the Pico module.

Manufacturer and MPN fields are blank. Select compatible lead dimensions, body width, and mating height, then enter the selected part on both J1 and J2. For factory assembly, set BOM and placement exclusions to match the parts the factory will fit.

## Local libraries and files

Both library tables use the `pico-wattmeter` nickname and `${KIPRJMOD}` paths. All required libraries are inside this directory. The header footprint has no attached 3D model.

- [Project settings](Pico%202W%20Shield%20Template.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](Pico%202W%20Shield%20Template.kicad_sch): U1 interface and J1/J2 procurement symbols.
- [PCB](Pico%202W%20Shield%20Template.kicad_pcb): header interface, outline, and antenna keepout.
- [Symbol library](pico-wattmeter.kicad_sym): Pico interface and socket definitions.
- [Header footprint](pico-shield.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod).
- [Symbol table](sym-lib-table) and [footprint table](fp-lib-table): local library registration.
- [Template description](meta/info.html) and [preview](meta/board.png): template selector assets.
- [License](LICENSE.md): included with new projects.

KiCad renames the three project design files for the chosen project name and omits `meta` from the new project. Library filenames remain unchanged. Keep temporary exports and local preferences out of the template folder because other non-hidden files can be copied into new projects.

Git ignores `jlcpcb/`, generated exports, fabrication packages, backups, caches, and editor state. Design sources, local libraries, template metadata, and documentation belong in Git.

## Validation and limits

The unwired interface produces expected ERC findings: 40 unconnected pins, 10 undriven power inputs, and two undriven signal inputs. Connect required pins and mark only unused pins with no-connect flags when developing a circuit. ERC ignores `footprint_filter`, `four_way_junction`, `simulation_model_issue`, and `single_global_label`.

Run ERC and DRC after developing the circuit or changing the mechanical interface. This template has no verified physical assembly, socket fit, fabrication, or RF performance.

## Sources and license

The interface derives from the Pico 2W Wattmeter Shield in [WsprryPi PCB Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs). See [LICENSE.md](LICENSE.md).

- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)
- [Raspberry Pi Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf)
