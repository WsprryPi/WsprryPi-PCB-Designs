# Pico shield socket 3D model

`PinSocket_1x20_P2.54mm_Vertical.step` is the standard KiCad 1×20, 2.54 mm vertical female pin-socket model, copied unchanged from the KiCad 10.0.6 macOS installation's `Connector_PinSocket_2.54mm.3dshapes` library. Two instances in the local `Raspberry_Pi_Pico_2W_Header` footprint align with the electrical pad rows. The model is referenced through `${KIPRJMOD}` so this independent shield remain self-contained.

These are generic preview models. They do not select a purchasable part or establish socket lead fit, mating height, or clearance for an actual assembly. U11 and the schematic socket descriptions remain excluded from BOM and placement output by default.

Copyright (C) 2024, KiCAD, as recorded in the STEP file's preserved license notice. The model is provided under [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). The repository MIT license does not replace these third-party terms. The upstream asset is [PinSocket_1x20_P2.54mm_Vertical.step](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x20_P2.54mm_Vertical.step).

## Component selection assets

`FT37-43_25T_Upright.wrl` is an unchanged copy of the GPIO shield's original MIT-licensed illustrative wound-choke model. The copied footprint's model path uses this project's `${KIPRJMOD}` folder. The model is provisional while the drain-choke sourcing choice remains open; it is not a measured or supplier-certified solid. Its generator is [the GPIO project's original script](../../WsprryPico%20GPIO%20Shield/wsprrypico-gpio-shield.3dshapes/generate_ft37_43.py).

Selected standard footprints reference installed `${KICAD10_3DMODEL_DIR}` assets where available. The Bourns TC33X potentiometer and BAT WIRELESS SMA footprints retain their stock STEP references, but those two files are missing from the installed KiCad 10.0.6 model collection. The KDS oscillator, XUNPU pushbutton and copper power selector have no assigned 3D solid. New footprint provenance and these model gaps are recorded in [LIBRARY-SOURCES.md](../LIBRARY-SOURCES.md). The selected socket ordering code is recorded in [PARTS.md](../PARTS.md); the retained socket STEP remains a generic preview.

## QLG3 GPS assembly

`QLG3_GPS_UndersideHeader.step` and `.wrl` depict the QLG3 above its host socket, with header underneath, E108 module and SMA on top, and two mounting spacers. The board is turned over relative to Hans's drawing and the XY coordinates are transformed consistently. Exact XY comes from Hans Summers; standard 1×5 header/socket STEP inputs are copied locally from KiCad 10.0.6. Other dimensions are photo-based approximations. The combined models retain the KiCad library terms for their incorporated connector geometry. See [dimensions, assumptions, generator and validation](../qlg3-model/README.md).
