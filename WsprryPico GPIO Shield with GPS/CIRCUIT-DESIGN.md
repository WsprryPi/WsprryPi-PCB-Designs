# WsprryPico GPIO Shield with GPS circuit details

The shield combines a direct Pico GP2 RF input, USB-powered BS170 amplifier and onboard GNSS receiver. The intended RF range is **2200 m through 10 m**, with external band-specific low-pass filtering. The [schematic](WsprryPico%20GPIO%20Shield%20with%20GPS.kicad_sch), [PCB](WsprryPico%20GPIO%20Shield%20with%20GPS.kicad_pcb), [parts inventory](PARTS.csv) and [Pico pin table](README.md#pico-pin-contract) define the implemented hardware.

## Power supplies

USB VBUS on Pico physical pin 40 supplies U21 and U31. U21 **TPS7A2033PDBVR** generates `GNSS_3V3` for U71 VCC/VBAT. Its EN pin is connected to IN. U31 **TPS22918DBVR** switches the amplifier supply under active-high `AMP_EN`, GP28 / physical pin 34. R31, 100 kΩ, provides a default-off pull-down; R32, 1 kΩ, connects VOUT to the quick-output-discharge pin.

| U21 pin | Function | Connection |
| --- | --- | --- |
| 1 | IN | VBUS, C21 bypass |
| 2 | GND | GND |
| 3 | EN | IN/VBUS |
| 4 | NC | Unconnected |
| 5 | OUT | `GNSS_3V3`, C22 bypass |

| U31 pin | Function | Connection |
| --- | --- | --- |
| 1 | VIN | VBUS, C31 bypass |
| 2 | GND | GND |
| 3 | ON | `AMP_EN`, R31 pull-down |
| 4 | CT | C32, 1 nF to GND |
| 5 | QOD | R32 to VOUT |
| 6 | VOUT | `AMP_5V_SW`, C33 bypass |

The [TPS7A20 datasheet](https://www.ti.com/lit/gpn/tps7a20) specifies a 300 mA device rating; available load also depends on input voltage, dissipation and board temperature. The LDO budget includes the receiver and active antenna. Validate total current, effective bypass capacitance, startup, supply ripple and thermal margin with the actual assembly. [TPS22918 pin functions and discharge behavior](https://www.ti.com/lit/ds/symlink/tps22918.pdf)

## RF amplifier and bias

The input is **GP2 / Pico physical pin 4 → CLOCK_RF → C61, 100 nF → R61, 22 Ω → Q61 gate**. RV61's 5 kΩ divider feeds the gate through R62, 4.7 kΩ; R63, 100 kΩ, returns it to ground. C65, 100 nF, bypasses the wiper. Q61 **BS170** uses pin **1 drain, 2 gate, 3 source**. The source is grounded. [BS170 datasheet](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)

L61 **VLS6045EX-331M**, 330 µH, feeds the drain from `AMP_5V_SW`; C62/C63 bypass its supply side. The output is **drain → C64, 100 nF C0G → J61 SMA → external LPF → load**. The chosen choke's RF impedance under DC bias, amplifier output, harmonics and thermal behavior must be measured over 2200 m–10 m. At 135.7 kHz, each ideal 100 nF coupling capacitor has approximately 11.73 Ω reactance; the assembled path determines actual matching and loss.

RV61's clockwise end, pin 3, is grounded. The [README bias procedure](README.md#adjusting-rv61) specifies RF-off measurement across L61 and a conservative **5 mV initial drop**, approximately 3.5 mA at typical winding resistance. TP61 is assigned to `AMP_5V_SW`, and TP62 to `AMP_DRAIN`. Gate voltage is measured from Q61 pin 2 to GND.

## GNSS and calibration connections

U71 is **ATGM336H-5N31**, an AT6558/CASIC receiver. Its [module manual](https://www.lcsc.com/datasheet/C90770.pdf) governs UART commands, pin functions and antenna requirements. GPS_RX/GPS_TX net names use the receiver's perspective.

| U71 pin | Function | Connection |
| --- | --- | --- |
| 1, 10, 12 | GND | GND |
| 2 | TX | Pico GP13 / physical pin 17 |
| 3 | RX | R71, 1 kΩ, from Pico GP12 / physical pin 16 |
| 4 | PPS | R73, 1 kΩ, to GP16 / physical pin 21; R72, 100 kΩ, pull-down |
| 6 | VBAT | `GNSS_3V3`, C73 bypass |
| 8 | VCC | `GNSS_3V3`, C71/C72 bypass |
| 11 | RF_IN | J71 U.FL signal and L71 antenna-bias choke |
| 14 | VCC_RF | L71, 47 nH, to the antenna signal |

The remaining receiver pins are unconnected in this design. J71 selects **Hirose U.FL-R-SMT-1(10)** for a U.FL/MHF1 pigtail. Verify antenna supply compatibility and current, receiver fix/PPS validity and RF coexistence with the transmitter. VCC and VBAT share the powered rail.

GNSS PPS is wired to GP16. GPIO-clock calibration requires implemented capture/counting logic, overflow handling and rejection of invalid or missing PPS. Keep frequency corrections fixed through a complete transmission. UTC scheduling and RF-frequency correction are separate functions; confirm RF frequency independently after implementing calibration.

Keep `AMP_EN` low at startup. Enable the amplifier and allow its rail and bias to settle before starting GP2. Stop GP2 before disabling the amplifier. C61 blocks DC; the gate-bias and switched-drain circuits retain their separate roles.

## Board geometry and assembly

The two-layer board has a **53.33 × 22.85 mm envelope**, **1.6 mm thickness**, and a **14 × 9 mm antenna opening** with a keepout on both copper layers. The combined U11 interface has two 1×20 rows, 2.54 mm pitch and 17.78 mm row spacing. Components occupy F.Cu; the Pico and sockets mate from B.Cu.

All routed signals use F.Cu over the B.Cu ground plane. The board has **83 GND vias**, with returns around the amplifier/output and GNSS RF route. The R61 pad-2 to Q61 gate copper path is **4.111 mm**; GP2 to C61 is **13.70 mm**. Preserve the antenna keepout and ground returns when changing the layout. GNSS module shielding and the shielded drain choke do not establish isolation from amplifier or Wi-Fi activity.

The main drain/output route uses **0.85 mm traces** and a **0.15 mm drain-to-front-pour rule**. The GNSS antenna route uses **0.45 mm traces** and a **0.10 mm gap rule**. Other drain-to-ground objects retain the **0.20 mm clearance**. These are nominal impedance starting geometries; the manufactured dielectric, copper, mask and pad transitions determine impedance.

The design contains **38 non-power schematic references**, **36 PCB footprints** and **30 SMT assembly positions**. J11/J12 describe the purchased sockets; U11 owns their electrical pads. The engineering CSV has 37 entries excluding U11; the workbook has all 38 references. The [parts specification](PARTS.md) defines manual parts and fabrication-output exclusions.

The local libraries contain **18 used symbols**, **17 assigned footprint types** and **eight local model files**, using `wsprrypico-gpio-shield-with-gps` and `${KIPRJMOD}` paths. Standard models use the installed KiCad 3D library. Illustrative models do not establish physical fit. Q61's [hole, pad and lead-forming dimensions](LIBRARY-SOURCES.md#transistor) govern assembly.

## Sources and attribution

QRP Labs provides the [single-BS170 amplifier/bias study](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html). The [GPIO shield](https://github.com/WsprryPi/WsprryPi-PCB-Designs/blob/64fdd8f336c573cca9bfd5ce1ed3fad3cb0c8cb8/WsprryPico%20GPIO%20Shield/README.md) supplies the reusable amplifier topology. Manufacturer documents govern the selected parts; the separate [QRP module electrical models](../QRP%20Labs%20Modules/README.md) describe their own photographed hardware and unresolved component values.

Original repository work follows [LICENSE.md](LICENSE.md). Imported KiCad graphics retain [their library terms](KICAD-LIBRARY-LICENSE.md); manufacturer and QRP Labs documents retain their respective ownership.
