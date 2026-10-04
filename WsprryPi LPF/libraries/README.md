# Project libraries

This folder contains the project's symbol library, footprint library, and available 3D models. Library tables use `${KIPRJMOD}` paths; no sibling project folder is required. Open the project with KiCad 10.0.1 or newer to edit the local library assets.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/WsprryPi%20LPF.kicad_sym) | 5 symbols, including all definitions used by the schematic |
| Footprints | [Footprint library](footprints/WsprryPi%20LPF.pretty/) | 3 footprints, including all footprints used by the board |
| Models | [3D models](3dmodels/) | 3 local STEP files |

The registered library nickname is `WsprryPi LPF`. Instance values and purchasing fields remain the design's responsibility; a generic library symbol does not select a component value or supplier part.

The local `PWR_FLAG` symbol documents the externally supplied ground connection at the input header ground connection.

## Used asset inventory

Only assets referenced by the current schematic or PCB are retained. The local symbols are `C`, `GND`, `L`, `PWR_FLAG`, and `LPF_HeaderPair_2x1x04_P2.54mm_S33.02mm`. The three local footprints are `C_Disc_D3.0mm_W1.6mm_P2.50mm`, `L_Axial_Horiz_Torroid_Vert_12mm_D5mm_P10.2mm`, and `LPF_HeaderPair_2x1x04_P2.54mm_S33.02mm`.

The three retained STEP models represent the disc capacitor, generic axial inductor, and single four-pin header (instanced twice by the paired header). Every model path is rooted at `${KIPRJMOD}/libraries/3dmodels/`. The library symbol definitions are taken from the current schematic's embedded definitions, including its updated J1 pin names.

The unused `Conn_01x04` and `SMA_Adafruit_1865` symbols and the standalone header, SMA, and two optional capacitor footprints were removed. The unavailable optional capacitor model reference was removed with its unused footprint. No used model is missing; the generic inductor model limitation below remains.

## Paired LPF headers

`WsprryPi LPF:LPF_HeaderPair_2x1x04_P2.54mm_S33.02mm` is the placed combined symbol and footprint for two hand-fitted male 1×4 headers. Header centerlines are 33.02 mm (1.300 inches) apart; each header has 2.54 mm pin pitch, 1.7 mm pads, and 1.0 mm holes. The footprint origin is input-header pin 1; output-header pin 5 is at X = 33.02 mm. Both rows run in the same direction. Separate courtyards cover the two header bodies and leave the intervening filter area available.

| Header | Pad numbers in row order | Intended connections |
| --- | --- | --- |
| Input | 1, 2, 3, 4 | GND, RF_IN, RF_IN, GND |
| Output | 5, 6, 7, 8 | GND, RF_OUT, RF_OUT, GND |

The symbol exposes all eight passive pins separately; connect the paired RF pins and ground pins explicitly when placing it. It assigns the combined footprint and defaults to exclusion from the BOM. The footprint reuses the existing local header geometry and STEP model twice. These are two physical headers represented as one KiCad component, not a selected eight-pin purchasing part.

The spacing targets the QRP Labs LPF mechanical interface, independently corroborated by the QRP Labs-compatible T41 filter daughter-board [Gerbers](https://github.com/DRWJSCHMIDT/T41/blob/main/T41_V011_Files/Gerbers/T41_Filter_Daughter_V011_Gerber.zip) and [assembly manual](https://www.4sqrp.com/kits/T41/T41-Builders-Manual.pdf). The WsprryPi pinout is retained and is **not electrically interchangeable with the QRP Labs LPF**. Physical fit has not been checked with an assembled QRP Labs module.

The combined header is now placed as J1 on the PCB underside (B.Cu). Flipping it about the midpoint of the pin rows preserves all eight hole locations and their nets because each row has a symmetric GND–RF–RF–GND assignment. Pad-number order reverses spatially on the underside; use the pad numbers rather than apparent top-view order. KiCad 10.0.6 DRC before and after the flip reported zero violations and zero unconnected items. These checks do not establish assembled fit or RF performance.

## Cleanup validation

On 2026-10-03, KiCad 10.0.6 loaded all three retained footprints and exported all five retained symbols. DRC with an in-memory zone refill and schematic parity reported zero violations, zero unconnected items, and zero parity issues. ERC reported only two explicitly excluded four-way-junction warnings, with no active violations. All referenced STEP files exist locally. Hash checks confirmed that the PCB, schematic, and project configuration were unchanged by cleanup. These checks do not qualify assembled fit or RF performance.

## Model limits

The toroidal-inductor footprint uses a generic axial-inductor model. That model is not a mechanical representation of the actual wound toroid; check dimensions against the assembled component.

See the [project README](../README.md) for assembly requirements and ERC/DRC findings.

## Sources and licenses

Standard symbols, footprints, and STEP models derive from KiCad libraries. Local footprints include project-specific geometry. Part names and descriptions identify their original library families. Copyright KiCad Library Contributors; [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/) applies to those assets.

The repository MIT license does not replace third-party license terms.
