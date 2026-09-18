# Pico sockets and antenna notch

## Header interface

The `Raspberry_Pi_Pico_2W_Header` footprint represents both rows of Pico connections.

| Feature | Geometry |
| --- | --- |
| Header rows | Two rows of 20 plated holes |
| Pin pitch | 2.54 mm |
| Row spacing | 17.78 mm |
| Drill diameter | 1.00 mm |
| Copper pads | 1.508 × 1.508 mm |
| Ground pads | 3, 8, 13, 18, 23, 28, 33, 38 |
| Ground thermal reliefs | 0.20 mm gap, 0.30 mm spoke width |

J2 and J3 are pinless, schematic-only procurement symbols for two female 1×20 sockets. U3 represents their physical PCB interface. The sockets and Pico module are fitted by hand and excluded from factory assembly. Select socket lead dimensions, body width, and mating height for the actual Pico stack; no socket manufacturer or part number is specified.

## Antenna notch

The header footprint contains three `Edge.Cuts` segments defining a **14 mm-wide × 9 mm-deep open notch**. On this board, the opening spans x = 164.46–173.46 mm and y = 82.69–96.69 mm. A matching `Pico antenna keepout` on both copper layers prohibits tracks, vias, pads, copper fills, and footprints.

The footprint's local notch endpoints are (−7.89, 26.65) and (6.11, 26.65) mm, with the inner edge at y = 17.65 mm. When reusing the footprint, join both endpoints to the receiving board's outer outline. Do not close the mouth with a fourth edge. Moving the footprint requires updating the adjoining outline segments.

Confirm the fabricator's internal corner radius and the assembled Pico clearance. The antenna clearance reference is the [Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf).

## Reusable schematic block

`pico-wattmeter:Pico_2W_Two_Female_Sockets` contains the Pico interface symbol, its combined footprint assignment, and the two socket procurement symbols. Application wiring and no-connect flags are supplied by the receiving design. Both socket symbols default to exclusion from the factory BOM.

In the Schematic Editor, select **View > Panels > Design Blocks**, choose `pico-wattmeter`, and place `Pico_2W_Two_Female_Sockets`. Wire the interface and run Update PCB from Schematic. Enable socket BOM inclusion only when the assembly order should purchase those parts. Placing the Pico symbol alone does not add the socket procurement symbols.

The block is registered in `design-block-lib-table` using `${KIPRJMOD}`. Reuse requires the accompanying symbol, footprint, and block libraries under the `pico-wattmeter` nickname.
