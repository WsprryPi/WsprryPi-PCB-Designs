# QRP Labs module electrical models

Editable KiCad models of the separately photographed **QRP Labs 25 MHz TCXO daughterboard** and **2023 Rev6 synthesizer module**. Open [QRP Labs Modules.kicad_pro](QRP%20Labs%20Modules.kicad_pro). The three-sheet [schematic](QRP%20Labs%20Modules.kicad_sch) contains the intended module interconnection, the Rev6 synthesizer circuit, and the TCXO circuit model.

This is a schematic-only documentation project. It has no PCB, footprint assignments, fabrication package, selected replacement parts, or measured electrical/RF qualification. The TCXO internal detail is explicitly photo-inferred. The root sheet shows the documented intended assembly of the two boards; the photos show them separately and do not establish completed mounting joints.

## Relation to the Pico synth shield

The companion [WsprryPico Synth Shield](../WsprryPico%20Synth%20Shield/README.md) selects KDS/Daishinku DSB321SDN **1XTW25000MAA, 25 MHz, C253672**, and **Si5351A** for its proposed circuit. This project records the photographed Rev6 **MS5351M** hardware. Its functional TCXO symbol describes the photographed module without assigning an unverified factory package identity; the selected KDS part itself has documented pins 1/2 GND, 3 OUT and 4 VCC. Its specification is consistent with the observed marking.

See the [chat reconciliation and remaining decisions](../WsprryPico%20Synth%20Shield/RECONCILIATION.md). The shield's proposed 10 nF supply bypass and 1 nF coupling values come from the KDS measurement circuit; they do not resolve this model's unknown C101/C102 values. The circuit sources and PDFs remain unchanged.

## Files

| File | Purpose |
| --- | --- |
| [QRP Labs Modules.kicad_pro](QRP%20Labs%20Modules.kicad_pro) | Project settings, ERC severities and empty exclusions |
| [QRP Labs Modules.kicad_sch](QRP%20Labs%20Modules.kicad_sch) | Sheet 1: power, I2C, clock outputs and three-wire TCXO interconnection |
| [Synth Rev6.kicad_sch](Synth%20Rev6.kicad_sch) | Sheet 2: populated Rev6 circuit and module/edge-pad interface |
| [TCXO 25MHz.kicad_sch](TCXO%2025MHz.kicad_sch) | Sheet 3: functional oscillator, photo-inferred capacitors and documented interface |
| [QRP Labs Modules.pdf](QRP%20Labs%20Modules.pdf) | Complete three-page reference export |
| [Synth Rev6.pdf](Synth%20Rev6.pdf) | Individual synthesizer reference export |
| [TCXO 25MHz.pdf](TCXO%2025MHz.pdf) | Individual TCXO reference export |
| [qrp-labs-models.kicad_sym](qrp-labs-models.kicad_sym) | Independent project-local symbols |
| [sym-lib-table](sym-lib-table) | `${KIPRJMOD}` library registration |
| [KiCad library terms](KICAD-LIBRARY-LICENSE.md) | Terms for copied and modified KiCad symbols |

Keep this folder together. It has no symbol-library dependencies on other repository projects and no machine-specific library paths. Saved schematic format is KiCad 10.0; creation and validation used **KiCad 10.0.6**. Reports, the exported XML netlist, source hashes, and raster previews are disposable outputs in ignored `generated/`. The three PDFs above are intentional reference artifacts.

## Photographed population and Rev6 changes

Photo identifiers are recorded for provenance; the personal photos and temporary conversions are not stored in this project or Git.

| Item | Evidence and representation |
| --- | --- |
| Synth board revision | `IMG_1703` shows `QRP Labs 2023 Rev6` and an older `Rev. 5` legend inside the retained crystal area. The Rev6 circuit is modeled. |
| IC1 | Photo marking **MS5351M** confirmed. The Ruimeng MSOP-10 datasheet supplies the pin map, including VDDO on pin 7. |
| IC2 | Photo marking **78M33** confirmed. A fixed 3.3 V regulator replaces the historical LM317; R5/R6 are absent. Model pins are 1 = input, 2 = GND/tab, 3 = output, using the 78Mxx TO-252 functional mapping. The actual maker/order code is unresolved. |
| Q1/Q2 | BSS123 per the Rev6 manual; SOT-23 population visible in the photo. Pins 1/2/3 = gate/source/drain. No manufacturer is inferred from the photograph. |
| R1-R4 | Four fitted pull-ups. The schematic uses the manual's 1 kOhm values, tagged `(doc)`; these are not resistance measurements. |
| C1/C2 | Fitted bypass capacitors, 100 nF each per the manual circuit. Values are tagged `(doc)` and have not been measured. |
| C4 | Fitted near the regulator. Rev6 track drawing connects it between regulated 3.3 V and GND. Its value remains **Unknown**. |
| C3 | Through-hole VDD/GND capacitor pads are empty in the photo. No fitted C3 is added to the electrical model. |
| Reference options | The 27 MHz crystal and direct-mounted four-pad TCXO positions are empty. The separate 25 MHz daughterboard is the intended reference; alternate oscillators are not added to the populated circuit. |
| Module/clock connections | Both 10-pad rows and all three SMA pad groups are modeled. Header and SMA connector hardware is absent from the photo. |
| Gate repair | The photo shows a wire joining Q1 and Q2 gates. This agrees with QRP Labs' documented Rev6 missing-Q1-gate-trace repair. `W1` models the fitted wire, not an additional resistor or a known shipment date. |
| TCXO daughterboard | `IMG_1702` shows `25.00BN / D441`; `IMG_1705` provides the clearer trace/capacitor view. Both C101/C102 are fitted. The oscillator is modeled by function, without assigning its unknown physical package pin numbers. |

`J1` is an assigned model reference for the whole 20-pad module interface; its **pin numbers match QRP Labs' module numbering**. `J3/J4/J5` are assigned model references for CLK0/CLK1/CLK2 edge-pad groups; their pin 1 = signal and pins 2/3 = ground are model identifiers, not a selected SMA part's footprint numbering. `Y101` and `W1` are also assigned references. C101/C102, IC1/IC2, Q1/Q2, and R1-R4 retain the photographed/documented designators.

`A1` and `A2` are schematic-only external boundaries, excluded from the BOM and board. A1 expresses external 5 V, ground, a separately supplied I2C high-side voltage, and the host's I2C drive. A2 expresses accessible clock output connections. Neither is a component on a photographed board. These boundary pin types allow ERC to check the intended complete connection model; they do not prove a real host is connected, powered, or compatible.

## Synthesizer module pinout

Numbering follows the manual, not an odd/even 2x10 connector convention. In the component-side orientation shown in `IMG_1703` (regulator on the left, MS5351M on the right), the top row runs **10 to 1 from left to right**, and the bottom row runs **11 to 20 from left to right**. The two rows have 2.54 mm pin pitch. All listed GND pads are interconnected.

| Pin | Function | Pin | Function |
| --- | --- | --- | --- |
| 1 | GND | 20 | CLK1 |
| 2 | NC | 19 | CLK2 |
| 3 | GND | 18 | Regulated 3.3 V |
| 4 | GND | 17 | CLK0 |
| 5 | GND | 16 | GND |
| 6 | GND | 15 | GND |
| 7 | GND | 14 | High-side I2C SDA |
| 8 | 5 V input | 13 | High-side I2C SCL |
| 9 | 5 V input | 12 | GND |
| 10 | 5 V input | 11 | High-side I2C pull-up supply (`I2C_VIO`) |

Pins **8/9/10 are joined**. Pin **11 is separate** and feeds only R1/R2's high-side pull-ups; the schematic does not tie it internally to 5 V. Pin **18** is the regulator's output. The manual's older-Ultimate3 instruction to remove header pin 12 concerns the mating host; pin 12 remains grounded on this board model.

The level shifters use Q1 for SDA and Q2 for SCL. Their sources connect to the IC-side bus with R3/R4 pull-ups to 3.3 V. Their drains connect to the host-side bus with R1/R2 pull-ups to pin 11. Q2 gate connects directly to 3.3 V; Q1 gate reaches it through the photographed W1 repair wire. W1's two ends appear as separate netlist nodes separated by the explicit wire component; electrically the fitted wire joins them.

IC1 pins are: 1 VDD, 2 XA, 3 XB, 4 SCL, 5 SDA, 6 CLK2, 7 VDDO, 8 GND, 9 CLK1, 10 CLK0. XB is unused in the selected external-reference configuration; the omitted crystal position would connect XA/XB.

## TCXO interconnection and uncertainty

The QRP Labs interface is documented as **GND / VDD (3.3 V) / OUT (25 MHz)**. The board measures 14.8 x 10.5 mm and has the window seen in the photo. For installation on the synthesizer, connect VDD to its regulated 3.3 V net, GND to common ground, and OUT to the XA crystal-input node at **IC1 pin 2**. Omit the 27 MHz crystal and configure the reference frequency as **25,000,000 Hz**, including when using GPS discipline.

The internal drawing uses visible traces to infer **C101 across VDD/GND** and **C102 in series between the oscillator's raw output and the module OUT pad**. That inference is identified on the sheet and in symbol `Evidence` fields; it has not been established by a continuity measurement or an official daughterboard circuit diagram. The model does not assign hidden package wiring or an enable/trim function to the fourth oscillator pad.

Remaining items are bounded:

- **C101, C102 and C4 values:** not specified by the checked QRP sources or readable from the unmarked capacitors. All remain `Unknown`.
- **TCXO internal connectivity:** confirm the C101/C102 inference by unpowered continuity tracing before using this internal drawing to reproduce hardware.
- **TCXO identity/pins:** `25.00BN / D441` does not establish a manufacturer/order code, physical pin numbering, fourth-pad function, output waveform, amplitude, or loading requirements. Y101 therefore uses semantic functional pin identifiers and has no footprint.
- **Regulator identity:** the observed `78M33` establishes the documented function, but not a manufacturer-specific guaranteed operating envelope or an exact ordering code. The TI source is a functional pin-map reference, not identification of the photographed part.

Capacitor values, hidden package connections and manufacturer identities were not guessed to complete a manufacturing design. No measured stability, output power, drive-level, thermal, or RF performance claim is made by these models.

## Validation recorded on 2026-10-06

| Check | Result |
| --- | --- |
| KiCad version | 10.0.6, installed macOS CLI |
| Hierarchy and XML netlist | Three sheets, 21 symbol instances, 16 nets including two intentional no-connect nets |
| Connectivity audit | Exact comparison of every net's pin membership against a separately enumerated expected connection map; all groups match |
| Audited interfaces | All 20 module pins, IC1/IC2 pin maps, each level-shifter G/S/D, pull-ups, W1, bypass capacitors, three clock pad groups and the TCXO reference/supply/ground path |
| ERC | **0 errors / 12 warnings**. Every warning is `footprint_filter` for an unassigned physical footprint; no electrical connectivity findings remain. |
| ERC exclusions/ignored checks | **None.** The four checks normally ignored by KiCad defaults were enabled as warnings. No check was weakened to clear a finding. |
| Warning references | R1/R2/R3/R4, Q1/Q2, IC2, C1/C2/C4/C101/C102. Footprints were deliberately left unassigned for this schematic-only task. |
| PDF review | Complete export and individual board exports produced; all three pages rendered and visually inspected after the final layout corrections |
| DRC | Not applicable: no PCB was created or changed by this work |
| Physical verification | Not performed; photo-inferred TCXO detail and exact part identities remain open as listed above |

ERC's `--exit-code-violations` mode returns a nonzero result for the retained footprint warnings. These are not silently excluded. Library symbols, hierarchy, disconnected endpoints, off-grid connections and net-name conflicts were checked. All symbols have simulation excluded because no behavioral/SPICE model is supplied; this is not a simulation project. KiCad emitted a Fontconfig cache-version warning while exporting; the rendered pages were checked and remained readable.

To reproduce the saved-source checks from this folder with the installed CLI:

```bash
KICAD_CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
mkdir -p generated
"$KICAD_CLI" sch erc --severity-all --exit-code-violations \
  -o generated/erc.rpt 'QRP Labs Modules.kicad_sch'
"$KICAD_CLI" sch export netlist --format kicadxml \
  -o generated/connectivity.xml 'QRP Labs Modules.kicad_sch'
"$KICAD_CLI" sch export pdf \
  -o 'QRP Labs Modules.pdf' 'QRP Labs Modules.kicad_sch'
"$KICAD_CLI" sch export pdf --pages 2 \
  -o 'Synth Rev6.pdf' 'QRP Labs Modules.kicad_sch'
"$KICAD_CLI" sch export pdf --pages 3 \
  -o 'TCXO 25MHz.pdf' 'QRP Labs Modules.kicad_sch'
```

Regenerate and inspect the PDFs after source edits; a reference PDF alone does not establish current-source validity. The initial work was created on repository branch `main` without staging, committing or pushing. Concurrent shield-project changes are outside this work's scope.

## Sources and attribution

Checked on 2026-10-06:

- [QRP Labs synthesizer product/documentation page](https://qrp-labs.com/synth.html): board dimensions, revisions and primary source links.
- [QRP Labs Rev6 assembly manual](https://www.qrp-labs.com/images/synth/synth_assembly6.pdf), document update 29-Nov-2023: p1 full header pinout; p2 circuit, values and explicit MS5351M/78M33/BSS123 updates; pp3-4 population, orientation and tracks; pp5-6 daughterboard installation. The circuit diagram credits **John VK6Y** and carries **QRP Labs 2014** copyright; the photographed board carries **QRP Labs 2023**.
- [QRP Labs Rev6 PCB repair](https://qrp-labs.com/synth/rev6fix.html), 03-Feb-2025: missing Q1 gate trace and repair destinations. Used with the visible gate-to-gate wire, without inferring the shipment date or who fitted it.
- [QRP Labs 25 MHz TCXO product page](https://shop.qrp-labs.com/tcxo): module size, two capacitors and the three functional connections. It does not supply capacitor values or the exact oscillator package identity.
- [Ruimeng MS5351M datasheet hosted by QRP Labs](https://qrp-labs.com/images/synth/ms5351m.pdf), V1.0 2021-03-08, p3: manufacturer pin-function table. Linked from [QRP Labs' MS5351M page](https://qrp-labs.com/synth/ms5351m.html).
- [Nexperia BSS123 datasheet](https://assets.nexperia.com/documents/data-sheet/BSS123.pdf), p1: gate/source/drain numbering. This is a pin-map reference, not the photographed MOSFET manufacturer's identification.
- [TI UA78M datasheet](https://www.ti.com/lit/ds/symlink/ua78m.pdf), SLVS059V, p3: TO-252 input/common/output mapping. Used only for the generic 78M33 functional mapping.
- User-provided `IMG_1702`, `IMG_1703` and `IMG_1705`: actual population, revision/part markings, jumper and visible TCXO traces. Personal image contents are not redistributed.

This is an independent redraw of documented electrical connections and visible population, not an official QRP Labs CAD release. The QRP Labs manual artwork and personal photographs were not copied into the project; no QRP Labs source license was established, and their material is not represented as repository-owned MIT work. Original project documentation/custom symbol work follows the repository [MIT license](../LICENSE.md).

Local symbols `R` and `C` come from KiCad 10.0.6 `Device`; `BSS123` is flattened from `Transistor_FET:BSS123` and its `Q_NMOS_GSD` parent; `78M33_Functional` modifies `Regulator_Linear:LM78M05_TO252` for the fixed 3.3 V functional model. Their KiCad copyright/license attribution and CC-BY-SA 4.0 design exception are retained in [KICAD-LIBRARY-LICENSE.md](KICAD-LIBRARY-LICENSE.md). New MS5351M, functional TCXO, module-pad, wire and external-boundary symbols were drawn for this project. No footprints or 3D models were imported.
