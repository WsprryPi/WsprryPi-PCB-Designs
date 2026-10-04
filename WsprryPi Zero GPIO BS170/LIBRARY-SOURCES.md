# Local library sources and licensing

The `wsprrypi-zero-gpio-bs170` symbol and footprint libraries are project-local. Their entries must continue to use the `wsprrypi-zero-gpio-bs170:` nickname and `${KIPRJMOD}` library-table paths.

## BS170 redesign additions

The following symbols, now placed as Q41, RV31, and L41, were copied from the standard symbol libraries installed with KiCad 10.0.6. They retain the KiCad library license below. Each includes the project's `Manufacturer`, `MPN`, and `LCSC_PART` fields; unselected purchasing fields remain blank.

| Local symbol | Source | Pins and footprint status |
| --- | --- | --- |
| `BS170` | `Transistor_FET:BS170`, with its inherited `BS107` geometry flattened into a standalone symbol | 1 = drain, 2 = gate, 3 = source; assigned local `TO-92_Inline` footprint for the straight-lead onsemi BS170 |
| `R_Potentiometer_US` | `Device:R_Potentiometer_US` | Passive pins 1 and 3 are the resistance ends; pin 2 is the wiper. Assigned local `Potentiometer_Bourns_TC33X_Vertical` footprint for Bourns TC33X-2-502E, 5 kΩ. |
| `L` | `Device:L` | Passive pins 1 and 2. Assigned local `L_Toroid_FT37-43_Vertical_P5.08mm` footprint for 25 turns on FT37-43; current and RF performance require measurement. |

The BS170 symbol retains the source pin types and drawing. Its manufacturer is onsemi, its MPN is `BS170`, and its data-sheet link points to the current [BS170/MMBF170 data sheet](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf). Its supplier field is blank; no availability or RF performance claim follows from adding the symbol. The straight-lead TO-92 assignment does not cover every formed-lead ordering variant or the SOT-23 MMBF170.

`TO-92_Inline.kicad_mod` was copied from KiCad's `Package_TO_SOT_THT.pretty` library. Only its model path changed, to `${KIPRJMOD}/wsprrypi-zero-gpio-bs170.3dshapes/TO-92_Inline.step`. Pad centers remain 1.27 mm apart, with 0.75 mm drills and the original pad, courtyard, and fabrication geometry. The matching standard KiCad STEP model was copied without modification.

The generic trimmer/inductor masters retain their source values (`R_Potentiometer_US` and `L`), with the selected footprints and physical-part metadata now assigned in both the local library and schematic cache. RV31 retains 5 kΩ; L41 now displays `25T FT37-43`. No pin geometry or numbering changed.

## Selected choke and trimmer footprints

`L_Toroid_FT37-43_Vertical_P5.08mm.kicad_mod` adapts the installed KiCad 10.0.6 `Inductor_THT:L_Toroid_Vertical_L10.0mm_W5.0mm_P5.08mm` footprint under the KiCad library license. It mounts the selected toroid upright. Pads 1/2 remain at (0, 0)/(0, 5.08) mm; their diameter increases from 2.0 to 2.4 mm and their drills from 1.0 to 1.2 mm for hand assembly. The fabrication outline depicts the bare FT37-43 board projection, 9.525 × 3.175 mm, centered at (0, 2.54) mm. `Dwgs.User` marks the maximum 11 × 5 mm wound-body projection, and the courtyard reserves 11.5 × 7.98 mm including the lead pads. Reference/value labels are outside the courtyard. Allow up to 11 mm wound-body height plus the mounting gap, and form the winding leads to the 5.08 mm pitch; this is a hand-formed lead arrangement, not a factory core pin specification. The source's generic 10 × 5 mm toroid model reference is removed because it does not establish the selected wound assembly's geometry. The footprint has through-hole mounting and automated BOM/position exclusions; L41 retains matching exclusions and both electrical pins in the netlist.

The superseded `L_Toroid_FT37-43_Horizontal_P15.00mm` local asset is retained for the currently saved PCB's L41 instance. It was adapted from KiCad's `Inductor_THT:L_Toroid_Horizontal_D9.5mm_P15.00mm_Diameter10-5mm_Amidon-T37` under the same library license. Update L41 on the PCB from the schematic to adopt the upright footprint; this change does not alter the user's current PCB placement or routing.

The [Amidon FT37-43 specification](https://www.amidoncorp.com/ft-37-43/) gives 0.375 inch outside diameter, 0.187 inch inside diameter, 0.125 inch height, and nominal A_L = 350 nH/turn². The comparable [Fair-Rite 5943000201 dimensions and tolerances](https://fair-rite.com/product/toroids-5943000201/) support the envelope review. The selected 25-turn winding follows the [QRP Labs Ultimate3S assembly manual](https://www.qrp-labs.com/images/ultimate3s/assembly.pdf). Starting 0.32 mm enamelled wire fits within the reserved envelope on dimensional estimates; physical wound fit and RF behavior remain to be checked. No rated-current or VHF-impedance claim follows from footprint assignment.

`Potentiometer_Bourns_TC33X_Vertical.kicad_mod` is copied from the installed KiCad 10.0.6 `Potentiometer_SMD` library, with all lands, drawing geometry, and UUIDs retained. Pads 1/3 are 1.2 × 1.2 mm at (-1.8, -1.0)/(-1.8, 1.0) mm; wiper pad 2 is 1.5 × 1.6 mm at (1.45, 0) mm. Lands and terminal numbering were compared with the [Bourns TC33 drawing](https://www.bourns.com/docs/Product-Datasheets/TC33.pdf). RV31 selects the rotational-stop TC33X-2-502E variant, 5 kΩ, 0.15 W, with [JLCPCB/LCSC identifier C719177](https://jlcpcb.com/partdetail/BOURNS-TC33X_2502E/C719177). The referenced standard `Potentiometer_Bourns_TC33X_Vertical.step` file is absent from this KiCad installation, so its unresolved model reference is removed from the local copy. A project-local illustrative VRML model is now attached. Stock and assembly price remain ordering-time checks.

`FT37-43_25T_Upright.wrl` is an original, repository-MIT-licensed visualization generated by [generate_ft37_43.py](wsprrypi-zero-gpio-bs170.3dshapes/generate_ft37_43.py). It uses the [Amidon FT37-43 dimensions](https://www.amidoncorp.com/ft-37-43/) (9.525 mm OD, 4.7498 mm ID, 3.175 mm thickness), 25 illustrative turns of 0.32 mm wire, a 0.5 mm winding-to-board gap, and hand-formed leads to the existing 5.08 mm pad pitch. The approximate wound body is 10.17 mm wide, 3.82 mm deep, and 10.67 mm high above the PCB. It is attached to both the local upright footprint and saved L41 instance. L41 stays excluded from BOM and position output. This VRML mesh supports KiCad 3D viewing; it is not a STEP solid for MCAD export or a measured assembly model. Physical wound fit, insulation, mounting stability, height clearance, and RF performance remain unqualified. RV31 now has a project-local illustrative 3D model.

## Template assets

The Raspberry Pi interface, 2×20 socket purchasing symbol, selectable socket footprint, and grouped `Dual_PinSocket_1x04_P2.54mm_J81_J82` symbol and footprint came from the repository's `RPi Zero HAT Template`. The grouped LPF header was subsequently adjusted to the current `WsprryPi LPF` board's exact 33.020 mm J1/J2 center spacing. Its hard keepout is intentionally limited to `F.Cu`, allowing the bottom-layer ground pour beneath the LPF; it is therefore no longer byte-identical to the template's older 32.020 mm, two-copper-layer version.

## Edge-launch SMA connector

`SMA_Adafruit_1865` and `SMA_Adafruit_1865_EdgeMount` were copied from the repository's `WsprryPi-GPIO-Univ` project and renamed only at the library-nickname boundary. The footprint remains byte-identical to that source. It derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library); the matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` under the KiCad library license. It is for an Adafruit 1865 standard-polarity female connector on a 1.6 mm board, with pin 1 signal and pin 2 ground. The current J51 instance is placed and routed, hand-soldered, excluded from BOM and position output, and has no attached 3D model.

## GPIO indicator assets

The `LED` and `R_US` symbols, `LED_0603_1608Metric` footprint, and LED STEP model were copied from `WsprryPi-GPIO-Univ` for the placed D11/R11 indicator circuit. D11 retains its `KT-0603W`/`LCSC_PART` C2286 fields and uses the project-local LED footprint. R11 retains its 220 ohm/`LCSC_PART` C22962 fields and uses this project's existing `R_0603_1608Metric` footprint, whose pad geometry matches the source footprint. The copied GND instance was redirected to the existing project-local `GND` symbol. No placed symbol or footprint now depends on the `Wsprry Pi` library nickname.

## 1×3 male header

`Conn_01x03`, `PinHeader_1x03_P2.54mm_Vertical`, and `PinHeader_1x03_P2.54mm_Vertical.step` were copied from `WsprryPi-GPIO-Univ` and redirected to the `wsprrypi-zero-gpio-bs170` nickname and project-local model directory. They derive from the standard KiCad connector symbol, 2.54 mm through-hole male-header footprint, and matching STEP model. The current J12 instance is placed and routed with pin 1 on GPIO4, pin 2 on `GPIO_RF`, and pin 3 on GPIO20. It is excluded from BOM and position output while remaining visible in the 3D board view.

## Tactile switch

`SKRPANE010` is an Alps Alpine top-actuated SPST-NO momentary tactile switch, identified by `LCSC_PART` C470426 and placed as SW11. The two-pin local symbol and duplicate-numbered footprint encode the switch's internal terminal grouping: logical pin/pad 1 represents manufacturer terminals 1 and 2, logical pin/pad 2 represents manufacturer terminals 3 and 4, and pressing the actuator bridges the two groups. The `ALPS_SKRP_4.2x3.2mm` footprint was drawn from Alps Alpine's published SKRP-series dimensions and recommended land pattern. Its four physical 1.05 × 0.65 mm lands use 4.15 mm horizontal and 2.15 mm vertical center spacing.

The local `ALPS_SKRP_4.2x3.2x2.5mm.step` model was converted from the EasyEDA/JLCPCB C470426 model with `easyeda2kicad` 1.0.1 and renamed without geometric modification. The supplier model is retained under its applicable source terms and is not relicensed by the repository's MIT license. Verify model alignment and physical fit before relying on the 3D view for enclosure or assembly decisions.

## BOM symbols

The following symbols were drawn or copied for this project from the named manufacturers' pin tables, package documentation, or identified source libraries. The local LTC6432-15 library master and copied PCB U31 instance select `LTC6432AIUF-15#PBF`, `LCSC_PART` C689344. Project supplier-ordering metadata uses `LCSC_PART` exclusively; the legacy `LCSC` property is not used.

| Symbol | Source | Assigned local footprint |
| --- | --- | --- |
| `LTC6432-15` | [Analog Devices LTC6432-15 data sheet](https://www.analog.com/media/en/technical-documentation/data-sheets/643215f.pdf) | `Analog_UF24_QFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm_ThermalVias` |
| `YA9308-AEC` | [Coilcraft YA9308 data sheet](https://www.coilcraft.com/getmedia/508634a8-8a9d-4933-83b8-7660d3e9ca71/ya9308.pdf) | `Coilcraft_YA9308` |
| `WBC2-1TLC` | [Coilcraft WBC data sheet](https://www.coilcraft.com/getmedia/f685d903-2563-4c96-8ba6-f82a58883aeb/wbc.pdf), [LCSC C19191658](https://www.lcsc.com/product-detail/C19191658.html) | `Coilcraft_WBC2-1TLC` |
| `TPS22918` | [Texas Instruments TPS22918 data sheet](https://www.ti.com/lit/ds/symlink/tps22918.pdf) | `SOT-23-6` |
| `24AA32A-I-ST` | [Microchip 24AA32A/24LC32A data sheet](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/24AA32A-24LC32A-32-Kbit-I2C-Serial-EEPROM-DS20001713.pdf) | `TSSOP-8_4.4x3mm_P0.65mm` |
| `R_0603` | Generic passive using the compact KiCad US zigzag convention | `R_0603_1608Metric` |
| `R_0805` | Copy of the local `R_0603` symbol with the 0805 default footprint and filter; R41 is 0 Ω | `R_0805_2012Metric` |
| `C_0603` | Generic passive | `C_0603_1608Metric` |
| `C_0805` | Generic passive | `C_0805_2012Metric` |
| `GND` | KiCad 10.0.6 standard GND power-symbol geometry, copied locally | None |
| `LED` | KiCad LED symbol copied through `WsprryPi-GPIO-Univ`; D11 is `KT-0603W`/`LCSC_PART` C2286 | `LED_0603_1608Metric` |
| `R_US` | KiCad US resistor symbol copied through `WsprryPi-GPIO-Univ`; R11 is 220 ohm/`LCSC_PART` C22962 | `R_0603_1608Metric` |
| `SKRPANE010` | [Alps Alpine SKRPANE010 product data](https://tech.alpsalpine.com/e/products/detail/SKRPANE010/) and terminal diagram | `ALPS_SKRP_4.2x3.2mm` |
| `Conn_01x03` | KiCad connector symbol copied through `WsprryPi-GPIO-Univ` | `PinHeader_1x03_P2.54mm_Vertical` |

`24AA32A-I/ST` and its TSSOP-8 footprint remain as unused, attributed local-library assets. They are not part of the current schematic, BOM, or selected design, which intentionally omits an identification EEPROM.

The copied PCB retains 1206 capacitors from the baseline. In the new schematic RF stage, C31/C32/C41/C51 use `C_0603` and the local 0603 footprint, while C42 uses `C_0805` and the local 0805 footprint. The `C_1206_3216Metric` baseline footprint remains in the library.

## BOM footprints

On 2026-10-02, `R_0805_2012Metric.kicad_mod` was copied without modification from the KiCad 10.0.6 `Resistor_SMD.pretty` library. R41 uses the new local `R_0805` symbol, value `0Ω`, and `wsprrypi-zero-gpio-bs170:R_0805_2012Metric`. Its two passive pins and schematic connections are preserved. The standard installed KiCad 0805 resistor STEP-model reference is retained; supplier fields are unselected. The KiCad library license below covers this imported footprint and the derived symbol.

The SOT-23-6, TSSOP-8, 0603 resistor, 0603 capacitor, 0805 capacitor, and 1206 capacitor footprints are unmodified copies from the KiCad 10.0.6 standard footprint installation. Their standard `${KICAD10_3DMODEL_DIR}` references are retained. The 2.54 mm 1×3 male-header footprint is a KiCad library copy whose model reference was redirected to the project-local STEP file and whose BOM and position-output exclusions implement this project's library policy.

The Analog Devices UF24 footprint began from KiCad's `WQFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm_ThermalVias` geometry and was renamed and documented for the LTC6432-15. The 4 × 4 mm body, 0.5 mm pitch, and 2.45 × 2.45 mm exposed-pad land pattern agree with Analog Devices drawing 05-08-1697 Rev B. Its thermal-via pattern is an implementation candidate and must be reviewed against the selected fabricator's via, solder-mask, and paste-process capabilities.

The `Coilcraft_YA9308` footprint was drawn from Coilcraft Document 1581-2. It uses 0.76 × 1.14 mm lands, 1.52 mm pad pitch within each row, and 3.05 mm row-center spacing. No YA9308 3D model has been added.

The baseline `WBC2-1TLC` symbol and `Coilcraft_WBC2-1TLC` footprint were drawn from Coilcraft WBC Document 424-1/424-2. Pins 4 and 6 are the primary; pin 5 is unconnected. Pins 1 and 3 are the secondary ends; pin 2 is the center tap. The dedicated footprint uses Coilcraft's recommended 0.76 × 1.14 mm lands, 1.52 mm pad pitch within each row, and 3.05 mm row-center spacing. Its geometry matches the existing YA9308 footprint, but its separate name and part metadata keep the two devices distinct. The library symbol records `LCSC_PART` C19191658. No WBC 3D model has been added. T21 and T41 remain on the copied PCB but are removed from the schematic. RF performance and assembly suitability remain unqualified; the two-transformer implementation has since been rejected on cost grounds.

The `ALPS_SKRP_4.2x3.2mm` footprint was drawn from the Alps Alpine SKRP-series recommended land pattern. The manufacturer drawing specifies a 5.2 mm horizontal outside span, 3.1 mm horizontal inside gap, 2.8 mm vertical outside span, and 1.5 mm vertical inside gap; these resolve to four 1.05 × 0.65 mm lands centered at X = ±2.075 mm and Y = ±1.075 mm. The courtyard includes the pads, 4.2 × 3.2 mm body, and 0.25 mm nominal clearance.

## KiCad library license

The copied and adapted KiCad symbols and footprints are licensed under the Creative Commons CC-BY-SA 4.0 License with the KiCad library exception. The adjacent [KiCad library license notice](KICAD-LIBRARY-LICENSE.md) applies to those imported assets. Manufacturer names, product names, and data sheets remain the property of their respective owners.

## Validation boundary

KiCad 10.0.6 successfully parsed and exported all 20 local symbols and 17 local footprints after the BS170 additions. The three new symbols and TO-92 footprint were visually inspected, and their pin/pad mapping was checked against the source assets. All 17 pre-existing symbols, the saved schematic, PCB, project settings, and library tables remained byte-for-byte unchanged during that import. At that time, the schematic reported 0 ERC errors and one expected isolated `GPIO_RF` warning. The subsequent placement of eleven unwired parts is documented in the [project validation notes](README.md#validation-and-limits); it did not change the local library definitions. On 2026-10-01, two selected footprints were imported and L31/RV21 metadata assigned in the library and schematic cache. KiCad 10.0.6 exported all 19 local footprints; the new footprints and updated schematic were visually inspected. All 24 physical schematic parts resolve locally; pin/pad sets match and netlist connectivity is unchanged. At that footprint-assignment stage, ERC reported 14 errors and 2 warnings from incomplete input/bias wiring. The PCB, project settings, library tables, existing footprints, symbol/pin UUIDs, and electrical drawing objects are unchanged by this update. No PCB DRC was rerun. Library export and inspection validate syntax and visible pin/pad organization only; they do not establish assembly fit, solderability, electrical correctness, RF performance, or HAT+ compliance.

The user-selected upright L31 revision on 2026-10-01 adds the vertical toroid footprint and changes only the L31/master footprint and description properties in the schematic and symbol library. KiCad 10.0.6 exported the new footprint and saved schematic for visual inspection; ERC before and after reported **0 errors and 0 warnings** with existing ignored checks preserved. The before/after netlists have identical connectivity. All 24 physical symbols resolve locally with matching pin/pad numbers. The user's saved PCB, project settings, library tables, and existing footprint/model assets were unchanged by this revision; the current PCB's horizontal L31 instance still needs updating from the schematic. Physical wound fit, mounting stability, height clearance, and RF performance remain unqualified.

## RV31 and J51 3D visualization

`TC33X_Preview.wrl` and `SMA_Adafruit_1865_Preview.wrl` are original repository-MIT-licensed models attached to both the local footprint masters and the saved PCB through `${KIPRJMOD}`. The trimmer follows the footprint fabrication outline (3.8 × 3.0 mm), with an illustrative 1.6 mm height and adjustment disk. The SMA follows its existing fabrication outline: 6.5 mm flange, 6.1 mm barrel diameter, 9.5 mm forward reach, and 3.9 mm rear fingers straddling the 1.6 mm board. Heights, threads, internal details, and tolerances are simplified assumptions; these are visualizations, not supplier CAD or clearance qualification. The SMA points outward along footprint +Y; terminal fingers align with its pads. Placement, copper, connectivity, and settings are preserved.

The original visualization meshes can be regenerated with `python3 wsprrypi-zero-gpio-bs170.3dshapes/generate_rv31_j51.py` from the project directory. KiCad 10.0.6 DRC before and after model attachment reported 0 violations and 0 unconnected items without refilling or saving zones; both models were visually inspected in a 3D render.
