# PCB layout

The PCB has two copper layers and short clock and RF paths. The [BOM](BOM.csv) identifies its parts. This layout has no extracted electromagnetic or supply-impedance model.

| Item | Design |
| --- | --- |
| Board envelope | 27.08 × 16.00 mm |
| Corner radius | 1.00 mm |
| Nominal finished thickness | 1.57 mm |
| Copper | F.Cu and B.Cu, nominal 35 um per layer |
| Track segments | 103: 91 on F.Cu and 12 GND segments on B.Cu |
| Track widths | 0.20, 0.25, 0.50, 0.60, and 1.20 mm |
| Ground vias | 31 through vias, nominal 0.60 mm diameter and 0.30 mm drill |
| Signal vias | None |
| Ground zones | Separate filled GND zones on F.Cu and B.Cu |
| Mounting holes | None |

The stackup assumes nominal FR4 properties. The Amphenol 132289 connector accepts a maximum PCB thickness of 1.57 mm, so finished thickness and tolerance affect its fit. Actual connector fit is unmeasured. See the [connector product information](https://www.amphenolrf.com/en-us/part/132289/1030/).

## Placement and routing

All nineteen footprints are placed, and all connections are routed. R2 samples RF_RAW on the U1 side of C4; the 220-ohm resistor connects the tap to C5 and the diode detector. D2 and D3 are the activity and 3.3 V power LEDs. Their part-specific local footprint uses KENTO terminal 1 as the anode and terminal 2 as the cathode.

J1 and J3 are on opposite ends of the board. The input reaches a shared A1/A2 junction beside U1. B1/B2 join beside the IC and feed C4 and J3. Signal and supply tracks run on the front copper layer; the back layer is the ground reference, with twelve additional ground-track segments around the SMA returns.

J1/J3 anchors lie on the 0.25 mm placement grid. The other seventeen component anchors and some stitching vias use different coordinates. Pads and IC pitch follow their footprint geometry. The board edges at X = 50.46 and 77.54 mm preserve the SMA connector offsets.

C1 sits beside VCCA, and C2/C3 sit beside the 5 V feed. Nearby vias connect their grounds to the planes. R1 is close to the input fanout. DIR joins VCCA on the front copper layer.

Six stitching vias flank each RF path. Their X coordinates are 56.50, 58.25, 60.00, 67.96, 69.98, and 72.00 mm; their Y coordinates are 56.75 and 59.25 mm. The other ground vias serve the perimeter and local returns.

The RF tracks and SMA transitions have no controlled 50-ohm fabrication or electromagnetic qualification. Stitching alone cannot establish output impedance, channel skew, current sharing, or full-band RF performance. The output needs a filter for the selected band and a 50-ohm load.

## Rules and checks

The default net class requires 0.20 mm clearance. The U1 rule permits 0.15 mm between pads within that footprint. The minimum track width is 0.20 mm, and the copper-to-edge setting is 0.50 mm. Other named-net rules in the custom-rule file have no matching nets on this board and therefore do not apply. Teardrops are present on the front copper layer, and their fill must respect the separate pad-to-track/zone clearance requirement.

DRC reports zero violations, zero unconnected items, and zero schematic-parity issues under the configured checks. The ignored categories are listed in [VALIDATION.md](VALIDATION.md). That result covers CAD checks, not fabrication or RF performance.

J1/J2/J3 are visible in the [assembly view](docs/pcb-preview.png), on the board, excluded from the BOM, and not DNP. Use the native design files for geometry and connectivity.

The CLK_IN and RF_RAW fanouts include overlapping and redundant track segments near U1. They are electrically connected and pass the configured DRC.

C6 sits beside D1. A direct 1.46 mm trace connects D1's cathode to C6, and C6's ground pad has a ground via about 0.76 mm from its center. This gives the rectifier a short connection to its reservoir capacitor and a nearby return to the ground plane. The longer connection serves Q1 and R3. The layout has no extracted detector-loop model or measured VHF performance.
