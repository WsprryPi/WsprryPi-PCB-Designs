# Synth shield circuit details

The shield combines a 25 MHz TCXO, Si5351A, USB-powered BS170 amplifier and onboard GNSS receiver. The intended RF range is **2200 m through 10 m**, with external band-specific low-pass filtering. The [schematic](WsprryPico%20Synth%20Shield.kicad_sch), [PCB](WsprryPico%20Synth%20Shield.kicad_pcb), [parts inventory](PARTS.csv) and [Pico pin table](README.md#pico-pin-contract) define the implemented hardware.

## Power supplies

USB VBUS on Pico physical pin 40 supplies U21 and U31. U21 **TPS7A2033PDBVR** generates `SYNTH_3V3` for Y41, U51, R51/R52 and U71 VCC/VBAT. Its EN pin is connected to IN. U31 **TPS22918DBVR** switches the amplifier supply under active-high `AMP_EN`, GP28 / physical pin 34. R31, 100 kΩ, provides a default-off pull-down; R32, 1 kΩ, connects VOUT to the quick-output-discharge pin.

| U21 pin | Function | Connection |
| --- | --- | --- |
| 1 | IN | VBUS, C21 bypass |
| 2 | GND | GND |
| 3 | EN | IN/VBUS |
| 4 | NC | Unconnected |
| 5 | OUT | `SYNTH_3V3`, C22 bypass |

| U31 pin | Function | Connection |
| --- | --- | --- |
| 1 | VIN | VBUS, C31 bypass |
| 2 | GND | GND |
| 3 | ON | `AMP_EN`, R31 pull-down |
| 4 | CT | C32, 1 nF to GND |
| 5 | QOD | R32 to VOUT |
| 6 | VOUT | `AMP_5V_SW`, C33 bypass |

The [TPS7A20 datasheet](https://www.ti.com/lit/gpn/tps7a20) specifies a 300 mA device rating; available load also depends on input voltage, dissipation and board temperature. The shared LDO budget includes the TCXO, synthesizer, receiver and active antenna. Validate total current, effective bypass capacitance, startup, supply ripple and thermal margin with the actual assembly. [TPS22918 pin functions and discharge behavior](https://www.ti.com/lit/ds/symlink/tps22918.pdf)

## TCXO and reference input

Y41 is **KDS 1XTW25000MAA**, 25 MHz, DSB321SDN. The [exact KDS specification](https://datasheet.lcsc.com/datasheet/pdf/4560f1646e80e1d25a345e540c19e02b.pdf?productCode=C253672) identifies:

| Parameter | Specified value |
| --- | --- |
| Supply | 3.3 V nominal; 3.135–3.465 V |
| Output | DC-coupled clipped sine; at least 0.8 V peak-to-peak |
| Specified load | 10 kΩ in parallel with 10 pF |
| Supply current | 1.5 mA maximum |
| Operating temperature | −30 to +85 °C |
| Initial frequency tolerance | ±1.5 ppm after two reflows |
| Temperature stability | ±0.5 ppm relative to 25 °C |
| Supply/load sensitivity | ±0.2 ppm each under specified variation |
| Aging | ±1 ppm/year at room ambient |
| Startup | At most 2 ms to 90% output amplitude |

Pins **1 and 2 are GND, 3 is OUT, and 4 is VCC**. C41, 10 nF, and C43, 100 nF, bypass VCC. C42, **1 nF C0G**, couples OUT to U51 XA. XB is unconnected. Measure loaded XA amplitude and startup with a suitable high-impedance probe; this clipped-sine reference is not intended for a 50 Ω load. [KDS package drawing](https://www.kds.info/wp-content/uploads/2015/11/dsb321sdn-1-d_pdf_en-1.pdf#page=2)

The architecture follows [QRP Labs' TCXO-to-synthesizer connection](https://www.qrp-labs.com/images/synth/synth_assembly5.pdf#page=5). QRP Labs' description of its module's compensation does not establish the exact selected KDS part's internal compensation mechanism or guarantee phase continuity; those behaviors require source evidence or measurement for this part.

## Si5351A

U51 is **SI5351A-B-GTR**, 10-pin MSOP, with direct 3.3 V I²C0 and 4.7 kΩ pull-ups to `SYNTH_3V3`.

| U51 pin | Function | Connection |
| --- | --- | --- |
| 1 | VDD | `SYNTH_3V3`, C51 bypass |
| 2 | XA | C42 from Y41 OUT |
| 3 | XB | Unconnected |
| 4 | SCL | GP5 / physical pin 7, R52 pull-up |
| 5 | SDA | GP4 / physical pin 6, R51 pull-up |
| 6 | CLK2 | R53, 33 Ω, to GP3 / physical pin 5 |
| 7 | VDDO | `SYNTH_3V3`, C52 bypass |
| 8 | GND | GND |
| 9 | CLK1 | Unconnected |
| 10 | CLK0 | C61 to the amplifier input |

C51/C52 are 100 nF each. Configure firmware for a **25,000,000 Hz reference** and board-specific frequency correction. Validate I²C rise time at the selected bus speed, output drive, divider allocation and frequency transitions. The external-reference input and register settings must follow the exact silicon documentation. In particular, resolve register 183's crystal-load setting against the [Si5351 datasheet](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/data-sheets/Si5351-B.pdf) and [AN619](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/application-notes/AN619.pdf#page=60) before using a driver's generic zero-load option.

Keep `AMP_EN` low during startup and initialize with RF disabled. Keep the reference supply on between transmissions and control RF output through the synthesizer. Reinitialize after actual supply loss. WsprryPico's [Si5351 engine and CLK2 integration](https://github.com/WsprryPi/WsprryPico/blob/devel/docs/development/si5351-transmission-backlog.md) require firmware implementation and qualification.

## RF amplifier and bias

The input is **CLK0 → C61, 100 nF → R61, 22 Ω → Q61 gate**. RV61's 5 kΩ divider feeds the gate through R62, 4.7 kΩ; R63, 100 kΩ, returns it to ground. C65, 100 nF, bypasses the wiper. Q61 **BS170** uses pin **1 drain, 2 gate, 3 source**. The source is grounded. [BS170 datasheet](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)

L61 **VLS6045EX-331M**, 330 µH, feeds the drain from `AMP_5V_SW`; C62/C63 bypass its supply side. The output is **drain → C64, 100 nF C0G → J61 SMA → external LPF → load**. The chosen choke's RF impedance under DC bias, amplifier output, harmonics and thermal behavior must be measured over 2200 m–10 m. At 135.7 kHz, each ideal 100 nF coupling capacitor has approximately 11.73 Ω reactance; the assembled path determines actual matching and loss.

RV61's clockwise end, pin 3, is grounded. The [README bias procedure](README.md#adjusting-rv61) specifies RF-off measurement across L61 and a conservative **5 mV initial drop**, approximately 3.5 mA at typical winding resistance. TP61 is assigned to `AMP_5V_SW`, and TP62 to `AMP_DRAIN`. Check their connection status in [VALIDATION.md](VALIDATION.md#outstanding-findings) before using them. Gate voltage is measured from Q61 pin 2 to GND.

## GNSS and calibration connections

U71 is **ATGM336H-5N31**, an AT6558/CASIC receiver. Its [module manual](https://www.lcsc.com/datasheet/C90770.pdf) governs UART commands, pin functions and antenna requirements. GPS_RX/GPS_TX net names use the receiver's perspective.

| U71 pin | Function | Connection |
| --- | --- | --- |
| 1, 10, 12 | GND | GND |
| 2 | TX | Pico GP13 / physical pin 17 |
| 3 | RX | R71, 1 kΩ, from Pico GP12 / physical pin 16 |
| 4 | PPS | R73, 1 kΩ, to GP16 / physical pin 21; R72, 100 kΩ, pull-down |
| 6 | VBAT | `SYNTH_3V3`, C73 bypass |
| 8 | VCC | `SYNTH_3V3`, C71/C72 bypass |
| 11 | RF_IN | J71 U.FL signal and L71 antenna-bias choke |
| 14 | VCC_RF | L71, 47 nH, to the antenna signal |

The remaining receiver pins are unconnected in this design. J71 selects **Hirose U.FL-R-SMT-1(10)** for a U.FL/MHF1 pigtail. Verify antenna supply compatibility and current, receiver fix/PPS validity and RF coexistence with the transmitter. VCC and VBAT share the powered rail.

CLK2 feedback and GNSS PPS provide inputs for Pico-side frequency measurement. Firmware must establish a verified fixed CLK2/reference ratio, coherent counting/capture, overflow handling and rejection of invalid or missing PPS. Frequency corrections should remain fixed through a complete transmission. UTC scheduling and RF-reference correction are separate functions; neither is established by wiring PPS alone.

## Sources and attribution

QRP Labs provides the preferred [synthesizer precedent](https://qrp-labs.com/synth.html) and [single-BS170 amplifier/bias study](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html). The [GPIO shield](../WsprryPico%20GPIO%20Shield/README.md) supplies the reusable amplifier topology. Manufacturer documents govern the selected parts; the separate [QRP module electrical models](../QRP%20Labs%20Modules/README.md) describe their own photographed hardware and unresolved component values.

Original repository work follows [LICENSE.md](LICENSE.md). Imported KiCad graphics retain [their library terms](KICAD-LIBRARY-LICENSE.md); manufacturer and QRP Labs documents retain their respective ownership.
