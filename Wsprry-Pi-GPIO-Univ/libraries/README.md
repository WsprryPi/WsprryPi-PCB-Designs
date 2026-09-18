# Project libraries

This folder contains the project's symbol library, footprint library, and available 3D models. Library tables use `${KIPRJMOD}` paths; no sibling project folder is required. Open the project with KiCad 10.0.1 or newer to edit the local library assets. The saved board and schematic retain their existing file formats.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/Wsprry-Pi.kicad_sym) | 13 symbols, including all definitions used by the schematic |
| Footprints | [Footprint library](footprints/Wsprry-Pi.pretty/) | 23 footprints, including all footprints used by the board |
| Models | [3D models](3dmodels/) | 12 local STEP files |

The registered library nickname is `Wsprry Pi`. Symbols and footprints use the same electrical pins and physical geometry as the saved design. Instance values and purchasing fields remain the design's responsibility; a generic library symbol does not select a component value or supplier part.

## SMA connectors

[SMA_Adafruit_1865_EdgeMount](footprints/Wsprry-Pi.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod) is the same edge-launch footprint used by the Pico 2W Wattmeter Shield. Select `Wsprry Pi:SMA_Adafruit_1865` for the matching symbol. Pin 1 is signal and pin 2 is ground. The part is an Adafruit 1865 standard-polarity female SMA connector for a 1.6 mm board, fitted by hand with no paste apertures. Its symbol and footprint are excluded from the assembly BOM by default; set purchasing and placement options for the intended assembly process.

The footprint origin is the board seating edge on the signal centerline. Copper extends 0.500–4.064 mm into the board. Place the origin at the board edge and check physical fit against the [Adafruit connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf). It has no attached 3D model.

The board uses J83, a through-hole BWSMA-KWE-Z001 connector ([LCSC C496551](https://www.lcsc.com/product-detail/C496551.html)). It is not interchangeable with the edge-launch footprint: its signal pin is 5 and ground pins are 1–4. An edge-launch conversion requires deliberate schematic pin mapping and board routing changes.

## Model limits

The optional `CAP-TH_L17.5-W11.1-P7.50-D0.8` footprint references an unavailable `EASYEDA_MODELS/CAP-TH_L17.5-W11.1-P7.50-D0.8.step` file. That footprint is not placed on this board.

The switch and through-hole SMA models correspond to [C318884](https://www.lcsc.com/product-detail/C318884.html) and [C496551](https://www.lcsc.com/product-detail/C496551.html). Saved model offsets, rotations, and scales are retained. Model availability does not establish physical fit.

## Part data and validation

**C11 has conflicting part data:** its schematic and board value is 100 µF, while its `C178565` purchasing fields select [Panasonic EEEFK1V470P, 47 µF / 35 V](https://www.lcsc.com/product-detail/C178565.html). Resolve the intended capacitance and purchasing number before ordering. The library default describes the 47 µF part; existing instance values are preserved.

KiCad 10.0.1 DRC reports zero violations, unconnected pads, or footprint errors. ERC reports 1 existing unconnected-wire-endpoint warning and no errors.

Existing ERC/DRC ignored categories remain in the project settings. Library resolution is not physical, electrical, or RF qualification.

## Sources and licenses

Standard symbol definitions come from the schematic's embedded KiCad symbols; local standard footprints preserve the placed board definitions, including project-specific geometry. Their original KiCad library families are identified by the part names and descriptions. Standard STEP models come from the installed KiCad model libraries. Copyright KiCad Library Contributors; [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/) applies to those assets.

The Adafruit land pattern derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). Its description retains attribution. Its matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` symbol under the KiCad library license.

The custom BWSMA-KWE-Z001, EEEFK1V470P, and TS-1187A-B-A-B symbol definitions retain the schematic's supplier metadata and datasheet links. Switch and through-hole SMA STEP assets are supplied by EasyEDA/LCSC for the identified part numbers, retrieved with easyeda2kicad 1.0.1. Their supplier attribution and embedded notices are preserved; no MIT relicensing is asserted.

Other custom footprints retain the repository's definitions and metadata. The repository MIT license does not replace third-party license terms.
