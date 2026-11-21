# Validation

The schematic and PCB pass the configured electrical and design checks. There are no RF measurements of the assembled circuit.

| Check | Result |
| --- | --- |
| Schematic ERC | Zero violations |
| PCB DRC | Zero violations |
| Unconnected items | Zero |
| Schematic parity | Zero issues |
| Native BOM export | Six components: U1, R1, and C1–C4 |
| Connector flags | J1/J2/J3 excluded from BOM, on board, and not DNP |
| Project text variables | Sixteen definitions in the project file |
| Visual inspection | Schematic connections, resolved labels, PCB arrangement, and connector models inspected |

Local evidence includes the [ERC report](generated/rename/erc.json), [DRC report](generated/rename/drc-refilled.json), [native BOM](generated/basic-passives/native-bom.csv), and [source audit](generated/basic-passives/audit.json). The reports include error, warning, and exclusion severities for the enabled check categories.

## Check configuration

The PCB configuration ignores missing courtyards, track endpoints not centered on vias, tuning-profile geometry, footprint-filter mismatches, and footprint-type mismatches. The schematic configuration ignores single-use global labels, four-way junctions, simulation-model issues, and footprint-filter mismatches. A zero-violation result says nothing about these ignored categories. See the [project settings](Logic%20RF%20Driver.kicad_pro).

Clearance checks use 0.20 mm for the default net class and 0.15 mm between pads within U1. These are CAD rules, not assembly measurements.

## Connectivity

| Net | Connections |
| --- | --- |
| +3V3 | J2.1, C1.1, U1.1, U1.5 |
| +5V | J2.2, C2.1, C3.1, U1.8 |
| CLK_IN | J1.1, R1.1, U1.2, U1.3 |
| RF_RAW | U1.6, U1.7, C4.1 |
| RF_OUT | C4.2, J3.1 |
| GND | Connector shields, J2.3, R1.2, C1.2, C2.2, C3.2, U1.4 |

The schematic connects its pins with wires and local net labels on a 1.27 mm connection grid. PCB pads follow the package geometry, and several component anchors are off the 0.25 mm placement grid. See [layout details](PCB-LAYOUT.md).

## Simulation evidence

The [C4 analysis](C4-SELECTION.md) uses Samsung impedance and ESR data at 0, 2.5, and 5 V bias. The [amplifier comparison](COMPARISON.md) contains 78 logic and resistor-fed BS170 cases, fourteen timestep checks, and six bias-recentering checks. Ideal-choke results are diagnostic only. The [model scope](MODEL-SCOPE.md) explains what those calculations cover.

RF output power, heating, current sharing, supply transients, emissions, filter interaction, mechanical fit, and fabrication performance have no assembled-board measurement evidence. CAD checks and numerical consistency are not substitutes for those measurements.