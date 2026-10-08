# QLG3 GPS daughterboard part

Created and orientation corrected 2026-10-07 for the Synth Shield with **KiCad 10.0.6**. Select **`wsprrypico-synth-shield:QLG3_GPS_UndersideHeader`** in the symbol or footprint chooser. J71 now assigns this assembly footprint while retaining its existing five-pin schematic drawing, UUIDs, position and wiring. The active PCB has not been changed.

## QLG3 GPS Receiver kit contents and assembly

Kit information supplied by the user on 2026-10-07: the SMD components are pre-soldered to the PCB during manufacture. Only the SMA connector and pin header connectors need to be soldered to the QLG3 PCB.

The kit includes:

- PCB with module soldered.
- 90° SMA connector.
- Magnetic-mount patch antenna with 2 m coax and SMA connector.
- Two 11 mm nylon hex spacers.
- Four 6 mm nylon screws.
- One 1×5-pin male header and one 1×5-pin female header.

## Single-post variant — selected 2026-10-07

J71 now uses **`QLG3_GPS_UndersideHeader_SinglePost`** in the schematic and placed PCB. The original `QLG3_GPS_UndersideHeader` two-post symbol, footprint and models remain available unchanged. Both use the same five-pin electrical interface and retain BOM/position exclusions.

The single-post variant removes the upper post and screw (the mounting point away from the header), its host-board drill, fabrication hardware circle, courtyard and component keepout. In footprint-local coordinates, the removed host hole was at **X=3.175, Y=−15.39875 mm**. The lower post beside the header and its keepout remain, as does the socket keepout. The real QLG3 daughterboard still has both mounting holes: its unused upper hole and copper ring remain visible in the model, without a post or screw. The complete receiver, SMA and header/socket remain in 3D.

This variant uses one of the kit's two spacers; the kit contents above are unchanged. Mechanical support with one spacer and the header requires an assembly check. J71's position, orientation, reference, electrical pad UUIDs and nets are preserved, as are all other saved board objects.

Rebuild this variant with `python generate_qlg3.py --single-post`; invoking the generator without the option rebuilds the original two-post assets. The single-post symbol, footprint and STEP/VRML use the `_SinglePost` suffix in the same project-local libraries.

KiCad **10.0.6** validation: schematic ERC **0 findings**; schematic/PCB parity **0 findings**. The saved placement's DRC findings fall from **17 to 1**, retaining an existing J71 silkscreen/board-edge clearance warning. The **124 unrouted connections** are unchanged. No rules or exclusions were relaxed. The isolated single-post footprint fixture has **0 DRC findings / 0 unconnected items**. Footprint and 3D views were inspected; this does not establish physical fit or RF qualification.

## Assets and use

- [Symbol library](../wsprrypico-synth-shield.kicad_sym): named five-pin module symbol, default reference prefix `A`.
- [Host footprint](../wsprrypico-synth-shield.pretty/QLG3_GPS_UndersideHeader.kicad_mod): five socket pads, two matching host mounting holes, daughterboard outline and approximate SMA envelope.
- [Colored VRML](../wsprrypico-synth-shield.3dshapes/QLG3_GPS_UndersideHeader.wrl): linked through `${KIPRJMOD}` for KiCad's 3D viewer.
- [STEP assembly](../wsprrypico-synth-shield.3dshapes/QLG3_GPS_UndersideHeader.step): matching solid CAD assembly for mechanical work.
- [Dimension inputs](dimensions.json) and [generator](generate_qlg3.py).
- [Hans's supplied engineering drawing](../QLG3%20GPS%20Receiver%20Kit%20Dimensions.png).

The footprint is for the **host shield**, with its female socket on top. The QLG3 sits above it, with the **E108 receiver and right-angle SMA on top and the male header underneath**, opposite the receiver. The QLG3 is turned over about the X axis relative to Hans's drawing; the SMA still points left. Fit the male header from the opposite face to the QMX+ assembly photographs. Small factory-fitted components on the other PCB face remain there; this orientation change does not relocate them. The model includes the socket, male header, daughterboard, receiver body, SMA, two spacers and upper screw heads. The preview's rectangular host board is a test fixture and is not part of the reusable model.

Symbol and footprint exclude BOM and position exports because this is a manually fitted assembly. J71 already selects this footprint; do not add a second QLG3 footprint at the same interface. Its plain 0.1-inch (2.54 mm) socket/header hardware is unkeyed. Updating the PCB from the schematic will bring in the complete receiver model with J71. The separate optional command hand-wire pad TP71 belongs to the ongoing 70-series schematic work, outside this focused part commit. QLG3 header pin 5 is **GND**, not RX. Module RX is not available on this five-pin header.

| Physical header pin | Signal | Existing shield net |
| --- | --- | --- |
| 1 | VCC, 3.3 V supply | PICO_3V3 |
| 2 | VBAT | PICO_3V3 |
| 3 | PPS output | GPS_PPS_RAW |
| 4 | TXD output | GPS_TX |
| 5 | GND | GND |

Pins run left to right in the assembled **E108-up view**, on the lower edge rather than the upper edge shown in Hans's drawing. Pin numbers and signals are unchanged. Symbol power pins are power inputs and PPS/TXD are outputs. No electrical connection is assigned to the two mounting holes.

## Exact, standard and estimated geometry

Hans specified inches with origin at the board's bottom-left corner. These dimensions are transferred directly, using 25.4 mm/inch. The source dimensions below remain in Hans's view. For the E108-up assembly, use **X′ = X, Y′ = 18.0975 − Y**. The footprint origin is the assembled board's bottom-left corner, with KiCad Y = −Y′. The model uses X′/Y′ with Z upward. Header pads 1–5 therefore have Y′=2.69875 mm (KiCad Y=−2.69875 mm); X and pin numbering are unchanged. The mounting-hole pair exchanges upper/lower positions; the centered SMA stays at Y′=9.04875 mm.

| Feature | X, Y or size in mm | Basis |
| --- | --- | --- |
| PCB outline | 18.415 × 18.0975 | Hans: 0.725 × 0.7125 inch |
| Lower mounting center | 3.175, 2.69875 | Hans |
| Upper mounting center | 3.175, 15.39875 | Hans |
| Header pin 1 | 7.14375, 15.39875 | Derived from Hans's pin 3 and pitch |
| Header pin 3 | 12.22375, 15.39875 | Hans |
| Header pin 5 | 17.30375, 15.39875 | Derived from Hans's pin 3 and pitch |
| Header pitch | 2.54 | Hans and standard KiCad connector |
| SMA signal center | 4.203549886, 9.04875 | Hans: 0.16549409, 0.35625 inch |
| Host socket pads / drills | 1.7 / 1.0 diameter | Standard KiCad 1×5 socket pattern |
| Host mounting drills | 3.2 diameter, unplated | Chosen M3 clearance, not a supplied module hole measurement |

The header and socket use actual locally copied **KiCad 10.0.6 standard 1×5 vertical STEP solids**: 0.64 mm square pins, 2.54 mm male insulator, 6 mm mating pin length, 3 mm male solder tails, 8.5 mm female body and 3.1 mm female tails. These are generic standard connector dimensions, not a supplier part-number selection.

The [QLG3 product page](https://qrp-labs.com/qlg3.html) specifies 11 mm spacers. The nominal fully seated generic connector stack is 8.5 + 2.54 = **11.04 mm**, so the model locates the daughterboard underside there and depicts 11 mm spacers. The resulting 0.04 mm nominal gap is retained; actual socket engagement and assembly tolerances require checking with the purchased hardware.

The remaining dimensions are **user-authorized approximations**, informed by the underside assembly photographs on page 61 of the [QMX+ assembly manual, revision 3.07a](https://qrp-labs.com/images/qmxp/manuals/assembly_3_07a.pdf#page=61):

- PCB thickness 1.6 mm, square-corner envelope, module holes modeled at 3.2 mm.
- SMA body 6.35 × 6.35 × 8.5 mm, barrel 8 mm long and 6.35 mm diameter. Thread rings and dielectric opening are visual details, not thread or mating specifications.
- E108 receiver body 10 × 10 × 2.5 mm, centered at assembled X=12.7, Y=12.2975 mm on top (source-view Y=5.8 mm). Small component and lead details are omitted.
- M3 spacers 5.5 mm across flats and simplified upper screw heads.

The full daughterboard and projected SMA remain on F.Fab as reference geometry; the module outline also remains on F.SilkS, **not Edge.Cuts**. There is no full-module courtyard or blanket component keepout. Three named **front-side component keepouts** reserve only:

- The socket body plus 0.5 mm clearance: 13.7 × 3.54 mm.
- Each mounting location: a 7.4 × 7.4 mm square centered on its hole. This encloses the provisional 5.5 mm-across-flats hex post's 6.351 mm corner diameter at any rotation, plus at least 0.5 mm per side.

The F.CrtYd outlines cover the same hardware envelopes. The adjacent socket/post courtyard regions are merged into one closed outline to avoid self-overlap; the other post has its own closed outline. The rule areas prohibit other footprints on F.Cu, while allowing tracks, vias, pads and copper pours subject to ordinary pad/hole clearance rules. They do not impose backside component restrictions.

The remaining area is available for components that fit vertically below the QLG3. The nominal underside height is 11.04 mm, reduced locally by solder tails and small reverse-side parts; this is not an automatic component-height check. The approximate post model near pin 1 crowds the socket, so final post diameter/shape and assembly fit still require confirmation; the conservative keepout does not establish a compatible hardware selection. A host TX SMA under the daughterboard still requires a vertical-clearance assessment. The antenna and mating cable are not depicted.

## Validation

Native KiCad symbol/footprint SVG exports and the colored 3D render were inspected. After restricting the keepouts to the hardware, the updated courtyard drawing was also inspected. A C_0603 probe at assembled X=12, Y=9 mm passes DRC beneath the module; three probes placed at the socket and mounting centers each trigger the corresponding named `items_not_allowed` error. That deliberately invalid fixture has 27 total expected collision findings, including the three keepout errors; none is suppressed. Five numbered pads and two unnumbered mounting holes were checked against the coordinate table; symbol pins match pads 1–5. CadQuery validates every generated solid. A separate ignored fixture under `generated/qlg3-part/` passed footprint DRC with the existing project rules: **0 violations, 0 unconnected pads, 0 footprint errors, no ignored checks**. This is a mechanical library fixture, not a wired transmitter. Sandboxed DRC initially aborted during macOS application registration; rerunning with approved native access completed successfully. An initial fixture-only reference-text/board-edge warning was resolved by enlarging the test board, without changing footprint geometry or rules.

In the working checkout with the separate in-progress wiring edits, schematic ERC remains **3 errors, 0 warnings**: undriven U11 VSYS, GND power input and U41 IN. Those pre-existing findings are unrelated to this unplaced part. The initial library-part creation preserved the active schematic and PCB; the later J71 assignment updates only its metadata and footprint selection, preserving connectivity and the active PCB. Whole-design schematic/PCB parity and physical fit are not claimed.

## Rebuild and provenance

Install the pinned dependency from [requirements.txt](requirements.txt) in an isolated Python environment, then run `python generate_qlg3.py` from this folder. The generator reads local inputs only and replaces only the named symbol within the library. It writes the footprint, STEP and VRML together. Keep both standard connector STEP inputs beside the generated models.

The symbol, footprint and generator are original repository work under the [MIT license](../LICENSE.md). Hans Summers/QRP Labs supplied the engineering drawing; it is retained with attribution and no new license grant asserted. The copied standard connector STEP files and the combined STEP/VRML that incorporate them retain [CC BY-SA 4.0 with the KiCad library exception](../KICAD-LIBRARY-LICENSE.md). Source collections: [KiCad 3D models](https://gitlab.com/kicad/libraries/kicad-packages3D), `Connector_PinHeader_2.54mm` and `Connector_PinSocket_2.54mm`.

## Focused commit scope

The part commit includes J71 metadata/footprint assignment, library assets and these notes. Separate circuit wiring, TP71 placement, control-pin decisions and other schematic edits remain outside this commit. The committed schematic retains the earlier unwired symbol-placement baseline; its ERC result is recorded separately in [validation](../VALIDATION.md). The 3-error working-checkout result above must not be applied to that unwired snapshot.
