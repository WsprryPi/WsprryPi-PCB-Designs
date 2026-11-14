# Torroid Edition validation - review after saved marking edits, 2026-10-21

## Current saved-source check — 2026-11-13

KiCad **10.0.6** was used for ERC and DRC with all severities, all track errors, and schematic parity enabled for DRC. ERC reports **0 findings**. Saved-board DRC reports **9 findings (6 errors and 3 warnings), 12 unconnected items, and 0 schematic-parity differences**. A second read-only run with in-memory zone refill reports **4 findings (1 courtyard-overlap error and 3 dangling-track warnings), 12 unconnected items, and 0 parity differences**. The saved board was not refilled or modified. These results supersede the historical clean-board claims below. Routing, the C32/U31 courtyard overlap, and unconnected items remain unresolved. Existing ignored categories and design rules were retained without changes. Schematic PDF and board-layer exports were visually reviewed. Electrical, physical, and RF qualification remain open.

Reports and renders are retained locally in ignored `generated/commit-all-review/`. SHA-256 of the checked source files:

- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_sch`: `4760fa04bf06ee00f2fa5a5e8b79bbc4cd3d2c181798e3e7bc564a992b2a9547`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb`: `1d5e3bedc6dac98eaaae2106a7b22cb0fa4203badbaf4cf3a7bbcd504a8a6eb4`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pro`: `b691d3ccdcd9c5ec0bf0c95e0d252ce9f25f2f8f83589eaf0f250dcbae014585`

## Historical validation record

**KiCad 10.0.6 full DRC: 0 violations, 0 opens and 0 schematic/PCB differences. ERC: 0 reported violations with four existing ignored categories.** All 29 placements and 14 local footprint types were reviewed for assembly polarity, pin 1 and orientation. The Pico header now uses one square pin-1 pad and 39 round pads. Hole diameters, component positions and 3D geometry are unchanged, so earlier component and support clearance checks remain applicable. Actual mounting, winding and RF performance remain unqualified.

## Review after saved marking edits, 2026-10-21

**No new schematic, polarity, routing or modeled-clearance fault found.** This review uses the latest saved PCB, including the builder's moved T61 labels, hidden reference/title fields, removed probe Fab text and relocated **BIAS mV** caption at **(133.00, 79.40) mm**. It does not restore earlier marking positions. Native comparison against the preceding square-pin-1 revision confirms all **217 track and 70 via UUIDs/geometry**, all **29 component placements**, **105 pad geometries/nets**, and model assignments/transforms are unchanged. Native formatting and some field UUIDs changed during the user's save; these are retained.

### Polarity and orientation

All placed pad definitions match their corresponding **14 project-local footprint types**, with correct front/back transformation. The saved schematic netlist agrees with the PCB, including KiCad's escaped slash spelling on two explicitly unconnected ADC pins.

- **U11:** pin 1 is the only square Pico pad; 2–40 are round. The 1.508 mm lands, 1.00 mm circular drills and 0.254 mm nominal annulus remain. No USB arrow/text or printed 1/40 labels have returned.
- **D11:** square pad 1 is cathode/GND; round pad 2 is anode/LED_A. The visible top **+** is beside pad 2 at (159.60, 95.94) mm. The body outline and polarity agree with the [Kingbright drawing](https://www.kingbrightusa.com/images/catalog/SPEC/WP710A10LID.pdf). Long stock LED leads must be trimmed before mating the Pico.
- **Q61:** flat-body outline and square drain pad agree with the selected [onsemi BS170](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf): drain, gate, source. The footprint still requires the documented outer-lead forming.
- **U31:** the bottom pin-1 triangle identifies VIN, with pins 2–6 GND/ON/CT/QOD/VOUT matching the [TI pinout](https://www.ti.com/lit/ds/symlink/tps22918.pdf). RV61's asymmetric footprint and pin-1 bracket remain; pin 3 is the clockwise/grounded end per [Bourns](https://www.bourns.com/docs/product-datasheets/tc33.pdf), so clockwise reduces bias.
- **TP61/TP62:** visible **+ / −** and the moved BIAS mV caption still identify the drop across R64. TP62 is **AMP_XFMR_FEED, not GND**.
- **T61:** labels identify separate 1/4 holes on one face and the shared 2/3 hole on the other. Dotted starts remain 1 and 3. Pads 2/3 both connect to AMP_DRAIN. Model tails align inside the three physical drills, with two deliberately offset tails in the common hole. Verify the labels and winding ends before fitting; the coil can obscure nearby ink after assembly.
- SW11 is a nonpolar contact. Ceramic capacitors and resistors require no polarity marks; J61's center RF pad and surrounding ground lands remain distinct.

### Fresh mechanical screen

Rebuilt the temporary fitted-Pico fixture from this saved PCB and reran OpenCascade clearances. The official **Pico W STEP** remains a board/header-envelope reference for Pico 2 W; it does not establish exact Pico 2 W component geometry, mating engagement or manufacturing tolerance. Production files contain no fixture or absolute model paths.

| Check | 11.00 mm nominal gap | 10.65 mm housing-minimum gap | 8.30 mm conservative gap |
| --- | ---: | ---: | ---: |
| Output bank, C61 and C63, screened maximum bodies plus solder stand-off | 9.10 mm | 8.75 mm | **6.40 mm** |
| C62 body plus solder stand-off | 9.95 mm | 9.60 mm | **7.25 mm** |
| T61/Q61/SW11/D11 joints, ≤1.5 mm finished underside projection | 9.50 mm | 9.15 mm | **6.80 mm** |

**Untrimmed D11 leads intersect the Pico reference.** The favorable distances above require the documented trimmed-joint envelopes; this is an assembly condition, not an untrimmed-lead pass. RV61 still needs adjustment access before mating or through a suitable fixture.

The smaller support remains **8 mm diameter × 1.25 mm high**, with **4 × 6 × 0.5 mm** bedding. Fresh conservative wire-radius clearances are **0.788 mm to the pad** and **1.141 mm to bedding**. Model plan is **23.308 × 11.024 mm**, height **24.315 mm**, inside the retained envelope and outline. Full model-box distances to Q61/D11/SW11 are **1.83/1.80/2.05 mm**; to socket housings **2.05/2.17 mm**. Winding paths retain 15 passages per wire and free leads add no window passages. Mounting materials, compression and retention remain builder fit checks.

SW11/D11 land-to-socket-body margins remain **0.735/0.440 mm nominal**. C62 maximum-body clearance to the T61 pin-1 land remains about **0.35 mm**. Control real solder spread and check actual socket/lead tolerance. The model is illustrative; generic LED/TO-92 solids do not qualify the actual manufacturer's leads.

![Current fitted assembly](generated/post-marking-review-20261021/fitted-isometric.png)

### RF, power and ground review

| Path | Fresh planar copper length | Discrete vias |
| --- | ---: | ---: |
| Pico GP2 → C61 | 3.445 mm | 0 |
| R61 → Q61 gate | 4.319 mm | 0 |
| Q61 drain → T61 shared 2/3 | 10.727 mm | 0 |
| T61 output → C69 input | 6.739 mm | 0 |
| Each T61 → output-capacitor → SMA branch | **19.942 mm** | **1 shared output transition** |
| U31 VIN → C31 | **2.694 mm** | **0** |
| U31 VOUT → C33 | **2.000 mm** | **0** |
| T61 feed → C62 / C63 | 2.275 / 5.736 mm | 0 / 0 |
| Pico VBUS → C31 | 41.323 mm | 2 |
| U31 VOUT → R64 | 37.586 mm | 2 |
| R64 → C62 / C63 | 27.293 / 23.533 mm | 2 / 2 |

The five output capacitors retain consistent 90° orientation and short **1.00 mm common buses**. They connect **AMP_RF_XFMR to TX_OUT; neither side is ground**. Each branch has the same geometric total because the buses are fed from opposite ends. The 0.85 mm drain route and 22 Ω series gate damping are intact; no new RF stub or branch via appears. Equal geometry does not establish equal current or precise 50 Ω impedance; stackup, device/core behavior and parasitics still require measurement. The retained quiet-control crossover under the drain reference is unchanged.

There are **51 GND stitches** and 19 signal/power vias. Fresh refill produces **five front and five bottom GND regions**, each connected through a plated GND pad or via. The small 0.634 mm² bottom region beside SW11 connects through pad 2's copper annulus; a pad-center-only test misses that contact. C62/C63 ground pads remain about **0.925 mm** from their nearest ground stitch; Q61 source **1.060 mm**, C65 **0.562 mm**. The antenna notch/keepout is preserved and no new copper/part entry is reported.

U31's default-off pull-down, CT capacitor and QOD resistor agree with the schematic and TI circuit. C31/C33 bypasses remain direct on B.Cu. The longer upstream power trunks retain their local reservoir/bypass arrangement. R64 remains 1 Ω/0.25 W: 40 mW at 200 mA and 90 mW at 300 mA are calculation screens, not qualified operating currents. Confirm supply droop/ripple, startup/shutdown, warmed idle current and device temperatures on a build. **C63's ≥4.7 µF effective-at-5-V requirement remains unverified.**

The output bank remains 500 nF C0G, 2.346 Ω ideal reactance at 135.7 kHz; C61 remains 100 nF. Actual transformer impedance with drain DC, phase, LF/HF response, 10 m performance, matching, stability, harmonics and temperature are still open prototype measurements with an external band-appropriate LPF and 50 Ω load. No measured full-band or production qualification is claimed.

### Checks and source preservation

**KiCad 10.0.6 outside the sandbox:** full DRC, all severities/all track errors, zone refill and schematic parity: **0 violations, 0 opens, 0 parity differences**. ERC: **0 reported violations**, retaining the same four ignored categories: single_global_label, four_way_junction, simulation_model_issue and footprint_filter. No rule, threshold or exclusion changed. All 21 factory SMT positions remain B.Cu. Native board top/bottom, copper/silkscreen views, fitted assembly/profile, complete schematic PDF and manufacturer package drawings were visually inspected.

An additional native footprint-inspection helper crashed outside the sandbox. Its mutating temporary-footprint calls were replaced with a read-only coordinate comparison, which completed for all 29 placements/14 types. The full DRC/ERC and native renders completed successfully. A pad-center-only ground test and a hole-center-only common-tail test were replaced with checks of actual plated-annulus contact and the two offset wire envelopes, respectively; these initial assumptions and their resolutions remain documented here.

Only **VALIDATION.md** and the calculation record's **PCB source hash** change in this review. PCB, schematic, local footprints/symbols/models, project/rule/library files, mounting drawings, workbook and CSV remain byte-identical to the review's starting saved files. The user's open KiCad session and recovery files were not operated on. No commit or push was made. Detailed checks, geometry, source hashes, route measurements, model distances and renders are in ignored `generated/post-marking-review-20261021/`.

## Implemented change

The local native model now shows an **8 mm diameter × 1.25 mm insulating pad**, reduced from 11 mm diameter. The **1.25 mm height stays unchanged**. The illustrative bedding plan reduces from 4 × 7.1 to **4 × 6 mm**, retaining its **0.5 mm height**. Bare core bottom/top remain **1.75 / 23.60 mm** above the PCB, and modeled top stays **24.315 mm**. The retained acceptance envelope is **≤24 × 11.4 mm in plan, ≤30 mm high** and **≤1.5 mm finished underside lead/solder projection**.

**Support and attachment materials remain builder-selected.** The workbook is byte-identical: it already specifies the illustrative height without a diameter. Only CSV cell D34 changes its illustrative diameter from 11 to 8 mm. No required manufacturer, MPN, supplier, pack quantity or cost is added. Core, winding wire and electronic selections are unchanged.

The preceding narrower-pad revision changed the **T61 F.Fab support-circle radius from 5.5 to 4 mm**. Subsequent marking changes are recorded below. The schematic, symbol library, project settings, rules and library tables are byte-identical. At the end of that narrower-pad revision, native/source comparison confirmed all electrical content, UUIDs, component placements, pads, copper, vias, zones, outline, socket rows, SMA and antenna geometry were unchanged. The later header pad-shape change is recorded below. There are still 29 footprints, 105 logical pads, 217 segments, 70 vias and **21 factory SMT positions, all on B.Cu**. The original GPIO/GPS project and all other source files are preserved.

The winding and free-lead paths are identical to the preceding low-support revision. The corrected Y export convention still aligns separate ends **1/4 to the +Y holes and 2/3 to the one -Y hole**. Each winding retains 15 window passages with zero extra free-tail passages. Twists and actual winding tolerances remain unmodeled.

## F.Fab text cleanup

Following the narrower-pad revision, all **six T61 F.Fab user annotations** are removed from the library footprint and placed PCB copy. The required value field is hidden while retaining its data. The silkscreen reference and terminal IDs retain their existing visibility. Fabrication rectangles, support circle, courtyard, pads, models, winding/lead paths and all copper are unchanged. The maintained generator reproduces the cleaned footprint while preserving surviving UUIDs.

KiCad **10.0.6** full DRC remains **0 violations / 0 opens / 0 schematic-parity differences**. ERC reports **0 violations**, retaining the same four ignored categories. Native footprint and board-layer exports were visually checked. Fresh checks, source comparison and the file inventory are in ignored `generated/fab-text-cleanup-validation/`. Parts records, mounting PDF and 3D model remain byte-identical to the start of this cleanup.

## LED polarity marking

The saved LED reference is **D11**. A **+** is added on F.SilkS beside anode pad 2 in its project-local library footprint and placed PCB copy. It sits at local (2.54, 2.50) mm, or board (159.60, 95.94) mm at the retained -90° placement. The existing square pad 1 remains cathode/GND; round pad 2 remains anode `/LED_A`. The 0.8 mm mark uses a 0.12 mm stroke and stays outside the nominal LED body. Pad shapes, drills, nets, placement, copper, courtyard and models are unchanged.

KiCad **10.0.6** full DRC reports **0 violations / 0 opens / 0 schematic-parity differences**. ERC reports **0 violations**, with the same four ignored categories retained. Native library and board silkscreen exports were visually checked. Fresh results and source-preservation evidence are in ignored `generated/led-polarity-validation/`. The schematic, workbook, CSV, T61 footprint/model/drawings and all other source files remain unchanged.

## Assembly orientation and polarity audit

Reviewed **all 29 placements and all 14 active project-local footprint types** against the saved schematic fields and PCB pad numbers, functions and nets. That initial audit added or exposed silkscreen only. The subsequent Pico marker simplification below supersedes its header legends and changes header pad shapes. Pin numbering, land sizes, drills, nets, placements, routed copper, zones, keepouts, board outline, models, courtyards, rules and assembly exclusions remain unchanged.

| Placement(s) | Polarity / orientation evidence | Result |
| --- | --- | --- |
| U11 Pico interface | Pin 1 = GP0/BUTTON; pin 40 = VBUS; USB end opposite antenna opening | Current marker: **pin 1 square, pads 2–40 round**. Prior 1/40 text, USB text/arrows and pin-1 silkscreen box removed from library and PCB. |
| TP61 / TP62 | Across R64: pin 1 AMP_5V_SW / pin 2 AMP_XFMR_FEED | Exposed **+ / −** instance values on F.SilkS and added **BIAS mV**. **TP62 is not GND**. |
| U31 TPS22918 | Pin 1 VIN; existing bottom filled triangle identifies that corner | Clear, retained unchanged. |
| Q61 BS170 | 1 drain, 2 gate, 3 source; flat body outline and square pad 1 | Clear, retained unchanged. |
| RV61 trimmer | Offset pin-1 corner bracket; asymmetric three-pad pattern | Clear, retained unchanged; 1 feed end, 2 wiper, 3 GND end. |
| T61 transformer | Square pad 1 and explicit 1 / 2/3 / 4 terminal labels | Clear, retained unchanged; winding starts and series-aiding connection remain in the schematic and mounting drawing. No F.Fab text reintroduced. |
| D11 LED | Square cathode pad 1, round anode pad 2 and top + | Previous polarity fix retained and checked. |
| J61 SMA | Unique center signal pad 1; four outer ground lands numbered 2; board-edge mounting | Mechanically unambiguous, retained unchanged. |
| SW11 button | Nonpolar two-terminal contact; distinct square pad 1 and body outline | No polarity symbol needed; retained unchanged. |
| C31–C33, C61–C69 (12 capacitors) | Selected X7R or C0G/NP0 ceramic parts | Nonpolar; no +/− or mandatory assembly pin-1 mark needed. |
| R11, R31/R32, R61–R64 (7 resistors) | Two-terminal thick-film resistors | Nonpolar; no mandatory assembly pin-1 mark needed. |

All new text is **0.8 mm high with 0.12 mm stroke**, meeting the existing rule. Probe values are printed left of TP61 and right of TP62; the shared local footprint uses a short, neutral **TP** default caption below its pad, while the PCB instances show their schematic +/− values at the documented left/right positions. The former USB legends and arrows have since been removed from both faces; the local header and placed PCB now use pad shape for pin 1.

Native **KiCad 10.0.6** full DRC: **0 violations / 0 opens / 0 schematic-parity differences**. ERC: **0 reported**, with the same four existing ignored categories. All **21 factory SMT positions stay underneath**. Native top, mirrored-bottom and affected-footprint exports were visually inspected. The first 0.7 mm text trial produced seven text-height warnings; those were corrected to 0.8 mm and the initial report is retained. No thresholds or exclusions were relaxed.

The initial marking audit checks, native element comparisons, before/after silkscreen views, initial/final DRC and source inventory remain in ignored `generated/orientation-marking-validation/`. The current simplification checks are in `generated/square-pin1-validation/`. Schematic, workbook, CSV, all electronics selections, 3D models and mounting drawings remain byte-identical to the beginning of this audit. Physical component fit and RF qualification remain open as previously recorded.

## Pico pin-1 pad marker

Removed the Pico **1**, **40**, **USB** legends and USB arrow from both silkscreen faces, the original USB text on Dwgs.User, and the old small pin-1 silkscreen box. This applies to both the placed U11 footprint and its project-local library definition. T61 terminal labels and all other assembly markings remain intact.

All 40 Pico pads were previously square. **Pin 1 stays square; pads 2–40 are now round**, so shape identifies pin 1 without text. The 1.508 mm pad dimension, circular 1.00 mm drill, 0.102 mm local mask margin, numbering, nets, positions and surviving UUIDs are retained. Round pads retain a 0.254 mm nominal annulus. Tracks, vias, stored zones, all other footprints, board outline, 3D models, mounting drawings, schematic, workbook and CSV are byte-identical to this revision's starting files. All 21 factory SMT positions remain underneath.

Native **KiCad 10.0.6** full saved-board DRC with zone refill, all severities, all track errors and schematic parity reports **0 violations / 0 opens / 0 parity differences**. ERC reports **0 violations**, retaining the four existing ignored categories. Native top, mirrored-bottom and copper/silkscreen footprint exports were visually inspected. No thresholds or exclusions were changed. Checks and preservation evidence are in ignored `generated/square-pin1-validation/`.

## Clearance recheck

| Check | Current result and limit |
| --- | --- |
| Three physical T61 holes | 1: (151.75,95.10), 1.0 mm; 2/3: (141.15,85.20), one 1.2 mm; 4: (141.75,95.10), 1.0 mm |
| Native model plan / height | About 23.308 × 11.024 mm / 24.315 mm, within retained acceptance envelope |
| Fitted Pico to ≤1.5 mm finished joints | 9.50 mm nominal; 9.15 mm housing-minimum; 6.80 mm conservative screen |
| Maximum output-cap/C61/C63 bodies to Pico | 9.10 / 8.75 / 6.40 mm in the same three scenarios |
| C62 maximum body to Pico | 9.95 / 9.60 / 7.25 mm |
| Entire T61 model box to Q61 / D11 / SW11 references | Conservative 1.83 / 1.80 / 2.05 mm separations |
| Entire T61 model box to socket housings | About 2.05 / 2.17 mm using nominal housing envelopes |
| 8 mm support to nearest land | About 1.873 mm; increased from 0.373 mm |
| Lowest winding capsule envelope to board | About 1.26 mm in nominal illustration |
| Winding / free-lead capsule envelope to pad | **0.788 / 0.788 mm** nominal clearance |
| Winding / free-lead capsule envelope to bedding | **1.141 / 1.155 mm** nominal clearance |
| Bedding corners inside pad edge | **0.394 mm** |

These are conservative nominal wire-radius clearances, independently checked with OpenCascade solid-to-polyline distances and segment minimization in the maintained generator (agreement within 0.000001 mm). Actual winding, twist build, coating tolerances, compression and bedding spread remain builder fit checks. The 1.25/0.50 mm stack is illustrative, not a prescribed or qualified minimum mounting height. Adjust actual support shape, bedding and lead dressing to avoid pinching enamel or contacting copper. Inspect support compression, independent retention and the real winding before soldering. No physical assembly pass is inferred.

The fitted reference uses the official Pico W STEP inverted with its bare back toward the shield, as a Pico 2 W board/header-envelope reference. It is not exact Pico 2 W component geometry or qualified connector engagement. Gap scenarios are 11.00, 10.65 and 8.30 mm. The unchanged C62-to-pin-1-land gap remains about 0.35 mm; control actual solder spread. Untrimmed LED leads still intersect the Pico reference. See the [current mechanical review](MECHANICAL-REVIEW-2026-10-21.md) for assumptions, images and conservative envelope definitions.

![Native fitted assembly with narrower support](generated/narrow-pad-validation/fitted-isometric.png)

## Saved-source checks

| Check | Result |
| --- | --- |
| Native tools | **KiCad 10.0.6**, outside the sandbox |
| Full DRC | **0 violations / 0 opens / 0 parity differences**, all severities, all track errors, zone refill and schematic parity |
| ERC | **0 reported**; existing ignored single_global_label, four_way_junction, simulation_model_issue and footprint_filter categories retained |
| Electrical preservation | Current simplification: only U11 header ink and shapes of pads 2–40 differ from its starting PCB; all pad sizes, drills, nets, positions, mask margins, routed copper, stored zones, models, surviving UUIDs and other footprint data compare exactly |
| SMT assembly | 21 factory positions, all bottom; manual parts and copper-only test pads excluded |
| T61 drills | Three physical holes for four logical ends; no extra common drill |
| Model geometry | Correct Y export convention; numerical tails align to drilled holes; 15 passages per wire and zero extra dressing passages |
| Mechanical | Updated native 3D, fitted Pico and OpenCascade pad/bedding/component/joint envelopes checked; real mounting fit remains open |
| Records | Workbook, CSV and electronic selections byte-identical for this marking audit |
| Drawings | Four current mounting PDF pages rendered and visually inspected; plan and lower-support elevation agree |
| Documentation | Local Markdown paths/anchors and changed-source whitespace checked; active diameter notes synchronized; previous review records retained |

No rule, threshold or exclusion was relaxed. Earlier routing DRC evidence remains in `generated/opposite-face-validation/`; previous terminal-coupon views remain in `generated/low-support-validation/`; current checks, fresh clearance results, source-change inventory and fitted fixtures are in ignored `generated/narrow-pad-validation/`. Production source contains no fitted-Pico dummy or temporary absolute model path.

## RF and power baseline, unchanged by this revision

The table below retains the previously documented routing comparison. Both columns predate the support and marking revisions; current tracks and vias match the corrected column. The U11 header pads now use the shape convention described above.

The RF input, gate, drain, transformer output and TX_OUT segment UUIDs, endpoints, widths and layers are identical to this correction's starting board. The five Walsin 100 nF C0G output capacitors retain one underside row and the two 1.00 mm straight common buses. Total 500 nF; neither side is GND. The one existing shared SMA via remains the only output transition; no RF branch vias or stubs are added.

| Connection | Starting PCB | Corrected PCB, planar length / vias |
| --- | ---: | ---: |
| Pico VBUS pad 40 → C31 | 36.985 mm / 0 | 41.323 mm / 2 |
| U31 VIN → C31 | 2.694 mm / 0 | 2.694 mm / 0 |
| U31 VOUT → C33 | 2.000 mm / 0 | 2.000 mm / 0 |
| U31 VOUT → R64 | 37.586 mm / 2 | 37.586 mm / 2 |
| R64 → C62 | 14.786 mm / 0 | 27.293 mm / 2 |
| R64 → C63 | 19.199 mm / 0 | 23.533 mm / 2 |
| T61 feed → C62 | 1.475 mm / 0 | 2.275 mm / 0 |
| T61 feed → C63 | 2.938 mm / 0 | 5.736 mm / 0 |
| Pico GP2 → C61 | 3.445 mm / 0 | 3.445 mm / 0 |
| R61 → Q61 gate | 4.319 mm / 0 | 4.319 mm / 0 |
| Q61 drain → shared 2/3 | 10.727 mm / 0 | 10.727 mm / 0 |
| T61 output → C69 input | 6.739 mm / 0 | 6.739 mm / 0 |
| Each complete bank branch, T61 → cap → SMA | 19.942 mm / 1 | 19.942 mm / 1 |

Lengths exclude component body and vertical barrel length. Shared bus lengths are shared copper; geometric equality does not establish equal RF current or controlled impedance. The added power transitions are upstream of the local transformer bypasses or U31 input reservoir. T61's local C62/C63 connections have no discrete vias. Direct U31 bypass routing remains intact. The longer DC feed and two added supply transitions require ripple, droop, startup/shutdown and warm-bias checks on a build.

Both C62/C63 ground pads are approximately **0.925 mm** from their nearest ground stitch; C65 remains 0.562 mm and Q61 source 1.060 mm. All **five front / five bottom** fill regions attach to GND pads/vias, including the small region touching SW11 pad 2's annulus. Front GND beneath the capacitor bank remains; drain return reference still has the existing quiet-control crossover and pad clearances. No isolated fill, clearance violation or open is reported. No shield can or conductive retaining loop is added; the antenna opening stays clear.

R64 remains 1 Ω / 0.25 W: calculated 40 mW at 200 mA and 90 mW at 300 mA; these are screening currents, not qualified continuous BS170 operating points. C63 must retain ≥4.7 µF effective at 5 V. The 500 nF output bank has 2.346 Ω ideal reactance at 135.7 kHz. Real impedance, loss, ringing, stability, harmonics, temperature, USB supply behavior and Pico/Wi-Fi coexistence remain hardware checks.

## Remaining physical and RF work

Check actual wire-pair/finished-hole fit, phase, winding build, low turns and free tails, builder-selected support/attachment, retention, solder spread, formed BS170 leads, Pico/socket engagement, RV61 access and enclosure height. Keep sound hand joints within the ≤1.5 mm underside projection target. The low support is illustrative and does not qualify a material, tolerance stack or bond.

Measure primary inductance/impedance under the documented DC-bias points and verify the complete amplifier with the external LPF and 50-ohm load from 135.7 kHz through 29.7 MHz. RF output, matching, harmonics, stability, USB behavior, temperature and coexistence remain hardware checks.

## Current source identities

| Saved asset | SHA-256 |
| --- | --- |
| WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_sch | `4760fa04bf06ee00f2fa5a5e8b79bbc4cd3d2c181798e3e7bc564a992b2a9547` |
| WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb | `2f77987f8b34a6fd12559d4750a183b6da6cf8d9ea665d77bb2597fd290a566e` |
| WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pro | `74aa899ef2d48517a47ea3f3c92c212237d2d832c23e4a974708bc0a3c0bb8cf` |
| WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_dru | `31cf30504736a1dab394ca73ff13c8c4575e2c55b485f6fd1219cab8a9ad4818` |
| PARTS.csv | `6dda807b5eb41050363e933e655471ee71da4a37188f8abb03b4658aab06befa` |
| LCSC-parts-collection.xlsx | `fbf3234ff7b7ecdd38fd070c910d0758b1fbfdc6d15789fbc22bcf4f643286b2` |
| wsprrypico-gpio-shield-with-gps-torroid-edition.kicad_sym | `91e93ac8d67e65092448ebd16789dc4bf4ab3e7b1f6f6d42317ce7cc108fb868` |
| wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/T61_FairRite_5977000621_Upright_Bumper_4Pin.kicad_mod | `c5dbb31df1250519c8097fcd33ecf53ce303f231ff5b14a5412153aabe5bd326` |
| wsprrypico-gpio-shield-with-gps-torroid-edition.3dshapes/T61_FairRite_5977000621_Upright_Bumper_4Pin_Preview.wrl | `01df0b86b65c6189bece9199f0371e6f35615860baddc463268710b6ae6852ad` |
| wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod | `81ec4eb6be9f3bb03fe8e1de970a89ef15dcaa7f9db22fd2a55f384da6d1af01` |
| wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/TestPoint_Pad_D1.0mm.kicad_mod | `029d03dbd601d69c9e7b69bc728963d86b91e7c2ebe08387703ad3564e863326` |

## Files changed for the preceding narrower-pad revision

Only the Torroid Edition assets below change. The workbook, schematic, symbol library and all other projects are byte-identical to the start of this revision.

- `CIRCUIT-DESIGN.md`
- `MECHANICAL-REVIEW-2026-10-21.md`
- `PARTS.csv`
- `PARTS.md`
- `README.md`
- `VALIDATION.md`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb`
- `design/bifilar-transformer-study/calculations.json`
- `design/t61-mount/README.md`
- `design/t61-mount/dimensions.json`
- `design/t61-mount/generate_mount.py`
- `design/t61-mount/output/pdf/t61-mounting.pdf`
- `wsprrypico-gpio-shield-with-gps-torroid-edition.3dshapes/README.md`
- `wsprrypico-gpio-shield-with-gps-torroid-edition.3dshapes/T61_FairRite_5977000621_Upright_Bumper_4Pin_Preview.wrl`
- `wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/T61_FairRite_5977000621_Upright_Bumper_4Pin.kicad_mod`

## Files changed for F.Fab text cleanup

Only these six Torroid Edition files change in this follow-up:

- `VALIDATION.md`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb`
- `design/bifilar-transformer-study/calculations.json` (PCB source hash only)
- `design/t61-mount/README.md`
- `design/t61-mount/generate_mount.py`
- `wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/T61_FairRite_5977000621_Upright_Bumper_4Pin.kicad_mod`

## Files changed for LED polarity marking

- `README.md`
- `LIBRARY-SOURCES.md`
- `VALIDATION.md`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb`
- `design/bifilar-transformer-study/calculations.json` (PCB source hash only)
- `wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/LED_Kingbright_WP710A10LID_D3.0mm_P2.54mm_D1.3mm.kicad_mod`

## Files changed for the complete marking audit

- `README.md`
- `LIBRARY-SOURCES.md`
- `VALIDATION.md`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb`
- `design/bifilar-transformer-study/calculations.json` (PCB source hash only)
- `wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod`
- `wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/TestPoint_Pad_D1.0mm.kicad_mod`

## Files changed for Pico marker simplification

- `README.md`
- `LIBRARY-SOURCES.md`
- `VALIDATION.md`
- `WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb`
- `design/bifilar-transformer-study/calculations.json` (PCB source hash only)
- `wsprrypico-gpio-shield-with-gps-torroid-edition.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod`
