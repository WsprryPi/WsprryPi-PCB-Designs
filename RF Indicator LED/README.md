# RF Indicator LED

This project contains an RF indicator schematic with diode, transistor, comparator, and LED stages. Open [the KiCad project](RF%20Indicator%20LED.kicad_pro) or the [schematic reference PDF](RF%20Indicator%20LED.pdf). The PCB file is empty: it has no outline, footprints, tracks, vias, or zones.

## Design status

The schematic has 21 physical component references. Part selection and footprint assignments are incomplete. It is a circuit draft, with no fabrication-ready PCB or measured RF performance.

| Item | Current limitation |
| --- | --- |
| R1–R4 and R6–R9 | Assigned DIP-8 footprints are placeholders that do not match two-terminal resistors |
| R5 and C1–C4 | No footprint assigned |
| C5 | Assigned SOT-23 footprint does not match a two-terminal capacitor |
| D1 | BAS70 value uses a generic Schottky symbol and an eight-pin WSON footprint; package selection is unresolved |
| D2 and D4 | Generic LEDs use Cree XHP50 footprints; LED part and package selection are unresolved |
| U1 | Value is TLV7011DBVR, while the embedded symbol is TLV7031DBV; the selected device and symbol must be reconciled |
| Supply | Two power-input pins have no driving power-output pin |

The saved assignments are retained as design evidence. They do not select validated physical components. See [validation](VALIDATION.md).

## Libraries and files

The schematic embeds its ten symbol definitions and references the standard KiCad `Comparator`, `Device`, `Diode`, `Transistor_BJT`, and `power` libraries. Its six assigned footprint types resolve in the installed standard KiCad footprint libraries; there are no project-local symbol, footprint, or model libraries. The empty PCB has no assigned 3D models. Editing symbol definitions or populating a board requires the corresponding KiCad libraries.

The repository [ignore rules](../.gitignore) cover local preferences, backups, locks, caches, and generated output. The schematic, project, empty PCB, reference PDF, and documentation are tracked sources or intentional reference assets.

Repository-owned work follows the [MIT license](../LICENSE.md). Embedded KiCad symbols retain their [KiCad library terms](https://www.kicad.org/libraries/license/).
