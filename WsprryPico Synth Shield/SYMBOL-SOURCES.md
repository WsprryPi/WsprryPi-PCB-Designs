# Synth shield symbol sources and placement

The 2026-10-06 schematic placement contains **53 component symbols** in eight decade-series boxes, following the GPIO Pico shield's titled-box style. It includes the existing U11 electrical Pico interface, J11/J12 purchasing descriptions and 50 newly placed parts from [PARTS.csv](PARTS.csv). A3 provides room for subsequent wiring. No wires, labels, junctions or no-connect flags were added, and the PCB was not synchronized.

The two existing library definitions are preserved. Seventeen standalone definitions were added to `wsprrypico-synth-shield.kicad_sym` and the schematic cache; no new symbol depends on another project's library or a global library nickname. Instances carry selected values, technologies/dielectrics, ratings, tolerances, manufacturer, MPN, `LCSC Part #`, supplier link, assembly method and selection status. Physical instances use the selected local footprints. J11/J12 remain pinless, off-board descriptions; U11 owns their combined pad rows.

## Copied and adapted symbols

| Local definitions | Origin | Adaptation |
| --- | --- | --- |
| C, R, L, LED, R_Potentiometer_US, BS170 | GPIO Pico local C_0603, R_0603, L, LED, R_Potentiometer_US and BS170; ultimately KiCad Device/Transistor_FET symbols | Standalone copies; supplier-specific passive defaults removed, instance metadata supplied from the inventory; capacitor/resistor filters corrected for the selected local footprint names |
| TPS22918 | GPIO Pico local TPS22918 | Retain the donor's six-pin topology and drawing; switch specification and footprint assigned per instance |
| SMA | GPIO Pico SMA_Adafruit_1865, derived from KiCad Conn_Coaxial_Small | Retain the generic two-pin coaxial symbol; selected BAT WIRELESS purchasing/footprint data replaces the donor connector data |
| SW_Push, SolderJumper_2_Open, SolderJumper_3_Bridged12, Conn_01x05 | Installed KiCad 10.0.6 Switch, Jumper and Connector_Generic libraries | Selected switch, copper jumpers and five-position GPS header; exact local footprint assignments/filtering. JP41 uses the stock SolderJumper_3_Bridged12 drawing and pins; its local definition excludes position output and selects the existing cuttable footprint |
| Si5351A | KiCad Oscillator:Si5351A-B-GT | Retain MSOP-10 pins; reference prefix U and selected SI5351A-B-GTR ordering code assigned per instance |
| TPS7A2033PDBVR | KiCad Regulator_Linear:TPS7A20xxxDBV | Flatten inherited LP5907MFX-1.2 geometry into a standalone symbol; verify DBV pins 1 IN, 2 GND, 3 EN, 4 NC, 5 OUT against [TI's datasheet](https://www.ti.com/lit/gpn/tps7a20) |
| SN74LVC1G14DBVR | KiCad 74xGxx:SN74LVC1G14DBV | Flatten inherited 74LVC1G14 geometry; retain pins 1 NC, 2 input, 3 GND, 4 output, 5 VCC |

Copied/adapted KiCad graphics retain [CC BY-SA 4.0 with the KiCad library exception](KICAD-LIBRARY-LICENSE.md). The source GPIO assets and their prior provenance are documented in [the Zero BS170 library notes](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md). Repository-owned donor work retains its original MIT terms.

## Original symbols

KDS_DSB321SDN_25MHz and LS7366R_S are original MIT-licensed symbols drawn for this project. The KDS part uses four separate physical pins: **1/2 GND, 3 OUT, 4 VCC**, following the [exact specification](https://datasheet.lcsc.com/datasheet/pdf/4560f1646e80e1d25a345e540c19e02b.pdf?productCode=C253672). The LS7366R-S uses the manufacturer's 14-pin map, with **LFLAG pin 8 open drain**, **DFLAG pin 9 push-pull** and MISO tristate, following the [LSI/CSI datasheet](https://lsicsi.com/wp-content/uploads/2021/06/LS7366R.pdf).

## Placement and exclusions

On 2026-10-07, JP41 was replaced with **wsprrypico-synth-shield:SolderJumper_3_Bridged12**, imported from the installed KiCad 10.0.6 `Jumper` library. The custom PowerSelector definition was removed from both the local library and schematic cache. The standard drawing, pin geometry, pin names and electrical types are unchanged from KiCad. Pin assignments remain **1 USB/VBUS (Pico 40), 2 shared IN, 3 VSYS (Pico 39)**. The existing local footprint supplies the normally closed, exposed cuttable copper between pads 1–2 and the open alternate solder gap between pads 2–3. JP41 retains its instance/pin UUIDs, position, footprint and no-BOM/no-position exclusions. Its previously unconnected pins move to the stock symbol's shorter endpoints; existing schematic wiring is untouched. With power removed, cut the 1–2 link and verify isolation before bridging 2–3; never bridge both sources. PCB synchronization remains pending.

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

All headers, SMA and hand-wound inductors are excluded from BOM and positions; the manual BS170 and copper features retain their exclusions. The 44 SMT instances agree with the inventory's assembly filter. Existing symbol/pin UUIDs, the Pico symbol definition, PCB, project settings, footprint library and models are preserved. Control GPIOs are approved as GP6 AMP_EN, GP14 BUTTON_N and GP15 LED_DRIVE on 2026-10-07. The L61 source and button/LED behavior remain open. [VALIDATION.md](VALIDATION.md) records current ERC, physical DRC, expected schematic/PCB differences and visual inspection. Placement and pin/pad checks do not establish a wired circuit, assembly fit or RF performance.

## QLG3 interface update, 2026-10-07

J71 retains its existing local Conn_01x05 symbol and UUIDs, with its filter/assignment changed to the local 2.54 mm female socket. Added TP71 using the installed KiCad 10.0.6 Connector:TestPoint symbol, copied into the local library with BOM/position exclusions and a local copper-pad footprint. There are now 54 non-power component symbols; the 44 SMT inventory entries remain unchanged. All 70-series pins receive net labels or intentional no-connect markers. Original component positions remain unchanged, including the user-requested off-sheet 70-series location.

## Reusable QLG3 module symbol, 2026-10-07

Added original MIT-licensed `QLG3_GPS_UndersideHeader`: pins 1 VCC_3V3, 2 VBAT, 3 PPS, 4 TXD, 5 GND, with matching local host footprint and BOM/position exclusions. It remains unplaced; the active schematic still uses J71 and TP71. See [module documentation](qlg3-model/README.md) for orientation, geometry and model provenance.

## J71 complete receiver footprint assignment

J71 retains its Conn_01x05 drawing and all pin/instance UUIDs and connections, but now selects `QLG3_GPS_UndersideHeader` and displays value `QLG3 GPS Receiver`. Its properties specify an unkeyed 0.1-inch (2.54 mm) socket/header pair; obsolete JST and LCSC metadata were cleared. The generic connector's local and cached footprint filters now accept the module footprint as well as the standalone socket. The separately available QLG3 electrical symbol is not additionally placed.
