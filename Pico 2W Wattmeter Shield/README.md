# Pico 2W QRP Wattmeter Shield

A Raspberry Pi Pico 2 W shield with an ADL5904 RF power detector, an ADS1115 ADC, and a nominal 10 dB input attenuator. Open [Pico 2W Wattmeter Shield.kicad_pro](Pico%202W%20Wattmeter%20Shield.kicad_pro) in KiCad 10. The project uses local symbol, footprint, design-block, and 3D-model libraries with `${KIPRJMOD}` paths.

## Board-side and USB reference update — 2026-10-07

The complete assembly was flipped as requested: factory components, J1 and the Pico interface are now on B.Cu. The two decorative logos also exchanged sides. The entire board was reflected about its horizontal centerline, including components, tracks, vias, zones, outline, markings and antenna clearance. Relative placement, pad numbers/net assignments, routed lengths and widths, UUIDs, locks and assembly exclusions were preserved. The USB label is centered in its Dwgs.User reference box in both the placed interface and the independent local header library. The library footprint remains front-sided; the board instance determines the mounting side.

KiCad **10.0.6**: after refilling copper, **0 DRC violations, 0 unconnected items and 0 schematic-parity findings**. ERC remains **0 errors / 9 existing C1–C9 library-symbol mismatch warnings**; the schematic and project settings are byte-for-byte unchanged. Preservation checks cover 23 footprints, 110 pads, 149 tracks/vias and 57 board zones. A complete inverse-flip comparison reproduced the original board properties apart from KiCad's invalidated fill-cache flag; final saved routing and pin/net geometry were checked again after refill. Native 3D views were inspected. Existing ERC ignored-check categories remain unchanged; no new suppressions or weakened rules were introduced.

The five U1 filled/capped vias explicitly exchanged their asymmetric tenting flags: F side covered, B side solderable. The four exposed-pad stencil apertures are now on B.Paste. Updated manufacturing notes and B-side drawings must accompany regenerated fabrication outputs; earlier output packages predate this flip. Physical/RF qualification remains unchanged.

## Measurement range

| Parameter | Design target |
| --- | --- |
| J1 input | −20 to +20 dBm, approximately 10 µW to 100 mW |
| Attenuation | 9.96 dB calculated with a nominal 50 Ω detector-side termination |
| Frequency | 136 kHz–148 MHz, covering 2200 m through 2 m |
| Source | Unamplified WsprryPi GPIO clock |

The board is an unqualified prototype. Input limits and accuracy require resistor-rating verification, assembly checks, and RF calibration. See [input range](INPUT-RANGE.md) for calculations and measurement conditions.

## Assembly

The factory fits **C1–C9, R1–R8, U1, and U2: 19 components**, all on the back (B.Cu), following the whole-board flip on 2026-10-07. The SMA connector, Pico sockets, and Pico module are fitted by hand. J1, J2, J3, U3, and the decorative logos are excluded from the factory BOM; J1, U3, and the logos are excluded from machine placement.

The **Shield purchasing BOM** preset exports the `LCSC Part #` field. The BOM and placement file must contain the same 19 component references. Use the supplier's required column headers and verify matched parts and IC orientation in its assembly preview. Plugin-generated exports must honor the manual-part exclusions.

U1 requires **selective epoxy-filled, planarized, copper-capped vias**: exactly the five vias inside its exposed ground pad. Their B-side surfaces are solderable; their F-side pads are covered with soldermask. The stencil has four separate paste windows. These requirements must be included in the fabrication order.

- [Fabrication and assembly order notes](manufacturing-notes/ORDER-NOTES.txt)
- [Bottom assembly map](manufacturing-notes/ASSEMBLY-BOTTOM.svg)
- [Selective via-treatment drawing](manufacturing-notes/U1-VIA-TREATMENT.svg)
- [U1 exposed-pad and stencil geometry](U1-PASTE-WINDOWS.md)
- [SMA connector and board-edge fit](J1-CONNECTOR-NOTES.md)
- [Pico sockets and antenna notch](PICO-HEADERS-AND-NOTCH.md)

The drawings identify the source PCB with a SHA-256 hash. Generate Gerbers, drills, BOM, and placement files from the board revision being ordered. The fabricator must confirm the selective via process; the assembler must confirm the stencil process. Socket mating height, connector fit, and RF performance require physical verification.

## Libraries and 3D view

Source libraries are in `pico-wattmeter.pretty/`, `pico-wattmeter.kicad_sym`, `pico-wattmeter.kicad_blocks/`, and `pico-wattmeter.3dshapes/`. See [footprint sources and licenses](pico-wattmeter.pretty/LIBRARY-SOURCES.md) and [U1's package model](pico-wattmeter.3dshapes/README.md).

Select **View > 3D Viewer** in the PCB Editor to inspect the assembly. U1 uses the included CP-16-22 STEP model. Passive and U2 models use the installed KiCad model libraries. J1 and the Pico/header assembly have no attached models.

The optional, unplaced `Raspberry_Pi_Pico_2W_SMD` footprint uses the STEP file in this project's [local Pico asset copy](pico-2w-libs/README.md), through `${KIPRJMOD}/pico-2w-libs/Raspberrypi pico2 W.step`. Its placement transform is unchanged. The supplied model's Pico 2 W geometry and alignment remain unverified; this does not add a model to the placed header footprint. The copied symbol and footprints retain their documented pin/pad and assembly compatibility limits.

Each silkscreen logo is a single unlocked footprint containing both polygons. The front and back logos move independently of their adjacent text.

## Project files

`fabrication-toolkit-options.json` contains export preferences. KiCad sources contain the part identifiers and assembly exclusions. The local JLCPCB plugin database, generated exports, fabrication packages, backups, and editor state are ignored by Git.

The earlier KiCad 10.0.1 validation recorded zero ERC errors or warnings and zero DRC violations, unconnected pads, or footprint errors. Rechecking the unchanged schematic with KiCad 10.0.6 CLI during the local-model-path update reports nine existing `lib_symbol_mismatch` warnings for C1–C9 against the installed `Device:C_Small` symbol; DRC still reports zero rule violations, unconnected items, or schematic-parity findings. DRC has no ignored checks. ERC ignores single-use global labels, four-way junctions, SPICE model issues, and footprint-filter mismatches. Run the checks after design edits; passing CAD checks does not establish physical or RF performance.
