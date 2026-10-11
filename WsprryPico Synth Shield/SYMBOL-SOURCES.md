# Synth shield symbol sources

All active symbol definitions resolve through the independent `wsprrypico-synth-shield` library and [project-local table](sym-lib-table). The library contains exactly **20 used definitions**, including GND and PWR_FLAG. The schematic contains **48 non-power component symbols in seven blocks**, including the two schematic-only socket descriptions. The [README block and pin tables](README.md#hardware) and [component inventory](PARTS.csv) identify their current roles and ordering codes.

## Copied and adapted KiCad symbols

These graphics originate in KiCad 10.0.6 and retain **CC BY-SA 4.0 with the KiCad library exception**, documented in [KICAD-LIBRARY-LICENSE.md](KICAD-LIBRARY-LICENSE.md). Copies from the [GPIO shield](../WsprryPico%20GPIO%20Shield/README.md) retain its existing provenance and the [Zero amplifier source notes](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md).

| Local definitions | Origin and function |
| --- | --- |
| C, R, L, LED, R_Potentiometer_US, BS170 | KiCad passive/transistor graphics via the GPIO shield; supplier fields are set per component |
| VLS6045EX_331M | Device:L graphics with TDK 330 µH defaults and local SMT footprint |
| TPS22918 | GPIO shield's six-pin load-switch drawing and pin map |
| SMA, U_FL | Conn_Coaxial_Small-derived two-terminal signal/shield graphics |
| SW_Push | KiCad Switch momentary pushbutton |
| TestPoint | KiCad Connector test point; copper feature excluded from BOM/positions |
| Si5351A | Oscillator:Si5351A-B-GT, 10-pin MSOP |
| TPS7A2033PDBVR | Regulator_Linear:TPS7A20xxxDBV; inherited graphics flattened into a standalone local definition |
| GND, PWR_FLAG | KiCad power symbols |

U21 uses pins 1 IN, 2 GND, 3 EN, 4 NC and 5 OUT. U31 uses 1 VIN, 2 GND, 3 ON, 4 CT, 5 QOD and 6 VOUT. Q61 uses 1 drain, 2 gate and 3 source. RV61 pin 2 is the wiper and pin 3 the clockwise end. Exact connected nets are recorded in [circuit details](TCXO-SI5351A-DESIGN.md).

Generic C and R definitions keep ordering data in each placed instance because their values and manufacturers vary. The project-specific trimmer definition defaults to Bourns TC33X-2-502E / C719177 and its local footprint. Verified supplier fields are shared by the schematic, PCB and [parts inventory](PARTS.csv); the [collection workbook](LCSC-parts-collection.xlsx) contains the corresponding editable entries.

## Original symbols

Original project graphics follow [LICENSE.md](LICENSE.md). Manufacturer references establish electrical pin functions rather than granting a license to reproduce their drawings.

- **KDS_DSB321SDN_25MHz:** Y41, with pins 1/2 GND, 3 OUT and 4 VCC, from the [exact KDS specification](https://datasheet.lcsc.com/datasheet/pdf/4560f1646e80e1d25a345e540c19e02b.pdf?productCode=C253672).
- **ATGM336H_5N31:** U71's receiver pin map from the [module manual](https://www.lcsc.com/datasheet/C90770.pdf).
- **Raspberry_Pi_Pico_2W:** combined 40-pin electrical interface U11, with independent schematic-only J11/J12 purchasing descriptions in **Socket_1x20_P2.54mm_BOM**, from the [local Pico reference assets](../Pico%202W%20Wattmeter%20Shield/pico-2w-libs/README.md).

## Assembly and validation

J11/J12 have no separate PCB footprints; U11 owns both socket rows. Manual parts and test points retain their exclusions from automated assembly outputs. All selected physical parts have local footprints. See [current ERC/DRC results and outstanding findings](VALIDATION.md).
