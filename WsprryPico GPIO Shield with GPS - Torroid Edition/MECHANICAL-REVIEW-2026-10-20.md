# Torroid Edition fitted-Pico opposite-face terminal recheck, 2026-10-20

**Historical review:** mounting-material selections and support height in this record are superseded by the [2026-10-21 low-support review](MECHANICAL-REVIEW-2026-10-21.md). Refer to current validation for saved-source identities and checks.

**The output capacitor bank is now one compact, consistently oriented underside row.** The bank, relocated feed bypasses, hand-fit joint envelopes and top-side support clear the fitted-Pico reference under the stated assumptions. Exact physical assembly and RF qualification remain open. Current procurement data are in [PARTS.md](PARTS.md#availability-checked-2026-10-20); the selected bumper and $4.95 small adhesive tube have small-lot listings.

This replaces the earlier same-day review’s 470 nF / APEM / 5 kΩ findings. It uses KiCad **10.0.6 outside the sandbox**, native source checks, and OpenCascade solid-distance checks against the official Raspberry Pi Pico W STEP as a mechanical reference for Pico 2 W. The active PCB was updated under the user’s instruction; the fitted dummy boards remain separate review fixtures.

## Reference assembly and limits

The [official Pico W model](https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008318-DS-1-PicoW-step.zip) is inverted to put the bare Pico back toward the shield and its components outward. The [Pico-series documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html) and [Pico 2 W datasheet](https://pip-assets.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w/documents/RP-008304-DS-2-pico-2-w-datasheet.pdf) establish the 51 × 21 mm compatible board/header envelope. The MCU solid is a Pico W reference, not an exact Pico 2 W model; the cavity faces the bare board.

The 40 header holes align within 0.000224 mm in the established reference pose. The 11.00 mm nominal PCB-facing gap uses the selected 8.50 mm female socket and a 2.50 mm male-header spacer reference. Minimum housing-height scenario is 10.65 mm. An additional conservative 8.30 mm screen ignores the male spacer entirely. These are explicit reference geometries, not a qualified connector engagement stack. The male reference is not an added shield BOM purchase.

![Reference assembly](generated/opposite-face-validation/fit/fitted-profile.png)

| Checked envelope | Nominal 11.00 mm gap | Minimum-housing 10.65 mm gap | Conservative 8.30 mm gap |
| --- | ---: | ---: | ---: |
| C61 and C64/C66–C69, maximum 1.8 mm height + 0.10 mm solder stand-off | **9.10 mm** | **8.75 mm** | **6.40 mm** |
| C63 maximum 1.8 mm height + 0.10 mm solder stand-off | **9.10 mm** | **8.75 mm** | **6.40 mm** |
| C62 maximum 0.95 mm height + 0.10 mm solder stand-off | **9.95 mm** | **9.60 mm** | **7.25 mm** |
| Q61, three T61 holes, SW11, D11 final solder/lead projection ≤1.5 mm | **9.50 mm** | **9.15 mm** | **6.80 mm** |

![Cavity with socket housings and male-header fixture hidden](generated/opposite-face-validation/fit/cavity.png)

The cutaway hides housings and male-header fixture to expose the cavity, retaining the same board separation. Blue marks conservative capacitor maxima; grey marks lead/solder envelopes. No underside ties remain. Models and distances omit board warp and deviations beyond the stated allowances.

## Switch, LED and capacitor margins

SW11 **Alps Alpine SKHLACA010**, now at **(162.20, 84.10) mm**, has pad-1 radius 1.125 mm and nearest pad edge Y = 82.975 mm. The nominal socket inner edge is Y = 82.240 mm, giving **0.735 mm** lateral margin, increased by 0.600 mm from the prior 0.135 mm. Its 6 × 3.5 mm body and 4.3 ±0.2 mm actuator use the [manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/1a3e3d210bb2ea7d5f11862ab84517d8.pdf?productCode=C382056). The local 1.30 mm holes at 6.50 mm pitch provide allowance over the recommended 1.25 mm holes. Spring-lead compliance, finished-hole tolerance and the socket’s unspecified width tolerance still need real samples. The nominal preview is original repository geometry, not manufacturer CAD.

D11 moved to **(162.10, 93.40) mm**, putting its lower pad edge at 97.040 mm versus the nominal socket edge 97.480 mm: **0.440 mm** margin. Its courtyard clears the switch. The [Kingbright drawing](https://www.kingbrightusa.com/images/catalog/spec/wp710a10lid.pdf) and polarity govern fitting. The generic LED model’s short tails are illustrative: an untrimmed ≥27 mm real lead can project about 25.4 mm below the shield and intersect the Pico. Trim and inspect all leads while preserving sound joints.

The Alps terminals are 3.5 ±0.5 mm from the seating plane, at most approximately **2.4 mm below a 1.6 mm PCB** if flush fitted. The untrimmed maximum still clears the nominal Pico reference by **8.6 mm**, but retain the common ≤1.5 mm finished joint/lead target. Q61 keeps 1.00 mm finished holes and the documented outer-lead forming; the generic TO-92 solid does not represent those formed leads.

The five output caps use **Walsin 1206N104J500CT**, maximum **3.40 × 1.80 × 1.80 mm**, and the 0.10 mm assembly allowance. All five now face 90° at Y = 92.30 mm and X = 125.88, 128.30, 130.72, 133.14 and 135.56 mm. Maximum bodies reach Y = 94.00 mm, leaving **3.48 mm** to the nominal lower socket body. Their 2.42 mm pitch leaves **0.62 mm** between maximum-width bodies. The bank is about 11.48 × 3.40 mm in maximum body extent; its courtyard reserve is about 12.08 × 4.60 mm. At the ends, maximum bodies leave approximately **0.406 mm** to the nearest SMA ground land and **4.40 mm** to the relocated T61 output land. Allow for actual hand-solder fillets and assembly tolerances. Moved R62/R63/C65 stay above the bank on B.Cu, clear of the capacitor courtyards and T61 solder-joint envelopes. C61 retains **0.96 mm** planar maximum-body clearance to the upper socket. The former oversized 2220 model and footprint are absent.

## Transformer retention and side holes

T61 remains at **(146.75, 89.80) mm**, with the unchanged Fair-Rite 5977000621 core and 15+15 AWG26 turns. The **25 × 13.5 mm** front courtyard spans X **134.25–159.25**, Y **83.05–96.55 mm**, with 0.56 / 0.68 mm upper/lower courtyard clearance to the socket courtyards. The accepted body, support and leads remain ≤24 × 11.4 mm in plan and ≤30 mm above the PCB, inside the outline. No ties or underside straps are present.

Separate 1/4 holes are on the +Y face; the shared 2/3 hole is on the opposite -Y face. Only pin 1 moves in this correction; the common drain hole and output terminal remain fixed. Ends 1/4 use 1.0 mm holes at (151.75,95.10) and (141.75,95.10); ends 2/3 share a 1.2 mm hole at (141.15,85.20). Land-to-nominal-socket-body margins are **1.38 mm** at pin 1, **1.76 mm** at common 2/3 and **1.38 mm** at pin 4. The minimum nominal bumper-to-land gap is **0.373 mm**. These calculations assume joint spread stays within the land envelope; qualify actual fillets and tolerances.

End 1 is dressed around the lower-right exterior, clear of the core and bumper, to join end 4 on the +Y face. End 3 crosses the opposite -Y axial face outside the core window and above the bumper before joining end 2; no added core passage or metal retaining loop is specified. The nominal 11 × 5 mm COM-17736 bumper and thin EGS10W-20G bed are unchanged. Bare core bottom is about 6 mm above the board, including nominal 1 mm bedding. The 330° winding leaves a lower 30° bare arc. The model illustrates this routing but is not a continuous winding or a tolerance/adhesion qualification.

C62 moves to **(149.50,94.30) mm**, C63 to **(149.70,91.00) mm**, both 180° on B.Cu. The [PSA FN series manufacturer sheet](https://datasheet.lcsc.com/datasheet/pdf/54060d89de1cf445ebdd0f6237285e17.pdf?productCode=C235731) gives C62 FN18X104K500PBG a maximum 1.75 × 0.95 × 0.95 mm body; the fit screen uses 1.8 × 1.0 × 0.95 mm plus 0.10 mm stand-off. The [Samsung manufacturer reference](https://datasheet.lcsc.com/datasheet/pdf/02336ea48ea44ca18c72517dd3cb7b47.pdf?productCode=C14860) gives C63 a maximum 3.4 × 1.8 × 1.8 mm body. Both clear the Pico reference as tabulated. The conservative C62 body-to-T61-pin-1 land gap is **0.35 mm**; control hand-solder spread and inspect that joint. T61 joint envelopes do not overlap either bypass body.

Confirm actual bumper size/compression, winding build, adhesion to both interfaces, full cure, finished-hole fit, socket engagement and the 30 mm enclosure allowance on samples. Untrimmed LED leads intersect the Pico reference. Keep finished hand joints ≤1.5 mm below the shield while preserving sound solder joints.

## Checks and evidence

KiCad **10.0.6** reports **0 board DRC violations, 0 opens, and 0 schematic/PCB differences**. ERC reports **0 violations with four existing ignored categories**, listed in [validation](VALIDATION.md). All 21 factory SMT parts remain bottom; the five-capacitor bank, U31 bypasses, socket rows, SMA, Q61 and antenna geometry are preserved. T61 terminals, C62/C63 and associated local routing change.

Ignored `generated/opposite-face-validation/fit/` holds current fitted/cutaway boards, portable models, geometry and solid-distance results. These are review fixtures, not manufacturing inputs; production source has no Pico dummy model. Native 3D and copper plots have been visually inspected. Physical assembly, retention and RF behavior remain unmeasured.
