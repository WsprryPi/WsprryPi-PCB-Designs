# Validation

Quad Logic Buffer Amp is a placed, unrouted prototype. Its schematic and PCB have matching component and net assignments, with unresolved electrical and placement findings.

| Check | Current result |
| --- | --- |
| Active ERC findings | 2 |
| ERC exclusions | 2; the two paralleled inverter-output pairs |
| Board-rule findings | 0 |
| Unconnected PCB items | 205 |
| Schematic parity | 0 issues |
| Physical footprints | 65 |
| Routed tracks and vias | Zero |
| Library and model paths | Project-local paths resolve |
| Manifest model hashes | Match the local assets |

## Electrical findings

- `pin_not_connected`: 2.

U8 pins 4/6 and U59 pins 4/6 have individual ERC exclusions for their paralleled output pairs. The reports retain these exclusions and the existing ignored rule categories. No rule thresholds or exclusions are relaxed for this review.

R12 pin 1 and D5 pin 1 are open in the schematic. Their physical connections remain unresolved; routing is on hold. The transformer uses the BN43-1502 footprint with measured lead pitches of 6.5 mm across each pair and 17.5 mm between rows.

## PCB findings

The configured board-rule checks report no violations. The unrouted connections remain open.

## Files and checks

The project name, root KiCad filenames, hierarchy references, title variable, schematic export, and documentation links agree. Library identifiers retain their project-local names and `${KIPRJMOD}` paths. The root [ignore rules](../.gitignore) exclude local settings, locks, caches, backups, and generated output. Sources, reusable libraries, models, and the schematic reference PDF remain trackable.

Local review evidence is in `generated/project-review/`: `erc.json`, `drc.json`, and `asset-audit.json`. These reports are local generated output. The counts above describe the saved design; they do not establish electrical, RF, thermal, or physical qualification.
