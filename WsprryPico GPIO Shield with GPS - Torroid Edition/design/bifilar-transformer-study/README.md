# Bifilar transformer investigation

This study belongs to **WsprryPico GPIO Shield with GPS - Torroid Edition**, copied from the original GPIO/GPS project on **2026-10-20**. The original project's schematic, PCB, libraries and parts records remain preserved.

The target is **135.7 kHz through 29.7 MHz (2200 m through 10 m)**. The [three-page electrical study](output/pdf/bifilar-transformer-study.pdf) contains phasing, circuit changes, calculations and proposed acceptance measurements. The circuit and parts records are implemented in the saved schematic; **the PCB is now placed and routed with T61, all SMT on the underside**.

## Within-outline core revision

The complete transformer assembly must stay within the **53.33 × 22.85 mm board outline**, with no overhang. The former 36.8 mm coated-core mounting proposal has been superseded by **Fair-Rite 5977000621**, coated material 77, with **15 bifilar AWG26 turns per wire**. The [mounting definition and drawing](../t61-mount/README.md) specify a lengthwise upright assembly, 25 × 13.5 mm courtyard and 30 mm height, with a 1.25 mm illustrative insulating pad and 0.5 mm bedding allowance. Support and attachment are builder-selected. Separate ends 1/4 are on the +Y face, with common 2/3 on the opposite -Y face; lead dressing preserves the series-aiding connection. Its envelope fits the board rectangle; actual populated-board fit remains unverified.

| Candidate | Turns / wire | Nominal / AL-minimum primary inductance | Role |
| --- | ---: | ---: | --- |
| **5977000621**, coated 77; 21.85 mm OD max | **15** | **285.75 / 200.025 µH** | Selected within-outline prototype |
| 5943000621, coated 43; same exterior | 24 | 270.72 / 203.040 µH | HF comparison |
| 5977004921, coated 77; 16.9 mm OD max | 14 | 274.40 / 192.080 µH | Smaller, higher DC magnetic stress |
| 5977002721, coated 77; 36.8 mm OD max | 11 | 272.25 / 190.575 µH | Historical large-core comparison; mounting superseded |

The selected core specifies **AL = 1270 nH/turn², +25/−30%**, tested at 10 kHz. Effective area/path are **24.3 mm² / 52 mm**; exterior limits are **21.85 mm OD maximum, 12.40 mm ID minimum and 7.10 mm axial thickness maximum**. [Fair-Rite specification](https://fair-rite.com/product/toroids-5977000621/)

Use two identified AWG26 enamelled copper wires, initially about **0.65 m each**, twisted uniformly about 8–10 twists/inch. Wind 15 passages through the window in one layer over approximately 330°, leaving the lower 30° bare for the support; route paired ends closely along the axial faces. Each passage is one turn in each wire. Use about 0.90 m per wire for the 24-turn same-size 43 comparison. Inspect coating and verify continuity and series-aiding phase before drain power.

The smaller selected core has calculated Hdc **0.725 Oe at 200 mA**, versus 0.311 Oe for the former large core. Linear Bdc estimates are approximately **157 versus 63.5 mT**. These are screening calculations, not nonlinear saturation or loss models. The reduced magnetic area and thermal volume increase the need for DC-biased measurements; shrinking the package does not preserve a previously measured full-band result, since neither core has been qualified here.

The explicit 50% retention scenario gives **100.0125 µH / 85.27 Ω at 135.7 kHz**. That scenario is an assumption, not a guaranteed DC-biased value. Measure the actual winding at 0/50/100/200/300 mA; the initial gate remains at least 100 µH at 200 mA. 300 mA is a core screening point, not an approved continuous BS170 current.

The supply-to-drain and drain-to-output windings are series aiding, giving **1:2 voltage / 1:4 impedance**; a 50 Ω fundamental load reflects about 12.5 Ω at the drain. Material-only calculations exclude winding capacitance, leakage and DC-dependent RF properties. Correctly matched RF measurements remain required through 29.7 MHz.

## Implemented circuit

- T61 pin 1 is A start/dot, connected to bypassed `AMP_XFMR_FEED`; pin 2 A finish joins pin 3 B start/dot at `AMP_DRAIN` in one shared 1.2 mm finished plated hole; pin 4 B finish feeds `AMP_RF_XFMR`. The separate 1/4 holes are on +Y and the shared 2/3 hole is on -Y.
- **R64**, Yageo RC1206FR-071RL / C137355, is **1 Ω ±1%, 0.25 W**, in the drain-feed branch. RV61 remains upstream. TP61 is upstream and TP62 downstream of R64. With RF off, 1 mV means 1 mA; begin near **3.5 mV / 3.5 mA**, then qualify bias and temperature. The old voltage-across-L61 procedure does not apply.
- **C62 100 nF** and **C63 10 µF X7R, 25 V, 1206**, Samsung CL31B106KAHNNNE / C14860, bypass the feed. Require at least **4.7 µF effective at 5 V**, including relevant tolerances; verification remains open.
- **C64 and C66–C69** are five parallel **Walsin 1206N104J500CT / C170182**, 100 nF C0G, 50 V, 1206 each. The 500 nF bank connects `AMP_RF_XFMR` to `TX_OUT` before J61; ideal LF reactance is 2.346 Ω at 135.7 kHz.
- Q61, RF input/gate damping, RV61 and U31 retain their circuit roles. The latest user-saved design removes the GNSS circuit. Preserve AMP_EN/RF sequencing. The saved PCB now connects TP61/TP62 across R64 for the revised bias procedure.

The original local **Bifilar_Autotransformer_1to4** symbol retains four independent terminals and start dots. Its defaults, placed instance, footprint, workbook and CSV now select the same 15-turn core prototype. T61 is manually assembled and excluded from automated SMT BOM/positions. The former overhanging footprint/model were removed from the active local library. The unused TDK L61 and removed GNSS library assets have been deleted.

## Procurement and reproducibility

On **2026-10-20**, the [DigiKey selected-core page](https://www.digikey.com/en/products/detail/fair-rite-products-corp/5977000621/15930531) listed **125 in stock at $2.17 each**. This is a purchasing snapshot, not a stock guarantee. The ordering code buys one core; wire is a separate purchase, while support and attachment materials are chosen by the builder in the [mounting record](../t61-mount/README.md#mounting-materials).

The smaller [5977004921](https://fair-rite.com/product/toroids-5977004921/), same-size [5943000621](https://fair-rite.com/product/toroids-5943000621/) and [73 binocular](https://fair-rite.com/product/multi-aperture-cores-2873000202/) comparison are documented in the mounting review. The binocular manufacturer controls HF impedance, rather than a guaranteed LF AL/DC-bias curve; sample characterization is needed before assigning a winding count. No binocular substitution is selected.

[calculate.py](calculate.py) uses retained manufacturer [material 43](inputs/fair-rite-43.csv) and [material 77](inputs/fair-rite-77.csv) inputs. Run it with Python 3 to regenerate [calculations.json](calculations.json), then [render.py](render.py) with ReportLab to rebuild the PDF. Each candidate uses its own effective area/path for DC and flux calculations. The JSON records exact part identity in each material-only sweep and current schematic/PCB hashes.

The study is not a circuit simulation or measured RF model. Verify DC-biased inductance/impedance, correctly matched transformer loss, amplifier output/harmonics, ringing, heating and Pico/Wi-Fi coexistence before freezing the winding. See [project validation](../../VALIDATION.md) for the saved-source checks and remaining physical/RF acceptance.
