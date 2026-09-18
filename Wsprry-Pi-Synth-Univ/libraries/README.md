# Project libraries

This folder contains the project's symbol library, footprint library, and available 3D models. Library tables use `${KIPRJMOD}` paths; no sibling project folder is required. Open the project with KiCad 10.0.1 or newer to edit the local library assets.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/Wsprry-Pi.kicad_sym) | 15 symbols, including all definitions used by the schematic |
| Footprints | [Footprint library](footprints/Wsprry-Pi.pretty/) | 26 footprints, including all footprints used by the board |
| Models | [3D models](3dmodels/) | 14 local STEP files |

The registered library nickname is `Wsprry Pi`. Instance values and purchasing fields remain the design's responsibility; a generic library symbol does not select a component value or supplier part.

## SMA connectors

[SMA_Adafruit_1865_EdgeMount](footprints/Wsprry-Pi.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod) is the same edge-launch footprint used by the Pico 2W Wattmeter Shield. Select `Wsprry Pi:SMA_Adafruit_1865` for the matching symbol. Pin 1 is signal and pin 2 is ground. The part is an Adafruit 1865 standard-polarity female SMA connector for a 1.6 mm board, fitted by hand with no paste apertures. Its symbol and footprint are excluded from the assembly BOM by default, and its footprint is excluded from position files. Set these options for the intended assembly process.

The footprint origin is the board seating edge on the signal centerline. Copper extends 0.500–4.064 mm into the board. Place the origin at the board edge and check physical fit against the [Adafruit connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf). It has no attached 3D model.

## Model limits

The optional `CAP-TH_L17.5-W11.1-P7.50-D0.8` footprint references an unavailable `EASYEDA_MODELS/CAP-TH_L17.5-W11.1-P7.50-D0.8.step` file. That footprint is not placed on this board.

Y21 also references the unavailable `Oscillator_SMD_SeikoEpson_TG2520SMN-xxx-xxxxxx-4Pin_2.5x2.0mm.step` through `KICAD9_3DMODEL_DIR`. Its symbol and footprint are local and usable; its 3D body is missing. No substitute oscillator model is assigned.

The switch and through-hole SMA models correspond to [C318884](https://www.lcsc.com/product-detail/C318884.html) and [C496551](https://www.lcsc.com/product-detail/C496551.html). Verify model alignment and physical fit before using the 3D view for mechanical design.

See the [project README](../README.md) for assembly requirements and ERC/DRC findings.

## Sources and licenses

Standard symbols, footprints, and STEP models derive from KiCad libraries. Local footprints include project-specific geometry. Part names and descriptions identify their original library families. Copyright KiCad Library Contributors; [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/) applies to those assets.

The Adafruit land pattern derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). Its description retains attribution. Its matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` symbol under the KiCad library license.

The custom BWSMA-KWE-Z001, EEEFK1V470P, and TS-1187A-B-A-B symbols include supplier metadata and datasheet links. Switch and through-hole SMA STEP assets are supplied by EasyEDA/LCSC for the identified part numbers. Supplier attribution and embedded notices apply to those models.

The repository MIT license does not replace third-party license terms.
