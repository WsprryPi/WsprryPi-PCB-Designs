# Pico 2W QRP Wattmeter Shield

A Raspberry Pi Pico 2 W shield with an ADL5904 RF power detector, an ADS1115 ADC, and a nominal 10 dB input attenuator. Open [Pico 2W Wattmeter Shield.kicad_pro](Pico%202W%20Wattmeter%20Shield.kicad_pro) in KiCad 10. The project uses local symbol, footprint, design-block, and 3D-model libraries with `${KIPRJMOD}` paths.

## Measurement range

| Parameter | Design target |
| --- | --- |
| J1 input | −20 to +20 dBm, approximately 10 µW to 100 mW |
| Attenuation | 9.96 dB calculated with a nominal 50 Ω detector-side termination |
| Frequency | 136 kHz–148 MHz, covering 2200 m through 2 m |
| Source | Unamplified WsprryPi GPIO clock |

The board is an unqualified prototype. Input limits and accuracy require resistor-rating verification, assembly checks, and RF calibration. See [input range](INPUT-RANGE.md) for calculations and measurement conditions.

## Assembly

The factory fits **C1–C9, R1–R8, U1, and U2: 19 components**, all on the front. The SMA connector, Pico sockets, and Pico module are fitted by hand. J1, J2, J3, U3, and the decorative logos are excluded from the factory BOM; J1, U3, and the logos are excluded from machine placement.

The **Shield purchasing BOM** preset exports the `LCSC Part #` field. The BOM and placement file must contain the same 19 component references. Use the supplier's required column headers and verify matched parts and IC orientation in its assembly preview. Plugin-generated exports must honor the manual-part exclusions.

U1 requires **selective epoxy-filled, planarized, copper-capped vias**: exactly the five vias inside its exposed ground pad. Their front surfaces are solderable; their rear pads are covered with soldermask. The stencil has four separate paste windows. These requirements must be included in the fabrication order.

- [Fabrication and assembly order notes](manufacturing-notes/ORDER-NOTES.txt)
- [Top assembly map](manufacturing-notes/ASSEMBLY-TOP.svg)
- [Selective via-treatment drawing](manufacturing-notes/U1-VIA-TREATMENT.svg)
- [U1 exposed-pad and stencil geometry](U1-PASTE-WINDOWS.md)
- [SMA connector and board-edge fit](J1-CONNECTOR-NOTES.md)
- [Pico sockets and antenna notch](PICO-HEADERS-AND-NOTCH.md)

The drawings identify the source PCB with a SHA-256 hash. Generate Gerbers, drills, BOM, and placement files from the board revision being ordered. The fabricator must confirm the selective via process; the assembler must confirm the stencil process. Socket mating height, connector fit, and RF performance require physical verification.

## Libraries and 3D view

Source libraries are in `pico-wattmeter.pretty/`, `pico-wattmeter.kicad_sym`, `pico-wattmeter.kicad_blocks/`, and `pico-wattmeter.3dshapes/`. See [footprint sources and licenses](pico-wattmeter.pretty/LIBRARY-SOURCES.md) and [U1's package model](pico-wattmeter.3dshapes/README.md).

Select **View > 3D Viewer** in the PCB Editor to inspect the assembly. U1 uses the included CP-16-22 STEP model. Passive and U2 models use the installed KiCad model libraries. J1 and the Pico/header assembly have no attached models.

Each silkscreen logo is a single unlocked footprint containing both polygons. The front and back logos move independently of their adjacent text.

## Project files

`fabrication-toolkit-options.json` contains export preferences. KiCad sources contain the part identifiers and assembly exclusions. The local JLCPCB plugin database, generated exports, fabrication packages, backups, and editor state are ignored by Git.

KiCad 10.0.1 ERC reports zero errors and warnings; DRC reports zero violations, unconnected pads, or footprint errors. DRC has no ignored checks. ERC ignores single-use global labels, four-way junctions, SPICE model issues, and footprint-filter mismatches. Run the checks after design edits; passing CAD checks does not establish physical or RF performance.
