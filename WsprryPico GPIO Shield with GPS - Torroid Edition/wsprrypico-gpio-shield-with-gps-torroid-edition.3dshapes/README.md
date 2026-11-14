# WsprryPico GPIO Shield with GPS - Torroid Edition 3D models

Local model references use `${KIPRJMOD}/wsprrypico-gpio-shield-with-gps-torroid-edition.3dshapes/`. Standard footprint models also use the installed `${KICAD10_3DMODEL_DIR}` library. Manufacturer drawings and actual parts govern physical fit; illustrative models show envelopes and placement.

T61's [upright low-support footprint and illustrative model](../design/t61-mount/README.md) are placed on the main PCB. All machine-assembled parts are on the underside. The unused L61 and GNSS models have been removed. R64 uses the installed standard KiCad resistor model.

## Assigned models

| Component | Asset | Basis and limits |
| --- | --- | --- |
| U11 socket rows | [PinSocket_1x20_P2.54mm_Vertical.step](PinSocket_1x20_P2.54mm_Vertical.step) | Standard KiCad 10.0.6 socket solid; two aligned instances; generic geometry |
| J61 SMA | [SMA_Adafruit_1865_Preview.wrl](SMA_Adafruit_1865_Preview.wrl) | Original MIT preview via the GPIO shield; simplified body, barrel and fingers |
| SW11 pushbutton | [SW_PUSH_Alps_SKHLACA010_NominalPreview.wrl](SW_PUSH_Alps_SKHLACA010_NominalPreview.wrl) | Original repository MIT nominal Alps 6 × 3.5 mm body / 4.3 mm actuator / simplified two-terminal preview; not manufacturer CAD |
| D11 LED | [LED_D3.0mm.step](LED_D3.0mm.step) | Imported generic KiCad 3 mm LED; illustrative rather than an exact Kingbright solid |
| T61 transformer | [T61_FairRite_5977000621_Upright_Bumper_4Pin_Preview.wrl](T61_FairRite_5977000621_Upright_Bumper_4Pin_Preview.wrl) | Original MIT upright core, continuous illustrative 15+15 winding paths, 8 mm diameter × 1.25 mm insulating pad and 4 × 6 × 0.5 mm bedding allowance; core bottom 1.75 mm above PCB. Mounting materials are builder-selected. Separate 1/4 on +Y, common 2/3 on -Y. Twists/tolerances/retention and real winding fit remain unqualified; legacy `Bumper` filename retained for compatibility |
| C61, C64, C66–C69 | Installed KiCad C_1206_3216Metric model | Walsin maximum 3.40 × 1.80 × 1.80 mm body governs fit; fitted-Pico checks add 0.10 mm solder stand-off |
| RV61 trimmer | [TC33X_Preview.wrl](TC33X_Preview.wrl) | Original MIT preview via the GPIO shield; illustrative body/height rather than exact TC33X-2 CAD |

The [footprint/model source document](../LIBRARY-SOURCES.md) links manufacturer drawings and records detailed geometry. The socket STEP retains its KiCad copyright notice, including Copyright (C) 2024, KiCAD. Imported KiCad solids follow [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/); the repository MIT license does not replace those terms.

## Rebuilding previews

Run `python3 ../design/t61-mount/generate_mount.py` to rebuild the transformer footprint, preview and dimensioned drawing. Its separate ignored blank coupon never modifies the project PCB.

The superseded SMT switch preview and its generator have been removed. The reused trimmer/SMA geometry is available in the [GPIO generator](https://github.com/WsprryPi/WsprryPi-PCB-Designs/blob/64fdd8f336c573cca9bfd5ce1ed3fad3cb0c8cb8/WsprryPico%20GPIO%20Shield/wsprrypico-gpio-shield.3dshapes/generate_rv31_j51.py).
