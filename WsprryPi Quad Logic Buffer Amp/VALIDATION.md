# Validation

WsprryPi Quad Logic Buffer Amp is a placed, unrouted prototype. Its schematic and PCB have matching component and net assignments, with unresolved electrical and placement findings.

| Check | Current result |
| --- | --- |
| Active ERC findings | 34 |
| ERC exclusions | 2; the two paralleled inverter-output pairs |
| Board-rule findings | 206 |
| Unconnected PCB items | 202 |
| Schematic parity | 0 issues |
| Physical footprints | 64 |
| Routed tracks and vias | Zero |
| Library and model paths | Project-local paths resolve |
| Manifest model hashes | Match the local assets |

## Electrical findings

- `pin_not_connected`: 31.
- `power_pin_not_driven`: 3.

U8 pins 4/6 and U59 pins 4/6 have individual ERC exclusions for their paralleled output pairs. The reports retain these exclusions and the existing ignored rule categories. No rule thresholds or exclusions are relaxed for this review.

The host interface has open pins and undriven power pins. The board placement also has the findings listed below. These designs are not ready for fabrication.

## PCB findings

| Finding | Count |
| --- | ---: |
| `shorting_items` | 32 |
| `clearance` | 12 |
| `hole_clearance` | 6 |
| `courtyards_overlap` | 14 |
| `pth_inside_courtyard` | 42 |
| `npth_inside_courtyard` | 3 |
| `solder_mask_bridge` | 38 |
| `hole_to_hole` | 1 |
| `silk_over_copper` | 54 |
| `silk_overlap` | 4 |

## Files and checks

The project name, root KiCad filenames, hierarchy references, title variable, schematic export, and documentation links agree. Library identifiers retain their project-local names and `${KIPRJMOD}` paths. The root [ignore rules](../.gitignore) exclude local settings, locks, caches, backups, and generated output. Sources, reusable libraries, models, and the schematic reference PDF remain trackable.

Local review evidence is in `generated/project-review/`: `erc.json`, `drc.json`, and `asset-audit.json`. These reports are local generated output. The counts above describe the saved design; they do not establish electrical, RF, thermal, or physical qualification.
