# WsprryPico Quad Logic Buffer Amp

The drawing uses native symbols, 375 wire segments, branch junctions, and common VDD and GND power symbols. J2 and R6 connect the isolated output return to circuit ground as drawn. U1, U2, U4, and U5 use the reference symbol layout and the local TSSOP-20 footprint. The printed supplier code C6930 identifies [TI SN74ACT244PWR](https://www.lcsc.com/product-detail/C6930.html). The connector and RGB LED symbols reproduce the visible terminal functions. Their physical pin assignments and package selections are recorded below.

## Pico header provenance

The [Pico Interface sheet](Pico%20Interface.kicad_sch) carries J101. All 40 pins are open pending interface design. Amplifier U1 retains its original reference and TSSOP-20 assignment.

| Source at template revision `87d6268df1dd34253c492e66f261d344bf743a17` | Current instance | Preserved UUID |
| --- | --- | --- |
| [Template schematic](../Pico%202W%20Shield%20Template/Pico%202W%20Shield%20Template.kicad_sch), U1 | Pico Interface / J101 | `4956bacf-ccac-441b-a2fa-51ce082195af` |
| [Template PCB](../Pico%202W%20Shield%20Template/Pico%202W%20Shield%20Template.kicad_pcb), U1 | [Amplifier PCB](WsprryPico%20Quad%20Logic%20Buffer%20Amp.kicad_pcb), J101 | `fee22fe9-065f-4dae-90f5-398417a3d92f` |

The existing locked header remains on B.Cu at (146.81, 90.75) mm, rotated −90°. Its schematic path follows the Pico Interface sheet to the template symbol UUID. Use KiCad’s default UUID matching for future board updates.

## Independent local library

The [symbol table](sym-lib-table) and [footprint table](fp-lib-table) register `wsprrypico-logic-buffer-amp`. Every library and assigned 3D-model path uses `${KIPRJMOD}`; neither source project nor an installed KiCad 3D-model library is needed to resolve these copied assets.

- [Symbol library](wsprrypico-logic-buffer-amp.kicad_sym): template `Raspberry_Pi_Pico_2W` and `Socket_1x20_P2.54mm_BOM`, plus synth-shield `C`, `GND`, `L`, `LED`, `PWR_FLAG`, `R`, and `SMA`, and a standalone `SN74ACT244`.
- [Footprint library](wsprrypico-logic-buffer-amp.pretty/): the template header and all synth-shield capacitor, inductor, LED, resistor, and SMA footprint variants listed below, plus the TSSOP-20 buffer footprint.
- [3D models](wsprrypico-logic-buffer-amp.3dshapes/README.md): twenty-two local assets, including local copies of the standard models referenced by the synth shield.
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

The `SN74ACT244` symbol defaults to the local TSSOP-20 footprint for **SN74ACT244PWR** (TI PW package, 4.4 x 6.5 mm body, 0.65 mm pitch). Its 20 pin names and electrical types were checked against [TI SCAS517G, page 3](https://www.ti.com/lit/ds/symlink/sn74act244.pdf#page=3). The installed KiCad 74HC244 graphics were adapted into a standalone ACT definition, with TI pin naming and datasheet; this is not a simulation model. Other imported symbols retain their source defaults. Assign the appropriate `wsprrypico-logic-buffer-amp` footprint when placing a component; generic symbols do not select a particular physical part. The placed schematic assignments and remaining package decisions are listed below.

## Footprints and models

All 63 physical references, including ten test points and J101, have project-local footprints. The schematic-only power symbols are outside this count. KiCad 10.0.6 netlist verification confirmed that every assigned symbol has the same set of pin numbers as the footprint pads and that every populated package resolves to a local model. The ten bare test pads have no component body. The footprint update preserved net connectivity.

| Assigned references | Local package and model |
| --- | --- |
| C2, all 100 nF capacitors, and all 0603 resistors | See the [passive BOM](#passive-bom) below. |
| U1, U2, U4, U5 | TI PW TSSOP-20, matching KiCad package STEP |
| J101 | Local Pico header with two 1×20 socket STEP model instances |
| L1 | Murata BLM18PG121SN1D, 0603 power-line ferrite bead, 120 Ω ±25% at 100 MHz, 2 A through 85 °C, 50 mΩ maximum initial DC resistance. LCSC reported 832,350 units on 2026-11-18. [LCSC C14709](https://www.lcsc.com/product-detail/C14709.html) · [Murata specification](https://pim.murata.com/asset/pim4/ferriteBeadInductortypefilter/ENFA2345_PDF_FERRITEBEADINDUCTORTYPEFILTER) |
| J5, J6 | Adafruit product 1865 female edge-launch SMA for a 1.6 mm board. Both connectors are on hand. Local VRML is an illustrative preview. [Connector specification](https://www.adafruit.com/product/1865) |
| J1, J2 | Vertical 1×2 through-hole pin header on 2.54 mm pitch, with the Zero GPIO BS170 shield’s footprint and STEP model |
| Z6 | Nexperia PESD5V0U1UA,115 in SOD323. Pad 1 is cathode and pad 2 is anode. [Manufacturer pinning](https://assets.nexperia.com/documents/data-sheet/PESD5V0U1UA.pdf) |
| R9 | Panasonic ERJP14J510U, 51 Ω, ±5%, 0.5 W rated, 1210. The permissible continuous input depends on board temperature and derating. [Manufacturer specifications](https://industrial.panasonic.com/tw/products/pt/small-and-high-power-chip-resistors/models/ERJP14J510U) |
| TP3–TP7, TP10, TP16, TP18, TP19, TP21 | Synth shield’s square 1 mm plated through-hole test pad with 0.5 mm drill. No fitted part or 3D body. |
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
| R1 | 1 | 1 kΩ | 0603WAF1001T5E | [C21190](https://www.lcsc.com/product-detail/C21190.html) | 5,182,100 |
| R30, R31 | 2 | 5.1 kΩ | 0603WAF5101T5E | [C23186](https://www.lcsc.com/product-detail/C23186.html) | 13,449,700 |
| R4, R5, R8, R13, R19, R36 | 6 | 10 kΩ | 0603WAF1002T5E | [C25804](https://www.lcsc.com/product-detail/C25804.html) | 2,287,600 |
| R10 | 1 | 100 kΩ | 0603WAF1003T5E | [C25803](https://www.lcsc.com/product-detail/C25803.html) | 4,436,200 |
| R6 | 1 | 1 MΩ | 0603WAF1004T5E | [C22935](https://www.lcsc.com/product-detail/C22935.html) | 2,087,900 |

C10/C11 and C12/C13 are the two bridge coupling pairs. At 1 W into 50 Ω, the ideal 1:2 transformer reflects 12.5 Ω and carries 0.283 A RMS of load current in its primary. Each matched parallel pair splits that current, giving 0.141 A RMS per capacitor. As a design check, 0.25 A RMS per capacitor allows margin for magnetizing current and unequal sharing. At 1 MHz the two 200 nF pairs contribute about 1.59 Ω of ideal series reactance around the loop.

The bridge uses a Class I C0G dielectric for capacitance stability and low dielectric loss. Verify loaded output and capacitor temperature with these parts at the intended duty cycle across 1–60 MHz.

L1 sits between the protected USB supply at Q6 and the amplifier VDD rail, with C14 on the input side and C2 on the load side. The reference amplifier drew 364–400 mA into 50 Ω at the three documented frequencies (1, 10, and 60 MHz) and 488 mA into 25 Ω at 10 MHz. At 488 mA, the maximum initial DC resistance gives a 24.4 mV drop and 11.9 mW of DC loss. Murata’s typical impedance curve rises from a few ohms at 1 MHz to roughly 40 Ω at 10 MHz and 100 Ω at 60 MHz. This favors isolation of fast driver currents from the USB lead. Actual attenuation depends on DC bias, the capacitors, and the routed board. [Murata impedance curve, page 3](https://datasheet.octopart.com/BLM18PG121SN1D-Murata-datasheet-138707164.pdf#page=3)

The bead body is nominally 1.6 × 0.8 × 0.8 mm. The project’s generic 0603 pattern and Murata’s reflow pattern both have a 0.70 mm inner gap. The project uses a 2.45 mm outer span and 0.95 mm pad width, compared with Murata’s 2.0 mm span and 0.7 mm exposed width. The current rating and DC-drop calculation apply to the bead. The local STEP is a nominal package preview. [Murata mounting drawing, page 9](https://pim.murata.com/asset/pim4/ferriteBeadInductortypefilter/ENFA2345_PDF_FERRITEBEADINDUCTORTYPEFILTER#page=9)

D1 and D2 use CHONGTIAN CT-3210URGBC-P15-2B side-view RGB LEDs. With the lens facing the board edge (local −Y), the four lands read left to right as 1 red, 4 green, 3 blue, and 2 common anode. Both anodes go to VDD. D1 uses blue through R8 and D2 uses green through R13. The local footprint follows the recommended 3.9 mm land span. The local 3D model represents the nominal body and side lens. LCSC listed 2,450 units on 2026-11-18. [LCSC C52676076](https://www.lcsc.com/product-detail/C52676076.html) · [Manufacturer drawing, PDF page 2](https://datasheet.lcsc.com/datasheet/pdf/34cd5fd2fc904333a2eb28493617a30e.pdf#page=2)

X1 uses the HRO TYPE-C-31-M-12 horizontal top-mount USB-C receptacle. The drawing combines A1/B12 and B1/A12 into two ground lands and A4/B9 and B4/A9 into two VBUS lands. A6/B6 are D+, A7/B7 are D−, A5 is CC1, B5 is CC2, and A8/B8 are the open SBU contacts. All four shell stakes use SH on GND. The two locating holes are unplated. The local footprint uses the paired land names in the schematic and a supplier 3D model. LCSC listed 491,060 units on 2026-11-18. [LCSC C165948](https://www.lcsc.com/product-detail/C165948.html) · [Manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/9e56b777c022540fcce7c7f67825f55e.pdf)

Page 3 specifies SC70 for U8 and U59. In the page 4 prototype photograph, U6 and U88 have the same apparent body size and lead pitch as those adjacent inverters. The corresponding TI DCK packages preserve the schematic pin numbers. The visible size of D3 relative to Q3 and nearby 0603 passives supports SOD-123. The selected ordering codes are implementation choices for this shield.

### L2 flat-mount transformer

The [four-pad footprint](wsprrypico-logic-buffer-amp.pretty/Transformer_BN43-202_Flat_4Lead.kicad_mod) and [VRML model](wsprrypico-logic-buffer-amp.3dshapes/Transformer_BN43-202_Flat_4Lead.wrl) mount the BN-43-202 flat with both bores parallel to the board. Page 3 specifies an isolated 1:2 turns ratio. Page 4 shows two winding ends emerging at each end of the core. The footprint assigns the primary to the negative-Y end and the secondary to the positive-Y end. Left and right below refer to the top view at zero footprint rotation.

| Pad | Center X, Y (mm) | Winding and schematic connection |
| --- | --- | --- |
| 1, square | −3, −10 | Primary, C12.2 and C13.2, also R1.1 |
| 2 | +3, −10 | Primary, C10.2 and C11.2 |
| 3 | −3, +10 | Secondary output, TP6 and J5 center contact |
| 4 | +3, +10 | Secondary return, TP7 and J5 shield on GND_OUT |

**First-build winding for 1–60 MHz:** Wind **2 primary turns and 4 secondary turns** on one BN-43-202, using two separate lengths of **26 AWG solid enamelled copper magnet wire** (0.405 mm nominal bare diameter). Use different enamel colors or mark the starts with tape. Allow about **150 mm for the primary and 250 mm for the secondary** as cut lengths with handling allowance. Trim after fitting. The model illustrates the lead exits only.

A 50 Ω secondary load reflects 12.5 Ω to the bridge. Amidon's nominal hole-to-hole inductance factor is 2.89 µH/turn², giving an estimated 11.6 µH primary and 72.6 Ω magnetizing reactance at 1 MHz, about 5.8 times the reflected load. One primary turn gives only 18.2 Ω. Two turns are the shortest winding that meets a design target of five times the load at the low end. As a volt-second check, an ideal symmetric ±5 V primary square wave at 1 MHz applies 2.5 V·µs per half-cycle, giving about 0.216 A peak-to-peak magnetizing current with the estimated inductance. Actual core permeability, coupling capacitors, and bridge losses affect the result. [Amidon BN-43-202 core data](https://www.amidoncorp.com/product_images/Amidon-Tech-Data-Flyer-v19.pdf)

At 1 W into 50 Ω the ideal load currents are 0.141 A RMS secondary and 0.283 A RMS primary, before magnetizing current and losses. The selected wire gives short, low-resistance windings, fits the 1 mm pad holes, and leaves room for six insulated strands in each 3.81 mm bore. At 60 MHz, leakage inductance, winding capacitance, core loss, and exposed lead length matter. Keep the two windings close together through the bores and their end loops close to the ferrite. The 1 MHz calculation sets the turn count. The upper band edge requires a wound-sample test.

**Winding and installation**

1. Lay the core flat in its footprint orientation. Call the end facing pads 1 and 2 the primary face and the opposite end the secondary face. Label the **whole bore** beside pads 1 and 3 **A**, and the bore beside pads 2 and 4 **B**. Keep these labels fixed when working from the other end. One turn goes out through one bore and returns through the other.
2. **Primary, pad 1 to pad 2:** Leave a tail at pad 1. Feed the wire through A from the primary face to the secondary face, then back through B to the primary face. Repeat that complete path once. The finish exits B beside pad 2.
3. **Secondary, pad 4 to pad 3:** Leave a tail at pad 4. Feed a fresh wire through B from the secondary face to the primary face, then back through A to the secondary face. Repeat that complete path three more times. The finish exits A beside pad 3. This convention gives pads **1 and 4** the same instantaneous winding polarity. The reference schematic specifies no dots. Keep all four ends separate.
4. Before installation, strip and tin the four tails and check continuity on **1–2** and **3–4**, with an open circuit between windings. Dry-fit the core and dress the leads directly to their holes without scraping the enamel on the ferrite. Solder one lead per pad. Pad 3 feeds the SMA center and pad 4 feeds its isolated return. J2 and R6 provide the board’s intended return connection.
5. For a winding check before installation, apply a small 100 kHz sine wave across 1–2 and measure the actual primary voltage and the unloaded voltage across 4–3. Expect approximately twice the primary voltage, in phase with those probe polarities. On the powered amplifier, use a 50 Ω dummy load and compare loaded output and supply current at 1, 10, 30, and 60 MHz. Inspect low-frequency waveform droop, upper-band roll-off or ringing, and core heating at the intended duty cycle. Use a differential probe for the driven primary. Both primary ends are active.

| Feature | Basis |
| --- | --- |
| Core width × bore-axis length × height | Amidon nominal 0.525 × 0.550 × 0.295 in, modeled as 13.335 × 13.970 × 7.493 mm. Nominal bore diameter is 3.810 mm. [Amidon Type 1 data](https://www.amidoncorp.com/product_images/Amidon-Tech-Data-Flyer-v19.pdf) |
| Bore center spacing | 5.70 mm from Fair-Rite 2843000202 as a dimensional reference. Its listed axial length is 14.35 ±0.50 mm. The model uses Amidon's nominal length and approximates the outside corner profile. [Fair-Rite drawing](https://fair-rite.com/product/multi-aperture-cores-2843000202/?print=pdf) |
| Lead pattern | Estimated 6.0 mm across each pair and 20.0 mm between rows. Nominal axial clearance from each core face to its pad centers is 3.015 mm. The photograph establishes orientation and lead arrangement only. |
| Through-hole pads | Design choice of 2.50 mm copper lands with 1.00 mm finished holes for individual tinned ends. Check the actual wire and tinned diameter. |
| Model and clearance | Estimated 0.25 mm bedding allowance, nominal assembled height 7.74 mm, illustrative 0.50 mm insulated lead diameter and 0.42 mm stripped diameter, with 1.9 mm of lead below the board surface. Bend profiles are approximate. The 15.0 × 23.5 mm courtyard is a placement allowance. Confirm on a wound sample before fabrication, including retention and clearance to the shield stack. |

## Validation

See the [current validation record](VALIDATION.md) for active findings, exclusions, library checks, and PCB status.

KiCad 10.0.6 exported the two-sheet PDF and XML netlist. Visual review covered the input network, complementary logic paths, four driver packages, transformer, indicator circuit, and USB supply. The two bridge output nets each contain sixteen driver pins and their own pair of coupling capacitors.

The amplifier sheet has zero active ERC findings. The Pico Interface sheet has 52 expected ERC errors while its pins are open, comprising 40 unconnected pins, ten undriven power inputs, and two undriven signal inputs. Seven no-connect markers identify X1 SBU1/SBU2, U6 pin 4, D1 green/red, and D2 blue/red. Power flags at TP21 (VDD) and TP19 (GND) identify the supplied rails.

The project records two individual ERC exclusions. U8 pins 4 and 6 drive the U1/U2 input bank together. U59 pins 4 and 6 drive the U4/U5 input bank together. In each package both inverter inputs receive the same signal. The exclusions apply only to those output pairs. The project retains its existing ERC rule settings.

## PCB placement review

KiCad’s Update PCB from Schematic transferred the 62 amplifier footprints. The board now contains all 63 schematic references. Comparison with the pre-transfer board confirmed the same shield outline, antenna cutout and keepout, locked J101 position, footprint UUID, schematic path, and 40 independent Pico pad nets. KiCad added unit metadata to J101.

Viewed from the top, both SMA barrels face left, X1 faces the upper edge, D1 and D2 face the lower edge, and L2 lies flat on the right. The short edge accommodates both SMA ground forks between the header rows. U1, U2, U4, and U5 form a two-by-two bank on the underside between the Pico sockets. The bridge coupling capacitors C10–C13 sit near the primary winding pads.

The configured checks report 19 board-rule findings, zero schematic-parity issues, and 193 unconnected items. The board contains zero tracks and zero vias. Before routing, check a USB-C plug over the upper header tails and board lip, simultaneous SMA cable access at 8.73 mm connector spacing, and clearance between the mated Pico and underside parts, including L2’s trimmed leads. The fit of a wound L2 and access for probing with cables connected still need a physical check.

### C10–C13 clearance review

With the four 1206 parts at their existing underside positions and rotations, KiCad 10.0.6 reports **19 DRC findings**, zero schematic-parity issues, and 193 unconnected items. These findings remain open until placement resumes.

| Finding | Count | Affected items |
| --- | ---: | --- |
| Copper short | 3 | C10.2 to U4.20 (VDD), C11.1 to C13.2, and C11.2 to C12.1 |
| Copper clearance below 0.2000 mm | 2 | C10.1 to C11.2 measures 0.0025 mm. C10.2 to U1.1 (GND) measures 0.1654 mm. |
| Courtyard overlap | 9 | C10 with C11, U1, and U4. C11 with C12, C13, and R6. C12 with R6 and U8. C13 with U59. |
| Rear solder-mask bridge | 3 | The same three pad pairs listed under copper shorts |
| Rear silkscreen clipped by solder mask | 2 | C11 outline at C10.1 and U1 reference at C12.2 |
