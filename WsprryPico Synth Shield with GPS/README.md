# WsprryPico Synth Shield with GPS

A two-layer Pico 2 W shield with a **25 MHz TCXO, Si5351A synthesizer, switched BS170 RF amplifier, onboard GNSS receiver, pushbutton and LED**. The schematic and PCB are implemented in KiCad 10 with independent project-local libraries. The intended transmitter range is **2200 m through 10 m**, with a band-appropriate external low-pass filter after the SMA output.

The hardware provides synthesizer control, GNSS UART/PPS and clock-counting connections. WsprryPico's Si5351 transmission engine remains a [deferred firmware feature](https://github.com/WsprryPi/WsprryPico/blob/devel/docs/development/si5351-transmission-backlog.md). Band-specific output power, spectral performance, calibration accuracy and thermal margins require assembled-board measurements. See [current validation status](VALIDATION.md) before fabrication.

## Hardware

| Series | Circuit | Components |
| --- | --- | --- |
| 10 | Pico interface, button and LED | U11, J11/J12, SW11, D11, R11 |
| 20 | Shared 3.3 V clock/GNSS regulator | U21, C21/C22 |
| 30 | Switched amplifier supply | U31, C31–C33, R31/R32 |
| 40 | 25 MHz TCXO reference | Y41, C41–C43 |
| 50 | Si5351A synthesizer | U51, C51/C52, R51–R53 |
| 60 | RF amplifier, bias measurement and SMA output | Q61, L61, RV61, R61–R63, C61–C65, TP61/TP62, J61 |
| 70 | GNSS receiver and antenna interface | U71, J71, L71, R71–R73, C71–C73 |

**Reference and synthesizer:** Y41 is KDS **1XTW25000MAA / C253672**, a 25 MHz DSB321SDN TCXO. Its output couples through C42, 1 nF C0G, to U51 XA; XB is unconnected. U51 is **SI5351A-B-GTR / C504891** in MSOP-10. CLK0 drives the amplifier, and CLK2 feeds the Pico through R53, 33 Ω. SDA/SCL have 4.7 kΩ pull-ups to `SYNTH_3V3`.

**Power:** Pico physical pin 40, USB VBUS, supplies both U21 and U31. U21, **TPS7A2033PDBVR / C2862740**, produces `SYNTH_3V3` for the TCXO, Si5351A, I²C pull-ups and GNSS VCC/VBAT. Its EN pin is tied to IN. U31, **TPS22918DBVR / C131941**, independently switches VBUS onto `AMP_5V_SW` for the amplifier's drain and bias circuits. R31, 100 kΩ, holds `AMP_EN` low by default. The combined LDO load includes the receiver and active antenna; supply noise, startup and temperature must be checked with the selected antenna.

**RF amplifier:** Q61 is a hand-fitted **BS170 / C111691**. C61, 100 nF C0G, AC-couples the synthesizer through R61, 22 Ω, to the gate. RV61 provides adjustable bias through R62, 4.7 kΩ; R63, 100 kΩ, returns the gate to ground. L61 is **TDK VLS6045EX-331M / C501933**, a 330 µH factory SMT drain choke. C64, 100 nF C0G, DC-blocks the output to J61's **Adafruit 1865 board-edge SMA**. Connect the appropriate external LPF before an antenna; J61 carries the unfiltered amplifier output.

**GNSS:** U71 is **ATGM336H-5N31 / C90770**, with UART and PPS connections to the Pico. VCC pin 8 and VBAT pin 6 share `SYNTH_3V3`; C71, 10 µF, and C72/C73, 100 nF, provide local bypassing. J71 is **Hirose U.FL-R-SMT-1(10) / C88373**, with L71, **LQW18AN47NG00D / C98076**, providing active-antenna DC bias. Use a compatible U.FL/MHF1 pigtail and antenna. The PPS and CLK2 connections support frequency measurement in firmware; PPS alone does not measure the RF reference.

**Controls:** SW11 connects GP0 to ground when pressed and requires the Pico's internal pull-up and software debounce. D11 is an active-high red LED driven by GP1 through R11, 1 kΩ. Button action and indicator behavior are firmware functions.

## Pico pin contract

Configure firmware with GPIO numbers; the physical-pin column identifies the header pad.

| Function | Pico GPIO | Physical pin | Connection |
| --- | --- | --- | --- |
| Button, active low | GP0 | 1 | SW11 to GND; enable internal pull-up |
| LED, active high | GP1 | 2 | R11 to D11 anode |
| CLK2 feedback | GP3 | 5 | U51 pin 6 through R53 |
| I²C0 SDA | GP4 | 6 | U51 pin 5 |
| I²C0 SCL | GP5 | 7 | U51 pin 4 |
| UART0 TX to receiver RX | GP12 | 16 | R71 to U71 pin 3 |
| UART0 RX from receiver TX | GP13 | 17 | U71 pin 2 |
| GNSS PPS | GP16 | 21 | U71 pin 4 through R73; R72 pull-down |
| Amplifier enable, active high | GP28 | 34 | U31 ON pin 3 |
| Shield input power | — | 40 | USB VBUS |

Reserve these roles exclusively according to the [WsprryPico pin-assignment contract](https://github.com/WsprryPi/WsprryPico/blob/devel/docs/pin-assignment-contract.md). Keep `AMP_EN` low during initialization and configure the synthesizer with its RF output disabled before transmitting. Keep I²C pins undriven, with internal pull-ups disabled, whenever `SYNTH_3V3` is unavailable.

## Adjusting RV61

**Viewed from above its adjustment screw, clockwise reduces bias toward ground; counterclockwise increases it.** RV61 pin 1 connects to `AMP_5V_SW`, pin 2 is the wiper, and pin 3 is GND. The [Bourns TC33 drawing](https://www.bourns.com/docs/product-datasheets/tc33.pdf#page=1) identifies pin 3 as the clockwise end. Turn gently to the stop without forcing it.

Set bias by the onset of idle drain current. BS170 devices have different gate thresholds, so there is no universal gate-voltage setting. The [QRP Labs PA bias study](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html) describes adjustment near the first rise in idle current.

With RF disabled, Q61's drain current creates a DC voltage drop across L61's winding resistance. Measure this with the meter in **DC millivolts**, using its normal **V/Ω and COM sockets**:

| Probe | Measurement point | Net |
| --- | --- | --- |
| Red | L61 pad 1 | `AMP_5V_SW` |
| Black | L61 pad 2, or Q61 pin 1 | `AMP_DRAIN` |

TP61 (+) and TP62 (−) connect to these same two nets for measuring the drop. For gate voltage, measure Q61 pin 2 relative to Q61 pin 3/GND. RV61's wiper voltage is available at C65 pad 1 relative to C65 pad 2/GND.

1. With power off, turn RV61 gently **clockwise to its grounded end** and attach the meter across L61.
2. Connect a band-appropriate external LPF and 50 Ω dummy load. Disable the Si5351 RF output and hold **AMP_EN high** to power the amplifier during adjustment.
3. Power up and record the initial millivolt reading near zero.
4. Turn RV61 slowly **counterclockwise** toward a small, steady drop. **About 5 mV DC across L61 is the recommended conservative starting point**, above the initial meter offset.
5. Recheck after warming. Record the drop and gate voltage; confirm RF output, harmonics and device temperature before selecting the final operating bias. Include 10 m, the highest intended band, in that verification.
6. Return `AMP_EN` low after setup and keep RF disabled until transmission is intentionally enabled.

TDK specifies **1.44 Ω typical / 1.872 Ω maximum DCR** for the [VLS6045EX-331M](https://product.tdk.com/en/search/inductor/inductor/smd/info?part_no=VLS6045EX-331M). Estimate idle current as `I (mA) = DC drop (mV) / winding resistance (Ω)`:

| DC drop across L61 | Current at typical 1.44 Ω DCR |
| --- | --- |
| 5 mV | 3.5 mA |
| 10 mV | 6.9 mA |
| 14.4 mV | 10 mA |

At the specified maximum DCR, 5 mV corresponds to about 2.7 mA. Actual resistance and temperature affect this estimate. **The 5 mV recommendation is an initial bench setting; the assembled shield's optimum is unmeasured.** Keep RF disabled throughout the millivolt measurement because the drain carries RF voltage during transmission.

## Mechanical interface and assembly

The synth components are on **F.Cu**; the Pico and two female socket rows are on **B.Cu**. The board has a **53.33 × 22.85 mm envelope**, 1.6 mm thickness and two copper layers. Its right-edge antenna opening is 14 × 9 mm, with a keepout on both copper layers. The two 1×20 header rows have 2.54 mm pitch and 17.78 mm row spacing; U11 owns their combined 40 electrical pads.

The current PCB has **46 footprints, including 40 SMT assembly positions**. Fit the two Pico sockets, Q61, J61 and J71 by hand. U11, Q61, J61, J71 and the copper test points are excluded from assembly BOM/position output; J11/J12 are schematic-only purchasing descriptions. L61 and L71 are included in SMT assembly. Generate manufacturing BOM and position files from the saved design and verify supplier matching and orientation before ordering.

The front-layer `AMP_DRAIN` ground-pour rule uses **0.15 mm clearance**, with **0.85 mm traces on the main RF route**, as the nominal 50 Ω CPWG starting geometry. Actual impedance depends on the manufactured stackup, mask and pad transitions. Preserve the antenna keepout, ground returns and joined outline endpoints when editing the layout.

## Files and libraries

Open [WsprryPico Synth Shield with GPS.kicad_pro](WsprryPico%20Synth%20Shield%20with%20GPS.kicad_pro) in KiCad 10. The [schematic](WsprryPico%20Synth%20Shield%20with%20GPS.kicad_sch) and [PCB](WsprryPico%20Synth%20Shield%20with%20GPS.kicad_pcb) are the design authority.

- [Parts specifications](PARTS.md) and [engineering inventory](PARTS.csv).
- [LCSC parts collection workbook](LCSC-parts-collection.xlsx): all 48 references, with the saved selections and editable supplier fields. U11 and TP61/TP62 are PCB features; J11/J12 are the two purchased socket rows. Blank datasheet cells need the actual PDF collected.
- [Circuit details](TCXO-SI5351A-DESIGN.md) and [current validation](VALIDATION.md).
- [Symbol provenance](SYMBOL-SOURCES.md), [footprint provenance](LIBRARY-SOURCES.md) and [3D-model inventory](wsprrypico-synth-shield.3dshapes/README.md).
- [Symbol table](sym-lib-table), [footprint table](fp-lib-table) and [custom clearance rules](WsprryPico%20Synth%20Shield%20with%20GPS.kicad_dru).
- [Repository license](LICENSE.md) and [KiCad library terms](KICAD-LIBRARY-LICENSE.md).

The local library contains the **20 used symbol definitions and all 19 assigned footprint types**, plus nine assigned local 3D models. Symbols, footprints and local models use `wsprrypico-synth-shield` and `${KIPRJMOD}` paths. Standard 3D models also require the installed KiCad model library. SW11, RV61, Y41 and L61 have local illustrative previews; physical-fit decisions use manufacturer drawings and actual parts. The circuit follows the QRP Labs TCXO/Si5351A and single-BS170 architecture, with sources and attribution in the circuit and library documents.
