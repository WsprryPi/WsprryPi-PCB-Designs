# Torroid Edition narrower-pad clearance recheck, 2026-10-21

**The native model now shows an 8 mm diameter insulating pad, reduced from 11 mm, with the short 1.25 mm height retained. Bedding is 4 × 6 × 0.5 mm.** The conservative winding/lead envelope clears the pad by **0.788 mm**, replacing the previous 0.010 mm allowance, and clears bedding by at least **1.141 mm**. Mounting materials remain builder-selected. Winding, lead dressing and vertical geometry are unchanged; this remains a nominal illustration requiring a real builder fit check.

The preceding review corrected a pre-existing 3D-model coordinate error: footprint +Y points down, while VRML/CAD +Y points up. The generator now reflects Y once on export. Model 1/4 tails land in their +Y PCB holes and the two common tails land in the single opposite-face 2/3 hole. Hole positions, winding-end mapping and electrical connections are unchanged. A native terminal coupon was checked before and after that correction; the unchanged terminal tails are reverified numerically in this revision.

![Current fitted Pico assembly](generated/narrow-pad-validation/fitted-isometric.png)

## Support and winding

| Quantity | Current illustration |
| --- | ---: |
| Insulating pad diameter / height | 8.00 / 1.25 mm; formerly 11.00 mm diameter |
| Bedding allowance | 4 × 6 × 0.50 mm; formerly 4 × 7.1 mm plan |
| Bare core bottom / top above PCB | 1.75 / 23.60 mm |
| Model height above PCB | 24.315 mm |
| Model plan envelope, including leads/support | 23.308 × 11.024 mm |
| Retained finished assembly acceptance | ≤24 × 11.4 × 30 mm above board |
| Conservative lower-turn envelope to PCB | 1.260 mm |
| Conservative wire-radius envelope to pad | 0.788 mm, winding and free leads |
| Winding / free leads to bedding | 1.141 / 1.155 mm |
| Bedding corners inside pad edge | 0.394 mm |

The clearance screen uses exact OpenCascade distances from the linear winding/lead centerlines to the cylindrical pad and rectangular bedding, subtracting a 0.2235 mm radius corresponding to the selected nominal 0.447 mm heavy-build wire. Independent segment minimization in the maintained generator agrees within 0.000001 mm. It does not include winding variation, twist build, coating tolerance, support compression or adhesive fillets. Adjust the actual pad shape, bedding and lead dressing to avoid pinching enamel or touching exposed copper. The 1.25 mm pad and 0.5 mm allowance are illustrative, not a mandatory product or minimum safe mounting height.

The preview retains continuous illustrative paths, with **15 window passages in A, 15 in B, and zero additional window passages in each free-tail route**. Twists are omitted. Real winding continuity, series-aiding phase, inductance, insulation and fit remain build checks. Starting ends are 1/3; finishing ends 2/4. Ends 1 and 2 change faces around the lower exterior; 3 crosses below the window to the common hole; 4 remains on the separate-hole face.

The unchanged 25 × 13.5 mm courtyard and terminal map stay within the 53.33 × 22.85 mm outline. The 8 mm illustrative support diameter leaves **1.873 mm** nominal clearance to the closest land, an increase of 1.5 mm. Retention and compatible mounting materials are up to the builder; winding leads are not the primary retainer, and no conductive loop may pass through the window.

## Nearby parts and sockets

OpenCascade distances below use the **entire rectangular T61 model envelope** against the stated neighboring solid/envelope. Because the box includes empty space, these are conservative model-space separations, not exact distances to a real wound transformer. Manufacturer drawings, lateral tolerances and actual leads govern fit.

| Neighbor | Conservative separation | Reference |
| --- | ---: | --- |
| Q61 | 1.83 mm | Generic installed TO-92 STEP; actual formed BS170 leads not represented |
| D11 | 1.80 mm | Generic 3 mm LED STEP; actual Kingbright body/trim still govern |
| SW11 | 2.05 mm | Nominal 6 × 3.5 mm body box, 4.5 mm maximum actuator height |
| Upper socket housing | 2.05 mm | Existing nominal housing envelope |
| Lower socket housing | 2.17 mm | Existing nominal housing envelope |

No placements, pad coordinates, drills, traces, vias, zones or antenna geometry change. The C62-body-to-T61-pin-1-land screen remains about **0.35 mm**; keep hand-solder spread controlled. Socket-body-to-SW11/D11 land margins remain 0.735 / 0.440 mm from the unchanged board geometry.

## Fitted Pico and underside joints

The [official Pico W STEP](https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008318-DS-1-PicoW-step.zip) is inverted with its bare back toward the shield, as in the [previous reference setup](MECHANICAL-REVIEW-2026-10-20.md#reference-assembly-and-limits). It is a Pico 2 W board/header-envelope reference, not an exact Pico 2 W component model or qualified connector engagement. Header alignment and board pose are retained. The smaller top-side support does not change the underside stack.

| Envelope | 11.00 mm nominal gap | 10.65 mm housing-minimum gap | 8.30 mm conservative gap |
| --- | ---: | ---: | ---: |
| T61/Q61/SW11/D11, finished joints ≤1.5 mm | 9.50 mm | 9.15 mm | 6.80 mm |
| Output caps/C61/C63, max 1.8 mm + 0.1 mm stand-off | 9.10 mm | 8.75 mm | 6.40 mm |
| C62, max 0.95 mm + 0.1 mm stand-off | 9.95 mm | 9.60 mm | 7.25 mm |

These are fresh OpenCascade checks against the retained official reference. Untrimmed LED leads still intersect the Pico reference; trim and inspect hand joints while preserving sound solder joints. Board warp, real support/coil variation and deviations outside these stated envelopes are not modeled.

![Native profile with narrower support pad](generated/narrow-pad-validation/fitted-profile.png)

## Checks and records

KiCad **10.0.6**, run outside the sandbox: full DRC **0 violations, 0 opens, 0 schematic/PCB differences**. ERC **0 reported**, retaining the existing four ignored categories listed in [validation](VALIDATION.md). The updated native model, fitted assembly and four mounting-drawing pages were visually checked. Numerical end-cap positions verify the unchanged model-to-hole alignment. All 21 factory SMT positions stay on B.Cu. There are still three physical T61 holes for four logical winding ends.

Workbook and CSV continue to leave support/attachment materials to the builder. No required mounting-material manufacturer, MPN, source, pack quantity or price remains. Wire and electronics selections are unchanged. The workbook is byte-identical; its existing support note specifies height without a diameter. Only CSV cell D34 changes, from 11 to 8 mm diameter. Source changes are limited to the T61 support Fab circle, model/generator/drawings, that CSV note, matching documentation and the study's PCB source hash.

Ignored `generated/narrow-pad-validation/` holds the current renders, fitted fixtures, geometry, native checks, source-change inventory and clearance results. Earlier terminal-coupon before/after views remain in `generated/low-support-validation/`. Production sources contain no fitted-Pico dummy or temporary absolute model paths. Physical assembly, independent retention, phase/inductance, DC-biased RF behavior and thermal performance remain unmeasured.
