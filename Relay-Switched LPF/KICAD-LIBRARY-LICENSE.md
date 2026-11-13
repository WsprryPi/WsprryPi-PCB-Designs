# KiCad library asset attribution and license

The following files in `relay-switched-lpf.3dshapes/` are unmodified copies from the installed **KiCad 10.0.6** library package:

| File | KiCad library source |
| --- | --- |
| `D_DO-35_SOD27_P7.62mm_Horizontal.step` | `Diode_THT.3dshapes/D_DO-35_SOD27_P7.62mm_Horizontal.step` |
| `PinSocket_1x04_P2.54mm_Vertical.step` | `Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x04_P2.54mm_Vertical.step` |
| `PinSocket_2x05_P2.54mm_Vertical.step` | `Connector_PinSocket_2.54mm.3dshapes/PinSocket_2x05_P2.54mm_Vertical.step` |

These assets retain **Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA-4.0), with the KiCad libraries exception**. The repository MIT license does not replace those terms. Preserve this attribution, the original model metadata/notices, and the linked license terms when redistributing these library assets.

- [KiCad library license and exception](https://www.kicad.org/libraries/license/)
- [CC-BY-SA 4.0 license text](https://creativecommons.org/licenses/by-sa/4.0/legalcode)
- [KiCad packages3D source and license](https://gitlab.com/kicad/libraries/kicad-packages3D/)
- [Recorded source paths and file hashes](relay-switched-lpf.3dshapes/sources.json)

The two socket model headers identify `Copyright (C) 2024, KiCAD` and include the library license notice and exception. The diode model retains the original 2017 header metadata crediting `kicad StepUp` and `ksu MCAD`. The files were copied without geometry edits or header removal.

## Four-pin connector symbols

The boxed body and contact graphics of project-local `LPF_IN` and `LPF_OUT` are adapted from **KiCad 10.0.6 `Connector_Generic:Conn_01x04`**, distributed in `Connector_Generic.kicad_sym` by the KiCad symbol-library contributors. The graphics are rotated/reflected, translated, and scaled for the compact schematic. Existing project pin endpoints, pin numbering, names, electrical types, instance UUIDs, and footprint assignments are retained; pin lengths match the adapted body. These definitions appear in `relay-switched-lpf.kicad_sym`, the schematic's embedded library, and the reproduction helper in `design/redraw_schematic.py`.

This adapted artwork retains the **CC-BY-SA-4.0 license with the KiCad libraries exception**, linked above. Source: [KiCad connector symbol library](https://gitlab.com/kicad/libraries/kicad-symbols/-/blob/master/Connector_Generic.kicad_sym). The repository MIT license does not replace those terms.

Other symbols, footprints, nominal VRML previews, and original generator code newly drawn for Relay-Switched LPF remain original repository work under [MIT](../LICENSE.md), except for the imported STEP assets and adapted connector artwork listed above. No manufacturer-provided CAD file or model of another relay was relabeled as a TX2.
