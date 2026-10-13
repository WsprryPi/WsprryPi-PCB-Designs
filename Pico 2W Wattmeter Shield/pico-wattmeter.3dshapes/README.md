# Wattmeter 3D models

`LFCSP-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm.step` is the KiCad CP-16-22 package model used by U40 and its reusable footprint. It represents nominal package geometry without ADL5904 branding.

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

## Pico interface socket models

`PinSocket_1x20_P2.54mm_Vertical.step` is an independent copy of the socket asset in the [Pico shield template](../../Pico%202W%20Shield%20Template/pico-shield.3dshapes/README.md) and represents the standard KiCad 10.0.6 female 1×20, 2.54 mm socket model. Two instances in the local header footprint and placed U10 align with the pad rows and appear on B.Cu, following the template's mounting side.

Copyright (C) 2024, KiCAD, as recorded in the preserved STEP notice. The model uses [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/); the repository MIT license does not replace these terms. It is a generic visual aid, without selecting a purchasable socket or qualifying lead fit, mating height, or clearance. U10 is excluded from the automatic BOM and placement files.

## SMA connector model

`SMA_Adafruit_1865_Preview.wrl` is an unchanged copy of the [GPIO Shield's original illustrative SMA asset](../../WsprryPico%20GPIO%20Shield/wsprrypico-gpio-shield.3dshapes/README.md#bs170-circuit-assets). Both J30 in the saved PCB and the local `SMA_Adafruit_1865_EdgeMount` footprint reference this independent local copy through `${KIPRJMOD}/pico-wattmeter.3dshapes/`, with zero offset, unit scale, and zero additional rotation. The connector footprint's existing position and rotation determine its board orientation.

The mesh follows the existing Adafruit-derived fabrication outline: 6.5 mm flange, 6.1 mm barrel diameter, 9.5 mm forward reach, and 3.9 mm rear fingers straddling the 1.6 mm board. KiCad's VRML unit convention is already accounted for in the mesh coordinates. Threads, internal contacts, heights, and tolerances are simplified assumptions. It is a preview, rather than manufacturer CAD or mechanical qualification; confirm the supplied connector's fit independently.

The SMA-only [generator](generate_sma_1865_preview.py) retains the original mesh construction from the GPIO/Zero BS170 generator, without producing the unrelated trimmer model. Run `python3 pico-wattmeter.3dshapes/generate_sma_1865_preview.py` from this project directory to regenerate the same SMA mesh. The model and generator are original repository work under the [MIT license](../../LICENSE.md), with no third-party CAD geometry.
