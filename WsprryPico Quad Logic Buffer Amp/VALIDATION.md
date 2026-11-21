# Validation

WsprryPico Quad Logic Buffer Amp is a placed, unrouted prototype. Its schematic and PCB have matching component and net assignments, with unresolved electrical and placement findings.

| Check | Current result |
| --- | --- |
| Active ERC findings | 52 |
| ERC exclusions | 2; the two paralleled inverter-output pairs |
| Board-rule findings | 19 |
| Unconnected PCB items | 193 |
| Schematic parity | 0 issues |
| Physical footprints | 63 |
| Routed tracks and vias | Zero |
| Library and model paths | Project-local paths resolve |
| Manifest model hashes | Match the local assets |

## Electrical findings

- `pin_not_connected`: 40.
- `power_pin_not_driven`: 10.
- `pin_not_driven`: 2.

U8 pins 4/6 and U59 pins 4/6 have individual ERC exclusions for their paralleled output pairs. The reports retain these exclusions and the existing ignored rule categories. No rule thresholds or exclusions are relaxed for this review.

The host interface has open pins and undriven power pins. The board placement also has the findings listed below. These designs are not ready for fabrication.

## PCB findings

| Finding | Count |
| --- | ---: |
| `shorting_items` | 3 |
| `clearance` | 2 |
| `courtyards_overlap` | 9 |
| `solder_mask_bridge` | 3 |
| `silk_over_copper` | 2 |

## Files and checks

The project name, root KiCad filenames, hierarchy references, title variable, schematic export, and documentation links agree. Library identifiers retain their project-local names and `${KIPRJMOD}` paths. The root [ignore rules](../.gitignore) exclude local settings, locks, caches, backups, and generated output. Sources, reusable libraries, models, and the schematic reference PDF remain trackable.

Local review evidence is in `generated/project-review/`: `erc.json`, `drc.json`, and `asset-audit.json`. These reports are local generated output. The counts above describe the saved design; they do not establish electrical, RF, thermal, or physical qualification.
