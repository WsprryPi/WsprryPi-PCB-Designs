# Synth shield 3D models

Local model references use `${KIPRJMOD}/wsprrypico-synth-shield.3dshapes/`. Standard footprint models also use the installed `${KICAD10_3DMODEL_DIR}` library. Manufacturer drawings and actual parts govern physical fit; illustrative models show envelopes and placement.

## Assigned local models

| Component | Asset | Basis and limits |
| --- | --- | --- |
| U11 socket rows | [PinSocket_1x20_P2.54mm_Vertical.step](PinSocket_1x20_P2.54mm_Vertical.step) | Standard KiCad 10.0.6 socket solid; two aligned instances; generic geometry |
| J61 SMA | [SMA_Adafruit_1865_Preview.wrl](SMA_Adafruit_1865_Preview.wrl) | Original MIT preview via the GPIO shield; simplified body, barrel and fingers |
| J71 U.FL | [U.FL_Hirose_U.FL-R-SMT-1_Vertical.step](U.FL_Hirose_U.FL-R-SMT-1_Vertical.step) | Standard KiCad solid; embedded license retained |
| L61 drain choke | [VLS6045EX_6x6x4.5_Preview.wrl](VLS6045EX_6x6x4.5_Preview.wrl) | Original MIT 6 × 6 mm body, 4.5 mm maximum height; detailed terminals/winding omitted |
| L71 antenna choke | [L_0603_1608Metric.step](L_0603_1608Metric.step) | Standard KiCad generic 0603 inductor solid |
| U71 GNSS | [Zhongke_ATGM336H-5N31.wrl](Zhongke_ATGM336H-5N31.wrl) | Original MIT 9.7 × 10.1 × 2.4 mm approximate envelope |
| SW11 pushbutton | [XUNPU_TS1088R_3.9x3x2_Preview.wrl](XUNPU_TS1088R_3.9x3x2_Preview.wrl) | Original MIT 3.90 × 3.00 × 2.00 mm preview; cover, actuator and tabs simplified |
| RV61 trimmer | [TC33X_Preview.wrl](TC33X_Preview.wrl) | Original MIT preview via the GPIO shield; illustrative body/height rather than exact TC33X-2 CAD |
| Y41 TCXO | [KDS_DSB321SDN_3.2x2.5x0.9_Preview.wrl](KDS_DSB321SDN_3.2x2.5x0.9_Preview.wrl) | Original MIT 3.20 × 2.50 × 0.90 mm family envelope; simplified lid/contacts and pin-1 marker |

The [footprint/model source document](../LIBRARY-SOURCES.md) links manufacturer drawings and records detailed geometry. The socket STEP retains its KiCad copyright notice, including Copyright (C) 2024, KiCAD. Imported KiCad solids follow [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/); the repository MIT license does not replace those terms.

## Rebuilding previews

Run `python3 generate_switch_tcxo_previews.py` from this folder to regenerate the switch and oscillator previews. [The generator](generate_switch_tcxo_previews.py) uses KiCad's 0.1-inch VRML units, centered XY origins and mounting surface Z = 0. The reused trimmer/SMA geometry is available in the [GPIO generator](../../WsprryPico%20GPIO%20Shield/wsprrypico-gpio-shield.3dshapes/generate_rv31_j51.py).
