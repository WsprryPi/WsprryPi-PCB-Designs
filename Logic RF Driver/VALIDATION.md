# Validation

The schematic passes the configured electrical checks. The saved PCB has filled ground zones and passes the configured design checks, including the local edge-contact rule for the SMA lands. It has no unrouted connections. There are no RF measurements of the assembled circuit.

| Check | Result |
| --- | --- |
| Schematic ERC | Zero violations |
| PCB DRC | Zero violations |
| Unconnected items | Zero |
| Schematic parity | Zero issues |
| Local footprint parity | Nineteen placed footprints match their local library definitions under KiCad's DRC comparison |
| BOM contents | Sixteen selected assembly positions; fourteen Basic, U1/D1 Extended |
| JLCPCB BOM export | Saved preset produces eleven grouped rows with supplier codes in `LCSC Part #`; connectors excluded |
| Connector flags | J1/J2/J3 excluded from BOM, on board, and not DNP |
| Project text variables | Sixteen definitions in the project file |
| Visual inspection | J1/J3 edge registration, signal fanouts, front/back ground lands, schematic, and local connector envelopes |

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

The schematic connects its pins with wires and local net labels on a 1.27 mm connection grid. PCB pads follow the package geometry, and nineteen component anchors are off the 0.25 mm placement grid. See [layout details](PCB-LAYOUT.md).

## Simulation evidence

The [output-sharing study](OUTPUT-SHARING.md) contains 92 candidate-circuit cases, including resistor values, timing skew, full-band sweeps, drive-strength mismatch, resistor parasitics, and finer-timestep checks. The design retains direct output paralleling. The current PCB pad nets match the unchanged schematic; layout and fill geometry are outside the circuit model.

The [board circuit simulation](BOARD-SIMULATION.md) contains 32 numerically checked cases with the detector, LED branches, timing-skew sensitivity, and finer-timestep checks. Its record identifies the saved design by file hashes. The calculation has no extracted PCB, connector, filter, or supply-network model.

The [C4 analysis](C4-SELECTION.md) uses Samsung impedance and ESR data at 0, 2.5, and 5 V bias. The [amplifier comparison](COMPARISON.md) contains 78 logic and resistor-fed BS170 cases, fourteen timestep checks, and six bias-recentering checks. Ideal-choke results are diagnostic only. The [model scope](MODEL-SCOPE.md) explains what those calculations cover. The separate [detector study](INPUT-LOADING.md) evaluates RF_RAW loading through 220 ohms with surrogate semiconductor and LED models.

RF output power, heating, current sharing, supply transients, emissions, filter interaction, mechanical fit, and fabrication performance have no assembled-board measurement evidence. CAD checks and numerical consistency are not substitutes for those measurements.

## SMA edge-clearance rule

J1 and J3 use the local Adafruit 1865 footprint derived from Adafruit's SMA_EDGELAUNCH package. The footprint origin is at each board edge, and its signal and ground lands extend from the edge to 4.064 mm inside the board.

The custom rule `Adafruit 1865 SMA lands at board edge` applies only to pads 1 and 2 belonging to J1/J3 with library identifier `SN74LVC2T45_Amp:SMA_Adafruit_1865_EdgeLaunch`. It covers both copper faces and both object orders in the edge-clearance check. A −0.01 mm minimum permits exact edge contact, which KiCad flags with a zero minimum. The actual copper stops at the edge. The rule changes no pad-to-pad or pad-to-track clearance. Tracks, zones, vias, and all other footprints retain the 0.50 mm copper-to-edge minimum. There are no added DRC exclusions or ignored categories.

The saved PCB reports zero violations, zero unconnected items, and zero schematic-parity findings under the enabled checks. Both ground zones are filled. These checks do not establish fabrication suitability of exposed edge copper, connector retention, or RF launch performance.

## Power terminal

J2 uses the local shared Adafruit 2136 / KF120-3P and 1×3-header footprint at X = 61.46 mm, Y = 52.25 mm, with 1.25 mm of housing overhang at the board edge. Its open-front silkscreen ends 0.25 mm inside the board; the fab outline and courtyard cover the full housing. All three pads have 1.2 mm finished holes and 2.0 mm copper pads. The terminal courtyard clears C1, C2, and C3. J1/J2/J3 remain excluded from the BOM, included on the board, and not DNP. The saved JLCPCB BOM contains sixteen assembly positions in eleven grouped rows.
