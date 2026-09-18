# Pico 2W QRP Wattmeter Shield

KiCad 10 project for a Raspberry Pi Pico 2 W shield using an ADL5904 RF power
detector and ADS1115 ADC. Open
[Pico 2W Wattmeter Shield.kicad_pro](Pico%202W%20Wattmeter%20Shield.kicad_pro).
The schematic, board, symbol library, footprint library and reusable schematic
block are included. Library tables use `${KIPRJMOD}` paths.

This is an unqualified prototype. The intended J1 measurement range is roughly
10 uW to 100 mW with nominal 10 dB attenuation, targeting 2200 m through 2 m.
These are design targets, not measured accuracy or guaranteed power ratings.
See [input range and calibration requirements](INPUT-RANGE.md).

## Assembly and fabrication

- The schematic uses `LCSC Part #` fields. The **Shield purchasing BOM** preset
  exports those part numbers for the 19 electronic components.
- J1 (SMA connector), J2/J3 (socket procurement symbols), and U3 (Pico header
  interface) are excluded from the factory assembly BOM as applicable. Fit the
  connector and headers manually. Decorative logos are also excluded.
- Follow [the order notes](manufacturing-notes/ORDER-NOTES.txt), particularly the
  selective fill/planarize/cap requirement for U1's five exposed-pad vias.
- [Assembly map](manufacturing-notes/ASSEMBLY-TOP.svg) and
  [via-treatment drawing](manufacturing-notes/U1-VIA-TREATMENT.svg) are retained
  reference drawings from the manufacturing review. Their source hashes identify
  the earlier board snapshot; regenerate manufacturing outputs from the current
  KiCad source before ordering.
- Exported files still need the supplier's required headers, part matching,
  orientation review and fabrication confirmation. The plugin database is not
  authoritative for assembly exclusions; verify that J1 and headers are omitted
  when using any plugin-generated BOM or placement file.

Additional design notes:
[headers and antenna notch](PICO-HEADERS-AND-NOTCH.md),
[SMA connector](J1-CONNECTOR-NOTES.md),
[U1 paste windows](U1-PASTE-WINDOWS.md),
[manufacturing review](MANUFACTURING-REVIEW-2026-09-18.md), and
[manufacturing changes](MANUFACTURING-CHANGES-2026-09-18.md).
These dated records describe their respective snapshots; later silkscreen and
field-name edits are present in the current source.

## Repository contents

`pico-wattmeter.pretty/`, `pico-wattmeter.kicad_sym` and
`pico-wattmeter.kicad_blocks/` are source libraries. Preserve their
[provenance and license notices](pico-wattmeter.pretty/LIBRARY-SOURCES.md).
`fabrication-toolkit-options.json` records the project's export preferences.
`AD8307 Design.zip` is a preserved historical alternate-design archive, not the
current ADL5904 design or a fabrication package.

Generated exports, fabrication packages, automatic backups and local KiCad
state are ignored by the repository-level rules. This directory's `.gitignore`
also excludes the JLCPCB plugin's mutable `jlcpcb/project.db` and SQLite sidecars;
the part numbers are retained in the KiCad sources. Ignored review evidence is
local-only and is not included when cloning this repository.

ERC/DRC results apply to the exact checked source, not assembled hardware.
No physical RF or manufacturing qualification is implied by a successful check.
