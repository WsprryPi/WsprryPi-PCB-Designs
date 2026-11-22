# Validation

The schematic passes the configured electrical checks. The PCB has no configured board-rule violations or unrouted connections. There are no RF measurements of the assembled circuit.

| Check | Result |
| --- | --- |
| Schematic ERC | Zero violations |
| PCB DRC | Zero violations |
| Unconnected items | Zero |
| Schematic parity | Zero issues |
| BOM contents | Sixteen selected assembly positions; fourteen Basic, U1/D1 Extended |
| Connector flags | J1/J2/J3 excluded from BOM, on board, and not DNP |
| Project text variables | Sixteen definitions in the project file |
| Visual inspection | Schematic connections, resolved labels, C6 reservoir placement, PCB arrangement, and connector models |

The [CAD check record](docs/cad-validation.json) contains ERC and DRC results, ignored check categories, and source-file hashes. Its reports include error, warning, and exclusion severities for the enabled check categories. The [library manifest](libraries/MANIFEST.json) identifies local symbols, footprints, and models.

## Check configuration

The PCB configuration ignores missing courtyards, track endpoints not centered on vias, tuning-profile geometry, footprint-filter mismatches, and footprint-type mismatches. The schematic configuration ignores single-use global labels, four-way junctions, simulation-model issues, and footprint-filter mismatches. A zero-violation result says nothing about these ignored categories. See the [project settings](Logic%20RF%20Driver.kicad_pro).

Clearance checks use 0.20 mm for the default net class and 0.15 mm between pads within U1. These are CAD rules, not assembly measurements.

## Connectivity

All nineteen physical references are unique and have matching schematic UUID paths and pad nets. The indicator input joins RF_RAW on the U1 side of C4. J1/J2/J3 are excluded from the BOM, on the board, and not DNP.

| Net | Connections |
| --- | --- |
| +3V3 | J2.1, C1.1, U1.1, U1.5, R4.2, R5.2 |
| +5V | J2.2, C2.1, C3.1, U1.8 |
| CLK_IN | J1.1, R1.1, U1.2, U1.3 |
| RF_RAW | U1.6, U1.7, C4.1, R2.1 |
| RF_OUT | C4.2, J3.1 |
| Activity LED | R4.1 to D2.1 (anode); D2.2 (cathode) to Q1.3 |
| Power LED | R5.1 to D3.1 (anode); D3.2 (cathode) to GND |
| GND | Connector shields, J2.3, R1.2, C1.2, C2.2, C3.2, U1.4, D1.1, Q1.2, C6.2, R3.2, D3.2 |

C6 connects directly to D1's cathode through a 1.46 mm trace and has a nearby ground via.

The schematic connects its pins with wires and local net labels on a 1.27 mm connection grid. PCB pads follow the package geometry, and seventeen component anchors are off the 0.25 mm placement grid. See [layout details](PCB-LAYOUT.md).

## Simulation evidence

The [C4 analysis](C4-SELECTION.md) uses Samsung impedance and ESR data at 0, 2.5, and 5 V bias. The [amplifier comparison](COMPARISON.md) contains 78 logic and resistor-fed BS170 cases, fourteen timestep checks, and six bias-recentering checks. Ideal-choke results are diagnostic only. The [model scope](MODEL-SCOPE.md) explains what those calculations cover. The separate [detector study](INPUT-LOADING.md) evaluates RF_RAW loading through 220 ohms with surrogate semiconductor and LED models.

RF output power, heating, current sharing, supply transients, emissions, filter interaction, mechanical fit, and fabrication performance have no assembled-board measurement evidence. CAD checks and numerical consistency are not substitutes for those measurements.
