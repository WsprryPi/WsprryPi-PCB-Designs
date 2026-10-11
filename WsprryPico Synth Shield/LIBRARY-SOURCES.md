# Synth shield footprint and model sources

The independent `wsprrypico-synth-shield` libraries use `${KIPRJMOD}` paths. The footprint library contains exactly the **19 footprint types** assigned in the saved schematic and PCB. All are imported locally; the [parts inventory](PARTS.csv) records their component assignments. This document records asset provenance, dimensions and model limits; [VALIDATION.md](VALIDATION.md) records current board findings.

## KiCad footprint assets

Copies originate in the [KiCad 10.0.6 footprint collection](https://gitlab.com/kicad/libraries/kicad-footprints) and retain **CC BY-SA 4.0 with the KiCad library exception**. See [KICAD-LIBRARY-LICENSE.md](KICAD-LIBRARY-LICENSE.md).

| Local footprint | Upstream collection | Relevant geometry or adaptation |
| --- | --- | --- |
| C_0603_1608Metric, C_0805_2012Metric, C_1206_3216Metric | Capacitor_SMD | Standard passive lands |
| R_0603_1608Metric | Resistor_SMD | Standard passive lands |
| LED_0603_1608Metric | LED_SMD | Pad 1 cathode; pad 2 anode |
| SOT-23-5, SOT-23-6 | Package_TO_SOT_SMD | Reference text clears pin-1 silkscreen |
| Potentiometer_Bourns_TC33X_Vertical | Potentiometer_SMD | Pin 2 wiper; local illustrative model |
| TO-92_Inline | Package_TO_SOT_THT | 0.75 mm drills; 1.25 × 1.35 mm pads; 1.45 mm pitch |
| MSOP-10_Si5351A_3x3mm_P0.5mm | Package_SO | Si5351 land-pattern adaptation described below |
| L_TDK_VLS6045EX_VLS6045AF | Inductor_SMD | 6.8 × 6.8 mm courtyard; local illustrative model |
| L_0603_1608Metric | Inductor_SMD | L71; generic STEP copied locally |
| U.FL_Hirose_U.FL-R-SMT-1_Vertical | Connector_Coaxial | J71; manual BOM/position exclusions; local STEP |
| TestPoint_THTPad_1.0x1.0mm_Drill0.5mm | TestPoint | TP61/TP62; plated copper pads excluded from BOM/positions |

Standard model references use `${KICAD10_3DMODEL_DIR}` where applicable and require the installed KiCad 3D library. Assigned local assets are listed in the [model inventory](wsprrypico-synth-shield.3dshapes/README.md).

## Synthesizer and transistor

**Si5351A MSOP:** the [Skyworks recommended land pattern, Figure 30/Table 26](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/data-sheets/Si5351-B.pdf#page=43) specifies 0.50 mm pitch, 4.40 mm row centers, 1.40 mm pad length and at most 0.30 mm pad width. The local footprint uses **0.28 mm pad width**, leaving 0.22 mm nominal copper clearance. Its **0.06 mm mask expansion** leaves a **0.10 mm mask web**. Specify a fabrication process and mask color that accept that web; it does not cover a 0.13 mm mask-web requirement. The standard MSOP model is a package preview.

**BS170 TO-92:** the footprint uses **0.75 mm drills**, **1.25 × 1.35 mm pads**, a **0.25 mm minimum annular ring** and **1.45 mm pitch**, with 0.20 mm nominal adjacent copper clearance. Local hole centers are X = −0.18, 1.27 and 2.72 mm. Each outer lead of the straight-lead [onsemi BS170](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf) requires a slight 0.18 mm outward spread during hand fitting. The stock TO-92 model depicts straight leads at the generic pitch. Pin mapping remains 1 drain, 2 gate, 3 source.

## Original footprints

These factual-dimension drawings are original repository work under [LICENSE.md](LICENSE.md).

| Footprint | Geometry and pin numbering | Source |
| --- | --- | --- |
| KDS_DSB321SDN_3.2x2.5mm | 3.2 × 2.5 mm body; 0.78 × 0.90 mm pads, centers 3.02 × 1.40 mm; 1/2 GND, 3 OUT, 4 VCC | [KDS drawing](https://www.kds.info/wp-content/uploads/2015/11/dsb321sdn-1-d_pdf_en-1.pdf#page=2) |
| SW_SPST_XUNPU_TS1088R_4x3mm | 3.90 × 3.00 × 2.00 mm body; two 1.05 × 2.00 mm pads, centers 4.45 mm apart | [XUNPU drawing](https://datasheet.lcsc.com/datasheet/pdf/d36ef8d43e89de62c59fa43456d00a3f.pdf?productCode=C455280) |
| Zhongke_ATGM336H-5N31_9.7x10.1mm_P1.1mm | 9.7 × 10.1 mm body; rows X = ±4.85 mm; 1.1 mm pitch; 1.8 × 0.8 mm lands; manual top view rotated 180° to put pin 1 upper left | [ATGM336H manual, pages 9–14](https://www.lcsc.com/datasheet/C90770.pdf) |
| Raspberry_Pi_Pico_2W_Header | Combined two-row, 40-pad interface, 2.54 mm pitch and 17.78 mm row spacing | [Project-local Pico reference assets](../Pico%202W%20Wattmeter%20Shield/pico-2w-libs/README.md) |

## Bias trimmer

The [Bourns TC33X-2 drawing](https://www.bourns.com/docs/product-datasheets/tc33.pdf) specifies a 3.6 × 3.8 mm body and asymmetric three-pad pattern. The footprint is a rotated implementation with 1.2 mm square end pads and a 1.5 × 1.6 mm wiper pad. **Pin 1 is the counterclockwise end, pin 2 the wiper, and pin 3 the clockwise end.** RV61 connects pin 3 to GND, so clockwise lowers the bias. Its local model has an illustrative 3.8 × 3.0 mm body and approximately 1.6 mm height; use the manufacturer's drawing for physical fit.

## Drain choke

L61 selects **TDK VLS6045EX-331M / C501933**. The KiCad-derived footprint has **1.9 × 5.1 mm lands**, centers at X = ±2.1 mm, matching the [TDK recommended land pattern](https://product.tdk.com/system/files/dam/doc/product/inductor/inductor/smd/catalog/inductor_commercial_power_vls6045ex_en.pdf). The 6.8 × 6.8 mm courtyard allows 0.25 mm beyond the 6.3 mm maximum body width. The footprint retains KiCad library terms.

`VLS6045EX_6x6x4.5_Preview.wrl` is original MIT-licensed geometry showing the nominal 6 × 6 mm body and 4.5 mm maximum height. It omits detailed terminal and winding geometry. L61 has an assigned local visual preview; a supplier STEP model is not provided. Electrical ratings and RF limits are in [PARTS.md](PARTS.md#drain-choke-selection).

## RF connectors

**J61 SMA:** `SMA_Adafruit_1865_EdgeMount` follows the public-domain Adafruit Eagle land pattern, reused through the [GPIO/Zero amplifier assets](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md). It provides a front signal pad and ground lands on both faces of a 1.6 mm board, with no paste apertures. The [Adafruit 1865 drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) governs actual connector dimensions. Its local illustrative VRML model is original repository-MIT work.

**J71 U.FL:** the copied KiCad footprint uses signal pad 1 at (−1.525, 0) mm, 1.05 × 1.00 mm, and two ground pad-2 lands at (0, ±1.475) mm, 2.20 × 1.05 mm. It retains the central front-copper keepout, mask opening and paste apertures. The [Hirose drawing](https://www.hirose.com/product/download/?distributor=all&lang=en&series=U.FL&type=catalogue#page=12) identifies signal/ground and prohibits conductive traces beneath the central body. The copied local STEP retains KiCad library terms. J71 is hand fitted and excluded from BOM/positions; verify pigtail mating and cable clearance with the actual assembly.

## Local visual models

SW11 and Y41 use original MIT-licensed previews based on the manufacturer dimensions above. RV61's original MIT preview and J61's original MIT preview are reused from the GPIO shield. `Zhongke_ATGM336H-5N31.wrl` is an original 9.7 × 10.1 × 2.4 mm body approximation. The socket and U.FL STEP models retain their embedded KiCad copyright/license notices.

The [switch/TCXO generator](wsprrypico-synth-shield.3dshapes/generate_switch_tcxo_previews.py) rebuilds those two previews. The [GPIO trimmer generator](../WsprryPico%20GPIO%20Shield/wsprrypico-gpio-shield.3dshapes/generate_rv31_j51.py) records the reused trimmer geometry. KiCad VRML coordinates use 0.1-inch units. Preview details, colors and generic connector geometry do not qualify fit or assembly tolerances.
