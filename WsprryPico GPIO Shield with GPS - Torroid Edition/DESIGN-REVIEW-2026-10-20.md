# Torroid Edition saved-design review, 2026-10-20

**Historical review:** mounting-material selections and support height in this record are superseded by the [2026-10-21 low-support review](MECHANICAL-REVIEW-2026-10-21.md). Refer to current validation for saved-source identities and checks.

**Historical review, superseded by the implemented socket/bypass/C64 revision recorded in [current validation](VALIDATION.md).** The socket envelope, C61 spacing and local U31 bypass changes were implemented. The later availability revision selects Alps SW11, a 10 kΩ trimmer and five parallel 100 nF C0G capacitors. The observations below refer to the historical source identities. Physical mating and RF qualification remain open.

**Original recommendation: correct the Pico socket envelope/C61 spacing and improve U31 bypass routing before ordering.** The new through-hole controls have appropriate pin maps, pitches and holes. No schematic connectivity error, PCB short, open connection or parity difference was found. Physical mating and RF qualification remain open.

This is a review of the saved through-hole-control revision, on repository branch `main`, using **KiCad 10.0.6 outside the sandbox**. The schematic, PCB, project settings, rules, libraries, models, workbook and CSV were left unchanged. The original GPIO/GPS project was outside this review's editing scope. Findings below distinguish proposed improvements from observed failures; none of the proposed design changes has been applied.

## Findings requiring attention

### 1. Correct U11's socket envelope and provide assembly margin at C61

The selected **ZHOURI PM2.54-1*20** socket drawing specifies **2.54 mm width**, **51.30 +/-0.20 mm length** and **8.50 +/-0.20 mm height**. The local U11 socket courtyard outlines are only **1.83 mm wide and 50.08 mm long**, before the 0.05 mm drawing stroke. Thus the clean courtyard DRC does not test the actual purchased socket envelope. [Manufacturer drawing](https://datasheet.lcsc.com/datasheet/pdf/d644f3ae7335586a805c6e9751c61823.pdf?productCode=C5224030)

The row centerlines are Y = **80.97 and 98.75 mm**. Centering the nominal 2.54 mm socket bodies on those rows puts their inner edges at **82.24 and 97.48 mm**. C61 is centered at Y = **83.20 mm**: its nominal 1.60 mm body leaves **0.16 mm**, and its 1.80 mm maximum width leaves **0.06 mm**, before socket-width, component-placement and soldering allowances. Its copper pads begin at Y = **82.30 mm**, also only 0.06 mm from the nominal plastic envelope. The Walsin approval sheet identifies 1206/100 nF/50 V NP0 as thickness variant G, with width **1.60 +/-0.20 mm**. [Walsin drawing, pages 3 and 6](https://datasheet.lcsc.com/datasheet/pdf/d292b592987b2b556ebeda25b5137751.pdf?productCode=C170182)

This establishes inadequate tolerance margin, rather than a proven nominal body collision. Update the local and placed socket courtyards from the real part, including assembly allowance; move C61 sufficiently inward and recheck RV61, R64, C63 and R11 against those corrected boundaries. Preserve the accepted short GP2 input connection while resolving the mechanical constraint. The socket's nominal body span is approximately X = **121.15-172.45 mm** if centered on the pin row; the existing courtyard underestimates both ends as well.

The socket drawing recommends **1.02 mm holes**; U11 has **1.00 mm finished holes**. Its nominal 0.65 x 0.40 mm lead diagonal is about 0.763 mm, giving 0.237 mm nominal diametral allowance. This looks plausible, but is not a tolerance-qualified substitute for the drawing. Confirm the supplier's lead tolerances and fabricator's finished-hole tolerance.

### 2. Improve the local load-switch bypass connections

Measured pad-center copper paths are approximately:

| Connection | Routed length | Discrete vias |
| --- | ---: | ---: |
| U31 VIN to C31 supply pad | 5.97 mm | 0 |
| U31 VOUT to C33 supply pad | 6.47 mm | 2 |
| U31 VOUT to R64 input | 38.06 mm | 3, plus a layer transition through TP61's plated hole |

C33 is physically nearby but is electrically reached through a front-layer excursion. Place/orient C31 and C33 so their supply connections are short and direct on B.Cu, with close ground returns, then simplify the switched-rail route to R64. This follows [TI's layout guidance, sections 11.1-11.3](https://www.ti.com/lit/ds/symlink/tps22918.pdf). The observation is excessive connection inductance and routing complexity; no oscillation or malfunction has been measured.

The long 0.40 mm switched-rail route is not principally a copper-heating problem at 200 mA. At an assumed 35 micrometre copper thickness and 20 C, 38.06 mm contributes about **47 milliohms**, or **9.4 mV at 200 mA**, excluding barrels, pads and contacts. Actual fabrication copper and temperature must be used for final limits.

### 3. Define the complete Pico mating and lead-trim arrangement

The purchased female sockets are identified, but a specific upward-mating male header, engagement depth and completed board separation are not defined. The existing 3D view contains sockets, without the mated Pico and exact male headers. It cannot prove populated-board clearance.

For a Pico below the shield with components facing it, use the actual separation **G** between the shield's underside and the Pico's facing PCB surface. At every overlapping location require:

`G > shield-side protrusion + Pico component height + mechanical allowance`.

An 8.5 mm socket body suggests ample vertical space when correctly mated; with a 2.54 mm male spacer the nominal separation would be about **11.04 mm**. That is a conditional estimate, not a selected header specification or verified engagement. Confirm orientation, minimum insertion, bottoming, header/body tolerance, USB plug access, Pico BOOTSEL/SWD access and the RF can with actual parts. The official Pico is **51 x 21 x 1 mm**, with 17.78 mm row spacing. [Pico 2 W mechanical specification](https://pip-assets.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w/documents/RP-008304-DS-2-pico-2-w-datasheet.pdf)

For the prototype, adopt and inspect a proposed **1.5 mm maximum finished projection below the shield, including solder**, for D11, SW11, Q61 and transformer terminal wires, subject to the assembler's joint criteria. Do not bend tails flat. SW11's 3.5 mm nominal terminal length leaves about **1.9 mm** below a 1.6 mm PCB before trimming; D11's long supplied leads must be cut. T61 already reserves 1.5 mm beneath the board for flat tie returns. Keep tie heads above the board. Solder the crowded control joints before fitting the tall sockets; SW11 pad 1 is only **0.135 mm** from the nominal socket plastic edge in plan view.

RV61 remains an underside SMT part as requested. Its adjustment face points toward the Pico; specify an extender/servicing fixture and check warm bias before final mating. No in-place screwdriver access has been demonstrated.

### 4. Consider compacting the output capacitor bank in the next layout pass

Five parallel 100 nF C0G capacitors provide **500 nF**, with ideal reactance **2.346 ohms at 135.7 kHz**. All five see the full DC-blocking voltage; paralleling does not multiply voltage rating. Their use is a practical component/package choice, rather than a circuit requirement for five separate capacitors.

The present T61 pin 4 to capacitor input paths range from **9.36 mm at C69 to 19.16 mm at C64**. The 0.85 mm buses therefore form a distributed network at HF, rather than an ideal single lumped capacitor. This is not proof of unacceptable loss, but compacting the bank would reduce parasitic uncertainty and free routing space.

A concrete single-part candidate is **KEMET C2220C474J5GACTU**, **470 nF, +/-5%, 50 V C0G**, with **5.7 +/-0.4 x 5.0 +/-0.4 mm** body and **1.70 +/-0.15 mm** height. Its ideal reactance is 2.50 ohms at 135.7 kHz. This manufacturer-listed alternative needs a placement, assembly-availability, RF-current and impedance check before selection; it has not been substituted. [KEMET specification](https://search.kemet.com/component-documentation/download/specsheet/C2220C474J5GACTU)

## New through-hole parts

| Check | Result |
| --- | --- |
| SW11 selection | APEM MJTP1243, two-pin SPST normally open; 6 x 3.5 mm nominal body, 4.3 mm actuator |
| SW11 footprint | Two 1.30 mm holes at 6.50 mm pitch, 2.25 mm lands; matches manufacturer PCB layout |
| SW11 connectivity | GP0/BUTTON to GND; no duplicated internally common pin ambiguity |
| D11 selection | Kingbright WP710A10LID, low-current red 3 mm LED |
| D11 footprint | 2.54 mm pitch, 1.30 mm holes, 2.20 mm lands; pad 1 cathode, pad 2 anode |
| D11 hole margin | Maximum specified lead diagonal about 1.061 mm; 0.239 mm nominal diametral allowance, 0.189 mm at a 1.25 mm finished hole |
| LED drive | 1 kohm R11 retained; about 1.6 mA using typical 1.7 V forward voltage at 3.3 V; brightness needs observation |
| Factory assembly | Both F.Cu, TH and excluded from automated BOM and position output |

[APEM drawings, pages 6 and 8](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6535/MJTPSERIES16NOV2021.pdf); [Kingbright drawing and assembly precautions](https://www.kingbrightusa.com/images/catalog/spec/wp710a10lid.pdf).

D11's maximum 3.45 mm flange is centered at approximately **(162.10, 94.27) mm**. It clears the antenna notch at X = 164.46 mm by about **0.635 mm**. SW11's nominal body ends at X = **163.95 mm**, leaving **0.51 mm**. Both are beside the cutout and clear T61's front courtyard. LED and button courtyard gaps to T61 are approximately **0.14 and 0.45 mm** respectively. These are plan-view checks, not finger-access qualifications beside the 28 mm transformer.

Keep the LED out of SMT reflow. Use an appropriate supported stand-off if needed; form any bends before insertion and retain the maker's lens-to-bend allowance. The generic LED model does not represent exact Kingbright lead geometry. APEM provides a maximum contact rating, but no demonstrated minimum reliable load for this internal-pull-up application; exercise the button at actual GPIO current with debounce during the sample build.

Q61 retains the 1.00 mm finished holes and 1.70 mm pitch. The BS170's maximum lead diagonal is approximately 0.764 mm, leaving 0.236 mm nominal diametral margin. Straight leads require 0.43 mm outward forming of each outer lead. The stock TO-92 preview omits that forming. [onsemi BS170 drawing](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)

## RF, grounding and shielding

The saved circuit agrees with the intended topology: GP2 through C61 and R61 to the gate; adjustable switched-supply bias through R62; grounded source; T61 pins 2/3 joined at the drain; pin 1 bypassed to ground through C62/C63; pin 4 through the capacitor bank to SMA. Check actual winding continuity and series-aiding phasing before power.

| Measured connection | Length | Comment |
| --- | ---: | --- |
| Pico GP2 pad to C61 | 2.59 mm | Direct bottom route |
| R61 gate-side pad to Q61 gate | 4.77 mm | One signal via; retain damping at the gate end |
| Q61 drain to T61 pin 2 | 9.61 mm | 0.85 mm front copper, no via |
| Q61 drain to T61 pin 3 | 12.15 mm | Includes the 2.54 mm terminal link |
| T61 feed pin to C62 | 1.67 mm | Useful short local RF bypass connection |
| T61 feed pin to C63 | 4.83 mm | Bulk bypass farther away |
| C64 output pad to SMA signal pad | 5.71 mm | One signal via and a 0.35 mm neck |

Lengths are approximate pad-center planar routed distances, including connections across pads and excluding vertical barrel length. They are not field-solver electrical lengths. The bias connection to R63 is about 11.76 mm with two vias; it is a branch of the gate net rather than the main driven RF path.

The ground planes are joined by **61 GND vias**. The front fill is one connected polygon; the bottom fill has eight separate polygons, all with at least one plated ground connection to the front. Two small bottom areas have only one connection each. Connectivity is adequate in CAD; it does not imply equal RF impedance everywhere. C62 and Q61 source have nearby GND stitches approximately **1.04 and 1.06 mm** away; Q61's source is itself plated through. The SMA signal-transition via has a nearest GND via **1.66 mm** away; the main gate-transition via's nearest GND via is **2.46 mm** away. Preserve these returns during any reroute and improve local return proximity where practical without cutting the plane.

There is no evidence demanding a shield can or wholesale additional stitching. Preserve the continuous front return, short drain/source loop and separate input/output routing. The retained 0.15 mm drain-to-front-pour rule is a clearance setting, not a characterized controlled impedance. The SMA neck, transition, bifilar leads and final stackup require RF testing.

The actual footprint-embedded antenna keepout and board notch are **9 x 14 mm**, spanning X = **164.46-173.46 mm**, Y = **82.86-96.86 mm**. The earlier approximate 12.22 mm notch-width description is incorrect. The current region matches the official 14 x 9 mm requirement after rotation and DRC finds no infringement. Nearby parts, ferrite, wiring and any enclosure can still affect Wi-Fi: compare with the final mated assembly. Do not introduce a shield or metal loop through T61's window.

## Power and operating limits

U31's six pin functions and the default-off R31, C32 slew capacitor and R32 discharge connection agree with the manufacturer's circuit. A 1 nF CT gives a typical turn-on ramp on the order of milliseconds; validate rail/bias settling before starting RF. Discharging roughly 11 microfarads through 1 kohm is an approximately 11 ms RC process before other paths and component effects. Stop RF before disabling the rail. The 2 A switch rating is not a current limit for Q61 or a USB current budget. [TI datasheet](https://www.ti.com/lit/ds/symlink/tps22918.pdf)

R64 dissipates **40 mW at 200 mA**, **90 mW at 300 mA**, and drops 0.20/0.30 V respectively. Its 250 mW rating has reasonable margin at the 200 mA screening condition, subject to derating. Those currents are not approved continuous BS170 operating points. At 5 V and 200 mA, input power is 1 W before losses; measure delivered RF power and transistor dissipation. The BS170's quoted 150 C/W thermal resistance makes even 0.5 W dissipation a nominal 75 C rise under the specified test assumptions. Check actual long-transmission temperature and ambient margin. [onsemi thermal limits](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)

C63's required **4.7 microfarads effective at 5 V** remains unverified. Check input current, USB cable droop, Wi-Fi load steps, switched-rail ripple, RF-off/warm bias and startup/shutdown on the assembly. Begin with current-limited power and the documented 3.5 mA RF-off bias procedure. C61's 11.73 ohm ideal reactance at 135.7 kHz is small relative to the gate's bias-network resistance, but drive amplitude and gate waveform still need measurement.

## Transformer and release qualification

The 26 x 15 mm T61 courtyard, four 1 mm wire holes, four 3.6 x 1.6 mm NPTH tie slots and the two underside strap regions fit within the saved 53.33 x 22.85 mm outline. No component or via occupies the defined underside strap regions. Masked tracks cross them; retention and abrasion still require a sample assembly. The 28 mm height includes an engineering envelope, not a guaranteed production winding.

The selected **5977000621 material-77 core, 15+15 AWG26 turns** remains a prototype starting point. Manufacturer AL is measured at zero bias, 10 kHz; it does not qualify the full band range. Fair-Rite's general material description and frequency-dependent complex-permeability data reinforce the need for measurement rather than extrapolating the nominal 285.75 microhenries to 10 m. [Core specification](https://fair-rite.com/product/toroids-5977000621/); [material data](https://www.fair-rite.com/wp-content/uploads/2015/04/77-Material-Fair-Rite.csv).

Measure the feed-winding inductance/impedance at 0/50/100/200/300 mA, with the initial target at least 100 microhenries at 200 mA. The 300 mA point is only a screening condition. Sweep loss and matching with appropriate 12.5/50 ohm termination, then test the amplifier with the final winding, band LPF and 50 ohm load for power, efficiency, harmonics, ringing, stability and heat on every intended band. Include Wi-Fi enabled/disabled comparisons. No measured results are implied by this review.

## Checks and records

- Native KiCad **10.0.6 DRC**, all severities, all track errors, zone refill and schematic parity: **0 violations, 0 opens, 0 parity differences**.
- Native ERC, all severities: **0 errors, 3 existing isolated-pin-label warnings**, GPS_RX/GPS_TX/GPS_PPS. The saved circuit has no onboard GNSS. Existing ignored checks remain footprint_filter, four_way_junction, simulation_model_issue and single_global_label; none was changed.
- **21 assembly positions, all bottom**; manual controls absent. All manual footprints retain factory BOM/position exclusions.
- **31 non-power schematic references, 29 footprints, 30 CSV entries excluding U11, 31 workbook references**. Manufacturer, MPN, supplier code and physical footprint fields reconcile; J11/J12 remain purchasing-only socket descriptions.
- All assigned 3D paths resolve. Local libraries contain no superseded SMT control definitions. Illustrative models and the undersized socket courtyard remain the mechanical limitations described above.
- Saved schematic, native copper plots and both 3D sides were visually inspected. Full Pico assembly and manufactured hardware were unavailable.
- T61's inventory MPN buys the core only: the hand-assembly kit also needs the defined wire, two ties and cut foam support. No order was placed and stock was not reserved.

Fresh diagnostic evidence is under ignored `generated/review-2026-10-20/`: ERC/DRC JSON, schematic PDF, copper plots, 3D images, geometry/route measurements, assembly export, audit and source-preservation manifest. The results do not replace fabricator review, a tolerance stack or RF testing.

| Reviewed source | SHA-256 |
| --- | --- |
| Schematic | `525717be48a7c8d0d9854daa8ae40f35092f353ac1966c11de3ce1f0d768c2d0` |
| PCB | `d7f9522af962a561666f669c2876184039fb9cbbcd7d24595476b723a8580dba` |
| Project settings | `74aa899ef2d48517a47ea3f3c92c212237d2d832c23e4a974708bc0a3c0bb8cf` |
| Custom rules | `31cf30504736a1dab394ca73ff13c8c4575e2c55b485f6fd1219cab8a9ad4818` |
| PARTS.csv | `582396184dccf345f1e8495ad737fba5ae3e11f2203daf2aab89795bdc39e74b` |
| Workbook | `d5772ca7386d803683b9e87f0aafc99da8fb075f19e25e674a71bb4386a2051b` |

Only this review and the validation cross-reference were authored. No design fix, commit or push was performed.
