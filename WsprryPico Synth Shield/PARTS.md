# Synth shield component specifications

Selected on 2026-10-06 for the first prototype. Values, dielectrics, ratings, ordering codes and project-local footprints are specified for the clock, amplifier, counter, GPS interface and controls. The **drain choke has an unresolved sourcing conflict**: the approved FT37-43 winding has no verified LCSC stock source. Its replacement or a sourcing exception awaits the user's choice. Measurements remain required for acceptance of the RF path, power supplies and PPS capture.

[PARTS.csv](PARTS.csv) is the complete 58-position engineering inventory, including manual purchases and PCB copper features. [ASSEMBLY-BOM-PREVIEW.csv](ASSEMBLY-BOM-PREVIEW.csv) contains the 49 selected SMT positions only. The references are now assigned to the placed schematic symbols. The assembly preview remains inventory-derived; neither file is a manufacturing release, and PCB synchronization/placement remain pending. The counter and onboard GPS receiver are selected for fitting on the shield; GPS remains optional for operation.

## Assembly exclusions

**All headers, the SMA and hand-wound inductors are excluded from the assembly BOM and position output**, as directed by the user on 2026-10-06. Keep their electrical connectivity and PCB footprints. J11/J12 purchasing descriptions remain schematic-only; U11 contains their two pad rows, so do not add duplicate footprints for the sockets. J61 TX SMA and J91 GPS SMA footprints explicitly carry both exclusions. Their placed schematic symbols use `in_bom no` and `on_board yes`; their future PCB instances must retain both exclusions, and all assembly exporters must respect those flags.

Preserve manual fitting of the source design's BS170 and hand-wound choke. L61 has `in_bom no` and `in_pos_files no` in the placed schematic; any other hand-wound inductor must retain those exclusions and both `exclude_from_bom` and `exclude_from_pos_files` on the PCB footprint. Retain their electrical connections and winding/purchasing specifications in this engineering inventory. This assembly exclusion does not settle L61's separate sourcing choice. JP41 and JP51 are copper features, not purchasable components. J11, J12, J61 and J91 remain listed here for manual purchasing; their presence in this engineering inventory does not put them into the assembly BOM. No position file is produced until actual placement.

## Capacitors

Use **C0G/NP0 for the reference coupling, RF input/output coupling and slew capacitor**. Use **X7R for bypass, bulk and button capacitors**. The approved reference-section values are retained. C61/C64 keep the source amplifier's 100 nF nominal coupling values; C51 retains its 10 µF nominal input reservoir while moving to a 25 V X7R 1206 part.

| References | Purpose | Value and dielectric | Tolerance / voltage | Package | LCSC |
| --- | --- | --- | --- | --- | --- |
| C21 | TCXO supply bypass | 10 nF X7R | 10% / 50 V | 0603 | [C1589](https://www.lcsc.com/product-detail/C1589.html) |
| C22 | TCXO OUT to XA AC coupling | 1 nF C0G / NP0 | 5% / 50 V | 0603 | [C77026](https://www.lcsc.com/product-detail/C77026.html) |
| C23, C31, C32 | TCXO additional bypass; Si5351 VDD/VDDO bypass | 100 nF X7R | 10% / 50 V | 0603 | [C14663](https://www.lcsc.com/product-detail/C14663.html) |
| C41, C42 | Clock LDO input/output capacitors | 2.2 uF X7R | 10% / 25 V | 0805 | [C364318](https://www.lcsc.com/product-detail/C364318.html) |
| C51 | Amplifier switch input reservoir | 10 uF X7R | 10% / 25 V | 1206 | [C77093](https://www.lcsc.com/product-detail/C77093.html) |
| C52 | TPS22918 CT slew capacitor | 1 nF C0G / NP0 | 5% / 50 V | 0603 | [C77026](https://www.lcsc.com/product-detail/C77026.html) |
| C53 | Amplifier switched rail local bulk | 1 uF X7R | 10% / 50 V | 0805 | [C726584](https://www.lcsc.com/product-detail/C726584.html) |
| C65 | Gate bias wiper bypass | 100 nF X7R | 10% / 50 V | 0603 | [C14663](https://www.lcsc.com/product-detail/C14663.html) |
| C61, C64 | RF input coupling; drain to SMA DC blocking | 100 nF C0G / NP0 | 5% / 50 V | 1206 | [C170182](https://www.lcsc.com/product-detail/C170182.html) |
| C62 | Amplifier drain-feed HF bypass | 100 nF X7R | 10% / 50 V | 0603 | [C14663](https://www.lcsc.com/product-detail/C14663.html) |
| C63 | Amplifier drain-feed local bulk | 1 uF X7R | 10% / 50 V | 0805 | [C726584](https://www.lcsc.com/product-detail/C726584.html) |
| C71, C73 | LS7366 supply bypass; PPS inverter supply bypass | 100 nF X7R | 10% / 50 V | 0603 | [C14663](https://www.lcsc.com/product-detail/C14663.html) |
| C72 | Counter local bulk | 1 uF X7R | 10% / 50 V | 0805 | [C726584](https://www.lcsc.com/product-detail/C726584.html) |
| C91 | GNSS supply bulk (formerly C74) | 10 uF X7R | 10% / 25 V | 1206 | [C77093](https://www.lcsc.com/product-detail/C77093.html) |
| C92, C93 | GNSS VCC / VBAT local bypass | 100 nF X7R | 10% / 50 V | 0603 | [C14663](https://www.lcsc.com/product-detail/C14663.html) |
| C81 | Button deglitch capacitor | 10 nF X7R | 10% / 50 V | 0603 | [C1589](https://www.lcsc.com/product-detail/C1589.html) |

The 2.2 µF LDO parts are 0805, 25 V, X7R, ±10%. After nominal tolerance and the X7R temperature envelope, the calculated capacitance is `2.2 × 0.90 × 0.85 = 1.683 µF` before DC-bias loss. Keeping at least 0.47 µF requires a remaining bias factor of at least `0.47 / 1.683 = 0.279`; this is a margin calculation, not a guarantee from a generic X7R label. Verify the exact capacitor's bias behavior at the maximum selected input and 3.3 V output, output ESR and startup/transients against the [TPS7A20 requirements](https://www.ti.com/lit/gpn/tps7a20). Supplier ordering details are resolved; effective capacitance remains an electrical acceptance check.

For C61/C64, ideal capacitive reactance at the 2200 m lower band edge of 135.7 kHz is `1 / (2π × 135700 × 100 nF) = 11.73 Ω`. That calculation supports retaining the source nominal value as a prototype; it does not predict the actual amplifier matching, power or insertion loss. Package inductance, mounting and self resonance govern VHF behavior. Measure the complete input/output path through 2 m, including external LPF and load, and verify drain RF voltage against the capacitor rating. No single capacitor selection establishes full-band RF qualification.

## Resistors and bias control

| References | Value | Specification | Ordering code / LCSC |
| --- | --- | --- | --- |
| R31, R32, R62 | 4.7 kohm | 0603, thick film, ±1%, 100 mW, 75 V, ±100 ppm/°C | 0603WAF4701T5E / [C23162](https://www.lcsc.com/product-detail/C23162.html) |
| R51, R63, R73 | 100 kohm | 0603, thick film, ±1%, 100 mW, 75 V, ±100 ppm/°C | 0603WAF1003T5E / [C25803](https://www.lcsc.com/product-detail/C25803.html) |
| R52, R75, R82, R83, R91 | 1 kohm | 0603, thick film, ±1%, 100 mW, 75 V, ±100 ppm/°C | FRC0603F1001TS / [C2907002](https://www.lcsc.com/product-detail/C2907002.html) |
| R61 | 22 ohm | 0603, thick film, ±1%, 100 mW, 75 V, ±100 ppm/°C | 0603WAF220JT5E / [C23345](https://www.lcsc.com/product-detail/C23345.html) |
| R71, R72, R81 | 10 kohm | 0603, thick film, ±1%, 100 mW, 75 V, ±100 ppm/°C | FRC0603F1002TS / [C2906982](https://www.lcsc.com/product-detail/C2906982.html) |
| R74 | 33 ohm | 0603, thick film, ±1%, 100 mW, 75 V, ±100 ppm/°C | 0603WAF330JT5E / [C23140](https://www.lcsc.com/product-detail/C23140.html) |

R31/R32 are the approved 4.7 kΩ pull-ups to `SYNTH_3V3`. The source amplifier retains a 22 Ω gate resistor, 4.7 kΩ bias feed, 100 kΩ gate return, 100 kΩ `AMP_EN` pull-down and 1 kΩ QOD resistor. R71/R72 are 10 kΩ counter CS/LFLAG pull-ups to Pico 3.3 V; R73 is the absent-PPS pull-down; R74 is the 33 Ω CLK2 source resistor. R75 is a 1 kΩ PPS input series resistor ahead of the shared GP16/inverter-input node. It does not provide level conversion or power-off isolation.

RV61 is **Bourns TC33X-2-502E / C719177**, 5 kΩ, ±25%, 150 mW, ±250 ppm/°C. Use the manufacturer's exact **TC33X-2-502E** ordering code. Pins 1 and 3 are the resistive ends; pin 2 is the wiper. Use the [Bourns TC33 drawing](https://www.bourns.com/docs/product-datasheets/tc33.pdf), and begin bias adjustment with the wiper at the grounded end and RF disabled. The manual JP51 bypass powers the amplifier regardless of `AMP_EN`; leave it open for normal operation. The TPS22918 is not a separate reverse-current isolator.

The button uses a 10 kΩ external pull-up, 1 kΩ GPIO series resistor and 10 nF deglitch capacitor; the nominal RC is 100 µs, with software debounce still required. D81 is a red KT-0603R LED with a **1 kΩ** series resistor, reducing current from the source design's 220 Ω choice to roughly 1.3 mA at an assumed 2.0 V forward drop and 3.3 V drive. LED pin 2 is anode and pin 1 cathode. Electrical part selections are complete. **Control GPIOs approved 2026-10-07: GP6 / physical 9 = AMP_EN; GP14 / physical 19 = BUTTON_N; GP15 / physical 20 = LED_DRIVE.** See the [locked control pin plan](TCXO-SI5351A-DESIGN.md#control-gpio-decisions). Button action and LED behavior remain open; startup/keying behavior still requires implementation and verification.

## Integrated circuits and interface parts

| Reference | Part | Selected footprint | Assembly |
| --- | --- | --- | --- |
| D81 | KT-0603R / [C2286](https://www.lcsc.com/product-detail/C2286.html) | LED_0603_1608Metric | SMT |
| J11 | PM2.54-1*20 / [C5224030](https://www.lcsc.com/product-detail/C5224030.html) | Raspberry_Pi_Pico_2W_Header | Manual |
| J12 | PM2.54-1*20 / [C5224030](https://www.lcsc.com/product-detail/C5224030.html) | Raspberry_Pi_Pico_2W_Header | Manual |
| J61 | Adafruit 1865; existing project board-edge SMA | SMA_Adafruit_1865_EdgeMount | Manual; no BOM/positions |
| J91 | GPS antenna SMA; existing project board-edge SMA | SMA_Adafruit_1865_EdgeMount | Manual; no BOM/positions |
| L91 | 47 nH muRata LQW18AN47NG00D / [C98076](https://www.lcsc.com/product-detail/C98076.html) | L_0603_1608Metric | Factory SMT; included in BOM/positions |
| U91 | ATGM336H-5N31 / [C90770](https://www.lcsc.com/product-detail/C90770.html) | Zhongke_ATGM336H-5N31_9.7x10.1mm_P1.1mm | SMT |
| TP91 | GPS_RX hand-wire pad; 1 × 1 mm, 0.5 mm plated hole | TestPoint_THTPad_1.0x1.0mm_Drill0.5mm | PCB copper; no BOM/positions |
| Q61 | BS170 / [C111691](https://www.lcsc.com/product-detail/C111691.html) | TO-92_Inline | Manual |
| RV61 | TC33X-2-502E / [C719177](https://www.lcsc.com/product-detail/C719177.html) | Potentiometer_Bourns_TC33X_Vertical | SMT |
| SW81 | TS-1088R-02026 / [C455280](https://www.lcsc.com/product-detail/C455280.html) | SW_SPST_XUNPU_TS1088R_4x3mm | SMT |
| U31 | SI5351A-B-GTR / [C504891](https://www.lcsc.com/product-detail/C504891.html) | MSOP-10_Si5351A_3x3mm_P0.5mm | SMT |
| U41 | TPS7A2033PDBVR / [C2862740](https://www.lcsc.com/product-detail/C2862740.html) | SOT-23-5 | SMT |
| U51 | TPS22918DBVR / [C131941](https://www.lcsc.com/product-detail/C131941.html) | SOT-23-6 | SMT |
| U71 | LS7366R-S / [C3827808](https://www.lcsc.com/product-detail/C3827808.html) | SOIC-14_3.9x8.7mm_P1.27mm | SMT |
| U72 | SN74LVC1G14DBVR / [C7835](https://www.lcsc.com/product-detail/C7835.html) | SOT-23-5 | SMT |
| Y21 | 1XTW25000MAA / [C253672](https://www.lcsc.com/product-detail/C253672.html) | KDS_DSB321SDN_3.2x2.5mm | SMT |

Use the exact package pin maps in [the circuit notes](TCXO-SI5351A-DESIGN.md). U31 is blank SI5351A-B-GTR in MSOP-10, not a factory-programmed variant or the photographed MS5351M. U41 is DBV SOT-23-5, with EN tied to IN. U51 is DBV SOT-23-6, with 1 VIN, 2 GND, 3 ON, 4 CT, 5 QOD and 6 VOUT. U72 is TI SN74LVC1G14DBVR, with 1 NC, 2 A, 3 GND, 4 Y and 5 VCC. Q61 BS170 is 1 drain, 2 gate, 3 source; keep this mapping separate from 2N7000 variants.

J61 uses the existing **Adafruit 1865 board-edge SMA** footprint for a 1.6 mm PCB, restored at the user's request on 2026-10-07. Pin 1 is TX_OUT; all four pad-2 lands are GND, with two ground lands on each board face. It is hand-soldered, with no paste, BOM or position output. The footprint and provisional local 3D model are copied from the GPIO shield into independent Synth libraries. The old BAT WIRELESS through-hole selection and C496551 ordering fields are superseded. The previously saved **Superbat B09V5811S7, “0.062 inch Straight Connector”** remains a probable substitute pending sample fit and RF checks; see the [existing connector record](../Pico%202W%20Wattmeter%20Shield/J1-CONNECTOR-NOTES.md#probable-amazon-alternative-superbat-b09v5811s7). The footprint origin is its board-edge seating point and the barrel faces local +Y. J61 remains at its existing unplaced staging origin; final edge placement and GPS/SMA clearance are still required.

The QLG3 carrier/J71 is retired. U91 is the onboard **ATGM336H-5N31 / C90770** in the new 90-series, with J91 antenna SMA, 47 nH L91 **LQW18AN47NG00D / C98076**, R91 and C91-C93. TP91 replaces TP71. See the [current pin plan, verified stock and implementation limits](TCXO-SI5351A-DESIGN.md#gps-configuration-locked). The 70-series retains the counter and PPS conditioner. New SMT parts are included in assembly inventory; J91 and TP91 are excluded. The current PCB still needs synchronization.

J11/J12 use **ZHOURI PM2.54-1*20 / C5224030**, 20 positions, 2.54 mm pitch, 8.5 mm body height, purchased and fitted by hand. The [supplier drawing](https://datasheet.lcsc.com/datasheet/pdf/d644f3ae7335586a805c6e9751c61823.pdf?productCode=C5224030) gives nominal 0.65 × 0.40 mm leads and a 1.02 mm recommended hole; the retained header footprint has 1.00 mm holes. The nominal lead diagonal is 0.763 mm, so the retained holes provide nominal clearance, but finished-hole and lead tolerances and socket engagement must be checked physically before fabrication approval. The generic STEP preview is not a supplier solid.

## Drain choke sourcing conflict

L61 retains the approved **25-turn FT37-43** drain choke and the source project's 5.08 mm upright footprint while procurement is pending. With Amidon's listed `AL = 350 nH/turn²`, nominal inductance is `350 nH × 25² = 218.75 µH`; the RF impedance under bias is not determined by that low-frequency nominal value. [Amidon 43-material table](https://www.amidoncorp.com/43-material-ferrite-toroids/)

No exact stocked LCSC FT37-43 core was verified. **A sourcing exception has not been approved.** Bourns **SRR7045-221M** is a possible SMT engineering candidate, but its [manufacturer specification](https://datasheet.lcsc.com/datasheet/pdf/4a05bf4afa36246babbe8de909ebf276.pdf?productCode=C3220878) gives 220 µH, ±20%, 0.69 Ω maximum DCR, 0.40 A typical saturation current and 4.5 MHz typical self resonance. The accessible LCSC stock evidence is insufficient to release it as an assured replacement, and its inductance alone does not establish 2 m suitability. Do not silently replace the winding with a generic 220 µH power inductor. An LCSC-only alternative requires a drain-feed redesign and biased LF/HF/VHF impedance and amplifier measurements.

## Source amplifier reference mapping

The placed schematic uses the following unique references. This mapping preserves the source topology plan while avoiding collisions with the clock section:

| GPIO source references | Synth references | Function |
| --- | --- | --- |
| U21 | U51 | TPS22918 |
| C21 / C22 / C23 | C51 / C52 / C53 | Input bulk / CT / switched bulk |
| C32 | C65 | Bias bypass |
| C31 | C61 | RF input coupling |
| C41 / C42 | C62 / C63 | Drain-feed bypass |
| C51 | C64 | RF output coupling |
| R21 / R22 | R51 / R52 | AMP_EN pull-down / QOD |
| R31 / R32 / R33 | R61 / R62 / R63 | Gate damping / bias feed / gate return |
| Q41 / L41 / RV31 | Q61 / L61 / RV61 | MOSFET / choke / trimmer |
| J51 / JP1 | J61 / JP51 | SMA / manual bias bypass |
| D11 / R11 | D81 / R82 | LED / 1 kΩ current limiter |

TCXO, Si5351, regulator, amplifier, counter and control symbols are now placed with these references. The wired schematic passes ERC; PCB synchronization, placement and routing remain pending. [SYMBOL-SOURCES.md](SYMBOL-SOURCES.md) records the definitions and decade-series placement.

## Supplier availability

The following are the inventory numbers shown by the inspected LCSC pages on 2026-10-06. They are supplier-page snapshots, sometimes served from cached pages, and are not reserved stock or proof of JLCPCB assembly availability. Recheck exact MPN, inventory and assembler support before ordering. Out-of-stock UNI-ROYAL C21190/C25804 were rejected in favor of stocked FOJAN 1 kΩ/10 kΩ parts. No substitute may change dielectric, pin map or ordering variant automatically.

| LCSC | Manufacturer | Ordering code | Stock shown |
| --- | --- | --- | --- |
| [C253672](https://www.lcsc.com/product-detail/C253672.html) | KDS | 1XTW25000MAA | 507 |
| [C504891](https://www.lcsc.com/product-detail/C504891.html) | Skyworks / Silicon Labs | SI5351A-B-GTR | 32922 |
| [C2862740](https://www.lcsc.com/product-detail/C2862740.html) | Texas Instruments | TPS7A2033PDBVR | 201955 |
| [C131941](https://www.lcsc.com/product-detail/C131941.html) | Texas Instruments | TPS22918DBVR | 11865 |
| [C3827808](https://www.lcsc.com/product-detail/C3827808.html) | LSI/CSI | LS7366R-S | 577 |
| [C7835](https://www.lcsc.com/product-detail/C7835.html) | Texas Instruments | SN74LVC1G14DBVR | 310340 |
| [C111691](https://www.lcsc.com/product-detail/C111691.html) | onsemi | BS170 | 13960 |
| [C719177](https://www.lcsc.com/product-detail/C719177.html) | Bourns | TC33X-2-502E | 12785 |
| [C496551](https://www.lcsc.com/product-detail/C496551.html) | BAT WIRELESS | BWSMA-KWE-Z001 — superseded J61 selection | 141173 |
| [C5224030](https://www.lcsc.com/product-detail/C5224030.html) | ZHOURI | PM2.54-1*20 | 2055 |
| [C455280](https://www.lcsc.com/product-detail/C455280.html) | XUNPU | TS-1088R-02026 | 159150 |
| [C2286](https://www.lcsc.com/product-detail/C2286.html) | Hubei KENTO Elec | KT-0603R | 2607700 |
| [C1589](https://www.lcsc.com/product-detail/C1589.html) | Samsung Electro-Mechanics | CL10B103KB8NNNC | 1684250 |
| [C77026](https://www.lcsc.com/product-detail/C77026.html) | Murata | GRM1885C1H102JA01D | 116800 |
| [C14663](https://www.lcsc.com/product-detail/C14663.html) | YAGEO | CC0603KRX7R9BB104 | 6123450 |
| [C364318](https://www.lcsc.com/product-detail/C364318.html) | Samsung Electro-Mechanics | CL21B225KAFNFNE | 4240 |
| [C77093](https://www.lcsc.com/product-detail/C77093.html) | Murata | GRM31CR71E106KA12L | 200000 |
| [C726584](https://www.lcsc.com/product-detail/C726584.html) | YAGEO | AC0805KKX7R9BB105 | 1985310 |
| [C170182](https://www.lcsc.com/product-detail/C170182.html) | Walsin | 1206N104J500CT | 158585 |
| [C23162](https://www.lcsc.com/product-detail/C23162.html) | UNI-ROYAL | 0603WAF4701T5E | 11600800 |
| [C25803](https://www.lcsc.com/product-detail/C25803.html) | UNI-ROYAL | 0603WAF1003T5E | 14346400 |
| [C23345](https://www.lcsc.com/product-detail/C23345.html) | UNI-ROYAL | 0603WAF220JT5E | 5914300 |
| [C2907002](https://www.lcsc.com/product-detail/C2907002.html) | FOJAN | FRC0603F1001TS | 10606600 |
| [C2906982](https://www.lcsc.com/product-detail/C2906982.html) | FOJAN | FRC0603F1002TS | 3080500 |
| [C23140](https://www.lcsc.com/product-detail/C23140.html) | UNI-ROYAL | 0603WAF330JT5E | 3573200 |

Live LCSC pages checked on **2026-10-08** showed **9,872 ATGM336H-5N31 / C90770** receivers and **12,690 LQW18AN47NG00D / C98076** 47 nH chokes. These are availability snapshots, not reserved inventory. The prior JST connector and QLG3 socket/header are no longer purchasing requirements.

## Footprint and circuit validation

All selected board footprints exist in the independent `${KIPRJMOD}` library; [LIBRARY-SOURCES.md](LIBRARY-SOURCES.md) records origins, dimensions, custom changes and model gaps. A separate footprint fixture checks library geometry with the project's existing rules. These checks do not wire the circuit or establish physical/RF performance. See [VALIDATION.md](VALIDATION.md) for current results and remaining acceptance work.
