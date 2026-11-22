# Connectors

J1, J2, and J3 are hand-fit connectors. They are visible in the schematic, PCB, and assembly rendering, excluded from the factory BOM, and not marked DNP. Their solder joints, cable clearance, and physical fit require inspection on the assembled board.

| Reference | Function | Selected connector | US source |
| --- | --- | --- | --- |
| J1 | Raw 3.3 V clock input | Adafruit 1865, standard SMA jack, 50 ohms | [Adafruit 1865](https://www.adafruit.com/product/1865) |
| J2 | +3.3 V, +5 V, and GND | Adafruit 2136 three-position screw terminal; straight 1×3 header is an assembly option | [Adafruit 2136](https://www.adafruit.com/product/2136) |
| J3 | DC-blocked RF output to the selected-band filter | Adafruit 1865, standard SMA jack, 50 ohms | [Adafruit 1865](https://www.adafruit.com/product/1865) |

## SMA jacks

[Adafruit 1865](https://www.adafruit.com/product/1865) is a standard 50-ohm SMA female edge-launch connector sold for nominal 1.6 mm / 0.062-inch PCBs. It mates with standard SMA plugs. The board has a nominal 1.57 mm thickness. The supplied connector and finished board thickness determine actual fit; the product listing does not establish launch loss or return loss across 137 kHz–145 MHz.

The project-local footprint follows the public-domain SMA_EDGELAUNCH package in [Adafruit's Eagle library](https://github.com/adafruit/Adafruit-Eagle-Library). The signal land is 4.064 × 1.270 mm, and each ground land is 4.064 × 1.524 mm. Ground-row centres are 5.08 mm apart. The signal land is on F.Cu; ground lands are on both copper faces. All five lands have solder-mask openings and no paste apertures for hand soldering.

The footprint origin marks the PCB edge. J1 is at X = 50.46 mm, Y = 58.00 mm, with zero rotation; J3 is at X = 77.54 mm, Y = 58.00 mm, rotated 180 degrees. Their signal-pad centres are 2.032 mm inside those edges, at X = 52.492 mm and 75.508 mm. The centre contacts connect to CLK_IN and RF_OUT. Upper and lower ground tabs connect to GND through the filled planes and nearby ground vias.

Adafruit's [C2387-001 drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) gives a 13.4 mm axial envelope and a nominal 6.5 mm body. The local STEP file is an original simplified envelope, with an illustrative slot for this board's nominal thickness. It has no thread or internal RF detail and is not manufacturer geometry or proof of mechanical fit. Solder the centre pin and all four ground tabs with the connector square to the board edge. Support the connector when mating cables.

The published lands reach the board edge. A local custom rule permits edge contact only for pads 1 and 2 of J1/J3 with the assigned Adafruit footprint, on both copper faces. Its minimum edge clearance is −0.01 mm because KiCad flags exact contact at a zero minimum. The actual lands stop at the board edge; the tolerance does not move copper. All other copper retains the 0.50 mm setback. See [validation](VALIDATION.md#sma-edge-clearance-rule). Fabrication suitability of the exposed edge copper and assembled RF performance remain unverified.

## Power connector and shared footprint

The [Adafruit 2136](https://www.adafruit.com/product/2136) accepts three wires through screw terminals on a 2.54 mm pitch. The project footprint follows Adafruit's linked [Kaweei KF120-3P drawing](https://cdn-shop.adafruit.com/product-files/2135/Kaweei_KF120-XP.pdf): an 8.0 × 6.3 mm body, 8.6 mm installed height, and nominal 0.8 × 0.5 mm solder pins. The drawing places the wire-entry face 3.5 mm from the pin row and the rear face 2.8 mm from it. Adafruit's approximate product dimensions and available variants do not replace a physical fit check.

J2 uses a single shared row of three 1.2 mm finished holes with 2.0 mm copper pads. The terminal's nominal pin diagonal is 0.943 mm, and a standard 0.64 mm square header pin has a 0.905 mm diagonal. Both fit the nominal holes. A straight 1×3 header at 2.54 mm pitch can therefore use the same pads without an adapter or a second row of holes. The larger holes give the header more play, so hold it square while soldering. Fit one connector at J2.

The top-view pin order is +3.3 V, +5 V, and GND from left to right. The two supply rails are separate; the board has no regulator or reverse-polarity protection. Pad 1 is at X = 61.46 mm, Y = 52.25 mm, with zero rotation. The terminal's wire-entry face is at Y = 48.75 mm, giving 1.25 mm of body overhang beyond the Y = 50.00 mm board edge. The rear housing face is at Y = 55.05 mm. J2's open-front silkscreen has side strokes ending at Y = 50.25 mm; the full body outline remains on the fab layer and courtyard. The fab layer shows the terminal and header bodies, and the courtyard covers the larger terminal body. C1, C2, and C3 lie outside the terminal courtyard. Physical clearance with the supplied connector remains unmeasured.

The local terminal STEP file is a dimensioned envelope with simplified geometry. The alternate local header STEP file is hidden by default. In **Footprint Properties → 3D Models**, display the model for the chosen assembly option. The default assembly image shows the screw terminal. All model paths use `${KIPRJMOD}`.
