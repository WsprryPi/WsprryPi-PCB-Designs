# Project-local 3D models

`PinSocket_1x20_P2.54mm_Vertical.step` is the standard KiCad 1×20, 2.54 mm vertical female pin-socket model, originally copied unchanged from the KiCad 10.0.6 macOS installation's `Connector_PinSocket_2.54mm.3dshapes` library and copied locally with this project. Two instances in the local `Raspberry_Pi_Pico_2W_Header` footprint align with the electrical pad rows. The model is referenced through `${KIPRJMOD}/wsprrypico-gpio-shield.3dshapes/` so this project remains self-contained.

These are generic preview models. They do not select a purchasable part or establish socket lead fit, mating height, or clearance for an actual assembly. U11 and the J11/J12 schematic socket descriptions remain excluded from BOM and placement output by default.

Copyright (C) 2024, KiCAD, as recorded in the STEP file's preserved license notice. The model is provided under [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). The repository MIT license does not replace these third-party terms. The upstream asset is [PinSocket_1x20_P2.54mm_Vertical.step](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x20_P2.54mm_Vertical.step).

## BS170 circuit assets

On 2026-10-05, the nine models below were copied unchanged from [Zero BS170's local model directory](../../WsprryPi%20Zero%20GPIO%20BS170/wsprrypi-zero-gpio-bs170.3dshapes/README.md). Their footprint paths were repointed to `${KIPRJMOD}/wsprrypico-gpio-shield.3dshapes/`. They are available for future PCB placement; the current PCB still contains only U11.

| Model | Circuit reference / origin |
| --- | --- |
| `TO-92_Inline.step` | Q41; unmodified standard KiCad 10.0.6 straight-lead TO-92 model |
| `PinHeader_1x03_P2.54mm_Vertical.step` | J13; standard KiCad male-header model |
| `PinHeader_1x02_P2.54mm_Vertical.step` | J21; standard KiCad male-header model |
| `PinSocket_1x04_P2.54mm_Vertical.step` | Two instances for J52; standard KiCad female-socket model |
| `LED_0603_1608Metric.step` | D11; standard KiCad LED model |
| `ALPS_SKRP_4.2x3.2x2.5mm.step` | SW11; EasyEDA/JLCPCB SKRPANE010 supplier model, converted by easyeda2kicad 1.0.1 |
| `FT37-43_25T_Upright.wrl` | L41; original illustrative model of the upright 25-turn hand-wound choke |
| `TC33X_Preview.wrl` | RV31; original illustrative trimmer model |
| `SMA_Adafruit_1865_Preview.wrl` | J51; original illustrative SMA model |

KiCad models retain their source copyright notices and [CC BY-SA 4.0 license with the KiCad exception](../KICAD-LIBRARY-LICENSE.md). The SKRPANE010 supplier model remains subject to its source terms; the repository MIT license does not relicense it. The three VRML models are original repository work under the [MIT license](../LICENSE.md), with no third-party geometry. Their original generator scripts were also copied unchanged:

- [generate_ft37_43.py](generate_ft37_43.py): run from this folder to regenerate the FT37-43 preview.
- [generate_rv31_j51.py](generate_rv31_j51.py): run from this folder to regenerate the trimmer and SMA previews.

The wound choke, trimmer, and SMA meshes simplify dimensions and details; they are visual aids rather than supplier solids or measured assemblies. The source project's [asset provenance](../../WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md) records their assumptions. Generic header and TO-92 models require comparison with the selected ordering variants. Physical fit and RF performance remain open.

Standard capacitor, resistor, and SOT-23-6 footprints retain `${KICAD10_3DMODEL_DIR}` references to installed KiCad model libraries. The source's missing Bourns TC33X STEP reference was already removed; the copied footprint uses the local illustrative VRML model instead.
