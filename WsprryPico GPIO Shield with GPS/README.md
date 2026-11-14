# WsprryPico GPIO Shield with GPS

A Pico 2 W shield with a **GPIO-driven BS170 RF amplifier, onboard GNSS receiver, pushbutton and LED**. GP2 supplies the RF signal, GP28 switches amplifier power, and the receiver provides position/time data and a PPS timing input.

The transmitter design targets **2200 m through 10 m**. Its SMA output requires a band-appropriate external low-pass filter and 50 Ω load. Output power, harmonics, stability and temperature are unmeasured on an assembled shield.

## Connections and power

Fit the shield to the Pico through the two 1×20 socket rows. The shield components face away from the Pico; the sockets are on the back of the shield. The board is **53.33 × 22.85 mm**, **1.6 mm** thick, with an opening at the Pico antenna end.

USB VBUS on Pico physical pin 40 powers the shield. Powering the Pico through VSYS alone does not supply this shield. The `GNSS_3V3` regulator powers the receiver and its antenna-bias circuit. Amplifier power is separately switched by `AMP_EN`.

Connect a compatible active GNSS antenna through a **U.FL/MHF1** pigtail to J71. J61 is the **SMA RF output**: connect it through the correct external low-pass filter to the load. SW11 is an active-low button; D11 is an active-high red indicator.

## Pico pin contract

Firmware uses GPIO numbers. Physical pins identify the header pads.

| Function | Pico GPIO | Physical pin | Connection |
| --- | --- | --- | --- |
| Button, active low | GP0 | 1 | SW11 to GND; enable internal pull-up |
| LED, active high | GP1 | 2 | R11 to D11 anode |
| RF output to amplifier | GP2 | 4 | `CLOCK_RF` to C61 pin 1 |
| UART0 TX to receiver RX | GP12 | 16 | R71 to U71 pin 3 |
| UART0 RX from receiver TX | GP13 | 17 | U71 pin 2 |
| GNSS PPS | GP16 | 21 | U71 pin 4 through R73; R72 pull-down |
| Amplifier enable, active high | GP28 | 34 | U31 ON pin 3 |
| Shield input power | — | 40 | USB VBUS |

## Firmware operation

Assign the pins according to the [WsprryPico pin contract](https://github.com/WsprryPi/WsprryPico/blob/devel/docs/pin-assignment-contract.md). Enable GP0's internal pull-up and software debounce for the button.

Keep `AMP_EN` low during initialization. Enable the amplifier and allow its rail and bias to settle before starting RF on GP2. Stop GP2 before disabling the amplifier. Leave receiver inputs undriven whenever its supply is unavailable.

PPS supplies a timing input. RF-frequency correction also requires firmware measurement and correction logic, followed by an independent frequency check. PPS wiring alone does not calibrate the RF clock.

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
2. Connect a band-appropriate external LPF and 50 Ω dummy load. Stop the GP2 RF clock and hold **AMP_EN high** to power the amplifier during adjustment.
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

## Assembly

Fit the two Pico sockets, Q61 BS170, J61 SMA and J71 U.FL by hand. The remaining purchased board components are SMT parts. Test points are plated copper features.

Q61 uses **1.00 mm finished plated holes** and **1.50 × 1.60 mm pads at 1.70 mm pitch**. Gently form each outer lead of the selected straight-lead BS170 outward by **0.43 mm**, supporting the lead near the bend. Confirm the fabricator's finished-hole tolerance and check fit with actual parts. Check socket height, Pico engagement, connector mating and cable clearance before soldering.

## Design files

Open [WsprryPico GPIO Shield with GPS.kicad_pro](WsprryPico%20GPIO%20Shield%20with%20GPS.kicad_pro) in KiCad 10. The schematic, PCB and project-local libraries belong together.

- [Circuit and board details](CIRCUIT-DESIGN.md)
- [Parts specifications and assembly exclusions](PARTS.md), [parts inventory](PARTS.csv) and [parts workbook](LCSC-parts-collection.xlsx)
- [CAD checks and engineering acceptance requirements](VALIDATION.md)
- [Symbols](SYMBOL-SOURCES.md), [footprints](LIBRARY-SOURCES.md) and [3D models](wsprrypico-gpio-shield-with-gps.3dshapes/README.md)

Repository-owned work follows [LICENSE.md](LICENSE.md). Imported KiCad assets retain [their library terms](KICAD-LIBRARY-LICENSE.md).
