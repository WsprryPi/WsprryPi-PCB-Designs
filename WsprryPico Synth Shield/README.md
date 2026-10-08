# WsprryPico Synth Shield

An independent KiCad 10 project copied from the [Pico 2W Shield Template](../Pico%202W%20Shield%20Template/README.md). It retains the Pico interface, board outline, antenna notch and local socket models. The schematic now contains **54 component symbols in eight decade-series boxes**, following the GPIO Pico board's style. The selected circuit is specified in the [TCXO and Si5351A design notes](TCXO-SI5351A-DESIGN.md); schematic wiring is in progress and PCB implementation remains pending. See [symbol sources and placement](SYMBOL-SOURCES.md).

The preferred circuit precedent is Hans Summers' QRP Labs design. The selected reference is **KDS/Daishinku 1XTW25000MAA, DSB321SDN, 25 MHz, LCSC C253672**, fitted directly on the shield as locked by the user on 2026-10-06. Direct 3.3 V I²C with **two 4.7 kΩ, ±1% prototype pull-ups to `SYNTH_3V3`**, and a dedicated low-noise **TI TPS7A2033PDBVR, SOT-23-5, LCSC C2862740** regulator for the TCXO and Si5351A are also locked. A three-pad selector defaults to pin 40 / VBUS; cutting its copper link and bridging the alternate gap selects pin 39 / VSYS. Only one connection may be closed. **Regulator EN pin 3 connects to its own IN pin 1**, keeping the TCXO and Si5351A powered whenever the selected supply is available. This always-on clock supply replaces the earlier `SYNTH_EN` GPIO and external 100 kΩ EN pull-down requirement; neither is retained. Keep independent `AMP_EN` amplifier control and use Si5351 I²C commands to enable/disable the RF output while preserving CLK2 calibration between transmissions. The I²C pins must be undriven with internal pull-ups disabled whenever the synth supply is unavailable. Prototype component values, dielectrics, ratings, supplier codes and local footprints are recorded in [PARTS.md](PARTS.md). Choke sourcing, bus-speed/rise-time validation and button/LED behavior remain open. The notes distinguish documented QRP Labs circuitry from proposed component values and preserve the compensation caveat.

**Target bands and 2 m WSPR locked 2026-10-06:** cover the amateur bands from **2200 m through 2 m**, including **WSPR on 2 m**, as specified by the user. Retain the selected **25 MHz** reference. Hans' newer U4B documentation provides a 25 MHz TCXO/Si5351A precedent with this band coverage and WSPR; see the [source comparison and implementation requirements](TCXO-SI5351A-DESIGN.md#2-m-wspr-and-the-25-mhz-reference). The older U3S warning is specific to that product and its synthesis implementation, not a reason to reopen the required band or automatically substitute a 27 MHz reference. Validate this shield's synthesis, reference continuity, amplifier and filters across the target range before claiming measured support.

**Synthesizer I²C pins locked 2026-10-06:** use **I²C0**, with **GP4 / Pico physical pin 6 → Si5351A SDA pin 5** and **GP5 / Pico physical pin 7 → Si5351A SCL pin 4**, as accepted by the user. Reserve the pair together for this bus, following the [firmware pin-assignment contract](https://github.com/WsprryPi/WsprryPico/blob/devel/docs/pin-assignment-contract.md). Control GPIOs are locked below; bus speed remains open. The Si5351 engine is still a future firmware feature; this selection does not wire the starter or enable a firmware adapter.

The completed [QRP module electrical models](../QRP%20Labs%20Modules/README.md) are a separate reference project. They model the photographed MS5351M Rev6 board and TCXO, while this shield retains Si5351A as its target. See the [chat reconciliation and remaining decisions](RECONCILIATION.md) for the distinction between observed hardware, selected parts and proposed values.

The first prototype uses **C22 = 1 nF C0G/NP0** for TCXO-to-XA coupling, **C21 = 10 nF X7R** and **C23 = 100 nF X7R** for local TCXO supply bypassing, **C31/C32 = 100 nF X7R each** at Si5351A VDD/VDDO, and **2.2 µF X7R each** at the regulator input and output. These values are locked by the user on 2026-10-06. The complete capacitor specifications are in [PARTS.md](PARTS.md). Production acceptance remains open: verify effective capacitor values, supply behavior, loaded XA amplitude and startup on the assembled board.

**Onboard amplifier locked 2026-10-06:** reuse the [GPIO shield's BS170 amplifier circuit](../WsprryPico%20GPIO%20Shield/README.md), including its separately controlled active-high `AMP_EN` supply switch, on this shield. Adapt the amplifier input to the Si5351 output. The shared-selector supply choice below resolves the amplifier supply source, and the external-LPF/SMA choice below resolves the output interface. The prototype input network and supplier parts are specified in [PARTS.md](PARTS.md), except for the unresolved FT37-43 choke source. Current budget, Si5351 drive setting and band qualification remain open. The clock regulator's `SYNTH_3V3` rail is reserved for the clock section, not the amplifier's drain/bias supply. Use the reserved amplifier reference mapping in [PARTS.md](PARTS.md#source-amplifier-reference-mapping) to avoid collisions with the clock section. Amplifier symbols are placed in the 50/60-series boxes; their wiring and PCB implementation remain pending.

**Shared power selector locked 2026-10-06:** use the **same three-pad `VBUS / IN / VSYS` selector** for the clock and amplifier branches, as accepted by the user. Its center `IN` pad feeds both the clock LDO input and the amplifier's `AMP_5V_IN` boundary, before the TPS22918 amplifier switch. Default to **Pico pin 40 / VBUS**; the cut-and-solder alternative selects **pin 39 / VSYS** for both branches together. This is the previously selected solder-pad arrangement with a default copper link, not a newly selected removable header jumper. Close only one source connection. USB is the default nominal 5 V source; external VSYS operation is intended for a regulated nominal 5 V feed with the required Pico supply isolation. The clock remains powered while `AMP_EN` independently switches the amplifier. Combined current, voltage drop and supply-noise validation remain open; no separate amplifier power connector is selected.

**RF output interface locked 2026-10-06:** route the amplifier output through a **series DC-blocking capacitor and then the SMA connector**. The **band-appropriate LPF is external**, after the SMA. Omit the GPIO shield's paired LPF sockets from this shield; no onboard filter bank or filter-selector GPIOs are selected. C64 is specified as 100 nF C0G/NP0, 50 V, ±5%, 1206; J61 uses the project's Adafruit 1865 board-edge SMA footprint and local preview model, restored on 2026-10-07; see [connector selection](PARTS.md). RF acceptance remains engineering work across 2200 m through 2 m. The SMA carries the output before external filtering.

**Shield controls locked 2026-10-06:** include **both a pushbutton and an LED on the shield**, as specified by the user. Button and LED parts and support values are specified in [PARTS.md](PARTS.md). Control GPIOs were approved on 2026-10-07: **GP6 / physical pin 9 = AMP_EN**, **GP14 / physical pin 19 = BUTTON_N**, and **GP15 / physical pin 20 = LED_DRIVE**. See the [locked control pin plan](TCXO-SI5351A-DESIGN.md#control-gpio-decisions). Button action and LED behavior remain open. Their inclusion does not reintroduce the GPIO shield's RF-selection header or onboard LPF sockets.

**GPS frequency-calibration hardware locked 2026-10-06:** include **LSI/CSI LS7366R-S, SOIC-14, LCSC C3827808**, with a GPS PPS connection, following the [shared calibration architecture](../design/GPS-FREQUENCY-CALIBRATION.md). Assign Si5351 CLK2 to the counter, targeting a verified one-quarter-reference ratio and a nominal **6.25 MHz** clock for this shield's **25 MHz** reference. The counter captures counts against PPS and the Pico retrieves them over SPI; future firmware applies accepted corrections between transmissions. GPS remains optional for operation. The external receiver interface, Pico 3.3 V supply and UART/SPI/PPS GPIO plan are now locked below. The shield connector and support parts are specified in [PARTS.md](PARTS.md). The exact external receiver accessory, PPS pulse-width behavior, power sequencing, divider configuration and qualification remain implementation work. No calibration circuitry or firmware has been implemented by this selection.

**GPS interface revised 2026-10-07:** use a QLG3 daughterboard with underside male pins mating into J71, a shield-top 1x5 female 2.54 mm socket. Pins 1-5 are 3V3, backup supply tied to 3V3, PPS, receiver serial output and GND. TP71 separately exposes the optional receiver command input. Existing GP0/GP1 UART, GP16 PPS and counter SPI/IRQ assignments remain. The receiver, counter and PPS conditioner use Pico 3V3_OUT. [Current pin plan and fit limits](TCXO-SI5351A-DESIGN.md#gps-configuration-locked).

**Component sourcing requirement, locked 2026-10-06:** select parts available from **LCSC stock**. Record the exact manufacturer ordering code and LCSC C-number for each supplier selection, and recheck inventory when completing the BOM and ordering. A catalog listing without stock does not meet this requirement. The selected 25 MHz KDS reference remains unchanged; no 27 MHz substitute has been selected.

## Component selection

[PARTS.md](PARTS.md) and [PARTS.csv](PARTS.csv) specify 53 assigned inventory references, including values, dielectrics, ratings, ordering codes and local footprints. L61 sourcing and J71 exact mating hardware remain open; the other positions have prototype selections; the FT37-43 choke retains an explicit unresolved LCSC sourcing conflict. [ASSEMBLY-BOM-PREVIEW.csv](ASSEMBLY-BOM-PREVIEW.csv) contains the 44 selected SMT positions only. All headers, the SMA and hand-wound inductors are **no BOM / no positions**, as required by the user; their purchasing information remains in the engineering inventory. BS170 is fitted by hand, and the selector/jumper are copper features. These files are specifications, not production exports from a populated board. [LIBRARY-SOURCES.md](LIBRARY-SOURCES.md) records the 18 added footprints, dimensions, license terms and model gaps.

## Open and develop the design

Open [WsprryPico Synth Shield.kicad_pro](WsprryPico%20Synth%20Shield.kicad_pro). The discrete KDS reference assembly, direct 3.3 V I²C interface with 4.7 kΩ, ±1% prototype pull-ups to `SYNTH_3V3`, TI regulator with always-on clock supply, shared clock/amplifier input selector, onboard BS170 amplifier, DC-blocked SMA output with external LPF, shield button/LED and LS7366R-S GPS calibration hardware with its external receiver interface and GPIO plan are selected. Resolve the choke sourcing conflict and decide button/LED behavior and amplifier power goals/current budget; verify GPS/counter and clock power sequencing, bus speeds and PPS/input conditioning before wiring the Pico. Verify I²C rise time at the selected speed and actual bus loading. Apply the reserved reference mapping when importing the amplifier and adding the counter, and resolve the synthesis and RF acceptance requirements for 2200 m through 2 m. Complete the circuit connections between the placed symbols, run ERC, synchronize the PCB, then place, route and run DRC.

## Base interface corrections

The project carries forward the base-interface conventions used in [WsprryPico GPIO Shield](../WsprryPico%20GPIO%20Shield/README.md):

- U11 is the combined 40-pad electrical Pico interface; J11 and J12 are the two pinless socket purchasing descriptions. The annotation record and isolated PCB net names use the same references.
- Header pads use physical pins 1–40 and match the symbol. The template already contains this correction.
- U11 remains excluded from BOM and placement output. J11/J12 remain pinless schematic purchasing descriptions excluded from BOM, PCB and placement output. The selected sockets are fitted through U11's combined board footprint. All headers, the SMA and hand-wound inductors are excluded from assembly BOM and position files.
- Two local socket models remain aligned to the header rows. Generic geometry does not select or qualify a supplier part.
- The footprint, outline and antenna keepout retain the template geometry and locks.
- Symbols, footprints and models use independent `wsprrypico-synth-shield` libraries and `${KIPRJMOD}` paths. Template metadata, editor state, backups and generated output were omitted.

The current GPIO shield's local Pico header geometry matches the template after normalizing model-directory names. Its amplifier circuit is selected for reuse, but its wiring and PCB layout have not been copied into the synth starter.

## QLG3 module library part

**Single-post variant selected 2026-10-07:** J71 now uses `QLG3_GPS_UndersideHeader_SinglePost`, preserving its saved placement and five electrical connections. The upper post/screw, host hole and associated keepout/courtyard are removed; the lower post and socket remain. The original two-post assets remain available. [Variant details and current validation](qlg3-model/README.md#single-post-variant--selected-2026-10-07).

A reusable [QLG3 symbol, host footprint and 3D assembly](qlg3-model/README.md) now uses Hans Summers' exact board/header/mounting coordinates, standard 2.54 mm connector solids, and photo-based body approximations. J71 now selects this complete assembly footprint, using plain unkeyed 0.1-inch (2.54 mm) socket/header hardware. Its placed footprint will show the full QLG3 receiver in 3D. PCB placement remains pending.

## Mechanical interface

**Primary side revised 2026-10-07:** the synth components belong on **F.Cu**, with the Pico and its two female socket rows on **B.Cu**. The existing starter board was flipped about its horizontal centerline as a complete assembly, including U11, board outline and antenna clearance; all 40 pad numbers and net associations are preserved. Keep U11 on B.Cu when updating the PCB from the schematic. The project-local footprint remains a standard front-side library definition; the PCB instance carries the back-side placement.

| Item | Retained geometry |
| --- | --- |
| Headers | Two 1×20 rows; 2.54 mm pitch; 17.78 mm row-center spacing |
| Pads | 1.508 × 1.508 mm; 1.00 mm drill |
| Board | 53.33 × 22.85 mm envelope; 1.6 mm thick; two copper layers |
| Antenna opening | 14 mm wide × 9 mm deep, open to the right edge |
| Keepout | Both copper layers; tracks, vias, pads, pours and footprints prohibited |

U11 and the nine board-level outline segments/arcs remain locked. Three Edge.Cuts segments in U11 form the notch. Preserve their joined endpoints when changing the outline.

## Files and libraries

- [Project](WsprryPico%20Synth%20Shield.kicad_pro), [schematic](WsprryPico%20Synth%20Shield.kicad_sch), and [PCB](WsprryPico%20Synth%20Shield.kicad_pcb).
- [Symbols](wsprrypico-synth-shield.kicad_sym), [symbol provenance and placement](SYMBOL-SOURCES.md), [header footprint](wsprrypico-synth-shield.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod), and [component footprint provenance](LIBRARY-SOURCES.md).
- [Socket models and provenance](wsprrypico-synth-shield.3dshapes/README.md), [symbol table](sym-lib-table), and [footprint table](fp-lib-table).
- [Circuit notes](TCXO-SI5351A-DESIGN.md), [proposed reference drawing](TCXO-SI5351A-CIRCUIT.svg), and [validation](VALIDATION.md).
- [License](LICENSE.md) and [KiCad library terms](KICAD-LIBRARY-LICENSE.md).

## Validation status

The schematic has 54 non-power component symbols. The latest saved schematic passes KiCad 10.0.6 ERC with **0 errors / 0 warnings**. After the primary-side flip, the starter PCB reports **0 physical DRC violations / 0 unconnected items**. Native schematic-parity checking completes with **75 findings: 51 missing footprints and 24 net conflicts**, because the PCB still contains only U11 and has not been synchronized with the wired schematic. Synchronization, placement and routing remain pending. See [VALIDATION.md](VALIDATION.md) for the current checks and historical checkpoints.

Current QLG3 adaptation: see the [GPS pin plan](TCXO-SI5351A-DESIGN.md#gps-configuration-locked) and latest [validation entry](VALIDATION.md). J71 uses a top-mounted 2.54 mm female socket, with TP71 for optional command input.
