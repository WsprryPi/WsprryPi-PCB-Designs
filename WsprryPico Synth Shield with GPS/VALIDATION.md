# WsprryPico Synth Shield with GPS validation status

Current source verification uses **KiCad 10.0.6** on **2026-10-11**, with all configured severities and schematic parity enabled. DRC refills zones in memory without saving the board. Checks before and after the project rename give identical results; schematic and PCB content differ only in project-name references, and the rendered board geometry is unchanged.

| Check | Result |
| --- | --- |
| Schematic ERC | **0 findings** |
| Physical PCB DRC | **0 violations** |
| Unconnected items | **0** |
| Schematic/PCB parity | **0** |
| Component inventory | 48 non-power schematic symbols; 46 PCB footprints; 47 engineering inventory entries excluding U11 |
| SMT assembly | 40 included positions |
| Local libraries | 20 used symbol definitions; all 19 assigned footprint types present; 9 assigned local models and installed standard model paths resolve |
| Supplier metadata | 31 capacitor/resistor/trimmer references checked against catalog specifications; schematic, PCB, workbook and inventory agree |

All active schematic symbols resolve to local library definitions. Footprint pad geometry, drills, mask settings and model transforms match the placed board instances. Board-specific ground-pad zone connections and teardrops are instance overrides.

The [parts collection workbook](LCSC-parts-collection.xlsx) provides the reviewed ordering fields. The native schematic netlist export contains matching manufacturer, MPN and LCSC codes for all 31 reviewed references. Supplier-field updates preserve component values, electrical pins and wires, assembly exclusions, pad geometry, placement and routing. Catalog and package checks do not establish assembled-board electrical or RF performance.

The ERC profile ignores `footprint_filter`, `four_way_junction`, `simulation_model_issue` and `single_global_label`. It has no individual ERC exclusions. The reported zero applies to that configured profile.

## Checked source identity

The results above apply to these saved source files, using this project's local libraries and configured rules:

| File | SHA-256 |
| --- | --- |
| WsprryPico Synth Shield with GPS.kicad_sch | `5917c2492fbcfe52df0ac9f9739ee5cfe22362249a89e3c1f5129c65bf2dd984` |
| WsprryPico Synth Shield with GPS.kicad_pcb | `8c4d92db480f536d5b2b2779f8191b80889fa146fcda88dfe00260043905aa4f` |
| WsprryPico Synth Shield with GPS.kicad_pro | `78e6ea8b6987e816781a35499fc6e43c1efa8a0afdba9267eec084e783fe0d4a` |
| WsprryPico Synth Shield with GPS.kicad_dru | `31cf30504736a1dab394ca73ff13c8c4575e2c55b485f6fd1219cab8a9ad4818` |
| wsprrypico-synth-shield.kicad_sym | `051ee3cf3ac254be9cc9e7e42f7fc70ada7fd9b2816a6c9415e33a6a9f070eea` |

## Outstanding findings

Native ERC, physical DRC, connectivity and schematic parity report no findings under the configured rules.

TP61 is assigned to `AMP_5V_SW`; TP62 to `AMP_DRAIN`. These are the two sides of L61. The [RV61 setup procedure](README.md#adjusting-rv61) uses a 5 mV initial RF-off drop rather than a universal gate-voltage target.

## Assembly and RF acceptance

The saved design provides the hardware connections described in the [README](README.md). An assembled shield has no recorded electrical, thermal or RF qualification. Acceptance requires:

- Effective bypass capacitance, rail startup/noise, combined LDO and active-antenna current, and operating temperature.
- Loaded TCXO/XA amplitude, synthesizer configuration and frequency transitions, and I²C rise time.
- Bias stability, choke impedance under current, output power and harmonics through the actual external LPF/load across 2200 m–10 m.
- GNSS fix/PPS validity, antenna compatibility and transmitter coexistence; firmware counting and correction behavior.
- Actual socket, connector and component fit, plus manufacturing BOM/position matching.

Rule checks establish saved-source connectivity and geometry within the configured rules. They do not establish measured RF performance, fabricated impedance or assembly fit. Refill copper and rerun ERC/DRC after design changes; generate manufacturing files from the final saved design.
