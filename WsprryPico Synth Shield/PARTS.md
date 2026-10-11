# Synth shield component specifications

[PARTS.csv](PARTS.csv) contains **47 engineering inventory entries** for the implemented circuit, including manual purchases and copper test points. U11 is the combined Pico interface rather than a separately purchased component. The PCB contains **40 SMT assembly positions**. Generate manufacturing BOM and position files from the saved KiCad design; the engineering inventory records specifications and purchasing information.

## Assembly

Factory SMT includes both inductors, the receiver, synthesizer, regulators, TCXO, trimmer, switch, LED and passive components. The two Pico sockets, Q61 BS170, J61 SMA and J71 U.FL are hand fitted. U11, Q61, J61, J71 and TP61/TP62 are excluded from automated BOM and position output; J11/J12 are schematic-only socket descriptions whose electrical pads belong to U11. Test points are PCB copper features.

Check the exact ordering code, supplier stock and assembler allocation when ordering. The schematic's supplier fields and this inventory identify selected parts; they do not reserve stock. Preserve these assembly exclusions in every manufacturing export.

The populated capacitor, fixed-resistor and RV61 ordering fields were checked against LCSC catalog specifications on **2026-10-10**: manufacturer, MPN, value, dielectric, tolerance, voltage/power rating and package. These 31 references have matching supplier fields in the schematic and PCB. The [collection workbook](LCSC-parts-collection.xlsx) records the same selections. This check establishes catalog and footprint-package compatibility; the electrical and RF acceptance checks remain in [VALIDATION.md](VALIDATION.md).

## Capacitors

| References | Purpose | Value / dielectric | Tolerance / rating | Package | LCSC |
| --- | --- | --- | --- | --- | --- |
| C21, C22 | LDO input/output bypass | 2.2 µF X7R | ±10%, 25 V | 0805 | [C277470](https://www.lcsc.com/product-detail/C277470.html) |
| C31 | Amplifier switch input reservoir | 10 µF X7R | ±10%, 25 V | 1206 | [C14860](https://www.lcsc.com/product-detail/C14860.html) |
| C32 | TPS22918 slew capacitor | 1 nF C0G | ±5%, 50 V | 0603 | [C106246](https://www.lcsc.com/product-detail/C106246.html) |
| C33, C63 | Switched amplifier rail bulk bypass | 1 µF X7R | ±10%, 50 V | 0805 | [C726584](https://www.lcsc.com/product-detail/C726584.html) |
| C41 | TCXO supply bypass | 10 nF X7R | ±10%, 50 V | 0603 | [C525264](https://www.lcsc.com/product-detail/C525264.html) |
| C42 | TCXO OUT to XA coupling | 1 nF C0G | ±5%, 50 V | 0603 | [C106246](https://www.lcsc.com/product-detail/C106246.html) |
| C43, C51, C52 | TCXO and synthesizer supply bypass | 100 nF X7R | ±10%, 50 V | 0603 | [C235731](https://www.lcsc.com/product-detail/C235731.html) |
| C61, C64 | RF input/output DC blocking | 100 nF C0G | ±5%, 50 V | 1206 | [C170182](https://www.lcsc.com/product-detail/C170182.html) |
| C62 | Drain-feed supply HF bypass | 100 nF X7R | ±10%, 50 V | 0603 | [C235731](https://www.lcsc.com/product-detail/C235731.html) |
| C65 | Bias wiper bypass | 100 nF X7R | ±10%, 50 V | 0603 | [C235731](https://www.lcsc.com/product-detail/C235731.html) |
| C71 | GNSS supply bulk | 10 µF X7R | ±10%, 25 V | 1206 | [C14860](https://www.lcsc.com/product-detail/C14860.html) |
| C72, C73 | GNSS VCC/VBAT bypass | 100 nF X7R | ±10%, 50 V | 0603 | [C235731](https://www.lcsc.com/product-detail/C235731.html) |

The 2.2 µF LDO capacitors require adequate effective capacitance and ESR after DC-bias, temperature and tolerance effects; follow the [TPS7A20 requirements](https://www.ti.com/lit/gpn/tps7a20). At 135.7 kHz, the ideal reactance of each 100 nF RF coupling capacitor is approximately 11.73 Ω. Actual insertion loss, matching and RF voltage require measurement of the assembled path and external LPF over 2200 m–10 m.

## Resistors and bias control

| References | Function | Value | Manufacturer / ordering code | LCSC |
| --- | --- | --- | --- | --- |
| R11 | LED current limiter | 1 kΩ | YAGEO RC0603FR-071KL | [C22548](https://www.lcsc.com/product-detail/C22548.html) |
| R31, R63, R72 | AMP_EN, gate and PPS pull-downs | 100 kΩ | UNI-ROYAL 0603WAF1003T5E | [C25803](https://www.lcsc.com/product-detail/C25803.html) |
| R32, R71, R73 | QOD, UART input and PPS series resistors | 1 kΩ | YAGEO RC0603FR-071KL | [C22548](https://www.lcsc.com/product-detail/C22548.html) |
| R51, R52, R62 | I²C pull-ups and gate-bias feed | 4.7 kΩ | YAGEO RC0603FR-074K7L | [C99782](https://www.lcsc.com/product-detail/C99782.html) |
| R53 | CLK2 source damping | 33 Ω | UNI-ROYAL 0603WAF330JT5E | [C23140](https://www.lcsc.com/product-detail/C23140.html) |
| R61 | RF gate damping | 22 Ω | UNI-ROYAL 0603WAF220JT5E | [C23345](https://www.lcsc.com/product-detail/C23345.html) |

All fixed resistors are 0603 thick-film, ±1%, 100 mW, 75 V, ±100 ppm/°C. RV61 is **Bourns TC33X-2-502E / C719177**, 5 kΩ, ±25%, 150 mW, ±250 ppm/°C. Pin 2 is the wiper; pin 1 connects to `AMP_5V_SW` and pin 3 to GND. **Clockwise reduces bias; counterclockwise increases it**, viewed from the adjustment screw. Follow the [README adjustment procedure](README.md#adjusting-rv61), using approximately **5 mV DC across L61** as the conservative initial bench setting.

SW11 connects GP0 directly to ground; use the Pico's internal pull-up and software debounce. D11's anode is driven by GP1 through R11; its cathode is grounded. R71/R73 provide series resistance rather than voltage translation.

## Active parts and interfaces

| References | Selected part | LCSC | Assembly |
| --- | --- | --- | --- |
| U21 | TI TPS7A2033PDBVR, 3.3 V LDO | [C2862740](https://www.lcsc.com/product-detail/C2862740.html) | SMT |
| U31 | TI TPS22918DBVR load switch | [C131941](https://www.lcsc.com/product-detail/C131941.html) | SMT |
| Y41 | KDS 1XTW25000MAA, 25 MHz TCXO | [C253672](https://www.lcsc.com/product-detail/C253672.html) | SMT |
| U51 | SI5351A-B-GTR, MSOP-10 | [C504891](https://www.lcsc.com/product-detail/C504891.html) | SMT |
| U71 | Zhongke ATGM336H-5N31 receiver | [C90770](https://www.lcsc.com/product-detail/C90770.html) | SMT |
| Q61 | onsemi BS170, straight-lead TO-92 | [C111691](https://www.lcsc.com/product-detail/C111691.html) | Manual |
| RV61 | Bourns TC33X-2-502E | [C719177](https://www.lcsc.com/product-detail/C719177.html) | SMT |
| SW11 | XUNPU TS-1088R-02026 | [C455280](https://www.lcsc.com/product-detail/C455280.html) | SMT |
| D11 | KT-0603R red LED | [C2286](https://www.lcsc.com/product-detail/C2286.html) | SMT |
| J11, J12 | ZHOURI PM2.54-1*20 Pico sockets | [C5224030](https://www.lcsc.com/product-detail/C5224030.html) | Manual |
| J61 | Adafruit 1865, SMA edge mount for 1.6 mm PCB | [Supplier](https://www.adafruit.com/product/1865) | Manual |
| J71 | Hirose U.FL-R-SMT-1(10) | [C88373](https://www.lcsc.com/product-detail/C88373.html) | Manual |
| L71 | muRata LQW18AN47NG00D, 47 nH | [C98076](https://www.lcsc.com/product-detail/C98076.html) | SMT |
| TP61, TP62 | 1 × 1 mm copper test pads, 0.5 mm plated holes | — | PCB copper |

U21 supplies the TCXO, synthesizer and GNSS VCC/VBAT from `SYNTH_3V3`. The GNSS antenna receives DC bias through L71 and J71; use a compatible active antenna and U.FL/MHF1 pigtail. L71 is a factory wirewound RF inductor, ±2%, with 380 mA rating and 0.29 Ω maximum DCR. Check the antenna-current budget and GNSS-band behavior against the [receiver manual](https://www.lcsc.com/datasheet/C90770.pdf).

J11/J12 have 20 positions, 2.54 mm pitch and 8.5 mm body height. Their [supplier drawing](https://datasheet.lcsc.com/datasheet/pdf/d644f3ae7335586a805c6e9751c61823.pdf?productCode=C5224030) gives nominal 0.65 × 0.40 mm leads and a 1.02 mm recommended hole; U11 uses 1.00 mm drills. Verify finished-hole clearance, socket engagement and Pico clearance using actual parts. J61's [drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) governs the selected edge connector; local 3D previews are illustrative.

## Drain choke selection

L61 is **TDK VLS6045EX-331M / C501933**, **330 µH ±20% at 100 kHz**, with **1.44 Ω typical / 1.872 Ω maximum DCR**, **500 mA at 30% inductance reduction**, and **470 mA typical at 40 °C temperature rise**. [TDK specifications](https://product.tdk.com/en/search/inductor/inductor/smd/info?part_no=VLS6045EX-331M)

Its body is 6.0 ±0.3 mm square and at most 4.5 mm high. The local SMT footprint uses 1.9 × 5.1 mm lands, 4.2 mm pitch, a 2.3 mm inner gap and a 6.8 × 6.8 mm courtyard. Pad 1 is `AMP_5V_SW`; pad 2 is `AMP_DRAIN`. The part is included in assembly BOM/positions. See [footprint and model provenance](LIBRARY-SOURCES.md#drain-choke).

These component ratings do not establish choke impedance, amplifier output or thermal performance across the intended bands. The [bias procedure](README.md#adjusting-rv61) uses the choke's winding resistance to estimate RF-off drain current. Final RF acceptance requires the assembled board and the actual external LPF/load.
