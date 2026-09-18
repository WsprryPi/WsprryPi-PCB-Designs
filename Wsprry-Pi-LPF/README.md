# Wsprry Pi LPF Board

Low-pass filter board.

## Project files

Open [Wsprry-Pi-LPF.kicad_pro](Wsprry-Pi-LPF.kicad_pro) in KiCad 10.0.1 or newer. The [schematic PDF](Wsprry-Pi-LPF.pdf) is a reference export; the KiCad sources are authoritative.

The [project libraries](libraries/README.md) contain every symbol and footprint used by the design, plus available 3D models. Keep the `libraries/` folder and library tables with the project; their `${KIPRJMOD}` paths resolve within this directory. Library documentation covers connector options, model limitations, sources, and licenses.

The [filter workbook](<LPF-(C-L-C)-and-DC-Blocking-Filters.xlsx>) contains C-L-C and DC-blocking filter calculations.

## Assembly

J1 and J2 are hand-fitted male 1×4 pin headers with 2.54 mm pitch. They remain populated in the schematic and PCB, including their existing pads and 3D models, but are excluded from the factory BOM. No manufacturer or purchasing part number is specified. BOM exporters must honor the exclusion flags; position-file settings are unchanged. An Adafruit 1865 edge-launch SMA symbol and footprint are available in the local library but are not placed on this board.

The toroid model is a generic axial-inductor visualization. Check the wound component dimensions against the footprint before assembly.

## Validation

The validation baseline is source revision `bc5cba8`, checked with KiCad 10.0.1. Run ERC and DRC again after design edits and before producing manufacturing files.

- ERC: one undriven-power-pin error at `#PWR01` and one warning for the shared `RF_IN`/`VDRN_FEED` net labels.
- DRC: zero geometric violations or unconnected pads; 11 footprint/symbol datasheet-field mismatches (`~` on the PCB versus blank in the schematic).

The project settings include ignored ERC/DRC categories. These checks do not establish assembly fit or electrical/RF performance. Treat the design as untested until revision-specific physical validation is documented. See the [repository conventions](../README.md) and [validation requirements](../CONTRIBUTING.md).
