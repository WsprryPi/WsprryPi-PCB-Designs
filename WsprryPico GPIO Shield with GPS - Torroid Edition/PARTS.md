# WsprryPico GPIO Shield with GPS - Torroid Edition component specifications

These records follow the revised **transformer schematic**. The [study](design/bifilar-transformer-study/README.md) records winding details, calculations and qualification requirements. **The saved schematic, PCB and purchasing records agree; both through-hole controls are hand fitted on top.**

[PARTS.csv](PARTS.csv) contains **33 engineering inventory entries**, including 30 circuit inventory entries and three transformer materials. U11 is the combined Pico interface rather than a separately purchased component; the [workbook](LCSC-parts-collection.xlsx) includes all **31 schematic references plus three purchasing-only transformer material entries**. The saved PCB has **21 SMT positions, all on B.Cu**. The latest user-saved GNSS removal is reflected in the inventory; physical and RF qualification remain open.

## Assembly

Factory SMT includes the amplifier power switch, trimmer and passive components, all on the underside. The two Pico sockets, Q61 BS170, hand-wound T61, J61 SMA, SW11 button and D11 LED are hand fitted. U11, Q61, T61, J61, SW11, D11 and TP61/TP62 are excluded from automated BOM and position output; J11/J12 are schematic-only socket descriptions whose electrical pads belong to U11. Test points are top copper-only probe pads with no drilled holes. T61's [mounting envelope and local footprint](design/t61-mount/README.md) are defined; mounting materials are selected by the builder. Within-outline CAD placement passes; physical fit remains open.

Check the exact ordering code, supplier stock and assembler allocation when ordering. The schematic's supplier fields and this inventory identify selected parts; they do not reserve stock. Preserve these assembly exclusions in every manufacturing export.

The original capacitor/resistor/trimmer catalog review is dated **2026-10-10**. The **2026-10-20** transformer revision uses R64 **Yageo RC1206FR-071RL / C137355** and C63 **Samsung CL31B106KAHNNNE / C14860**. The availability revision restores five parallel **Walsin 1206N104J500CT / C170182** output capacitors, changes SW11 to Alps and selects the stocked 10 kΩ trimmer. These supplier fields agree between schematic, workbook and CSV. The PCB now agrees with these fields and packages. Electrical and RF acceptance remain in [VALIDATION.md](VALIDATION.md).

## Capacitors

| References | Purpose | Value / dielectric | Tolerance / rating | Package | LCSC |
| --- | --- | --- | --- | --- | --- |
| C31, C63 | Switch input reservoir / transformer feed bulk | 10 µF X7R | ±10%, 25 V | 1206 | [C14860](https://www.lcsc.com/product-detail/C14860.html) |
| C32 | TPS22918 slew capacitor | 1 nF C0G | ±5%, 50 V | 0603 | [C106246](https://www.lcsc.com/product-detail/C106246.html) |
| C33 | Switched amplifier rail local bypass | 1 µF X7R | ±10%, 50 V | 0805 | [C726584](https://www.lcsc.com/product-detail/C726584.html) |
| C61 | RF input DC blocking | 100 nF C0G | ±5%, 50 V | 1206 | [C170182](https://www.lcsc.com/product-detail/C170182.html) |
| C64, C66–C69 | Parallel transformer output DC-blocking bank | 5 × 100 nF C0G = 500 nF | ±5% each, 50 V | 1206 | [C170182](https://www.lcsc.com/product-detail/C170182.html) |
| C62 | Drain-feed supply HF bypass | 100 nF X7R | ±10%, 50 V | 0603 | [C235731](https://www.lcsc.com/product-detail/C235731.html) |
| C65 | Bias wiper bypass | 100 nF X7R | ±10%, 50 V | 0603 | [C235731](https://www.lcsc.com/product-detail/C235731.html) |

C63 requires at least **4.7 µF effective at 5 V**, including relevant tolerance, DC-bias, temperature and aging effects; that acceptance remains open. At 135.7 kHz, ideal reactance is **11.73 Ω for C61** and **2.346 Ω for the 500 nF output bank**. Actual loss, matching and RF voltage require measurement over 2200 m–10 m.

## Resistors and bias control

| References | Function | Value | Manufacturer / ordering code | LCSC |
| --- | --- | --- | --- | --- |
| R11 | LED current limiter | 1 kΩ | YAGEO RC0603FR-071KL | [C22548](https://www.lcsc.com/product-detail/C22548.html) |
| R31, R63 | AMP_EN and gate pull-downs | 100 kΩ | UNI-ROYAL 0603WAF1003T5E | [C25803](https://www.lcsc.com/product-detail/C25803.html) |
| R32 | QOD resistor | 1 kΩ | YAGEO RC0603FR-071KL | [C22548](https://www.lcsc.com/product-detail/C22548.html) |
| R62 | Gate-bias feed | 4.7 kΩ | YAGEO RC0603FR-074K7L | [C99782](https://www.lcsc.com/product-detail/C99782.html) |
| R61 | RF gate damping | 22 Ω | UNI-ROYAL 0603WAF220JT5E | [C23345](https://www.lcsc.com/product-detail/C23345.html) |
| R64 | Transformer feed current sense | 1 Ω | YAGEO RC1206FR-071RL | [C137355](https://www.lcsc.com/product-detail/C137355.html) |

The original fixed resistors are 0603 thick-film, ±1%, 100 mW, 75 V, ±100 ppm/°C. **R64 is 1206, ±1%, 250 mW, 200 V, ±200 ppm/°C**. Its 1 Ω value gives nominally 1 mV per 1 mA with RF off; account for resistor and meter error. RV61 is **Bourns TC33X-2-103E / C719176**, 10 kΩ, ±25%, 150 mW, ±250 ppm/°C. Its pin 1 stays upstream of R64 on `AMP_5V_SW`, pin 2 is the wiper and pin 3 GND. **Clockwise reduces bias; counterclockwise increases it**, viewed from the adjustment screw. The [initial bias target](README.md#adjusting-rv61) is **3.5 mV across R64 / 3.5 mA**, applicable after assembling the revised circuit and confirming its nets.

SW11 connects GP0 directly to ground; use the Pico's internal pull-up and software debounce. D11's anode is driven by GP1 through R11; its cathode is grounded.

## Active parts and interfaces

| References | Selected part | LCSC | Assembly |
| --- | --- | --- | --- |
| U31 | TI TPS22918DBVR load switch | [C131941](https://www.lcsc.com/product-detail/C131941.html) | SMT |
| Q61 | onsemi BS170, straight-lead TO-92 | [C111691](https://www.lcsc.com/product-detail/C111691.html) | Manual |
| RV61 | Bourns TC33X-2-103E | [C719176](https://www.lcsc.com/product-detail/C719176.html) | SMT |
| SW11 | Alps Alpine SKHLACA010; 2-pin TH, 6 × 3.5 × 4.3 mm | [LCSC C382056](https://www.lcsc.com/product-detail/C382056.html) | Manual, top |
| D11 | Kingbright WP710A10LID; 3 mm low-current red TH LED | [DigiKey 754-1610-ND](https://www.digikey.com/en/products/detail/kingbright/WP710A10LID/2657763) | Manual, top |
| J11, J12 | ZHOURI PM2.54-1*20 Pico sockets | [C5224030](https://www.lcsc.com/product-detail/C5224030.html) | Manual |
| J61 | Adafruit 1865, SMA edge mount for 1.6 mm PCB | [Supplier](https://www.adafruit.com/product/1865) | Manual |
| TP61, TP62 | 1 mm diameter top copper probe pads, no drilled holes | — | PCB copper |

Q61's local footprint has **1.00 mm finished plated holes**, **1.50 × 1.60 mm pads** and **1.70 mm pitch**. Its 0.25 mm nominal annular ring and 0.20 mm pad clearance are retained. The selected straight-lead BS170 requires 0.43 mm outward forming of each outer lead; see [mechanical dimensions and hole allowance](LIBRARY-SOURCES.md#transistor).

J11/J12 have 20 positions, 2.54 mm pitch and 8.5 mm body height. Their [supplier drawing](https://datasheet.lcsc.com/datasheet/pdf/d644f3ae7335586a805c6e9751c61823.pdf?productCode=C5224030) gives nominal 0.65 × 0.40 mm leads and a 1.02 mm recommended hole; U11 uses 1.00 mm drills. Verify finished-hole clearance, socket engagement and Pico clearance using actual parts. J61's [drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) governs the selected edge connector; local 3D previews are illustrative.

## Transformer selection and winding

**T61 replaces L61 in both schematic and PCB.** Purchase one **Fair-Rite 5977000621 coated material 77 core** and supply two identified AWG26 enamelled copper wires, initially about **0.65 m each**. The manufacturer's MPN denotes the core, not a finished transformer. [Fair-Rite specifications](https://fair-rite.com/product/toroids-5977000621/)

Twist the pair about 8–10 twists per inch and pass it through the core **15 times** in one layer. Mark starts and finishes. Pin 1 is A start/dot on `AMP_XFMR_FEED`; pin 2 is A finish and pin 3 B start/dot, joined on `AMP_DRAIN`; pin 4 is B finish on `AMP_RF_XFMR`. Check continuity and series-aiding phasing with low-level RF before applying drain power.

With AL **1270 nH/turn², +25/−30%**, 15 turns gives a calculated **285.75 µH nominal / 200.025 µH AL-minimum** primary. That minimum exceeds the original uncoated 10-turn candidate's 180 µH. This is a winding starting point, not a guarantee under DC bias or across HF. Core exterior limits are **21.85 mm maximum OD, 12.40 mm minimum ID, 7.10 mm maximum height**. The [mounting definition](design/t61-mount/README.md) shows an illustrative 8 mm diameter × 1.25 mm insulating pad and 0.5 mm bedding allowance. Actual support and attachment are builder-selected; no catalog bumper or adhesive is required. The four-terminal footprint reserves **25 × 13.5 mm courtyard, 30 mm above-board and ≤1.5 mm finished-joint projection below**. Three side-positioned PTH holes serve four winding ends: 1/4 use separate 1.0 mm holes on one axial face, and 2/3 share one 1.2 mm drain hole on the opposite face. There are no tie slots; leads run along the core faces. The complete assembly must stay within the board outline; the proposed envelope needs no overhang, CAD placement passes while physical fit remains unverified.

L61 and the removed GNSS parts are absent from the active purchasing records and local libraries. T61 is hand assembled and excluded from automated SMT BOM/positions. Final acceptance requires DC-biased transformer measurements and the actual amplifier, LPF and load.

The 2026-10-20 within-outline revision supersedes the large-core mount. The selected 21.85 mm core uses **15 turns per wire**, with higher DC field/flux than the former large core. Purchasing agreement and an outline-sized envelope do not qualify DC-biased inductance, full-band RF loss, heating or populated-board fit. The [mounting comparison](design/t61-mount/README.md#core-comparison-and-selection) records the tradeoff and stock snapshot.

## Through-hole control selection, 2026-10-20

The [Alps SKHL manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/1a3e3d210bb2ea7d5f11862ab84517d8.pdf?productCode=C382056) specifies two 1.25 mm holes at nominal 6.5 mm pitch, a 6 × 3.5 mm body, 4.3 ±0.2 mm actuator height and 3.5 ±0.5 mm terminals. The local footprint uses 1.30 mm finished holes. Its contact limit is 50 mA / 12 VDC and minimum specified load 10 µA at 1 VDC; the manufacturer life is **50,000 cycles at 5 mA / 12 V**, despite LCSC’s erroneous 500,000-cycle field. Use GP0’s internal pull-up and software debounce; confirm operation at actual GPIO current. Untrimmed maximum terminal projection is about 2.4 mm below 1.6 mm PCB.

The [Kingbright WP710A10LID drawing](https://www.kingbrightusa.com/images/catalog/spec/wp710a10lid.pdf) specifies 2.54 mm lead pitch, 1.7 V typical / 2.1 V maximum forward voltage at 2 mA, and a 30 mA absolute maximum. R11 stays 1 kΩ; nominal current is (3.3 − 1.7) / 1000 ≈ 1.6 mA. This is an estimate, not a brightness measurement. DigiKey listed stock at lookup; LCSC C5879080 identifies this exact selection.

The LED drawing permits a 0.75 mm maximum square lead envelope, with a 1.061 mm diagonal. The adapted footprint uses **1.30 mm finished holes and 2.20 mm pads**, providing 0.239 mm nominal diametral margin, 0.45 mm annular ring and 0.34 mm pad-to-pad copper gap. Even a 1.25 mm finished hole leaves about 0.189 mm nominal diametral margin. Confirm fabrication tolerances and part fit; the manufacturer's nominal recommended hole is 0.9 mm. Pin 1 is cathode and pin 2 anode. Fit and trim both controls after SMT reflow, keeping soldered leads clear of the Pico.

## Stocked output capacitor bank, 2026-10-20

C64 and C66–C69 use five **Walsin 1206N104J500CT / C170182**, each 100 nF ±5%, C0G, 50 V. Total 500 nF ±5% worst-case has 2.346 Ω ideal reactance at 135.7 kHz. The [manufacturer sheet](https://datasheet.lcsc.com/datasheet/pdf/d292b592987b2b556ebeda25b5137751.pdf?productCode=C170182) assigns 1206 / 100 nF NP0 thickness G: maximum 3.40 × 1.80 × 1.80 mm. The fitted-Pico check adds 0.10 mm solder stand-off. C61 uses the same SKU. Distributed trace inductance and RF current still need bench verification. The low-stock single 470 nF / 2220 option and its unused local assets have been removed.

The 10 kΩ trimmer replaces the unavailable 5 kΩ version with the same pinout/footprint and adjustment direction. Divider current is nominally 0.5 mA and dissipation 2.5 mW at 5 V; the minimum 7.5 kΩ tolerance limit gives 3.33 mW, below its 150 mW rating. At mid travel, nominal divider Thevenin resistance is 2.5 kΩ before the 104.7 kΩ load, giving about 0.244 ms with nominal C65. At the +25% resistance limit it is 3.125 kΩ before that load: about 0.303 ms, or 1.52 ms for five time constants with nominal C65. Including C65’s +10% tolerance gives about 1.67 ms for five time constants, before temperature and rail-ramp effects. Allow the switched rail and bias to settle before RF. R64 still excludes divider current; the 3.5 mV initial bias procedure is unchanged.

The workbook keeps its native table, styles, panes and C-reference filter; R64 remains last. T61-WIRE remains a separate wire purchase. T61-SUPPORT and T61-ADHESIVE are builder-choice reminders, not required products, circuit references or factory positions. The 2026-10-21 revision updates F21 and B:H on rows 32/34: mounting manufacturer/MPN/source fields are blank and quantities/prices are no longer prescribed. Exactly 15 cell values change. Table A1:I35, native filter, styles, panes, row heights, other cells and all other workbook ZIP members are preserved.

## Availability checked 2026-10-20

Factory SMT parts were checked directly against LCSC listings on 2026-10-20, approximately 15:57–16:10 CDT. Counts are a stock snapshot, not allocated assembler inventory. Manual parts were also checked through normal small-lot suppliers. Supplier web snapshots may precede the lookup; recheck before purchase.

| Factory references | Exact MPN | LCSC | Listed stock |
| --- | --- | --- | ---: |
| C31, C63 | CL31B106KAHNNNE | [C14860](https://www.lcsc.com/product-detail/C14860.html) | 870,480 |
| C32 | CC0603JRNPO9BN102 | [C106246](https://www.lcsc.com/product-detail/C106246.html) | 1,404,450 |
| C33 | AC0805KKX7R9BB105 | [C726584](https://www.lcsc.com/product-detail/C726584.html) | 725,540 |
| C61, C64, C66, C67, C68, C69 | 1206N104J500CT | [C170182](https://www.lcsc.com/product-detail/C170182.html) | 145,055 |
| C62, C65 | FN18X104K500PBG | [C235731](https://www.lcsc.com/product-detail/C235731.html) | 2,830,850 |
| R11, R32 | RC0603FR-071KL | [C22548](https://www.lcsc.com/product-detail/C22548.html) | 10,250,100 |
| R31, R63 | 0603WAF1003T5E | [C25803](https://www.lcsc.com/product-detail/C25803.html) | 10,150,800 |
| R61 | 0603WAF220JT5E | [C23345](https://www.lcsc.com/product-detail/C23345.html) | 3,837,400 |
| R62 | RC0603FR-074K7L | [C99782](https://www.lcsc.com/product-detail/C99782.html) | 8,730,100 |
| R64 | RC1206FR-071RL | [C137355](https://www.lcsc.com/product-detail/C137355.html) | 205,460 |
| RV61 | TC33X-2-103E | [C719176](https://www.lcsc.com/product-detail/C719176.html) | 11,515 |
| U31 | TPS22918DBVR | [C131941](https://www.lcsc.com/product-detail/C131941.html) | 58,875 |

| Hand purchase | Small-lot source checked | Listing returned |
| --- | --- | --- |
| T61 core, Fair-Rite 5977000621 | [DigiKey](https://www.digikey.com/en/products/detail/fair-rite-products-corp/5977000621/15930531) | 125 cores; quantity-one pricing; core only |
| AWG26 wire, Remington 26H200P.125 | [DigiKey Marketplace](https://www.digikey.com/en/products/detail/remington-industries/26H200P-125/11615003) | 31 small 2 oz / 157 ft spools; ships from Remington, approximately 5 days; two initial 0.65 m lengths per transformer |
| SW11 Alps SKHLACA010 | [LCSC C382056](https://www.lcsc.com/product-detail/C382056.html), [Mouser 688-SKHLAC](https://www.mouser.co.uk/en/ProductDetail/Alps-Alpine/SKHLACA010?qs=sGAEpiMZZMsqIr59i2oRcqShR6iETrbs4h9%252BJVqfTmM%3D) | LCSC 915, minimum/multiple 5; Mouser snapshot 365, quantity one |
| D11 Kingbright WP710A10LID | [DigiKey](https://www.digikey.com/en/products/detail/kingbright/WP710A10LID/2657763), [LCSC C5879080](https://www.lcsc.com/product-detail/C5879080.html) | DigiKey 11,473, quantity one; LCSC 380, minimum 5 |
| Q61 onsemi BS170, straight leads | [DigiKey BS170-ND](https://www.digikey.com/en/products/detail/onsemi/BS170/244280), [LCSC C111691](https://www.lcsc.com/product-detail/C111691.html) | DigiKey 70,201; LCSC 11,935; do not silently buy a formed-lead suffix |
| J61 Adafruit 1865 | [Adafruit direct](https://www.adafruit.com/product/1865) | In stock, quantity one; DigiKey lists non-stocked with lead time. Retain the existing exact connector/footprint |
| J11/J12 ZHOURI PM2.54-1*20 | [LCSC C5224030](https://www.lcsc.com/product-detail/C5224030.html) | 205 pieces; two per board. No different-height catalog socket substituted |

**Mounting update, 2026-10-21:** support and attachment materials are now chosen by the builder. The former bumper and adhesive purchasing entries are superseded and no longer have required manufacturer, MPN, supplier, quantity or cost fields. The low pad and bedding are model illustrations; check actual winding clearance, compatibility and retention. No ties, routed slots or prescribed adhesive are added.

Unchanged-component stock above remains the 2026-10-20 snapshot. No new availability check, messages or orders are implied by this mounting change. Remington's [manufacturer specification](https://www.remingtonindustries.com/magnet-wire/magnet-wire-200c-26-awg-polyamideimide-8-spool-sizes/) gives 0.0176 inch nominal heavy-build wire diameter (about 0.447 mm) and MW35-C insulation; verify wire build, stripping and actual winding fit. Procurement does not qualify the transformer.
