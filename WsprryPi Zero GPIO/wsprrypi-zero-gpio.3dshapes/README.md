# Project-local 3D models

`PinSocket_2x20_P2.54mm_Vertical.step` is the standard KiCad 2×20, 2.54 mm vertical pin-socket model already used by the Raspberry Pi GPIO connector in `Wsprry-Pi-Synth-Univ`. The selectable H1 footprint places it on the underside of the WsprryPi Zero GPIO board and aligns it with the 40 electrical pads. Delete or restore H1 independently of the U10 electrical interface. The model file is copied locally so this project remains self-contained.

`PinHeader_1x03_P2.54mm_Vertical.step` is the standard KiCad 1×3, 2.54 mm vertical male-header model copied through `WsprryPi-GPIO-Univ`. The placed J12 `PinHeader_1x03_P2.54mm_Vertical` footprint references it through `${KIPRJMOD}/wsprrypi-zero-gpio.3dshapes/PinHeader_1x03_P2.54mm_Vertical.step`. J12 is excluded from BOM and position output but remains visible in the 3D board view. The model is a generic visualization and has not been validated against a selected purchasable header.

`LED_0603_1608Metric.step` is the KiCad 0603 LED model copied from `WsprryPi-GPIO-Univ` for D11. The local `LED_0603_1608Metric` footprint references it through `${KIPRJMOD}/wsprrypi-zero-gpio.3dshapes/LED_0603_1608Metric.step`.

`ALPS_SKRP_4.2x3.2x2.5mm.step` is the EasyEDA/JLCPCB model for Alps Alpine SKRPANE010, JLCPCB/LCSC C470426, converted with `easyeda2kicad` 1.0.1 and renamed without geometric modification. The local `ALPS_SKRP_4.2x3.2mm` footprint references it through `${KIPRJMOD}/wsprrypi-zero-gpio.3dshapes/ALPS_SKRP_4.2x3.2x2.5mm.step`. Verify the model against the physical component before using it for mechanical sign-off.

Copyright KiCad Library Contributors. The model is provided under [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). The repository MIT license does not replace these third-party terms.

The SKRPANE010 supplier model remains subject to its source terms; the repository MIT license does not relicense it.
