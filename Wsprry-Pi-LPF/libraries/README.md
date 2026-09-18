# Project libraries

This folder contains the project's symbol library, footprint library, and available 3D models. Library tables use `${KIPRJMOD}` paths; no sibling project folder is required. Open the project with KiCad 10.0.1 or newer to edit the local library assets. The saved board and schematic retain their existing file formats.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/Wsprry-Pi-LPF.kicad_sym) | 5 symbols, including all definitions used by the schematic |
| Footprints | [Footprint library](footprints/Wsprry-Pi-LPF.pretty/) | 6 footprints, including all footprints used by the board |
| Models | [3D models](3dmodels/) | 3 local STEP files |

The registered library nickname is `Wsprry Pi LPF`. Symbols and footprints use the same electrical pins and physical geometry as the saved design. Instance values and purchasing fields remain the design's responsibility; a generic library symbol does not select a component value or supplier part.

## SMA connectors

[SMA_Adafruit_1865_EdgeMount](footprints/Wsprry-Pi-LPF.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod) is the same edge-launch footprint used by the Pico 2W Wattmeter Shield. Select `Wsprry Pi LPF:SMA_Adafruit_1865` for the matching symbol. Pin 1 is signal and pin 2 is ground. The part is an Adafruit 1865 standard-polarity female SMA connector for a 1.6 mm board, fitted by hand with no paste apertures. Its symbol and footprint are excluded from the assembly BOM by default; set purchasing and placement options for the intended assembly process.

The footprint origin is the board seating edge on the signal centerline. Copper extends 0.500–4.064 mm into the board. Place the origin at the board edge and check physical fit against the [Adafruit connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf). It has no attached 3D model.

## Model limits

The optional `CAP-TH_L17.5-W11.1-P7.50-D0.8` footprint references an unavailable `EASYEDA_MODELS/CAP-TH_L17.5-W11.1-P7.50-D0.8.step` file. That footprint is not placed on this board.

The toroidal-inductor footprint retains its existing generic axial-inductor model. That model is not a mechanical representation of the actual wound toroid; check dimensions against the assembled component.

## Part data and validation

KiCad 10.0.1 DRC reports zero geometric violations and unconnected pads, with 11 existing footprint/symbol datasheet-field mismatches (`~` on the PCB versus blank in the schematic). ERC reports one undriven-power-pin error at `#PWR01` and one warning for the shared `RF_IN`/`VDRN_FEED` net labels. These circuit and field issues remain unresolved.

Existing ERC/DRC ignored categories remain in the project settings. Library resolution is not physical, electrical, or RF qualification.

## Sources and licenses

Standard symbol definitions come from the schematic's embedded KiCad symbols; local standard footprints preserve the placed board definitions, including project-specific geometry. Their original KiCad library families are identified by the part names and descriptions. Standard STEP models come from the installed KiCad model libraries. Copyright KiCad Library Contributors; [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/) applies to those assets.

The Adafruit land pattern derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). Its description retains attribution. Its matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` symbol under the KiCad library license.

Other custom footprints retain the repository's definitions and metadata. The repository MIT license does not replace third-party license terms.
