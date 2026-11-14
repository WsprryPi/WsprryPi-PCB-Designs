# WsprryPico GPIO Shield with GPS engineering validation

## Current saved-source check — 2026-11-13

KiCad **10.0.6** was used for ERC and DRC with all severities, all track errors, and schematic parity enabled for DRC. ERC reports **0 findings**. Saved-board DRC reports **0 violations, 0 unconnected items, and 0 schematic-parity differences**. Existing ignored categories and design rules were retained without changes. Schematic PDF and board-layer exports were visually reviewed. Electrical, physical, and RF qualification remain open.

Reports and renders are retained locally in ignored `generated/commit-all-review/`. SHA-256 of the checked source files:

- `WsprryPico GPIO Shield with GPS.kicad_sch`: `41fe366f506206ee4ed47c7c31420ab48772999fcecf36e92f1b739a37c134b7`
- `WsprryPico GPIO Shield with GPS.kicad_pcb`: `49021b5afcdd4e36904e10f1da8dd9e8db312acefa387b8eccc68545a98a1cd8`
- `WsprryPico GPIO Shield with GPS.kicad_pro`: `cb7671d5ee38d100be467f2d91efe4717c1960b6ceee432b1a1fd00e2106e77f`

## Historical validation record

The saved design has **zero ERC findings, PCB DRC violations, unconnected items and schematic parity issues** under its configured rules, checked with **KiCad 10.0.6 on 2026-10-19**. These CAD checks establish connectivity and geometric compliance within those rules. The assembled shield has no recorded electrical, thermal, RF or fabricated-impedance qualification.

## CAD checks

| Check | Result |
| --- | --- |
| Schematic ERC, all severities | 0 findings |
| PCB DRC, all severities and all track errors | 0 violations |
| Unconnected items | 0 |
| Schematic/PCB parity | 0 |
| Inventory | 38 non-power schematic references, 36 PCB footprints, 30 SMT assembly positions |
| Purchasing records | 37 engineering CSV entries excluding U11; 38 workbook references |
| Libraries | 18 used symbol definitions, 17 assigned footprint types, eight local model files |
| Model paths | All 16 distinct local/installed-standard model paths resolve |
| Supplier fields | Manufacturer, MPN and LCSC codes agree across schematic, CSV and workbook; the 23 capacitor/resistor/trimmer references also match the PCB |

DRC refills zones in memory without saving the PCB. No individual ERC or DRC exclusions are configured. ERC ignores `footprint_filter`, `four_way_junction`, `simulation_model_issue` and `single_global_label`; DRC lists no ignored checks. A zero result applies to this configured profile.

U21 supplies the receiver's VCC/VBAT on `GNSS_3V3`. U71's manufacturer is `Zhongke` throughout the parts records and placed components. The capacitor/resistor/trimmer catalog review is dated **2026-10-10**; it does not establish current stock, assembly fit or RF suitability.

## Source identity

The checks apply to these saved files with this project's local libraries and installed KiCad models.

| File | SHA-256 |
| --- | --- |
| WsprryPico GPIO Shield with GPS.kicad_sch | `41fe366f506206ee4ed47c7c31420ab48772999fcecf36e92f1b739a37c134b7` |
| WsprryPico GPIO Shield with GPS.kicad_pcb | `49021b5afcdd4e36904e10f1da8dd9e8db312acefa387b8eccc68545a98a1cd8` |
| WsprryPico GPIO Shield with GPS.kicad_pro | `cb7671d5ee38d100be467f2d91efe4717c1960b6ceee432b1a1fd00e2106e77f` |
| WsprryPico GPIO Shield with GPS.kicad_dru | `31cf30504736a1dab394ca73ff13c8c4575e2c55b485f6fd1219cab8a9ad4818` |
| wsprrypico-gpio-shield-with-gps.kicad_sym | `b687fcdecdfd5c8ff197ba1014c19bf2a8236dd3fa841f941837539d23850703` |
| wsprrypico-gpio-shield-with-gps.pretty/TO-92_Inline.kicad_mod | `b2bb5db749a811978248f5efe6fda7819f3bd7fa52098aec18cb6fb44b3eee74` |
| LCSC-parts-collection.xlsx | `79e7d6dfa1b64d51956d7394c1a4e234f18ea9b1138aa49423adb21d3ff2595b` |

Run from the project directory using the installed KiCad CLI:

```sh
kicad-cli sch erc --format json --severity-all --exit-code-violations -o /tmp/gpio-erc.json "WsprryPico GPIO Shield with GPS.kicad_sch"
kicad-cli pcb drc --format json --severity-all --all-track-errors --exit-code-violations --schematic-parity --refill-zones -o /tmp/gpio-drc.json "WsprryPico GPIO Shield with GPS.kicad_pcb"
```

## Assembly and electrical acceptance

- **Lead and connector fit:** Q61 uses 1.00 mm finished plated holes, 1.50 × 1.60 mm pads and 1.70 mm pitch. The nominal annular ring is 0.25 mm and adjacent pad clearance is 0.20 mm. The maximum specified 0.56 × 0.52 mm lead has a 0.7642 mm diagonal, leaving 0.2358 mm nominal diametral allowance. Form each straight outer lead 0.43 mm outward and confirm finished-hole tolerance. Verify the selected socket leads in 1.00 mm holes, socket height, Pico engagement, U.FL mating and SMA board-edge fit. [Footprint dimensions](LIBRARY-SOURCES.md#transistor)
- **Bias and power:** TP61 is `AMP_5V_SW`; TP62 is `AMP_DRAIN`. Use approximately 5 mV RF-off across L61 as an initial setting, then check warm bias stability, output and device temperature. Verify rail startup/shutdown, effective capacitance, USB supply capacity, GNSS plus active-antenna current, U21 dissipation and amplifier sequencing. [Bias procedure](README.md#adjusting-rv61)
- **Choke and RF path:** measure L61 impedance under representative drain current, then verify power, harmonics, matching, stability and temperature over 2200 m–10 m through the actual external LPF and 50 Ω load. Nominal inductance and current ratings do not establish band coverage. Each ideal 100 nF coupling capacitor has about 11.73 Ω reactance at 135.7 kHz; verify assembled LF loss and RF voltage.
- **Grounding and shielding:** the board has 83 GND vias and a B.Cu ground plane beneath F.Cu signal routing. Preserve antenna keepouts, ground returns and RF-route geometry. Measure GNSS desensitization during amplifier transmission and Pico/Wi-Fi activity; pours, module shielding and the shielded choke do not establish measured isolation.
- **GNSS and frequency correction:** confirm active-antenna supply compatibility, fix/PPS validity, firmware capture/counting and independent RF-frequency validation. UTC timing alone does not calibrate the RF clock.
- **Fabrication:** confirm the manufacturer's actual stackup before treating the RF geometry as 50 Ω. Generate BOM, positions and fabrication files from the final saved design and check supplier allocation, exclusions, polarity and orientation. [Parts and assembly records](PARTS.md)

Acceptance results need the exact board revision, assembly, supply, firmware, band, LPF, load and measurement setup. Refill copper and repeat ERC/DRC after design changes.
