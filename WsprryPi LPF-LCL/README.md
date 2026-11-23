# WsprryPi LPF-LCL

An independent, hand-assembled **five-element L–C–L–C–L low-pass filter**, using a common PCB populated for the selected WSPR/QRSS band. Three coils use the original combined axial-inductor/upright-toroid footprint. Each of the two shunt positions provides two parallel capacitor footprints.

**Status: routed development design, revision 0.1.0; physical assembly and RF performance unverified.** KiCad 10.0.6 ERC, DRC, saved zone refill, and schematic-parity checks pass with no violations or unconnected items. See [validation](VALIDATION.md).

Open [WsprryPi LPF-LCL.kicad_pro](WsprryPi%20LPF-LCL.kicad_pro). All six symbol definitions, four footprint types, and three STEP models and one illustrative SMA VRML model are in independent [project-local libraries](libraries/README.md), using `${KIPRJMOD}` paths. No sibling project is required to open this design or reproduce its numerical models.

## Circuit and band population

```text
RF_IN ── L1 ──┬── L3 ──┬── L5 ── RF_OUT
              │        │
           CA2 || CB2  CA4 || CB4
              │        │
             GND      GND
```

L1 and L5 use the selected row's `L1_L5_H` target; L3 uses `L3_H`. The installed total at **each** shunt position is `C2_C4_F`: `CA2 + CB2 = CA4 + CB4`. `L_END`, `L_MID`, `C_A`, and `C_B` in KiCad are population placeholders, not fixed part values. Select one row from the [minimum-loss component table](model/minimum-loss-values.csv), then record actual parts and measured coils for that assembly. This is one PCB for different band builds, not one fixed population covering every band.

The five-element, 1 dB-ripple Chebyshev response is scaled so its highest-frequency transmission maximum lies at the midpoint of the listed WSPR/QRSS windows. In the ideal real-50 Ω model, the carrier has essentially zero mismatch attenuation, with approximately **42.77 dB attenuation at 2f** and **62.35 dB at 3f**. Coil losses, tolerances, self-resonance, coupling, and PCB parasitics are additional effects; these are not measured results. There is no DC-blocking capacitor.

The [minimum-loss WSPR/QRSS study](model/MINIMUM-LOSS.md) covers frequencies, values, rounding, harmonic tradeoffs, and coil-Q sensitivity. All previous five-element studies, scripts, plots, and numerical results have moved here under [model/](model/README.md), with a local snapshot of the original C-first workbook. The original seven-element comparison is retained for context. Blank QRSS entries for 2200 m and 2 m remain blank. Paired labels such as `30 & 40m` are inherited build identifiers; they do not establish a minimum or adequate harmonic rejection on both bands.

For the 20 m build centered at **14.097000 MHz**, targets are **L1 = L5 = 1.146155 µH**, **L3 = 1.611108 µH**, and **234.3134 pF per shunt position**. A candidate pair is 160 pF + 75 pF per position. These are calculated targets, not purchasing selections or manufacturing tolerances.

## Preserved mechanical interface

Both independent LPF projects now use Adafruit 1865 SMA launches. This project retains the original outline, stackup, headers, and RF axes; the new connector origins are on the board-edge datums:

| Item | Preserved arrangement |
| --- | --- |
| Outline | 45.96 mm long, approximately 12.873 mm high; identical rounded corners and Edge.Cuts primitives |
| Thickness | 1.60 mm saved stackup |
| J1 | Two underside male 1×4 headers as one paired component; 33.02 mm centerline spacing, 2.54 mm pin pitch |
| Input header | Pads 1/4 = GND; 2/3 = RF_IN |
| Output header | Pads 5/8 = GND; 6/7 = RF_OUT |
| J2 input SMA | Adafruit 1865; edge datum (114.00, 99.12) mm, −90° |
| J3 output SMA | Adafruit 1865; edge datum (159.96, 99.12) mm, +90° |

Header geometry, holes, layer, and position match the original. SMA footprints, pad geometry, origins, rotations, and models are now specific to Adafruit 1865. The GND–RF–RF–GND header pinout is **not directly electrically compatible with unmodified QRP Labs LPFs**. Interpret underside contacts by KiCad pad number, not apparent top-view order. A symmetrically populated filter can operate in either direction in a matching WsprryPi socket.

The [Adafruit 1865](https://www.adafruit.com/product/1865) is for 1.6 mm PCBs, matching the saved 1.60 mm stackup. Its independent local footprint has 4.014 mm-long hand-solder lands, a 0.05 mm copper setback, a top RF contact, and ground fingers on both copper faces. There are no paste apertures. A project-local `.kicad_dru` rule permits **0 mm edge clearance only for J2/J3 pads**; all other copper retains the **0.50 mm global requirement**. The physical setback keeps copper clear of the drawn Edge.Cuts stroke. Rule control tests and detailed geometry are in [validation](VALIDATION.md).

The Adafruit footprint derives from its public-domain Eagle `SMA_EDGELAUNCH` package. The local `SMA_Adafruit_1865_Preview.wrl` is illustrative, not supplier CAD. Verify slot tolerance, top/bottom solder access, near-edge copper acceptance by the board fabricator, enclosure clearance, and actual fit. SMA bodies project beyond the board ends; controlled-impedance and RF performance remain unqualified.

## Capacitor mounting

Each of `CA2/CB2` and `CA4/CB4` retains the original strategy:

- For an `A + B` pair, fit one capacitor into each 2.50 mm-pitch footprint. Their sum is the shunt value.
- For one 2.50 mm-pitch capacitor, use pads 1 and 2 of either footprint, leaving the other available for tuning.
- For one 5.00 mm-pitch capacitor, span **CA pad 1 to CB pad 2**, or **CB pad 1 to CA pad 2**. Both combinations measure 5.00 mm. The two signal pads or the two ground pads must not be used as the capacitor terminals.

A spanning capacitor normally occupies both body areas. Check actual body dimensions, lead diameter, neighboring windings, and board edges. Select RF-suitable capacitors and voltage ratings for the intended power; no all-band capacitor family or power rating is qualified.

## Inductor mounting and layout

L1/L3/L5 retain the local `L_Axial_Horiz_Torroid_Vert_12mm_D5mm_P10.2mm` footprint. Its 0.8 mm holes provide two alternatives for each electrical terminal. Fit one winding end to any **pad 1** and the other to any **pad 2**. Same-number holes are connected mounting alternatives. The footprint supports the original axial or upright wound-component strategy, subject to actual lead/body fit.

The generic axial-inductor STEP model does not represent a wound toroid. Select core, turns, wire, measured inductance including leads, Q, self-resonance, power handling, and finished dimensions for each band. Original C-first turn counts do not apply: 2200 m targets reach approximately **117.5 µH at the ends and 165.2 µH at the center**, with physical fit unproven. At 2 m, characterize the assembled RF response rather than relying on low-frequency inductance measurements.

Filter anchors use a **0.25 mm placement grid**, retaining intrinsic pad geometry. J1/J2/J3 are deliberate grid exceptions preserving the mechanical interface. Schematic origins and connections use **1.27 mm / 50 mil**. The PCB retains ground pours on both copper faces, the two capacitor-pair pour keepouts, and stitching. Outer RF paths were rerouted without obsolete end-capacitor branches; small anchor-grid adjustments have repaired copper.

## Assembly and validation

All parts are hand fitted. As inherited, headers, inductors, and capacitors are excluded from default BOM/position outputs; SMAs are included. A default BOM is not a complete purchasing list. No manufacturing package or qualified power rating is supplied.

[VALIDATION.md](VALIDATION.md) records source identity, checks, corrected findings, and remaining work. [scripts/check_project.py](scripts/check_project.py) verifies the mechanical contract, local assets, grids, capacitor spans, and exported netlist topology. Disposable exports belong under ignored `generated/`; final records are under [validation/](validation/).

Repository-owned work follows the [MIT license](../LICENSE.md). KiCad-derived assets retain their [third-party attribution and library license](libraries/README.md#sources-and-licenses).
