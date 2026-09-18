# U1 ADL5904 package model

`LFCSP-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm.step` was copied unchanged from the
KiCad 10.0.1 standard `Package_CSP.3dshapes` library on 2026-09-18. This is
KiCad's nominal package model, not an Analog Devices-branded part model.

- [Upstream model](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Package_CSP.3dshapes/LFCSP-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm.step)
- [ADL5904 datasheet, package drawing on page 27](https://www.analog.com/media/en/technical-documentation/data-sheets/adl5904.pdf)
- [Analog Devices CP-16-22 package drawing](https://www.analog.com/media/en/package-pcb-resources/package/pkg_pdf/lfcspcp/cp-16/CP_16_22.pdf)

KiCad's matching standard footprint explicitly identifies CP-16-22. Its nominal
3 x 3 mm body, 0.75 mm height, 0.5 mm lead pitch and 1.6 x 1.6 mm exposed pad
match the ADL5904 package. STEP Cartesian-point coordinates span -1.5 to +1.5 mm
in X/Y and 0 to 0.75 mm in Z. The standard footprint pin-1 orientation agrees
with U1's existing pad numbering. The model uses zero offset, unit scale and
zero additional rotation.

The package's 1.6 mm exposed pad is distinct from the existing 1.8 mm PCB copper
land. Adding the model does not change the footprint's pads, paste windows,
mask, vias, placement or routing. It is for nominal assembly visualization;
it does not establish mechanical tolerances or manufacturing qualification.

The model is referenced through `${KIPRJMOD}/pico-wattmeter.3dshapes/` in both U1
and the reusable QFN footprint, so no machine-specific path is required.

Copyright (C) 2024, KiCAD. The STEP file retains its original attribution and
[CC BY-SA 4.0 license with the KiCad library exception](https://www.kicad.org/libraries/license/).
The model remains under that license rather than the repository's general MIT
license.

Copied model SHA-256:
`ac27b9f183c0de63b91c6998121fd103522d4c02fb589dc57c911edaae309669`.
