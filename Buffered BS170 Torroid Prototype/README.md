# Buffered BS170 Torroid Prototype

Schematic-only bench prototype for the pinned 18 nH, one-cap design. Open the [KiCad project](Buffered%20BS170%20Torroid%20Prototype.kicad_pro) and its [schematic](Buffered%20BS170%20Torroid%20Prototype.kicad_sch) in KiCad 10. The project provides its own symbols, footprints, and referenced 3D models.

## Shared schematic text

In the Schematic Editor, open **File → Schematic Setup → Project → Text Variables** to edit the sheet title, date, revision, section headings, and notes. Edit the variable value there so its references on the sheet stay linked. KiCad stores these values in the `.kicad_pro` file.

The J11 pinout uses `POWER_INPUT_PINOUT`, the watchdog note uses `CLOCK_WATCHDOG_NOTE`, and the load-switch measurement note uses `DRAIN_CURRENT_NOTE`. The PA sequencing note uses `PA_ENABLE_NOTE`. The notes follow the symbols’ KiCad IDs, so their displayed references and net names update when the symbols are renumbered.

## Schematic reference numbers

The saved schematic groups component numbers by circuit section.

| Section | Range | Main references |
| --- | --- | --- |
| Power and enable input | 10s | J11 |
| 5 V load switch and PA feed | 20s | U21 load switch, R21 current-sense shunt, TP21/TP22 |
| Clock watchdog | 30s | U31 watchdog, R31/C32 timing parts |
| Power and RF detector LEDs | 40s | Q41 detector, D41 power LED, D42 activity LED, D43 detector diode |
| Clock input and gate | 50s | J51 clock input, U51 AND gate |
| Clock buffer | 60s | U61 level shifter, R63 shared gate-drive pull-down |
| Parallel BS170s | 70s | Q71/Q72, R71/R72 gate resistors |
| Winding and RF output | 80s | T81 transformer, L81 trim, C81 coupling capacitor, J81 RF output |

## Connections

| Connector | Pin | Connection |
|---|---:|---|
| J51 | Center | 3.3 V ground-referenced CMOS clock |
| J51 | Shield | Common ground |
| J81 | Center | RF to external per-band C-first LPF and 50 Ω load |
| J81 | Shield | Common ground |
| J11 | 1 | +5 V input to the shared load switch |
| J11 | 2 | +3.3 V for the clock gate, buffer input side, indicators, and watchdog |
| J11 | 3 | Common ground |
| J11 | 4 | Active-high 3.3 V PA supply enable (existing Pi PA_EN GPIO) |

Connect common ground first and hold PA_EN low while applying power. Raise PA_EN with the clock low to bring up `5V_SW`. Wait for TP22 to settle relative to ground before starting the clock. For on/off QRSS, keep PA_EN high through the message and drive J51 low during each space. At the end of the message, lower PA_EN to clear the watchdog and disconnect both 5 V loads. TP21 and TP22 straddle R21. A 1 mV average differential drop corresponds to 1 mA of average drain-feed current.

## Hardware shutdown

- U31 (SN74LVC1G123DCUR) runs from 3.3 V and detects falling edges of the incoming clock at J51. B is held high and PA_EN drives active-low CLR. R31 (33 kΩ) and C32 (1 nF C0G) set a nominal 33 µs RC time constant. The actual one-shot pulse width depends on the device and timing parts. The longest operating clock period is about 7.4 µs.
- U31 Q drives U51's `CLOCK_OK` input. U51 (SN74LVC1G08DBVR) passes the clock to U61 when `CLOCK_OK` is high and drives `CLOCK_DRV` low when it is low. A low input clock cuts drive immediately. If J51 stalls high, U31 times out and U51 forces drive low. Raising PA_EN while J51 is low can create one `CLOCK_OK` pulse. U51's other input is low during that pulse, which keeps the gates low. The clock can restart the gate drive automatically while PA_EN stays high.
- PA_EN directly controls U21 and clears U31 when low. U21 supplies both U61 VCCB and the drain feed through R21. Every downstream 5 V load is on `5V_SW`, including during QRSS spaces. The 3.3 V logic stays powered while switched 5 V is off. R22 and U21's QOD discharge the downstream capacitors after PA_EN goes low.
- R32 (10 kΩ) pulls `CLOCK_OK` low if U31 goes high impedance. U61 isolates its outputs if either supply is lost completely, and R63 (22 kΩ) pulls the shared gate-drive node low. PA_EN still controls drain power if the local 3.3 V rail drops. U31 monitors J51. The design covers a stalled input clock, with analog brownouts and faults inside U61 requiring separate qualification. [TI watchdog datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g123.pdf) · [TI AND-gate datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf) · [TI buffer datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf)

Once the watchdog has armed, U51 passes the clock digitally. The first pulse after a gap can be skipped or shortened while the watchdog arms. The clock gate adds a short delay, and the RF network determines how the carrier settles. The load-switch ramp applies when PA_EN powers up the circuit for a message. The PA has no deliberate RF-envelope ramp between QRSS symbols.

## Circuit

- U61 is the SN74LVC2T45DCUR. Both inputs share `CLOCK_DRV` and the two outputs share a wired node. The raw output drives Q71 and Q72 through separate 120 Ω gate resistors, with the two sources grounded. The gate drive sets the DC level.
- U21 switches the common 5 V feed, including the original CT and output-discharge components. R21 remains 1 Ω, 0.25 W, and C23/C24 bypass the transformer feed. The 10 µF part specified at C24 must provide at least 4.7 µF effective at 5 V. The buffer activity detector and power LED are retained from the buffer design used in the model.
- T81 is hand-wound with 10+10 bifilar turns on the coated Fair-Rite 5977000621 mix 77 core. Pin 1 goes to the bypassed supply. The two dotted starts are pins 1 and 3. Pins 2 and 3 join at the common drain node for series-aiding phasing. Pin 4 feeds L81, the Coilcraft 0603HP-18NXJRW 18 nH trim, followed by the single C81 Walsin 1206N104J500CT 100 nF C0G, 50 V coupling capacitor.
- J11 is a standard four-pin 2.54 mm bench header. J51 and J81 use the Adafruit 1865 SMA interface. The band filter is external so the same PA can be tested across the sweep.

The prototype retains the mix 77 winding. See the [steady-state RF sweep](#steady-state-rf-sweep) for the mix 43 comparison and the 1 W results.

## Library provenance

- U61, the indicator devices, common passives and power symbols, and the SMA interface come from the [Logic RF Driver library](../Logic%20RF%20Driver/libraries/README.md).
- The BS170, TPS22918, transformer, test point, and associated footprints come from the [Torroid Edition library](../WsprryPico%20GPIO%20Shield%20with%20GPS%20-%20Torroid%20Edition/LIBRARY-SOURCES.md). The reused transformer preview depicts the original winding geometry. Use the 10+10 turn count and pin markings in this prototype's schematic.
- The generic inductor, four-pin header, and SOT-23-5 assets come from KiCad 10.0.6. The project-local U31 and U51 symbols follow TI's DCU VSSOP and DBV SOT-23 pinouts, respectively. U31 uses the same local VSSOP-8 footprint as U61. The header symbol’s footprint filter points to the equivalent local footprint. The gate resistors and trim follow the [Yageo 120 Ω part specification](https://yageogroup.com/component-documentation/download/specsheet/RC0603FR-07120RL) and [Coilcraft 18 nH part specification](https://www.coilcraft.com/en-us/products/rf/ceramic-core-chip-inductors/0603-%281608%29/0603hp/0603hp-18n/).
- See [KiCad library attribution](libraries/KICAD-LIBRARY-LICENSE.md) for the library license. Repository-authored assets retain the [repository license](../LICENSE.md).

## Validation

### Current saved schematic

After section-by-section re-annotation on 2026-11-26, KiCad 10.0.6 ERC reported **zero errors and zero warnings**, with no ignored checks. All 44 numbered components retained their symbol IDs, and all 26 nets matched the pre-annotation snapshot pin for pin.

The rendered schematic resolved all 16 shared text variables. J11 shows pins 1–4 as `+5V`, `+3V3`, `GND`, and `PA_EN`. The watchdog note shows **33 µs** from R31 (33 kΩ) and C32 (1 nF C0G), with U51 driving `CLOCK_DRV` low via `CLOCK_OK`. The load-switch notes show `PA_EN` switching `5V_SW` and identify TP21/TP22 across R21. Temporary test copies also verified the ps and ns output and the unit-error messages, which now name R31 and C32.

### Pinned schematic

Prototype B is the final schematic for the 18 nH trim and single 100 nF C0G coupling capacitor. The local snapshot in `generated/pinned/18nH-one-cap/` was refreshed on 2026-11-26 with the section reference numbers and shared text variables. It includes the KiCad project, schematic, local libraries, netlist, PDF, ERC report, and `SHA256SUMS`. The snapshot is schematic-only and Git-ignored. The previous snapshot is available locally at `generated/pinned/18nH-one-cap-pre-section-numbering/`.

KiCad 10.0.6 ERC reported **zero errors and zero warnings** on the pinned copy, with every rule enabled and no exclusions. All 26 nets match the reviewed netlist pin for pin. Connections use drawn wires, matching net labels, and GND symbols on the 50 mil connection grid. The regenerated PDF shows the J11 pinout, the calculated 33 µs RC time constant from R31/C32, and the TP21/TP22 measurement across R21.

### Steady-state RF sweep

The ngspice 45.2 sweep compares the retained 10+10-turn Fair-Rite 5977000621 mix 77 winding with the same-size 5943000621 mix 43 winding at 17 representative frequencies. Both models use the 18 nH trim, single 100 nF C0G coupling capacitor, and 120 Ω per gate. RF is the fundamental delivered to 50 Ω after the external seven-element C-first filter. Each band uses its own filter. Above 10 m, the model scales the 10 m filter values by frequency. The 8 m and 5 m rows are regional test points.

Nominal values use 127 nH of total winding leakage and 5 nH of modeled PCB series inductance. The RF ranges span nominal and the four combinations of 95 or 165 nH winding leakage and 0 or 12 nH PCB inductance, at nominal core inductance for each material. The 5 V current and per-transistor dissipation columns show nominal results. The model estimates core DC bias from drain-feed current. Winding fit, actual wound-core impedance, VHF filter behavior, RF output, and thermal performance remain open for prototype validation.

| Band | Test MHz | Mix 77 RF, mW | Mix 77 RF range, mW | Mix 43 RF, mW | Mix 43 RF range, mW | Avg. 5 V, mA (77 / 43) | Heat per BS170, mW (77 / 43) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2200 m | 0.1375 | 1,204.0 | 1,203.4–1,204.4 | 1,160.8 | 1,160.4–1,161.3 | 377 / 454 | 185 / 349 |
| 630 m | 0.4757 | 1,047.2 | 1,046.3–1,047.7 | 1,090.1 | 1,088.7–1,091.1 | 350 / 350 | 196 / 175 |
| 160 m | 1.8381 | 1,075.8 | 1,062.6–1,075.8 | 1,093.4 | 1,079.7–1,093.4 | 348 / 347 | 186 / 180 |
| 80 m | 3.5701 | 1,040.5 | 985.7–1,049.0 | 1,051.4 | 992.8–1,058.8 | 344 / 343 | 189 / 186 |
| 60 m | 5.2887 | 730.8 | 688.5–785.2 | 735.0 | 690.8–791.2 | 370 / 367 | 354 / 352 |
| 40 m | 7.0401 | 1,011.4 | 964.9–1,011.4 | 1,021.3 | 972.3–1,021.3 | 334 / 331 | 164 / 161 |
| 30 m | 10.1401 | 724.8 | 724.8–744.1 | 726.7 | 726.7–745.2 | 299 / 298 | 231 / 231 |
| 20 m | 14.0971 | 744.5 | 708.3–744.5 | 746.5 | 709.6–746.5 | 293 / 291 | 206 / 206 |
| 17 m | 18.1061 | 719.0 | 690.6–733.2 | 722.4 | 694.5–738.9 | 275 / 273 | 195 / 194 |
| 15 m | 21.0961 | 738.8 | 697.5–738.8 | 747.2 | 702.8–747.2 | 253 / 252 | 138 / 135 |
| 12 m | 24.9261 | 647.2 | 501.4–647.2 | 650.6 | 503.0–650.6 | 256 / 254 | 171 / 170 |
| 10 m | 28.1261 | 714.8 | 631.8–714.8 | 726.3 | 642.1–726.3 | 239 / 238 | 117 / 115 |
| 8 m | 40.68 | 484.7 | 484.7–571.9 | 490.0 | 490.0–582.0 | 208 / 207 | 169 / 167 |
| 6 m | 50.2945 | 467.6 | 302.0–467.6 | 473.4 | 305.3–473.4 | 180 / 179 | 107 / 105 |
| 5 m | 60.05 | 297.0 | 119.4–400.5 | 300.7 | 119.6–406.2 | 131 / 131 | 83 / 82 |
| 4 m | 70.0925 | 127.3 | 113.8–308.4 | 128.4 | 114.0–312.7 | 106 / 106 | 114 / 113 |
| 2 m | 144.4905 | 58.2 | 35.6–73.6 | 58.7 | 35.9–74.4 | 74 / 74 | 53 / 54 |

Both windings reach 1 W nominally on 2200 m, 630 m, 160 m, 80 m, and 40 m. At nominal core inductance, 2200 m, 630 m, and 160 m stay above 1 W at every sampled winding and PCB corner. For the retained mix 77 winding, the highest sampled dissipation is 355 mW per BS170 on 60 m and the highest modeled buffer-pin peak is 47.7 mA on 15 m.

Mix 43 adds 5.7 mW on 6 m, 3.7 mW on 5 m, 1.1 mW on 4 m, and 0.5 mW on 2 m. With mix 43 on 2200 m, output drops from 1.204 W to 1.161 W, average 5 V current rises from 377 to 454 mA, and dissipation rises from 185 to 349 mW per BS170. At 2200 m, reducing the mix 43 inductance factor by its catalog tolerance of 25% gives 0.999 W at nominal winding leakage and PCB inductance, or 0.881 W with the alternate DC-bias model. The mix 77 catalog tolerance endpoints of −30% and +25% give 1.176–1.268 W at the same nominal leakage and PCB inductance.

The per-band CSVs, matched corner cases, charts, and model assumptions are available locally in `generated/band-sweep-2200m-2m/` and `generated/mix43-band-sweep/`.

### Keyed and stuck-clock simulations

The keyed transient screen uses the pinned winding and band-filter models at 2200 m, 40 m, and 10 m. It starts with the 5 V rail charged and applies an ideal digital key to the modeled buffer. The cycle-averaged carrier amplitude enters and stays within 10% of its settled value about 15, 11, and 13 µs after the gated clock starts, respectively. These figures cover the modeled RF network and exclude U31 and U51 timing. Bench measurements are needed for actual watchdog timing, RF attack and decay into the band LPF, high-band clock duty cycle, and operation during supply ramps.

In nominal stuck-high simulations with the 5 V rail still enabled and an assumed 35 µs timeout, the drain peaked at about 32 V on 2200 m, 50.5 V on 40 m, and 39 V on 10 m when the gate drive was muted. The 40 m case reached 50.6 V with a 50 µs timeout. The fault-voltage margin to the BS170's 60 V rating still needs a bench check over winding and load variation. [onsemi BS170 datasheet](https://www.onsemi.com/download/data-sheet/pdf/mmbf170-d.pdf)
