# Library sources and terms

Created November 18, 2026, from repository sources on `main`. The [asset manifest](LIBRARY-MANIFEST.json) records copied footprint/model paths and model SHA-256 checksums. Copies are independent; changes to the original projects do not update this project.

## Pico interface

The two interface/socket symbols, header footprint, and socket STEP model originate in the [Pico 2W Shield Template](../Pico%202W%20Shield%20Template/README.md). Its original interface work uses the repository [MIT license](LICENSE.md). The generic socket STEP originates in KiCad's `Connector_PinSocket_2.54mm.3dshapes` collection and retains CC BY-SA 4.0 with the KiCad library exception and embedded notices.

## Synth-shield imports

`C`, `GND`, `L`, `LED`, `PWR_FLAG`, `R`, and `SMA` were copied from the synth shield's local symbol library. The seven definitions are standalone. See its [symbol provenance](../WsprryPico%20Synth%20Shield%20with%20GPS/SYMBOL-SOURCES.md) and [footprint provenance](../WsprryPico%20Synth%20Shield%20with%20GPS/LIBRARY-SOURCES.md).

The passive/power symbols and SMA's Conn_Coaxial_Small-derived graphics retain KiCad library terms. Capacitor, resistor, LED, and inductor footprints derive from KiCad libraries and retain [CC BY-SA 4.0 with the KiCad library exception](KICAD-LIBRARY-LICENSE.md). Footprint content is preserved except that model references point to this project's local model directory.

`SMA_Adafruit_1865_EdgeMount` follows the public-domain Adafruit Eagle land pattern through the repository's GPIO/Zero amplifier assets. Its illustrative VRML model is original repository work under MIT. It is a hand-fit board-edge connector pattern for a nominal 1.6 mm PCB; it is not a factory assembly or physical-fit qualification.

The TDK inductor footprint retains its source KiCad terms and source adaptation. `VLS6045EX_6x6x4.5_Preview.wrl` is an original MIT-licensed illustrative envelope, not a supplier STEP model. Importing its footprint does not select or qualify a drain choke for a logic amplifier.

## Model copies

The socket STEP came from the template; the inductor STEP, TDK preview, and SMA preview came from the synth shield. Five additional STEP files were copied byte-for-byte from the installed KiCad 10.0.6 model library to satisfy the synth shield footprints' standard model references: three Capacitor_SMD sizes, Resistor_SMD 0603, and LED_SMD 0603. All KiCad solids retain their embedded notices and KiCad library terms. No external model downloads or manufacturer CAD assets were added.

GND and PWR_FLAG have no footprints or models. Models are visual aids; manufacturer drawings and actual parts govern fit. The repository MIT license does not supersede third-party terms.

## SN74ACT244 addition

Added November 18, 2026, using installed KiCad **10.0.6** assets. The standalone `74xx:74HC244` definition supplied the graphics and pin geometry. The local `SN74ACT244` copy changes the name/value, description, keywords, footprint filter, datasheet URL, and signal names to TI nomenclature. All 20 pin numbers and electrical types were checked against [TI SNx4ACT244 datasheet SCAS517G, page 3](https://www.ti.com/lit/ds/symlink/sn74act244.pdf#page=3). Outputs remain `tri_state`; enables and data inputs remain `input`; pins 10/20 remain `power_in`. Active-low enable bubbles are preserved. No inherited external symbol is required.

The default footprint is a local copy of `Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm`, for TI **PW**, such as **SN74ACT244PWR**. TI's PW0020A outline specifies nominal 4.4 x 6.5 mm body and 0.65 mm pitch; this is not the DW, DB, DGS, N, NS, or RKS package. Footprint geometry is unchanged; its standard STEP reference now uses `${KIPRJMOD}`. The matching KiCad STEP is copied byte-for-byte. All three assets retain [KiCad library terms](KICAD-LIBRARY-LICENSE.md); no TI CAD graphics were copied. See [the manifest](LIBRARY-MANIFEST.json) for source hashes.

The symbol and footprint were exported and visually inspected, and their pin/pad sets checked as 1 through 20. The library addition does not place the device in the schematic or PCB and does not establish power, RF, thermal, or physical-fit qualification.

## Side indicators and USB input

The CT-3210URGBC-P15-2B land pattern and nominal VRML model are original project assets based on the manufacturer drawing. The HRO TYPE-C-31-M-12 footprint derives from the KiCad 10.0.6 Connector_USB library with the coincident power and ground pads consolidated to the paired physical lands. The connector VRML comes from EasyEDA part C165948 via easyeda2kicad 1.0.1. Model rotation and offset align its shell stakes with the footprint. Supplier CAD retains its source attribution. See the [project pin mapping and datasheets](README.md).

## R7 provisional package

The project-local Fuse_1206_3216Metric footprint and STEP model are from the KiCad 10.0.6 Fuse libraries and retain the [KiCad library terms](KICAD-LIBRARY-LICENSE.md). The footprint uses a project-relative model path. The production marking and photographs support this package estimate. The exact manufacturer and rating remain open.

R7 uses the project-local copy of KiCad 10.0.6 Device:Polyfuse_Small, with the fuse footprint filter extended for the 1206 pattern. The symbol retains the KiCad library terms.
