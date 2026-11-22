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
| Conn_Coaxial | Connector:Conn_Coaxial | SMA_Amphenol_132289_EdgeMount |
| Conn_01x03 | Connector_Generic:Conn_01x03 | PinHeader_1x03_P2.54mm_Vertical |
| GND | power:GND | Electrical symbol only |
| PWR_FLAG | power:PWR_FLAG | ERC annotation only |

The library contains only assets used by the schematic or PCB. The twelve symbols are standalone, with no `extends` dependency, and the schematic embeds the same definitions. Their assigned footprints use the local `SN74LVC2T45_Amp` library. U1 follows the DCU pin mapping in [TI's datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf).

The KENTO LED symbol and footprint use terminal 1 for the anode and terminal 2 for the cathode, matching the selected KT-0603R datasheet. The pad coordinates, cathode marking, and generic 0603 STEP model retain their physical orientation. The generic LED symbol and footprint are not included because they are unused.

The seven footprints reference seven STEP models under `${KIPRJMOD}/libraries/SN74LVC2T45_Amp.3dshapes/`. The IC footprint is for Texas Instruments DCU0008A, not every package offered for this device. A 3D model shows the assembly; manufacturer drawings and actual parts determine fit.

The symbols, footprints, and models carry their authors' copyrights and the [KiCad library license and exception](KICAD-LIBRARY-LICENSE.md). Those terms are separate from the repository's MIT license. STEP files include embedded notices. Manufacturer transistor and capacitor models are not part of these library assets.
