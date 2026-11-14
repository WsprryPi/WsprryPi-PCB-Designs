# T61 low support and side terminals

**The model shows an illustrative 8 mm diameter × 1.25 mm insulating pad, reduced from 11 mm diameter, with a 4 × 6 × 0.5 mm bedding allowance. The short height is retained. Mounting materials and attachment are selected by the builder.** No bumper or adhesive manufacturer, MPN, supplier, pack quantity or cost is prescribed. The bare core bottom is 1.75 mm above the PCB in this illustration, 4.25 mm lower than the previous mount.

Separate winding ends **1 and 4 are on the +Y axial face**. Ends **2 and 3 share one 1.2 mm finished plated hole on the opposite -Y face**. Ends 1/4 use separate 1.0 mm holes. Terminal coordinates, courtyard, core selection and copper routing are unchanged. All 21 factory SMT positions stay underneath.

The [four-page drawing](output/pdf/t61-mounting.pdf) includes the terminal plan and dimensioned lower-support elevation. [Dimensions and model paths](dimensions.json), the [electrical study](../bifilar-transformer-study/README.md), [current clearance review](../../MECHANICAL-REVIEW-2026-10-21.md) and [validation](../../VALIDATION.md) record the prototype. Models show nominal geometry; actual winding, mounting and RF performance remain unqualified.

## Core comparison and selection

| Core | Turns per wire | Nominal / AL-minimum primary L | Status |
| --- | ---: | ---: | --- |
| **5977000621, coated 77, 21.85 mm maximum OD** | **15** | **285.75 / 200.025 µH** | Retained within-outline prototype |
| 5977004921, 16.9 mm coated 77 | 14 | 274.40 / 192.080 µH | Smaller, higher calculated DC magnetic stress |
| 5943000621, same-size coated 43 | 24 | 270.72 / 203.040 µH | HF comparison; not selected |
| 5977002721, 36.8 mm coated 77 | 11 | 272.25 / 190.575 µH | Superseded overhanging proposal |

The mounting change does not select a different core or winding count. See the study for material data, calculated DC field/flux and the **≥100 µH at 200 mA** initial LF measurement gate. Full 2200 m–10 m behavior remains unmeasured.

## Mounting materials

| Item | Parts-record treatment |
| --- | --- |
| T61 core | Fair-Rite **5977000621**, one coated core; MPN buys the core only |
| T61-WIRE | Remington **26H200P.125**, AWG26 heavy enamel; initially two identified 0.65 m lengths |
| T61-SUPPORT | Builder-selected electrically insulating support; no required MPN or purchase quantity |
| T61-ADHESIVE | Optional builder-selected adhesive or other attachment method; no required adhesive or purchase quantity |

The two mounting rows are hand-build reminders, not schematic references or factory positions. Previous SparkFun bumper and Chip Quik adhesive selections, prices and supplier links are removed from active purchasing records. Wire and electronic component selections are unchanged. Select materials compatible with the core coating, PCB and operating temperature; verify shape/compression, retention and any preparation/cure requirements. Winding leads are not the primary retainer. Do not add a conductive closed loop through the window.

## Dimensions and acceptance envelope

| Item | Dimension / requirement |
| --- | --- |
| Bare core | 21.85 mm OD maximum, 12.40 mm ID minimum, 7.10 mm axial maximum |
| Illustrated support | **8 mm diameter × 1.25 mm high**, material selected by builder |
| Illustrated bedding allowance | **4 × 6 mm plan, 0.50 mm high**; not a specified adhesive or finished thickness |
| Illustrated bare-core bottom / top | **1.75 / 23.60 mm** above PCB |
| Current preview winding height | About **24.32 mm** above PCB |
| Finished assembly acceptance | **≤24 × 11.4 mm** in plan, **≤30 mm** above PCB |
| Front courtyard | **25 × 13.5 mm**; X 134.25–159.25, Y 83.05–96.55 mm |
| Position / orientation | **(146.75, 89.80) mm, 0°**; ring plane X–Z, axis Y |
| Underside joints | **≤1.5 mm** total lead/solder projection; preserve sound joints |

The 1.25/0.50 mm stack is illustrative, not a minimum qualified mounting height. The conservative nominal round-wire envelope clears the narrower pad by **0.788 mm** and the 4 × 6 mm bedding by at least **1.141 mm**. Bedding corners sit **0.394 mm inside** the pad edge. Independent OpenCascade solid-to-polyline distances agree with the generator's segment minimization to within 0.000001 mm, after subtracting the nominal 0.2235 mm wire radius. Check actual support shape, bedding and winding/lead dressing to avoid pinching insulation or touching copper. The lower-turn envelope stays about **1.26 mm above the PCB** in the nominal illustration. Twists, winding variation and support compression are not qualified by the model.

The 8 mm support plan clears the nearest land by about **1.873 mm**, increased from 0.373 mm. Courtyard separation to socket courtyards remains 0.56 / 0.68 mm. Finished acceptance dimensions do not establish supplier tolerances.

## Terminal definition

Local asset: [T61_FairRite_5977000621_Upright_Bumper_4Pin.kicad_mod](../../wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/T61_FairRite_5977000621_Upright_Bumper_4Pin.kicad_mod). The legacy `Bumper` filename is retained for library references; it no longer specifies a catalog bumper. `4Pin` describes four logical winding ends.

| End | Local X / Y, mm | PCB X / Y, mm | Winding end | Net / finished hole |
| --- | --- | --- | --- | --- |
| 1, square | +5.00 / +5.30 | 151.75 / 95.10 | A start / dot | AMP_XFMR_FEED / 1.0 mm |
| 2 | −5.60 / −4.60 | 141.15 / 85.20 | A finish | AMP_DRAIN / 1.2 mm common |
| 3 | same as 2 | same as 2 | B start / dot | AMP_DRAIN / shares hole 2 |
| 4 | −5.00 / +5.30 | 141.75 / 95.10 | B finish | AMP_RF_XFMR / 1.0 mm |

Ends 1/4 use 2.0 mm lands. Common 2/3 uses a 2.4 mm land. Pad 2 supplies the barrel and both annuli; pad 3 is coincident drill-free F.Cu copper. Output has exactly three T61 holes. Two nominal 0.405 mm bare AWG26 conductors fit side by side in the 1.2 mm hole before tin and finished-hole tolerance. Strip enamel fully, tin lightly and check a real pair and the fabricator's allowance.

## Winding and mounting

1. Identify starts 1/3 and finishes 2/4. Twist initially 8–10 twists/inch and wind 15 window passages per wire over about 330°, leaving the lower 30° bare. Check continuity, phase, coating and inductance before mounting.
2. Dress end 1 around the lower-right exterior to +Y. After the final window passage, end 2 returns around the lower-left exterior to -Y. End 3 crosses the -Y face below the window and above the support to join 2. End 4 drops to +Y beside 1. No free-tail route goes through the window again. The model represents fifteen passages per wire with zero extra dressing passages; real continuity and phasing still require checking.
3. Select and fit the insulating support and attachment. Keep winding and leads clear, with slack for compression and handling. Do not pinch low turns under the core. Keep material off terminals, sockets and the antenna opening. Verify retention independently of the soldered tails and follow instructions for the chosen material.
4. Insert stripped 2/3 together and make one sound joint; solder 1/4 separately. Trim underside joints to ≤1.5 mm total projection. Inspect C62's approximately 0.35 mm conservative lateral body-to-pin-1-land gap and control hand-solder spread.
5. Check socket/Pico engagement, finished holes, support movement, warm operation and handling/vibration on a sample. The 30 mm assembly/enclosure limit is retained.

## Sources and validation

The library and placed T61 footprint have no F.Fab user annotations. The required value field is hidden; the silkscreen reference and terminal IDs remain visible. Fabrication outlines, support circle, courtyard, pads and the 3D model are unchanged. The generator retains this display cleanup.

The [generator](generate_mount.py) writes the local footprint, original MIT preview, dimensions, nominal pad/bedding clearance calculations and PDF. It does not read or write the PCB. This revision changes only the support circle from 11 to 8 mm diameter in both the local footprint and placed T61 F.Fab drawing. The model also narrows the bedding plan from 4 × 7.1 to 4 × 6 mm. Winding/lead paths and all vertical geometry are unchanged. No pad geometry, UUID, net, placement, trace, via, zone or outline changes are made. Schematic, symbol library, settings and library tables remain byte-identical. [Validation](../../VALIDATION.md) records checks and exact saved sources.

The previous 3D recheck corrected the model's Y-axis reflection: footprint coordinates are +Y down, while native VRML/CAD coordinates are +Y up. The exporter reflects Y once so lead 1/4 and shared 2/3 now align with their actual PCB holes. This changes the preview, not the drilled positions or connections.
