# Quad Logic Buffer Amp

The drawing uses native symbols, 375 wire segments, branch junctions, and common VDD and GND power symbols. J2 and R6 connect the isolated output return to circuit ground as drawn. U1, U2, U4, and U5 use the reference symbol layout and the local TSSOP-20 footprint. The printed supplier code C6930 identifies [TI SN74ACT244PWR](https://www.lcsc.com/product-detail/C6930.html). The connector and RGB LED symbols reproduce the visible terminal functions. Their physical pin assignments and package selections are recorded below.

## Standalone PCB

The [PCB](Quad%20Logic%20Buffer%20Amp.kicad_pcb) uses an estimated **80 × 30 mm** rectangular outline. The finished instrument is specified as 85 × 30 × 45 mm. Page 4 shows the bare board nearly overhead. In a 1,650-pixel-high rendering, the board spans about 670 × 255 pixels and the USB-C shell spans about 75 pixels. Using the selected shell’s 8.94 mm nominal width gives about 80 × 30.4 mm. The roughly 2.6:1 board aspect ratio also matches the chosen outline. Shell variation, perspective, and edge selection limit the estimate to a few millimetres. The photo shows no distinct mounting holes. The PCB has a 1 mm fillet at each corner. [Product specifications](https://turnislandsystems.com/product/tis-1w-digital-1w-power-amplifier/) · [Board photograph and rendering, page 4](https://turnislandsystems.com/wp-content/uploads/2025/09/TIS-1W.pdf#page=4)

## Independent local library

The [symbol table](sym-lib-table) and [footprint table](fp-lib-table) register `logic-buffer-amp`. Every library and assigned 3D-model path uses `${KIPRJMOD}`; neither source project nor an installed KiCad 3D-model library is needed to resolve these copied assets.

- [Symbol library](logic-buffer-amp.kicad_sym): unused template symbols `Raspberry_Pi_Pico_2W` and `Socket_1x20_P2.54mm_BOM`, plus synth-shield `C`, `GND`, `L`, `LED`, `PWR_FLAG`, `R`, and `SMA`, and a standalone `SN74ACT244`.
- [Footprint library](logic-buffer-amp.pretty/): the template header and all synth-shield capacitor, inductor, LED, resistor, and SMA footprint variants listed below, plus the TSSOP-20 buffer footprint.
- [3D models](logic-buffer-amp.3dshapes/README.md): twenty-three local assets, including local copies of the standard models referenced by the synth shield.
- [Sources, terms, and limitations](LIBRARY-SOURCES.md) and [asset manifest](LIBRARY-MANIFEST.json).

| Symbol | Available local footprints |
| --- | --- |
| Raspberry_Pi_Pico_2W | Raspberry_Pi_Pico_2W_Header |
| Socket_1x20_P2.54mm_BOM | None; schematic-only purchasing description |
| C | C_0603_1608Metric, C_0805_2012Metric, C_1206_3216Metric |
| L | L_0603_1608Metric, L_TDK_VLS6045EX_VLS6045AF |
| LED | LED_0603_1608Metric |
| R | R_0603_1608Metric, R_1210_3225Metric |
| SMA | SMA_Adafruit_1865_EdgeMount |
| SN74ACT244 | TSSOP-20_4.4x6.5mm_P0.65mm (TI PW package) |
| GND, PWR_FLAG | None; schematic-only power symbols |

The `SN74ACT244` symbol defaults to the local TSSOP-20 footprint for **SN74ACT244PWR** (TI PW package, 4.4 x 6.5 mm body, 0.65 mm pitch). Its 20 pin names and electrical types were checked against [TI SCAS517G, page 3](https://www.ti.com/lit/ds/symlink/sn74act244.pdf#page=3). The installed KiCad 74HC244 graphics were adapted into a standalone ACT definition, with TI pin naming and datasheet; this is not a simulation model. Other imported symbols retain their source defaults. Assign the appropriate `logic-buffer-amp` footprint when placing a component; generic symbols do not select a particular physical part. The placed schematic assignments and remaining package decisions are listed below.

## Footprints and models

All 65 physical references, including five paired test-point footprints providing ten probe pads, have project-local footprints. The schematic-only power symbols are outside this count. KiCad 10.0.6 netlist verification confirmed that every assigned symbol has the same set of pin numbers as the footprint pads and that every populated package resolves to a local model. The ten bare test pads have no component body. The footprint update preserved net connectivity.

| Assigned references | Local package and model |
| --- | --- |
| C2, all 100 nF capacitors, and all 0603 resistors | See the [passive BOM](#passive-bom) below. |
| U1, U2, U4, U5 | TI PW TSSOP-20, matching KiCad package STEP |
| L1 | Murata BLM18PG121SN1D, 0603 power-line ferrite bead, 120 Ω ±25% at 100 MHz, 2 A through 85 °C, 50 mΩ maximum initial DC resistance. LCSC reported 832,350 units on 2026-11-18. [LCSC C14709](https://www.lcsc.com/product-detail/C14709.html) · [Murata specification](https://pim.murata.com/asset/pim4/ferriteBeadInductortypefilter/ENFA2345_PDF_FERRITEBEADINDUCTORTYPEFILTER) |
| J5, J6 | Adafruit product 1865 female edge-launch SMA for a 1.6 mm board. Both connectors are on hand. Local VRML is an illustrative preview. [Connector specification](https://www.adafruit.com/product/1865) |
| J1, J2 | Vertical 1×2 through-hole pin header on 2.54 mm pitch, with the Zero GPIO BS170 shield’s footprint and STEP model |
| Z6 | Nexperia PESD5V0U1UA,115 in SOD323. Pad 1 is cathode and pad 2 is anode. [Manufacturer pinning](https://assets.nexperia.com/documents/data-sheet/PESD5V0U1UA.pdf) |
| R9 | Panasonic ERJP14J510U, 51 Ω, ±5%, 0.5 W rated, 1210. The permissible continuous input depends on board temperature and derating. [Manufacturer specifications](https://industrial.panasonic.com/tw/products/pt/small-and-high-power-chip-resistors/models/ERJP14J510U) |
| TP22, TP4, TP21, TP10, TP6 | [Paired probe footprint](logic-buffer-amp.pretty/TestPoint_Pair_P2.54mm_Drill0.5mm.kicad_mod) with two of the same pads at a fixed 2.54 mm pitch. Each pair uses one reference. Schematic units A and B correspond to pads 1 and 2. TP22 is USB5V/GND (formerly TP22/TP3), TP4 is D+/D− (formerly TP4/TP5), and TP21 is VDD/GND (formerly TP21/TP19). TP10 is RF input/GND (formerly TP10/TP16). TP6 is RF output/GND_OUT (formerly TP6/TP7). On each RF pair, pad 1 is toward the rear and pad 2 is toward the SMA edge. |
| U6 | TI SN74LVC2G14DCKR, six-pin SC70. Inputs 1/3, outputs 6/4, GND 2, VCC 5. [TI pinout](https://www.ti.com/lit/ds/symlink/sn74lvc2g14.pdf) |
| U88 | TI SN74LVC1G00DCKR, five-pin SC70. Inputs 1/2, GND 3, output 4, VCC 5. [TI pinout](https://www.ti.com/lit/ds/symlink/sn74lvc1g00.pdf) |
| U8, U59 | TI SN74LVC2G04DCKR, six-pin SC70. Inputs 1/3, outputs 6/4, GND 2, VCC 5. [TI pinout](https://www.ti.com/lit/ds/symlink/sn74lvc2g04.pdf) |
| D3 | Diodes Incorporated 1N4148W-7-F in SOD-123. Banded cathode on pad 1, anode on pad 2. [Manufacturer datasheet](https://www.diodes.com/datasheet/download/1N4148W.pdf) |
| Q3 | onsemi MMBT3904LT1G, SOT-23. Base 1, emitter 2, collector 3. [onsemi pinout](https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf) |
| Q6 | Vishay Si2343DS-T1-GE3, SOT-23. Gate 1, source 2, drain 3. [Vishay pinout](https://www.vishay.com/docs/72079/si2343ds.pdf) |

### Passive BOM

Quantities are per board. Both Samsung capacitor types are X7R, ±10%, 50 V DC. C2 is a 1206 bulk capacitor on the 5 V rail after L1. The twelve general-purpose 100 nF positions use Samsung 0603 X7R capacitors. The four bridge coupling capacitors use Walsin 1206 C0G/NP0, ±5%, 50 V DC. The thirteen 0603 resistors are UNI-ROYAL thick film, ±1%, 100 mW, 75 V maximum working voltage, and ±100 ppm/°C. Both power and voltage limits apply. R9 uses the separately specified 0.5 W 1210 input termination. Stock was checked at LCSC on 2026-11-18.

| References | Qty | Value | Manufacturer part number | LCSC | Stock |
| --- | ---: | --- | --- | --- | ---: |
| C2 | 1 | 1 µF | CL31B105KBHNNNE | [C1848](https://www.lcsc.com/product-detail/C1848.html) | 141,650 |
| C5–C7, C9, C14, C15, C21, C22, C34, C127, C128, C160 | 12 | 100 nF | CL10B104KB8NNNC | [C1591](https://www.lcsc.com/product-detail/C1591.html) | 214,300 |
| C10–C13 | 4 | 100 nF | 1206N104J500CT | [C170182](https://www.lcsc.com/product-detail/C170182.html) | 119,055 |
| R2, R3 | 2 | 51 Ω | 0603WAF510JT5E | [C23197](https://www.lcsc.com/product-detail/C23197.html) | 650,600 |
| R37 | 1 | 100 Ω (production marking 01A) | TBD | — | — |
| R30, R31 | 2 | 5.1 kΩ | 0603WAF5101T5E | [C23186](https://www.lcsc.com/product-detail/C23186.html) | 13,449,700 |
| R4, R5, R8, R13, R19, R36 | 6 | 10 kΩ | 0603WAF1002T5E | [C25804](https://www.lcsc.com/product-detail/C25804.html) | 2,287,600 |
| R10 | 1 | 100 kΩ | 0603WAF1003T5E | [C25803](https://www.lcsc.com/product-detail/C25803.html) | 4,436,200 |
| R6 | 1 | 1 MΩ | 0603WAF1004T5E | [C22935](https://www.lcsc.com/product-detail/C22935.html) | 2,087,900 |

C10/C11 and C12/C13 are the two bridge coupling pairs. At 1 W into 50 Ω, the ideal 1:2 transformer reflects 12.5 Ω and carries 0.283 A RMS of load current in its primary. Each matched parallel pair splits that current, giving 0.141 A RMS per capacitor. As a design check, 0.25 A RMS per capacitor allows margin for magnetizing current and unequal sharing. At 1 MHz the two 200 nF pairs contribute about 1.59 Ω of ideal series reactance around the loop.

The bridge uses a Class I C0G dielectric for capacitance stability and low dielectric loss. Verify loaded output and capacitor temperature with these parts at the intended duty cycle across 1–60 MHz.

L1 sits between the protected USB supply at Q6 and the amplifier VDD rail, with C14 on the input side and C2 on the load side. The reference amplifier drew 364–400 mA into 50 Ω at the three documented frequencies (1, 10, and 60 MHz) and 488 mA into 25 Ω at 10 MHz. At 488 mA, the maximum initial DC resistance gives a 24.4 mV drop and 11.9 mW of DC loss. Murata’s typical impedance curve rises from a few ohms at 1 MHz to roughly 40 Ω at 10 MHz and 100 Ω at 60 MHz. This favors isolation of fast driver currents from the USB lead. Actual attenuation depends on DC bias, the capacitors, and the routed board. [Murata impedance curve, page 3](https://datasheet.octopart.com/BLM18PG121SN1D-Murata-datasheet-138707164.pdf#page=3)

The bead body is nominally 1.6 × 0.8 × 0.8 mm. The project’s generic 0603 pattern and Murata’s reflow pattern both have a 0.70 mm inner gap. The project uses a 2.45 mm outer span and 0.95 mm pad width, compared with Murata’s 2.0 mm span and 0.7 mm exposed width. The current rating and DC-drop calculation apply to the bead. The local STEP is a nominal package preview. [Murata mounting drawing, page 9](https://pim.murata.com/asset/pim4/ferriteBeadInductortypefilter/ENFA2345_PDF_FERRITEBEADINDUCTORTYPEFILTER#page=9)

D4 and D5 use CHONGTIAN CT-3210URGBC-P15-2B side-view RGB LEDs. With the lens facing the board edge (local −Y), the four lands read left to right as 1 red, 4 green, 3 blue, and 2 common anode. Both anodes go to VDD. D4 uses blue through R8. The D5 driver connects the two inner cathodes via R15 and R13 as detailed below. The local footprint follows the recommended 3.9 mm land span. The local 3D model represents the nominal body and side lens. LCSC listed 2,450 units on 2026-11-18. [LCSC C52676076](https://www.lcsc.com/product-detail/C52676076.html) · [Manufacturer drawing, PDF page 2](https://datasheet.lcsc.com/datasheet/pdf/34cd5fd2fc904333a2eb28493617a30e.pdf#page=2)

X1 uses the HRO TYPE-C-31-M-12 horizontal top-mount USB-C receptacle. The drawing combines A1/B12 and B1/A12 into two ground lands and A4/B9 and B4/A9 into two VBUS lands. A6/B6 are D+, A7/B7 are D−, A5 is CC1, B5 is CC2, and A8/B8 are the open SBU contacts. All four shell stakes use SH on GND. The two locating holes are unplated. The local footprint uses the paired land names in the schematic and a supplier 3D model. LCSC listed 491,060 units on 2026-11-18. [LCSC C165948](https://www.lcsc.com/product-detail/C165948.html) · [Manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/9e56b777c022540fcce7c7f67825f55e.pdf)

Page 3 specifies SC70 for U8 and U59. In the page 4 prototype photograph, U6 and U88 have the same apparent body size and lead pitch as those adjacent inverters. The corresponding TI DCK packages preserve the schematic pin numbers. The visible size of D3 relative to Q3 and nearby 0603 passives supports SOD-123. The selected ordering codes are implementation choices for this shield.

### L2 flat-mount transformer

The [four-pad footprint](logic-buffer-amp.pretty/Transformer_BN43-1502_Flat_4Lead.kicad_mod) and [VRML model](logic-buffer-amp.3dshapes/Transformer_BN43-1502_Flat_4Lead.wrl) mount the BN43-1502 flat with both bores parallel to the board. Page 3 specifies an isolated 1:2 turns ratio. Page 4 shows two winding ends emerging at each end of the core. The footprint assigns the primary to the negative-Y end and the secondary to the positive-Y end. Left and right below refer to the top view at zero footprint rotation.

| Pad | Center X, Y (mm) | Winding and schematic connection |
| --- | --- | --- |
| 1, square | −3.25, −8.75 | Primary, C12.2 and C13.2, also R37.1 |
| 2 | +3.25, −8.75 | Primary, C10.2 and C11.2 |
| 3 | −3.25, +8.75 | Secondary output, TP6 pad 1 and J5 center contact |
| 4 | +3.25, +8.75 | Secondary return, TP6 pad 2 and J5 shield on GND_OUT |

L2 uses the builder-confirmed BN43-1502 with two primary turns and four secondary turns. A 50 Ω secondary load reflects 12.5 Ω to the bridge. Production wire gauge is unknown. The model shows each turn passing through both bores, with separate winding ends at the measured hole positions.

**Winding and installation**

1. Lay the core flat in its footprint orientation. Call the end facing pads 1 and 2 the primary face and the opposite end the secondary face. Label the **whole bore** beside pads 1 and 3 **A**, and the bore beside pads 2 and 4 **B**. Keep these labels fixed when working from the other end. One turn goes out through one bore and returns through the other.
2. **Primary, pad 1 to pad 2:** Leave a tail at pad 1. Feed the wire through A from the primary face to the secondary face, then back through B to the primary face. Repeat that complete path once. The finish exits B beside pad 2.
3. **Secondary, pad 4 to pad 3:** Leave a tail at pad 4. Feed a fresh wire through B from the secondary face to the primary face, then back through A to the secondary face. Repeat that complete path three more times. The finish exits A beside pad 3. This convention gives pads **1 and 4** the same instantaneous winding polarity. The reference schematic specifies no dots. Keep all four ends separate.
4. Before installation, strip and tin the four tails and check continuity on **1–2** and **3–4**, with an open circuit between windings. Dry-fit the core and dress the leads directly to their holes without scraping the enamel on the ferrite. Solder one lead per pad. Pad 3 feeds the SMA center and pad 4 feeds its isolated return. J2 and R6 provide the board’s intended return connection.
5. For a winding check before installation, apply a small 100 kHz sine wave across 1–2 and measure the actual primary voltage and the unloaded voltage across 4–3. Expect approximately twice the primary voltage, in phase with those probe polarities. On the powered amplifier, use a 50 Ω dummy load and compare loaded output and supply current at 1, 10, 30, and 60 MHz. Inspect low-frequency waveform droop, upper-band roll-off or ringing, and core heating at the intended duty cycle. Use a differential probe for the driven primary. Both primary ends are active.

| Feature | Basis |
| --- | --- |
| Core width × bore-axis length × height | Measured 13.34 × 6.57 × 7.43 mm on the assembled core. |
| Bores | Approximately 3.8 mm diameter on 5.7 mm centers. |
| Lead pattern | Measured 6.5 mm across each pair and 17.5 mm between rows. |
| Through-hole pads | 2.50 mm copper lands with 1.00 mm finished holes. |
| Model and clearance | A 0.25 mm bedding allowance, winding dress and wire diameter are illustrative. The courtyard spans 14.4 × 21 mm. |

## Validation

See the [current validation record](VALIDATION.md) for active findings, exclusions, library checks, and PCB status.

KiCad 10.0.6 exported the single-sheet PDF. Visual review covered the input network, complementary logic paths, four driver packages, transformer, indicator circuit, and USB supply. The two bridge output nets each contain sixteen driver pins and their own pair of coupling capacitors.

The amplifier sheet has two active ERC findings: R12 pin 1 and D5 pin 1 are unconnected. The two intentional output-pair exclusions are separate. Seven no-connect markers identify X1 SBU1/SBU2, U6 pin 4, D4 green/red, and D5 blue/red. Power flags at TP21 pad 1 (VDD) and pad 2 (GND) identify the supplied rails.

The project records two individual ERC exclusions. U8 pins 4 and 6 drive the U1/U2 input bank together. U59 pins 4 and 6 drive the U4/U5 input bank together. In each package both inverter inputs receive the same signal. The exclusions apply only to those output pairs. The project retains its existing ERC rule settings.

## PCB placement review

Viewed from above with the SMA barrels toward the front, J6 is the left input and J5 is the right output. Their centers are 13.0 mm and 66.5 mm from the left edge, giving 53.5 mm spacing. The X1 centerline is 10 mm from the left edge at the rear. Its footprint origin sits 2.50 mm inside the rear edge, giving 1.15 mm nominal shell overhang and 0.55 mm from the nearest shell-stake copper to the edge. The supplier model is registered to both pairs of mounting slots. The mouth-side silkscreen is omitted where it would extend beyond the board. The two side-view LEDs face the front. All 65 footprints are on top with anchors on a 0.1 mm placement grid. TP22 pad 1 (USB5V) sits 2.54 mm directly above pad 2 (GND), beside X1. It probes both X1 VBUS lands at Q6’s drain, before supply protection and filtering.

On the measured 76.3 mm board, taking the USB measurement from the left side edge, the 9 mm wide X1 shell starts 5 mm inboard and centers at 9.50 mm. The 6.5 mm wide SMA bodies have outer clearances of 9.55 mm at J6 (left) and 9.24 mm at J5 (right). Their assembled centerlines are 12.80 mm from the left and 12.49 mm from the right, respectively, giving 51.01 mm center-to-center by the board-edge measurements. The directly measured outside span is 57.11 mm and the inside gap is 44.13 mm. Measured across corresponding connector surfaces, their mean gives 50.62 mm center-to-center and half their difference gives a mean connector width of 6.49 mm. Use 50.62 mm as the measured assembled spacing for panel fit. The board width minus the two outer clearances gives a 57.51 mm span, leaving a 0.40 mm discrepancy. The owner estimates 1.27 mm USB shell overhang at the rear edge (very rough) and approximately 12.5 mm from each side edge to its SMA center (difficult to measure). Centering the directly measured 50.62 mm span on the 76.3 mm board would give 12.84 mm per side. The connector block locates the panel-facing SMA shoulder 1.5 mm forward of the PCB edge. The measured PCB thickness is 1.6 mm, matching the saved board. The two LED lens locations were reported as 26 mm on the input side and 26 mm on the output side. If referenced to their respective side edges, D5 and D4 center at 26.0 and 50.3 mm from the left edge. The LED face-to-edge distance is approximately 0.84 mm, interpreted as an inward setback. The saved lens apex is 0.84 mm inboard (2.10 mm anchor setback minus 1.26 mm lens projection).

The rendering identifies U2/U1 as the rear row and U4/U5 as the front row. The input conditioning is beside J6. The protection and supply parts sit near X1. C10–C13 sit between the drivers and L2, with L2’s secondary leads toward J5. The two jumpers follow the prototype’s input-side and output-side positions. Small-part centers and test points are approximate. The placement accommodates the four selected 1206 bridge capacitors and the local transformer lead spacing. The schematic supplies the component population. The photograph also shows prototype current-monitoring parts and a heatsink. The measured heatsink is 20 × 20 × 10 mm, with the fin tops 11.15 mm above the PCB top. Its nearest fins are 32.1 mm from the left board edge and 2.5 mm from the rear (USB-side) edge. These offsets locate the fins; any base overhang beyond the fins is unmeasured.

The owner measured the finished production PCB at 76.3 × 29.29 mm. L2 is positioned relative to the rear and right edges of the project board. The rear-right hole is 7.15 mm from the right edge and 2.55 mm from the rear edge (measured 2.5 mm). The pattern center is snapped to the 0.1 mm grid at (169.6, 81.3) mm. The ferrite body is offset 0.77 mm left and 0.215 mm toward the rear of the hole-pattern center to reflect the measured face clearances of approximately 4.5 mm right and 7.75 mm rear.


The configured checks report zero board-rule violations, zero schematic-parity differences, and 205 unconnected items. There are no tracks or vias. Confirm board width and depth, SMA spacing, USB-C overhang, LED window alignment, and any enclosure rails or corner relief on the physical unit before routing to a fixed enclosure.

### Production transformer confirmation

In correspondence supplied by the owner on 2026-11-20, the builder confirmed using the smaller BN43-1502 in all production builds, with two primary turns and four secondary turns. The original schematic specifies BN43-202 and the production PCB can accommodate it. The 6.57 mm measured bore-axis length is for the installed production part. Production wire gauge is unconfirmed.

The builder chose 2:4 for approximately 1 W over the intended 160 m through 6 m amateur bands, accepting low-frequency falloff around 1 MHz to retain acceptable performance at 60 MHz. On the same core, 3:6 retains the ideal 12.5 Ω reflected load with a 50 Ω termination and raises nominal primary inductance by a factor of 2.25. The builder identified magnetizing inductance as the main low-frequency limitation and the effective 100 nF series coupling capacitance as a further constraint. Its reactance is 1.59 Ω at 1 MHz. The email describes a design trade-off and provides no measured frequency sweep or specified cutoff attenuation.

## Production board reference designators

The input indicator is D5 (original D2), and the output indicator is D4 (original D1). The production R37 marking 01A establishes 100 Ω. The schematic includes R7, R11, R12, R14, R15, R16, Q4 and Q5. The PCB includes all eight added parts, placed on the 0.1 mm grid from production-photo landmarks. The R7 placement uses a provisional KiCad 1206 fuse pattern. R7 sits slightly toward the rear edge for clearance. R16, R15 and R13 form a left-to-right row at Y = 95.2 mm, with X = 124.3, 126.7 and 129.1 mm respectively. Only the C14 and C128 reference labels were repositioned among existing footprints. KiCad 10.0.6 DRC with schematic parity reported zero rule violations, 205 unconnected items and zero parity issues before routing. The earlier BOM stock figures apply to the original component selection.

In the PCB orientation viewed from above, D5’s pads a/b/c/d correspond to KiCad pads 2/3/4/1 respectively. The bench test lit red with the positive probe on a and negative on d. The production colors for b and c are unverified. The red cathode gave no tone to GND. Its external connection and the precise R12 supply tap are both open in the schematic. R7 is in series before L1, and is represented as a 1206 polymer resettable fuse with a likely 1.0–1.1 A hold current. The exact part and hold rating are unconfirmed. The original Q6-to-VBUS assignment is provisional until the USB-C breakout check. The manufacturer confirms that Q6 provides reverse-polarity protection.


### Unpowered continuity measurements on the assembled board

The owner's completed probe worksheet gives **0.4 Ω across R7** and **0.6 Ω across L1**, both in circuit on the **20 Ω range**. These are displayed two-wire readings including probe and contact resistance. The other entries below are steady-tone observations. Left/right and top/bottom follow the component-side photograph with USB at the rear. On Q4 and Q5, A is upper left, B lower left, and C the single right lead. D5-a through D5-d run left to right.

| Worksheet probe | Terminals giving a tone from that probe |
|---|---|
| R7-L and R7-R (identical results) | USB5V, VDD, Q6-R, L1-L, L1-R, R12-T |
| Q4-A | R11-T, R12-B |
| Q4-B | GND (follow-up test). USB5V, R7-L, R7-R and the worksheet resistor ends were silent. |
| Q4-C | R14-R |
| Q5-A | R14-L |
| Q5-B | R11-B. Follow-up checks to GND, VDD and USB5V were all silent. R11-B also gave no tone to either SMA center contact (J6 input and J5 output). R11-B gave a tone to the physical bottom pin of J1 on the assembled board. In the saved PCB the SMA-side pin is pad 2 (GND) and the USB-side pin is pad 1 (quarter-power control). U88 pin 1 gave a tone to the physical top (USB-side) J1 pin, consistent with the control-pad position in the saved PCB. The physical bottom pin gave a tone directly to the labeled GND hole beside USB-C with J1 open, consistent with pad 2. On repeat with one probe on that same GND hole, both R11-B and Q5-B gave a tone. This supports a shared ground return. Reversed-probe results were not reported. |
| Q5-C | R15-T |
| D5-a | VDD |
| D5-b | R15-B |
| D5-c | R13-B, R16-T |
| R16-B | VDD. GND and Q4-C were silent. Together with R16-T to D5-c, this supports R16 acting as a pull-up from D5-c to VDD. |
| R13-T | Q4-C. No tone to the labeled GND hole. R13 links D5-c to Q4-C on the assembled board. The production update connects this end of R13 to Q4’s collector. |
| D5-d | None of the tested rails or resistor ends |

All other boxes in each corresponding worksheet row were marked silent. R14 links Q4-C to Q5-A, and R15 links Q5-C to D5-b. The measured branches support Q4 and Q5 controlling separate D5 channels through R13 and R15, respectively. The tone results do not identify its trigger or LED color, establish the exact R7 value, or resolve the copper connections on opposite sides of the low-resistance supply components.

The owner traced incoming USB5V to the bottom-right lead of Q6 (called Q6-C by the owner and Q6-R on the worksheet), and from that same lead to R7-L. The observed link from Q6 bottom-right to R7-L is established. The identity of the connector VBUS contact on this path awaits the breakout check. R7-R connects to L1-L. The labeled USB5V pad alone cannot distinguish a connector-side node from a protected supply node. The single top lead of Q6 (Q6-A or Q6-T) has a visible trace running under the X1 USB-C connector. No ground connection was apparent on visual inspection. The owner confirmed Q6-L (bottom-left) connects to GND, consistent with the grounded gate in the schematic. The endpoint of the top trace and the exact part number and rating of R7 remain unverified.

The close-up shows no clearly traceable top-layer connection leaving R12-T. Its routing and via type are unresolved. Direct probe checks from R12-T gave a tone to the labeled USB5V pad and silence to the labeled GND pad. This supports a supply-fed R12/R11 bias network at Q4-A. R7 and L1 also pass the tone, so these checks do not distinguish where R12-T taps the supply path.

The production close-ups show R3 marked 510 and R9 marked 51R0 (both 51 Ω), R11/R13/R15 marked 01C (10 kΩ), R12 marked 563 (56 kΩ), R14 marked 01D (100 kΩ), and R16 marked 473 (47 kΩ). R19 also appears to read 01C. Q4 and Q5 both show a 1AM marking consistent with an MMBT3904 NPN. The corresponding pinout in the worksheet orientation is A = base, B = emitter, C = collector. With the reported connections, R12 and R11 form a supply-voltage divider driving Q4, and R14 connects its collector to the base of Q5. The exact switching voltage and the colors driven through R13 and R15 still require functional evidence. [MMBT3904 marking and pinout](https://www.hygroup.com.tw/upfiles/ADUpload/all_/MMBT3904%20Rev-0.pdf)

R7 reads JH when rotated. Its series position, low measured resistance and this marking support a polymer resettable fuse. Fuzetec uses JH for FSMDH030-24-1206-R, while another 1206 series uses JH for multiple higher-current parts. The schematic and PCB record 1.0–1.1 A as the likely hold current. The exact installed part and hold rating are unconfirmed. Q6 shows a marking beginning P1, with ambiguous trailing characters. The photo does not establish the schematic's exact Q6 part number. [Fuzetec catalog](https://www.fuzetec.com/upload/download/Fuzetec%202023%20PPTC%20Catalog.pdf) · [SMD1206 series marking table](https://xonstorage.z8.web.core.windows.net/pdf/4159225_SMD1206P016TF_link.pdf)
