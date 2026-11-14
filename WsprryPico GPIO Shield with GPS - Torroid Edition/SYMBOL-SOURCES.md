# WsprryPico GPIO Shield with GPS - Torroid Edition symbol sources

All active symbol definitions resolve through the independent `wsprrypico-gpio-shield-with-gps-torroid-edition` library and [project-local table](sym-lib-table). The library contains exactly **14 used definitions**, including GND and PWR_FLAG. The schematic contains **31 non-power component symbols**, including the two schematic-only socket descriptions. The [circuit details and pin assignments](CIRCUIT-DESIGN.md) and [component inventory](PARTS.csv) identify their current roles and ordering codes. The PCB matches the saved schematic, including its unconnected GPS-reserved pins; [validation](VALIDATION.md) records current checks.

## Copied and adapted KiCad symbols

These graphics originate in KiCad 10.0.6 and retain **CC BY-SA 4.0 with the KiCad library exception**, documented in [KICAD-LIBRARY-LICENSE.md](KICAD-LIBRARY-LICENSE.md). Copies from the [GPIO shield](https://github.com/WsprryPi/WsprryPi-PCB-Designs/blob/64fdd8f336c573cca9bfd5ce1ed3fad3cb0c8cb8/WsprryPico%20GPIO%20Shield/README.md) retain its existing provenance and the [Zero amplifier source notes](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md).

| Local definitions | Origin and function |
| --- | --- |
| C, R, LED, R_Potentiometer_US, BS170 | KiCad passive/transistor graphics via the GPIO shield; supplier fields are set per component |
| TPS22918 | GPIO shield's six-pin load-switch drawing and pin map |
| SMA | Conn_Coaxial_Small-derived two-terminal signal/shield graphics |
| SW_Push | KiCad Switch momentary pushbutton |
| TestPoint | KiCad Connector test point; copper feature excluded from BOM/positions |
| GND, PWR_FLAG | KiCad power symbols |

U31 uses 1 VIN, 2 GND, 3 ON, 4 CT, 5 QOD and 6 VOUT. Q61 uses 1 drain, 2 gate and 3 source. RV61 pin 2 is the wiper and pin 3 the clockwise end. Exact connected nets are recorded in [circuit details](CIRCUIT-DESIGN.md).

Generic C and R definitions keep ordering data in each placed instance because their values and manufacturers vary. R permits the local 0603 and 1206 footprint types; R64 uses 1206. The project-specific trimmer definition defaults to Bourns TC33X-2-103E / C719176 and its local footprint. Supplier fields agree between schematic, [parts inventory](PARTS.csv) and [workbook](LCSC-parts-collection.xlsx). The component fields agree; native schematic/PCB parity reports zero differences in [validation](VALIDATION.md).

## Original symbols

Original project graphics follow [LICENSE.md](LICENSE.md). Manufacturer references establish electrical pin functions rather than granting a license to reproduce their drawings.

- **Bifilar_Autotransformer_1to4:** original four-terminal, series-winding graphic with dots at pins 1 and 3. A start = 1, A finish = 2, B start = 3, B finish = 4. The schematic joins 2/3 at the drain. Defaults select the [Fair-Rite 5977000621 core](https://fair-rite.com/product/toroids-5977000621/) and 15+15 AWG26 turns; the MPN is core-only. The default footprint is the original local `T61_FairRite_5977000621_Upright_Bumper_4Pin`, with matching logical pin numbering and filter. Ends 2/3 share one 1.2 mm plated hole; end 3 is a coincident drill-free copper pad, so the four-end symbol and phasing stay unchanged. The footprint places separate ends 1/4 on +Y and the shared 2/3 hole on -Y. It does not assert a simulated RF model. The unused VLS6045EX_331M symbol definition was removed from both library and schematic cache.
- **Raspberry_Pi_Pico_2W:** combined 40-pin electrical interface U11, with independent schematic-only J11/J12 purchasing descriptions in **Socket_1x20_P2.54mm_BOM**, from the [local Pico reference assets](../Pico%202W%20Wattmeter%20Shield/pico-2w-libs/README.md).

## Assembly and validation

J11/J12 have no separate PCB footprints; U11 owns both socket rows. Manual parts and test points retain their exclusions from automated assembly outputs. T61 is on-board in the electrical design and now has a local mounting footprint; it remains excluded from automated SMT BOM/positions. Every physical schematic component has a local footprint. T61's mechanical qualification remains open; PCB integration within the outline passes CAD checks. See [current ERC/DRC results and outstanding findings](VALIDATION.md).

The existing two-pin **LED** and **SW_Push** graphics are retained for D11/SW11; their defaults, placed fields, caches and local footprint assignments select **Kingbright WP710A10LID** and **Alps Alpine SKHLACA010**. Both placed symbols and footprints are excluded from factory BOM/positions and listed as manual purchases. D11 retains pin 1 cathode / pin 2 anode; SW11 remains normally open from GP0 to GND. RV61 retains its original underside SMT status.

C64 and restored C66–C69 use the generic C symbol, Walsin 1206N104J500CT / C170182, and the local 1206 footprint. Their five parallel 100 nF values total 500 nF. The former C66–C69 symbol UUIDs were restored. The capacitor filters now list only the used 0603/0805/1206 packages. TestPoint defaults and cached filters select the copper-only 1 mm pad. There are still 14 active electrical definitions.

## Low-support mounting description, 2026-10-21

T61 description metadata in the local symbol, schematic cache/instance and PCB now specifies a builder-selected mount. Symbol graphics, pins, phasing, footprint assignment, electrical properties and UUIDs are unchanged. The 1.25 mm support belongs to the illustrative 3D model, not a prescribed purchasing part.
