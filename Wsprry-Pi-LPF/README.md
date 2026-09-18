# Wsprry Pi LPF Board

Low-pass filter board.

## Project files

Open [Wsprry-Pi-LPF.kicad_pro](Wsprry-Pi-LPF.kicad_pro) in KiCad 10.0.1 or newer. The KiCad sources are authoritative; generate any required schematic export from the current source revision.

The [project libraries](libraries/README.md) contain every symbol and footprint used by the design, plus available 3D models. Keep the `libraries/` folder and library tables with the project; their `${KIPRJMOD}` paths resolve within this directory. Library documentation covers connector options, model limitations, sources, and licenses.

The [filter workbook](<LPF-(C-L-C)-and-DC-Blocking-Filters.xlsx>) lists standard E96/E24 values for a seven-element, 1 dB Chebyshev C-L-C ladder and its ideal, lossless 50-ohm response. Parallel E24 capacitor pairs are used where their sum better approaches the target value. The 3 dB cutoff and fundamental-loss columns are calculated from the listed installed values, not the unrounded prototype values. The board does not implement a DC-blocking capacitor.

The 2 m filter is fully specified as `47.5 pF – 60.4 nH – 68.1 pF – 63.4 nH – 68.1 pF – 60.4 nH – 47.5 pF`. Its modeled 3 dB cutoff is 148.279504 MHz and its modeled loss at the 144.4901 MHz upper WSPR edge is 0.376 dB. The row uses the 144.4899–144.4901 MHz transmit band in the [WSPR frequency list](https://www.wsprnet.org/drupal/sites/wsprnet.org/files/wspr-qrg.pdf). Only the 2 m QRSS frequency cell is blank; no 2 m QRSS operating frequency is asserted by this project.

## Assembly

J1 and J2 are hand-fitted male 1×4 pin headers with 2.54 mm pitch. They remain populated in the schematic and PCB, including their existing pads and 3D models, but are excluded from the factory BOM. No manufacturer or purchasing part number is specified. BOM exporters must honor the exclusion flags; position-file settings are unchanged.

The other filter components are also excluded from the BOM in the current design. The default KiCad BOM export therefore contains column headings and no component rows; it is not a complete purchasing list for hand assembly.

Each shunt-capacitor location provides electrically parallel `CA` and `CB` footprints. A workbook entry written as `A + B` means that both listed capacitors are installed, one in each footprint; their order is electrically irrelevant. A single-value entry uses one footprint and leaves the other available for measured tuning. Record the installed pair and total capacitance for every assembled filter.

An Adafruit 1865 edge-launch SMA symbol and footprint are available in the local library but are not placed on this board.

The toroid model is a generic axial-inductor visualization. Check the wound component dimensions against the footprint before assembly.

## Validation

The design and workbook were checked on 2026-09-18 with KiCad 10.0.1, retaining the existing KiCad 10 version saves. Run ERC and DRC again after design edits and before producing manufacturing files.

- ERC: two active four-way-junction warnings remain at the J1 and J2 pin 2 ground-branch junctions. The report also contains two explicitly excluded four-way-junction records at those locations. A `PWR_FLAG` on J1 pin 1 documents that ground is supplied by the connected equipment; `RF_IN` remains the electrical input label and `(VDRN_FEED)` is explanatory text.
- DRC against the currently saved board: zero geometric violations, zero unconnected items, and zero schematic-parity issues. The saved board includes regenerated curved teardrops and current zone fills; track-end teardrops are enabled in the project settings.
- BOM export: the output contains headings and no component rows. All 13 placed components, including J1 and J2, are excluded from the BOM and none is marked do-not-populate.
- Workbook: the standardized E96/E24 values, including the 2 m WSPR row, 3 dB cutoffs, and fundamental losses were recomputed under the documented ideal 50-ohm model; the rendered sheets and component inventory were visually checked.
- Visual inspection: the board retains both four-pin headers and all four parallel shunt-capacitor pairs. The schematic clearly shows the external-ground power flag and separates the `RF_IN` electrical label from the `(VDRN_FEED)` explanatory text. The title-block revision is `1.0.1` in the schematic, PCB, and project metadata.

No ERC or DRC rule severity is currently set to `ignore`; the two explicit four-way-junction ERC exclusions remain visible in the project settings. These checks do not establish assembly fit or electrical/RF performance. Treat the design as untested until revision-specific physical validation is documented. See the [repository conventions](../README.md) and [validation requirements](../CONTRIBUTING.md).
