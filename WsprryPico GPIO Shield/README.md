# WsprryPico GPIO Shield

A standalone Pico 2 W GPIO amplifier project, renamed from WsprryPico Shield on 2026-10-06. The current schematic and placed/routed PCB from commit 272b191 are preserved, including their wiring, geometry, UUIDs, settings and assembly exclusions. Project and local-library names now identify the GPIO shield.

Open [WsprryPico GPIO Shield.kicad_pro](WsprryPico%20GPIO%20Shield.kicad_pro). See [the current rename and validation record](RENAME-VALIDATION.md) for the changed-file inventory and checks. The earlier import descriptions below record the 2026-10-05 development stage and do not describe the current wired/routed source.

For the hand-fitted J51 SMA connector, **Superbat ASIN B09V5811S7, “0.062 inch Straight Connector”**, is a probable Amazon alternative to Adafruit 1865, pending sample fit and RF verification. The [connector candidate record](../Pico%202W%20Wattmeter%20Shield/J1-CONNECTOR-NOTES.md#probable-amazon-alternative-superbat-b09v5811s7) gives the purchasing link, supplier drawing, nominal land-pattern comparison, and acceptance checks. Its longer bulkhead barrel and nut require a separate clearance check; the current footprint, model, and manual-assembly exclusions are unchanged.

## Historical import record

A standalone KiCad 10 project based on the [Pico 2W Shield Template](../Pico%202W%20Shield%20Template/README.md), with the single-BS170 circuit copied from [WsprryPi Zero GPIO BS170](../WsprryPi%20Zero%20GPIO%20BS170/README.md). The schematic contains the same five functional groups and internal circuit connections. All 40 Pico bus pins remain electrically isolated, including power and ground, until the pin and supply plan is decided.

The PCB still contains only the Pico interface, board outline, and antenna keepout. Its header reference and isolated pad-net names were renumbered to U11; the imported circuit has not been placed or routed. This shield is in development.

## Schematic groups and references

On 2026-10-05, the original U1 interface became U11, and the J1/J2 socket purchasing descriptions became J11/J12. The source RF-selection header J12 became J13 to avoid colliding with the second Pico socket. The remaining copied references retain the Zero BS170 numbering.

| Series | Functional block | References |
| --- | --- | --- |
| 10 | Pico interface, two socket purchasing items, RF-selection header, indicator, and switch | `U11`, `J11`, `J12`, `J13`, `D11`, `R11`, `SW11` |
| 20 | TPS22918 switched amplifier supply and bias-setting bypass | `U21`, `C21`, `C22`, `C23`, `R21`, `R22`, `J21` |
| 30 | RF AC coupling, damping, adjustable gate bias, pull-down, and bias bypass | `C31`, `R31`, `RV31`, `R32`, `R33`, `C32` |
| 40 | BS170 amplifier, drain choke, supply bypassing, and 0 Ω link | `Q41`, `L41`, `C41`, `C42`, `R41` |
| 50 | Output DC blocking, SMA, and paired LPF socket interface | `C51`, `J51`, `J52` |

The import adds 25 physical circuit components, 16 local symbol definitions, 15 local footprints, and nine local 3D models. Values, sourcing fields, internal pin connections, and assembly exclusions are preserved from the source. The Pi interface and its purchasing symbol were replaced by the existing Pico interface and socket descriptions. Every imported instance has a new UUID; the Pico header and socket instance UUIDs are preserved.

The source host labels were changed to `PICO_RF_A`, `PICO_RF_B`, `PICO_LED`, `SWITCH_IN`, and `AMP_5V_IN`. These names identify open connection choices; they do not assign Pico GPIO numbers. `AMP_EN` remains the amplifier-enable boundary, and `GPIO_RF` remains the internal RF path from J13 pin 2 to C31.

## Connections to decide and correct

| Connection | Current circuit endpoint | Decision / correction required |
| --- | --- | --- |
| RF drive | J13 pin 1 = `PICO_RF_A`; pin 3 = `PICO_RF_B`; center pin 2 = `GPIO_RF` to C31 pin 1 | Choose the Pico RF GPIO and whether to retain two selectable candidates. Match the firmware pin assignment to the fitted shunt; reserve each selected GPIO exclusively for RF. |
| Amplifier enable | `AMP_EN`: U21 pin 3 and R21 pin 1 | Choose a free Pico GPIO and firmware enable timing, including startup and idle behavior. The input is active-high, with R21 providing a 100 kΩ pull-down. |
| Pushbutton | `SWITCH_IN`: SW11 pin 1; pin 2 is grounded | Choose a Pico GPIO with a pull-up and define its software action. If the button should reset the Pico, explicitly select RUN (physical pin 30) instead of a GPIO input. |
| Indicator | `PICO_LED`: D11 pin 2; D11/R11 return to ground | Choose an external indicator GPIO, or retain the Pico's onboard indicator and omit the external LED circuit in a later revision. The copied external circuit is active-high. |
| Amplifier supply | `AMP_5V_IN`: U21 pin 1, C21 pin 1, J21 pin 1 | Choose USB VBUS, VSYS, or an external regulated supply. Confirm the available voltage/current and power path before using the copied 5 V bias and drain circuit. |
| Ground return | Circuit `GND`; all Pico ground pins are currently open | Connect the selected Pico GND pins and define the RF/power return arrangement. Decide how AGND will be used if ADC functions are added. |
| Other Pico pins | RUN, 3V3_EN, 3V3_OUT, ADC_VREF, and unused GPIOs | Decide which are needed for reset, power control, sensing, or expansion. Mark only genuinely unused pins with no-connect flags after the complete pin plan is agreed. |

Pico physical pin 40 is USB VBUS (nominally 5 V); pin 39 is VSYS (1.8–5.5 V), so VSYS is not necessarily a 5 V amplifier supply. RUN is an active-low reset input. The onboard Pico 2 W LED uses wireless-chip WL_GPIO0 and has no header connection. These details and external-supply power-path requirements are defined in the [Raspberry Pi Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf). Pico GND pins are 3, 8, 13, 18, 23, 28, and 38; AGND is pin 33. The copied circuit has no present need for 3V3_OUT or ADC_VREF.

Two carried-over circuit details also need review before final wiring and layout:

- **Output net names:** the actual copied netlist uses `FINAL_OUT` between C51 pin 2 and J52 pins 2/3 (unfiltered LPF input), and `TX_OUT` between J52 pins 6/7 and J51 pin 1 (filtered output). This is reversed relative to the source README's description. Decide whether to swap those labels; the import preserves the source electrical connections.
- **R41 isolation:** both R41 pads are on `SW_5V`, with the source's explicit jumper-pin group retained. If R41 must provide removable supply isolation, split the rails and prevent a copper bypass. The current same-net connection does not enforce isolation.

J21 is a manual bias-setting bypass, not a Pico bus signal: pin 1 is `AMP_5V_IN`, and pin 2 is `SW_5V`. It normally stays open. A shunt bypasses U21 regardless of `AMP_EN`; stop RF drive, start RV31 at minimum gate voltage, and remove the shunt after bias adjustment. Q41 pins 1/2/3 remain drain/gate/source, and RV31 pin 2 remains the wiper.

## Develop this shield

1. Open [WsprryPico GPIO Shield.kicad_pro](WsprryPico%20GPIO%20Shield.kicad_pro) in KiCad.
2. Resolve the connection table above, wire the selected Pico pins, and mark unused pins with no-connect flags. Run ERC before synchronizing the board.
3. Run **Tools → Update PCB from Schematic…**, place the components, route the board, add and fill copper zones, and run ERC and DRC.

This project has independent copies of its design files and libraries. It has no symlinks or library dependencies on the source template, Wattmeter Shield, or Zero BS170 project. Changes in those projects do not update this shield. PCB placement must resolve component fit, LPF orientation and overhang, socket mating height, and access to RV31, J21, and SW11 within the Pico shield geometry.

## Mechanical interface

| Item | Geometry |
| --- | --- |
| Header rows | Two 1×20 rows, 2.54 mm pitch, 17.78 mm between row centers |
| Pads | 1.508 × 1.508 mm square pads; 1.00 mm drills |
| Board | 53.33 × 22.85 mm outer envelope; 1.6 mm thickness; two copper layers |
| Outer corners | Nominal 1 mm radius |
| Antenna opening | 14 mm wide × 9 mm deep, open to the right edge |
| Keepout | Both copper layers; tracks, vias, pads, copper pours, and footprints prohibited |

U11 is the combined 40-pad header footprint. It and the nine board-level outline segments/arcs are locked. Three `Edge.Cuts` segments inside U11 form the antenna notch and join the board perimeter. Keep these endpoints joined when resizing the shield; moving U11 alone breaks the outline. The imported J52 footprint uses 33.020 mm between its LPF socket-row centers; its fit on this smaller shield has not been established.

## Header previews and manufacturing outputs

U11 represents the electrical Pico interface and is excluded from the purchasing BOM and placement output. Its footprint carries two local female 1×20, 2.54 mm socket models aligned with the pad rows, so both headers appear in KiCad's 3D viewer and rendered previews. The models do not add components to manufacturing outputs.

J11 and J12 are pinless, schematic-only socket descriptions with optional purchasing fields. They are excluded from the BOM, board, and placement output by default and create no additional PCB footprints. The schematic's **Shield purchasing BOM** preset respects these exclusions and the copied circuit's assembly exclusions.

The import preserves hand-fitting exclusions for J13, J21, J51, J52, Q41, and L41. They remain electrical board components but are excluded from automated BOM and placement output. The 19 other imported components retain their supplier fields and BOM eligibility. The PCB still contains only the excluded starter interface, so it cannot yet produce the circuit's assembly BOM or placement output. Synchronize and lay out the circuit before preparing any order package. The Zero BS170's order-ready status does not apply to this shield.

The socket models are generic visual aids, not a selected manufacturer's part or a fit qualification. Manufacturer and MPN fields are blank. Select compatible lead dimensions, body width, and mating height before assembly. If this shield requires socket procurement, explicitly enable J11/J12 BOM inclusion and enter the selected part on both symbols. Configure manufacturing outputs to match the parts the factory will fit.

## Local libraries and files

Both library tables use the `wsprrypico-gpio-shield` nickname and `${KIPRJMOD}` paths. All schematic library IDs and footprint assignments use that nickname. Local model references use `${KIPRJMOD}/wsprrypico-gpio-shield.3dshapes/`. The imported standard passive and SOT-23-6 footprints retain their installed `${KICAD10_3DMODEL_DIR}` model references; KiCad's standard 3D model libraries are needed for those previews.

- [Project settings](WsprryPico%20GPIO%20Shield.kicad_pro): rules, defaults, and BOM preset.
- [Schematic](WsprryPico%20GPIO%20Shield.kicad_sch): U11 interface, J11/J12 purchasing descriptions, and grouped BS170 circuit with open Pico bus connections.
- [PCB](WsprryPico%20GPIO%20Shield.kicad_pcb): header interface, outline, and antenna keepout.
- [Symbol library](wsprrypico-gpio-shield.kicad_sym): Pico interface, socket descriptions, and copied circuit definitions.
- [Header footprint](wsprrypico-gpio-shield.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod).
- [Local 3D models and third-party terms](wsprrypico-gpio-shield.3dshapes/README.md).
- [KiCad library license](KICAD-LIBRARY-LICENSE.md) and [source asset provenance](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md).
- [Symbol table](sym-lib-table) and [footprint table](fp-lib-table): local library registration.
- [License](LICENSE.md): preserved from the source template.

The three project design files and their internal project/sheet names use `WsprryPico GPIO Shield`. The copied libraries use the distinct `wsprrypico-gpio-shield` name. Template-selector metadata, local preferences, locks, backups, and generated outputs were not copied.

Git ignores `jlcpcb/`, generated exports, fabrication packages, backups, caches, and editor state. Design sources, local libraries, and documentation belong in Git.

## Validation and limits

Checks on 2026-10-05 used **KiCad 10.0.6**. The schematic and starter PCB were visually inspected in the native editors, and the exported schematic was also checked. Netlist comparison confirmed that every copied component retains the source pin connections after reference/label substitution and removal of the Pi host connections; all 40 U11 pins remain singleton, isolated nets.

| Check | Result / remaining work |
| --- | --- |
| ERC before import | 52 errors: 40 unconnected Pico pins, 10 undriven power inputs, two undriven signal inputs |
| ERC after import | 54 errors and four warnings: the same 40 open Pico pins and two signal inputs, 12 undriven power inputs, and four isolated host-boundary labels |
| Physical PCB DRC | Zero violations and zero unconnected items on the starter PCB, which has no imported circuit footprints or routing |
| Native schematic-parity DRC | 25 missing-footprint findings, one for each imported circuit component; no header net-name mismatches remain |
| CLI schematic-parity DRC | Aborted with exit 134; native checking supplied the completed parity result above |
| Preservation | Source Zero BS170 files unchanged; target PCB differs only in U1-to-U11 reference and isolated pad-net names; original header footprint, models, project settings, and library tables unchanged |

ERC still ignores the existing `footprint_filter`, `four_way_junction`, `simulation_model_issue`, and `single_global_label` checks. No thresholds, exclusions, or no-connect flags were changed to suppress the open-interface findings. The completed native PCB DRC reported no ignored tests. Resolve the supply, ground, and GPIO choices before clearing ERC; synchronize and route the imported components before claiming schematic/PCB parity.

At the earlier independent-starter checkpoint, the **Shield purchasing BOM** and CSV placement exports contained no component rows, and a 3D render showed both socket rows. Those records describe the starter before the circuit import. Current component pin/pad mapping and local-library/model resolution were checked against the copied assets. Reports and disposable exports are under the ignored `generated/bs170-import/` directory.

Run ERC and DRC after developing the circuit or changing the mechanical interface. This shield has no verified physical assembly, socket fit, fabrication, or RF performance.

## Sources and license

The Pico interface derives from the Pico 2W Shield Template and Pico 2W Wattmeter Shield in [WsprryPi PCB Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs). The amplifier circuit and its required local assets were copied from the repository's Zero BS170 project. Repository-owned work retains [LICENSE.md](LICENSE.md); imported KiCad assets retain the [KiCad library license and exception](KICAD-LIBRARY-LICENSE.md). The SMA footprint derives from the public-domain Adafruit Eagle Library; its symbol derives from KiCad. Supplier model terms and original MIT visualization models are documented in the [3D asset notes](wsprrypico-gpio-shield.3dshapes/README.md).

- [KiCad 10 project templates](https://docs.kicad.org/10.0/en/kicad/kicad.html#project_templates)
- [Raspberry Pi Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf)
