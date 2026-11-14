# WsprryPico GPIO Shield with GPS - Torroid Edition circuit details

This document describes the transformer circuit implemented in the saved schematic. The [bifilar study](design/bifilar-transformer-study/README.md) supplies winding details and calculation limits. **The transformer circuit is placed and routed on the main PCB.** T61's [upright low-support footprint](design/t61-mount/README.md) is assigned in the schematic; the full assembly must remain within the board outline and CAD placement and routing checks pass; physical fit remains open.

The shield combines a direct Pico GP2 RF input, USB-powered BS170 amplifier. The intended RF range is **2200 m through 10 m**, with external band-specific low-pass filtering. The [schematic](WsprryPico%20GPIO%20Shield%20with%20GPS%20-%20Torroid%20Edition.kicad_sch), [parts inventory](PARTS.csv) and [Pico pin table](README.md#pico-pin-contract) define the revised circuit; the [PCB](WsprryPico%20GPIO%20Shield%20with%20GPS%20-%20Torroid%20Edition.kicad_pcb) matches that saved circuit.

## Power supplies

USB VBUS on Pico physical pin 40 supplies U31 **TPS22918DBVR**. It switches the amplifier supply under active-high `AMP_EN`, GP28 / physical pin 34. R31, 100 kΩ, provides a default-off pull-down; R32, 1 kΩ, connects VOUT to quick-output-discharge. The latest user-saved schematic removed U21 and the GNSS supply/circuit.

| U31 pin | Function | Connection |
| --- | --- | --- |
| 1 | VIN | VBUS, C31 bypass |
| 2 | GND | GND |
| 3 | ON | `AMP_EN`, R31 pull-down |
| 4 | CT | C32, 1 nF to GND |
| 5 | QOD | R32 to VOUT |
| 6 | VOUT | `AMP_5V_SW`, C33 bypass |

Validate USB current, effective bypass capacitance, startup, supply ripple and temperature on the assembled board. [TPS22918 pin functions and discharge behavior](https://www.ti.com/lit/ds/symlink/tps22918.pdf)

## RF amplifier and bias

The input is **GP2 / Pico physical pin 4 → CLOCK_RF → C61, 100 nF → R61, 22 Ω → Q61 gate**. RV61's 10 kΩ divider feeds the gate through R62, 4.7 kΩ; R63, 100 kΩ, returns it to ground. C65, 100 nF, bypasses the wiper. Q61 **BS170** uses pin **1 drain, 2 gate, 3 source**. The source is grounded. [BS170 datasheet](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)

R64 **1 Ω ±1%, 0.25 W, 1206** feeds `AMP_XFMR_FEED` from `AMP_5V_SW`. C62 **100 nF** and C63 **10 µF X7R, 25 V, 1206** bypass this feed to GND. Require at least **4.7 µF effective at 5 V** after relevant tolerances; verification remains open. RV61 stays on the upstream `AMP_5V_SW` supply.

T61 uses **Fair-Rite 5977000621**, coated material 77, wound with **15 turns in each of two bifilar AWG26 wires**. Its series-aiding connection provides a nominal 1:2 voltage / 1:4 impedance transformation, reflecting a 50 Ω fundamental load to approximately 12.5 Ω at the drain.

| T61 pin | Winding end | Schematic net |
| --- | --- | --- |
| 1, dot | A start | `AMP_XFMR_FEED` |
| 2 | A finish | `AMP_DRAIN` |
| 3, dot | B start | `AMP_DRAIN`, joined to pin 2 |
| 4 | B finish | `AMP_RF_XFMR` |

**C64 and C66–C69 are five parallel 100 nF C0G, 50 V Walsin 1206N104J500CT / C170182 capacitors**, between `AMP_RF_XFMR` and `TX_OUT`. Their 500 nF total has ideal reactance **2.346 Ω at 135.7 kHz**; C61 remains 100 nF, 11.73 Ω. The five parts form one underside row, all at 90°, with 1.00 mm straight common buses fed at opposite ends. Each branch has approximately 19.94 mm of total planar copper and one shared SMA via. Neither capacitor pad is ground. R62/R63/C65 sit above the bank; all 21 factory SMT positions remain on B.Cu. Actual matching, branch parasitics, RF-current capacity and loss require measurement.

RV61's clockwise end, pin 3, is grounded. The [README bias procedure](README.md#adjusting-rv61) uses R64 and an RF-off initial **3.5 mV / 3.5 mA** target. TP61 is upstream on `AMP_5V_SW`; TP62 is downstream on `AMP_XFMR_FEED`. Gate voltage is measured from Q61 pin 2 to GND. These connections now agree in the schematic and PCB.

## Reserved GPS connections

The current user-saved circuit has no receiver, LDO or antenna-bias network. The latest saved schematic and PCB both leave U11 pads 16, 17 and 21 unconnected. Current native parity checks report zero differences. ERC reports no violations with its four existing ignored categories. These pins do not provide a GNSS interface.

Keep `AMP_EN` low at startup. Enable the amplifier and allow its rail and bias to settle before starting GP2. Stop GP2 before disabling the amplifier. C61 blocks DC; the gate-bias and switched-drain circuits retain their separate roles.

## Board geometry and assembly

The two-layer board retains its original **53.33 × 22.85 mm envelope**, **1.6 mm thickness**, antenna notch, antenna keepout, Pico socket positions and SMA placement. All **21 machine-assembled SMT parts are on B.Cu**. Hand-fitted T61, Q61, D11 and SW11 are on the front; the sockets mate from the back and the SMA remains at the board edge.

T61 remains centered at **(146.75, 89.80) mm**, rotation 0°. Its **25 × 13.5 mm** front courtyard spans X = **134.25–159.25 mm**, Y = **83.05–96.55 mm**. The model now shows an illustrative 8 mm diameter × 1.25 mm insulating pad and 0.5 mm bedding allowance, putting the bare core bottom 1.75 mm above the PCB. Core and upper lead dressing are 4.25 mm lower. Actual support and attachment are builder-selected; no bumper or adhesive ordering code is prescribed. Three PTH holes are alongside the axial faces: ends 1 and 4 use separate 1.0 mm holes on the +Y face; ends 2/3 share one 1.2 mm hole on the opposite -Y face at the drain. The local footprint retains four logical end numbers, with a drill-free copper overlay for end 3. Reserve **30 mm top height** and ≤1.5 mm underside finished joints. C62 and C63 move next to the relocated feed terminal; the feed and VBUS trunks, quiet enable/LED routes and four ground stitches change accordingly. The RF input, gate, drain and complete output routes remain unchanged from the start of this correction. The capacitor bank and all other component placements remain unchanged. Physical adhesion, winding and socket/Pico fit remain sample checks.

The drain route retains **0.85 mm copper** and no vias. The output bank uses **1.00 mm common buses**, a short 0.50 mm neck at the existing shared SMA via, and 0.85 mm front SMA copper. Each complete branch retains approximately 19.94 mm planar copper and that one shared output transition. There are **51 GND vias** and **19 signal/power vias**, 70 total. Four new vias carry VBUS and the upstream transformer supply; the local T61-to-C62/C63 bypass connections have no vias. RF and bypass grounds use direct pour connections. The original rules and antenna keepout are preserved.

The schematic has **31 non-power references** and the PCB has **29 footprints**. J11/J12 describe the two purchased socket rows; U11 owns their pads. The CSV has **30 circuit entries excluding U11 plus three transformer material rows**. The workbook has **31 schematic references plus those three purchasing-only material rows**. The local libraries contain **14 active symbols**, **14 footprint types** and **six local model files**, using `${KIPRJMOD}` paths. Removed GNSS and L61 assets are absent from the active local libraries.

RV61 remains underneath and needs adjustment access using the actual stack height. SW11 and D11 are now hand-fitted through-hole controls on top, beside the antenna notch. Their existing GP0/GP1 connections and R11 value are unchanged. The [parts specification](PARTS.md), [Q61 lead dimensions](LIBRARY-SOURCES.md#transistor) and [validation record](VALIDATION.md) govern remaining checks.

## Sources and attribution

QRP Labs provides the [single-BS170 amplifier/bias study](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html). The [GPIO shield](https://github.com/WsprryPi/WsprryPi-PCB-Designs/blob/64fdd8f336c573cca9bfd5ce1ed3fad3cb0c8cb8/WsprryPico%20GPIO%20Shield/README.md) supplies the reusable amplifier topology. Manufacturer documents govern the selected parts; the separate [QRP module electrical models](../QRP%20Labs%20Modules/README.md) describe their own photographed hardware and unresolved component values.

Original repository work follows [LICENSE.md](LICENSE.md). Imported KiCad graphics retain [their library terms](KICAD-LIBRARY-LICENSE.md); manufacturer and QRP Labs documents retain their respective ownership.

## Socket clearance and bypass revision, 2026-10-20

U11 now reserves 52.00 × 3.04 mm courtyards for each purchased 51.30 ±0.20 × 2.54 mm socket. C61 is vertical at (127.90, 84.90) mm, rotation 270°; RV61 moved 0.30 mm inward. C61's maximum 3.40 mm body length leaves about 0.96 mm to the nominal socket edge. C31 VIN and C33 VOUT paths are approximately 2.69 and 2.00 mm, both on B.Cu without vias. TP61/TP62 remain at their accessible top probe locations and now use 1 mm copper pads without drilled holes beneath the socket bodies. The bias connections have been rerouted above the compact output bank; R61-to-Q61 gate is now 4.32 mm without vias; the short U31 bypass routes are retained. The [validation record](VALIDATION.md) identifies the exact saved revision.
