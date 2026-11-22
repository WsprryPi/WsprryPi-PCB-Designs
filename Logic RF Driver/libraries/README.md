# Project-local libraries

The project includes symbols, footprints, and STEP models. Paths use `${KIPRJMOD}`, so the library does not depend on another project or a machine-specific directory. The [manifest](MANIFEST.json) lists source identities, hashes, and local files.

| Symbol | Library definition | Assigned footprint |
| --- | --- | --- |
| SN74LVC2T45DCUR | Logic_LevelTranslator:SN74LVC2T45DCUR | VSSOP-8_2.3x2mm_P0.5mm |
| C | Device:C | C_0603_1608Metric |
| R_US | Device:R_US | R_0603_1608Metric |
| C_Small | Device:C_Small | C_0603_1608Metric |
| BAT54S | Diode:BAT54S | SOT-23 |
| MMBT3904 | Transistor_BJT:MMBT3904 | SOT-23 |
| LED_KT0603R | Device:LED with KENTO terminal numbering | LED_KT0603R |
| +3V3 | power:+3V3 | Electrical symbol only |
| Conn_Coaxial | Connector:Conn_Coaxial | SMA_Adafruit_1865_EdgeLaunch |
| Conn_01x03 | Connector_Generic:Conn_01x03 | Power_1x03_P2.54mm_Header_or_Adafruit_2136 |
| GND | power:GND | Electrical symbol only |
| PWR_FLAG | power:PWR_FLAG | ERC annotation only |

The library contains only assets used by the schematic or PCB. The twelve symbols are standalone, with no `extends` dependency, and the schematic embeds the same definitions. Their assigned footprints use the local `SN74LVC2T45_Amp` library. U1 follows the DCU pin mapping in [TI's datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf).

The KENTO LED symbol and footprint use terminal 1 for the anode and terminal 2 for the cathode, matching the selected KT-0603R datasheet. The pad coordinates, cathode marking, and generic 0603 STEP model retain their physical orientation. The generic LED symbol and footprint are not included because they are unused.

The seven footprints reference eight STEP models under `${KIPRJMOD}/libraries/SN74LVC2T45_Amp.3dshapes/`. The IC footprint is for Texas Instruments DCU0008A, not every package offered for this device. A 3D model shows the assembly; manufacturer drawings and actual parts determine fit.

KiCad-derived symbols, footprints, and models carry their authors' copyrights and the [KiCad library license and exception](KICAD-LIBRARY-LICENSE.md). Those terms are separate from the repository's MIT license. STEP files retain their embedded notices. Manufacturer transistor and capacitor models are not part of these library assets.

## Adafruit 2136 power terminal

J2 uses an original project-local footprint based on the [KF120-3P drawing linked by Adafruit](https://cdn-shop.adafruit.com/product-files/2135/Kaweei_KF120-XP.pdf). It has three positions at 2.54 mm pitch, 1.2 mm finished holes, and 2.0 mm pads. The nominal 0.8 × 0.5 mm rectangular leads have a 0.943 mm diagonal; the larger holes provide insertion clearance. The fab outline follows the drawing's 8.0 × 6.3 mm housing, with the wire-entry face 3.5 mm from the pad row and the rear face 2.8 mm from it. The courtyard adds 0.25 mm around that outline.

The local STEP file is an original dimensioned envelope with simplified housing, screws, and solder pins. It represents an 8.6 mm installed height and 3.5 mm pin length; it is not a manufacturer model. The footprint and envelope model use the repository's MIT license. The manifest identifies the drawing and asset hashes. Adafruit's product page gives approximate overall dimensions and lists multiple variants, so the supplied part's physical fit remains unmeasured.

J2 is a shared footprint for either the Adafruit 2136 screw terminal or a standard straight 1×3 header at 2.54 mm pitch. Both use the same three plated holes and the same pin order. The fab layer shows both body outlines; the courtyard covers the larger terminal housing. The terminal envelope is the default visible model. In Footprint Properties → 3D Models, disable the terminal model and enable the local header model to display the header option. Fit one connector at J2, not both.

## Adafruit 1865 SMA connectors

J1/J3 use the local SMA_Adafruit_1865_EdgeLaunch footprint converted from the public-domain SMA_EDGELAUNCH package in [Adafruit's Eagle library](https://github.com/adafruit/Adafruit-Eagle-Library). Adafruit attribution and source URL are present in the footprint description and manifest. Copper dimensions and no-paste settings follow the package. Eagle signal P maps to pad 1; all four ground tabs map to pad 2. The footprint origin marks the board edge, with pad centres 2.032 mm inward. Added front and back courtyards cover the connector envelope and lands.

The local STEP model is original project geometry under the MIT license, based on the [C2387-001 envelope drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf). It illustrates the body and contacts with a slot for a nominal 1.57 mm board. Threads and internal RF geometry are omitted. Actual fit and RF behaviour are unmeasured. The [connector notes](../CONNECTORS.md) describe the local copper-to-edge rule.

J2's silkscreen is an open-front outline suited to the board-edge mounting position. At the placed pad row Y = 52.25 mm, its side strokes end at Y = 50.25 mm, inside the board edge. The full terminal housing remains on F.Fab and F.CrtYd, including the 1.25 mm overhang. Pads, holes, and model offsets use the shared terminal/header geometry.
