# WsprryPi LPF validation — Adafruit SMA update

Date: **2026-11-22**. Connector replacement on the development design, based on repository HEAD `79b16fbc4cead7a90698ba5cb952b9d7eec6038f`. Both independent LPF projects now use **Adafruit 1865**. Exact current source/library/rule hashes are in [source-hashes.json](validation/source-hashes.json).

Rechecked for commit on **2026-11-23** using KiCad **10.0.6 outside the sandbox**. Current saved boards were refilled, checked with schematic parity, and visually reviewed. Reports and source hashes were refreshed. The original board's saved Samtec/Adafruit mismatch was repaired to retain the requested Adafruit connector selection. Recorded edge-rule control tests date from 2026-11-22.

## Changes and preserved geometry

J2/J3 schematic values, purchasing fields, local footprint assignments, PCB lands, and model references now select Adafruit 1865. Independent libraries each contain its custom footprint and illustrative local VRML preview. The generic passive coaxial symbols remain appropriate: pin 1 RF and pin 2 ground. Obsolete Samtec footprint/model assets have been removed.

The 45.96 × approximately 12.873 mm outline, 1.60 mm stackup, complete header footprint/hole geometry, all filter footprints/placement, and project settings were compared with a pre-change snapshot and are unchanged. SMA axes remain at Y = 99.12 mm. New edge-datum origins are J2 at (114.00, 99.12) mm, −90°, and J3 at (159.96, 99.12) mm, +90°. Copper launch endpoints were repaired to the new center-pad locations. The filter topology, band values, parallel-capacitor strategy, and numerical models are unchanged.

[connector-change.json](validation/connector-change.json) records the outline/header/filter/stackup/settings comparisons and local-rule controls.

## Local edge-pad rule

The project-local `.kicad_dru` file sets **0 mm minimum edge clearance only for pads of J2/J3**, in either object order. Global copper-edge clearance remains **0.50 mm**, with the project file byte-identical to its pre-change snapshot. Net clearances, hole/via rules, severities, and unrelated checks were not changed.

The Adafruit-derived lands preserve the published 1.27 mm RF width, 1.524 mm ground width, and ±2.54 mm ground offsets. Their 4.014 mm length gives a **0.05 mm physical copper setback** from the board edge while retaining the source land's inland end. This avoids intersection with the drawn Edge.Cuts stroke. There are no paste apertures; fingers are hand soldered on both faces.

Temporary copies tested the rule behavior without changing either working design:

| Control | Result |
| --- | --- |
| Current board with local rule | Zero DRC violations |
| Same LCL board with rule file removed | Exactly 10 copper-edge-clearance violations, one per SMA pad |
| Same LCL board with J2 renamed J99 | Exactly 5 copper-edge-clearance violations on J99; J3 still allowed |

The identical rule text is used in both projects. [No-override report](validation/rule-controls/no-override.json) and [other-reference report](validation/rule-controls/other-reference.json) retain the control evidence. These are deliberate failing test copies, not current design errors. No new DRC/ERC exclusions were added.

## KiCad checks and visual inspection

All KiCad operations used **10.0.6 outside the sandbox**.

| Check | Current result |
| --- | --- |
| ERC, including exclusions | No active errors/warnings; the two existing excluded four-way-junction warnings remain visible. |
| DRC after saved zone refill, all severities | Zero violations |
| Unconnected items | Zero |
| Schematic parity | Zero issues |
| Local models | Three STEP files plus one illustrative SMA VRML file, all resolving locally |
| Header/filter/outline/settings comparison | Preserved |

[ERC JSON](validation/erc.json) and [DRC JSON](validation/drc.json) are the final reports. Zone refill was saved during the connector-layout check; the final parity/DRC run also checked the polished schematic fields. `ignored_checks` is empty. The CLI emitted a Fontconfig cache-version warning but completed its CAD checks and exports.

Both final schematics and both PCB faces were visually inspected. Supplier descriptions and purchasing metadata are hidden on the drawing; the connector value/purchasing fields identify Adafruit 1865. [Front copper/silkscreen](docs/board-front.png) and [mirrored back copper/silkscreen](docs/board-back.png) are reference previews. Native KiCad sources remain authoritative.

## Corrected findings retained

[History](validation/history/) retains representative intermediate failed reports and the LCL project's earlier creation records. During this replacement, initial pad-angle/field mismatches and edge-touching lands were corrected; saved boards now have the intended horizontal lands, matching library geometry, and a small physical setback. The final zero-violation result uses the requested pad-only rule, not a broader global relaxation. Pre-replacement LCL Samtec reports/hashes remain labeled `samtec-*` for provenance; they do not describe the current SMA implementation.

## Reproduce and remaining work

With this project directory as the working directory, execute KiCad outside the sandbox:

```sh
kicad-cli sch erc --severity-all --format json -o generated/erc.json 'WsprryPi LPF.kicad_sch'
kicad-cli pcb drc --schematic-parity --refill-zones --save-board --severity-all --format json -o generated/drc.json 'WsprryPi LPF.kicad_pcb'
```

The [Adafruit product](https://www.adafruit.com/product/1865), [published drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf), and public-domain [Eagle library](https://github.com/adafruit/Adafruit-Eagle-Library) were checked. The 1.6 mm product selection matches the nominal saved stackup; actual slot/fabrication tolerances, solder access, and fit remain unverified. The preview model is illustrative repository-owned geometry, not supplier CAD.

Confirm fabrication acceptance of near-edge lands, connector/body clearance in the carrier/enclosure, and actual assembly fit. VNA response, launch impedance, harmonic rejection, amplifier loading, component heating, power handling, and RF performance remain unmeasured on the exact assembly/configuration. CAD checks do not establish those results.

Local Markdown links, source/export ignore behavior, and `git diff --check` were checked. Commit and publication status are tracked by Git.
