# WsprryPico GPIO Shield with GPS - Torroid Edition footprint and model sources

The independent `wsprrypico-gpio-shield-with-gps-torroid-edition` libraries use `${KIPRJMOD}` paths. The library contains **14 active footprint types**, matching the saved schematic and PCB. T61 uses the original local upright low-support footprint, now placed and routed on the main board. All 21 SMT positions are on the underside. The [parts inventory](PARTS.csv) and [validation](VALIDATION.md) record the current design.

## KiCad footprint assets

Copies originate in the [KiCad 10.0.6 footprint collection](https://gitlab.com/kicad/libraries/kicad-footprints) and retain **CC BY-SA 4.0 with the KiCad library exception**. See [KICAD-LIBRARY-LICENSE.md](KICAD-LIBRARY-LICENSE.md).

| Local footprint | Upstream collection | Relevant geometry or adaptation |
| --- | --- | --- |
| C_0603_1608Metric, C_0805_2012Metric, C_1206_3216Metric | Capacitor_SMD | Standard passive lands |
| R_0603_1608Metric, R_1206_3216Metric | Resistor_SMD | Standard passive lands; KiCad 10.0.6 1206 copy added for R64, 1 Ω / 0.25 W |
| LED_Kingbright_WP710A10LID_D3.0mm_P2.54mm_D1.3mm | LED_THT:LED_D3.0mm | Adapted to 1.30 mm finished holes, 2.20 mm pads and expanded courtyard; pad 1 cathode, pad 2 anode; top-silkscreen + marks the anode; silk cleared from larger lands |
| SW_PUSH_Alps_SKHLACA010 | Adapted KiCad Button_Switch_THT footprint; Alps-specific name and model; 6 × 3.5 mm body, 4.3 mm actuator, two 1.30 mm holes at 6.50 mm pitch | [Alps SKHL drawing](https://datasheet.lcsc.com/datasheet/pdf/1a3e3d210bb2ea7d5f11862ab84517d8.pdf?productCode=C382056) |
| SOT-23-6 | Package_TO_SOT_SMD | Reference text clears pin-1 silkscreen |
| Potentiometer_Bourns_TC33X_Vertical | Potentiometer_SMD | Pin 2 wiper; local illustrative model |
| TO-92_Inline | Package_TO_SOT_THT | 1.00 mm finished holes; 1.50 × 1.60 mm pads; 1.70 mm pitch |
| TestPoint_Pad_D1.0mm | TestPoint | TP61/TP62; top copper-only probe pads, no holes, excluded from BOM/positions; instance value printed on F.SilkS at 0.8 mm for probe +/−, offset left/right on the PCB |

Standard model references use `${KICAD10_3DMODEL_DIR}` where applicable and require the installed KiCad 3D library. Assigned local assets are listed in the [model inventory](wsprrypico-gpio-shield-with-gps-torroid-edition.3dshapes/README.md).

T61 has an electrical symbol with four independent terminals and marked winding starts. Its [prototype mounting definition](design/t61-mount/README.md) assigns three side-positioned PTH holes for four logical winding ends (1/4: 1.0 mm; common 2/3: 1.2 mm), with 1/4 on +Y and common 2/3 on -Y, a builder-selected insulating support and attachment (the model shows a 1.25 mm pad and 0.5 mm bedding allowance), no tie slots, a 25 × 13.5 mm front courtyard and an illustrative local model. The lengthwise assembly with a retained 30 mm height limit has no side overhang; the CAD layout passes courtyard and outline checks; physical fit remains open. The unused L61 and GNSS assets have been removed.

## Transistor

**BS170 TO-92:** the local footprint and placed Q61 use **1.00 mm finished plated holes**, **1.50 × 1.60 mm pads**, a **0.25 mm minimum nominal annular ring** and **1.70 mm pitch**, with **0.20 mm nominal adjacent copper clearance**. Local hole centers are X = −0.43, 1.27 and 2.97 mm. Gate/body center and pin mapping remain unchanged: 1 drain, 2 gate, 3 source.

The [onsemi BS170 drawing, case 135AN, page 8](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf#page=8) specifies maximum lead width/thickness of **0.56 × 0.52 mm**, giving a **0.7642 mm diagonal**. A 1.00 mm finished hole provides **0.2358 mm nominal diametral allowance**; even a 0.95 mm finished hole leaves 0.1858 mm. Specify finished plated-hole dimensions and confirm the fabricator's tolerance when ordering; the drill tool before plating is the fabricator's responsibility.

The straight-lead package has 1.27 mm nominal lead pitch. Gently form each outer lead **0.43 mm outward** for this 1.70 mm footprint, supporting the lead and keeping bending stress away from the body. The stock TO-92 model depicts straight leads at generic pitch and does not show this forming. The gate hole and body center align at local X = 1.27 mm. CAD check results and assembly limits are recorded in [VALIDATION.md](VALIDATION.md).

## Original footprints

`T61_FairRite_5977000621_Upright_Bumper_4Pin` and its preview model are original MIT-licensed repository work. [Dimensioned geometry, pad map, mounting materials and manufacturer sources](design/t61-mount/README.md) are maintained together with their generator. Ends 1/4 have 2.0 mm lands; the common 2/3 hole has a 2.4 mm land. Pad 2 owns the plated drill and both annuli; coincident pad 3 is drill-free F.Cu copper, preserving four-end schematic mapping without a duplicate drill. The `4Pin` asset suffix describes logical ends. The former terminal row is removed; there are three side holes, with separate 1/4 on +Y and shared 2/3 on -Y, no tie slots or underside straps. Silk is confined to the board-supported mounting region; the full projecting body is recorded on F.Fab/F.CrtYd. The preview now shows continuous illustrative paths with 15 window passages per wire and zero extra dressing passages, lowered with the core. The model omits wire twists and real winding, support and attachment tolerances; it does not qualify fit. The legacy `Bumper` asset name is retained for library compatibility and no longer prescribes a catalog bumper. See the [current clearance review](MECHANICAL-REVIEW-2026-10-21.md).

These factual-dimension drawings are original repository work under [LICENSE.md](LICENSE.md).

| Footprint | Geometry and pin numbering | Source |
| --- | --- | --- |
| Raspberry_Pi_Pico_2W_Header | Combined two-row, 40-pad interface, 2.54 mm pitch and 17.78 mm row spacing; only pin 1 square, pads 2–40 round; 1.508 mm lands and circular 1.00 mm drills; no USB arrow/text or printed 1/40 labels | [Project-local Pico reference assets](../Pico%202W%20Wattmeter%20Shield/pico-2w-libs/README.md) |

## Bias trimmer

The [Bourns TC33X-2 drawing](https://www.bourns.com/docs/product-datasheets/tc33.pdf) specifies a 3.6 × 3.8 mm body and asymmetric three-pad pattern. The footprint is a rotated implementation with 1.2 mm square end pads and a 1.5 × 1.6 mm wiper pad. **Pin 1 is the counterclockwise end, pin 2 the wiper, and pin 3 the clockwise end.** RV61 connects pin 3 to GND, so clockwise lowers the bias. Its local model has an illustrative 3.8 × 3.0 mm body and approximately 1.6 mm height; use the manufacturer's drawing for physical fit.

## RF connectors

**J61 SMA:** `SMA_Adafruit_1865_EdgeMount` follows the public-domain Adafruit Eagle land pattern, reused through the [GPIO/Zero amplifier assets](../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md). It provides a front signal pad and ground lands on both faces of a 1.6 mm board, with no paste apertures. The [Adafruit 1865 drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) governs actual connector dimensions. Its local illustrative VRML model is original repository-MIT work.

## Hand-fit controls and models

The Alps switch footprint adapts the former KiCad 10.0.6 APEM geometry, retaining its CC BY-SA 4.0 / KiCad-exception attribution. Two 1.30 mm finished holes at 6.50 mm pitch match the Alps nominal pattern (manufacturer recommends 1.25 mm holes). Its new local VRML is an original MIT nominal preview, not manufacturer CAD. The LED footprint derives from KiCad `LED_THT:LED_D3.0mm`, with enlarged plated holes/pads, corresponding courtyard and cleared silkscreen. Its local `LED_D3.0mm.step` is a generic KiCad illustration, not an exact Kingbright solid. The LED STEP retains CC BY-SA 4.0 with the KiCad library exception. The existing local LED and SW_Push electrical graphics already match the two-pin circuits; their default purchasing data, footprint assignments and schematic caches now select these TH parts and exclude factory BOM/position output. No signal or pin-number change was made. Superseded SMT LED/button footprints and the old switch preview/generator were removed.

## Corrected socket and C64 assets, 2026-10-20

The local and placed Pico socket courtyard outlines now reserve **52.00 × 3.04 mm per row**: the selected 51.30 ±0.20 mm body length and 2.54 mm nominal width, plus 0.25 mm per side. The [ZHOURI drawing](https://datasheet.lcsc.com/datasheet/pdf/d644f3ae7335586a805c6e9751c61823.pdf?productCode=C5224030) governs body height, leads and hole recommendation. Row centers, pad positions, antenna notch and keepout are unchanged. Courtyard allowance does not replace a supplier tolerance stack or a mated-Pico sample.

C64 and C66–C69 use the already active local KiCad **C_1206_3216Metric** footprint. The unused C_2220_5750Metric footprint/STEP and old APEM STEP were removed. TP61/TP62 retain imported KiCad **TestPoint_Pad_D1.0mm**, excluded from BOM/positions; no top factory component is added.

The [orientation and polarity audit](VALIDATION.md#assembly-orientation-and-polarity-audit) checked all 14 active footprint types. Existing U31, Q61, RV61, T61 and D11 orientation features are retained. The current socket revision removes the USB arrow/text, printed 1/40 labels and old pin-1 silkscreen box. Pin 1 stays square and pads 2–40 become round, keeping land size, hole diameter, numbering, locations, mask margins and connectivity. The test-point update exposes its existing instance value on silkscreen. Courtyards and models are unchanged.
