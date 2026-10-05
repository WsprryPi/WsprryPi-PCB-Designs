# BS170 fabrication and assembly notes

**Order status: Ready for order, confirmed by the project owner on 2026-10-05.** Order the current two-layer, 1.6 mm BS170 board. The headers and Q41 BS170 will be fitted by hand after manufacture. L41's hand-wound choke and J51's hand-soldered SMA connector also remain outside supplier assembly.

Generate Gerbers, plated and non-plated drills, the assembly BOM, and the placement file from the exact saved BS170 revision being ordered. Keep generated packages in the ignored `production/` or `fabrication/` directory and identify the source commit, board revision, KiCad version, and validation status with the package. See the [project README](README.md#validation-and-limits) for the recorded checks and their limits.

## Supplier assembly

The saved PCB has **19 SMD assembly components** with reviewed sourcing metadata. The assembly BOM and placement file must contain the same references:

| Type | References |
| --- | --- |
| Capacitors | C21, C22, C23, C31, C32, C41, C42, C51 |
| Indicator | D11 |
| Resistors | R11, R21, R22, R31, R32, R33, R41 |
| Gate-bias trimmer | RV31 |
| Shutdown button | SW11 |
| Load switch | U21 |

Use the selected `LCSC Part #` values in the board-based Fabrication Toolkit BOM. Check supplier matching and orientation in the assembly preview against the current board. U11, J12, J21, J51, J52, Q41, and L41 are excluded from both BOM and position output on the saved PCB. J11 is a schematic-only purchasing item and must not be added to the supplier assembly list.

## Hand-fitting list

Purchase these items separately and fit them after manufacture:

| Board reference / purchasing item | Quantity | Hand-fitted part |
| --- | ---: | --- |
| U11 interface / J11 purchasing item | 1 | Female 2×20, 2.54 mm Raspberry Pi socket, mounted underneath; choose mating height for the intended Pi and spacers |
| J12 | 1 | Male 1×3, 2.54 mm GPIO-selection header; provide a shunt for GPIO4 or GPIO20 selection |
| J21 | 1 | Male 1×2, 2.54 mm bias-setting header; provide a removable shunt and leave it open during normal operation |
| J52 | 2 | Female 1×4, 2.54 mm LPF sockets; the grouped board footprint represents two physical headers at 33.02 mm row-center spacing |
| Q41 | 1 | Straight-lead onsemi BS170, TO-92; verify pins 1/2/3 = drain/gate/source |
| L41 | 1 | Upright FT37-43 choke, hand-wound with 25 turns and leads formed to 5.08 mm spacing |
| J51 | 1 | Adafruit 1865 standard-polarity female edge-launch SMA connector for a 1.6 mm board |

U11 and J11 refer to the same physical Raspberry Pi socket, so purchase one socket. The plug-in LPF is a separate assembly; fit the filter for the operating band before RF testing. Follow the [choke assembly guidance](README.md#selected-hand-wound-choke-and-trimmer) and [J21 bias-setting instructions](README.md#schematic-block-numbering).

## Fabrication process

The current BS170 board has no U31 exposed-pad QFN or RF transformers. The historical nine-hole U31 epoxy-fill/copper-cap process is not a requirement for this revision. Do not apply those superseded selective-via instructions to the current order merely because an old library footprint or the `sk` user-layer name remains in the project. Preserve plated component holes for hand fitting and include the correct non-plated mounting-hole drills.

Order readiness records the project owner's manufacturing decision. Physical fit, GPIO loading, bias and switched-supply behavior, temperature, output power, and spectrum still require checks on the exact assembled board, Pi, LPF, and load. Historical ERC/DRC results and exclusions remain visible in the [project validation records](README.md#validation-and-limits).
