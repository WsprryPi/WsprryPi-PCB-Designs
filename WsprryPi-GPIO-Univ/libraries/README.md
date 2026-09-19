# Project libraries

This folder contains the project's symbol library, footprint library, and available 3D models. Library tables use `${KIPRJMOD}` paths; no sibling project folder is required. Open the project with KiCad 10.0.1 or newer to edit the local library assets.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/Wsprry-Pi.kicad_sym) | 15 symbols, including all definitions used by the schematic and the two amplifier-input parts below |
| Footprints | [Footprint library](footprints/Wsprry-Pi.pretty/) | 25 footprints, including all footprints used by the board and the two amplifier-input packages below |
| Models | [3D models](3dmodels/) | 15 local STEP files |

The registered library nickname is `Wsprry Pi`. Instance values and purchasing fields remain the design's responsibility; a generic library symbol does not select a component value or supplier part.

## SMA connectors

[SMA_Adafruit_1865_EdgeMount](footprints/Wsprry-Pi.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod) is the same edge-launch footprint used by the Pico 2W Wattmeter Shield and is placed as J83 on this board. Select `Wsprry Pi:SMA_Adafruit_1865` for the matching symbol. Pin 1 is signal and pin 2 is ground. The part is an Adafruit 1865 standard-polarity female SMA connector for a 1.6 mm board, fitted by hand with no paste apertures. Its symbol and footprint are excluded from the assembly BOM, and its footprint is excluded from position files.

The footprint origin is the board seating edge on the signal centerline. Copper extends 0.500–4.064 mm into the board. Place the origin at the board edge and check physical fit against the [Adafruit connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf). It has no attached 3D model.

## Model limits

The project library includes unplaced assets for the proposed amplifier input:

- `C689467` is Analog Devices `LTC6752HS5#TRMPBF`. Its local symbol follows the
  manufacturer's TSOT-23-5 pinout, and `TSOT-23-5` plus its STEP model are
  project-local copies of the KiCad library assets. See the
  [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/6752fc.pdf).
- `C42400210` is ElecSuper `PESD3V6Z1BCSF(ES)`. Its bidirectional TVS symbol
  identifies the exact MPN and LCSC number. The
  `DFN0603-2L_L0.62-W0.32-P0.40` footprint implements the 0.40 mm-pitch,
  0.25 mm by 0.32 mm pad recommendation in the manufacturer's Rev 1.2
  [datasheet](https://www.lcsc.com/datasheet/C42400210.pdf). Its supplier STEP
  model is stored locally.

These assets are not placed on the schematic or board. The DFN0603-2L package
is exceptionally small; verify stencil capability, assembly yield, model
alignment, and physical fit before production. The STEP models are
visualization aids, not physical-fit evidence.

The optional `CAP-TH_L17.5-W11.1-P7.50-D0.8` footprint references an unavailable `EASYEDA_MODELS/CAP-TH_L17.5-W11.1-P7.50-D0.8.step` file. That footprint is not placed on this board.

The C11 footprint references the local [CP_Elec_6.3x5.8 STEP model](3dmodels/Capacitor_SMD.3dshapes/CP_Elec_6.3x5.8.step), copied from the KiCad 3D model library. It represents the nominal 6.3 mm diameter by 5.8 mm package of the selected 47 µF capacitor, but it is a generic visualization and has not been validated against an assembled board.

The switch and through-hole SMA models correspond to [C318884](https://www.lcsc.com/product-detail/C318884.html) and [C496551](https://www.lcsc.com/product-detail/C496551.html). Verify model alignment and physical fit before using the 3D view for mechanical design.

See the [project README](../README.md) for assembly requirements and ERC/DRC findings.

## Sources and licenses

Standard symbols, footprints, and STEP models derive from KiCad libraries. Local footprints include project-specific geometry. Part names and descriptions identify their original library families. Copyright KiCad Library Contributors; [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/) applies to those assets.

The Adafruit land pattern derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). Its description retains attribution. Its matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` symbol under the KiCad library license.

The custom BWSMA-KWE-Z001, EEEFK1V470P, TS-1187A-B-A-B,
LTC6752HS5#TRMPBF, and PESD3V6Z1BCSF(ES) symbols include supplier metadata and
datasheet links. The LTC6752 symbol and TSOT-23-5 package assets derive from the
KiCad libraries and the Analog Devices datasheet. The PESD3V6Z1BCSF(ES) symbol
derives from KiCad's bidirectional TVS symbol, and its footprint dimensions
come from the ElecSuper datasheet. Switch, through-hole SMA, and
PESD3V6Z1BCSF(ES) STEP assets are supplied by EasyEDA/LCSC for the identified
part numbers. Supplier attribution and embedded notices apply to those models.

The repository MIT license does not replace third-party license terms.
