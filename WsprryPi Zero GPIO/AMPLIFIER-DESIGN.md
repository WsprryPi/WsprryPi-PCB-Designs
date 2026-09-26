# WsprryPi Zero GPIO amplifier design

Status: **not ready for order**. The selected architecture and saved schematic/PCB require two Coilcraft `YA9308-AEC` transformers, which do not have an accepted JLCPCB/LCSC assembly-sourcing path. The board is laid out and routed but has not been fabricated or physically validated.

This is a new Zero-size HAT amplifier effort. Requirements and component choices from the earlier 1 W `WsprryPi-GPIO-Univ` design are reference material only and are not inherited by this board.

## Selected architecture

The design uses one LTC6432-15 differential gain block from a single 5 V rail. It does not require a bipolar converter or another amplifier supply. A 1:2 impedance transformer converts the single-ended GPIO source to the amplifier's 100 ohm differential input, and a second 1:2 transformer converts the 100 ohm differential output back to 50 ohms for the plug-in LPF interface.

The following decisions are selected:

- The amplifier is an LTC6432-15. The local library master, schematic instance, and PCB footprint all select `LTC6432AIUF-15#PBF`, identified by `LCSC_PART` C689344; its order-time availability must still be confirmed.
- The RF amplifier and its power-control circuit operate entirely from the Raspberry Pi 5 V rail.
- GPIO drive-strength settings remain available as coarse experimental selections. They are not calibrated power steps, are not assumed to be monotonic, and do not promise a particular dB change.
- The design target remains 135 kHz through 144 MHz and retains the existing J81/J82 plug-in LPF mechanical keepout.
- The old 1 W design's 2 mA drive requirement, fixed output assumptions, bipolar supply, and THS3491 implementation are not requirements for this design.

The saved signal path is:

```text
GPIO4 or GPIO20 -> J12 selection -> series damping -> DC block
              -> 1:2 transformer -> LTC6432-15
              -> center-tapped 1:2 transformer -> J81/J82 LPF -> RF output
```

## Schematic block organization

The saved schematic is organized by functional decades rather than using a single continuous annotation sequence:

| Series | Function |
| --- | --- |
| 10 | Raspberry Pi HAT interface, GPIO indicator, and socket purchasing item |
| 20 | GPIO source conditioning and input transformer |
| 30 | LTC6432-15 gain block and required capacitors |
| 40 | Center-tapped output transformer and J81/J82 LPF interface |
| 50 | TPS22918 switched 5 V amplifier supply |

Circuit parts within a functional block use a reference number inside its decade, such as `C21`, `R20`, `R21`, and `T22` in the 20-series. The component prefix remains part of the identity, so different types may share a suffix, as `D11`, `R11`, `SW11`, and `J11` do in the 10-series. J1 and the board-only H1 retain special references outside that convention. Connections within a block use conventional wiring and explicit junctions; named nets carry signals and rails between blocks. The schematic and PCB record the implementation, while conducted qualification remains a separate gate.

## Expected RF level

The LTC6432-15 specifies approximately 15.2 dB power gain and a typical 22.5 dBm 1 dB compression point. The two proposed YA9308-AEC transformers are each specified for no more than 0.5 dB insertion loss, so approximately 14 dB of pre-LPF small-signal board gain is a reasonable first estimate. LPF loss and layout loss reduce the delivered gain further.

The first-pass output goal is **+20 dBm (100 mW) after the selected LPF**. **+21 dBm (125 mW)** is a stretch goal, not an acceptance value. Reaching either level over the entire 135 kHz to 144 MHz span depends on GPIO source amplitude and impedance, transformer behavior, LPF insertion loss, layout, and thermal performance. A 250 mW claim would be about +24 dBm, above the amplifier's typical compression point and at the transformer's RF rating, so this architecture must not be represented as a 250 mW design.

The GPIO drive-strength menu changes pad drive behavior, not a calibrated RF attenuator. Each setting therefore needs conducted measurement on every supported Raspberry Pi and frequency range before it can be associated with an output-power range.

## First-pass purchasing BOM

This table is the likely BOM for estimating space and cost, not an order-ready BOM. Parts marked **selected** define the architecture. Parts marked **provisional** remain subject to schematic, layout, and bench qualification. The required `YA9308-AEC` transformers are an order blocker until an accepted procurement path is established or the circuit is redesigned and qualified around a replacement.

| Function | Qty | Likely part or value | State | Notes |
| --- | ---: | --- | --- | --- |
| Differential gain block | 1 | `LTC6432AIUF-15#PBF`, `LCSC_PART` C689344 | Selected | 5 V, nominal 15.2 dB gain, 4 mm × 4 mm 24-QFN with exposed pad; confirm stock at order time. |
| Input and output transformers | 2 | Coilcraft `YA9308-AEC` | **Required; order blocker** | 1:2 impedance ratio, 0.1 MHz to 950 MHz specified bandwidth, 0.5 dB maximum insertion loss, 250 mW RF rating. No normally stocked JLCPCB/LCSC substitute has been qualified. |
| GPIO-side DC block | 1 | TDK `CGA5L3X8R1H105KT0Y0N`, 1 µF, X8R, 50 V, 1206; `LCSC_PART` C342628 | Required | C21, in series between R20 and the R21/T22 primary node. The schematic uses the project-local 1206 footprint; the PCB has not yet been updated. |
| Input DC blocks | 2 | TDK `CGA5L3X8R1H105KT0Y0N`, 1 µF, X8R, 50 V, 1206; `LCSC_PART` C342628 | Required | C30 and C31; X8R follows the amplifier vendor's linearity guidance. The schematic uses the project-local 1206 footprint; the PCB has not yet been updated. |
| Feedback capacitors | 2 | TDK `CGA5L3X8R1H105KT0Y0N`, 1 µF, X8R, 50 V, 1206; `LCSC_PART` C342628 | Required | C36 and C37, one from each FDBK pin to its corresponding OUT pin. The schematic uses the project-local 1206 footprint; the PCB has not yet been updated. |
| Bias-noise filter capacitors | 2 | 1 µF, X8R, 10 V or greater, 0805 | Required | One from each NFILT pin to ground. |
| High-frequency VCC bypass | 1 | 1 nF, 0402 or 0603 | Required | Place immediately at the amplifier VCC connection. |
| VCC bypass | 1 | 100 nF, 0402 or 0603 | Required | Local amplifier bypass. |
| Switched-rail bulk capacitor | 1 | 10 µF, X7R/X8R, 10 V or greater | Provisional | Final value and package depend on power-switch ramp and layout. |
| GPIO series damping | 1 | 22 ohm initial value | Provisional | Tune in the range 0 to 33 ohms from waveform and output measurements. |
| GPIO boot-state pull-down | 1 | 100 kohm | Provisional | Keeps the transformer input quiet while the source GPIO is high impedance. |
| GPIO indicator LED | 1 | `KT-0603W`, red, `LCSC_PART` C2286 | Selected | D11; 0603 LED copied with the existing indicator circuit. |
| GPIO indicator resistor | 1 | 220 ohm, `LCSC_PART` C22962 | Selected | R11; 0603, 100 mW, 1%. |
| Software shutdown-request pushbutton | 1 | Alps Alpine `SKRPANE010`, `LCSC_PART` C470426 | Selected | SW11 momentarily grounds GPIO26. Firmware must provide the pull-up, detect the request, and deassert GPIO23; this is not a failsafe hardware shutdown. |
| Amplifier load switch | 1 | TI `TPS22918DBVR`, `LCSC_PART` C131941 | Provisional | U50 allows a GPIO to remove the amplifier's roughly 850 mW idle load; 5.5 V, 2 A, SOT-23-6. |
| Load-switch input capacitor | 1 | 10 µF, 25 V, X5R, 0805, `LCSC_PART` C15850 | Implemented; validate | C51 is connected from `PI_5V` to ground at U50 input. |
| Load-switch enable pull-down | 1 | 100 kohm | Provisional | Makes amplifier power off the hardware default. |
| Load-switch rise-time capacitor | 1 | 1 nF, 50 V, X7R, 0603, `LCSC_PART` C1588 | Implemented; validate | C53 gives a nominal approximately 2.54 ms rise time at 5 V; verify startup behavior and 5 V droop. |
| Load-switch output-discharge resistor | 1 | Initial value 1 kohm | Provisional | Select or omit after checking shutdown behavior. |
| Load-switch output capacitor | 1 | 1 µF, 50 V, X7R, 0805, `LCSC_PART` C28323 | Implemented; validate | C55 is connected from `SW_5V` to ground. Together with the local U32 bypass capacitors, it keeps the local switched-rail capacitance well below C51's nominal input capacitance. |
| Raspberry Pi socket | 1 | Female 2×20, 2.54 mm | Required | Exact mating height remains a mechanical decision. |
| LPF sockets | 2 | Female 1×4, 2.54 mm | Required | J81 and J82; the plug-in LPF itself is excluded from this BOM. |
| RF output SMA | 1 | Adafruit 1865 or mechanically equivalent part matching the local footprint | Required; hand-soldered | J1 is placed and routed but intentionally excluded from automated BOM and placement output. |

The saved **Amplifier purchasing BOM** export contains 25 BOM units; its single J41 row represents two physical LPF socket pieces, so the export represents 26 physical pieces. J1 and J12 are intentionally excluded from that export. A complete hand-assembly purchasing list must add the required J1 SMA and any J12 hardware the build will use. Repeated passives reduce the automated export to 15 grouped rows. The preset exports supplier ordering codes from the single canonical `LCSC_PART` field; the legacy `LCSC` field is not used.

The center tap is the key BOM simplification. The YA9308-AEC secondary has a center tap, so the output transformer can connect that tap to switched 5 V and directly provide DC bias to both LTC6432-15 output pins. This removes the reference wideband choke-bias network: four inductors and four parallel damping resistors. That dependency also makes the current design not ready for order: the transformer pinout and current rating still require schematic review and physical qualification, and the exact part requires an accepted procurement path before release.

## DNP and omitted parts

The current layout does not reserve footprints for the vendor's optional low-frequency input stability networks. If a later revision adds them, they should be DNP initially because the input is already preceded by a low-frequency transformer; DNP footprints do not belong in the purchasing count.

The first-pass BOM intentionally omits:

- a bipolar or boosted amplifier supply;
- a second RF gain stage;
- a calibrated step attenuator or digital potentiometer;
- current, temperature, or forward-power telemetry;
- the plug-in LPF components; and
- parts inherited solely from the earlier 1 W amplifier.

## Open implementation decisions

The following choices are not locked by selecting the LTC6432-15:

- final transformer acceptance after endpoint gain, return-loss, phase-balance, and distortion measurements;
- exact passive manufacturers, packages, tolerances, and voltage ratings;
- exact connector MPNs;
- the production treatment of U32 exposed-pad thermal vias and stencil apertures;
- startup rail droop, rise time, and power-loss behavior with the implemented `C51 = 10 µF`, `C53 = 1 nF`, and `C55 = 1 µF` network;
- shutdown-request firmware behavior for SW11 and GPIO26;
- output-power acceptance limits per band and per GPIO drive setting; and
- copper area, exposed-pad via pattern, grounding, and thermal acceptance.

## Required qualification

The design remains proposed until an exact board revision and assembly are measured. At minimum, qualification must record gain and delivered power, input/output return loss, harmonics and spurious output after each selected LPF, 5 V current, case or junction-temperature proxy, startup/shutdown behavior, and GPIO-drive-setting behavior at the low and high frequency endpoints and representative amateur bands. Software selection or a successful ERC/DRC run is not RF evidence.

## Sources

- [Analog Devices LTC6432-15 product page](https://www.analog.com/en/products/ltc6432-15.html)
- [Analog Devices LTC6432-15 data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/643215f.pdf)
- [Analog Devices DC2496A evaluation board](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2496a.html)
- [Coilcraft YA9308-AEC product page](https://www.coilcraft.com/en-us/products/transformers/wideband-rf-transformers/smt/ya9308/ya9308-ae/)
- [Coilcraft YA9308 data sheet](https://www.coilcraft.com/getmedia/508634a8-8a9d-4933-83b8-7660d3e9ca71/ya9308.pdf)
- [Texas Instruments TPS22918 product page](https://www.ti.com/product/TPS22918)
