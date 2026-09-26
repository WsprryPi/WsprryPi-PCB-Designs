# Local library sources and licensing

The `wsprrypi-zero-gpio` symbol and footprint libraries are project-local. Their entries must continue to use the `wsprrypi-zero-gpio:` nickname and `${KIPRJMOD}` library-table paths.

## Template assets

The Raspberry Pi interface, 2×20 socket purchasing symbol, selectable socket footprint, and grouped `Dual_PinSocket_1x04_P2.54mm_J81_J82` symbol and footprint came from the repository's `RPi Zero HAT` template. The grouped LPF header was subsequently adjusted to the current `Wsprry-Pi-LPF` board's exact 31.880 mm J1/J2 center spacing. Its hard keepout is intentionally limited to `F.Cu`, allowing the bottom-layer ground pour beneath the LPF; it is therefore no longer byte-identical to the template's older 32.020 mm, two-copper-layer version.

## Edge-launch SMA connector

`SMA_Adafruit_1865` and `SMA_Adafruit_1865_EdgeMount` were copied from the repository's `WsprryPi-GPIO-Univ` project and renamed only at the library-nickname boundary. The footprint remains byte-identical to that source. It derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library); the matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` under the KiCad library license. It is for an Adafruit 1865 standard-polarity female connector on a 1.6 mm board, with pin 1 signal and pin 2 ground. The current J1 instance is placed and routed, hand-soldered, excluded from BOM and position output, and has no attached 3D model.

## GPIO indicator assets

The `LED` and `R_US` symbols, `LED_0603_1608Metric` footprint, and LED STEP model were copied from `WsprryPi-GPIO-Univ` for the placed D11/R11 indicator circuit. D11 retains its `KT-0603W`/`LCSC_PART` C2286 fields and uses the project-local LED footprint. R11 retains its 220 ohm/`LCSC_PART` C22962 fields and uses this project's existing `R_0603_1608Metric` footprint, whose pad geometry matches the source footprint. The copied GND instance was redirected to the existing project-local `GND` symbol. No placed symbol or footprint now depends on the `Wsprry Pi` library nickname.

## 1×3 male header

`Conn_01x03`, `PinHeader_1x03_P2.54mm_Vertical`, and `PinHeader_1x03_P2.54mm_Vertical.step` were copied from `WsprryPi-GPIO-Univ` and redirected to the `wsprrypi-zero-gpio` nickname and project-local model directory. They derive from the standard KiCad connector symbol, 2.54 mm through-hole male-header footprint, and matching STEP model. The current J12 instance is placed and routed with pin 1 on GPIO4, pin 2 on `GPIO_RF`, and pin 3 on GPIO20. It is excluded from BOM and position output while remaining visible in the 3D board view.

## Tactile switch

`SKRPANE010` is an Alps Alpine top-actuated SPST-NO momentary tactile switch, identified by `LCSC_PART` C470426 and placed as SW11. The two-pin local symbol and duplicate-numbered footprint encode the switch's internal terminal grouping: logical pin/pad 1 represents manufacturer terminals 1 and 2, logical pin/pad 2 represents manufacturer terminals 3 and 4, and pressing the actuator bridges the two groups. The `ALPS_SKRP_4.2x3.2mm` footprint was drawn from Alps Alpine's published SKRP-series dimensions and recommended land pattern. Its four physical 1.05 × 0.65 mm lands use 4.15 mm horizontal and 2.15 mm vertical center spacing.

The local `ALPS_SKRP_4.2x3.2x2.5mm.step` model was converted from the EasyEDA/JLCPCB C470426 model with `easyeda2kicad` 1.0.1 and renamed without geometric modification. The supplier model is retained under its applicable source terms and is not relicensed by the repository's MIT license. Verify model alignment and physical fit before relying on the 3D view for enclosure or assembly decisions.

## BOM symbols

The following symbols were drawn or copied for this project from the named manufacturers' pin tables, package documentation, or identified source libraries. The local LTC6432-15 library master and current U32 schematic/PCB instances select `LTC6432AIUF-15#PBF`, `LCSC_PART` C689344. Project supplier-ordering metadata uses `LCSC_PART` exclusively; the legacy `LCSC` property is not used.

| Symbol | Source | Assigned local footprint |
| --- | --- | --- |
| `LTC6432-15` | [Analog Devices LTC6432-15 data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/643215f.pdf) | `Analog_UF24_QFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm_ThermalVias` |
| `YA9308-AEC` | [Coilcraft YA9308 data sheet](https://www.coilcraft.com/getmedia/508634a8-8a9d-4933-83b8-7660d3e9ca71/ya9308.pdf) | `Coilcraft_YA9308` |
| `TPS22918` | [Texas Instruments TPS22918 data sheet](https://www.ti.com/lit/ds/symlink/tps22918.pdf) | `SOT-23-6` |
| `24AA32A-I-ST` | [Microchip 24AA32A/24LC32A data sheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/24AA32A-24LC32A-32-Kbit-I2C-Serial-EEPROM-DS20001713.pdf) | `TSSOP-8_4.4x3mm_P0.65mm` |
| `R_0603` | Generic passive using the compact KiCad US zigzag convention | `R_0603_1608Metric` |
| `C_0603` | Generic passive | `C_0603_1608Metric` |
| `C_0805` | Generic passive | `C_0805_2012Metric` |
| `GND` | KiCad 10.0.6 standard GND power-symbol geometry, copied locally | None |
| `LED` | KiCad LED symbol copied through `WsprryPi-GPIO-Univ`; D11 is `KT-0603W`/`LCSC_PART` C2286 | `LED_0603_1608Metric` |
| `R_US` | KiCad US resistor symbol copied through `WsprryPi-GPIO-Univ`; R11 is 220 ohm/`LCSC_PART` C22962 | `R_0603_1608Metric` |
| `SKRPANE010` | [Alps Alpine SKRPANE010 product data](https://tech.alpsalpine.com/e/products/detail/SKRPANE010/) and terminal diagram | `ALPS_SKRP_4.2x3.2mm` |
| `Conn_01x03` | KiCad connector symbol copied through `WsprryPi-GPIO-Univ` | `PinHeader_1x03_P2.54mm_Vertical` |

`24AA32A-I/ST` and its TSSOP-8 footprint remain as unused, attributed local-library assets. They are not part of the current schematic, BOM, or selected design, which intentionally omits an identification EEPROM.

C21, C31, C32, C37, and C38 reuse the generic local `C_0805` capacitor symbol but override its default footprint with the project-local `C_1206_3216Metric` footprint. The shared symbol's footprint filter permits both project-local capacitor footprints while retaining `C_0805_2012Metric` as the default.

## BOM footprints

The SOT-23-6, TSSOP-8, 0603 resistor, 0603 capacitor, 0805 capacitor, and 1206 capacitor footprints are unmodified copies from the KiCad 10.0.6 standard footprint installation. Their standard `${KICAD10_3DMODEL_DIR}` references are retained. The 2.54 mm 1×3 male-header footprint is a KiCad library copy whose model reference was redirected to the project-local STEP file and whose BOM and position-output exclusions implement this project's library policy.

The Analog Devices UF24 footprint began from KiCad's `WQFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm_ThermalVias` geometry and was renamed and documented for the LTC6432-15. The 4 × 4 mm body, 0.5 mm pitch, and 2.45 × 2.45 mm exposed-pad land pattern agree with Analog Devices drawing 05-08-1697 Rev B. Its thermal-via pattern is an implementation candidate and must be reviewed against the selected fabricator's via, solder-mask, and paste-process capabilities.

The `Coilcraft_YA9308` footprint was drawn from Coilcraft Document 1581-2. It uses 0.76 × 1.14 mm lands, 1.52 mm pad pitch within each row, and 3.05 mm row-center spacing. No YA9308 3D model has been added.

The `ALPS_SKRP_4.2x3.2mm` footprint was drawn from the Alps Alpine SKRP-series recommended land pattern. The manufacturer drawing specifies a 5.2 mm horizontal outside span, 3.1 mm horizontal inside gap, 2.8 mm vertical outside span, and 1.5 mm vertical inside gap; these resolve to four 1.05 × 0.65 mm lands centered at X = ±2.075 mm and Y = ±1.075 mm. The courtyard includes the pads, 4.2 × 3.2 mm body, and 0.25 mm nominal clearance.

## KiCad library license

The copied and adapted KiCad symbols and footprints are licensed under the Creative Commons CC-BY-SA 4.0 License with the KiCad library exception. The adjacent [KiCad library license notice](KICAD-LIBRARY-LICENSE.md) applies to those imported assets. Manufacturer names, product names, and data sheets remain the property of their respective owners.

## Validation boundary

KiCad 10.0.6 successfully parsed and exported every local symbol and footprint after import. The device symbols and the two custom RF footprints were visually inspected from those exports. This validates library syntax and visible pin/pad organization only; it does not establish assembly fit, solderability, electrical correctness, RF performance, or HAT+ compliance.
