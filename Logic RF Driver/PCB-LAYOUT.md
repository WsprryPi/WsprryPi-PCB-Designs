# PCB layout

The PCB has two copper layers and short clock and RF paths. The [BOM](BOM.csv) identifies its parts. This layout has no extracted electromagnetic or supply-impedance model.

| Item | Design |
| --- | --- |
| Board envelope | 27.08 × 16.00 mm |
| Corner radius | 1.00 mm |
| Nominal finished thickness | 1.57 mm |
| Copper | F.Cu and B.Cu, nominal 35 um per layer |
| Track segments | 87, all on F.Cu |
| Track widths | 0.20, 0.25, 0.50, 0.60, and 1.20 mm |
| Ground vias | 43 through vias, nominal 0.60 mm diameter and 0.30 mm drill |
| Signal vias | None |
| Ground zones | Separate filled GND zones on F.Cu and B.Cu |
| Mounting holes | None |

The stackup assumes nominal FR4 properties. The Adafruit 1865 SMA connector is sold for nominal 1.6 mm boards. This board's nominal thickness is 1.57 mm. Supplied connector dimensions and actual finished thickness determine fit. See the [connector information](CONNECTORS.md#sma-jacks).

## Placement and routing

All nineteen footprints are placed, and all connections are routed. R2 samples RF_RAW on the U1 side of C4; the 220-ohm resistor connects the tap to C5 and the diode detector. D2 and D3 are the activity and 3.3 V power LEDs. Their part-specific local footprint uses KENTO terminal 1 as the anode and terminal 2 as the cathode.

J1 and J3 are on opposite ends of the board. The input reaches a shared A1/A2 junction beside U1. B1/B2 join beside the IC and feed C4 and J3. Signal and supply tracks run on the front copper layer; the back layer provides the ground reference. All track segments are on F.Cu.

J1 and J3 use edge-referenced footprint origins at X = 50.46 and 77.54 mm, Y = 58.00 mm. Their signal pads are 2.032 mm inward from those edges. J1 has zero rotation, and J3 is rotated 180 degrees. J2 is at X = 61.46 mm, Y = 52.25 mm. All nineteen anchors have at least one coordinate outside the 0.25 mm placement grid. Pads and IC pitch follow their footprint geometry.

C1 sits beside VCCA, and C2/C3 sit beside the 5 V feed. Nearby vias connect their grounds to the planes. R1 is close to the input fanout. DIR joins VCCA on the front copper layer.

The 43 ground vias connect the front and back ground planes around the RF paths, perimeter, and local returns. The native PCB contains their coordinates.

The RF tracks and SMA transitions have no controlled 50-ohm fabrication or electromagnetic qualification. Stitching alone cannot establish output impedance, channel skew, current sharing, or full-band RF performance. The output needs a filter for the selected band and a 50-ohm load.

## Rules and checks

The default net class requires 0.20 mm clearance. The U1 rule permits 0.15 mm between pads within that footprint. The minimum track width is 0.20 mm, and the copper-to-edge setting is 0.50 mm. Other named-net rules in the custom-rule file have no matching nets on this board and therefore do not apply. Teardrops are present on the front copper layer, and their fill must respect the separate pad-to-track/zone clearance requirement.

The saved PCB has filled ground zones and reports zero DRC violations, zero unconnected items, and zero schematic-parity issues under the configured checks. A pad-only custom rule for the Adafruit 1865 footprint at J1/J3 uses −0.01 mm edge clearance to permit exact edge contact. The actual lands stop at the board edge. Tracks, zones, vias, and all other footprints retain the 0.50 mm edge setback. The ignored categories are listed in [VALIDATION.md](VALIDATION.md). That result covers CAD checks, not fabrication or RF performance.

J1/J2/J3 are visible in the [assembly view](docs/pcb-preview.png), on the board, excluded from the BOM, and not DNP. Use the native design files for geometry and connectivity.

C6 sits beside D1. A direct 1.46 mm trace connects D1's cathode to C6, and C6's ground pad has a ground via about 0.76 mm from its center. This gives the rectifier a short connection to its reservoir capacitor and a nearby return to the ground plane. The longer connection serves Q1 and R3. The layout has no extracted detector-loop model or measured VHF performance.

## Power terminal placement

J2 accepts either the [Adafruit 2136](https://www.adafruit.com/product/2136) three-position screw terminal or a straight 1×3 header on the same pads. The screw terminal is the default assembly option. Pad 1 is at X = 61.46 mm, Y = 52.25 mm, with zero rotation; pads 2 and 3 extend in +X at 2.54 mm pitch. The housing's wire-entry face lies at Y = 48.75 mm, giving 1.25 mm overhang at the Y = 50.00 mm edge; its rear face is at Y = 55.05 mm. The silkscreen has an open front with side strokes ending 0.25 mm inside the board edge. The fab and courtyard layers retain the full mechanical envelope. The 1.2 mm holes and 2.0 mm pads suit hand assembly of its nominal 0.8 × 0.5 mm leads. Pin order is +3.3 V, +5 V, and GND from left to right in the top view.

The power fanouts connect to the terminal pads, and both ground zones are filled. The terminal courtyard clears C1, C2, and C3. The assembly image uses the local dimensioned connector envelope described in the [library notes](libraries/README.md).

J1/J3 use the local Adafruit 1865 footprints and simplified STEP envelopes. Both connectors are excluded from the BOM and visible in the assembly view. See the [SMA launch geometry](CONNECTORS.md#sma-jacks) and [local edge-clearance rule](VALIDATION.md#sma-edge-clearance-rule).
