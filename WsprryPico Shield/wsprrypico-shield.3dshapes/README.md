# Pico shield socket 3D model

`PinSocket_1x20_P2.54mm_Vertical.step` is the standard KiCad 1×20, 2.54 mm vertical female pin-socket model, originally copied unchanged from the KiCad 10.0.6 macOS installation's `Connector_PinSocket_2.54mm.3dshapes` library and copied locally with this project. Two instances in the local `Raspberry_Pi_Pico_2W_Header` footprint align with the electrical pad rows. The model is referenced through `${KIPRJMOD}/wsprrypico-shield.3dshapes/` so this project remains self-contained.

These are generic preview models. They do not select a purchasable part or establish socket lead fit, mating height, or clearance for an actual assembly. U1 and the schematic socket descriptions remain excluded from BOM and placement output by default.

Copyright (C) 2024, KiCAD, as recorded in the STEP file's preserved license notice. The model is provided under [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). The repository MIT license does not replace these third-party terms. The upstream asset is [PinSocket_1x20_P2.54mm_Vertical.step](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x20_P2.54mm_Vertical.step).
