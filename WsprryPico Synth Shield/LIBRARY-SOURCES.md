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
| JST_PH_B5B-PH-K_1x05_P2.00mm_Vertical | Connector_JST | Retained historical asset; no longer assigned to J71 |
| PinSocket_1x05_P2.54mm_Vertical | Connector_PinSocket_2.54mm | Exclude from BOM/positions; STEP copied locally via `${KIPRJMOD}` |
| TestPoint_Pad_D2.0mm | TestPoint | Exclude from BOM/positions; copper hand-wire pad TP71 |
| SMA_BAT_Wireless_BWSMA-KWE-Z001 | Connector_Coaxial | Historical asset; superseded for J61 by SMA_Adafruit_1865_EdgeMount |
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

## QLG3 socket update, 2026-10-07

J71 now uses the copied KiCad 10.0.6 1x5 female socket footprint: 2.54 mm pitch, 10.16 mm first-to-last center spacing, 1.0 mm drills and 1.7 mm pads. It mounts on the shield top and accepts the QLG3 underside male pins. The copied STEP file uses the same KiCad library license and is generic geometry, not proof of mating height or SMA clearance. TP71 uses a copied 2 mm exposed copper test pad. Both footprints and instances exclude BOM/positions. Hans's board/header/mounting coordinates are now captured in the reusable module asset below. Actual socket/header engagement remains an assembly check. The historical JST footprint remains available but is no longer selected.

## QLG3 daughterboard part, 2026-10-07

Added original `QLG3_GPS_UndersideHeader` host footprint, dimension inputs and generator, plus local colored VRML and STEP assembly. The dimensions, exact pin mapping, standard connector geometry and photo-based approximations are recorded in [the module documentation](qlg3-model/README.md). The new male-header STEP and existing female-socket STEP are copied from KiCad 10.0.6 under the KiCad library terms; the combined 3D assets retain those terms. J71 now assigns this full module footprint; its electrical pins remain 1–5.

Orientation corrected to the user's requested E108/SMA-up, header-down arrangement. Hans's drawing is transformed using X′=X and Y′=18.0975−Y; header pads move to KiCad Y=−2.69875 mm without changing their numbers. The male header is installed opposite the E108 face, unlike the QMX+ photo assembly.

The QLG3 courtyard and front-side component keepouts now reserve only the socket plus 0.5 mm and two 7.4 mm-square mounting-hardware envelopes. The full board/SMA outlines remain fabrication references. The open space beneath the daughterboard accepts height-compatible components; normal routing clearances still apply. See the module documentation for limits and the DRC placement probes.

## J71 assembly assignment

J71 selects `QLG3_GPS_UndersideHeader`, whose local VRML model depicts the complete GPS receiver assembly. The generic socket-only footprint remains an available library asset. The hardware is a plain unkeyed 1×5 0.1-inch (2.54 mm) socket/header pair. Stale JST PH, 2.0 mm, keyed-connector and C157993 instance metadata were removed; BOM/position exclusions and all wiring are preserved.

## QLG3 single-post variant, 2026-10-07

Added `QLG3_GPS_UndersideHeader_SinglePost` symbol, footprint and local STEP/VRML models, generated with `qlg3-model/generate_qlg3.py --single-post`. It preserves the original two-post assets and their provenance/license terms. J71 now assigns this variant in the schematic and saved board; the upper host mounting hardware and its keepout/courtyard are omitted. Both holes remain in the depicted QLG3 PCB. See [variant scope and checks](qlg3-model/README.md#single-post-variant--selected-2026-10-07).

## J61 board-edge SMA restored, 2026-10-07

Copied `SMA_Adafruit_1865_EdgeMount` and `SMA_Adafruit_1865_Preview.wrl` from the GPIO shield into independent Synth libraries; only the footprint model path changes to the Synth `${KIPRJMOD}` folder. Adafruit's public-domain land-pattern attribution and the repository-MIT illustrative model are retained. [Source provenance and model limits](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md). The old BAT Wireless footprint remains an unused historical asset, including its unresolved stock model reference; J61 now has a resolving local preview model.

J61's schematic/PCB assignments and purchasing metadata now identify the edge-launch part. Pin 1 remains TX_OUT and all four pad-2 lands remain GND. The signal land is on F.Cu; ground lands straddle both faces of a 1.6 mm board. BOM/position exclusions remain set. This is a hand-soldered connector with no paste apertures. The original footprint origin is retained in the unplaced staging area; final board-edge placement remains work.

## TP71 through-hole test point — 2026-10-08

Imported `TestPoint_THTPad_1.0x1.0mm_Drill0.5mm` unchanged from the installed KiCad 10.0.6 `TestPoint.pretty` library into `wsprrypico-synth-shield.pretty`. It has one 1 × 1 mm rectangular plated-through pad with a 0.5 mm drill, no 3D model, and explicit BOM/position exclusions. It retains the [KiCad library license](KICAD-LIBRARY-LICENSE.md). The existing project-local footprint table resolves the new asset through `${KIPRJMOD}`.

TP71's schematic and board assignments now reference the local footprint. The local TestPoint symbol's default footprint and filter, the schematic's cached symbol definition and the PCB's copied filter all match the new choice. This supersedes the original 2 mm surface-pad selection; the older footprint remains available. Pad UUID, GPS_RX net, position, user geometry, teardrops and all unrelated saved layout/project edits are preserved.

## 2026-10-08 onboard GNSS, 90-series

Added original `ATGM336H_5N31` symbol and `Zhongke_ATGM336H-5N31_9.7x10.1mm_P1.1mm` footprint, using the manufacturer's [ATGM336H-5N manual](https://www.lcsc.com/datasheet/C90770.pdf), pages 9-14. Pin meanings are specific to ATGM336H, including NC pin13 and optional SDA/SCL16/17. The footprint rotates the manual's top view by 180 degrees to put pin1 at upper left: pad rows x=±4.85 mm, pitch1.1 mm, end centers y=±4.4 mm, lands1.8×0.8 mm. Body9.7×10.1 mm. The original local VRML is an approximate 2.4 mm-high body envelope, not a supplier solid. These independently drawn project assets use the repository MIT license; manufacturer reference documents are not redistributed.

Imported installed KiCad `Inductor_SMD:L_0603_1608Metric` for factory SMT L91. Existing KiCad library attribution/license applies. Its standard STEP model was copied unchanged into the local 3D folder and referenced through `${KIPRJMOD}`; it describes a generic envelope rather than the exact muRata part. J91 reuses the local edge SMA, excluded from BOM/positions. QLG3 assets remain available but are no longer assigned in the current schematic. Current receiver and choke stock checks are recorded in PARTS.csv. PCB synchronization and physical/RF qualification remain pending.
