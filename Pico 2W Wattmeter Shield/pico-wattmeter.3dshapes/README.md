# U1 ADL5904 package model

`LFCSP-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm.step` is the KiCad CP-16-22 package model used by U1 and its reusable footprint. It represents nominal package geometry without ADL5904 branding.

| Feature | Dimension |
| --- | --- |
| Body | 3 × 3 mm |
| Height | 0.75 mm |
| Leads | 16, at 0.5 mm pitch |
| Exposed pad | 1.6 × 1.6 mm |
| Model transform | Zero offset, unit scale, zero additional rotation |

The package's 1.6 mm exposed pad is distinct from the PCB's 1.8 mm copper land. Pin 1 matches the footprint's numbering. The model is referenced through `${KIPRJMOD}/pico-wattmeter.3dshapes/` and is intended for nominal assembly visualization, not tolerance qualification.

## Sources and license

- [KiCad STEP model](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Package_CSP.3dshapes/LFCSP-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm.step)
- [ADL5904 datasheet, package drawing on page 27](https://www.analog.com/media/en/technical-documentation/data-sheets/adl5904.pdf)
- [Analog Devices CP-16-22 package drawing](https://www.analog.com/media/en/package-pcb-resources/package/pkg_pdf/lfcspcp/cp-16/CP_16_22.pdf)

Copyright (C) 2024, KiCAD. The STEP file includes its original attribution and [CC BY-SA 4.0 license with the KiCad library exception](https://www.kicad.org/libraries/license/). These terms apply to the model rather than the repository's general MIT license.

Model SHA-256: `ac27b9f183c0de63b91c6998121fd103522d4c02fb589dc57c911edaae309669`.
