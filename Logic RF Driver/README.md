# Logic RF Driver

This two-layer board takes a raw 3.3 V CMOS clock and drives it through two paralleled SN74LVC2T45DCUR outputs powered from 5 V. Its target range is 137 kHz–145 MHz. Connect the output to a filter for the selected band, then to a 50-ohm load. The board has no RF power, thermal, emissions, or source-compatibility measurements.

Open [the KiCad project](Logic%20RF%20Driver.kicad_pro) for the schematic and PCB. The project includes the [symbols, footprints, and STEP models](libraries/README.md); their paths use `${KIPRJMOD}`.

## Connections

| Connector | Pin | Connection |
| --- | --- | --- |
| J1, CLOCK IN | Center | Raw 0–3.3 V CMOS clock from a Pico GPIO, Pi GPIO, or Si5351 CLK output |
| J1 | Shield | Ground |
| J2, POWER | 1 | +3.3 V for VCCA and DIR |
| J2 | 2 | +5 V for VCCB |
| J2 | 3 | Common ground |
| J3, RF TO LPF | Center | RF output through C4 to the selected-band filter and load |
| J3 | Shield | Ground |

Connect one clock source at a time, with a common ground for the source, supplies, board, filter, and load. J1 has no 50-ohm termination. The source must supply the desired frequency at valid logic levels; not every Pico, Pi, or Si5351 configuration can generate 145 MHz.

## Circuit

A1 and A2 share the clock input. B1 and B2 connect directly together, with no output resistors. DIR is tied to +3.3 V for A-to-B translation. R1 pulls the input low when it is undriven. C1 bypasses the 3.3 V supply, C2/C3 bypass the 5 V supply, and C4 blocks DC at the output.

The indicator samples `RF_RAW` on the U1 side of C4, through R2 (220 ohms) and C5 (10 nF). D1 is a BAT54S detector, Q1 is an MMBT3904, and D2 is the LED fed from +3.3 V through R4 (680 ohms). R3 is 1 Mohm, and C6 is 10 nF. C6 sits beside D1, with a 1.46 mm cathode connection and a nearby ground via. It stores rectified charge for Q1, while R3 provides a discharge path. The passive and LED footprints are 0603; D1 and Q1 use SOT-23. The detector loads U1's output stage. See the [input-loading study](INPUT-LOADING.md) for the R2 trade-off; its effect on RF output and total supply current is unmeasured and not included in the comparison model.

[TI's datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf) allows tying two outputs together for stronger drive. The device's electrical and thermal limits apply. Output current sharing and RF power across the target range are unmeasured on this board.

### Why the input is DC-coupled and C4 is on the output

The input needs a ground-referenced LOW and HIGH, so J1 is DC-coupled to A1/A2. R1 keeps it low if the clock source is disconnected or has high impedance. Putting a capacitor ahead of this pull-down removes the DC reference and can produce negative excursions or an unreliable HIGH. An AC-coupled clock or sine-wave source needs a separate bias and conditioning circuit.

The output capacitor has a different job: C4 removes the waveform's average voltage at the filter input. A 0–5 V waveform at 50% duty cycle has a nominal 2.5 V average, provided the downstream circuit gives it a DC return. The signal conductor is DC-blocked; the grounds are connected. See the [C4 impedance and bias analysis](C4-SELECTION.md).

## Parts and assembly

| References | Selected part | Specification | JLCPCB class |
| --- | --- | --- | --- |
| U1 | SN74LVC2T45DCUR / C15741 | VSSOP-8; dual-supply translator | Extended |
| R1 | 0603WAF1002T5E / C25804 | 10 kohms; 1%; 0.1 W; 0603 | Basic |
| R2 | 0603WAF2200T5E / C22962 | 220 ohms; 1%; 0.1 W; 0603 | Basic |
| R3 | 0603WAF1004T5E / C22935 | 1 Mohm; 1%; 0.1 W; 0603 | Basic |
| R4/R5 | 0603WAF6800T5E / C23228 | 680 ohms; 1%; 0.1 W; 0603 | Basic |
| C1/C2 | CC0603KRX7R9BB104 / C14663 | 100 nF; 10%; 50 V; X7R; 0603 | Basic |
| C3/C4 | CL10A105KB8NNNC / C15849 | 1 uF; 10%; 50 V; X5R; 0603 | Basic |
| C5/C6 | 0603B103K500NT / C57112 | 10 nF; 10%; 50 V; X7R; 0603 | Basic |
| D1 | BAT54S,215 / C47546 | 30 V; 200 mA; dual series Schottky; SOT-23 | Extended |
| D2/D3 | KT-0603R / C2286 | Red LED; 0603 | Basic |
| Q1 | MMBT3904(RANGE:100-300) / C20526 | NPN; 40 V; 200 mA; SOT-23 | Basic |

The sixteen-component [BOM](BOM.csv) covers U1, Q1, R1-R5, C1-C6, and D1-D3. Every assembly position has a selected ordering code. D2 indicates driver-output activity, and D3 indicates the 3.3 V supply through its own R5. J1/J2/J3 are visible in the schematic, board, and rendering, but excluded from the BOM and not marked DNP. J1/J3 use the Amphenol 132289 edge-mount SMA footprint. J2 is a 1x3 header with 2.54 mm pitch. See [ordering codes and supplier information](LCSC-PARTS.md).

## Layout and checks

The board is 27.08 × 16.00 mm, with 1 mm corner radii and a nominal thickness of 1.57 mm. It has two copper layers, 103 track segments (91 front and 12 back), and 31 ground vias. Both layers have a filled ground zone, and stitching runs along both sides of the short RF paths. The placement grid is 0.25 mm, though several component anchors sit off it. See [layout details](PCB-LAYOUT.md).

![PCB assembly](docs/pcb-preview.png)

The configured CAD checks report zero ERC violations, zero board-rule violations, zero unconnected items, and zero schematic-parity issues. All nineteen footprints are placed within the board arrangement, including the edge-mount connectors, and all connections are routed. [Validation](VALIDATION.md) lists the checks and ignored categories.

## Project text variables

The PCB Editor exposes these settings under **File → Board Setup → Text & Graphics → Text Variables**. Schematic Setup also includes these definitions. The project file holds 16 variables for title blocks, headings, supply notes, and board labels; they are not machine-wide environment variables.

Edit the project file externally with the KiCad editors and the project closed. KiCad keeps settings in memory and can overwrite an external edit when it closes. Reopen the project to load the file, and check label fit and DRC for the resulting labels. See the [KiCad text-variable reference](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#text_variables).

## Research and limitations

The [SN74LVC2T45 versus BS170 comparison](COMPARISON.md) predicts about 84.32 mW at 137 kHz and 83.03 mW at 145 MHz for the paralleled logic stage, excluding filter loss. It uses a behavioral logic model, ideal supplies, and a bias-dependent C4 fit. These figures are simulated, not measured, and exclude the detector branch. The separate [detector study](INPUT-LOADING.md) gives about 82.48 mW at 137 kHz and 79.89 mW at 145 MHz with R2 at 220 ohms, using surrogate semiconductor and LED models. The ideal-choke BS170 results are diagnostic only because they fail numerical robustness checks. See [model scope](MODEL-SCOPE.md).

Project-owned work follows the repository [MIT license](../LICENSE.md). Library assets retain the [KiCad library license and exception](libraries/KICAD-LIBRARY-LICENSE.md). Manufacturer data retain their own terms.
