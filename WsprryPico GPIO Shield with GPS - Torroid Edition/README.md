# WsprryPico GPIO Shield with GPS - Torroid Edition

This independent project implements the [bifilar transformer circuit](design/bifilar-transformer-study/README.md) in its schematic for a 2200 m through 10 m prototype. T61 uses **15 bifilar turns on coated Fair-Rite 5977000621 material 77**, with a 1:2 voltage / 1:4 impedance connection. It was copied from **WsprryPico GPIO Shield with GPS** on **2026-10-20** and has independent local libraries.

**The transformer circuit is now placed and routed on the main PCB.** T61's 25 × 13.5 mm low-support courtyard, with separate 1/4 holes on the +Y face and one shared 2/3 drain hole on the opposite -Y face, stays within the existing outline. All **21 factory SMT positions are on B.Cu**; Q61, T61, J61, D11, SW11 and the two Pico sockets are hand fitted. The 2026-11-13 KiCad 10.0.6 saved-board check reports **9 DRC findings and 12 unconnected items**, with zero schematic/PCB differences; an in-memory zone refill reduces the DRC findings to four but leaves all 12 unconnected items. Physical fit and RF performance remain unmeasured; see [validation](VALIDATION.md).

The latest user-saved schematic removed the GNSS receiver, its regulator and antenna circuit. That saved circuit is preserved in this layout. The project name remains unchanged. GP12, GP13 and GP16 are unconnected in both saved schematic and PCB. There is no receiver connection.

The transmitter design targets **2200 m through 10 m**. Its SMA output requires a band-appropriate external low-pass filter and 50 Ω load. Output power, harmonics, stability and temperature are unmeasured on an assembled shield.

The output uses **C64 and C66–C69, five parallel Walsin 100 nF C0G, 50 V capacitors / C170182**, giving 500 nF total. The bank is one consistently oriented underside row with short 1 mm common RF buses and one shared SMA via; nearby bias parts sit above it. All 21 factory SMT positions remain underneath. RV61 is the stocked **10 kΩ Bourns TC33X-2-103E / C719176**. Corrected socket courtyards and revised C61 placement provide assembly margin; C31/C33 now connect directly to U31 without bypass vias. See [current validation](VALIDATION.md) for measured paths and remaining physical/RF checks.

## Connections and power

Fit the shield to the Pico through the two 1×20 socket rows. T61 and Q61 face away from the Pico. The SMT components and sockets are on the back of the shield, facing the Pico. The board is **53.33 × 22.85 mm**, **1.6 mm** thick, with an opening at the Pico antenna end.

USB VBUS on Pico physical pin 40 powers the shield. Powering the Pico through VSYS alone does not supply this shield. Amplifier power is separately switched by `AMP_EN`.

J61 is the **SMA RF output**: connect it through the correct external low-pass filter to the load. SW11 is an active-low button; D11 is an active-high red indicator.

## Top-side hand-fit controls

**SW11 is Alps Alpine SKHLACA010**, a two-pin through-hole, normally open tactile switch with a 6 × 3.5 mm body, 4.3 mm actuator height and 6.5 mm lead pitch. **D11 is Kingbright WP710A10LID**, a 3 mm low-current red through-hole LED. Both are on top beside the antenna notch, outside the transformer courtyard. SW11 is now at (162.20, 84.10) mm, with 0.735 mm nominal pad-to-socket-body spacing; D11 is at (162.10, 93.40) mm. They are excluded from factory SMT BOM and position outputs.

D11 pad **1 is cathode/K (square)** and pad **2 is anode/A**. A top-silkscreen **+** beside pad 2 identifies the anode before fitting the LED. Match the LED's cathode marking before soldering. R11 remains 1 kΩ; nominal current is about 1.6 mA using 3.3 V and the LED's 1.7 V typical forward voltage. The local LED footprint uses 1.30 mm finished holes and 2.20 mm pads for hand-fitting margin. Follow the manufacturer's soldering instructions; fit both controls after the underside SMT assembly and inspect/trim their leads clear of the Pico. For the prototype, target no more than 1.5 mm finished projection below the shield including solder, subject to acceptable solder joints. Verify that target with the actual header engagement and Pico assembly.

## Assembly orientation and probe polarity

The Pico socket identifies **pin 1 with the only square pad**; pads 2–40 are round. All 40 holes remain circular, 1.00 mm diameter, with unchanged 1.508 mm land size and locations. The USB arrow, USB text, printed 1/40 labels and old pin-1 silkscreen box have been removed from both the PCB and local footprint. Existing U31 pin-1 triangle, Q61 flat-side outline/square drain pad, RV61 pin-1 corner bracket, T61 terminal numbers and D11 anode + are retained.

The two top probe pads now show **+** for TP61 and **−** for TP62, with a **BIAS mV** caption. They measure across R64: **TP61 is AMP_5V_SW and TP62 is AMP_XFMR_FEED; TP62 is not ground**. Use the bias procedure below. The [complete marking audit](VALIDATION.md#assembly-orientation-and-polarity-audit) covers all 29 placements and 14 local footprint types.

## Pico pin contract

Firmware uses GPIO numbers. Physical pins identify the header pads.

| Function | Pico GPIO | Physical pin | Connection |
| --- | --- | --- | --- |
| Button, active low | GP0 | 1 | SW11 to GND; enable internal pull-up |
| LED, active high | GP1 | 2 | R11 to D11 anode |
| RF output to amplifier | GP2 | 4 | `CLOCK_RF` to C61 pin 1 |
| Unused GP12 (formerly GPS_RX) | GP12 | 16 | Unconnected in schematic and PCB; no receiver circuit |
| Unused GP13 (formerly GPS_TX) | GP13 | 17 | Unconnected in schematic and PCB; no receiver circuit |
| Unused GP16 (formerly GPS_PPS) | GP16 | 21 | Unconnected in schematic and PCB; no PPS circuit |
| Amplifier enable, active high | GP28 | 34 | U31 ON pin 3 |
| Shield input power | — | 40 | USB VBUS |

## Firmware operation

Assign the pins according to the [WsprryPico pin contract](https://github.com/WsprryPi/WsprryPico/blob/devel/docs/pin-assignment-contract.md). Enable GP0's internal pull-up and software debounce for the button.

Keep `AMP_EN` low during initialization. Enable the amplifier and allow its rail and bias to settle before starting RF on GP2. Stop GP2 before disabling the amplifier.

This saved revision has no onboard GNSS or PPS source. There is no onboard source for timing or RF-frequency calibration.

## Adjusting RV61

The saved schematic and PCB put TP61 on `AMP_5V_SW` and TP62 on `AMP_XFMR_FEED`, across R64. RV61 is on the underside: arrange safe adjustment access before mating the Pico, or use a suitable temporary assembly fixture. SW11 and D11 are now through-hole parts on top and are hand fitted after factory assembly.

**Viewed from above its adjustment screw, clockwise reduces bias toward ground; counterclockwise increases it.** RV61 pin 1 connects to `AMP_5V_SW`, pin 2 is the wiper, and pin 3 is GND. The [Bourns TC33 drawing](https://www.bourns.com/docs/product-datasheets/tc33.pdf#page=1) identifies pin 3 as the clockwise end. Turn gently to the stop without forcing it.

Set bias by the onset of idle drain current. BS170 devices have different gate thresholds, so there is no universal gate-voltage setting. The [QRP Labs PA bias study](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html) describes adjustment near the first rise in idle current.

With RF disabled and the feed capacitors charged, measure the DC drop across **R64, 1 Ω ±1%**, with the meter in **DC millivolts**, using its normal **V/Ω and COM sockets**. RV61 is upstream of R64, so its divider current is excluded:

| Probe | Measurement point | Net |
| --- | --- | --- |
| Red | R64 pad 1 / TP61 | `AMP_5V_SW` |
| Black | R64 pad 2 / TP62 | `AMP_XFMR_FEED` |

TP61 (+) and TP62 (−) connect to these same two nets for measuring the drop. For gate voltage, measure Q61 pin 2 relative to Q61 pin 3/GND. RV61's wiper voltage is available at C65 pad 1 relative to C65 pad 2/GND.

1. With power off, turn RV61 gently **clockwise to its grounded end** and attach the meter across R64.
2. Connect a band-appropriate external LPF and 50 Ω dummy load. Stop the GP2 RF clock and hold **AMP_EN high** to power the amplifier during adjustment.
3. Power up and record the initial millivolt reading near zero.
4. Turn RV61 slowly **counterclockwise** toward a small, steady drop. **About 3.5 mV DC across R64 is the initial target**, above the initial meter offset, corresponding to approximately **3.5 mA**.
5. Recheck after warming. Record the drop and gate voltage; confirm RF output, harmonics and device temperature before selecting the final operating bias. Include 10 m, the highest intended band, in that verification.
6. Return `AMP_EN` low after setup and keep RF disabled until transmission is intentionally enabled.

For a 1 Ω sense resistor, nominally **1 mV means 1 mA**. Resistor tolerance, temperature and meter error affect accuracy; this avoids estimating current from a variable winding resistance.

| DC drop across R64 | Nominal current |
| --- | --- |
| 3.5 mV | 3.5 mA |
| 5 mV | 5 mA |
| 10 mV | 10 mA |

**The 3.5 mA recommendation is an initial bench setting; the assembled shield's optimum is unmeasured.** Keep RF disabled throughout this millivolt measurement. The original project's 5 mV-across-L61 instruction does not apply to this circuit.

## Assembly

T61 is a hand-wound assembly: its listed MPN purchases the **core only**, with winding wire supplied separately. Fit the two Pico sockets, Q61 BS170, T61, J61 SMA, SW11 button and D11 LED by hand. The PCB has 21 SMT assembly positions, all on the underside. Test points are top-side copper-only probe pads with no drilled holes. T61's [mounting envelope and four-terminal footprint](design/t61-mount/README.md) are defined; the model shows an 8 mm diameter × 1.25 mm support pad and 4 × 6 × 0.5 mm bedding allowance. Actual mounting materials and attachment are builder-selected. CAD checks pass; physical fit and retention remain untested.

Q61 uses **1.00 mm finished plated holes** and **1.50 × 1.60 mm pads at 1.70 mm pitch**. Gently form each outer lead of the selected straight-lead BS170 outward by **0.43 mm**, supporting the lead near the bend. Confirm the fabricator's finished-hole tolerance and check fit with actual parts. Check socket height, Pico engagement, connector mating and cable clearance before soldering.

## Design files

Open [WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pro](WsprryPico%20GPIO%20Shield%20with%20GPS%20-%20Torroid%20Edition.kicad_pro) in KiCad 10. The schematic, PCB and project-local libraries belong together.

- [Circuit and board details](CIRCUIT-DESIGN.md)
- [Transformer wiring, calculation sources and study PDF](design/bifilar-transformer-study/README.md)
- [Parts specifications and assembly exclusions](PARTS.md), [parts inventory](PARTS.csv) and [parts workbook](LCSC-parts-collection.xlsx)
- [CAD checks and engineering acceptance requirements](VALIDATION.md)
- [T61 mounting and dimensioned footprint](design/t61-mount/README.md)
- [Symbols](SYMBOL-SOURCES.md), [footprints](LIBRARY-SOURCES.md) and [3D models](wsprrypico-gpio-shield-with-gps-torroid-edition.3dshapes/README.md)

Repository-owned work follows [LICENSE.md](LICENSE.md). Imported KiCad assets retain [their library terms](KICAD-LIBRARY-LICENSE.md).

Factory SMT stock and small-lot hand-part sources are recorded in [parts availability](PARTS.md#availability-checked-2026-10-20). Core and wire selections are unchanged. T61-SUPPORT and T61-ADHESIVE are builder-choice reminders with no required MPN, supplier, pack quantity or cost. The preview retains its 1.25 mm pad height and 0.5 mm bedding allowance; pad diameter is reduced from 11 to 8 mm. The winding/lead envelope clears the pad by about 0.79 mm and the smaller 4 × 6 mm bedding by at least 1.14 mm in nominal geometry. The 30 mm assembly limit remains. See the [2026-10-21 clearance recheck](MECHANICAL-REVIEW-2026-10-21.md), for the revised lower-turn clearances and fitted-Pico checks.
