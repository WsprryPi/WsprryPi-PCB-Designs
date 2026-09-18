# Wsprry Pi LPF Board

Low-pass filter board.

## Project files

Open [Wsprry-Pi-LPF.kicad_pro](Wsprry-Pi-LPF.kicad_pro) in KiCad 10.0.1 or newer. The [schematic PDF](Wsprry-Pi-LPF.pdf) is a reference export; the KiCad sources are authoritative.

The [project libraries](libraries/README.md) contain every symbol and footprint used by the design, plus available 3D models. Keep the `libraries/` folder and library tables with the project; their `${KIPRJMOD}` paths resolve within this directory. Library documentation covers connector options, model limitations, sources, and licenses.

The [filter workbook](<LPF-(C-L-C)-and-DC-Blocking-Filters.xlsx>) contains C-L-C and DC-blocking filter calculations.

## Assembly

J1 and J2 are hand-fitted male 1×4 pin headers with 2.54 mm pitch. They remain populated in the schematic and PCB, including their existing pads and 3D models, but are excluded from the factory BOM. No manufacturer or purchasing part number is specified. BOM exporters must honor the exclusion flags; position-file settings are unchanged.

The other filter components are also excluded from the BOM in the current design. The default KiCad BOM export therefore contains column headings and no component rows; it is not a complete purchasing list for hand assembly.

An Adafruit 1865 edge-launch SMA symbol and footprint are available in the local library but are not placed on this board.

The toroid model is a generic axial-inductor visualization. Check the wound component dimensions against the footprint before assembly.

## Validation

The header BOM-exclusion update was checked on 2026-09-18 with KiCad 10.0.1, retaining the existing KiCad 10 version saves. Run ERC and DRC again after design edits and before producing manufacturing files.

- ERC: one undriven-power-pin error at `#PWR01` and one warning for the shared `RF_IN`/`VDRN_FEED` net labels.
- Geometric DRC: zero violations or unconnected pads, unchanged before and after the header update.
- Schematic-parity DRC: KiCad CLI aborted before producing a report, both before and after the header update. The earlier check at revision `bc5cba8` reported 11 footprint/symbol datasheet-field mismatches (`~` on the PCB versus blank in the schematic); their current status is not revalidated by the geometric check.
- BOM export: J1 and J2 are omitted. Their schematic instances remain on-board and are not marked do-not-populate.
- Visual inspection: the board export retains both four-pin headers. The before/after board SVG drawing content is identical; only export filename/time metadata differs. The header update changes purchasing metadata and BOM flags only.

The project settings include ignored ERC/DRC categories. These checks do not establish assembly fit or electrical/RF performance. Treat the design as untested until revision-specific physical validation is documented. See the [repository conventions](../README.md) and [validation requirements](../CONTRIBUTING.md).
