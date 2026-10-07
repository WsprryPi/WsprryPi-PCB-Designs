# Synth shield footprint sources

Component footprints selected on 2026-10-06 use the independent `wsprrypico-synth-shield` library through `${KIPRJMOD}`. The existing Pico board footprint, its STEP preview and library nickname are preserved. The new library assets support the [component inventory](PARTS.md) and are now assigned to the placed schematic instances. Their PCB placement remains pending. [SYMBOL-SOURCES.md](SYMBOL-SOURCES.md) records the separately added local symbol definitions.

## Copied KiCad footprints

The following files were copied from the installed **KiCad 10.0.6** library. Upstream names identify the corresponding [KiCad footprint collection](https://gitlab.com/kicad/libraries/kicad-footprints). Copies retain **CC BY-SA 4.0 with the KiCad library exception**, documented in [KICAD-LIBRARY-LICENSE.md](KICAD-LIBRARY-LICENSE.md).

| Local footprint | Upstream collection | Local changes |
| --- | --- | --- |
| C_0603_1608Metric, C_0805_2012Metric, C_1206_3216Metric | Capacitor_SMD | None |
| R_0603_1608Metric | Resistor_SMD | None |
| LED_0603_1608Metric | LED_SMD | None; pad 1 cathode, pad 2 anode |
| SOT-23-5, SOT-23-6 | Package_TO_SOT_SMD | Reference text moved outward to clear the pin-1 silkscreen under existing project rules |
| SOIC-14_3.9x8.7mm_P1.27mm | Package_SO | None; LS7366R-S uses narrow SOIC, not wide-body |
| Potentiometer_Bourns_TC33X_Vertical | Potentiometer_SMD | None; pin 2 wiper |
| JST_PH_B5B-PH-K_1x05_P2.00mm_Vertical | Connector_JST | Exclude from assembly BOM and positions; retain through-hole board footprint |
| SMA_BAT_Wireless_BWSMA-KWE-Z001 | Connector_Coaxial | Exclude from assembly BOM and positions; retain through-hole board footprint |
| TO-92_Inline | Package_TO_SOT_THT | None; future BS170 instance retains manual fitting/exclusions |
| SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm | Jumper | None; future JP51 instance is a copper feature excluded from assembly BOM and positions |
| MSOP-10_Si5351A_3x3mm_P0.5mm | Package_SO: MSOP-10_3x3mm_P0.5mm | Adapted to Skyworks' Si5351 recommended land pattern as described below |

Standard model references continue to use `${KICAD10_3DMODEL_DIR}`; these require installed KiCad models. The stock STEP references for `Potentiometer_Bourns_TC33X_Vertical` and `SMA_BAT_Wireless_BWSMA-KWE-Z001` do not resolve in the installed KiCad 10.0.6 model collection. Those references are preserved and the two missing solids remain documented gaps. The other referenced models resolve in this installation. No absolute machine path is introduced into project sources.

## Package drawings and dimensions

**Si5351A MSOP:** [Skyworks datasheet Rev. 1.3, Figure 30 and Table 26, page 43](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/data-sheets/Si5351-B.pdf#page=43) specifies 0.50 mm pitch, 4.40 mm row centers, 1.40 mm pad length and 0.30 mm maximum pad width. The local footprint uses those dimensions, leaving 0.20 mm nominal clearance between adjacent pads. The generic KiCad footprint's 0.35 mm pads left only 0.15 mm and failed the existing 0.20 mm clearance rule. The local adaptation fixes the footprint rather than relaxing the rule. Its 0.06 mm NSMD mask expansion follows Skyworks, leaving an approximately 0.08 mm mask web; confirm this with the fabricator/stencil process before fabrication release. Pin numbering and standard 3D-model reference are retained.

**LS7366R-S SOIC:** [LSI/CSI package selection](https://lsicsi.com/products/ls7366r-s-ls7366r-ts-ls7366r/) specifies the narrow 14-pin package. Its [SOIC outline](https://lsicsi.com/pdfs/Data_Sheets/SOIC_Outline_Dwgs.pdf) gives 3.90 mm body width, 8.65 mm body length, 6.00 mm overall lead width and 1.27 mm pitch. These match the selected standard SOIC-14 footprint envelope. The placed local LS7366R_S symbol uses the exact counter pin map.

**Bourns TC33X-2:** the [manufacturer drawing](https://www.bourns.com/docs/product-datasheets/tc33.pdf) gives the 3.6 × 3.8 mm body and asymmetric three-pad land pattern. The copied footprint is a rotated implementation of that pattern, with 1.2 mm square end pads and a 1.5 × 1.6 mm wiper pad. Pin 2 remains the wiper; preserve the end-terminal orientation when assigning bias nets.

**JST PH:** use the [JST PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) for the exact B5B-PH-K-S top-entry variant. The 5-pin header uses 2.00 mm pitch and 8.00 mm first-to-last pin spacing. Its through-hole pattern and pin-1 identification must be kept distinct from side-entry and SMT PH variants.

**SMA:** [BAT WIRELESS drawing, page 6](https://datasheet.lcsc.com/datasheet/pdf/b4f7aaba83295165fa8bc5302c54d3d3.pdf?productCode=C496551) gives four shell pins on a 5.10 mm square and five 1.40 mm holes. The local copied footprint matches those centers and holes. Pad 1 is the signal; the four pad-2 holes connect to ground. Its stock STEP reference is retained, but that model is missing from the installed collection. Connector-body and cable clearance remain placement/fit checks.

## Original footprints

These are original repository footprints under the [MIT license](LICENSE.md), drawn from factual dimensions rather than imported third-party CAD geometry.

| Footprint | Dimensions and pin numbering | Source / limits |
| --- | --- | --- |
| KDS_DSB321SDN_3.2x2.5mm | Body 3.2 × 2.5 mm; rectangular 0.78 × 0.90 mm pads, centers 3.02 × 1.40 mm; top view pin 1 bottom left, 2 bottom right, 3 top right, 4 top left | [KDS family drawing, page 2](https://www.kds.info/wp-content/uploads/2015/11/dsb321sdn-1-d_pdf_en-1.pdf#page=2); exact DSB pin map: 1/2 GND, 3 OUT, 4 VCC; no 3D solid |
| SW_SPST_XUNPU_TS1088R_4x3mm | 3.90 × 3.00 mm body, 2.00 mm height; two 1.05 × 2.00 mm pads, centers 4.45 mm apart, 3.40 mm inner gap and 5.50 mm total pad span | [XUNPU C455280 drawing](https://datasheet.lcsc.com/datasheet/pdf/d36ef8d43e89de62c59fa43456d00a3f.pdf?productCode=C455280); pins 1 and 2 close when pressed; no 3D solid |
| PowerSelector_VBUS_IN_VSYS_Cuttable | Pads 1/2/3 at −2/0/+2 mm; 1.50 × 2.00 mm pads; default 1–2 copper neck 0.35 × 0.50 mm; alternate gap open | Original copper selector meeting the approved requirement; pad 1 VBUS, 2 shared IN, 3 VSYS; net-tie group 1/2; no paste; both BOM/position exclusions |

The selector footprint is the default VBUS state. For a permanently redesigned VSYS manufacturing variant, update the schematic/default net tie and copper state together; a scratched/rebridged assembled unit is an assembly alteration. Never bridge both selector paths. Verify accessible cutting, isolation and the combined current/voltage-drop budget on the assembled revision.

## Reused provisional choke asset

`L_Toroid_FT37-43_Vertical_P5.08mm` and `FT37-43_25T_Upright.wrl` are copied from the GPIO shield. The only footprint change is its model path to this synth project's local 3D folder. The upright winding envelope, two 2.4 mm pads, 1.2 mm holes and 5.08 mm lead spacing are retained. The footprint derives from the source project's adapted KiCad toroid pattern under the same library terms; the illustrative VRML model is original MIT work. [Source provenance](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md)

Copying this asset preserves the approved amplifier plan; it does not approve a non-LCSC procurement exception. Exact choke sourcing remains the explicit unresolved item in [PARTS.md](PARTS.md#drain-choke-sourcing-conflict).

## Validation scope

The isolated library fixture uses unchanged project rules and is kept under ignored `generated/parts-validation/`. At the parts-selection checkpoint it included every new footprint and left the active starter board/schematic untouched. The subsequent symbol placement changed the schematic/local symbol library only; the PCB and footprint assets remain unchanged. Footprint pad dimensions/numbers and the critical manufacturer drawings were inspected; physical component fit, soldering process, RF impedance and complete-board placement remain separate acceptance work. Current ERC/DRC results are in [VALIDATION.md](VALIDATION.md).

## QLG3 receiver part, 2026-10-07

J71 is **QLG3 GPS Receiver**, using a plain unkeyed 1×5 **0.1-inch (2.54 mm)** female socket on the shield and male header underneath the receiver board. Its selected local footprint is `QLG3_GPS_UndersideHeader`; placing it displays the complete receiver, SMA, socket/header and mounting hardware in 3D. The receiver and SMA face up. Pins 1–5 are **3V3, VBAT tied to 3V3, PPS, receiver TX, GND**; receiver RX requires a separate hand wire. This supersedes the earlier JST PH/keyed interface and its pin order.

BOM and placement exclusions remain enabled. The footprint reserves only the socket and two mounting-hardware areas; remaining space accepts components with sufficient vertical clearance. Hans's exact XY dimensions, standard header geometry, estimated body dimensions, provenance and fit limits are documented in [the QLG3 part notes](qlg3-model/README.md). This focused part commit does not include the separate in-progress schematic wiring or PCB placement.
