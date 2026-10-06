# Synth shield symbol sources and placement

The 2026-10-06 schematic placement contains **53 component symbols** in eight decade-series boxes, following the GPIO Pico shield's titled-box style. It includes the existing U11 electrical Pico interface, J11/J12 purchasing descriptions and 50 newly placed parts from [PARTS.csv](PARTS.csv). A3 provides room for subsequent wiring. No wires, labels, junctions or no-connect flags were added, and the PCB was not synchronized.

The two existing library definitions are preserved. Seventeen standalone definitions were added to `wsprrypico-synth-shield.kicad_sym` and the schematic cache; no new symbol depends on another project's library or a global library nickname. Instances carry selected values, technologies/dielectrics, ratings, tolerances, manufacturer, MPN, `LCSC Part #`, supplier link, assembly method and selection status. Physical instances use the selected local footprints. J11/J12 remain pinless, off-board descriptions; U11 owns their combined pad rows.

## Copied and adapted symbols

| Local definitions | Origin | Adaptation |
| --- | --- | --- |
| C, R, L, LED, R_Potentiometer_US, BS170 | GPIO Pico local C_0603, R_0603, L, LED, R_Potentiometer_US and BS170; ultimately KiCad Device/Transistor_FET symbols | Standalone copies; supplier-specific passive defaults removed, instance metadata supplied from the inventory; capacitor/resistor filters corrected for the selected local footprint names |
| TPS22918 | GPIO Pico local TPS22918 | Retain the donor's six-pin topology and drawing; switch specification and footprint assigned per instance |
| SMA | GPIO Pico SMA_Adafruit_1865, derived from KiCad Conn_Coaxial_Small | Retain the generic two-pin coaxial symbol; selected BAT WIRELESS purchasing/footprint data replaces the donor connector data |
| SW_Push, SolderJumper_2_Open, Conn_01x05 | Installed KiCad 10.0.6 Switch, Jumper and Connector_Generic libraries | Selected two-terminal switch, copper jumper and five-position GPS header; exact local footprint assignments/filtering |
| Si5351A | KiCad Oscillator:Si5351A-B-GT | Retain MSOP-10 pins; reference prefix U and selected SI5351A-B-GTR ordering code assigned per instance |
| TPS7A2033PDBVR | KiCad Regulator_Linear:TPS7A20xxxDBV | Flatten inherited LP5907MFX-1.2 geometry into a standalone symbol; verify DBV pins 1 IN, 2 GND, 3 EN, 4 NC, 5 OUT against [TI's datasheet](https://www.ti.com/lit/gpn/tps7a20) |
| SN74LVC1G14DBVR | KiCad 74xGxx:SN74LVC1G14DBV | Flatten inherited 74LVC1G14 geometry; retain pins 1 NC, 2 input, 3 GND, 4 output, 5 VCC |

Copied/adapted KiCad graphics retain [CC BY-SA 4.0 with the KiCad library exception](KICAD-LIBRARY-LICENSE.md). The source GPIO assets and their prior provenance are documented in [the Zero BS170 library notes](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md). Repository-owned donor work retains its original MIT terms.

## Original symbols

KDS_DSB321SDN_25MHz, LS7366R_S and PowerSelector are original MIT-licensed symbols drawn for this project. The KDS part uses four separate physical pins: **1/2 GND, 3 OUT, 4 VCC**, following the [exact specification](https://datasheet.lcsc.com/datasheet/pdf/4560f1646e80e1d25a345e540c19e02b.pdf?productCode=C253672). The LS7366R-S uses the manufacturer's 14-pin map, with **LFLAG pin 8 open drain**, **DFLAG pin 9 push-pull** and MISO tristate, following the [LSI/CSI datasheet](https://lsicsi.com/wp-content/uploads/2021/06/LS7366R.pdf). PowerSelector labels **1 VBUS, 2 shared IN, 3 VSYS**; its footprint supplies the default 1–2 copper link. The placement adds no electrical connections between these pins.

## Placement and exclusions

| Series | Function |
| --- | --- |
| 10 | Pico electrical interface and manual sockets |
| 20 | TCXO, reference coupling and local bypass |
| 30 | Si5351A, bypass and I²C pull-ups |
| 40 | Shared power selector and clock regulator |
| 50 | Amplifier supply switch, support parts and manual bias bypass |
| 60 | BS170 amplifier, gate bias, drain feed and DC-blocked SMA output |
| 70 | GPS header, counter, PPS conditioner and support parts |
| 80 | Button, LED and support parts |

All headers, SMA and hand-wound inductors are excluded from BOM and positions; the manual BS170 and copper features retain their exclusions. The 44 SMT instances agree with the inventory's assembly filter. Existing symbol/pin UUIDs, the Pico symbol definition, PCB, project settings, footprint library and models are preserved. The L61 source and control GPIO/behavior choices remain open. [VALIDATION.md](VALIDATION.md) records current ERC, physical DRC, expected schematic/PCB differences and visual inspection. Placement and pin/pad checks do not establish a wired circuit, assembly fit or RF performance.
