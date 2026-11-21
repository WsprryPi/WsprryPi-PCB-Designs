# Local 3D models

All twenty-two assets resolve through `${KIPRJMOD}/logic-buffer-amp.3dshapes/`. Copies retain the source bytes and embedded notices; only their referencing footprint paths changed.

| Asset | Source and limits |
| --- | --- |
| Transformer_BN43-1502_Flat_4Lead.wrl | Original perforated core and two primary turns and four secondary turns with illustrative wire dress. See the [dimensions and estimates](../README.md#l2-flat-mount-transformer). |
| SOT-23.step, SOT-23-5.step, SOT-23-6.step, SOT-363_SC-70-6.step | KiCad Package_TO_SOT_SMD package models for Q3/Q6, the available five- and six-pin SOT-23 footprints, and U6/U8/U59 respectively |
| SOT-353_SC-70-5.step | KiCad five-pin SC70 model for U88 |
| D_SOD-123.step | KiCad SOD-123 model for D3 |
| LED_CT-3210URGBC-P15-2B.wrl | Original nominal body and side lens based on the CHONGTIAN drawing. |
| USB_C_Receptacle_HRO_TYPE-C-31-M-12.wrl | EasyEDA C165948 supplier model imported with easyeda2kicad 1.0.1. |
| D_SOD-323.step | Installed KiCad Diode_SMD model |
| R_1210_3225Metric.step | Installed KiCad Resistor_SMD model |
| PinHeader_1x02_P2.54mm_Vertical.step | Zero GPIO BS170 shield’s vertical two-pin header model |
| PinSocket_1x20_P2.54mm_Vertical.step | Template's generic KiCad socket; two instances in the header; no selected manufacturer or fit qualification |
| C_0603_1608Metric.step | Installed KiCad Capacitor_SMD model |
| C_0805_2012Metric.step | Installed KiCad Capacitor_SMD model |
| C_1206_3216Metric.step | Installed KiCad Capacitor_SMD model |
| R_0603_1608Metric.step | Installed KiCad Resistor_SMD model |
| LED_0603_1608Metric.step | Installed KiCad LED_SMD model |
| L_0603_1608Metric.step | Synth shield's generic KiCad inductor model |
| VLS6045EX_6x6x4.5_Preview.wrl | Synth shield's original MIT illustrative 6 x 6 x 4.5 mm envelope; terminals and winding detail omitted |
| TSSOP-20_4.4x6.5mm_P0.65mm.step | Installed KiCad Package_SO model for the SN74ACT244 PW package; generic package geometry |
| SMA_Adafruit_1865_Preview.wrl | Synth shield's original MIT illustrative connector preview; not exact manufacturer CAD |

KiCad models retain [KiCad library terms](../KICAD-LIBRARY-LICENSE.md); original previews retain the [MIT license](../LICENSE.md). See [provenance](../LIBRARY-SOURCES.md) and [copy checksums](../LIBRARY-MANIFEST.json). These models do not establish mechanical fit or RF performance.
