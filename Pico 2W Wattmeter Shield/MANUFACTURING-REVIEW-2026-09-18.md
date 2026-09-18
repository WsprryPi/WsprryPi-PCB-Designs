# Pico 2W Wattmeter Shield manufacturing review

Reviewed 2026-09-18 with KiCad **10.0.1**. This is a review of the saved working
tree, not a released or physically qualified board. No design assets were changed.
The requested assembly scope excludes the SMA connector and Pico sockets/module.

The board has no reported DRC or connectivity violations. Resolve the assembly
export issues below and agree the exposed-pad via process before ordering.
No major routing rearrangement is indicated by this review.

## Follow-up

The authorized CAD fixes are recorded in
[manufacturing changes](MANUFACTURING-CHANGES-2026-09-18.md).
The findings and measurements below describe the original review snapshot.
The user subsequently specified an unamplified WsprryPi GPIO clock source,
2-16 mA drive settings, and 2200 m-2 m coverage; see [input range](INPUT-RANGE.md).

## Findings

### 1. U1 disappears from an SMD-only placement export — fix before assembly

Both the placed U1 footprint and its local library footprint lack `(attr smd)`.
An ordinary position export contains U1; an otherwise identical export with
`--smd-only` omits it. This can leave the ADL5904 in the BOM but absent from the
machine placement file. DRC does not report it.

Set the fabrication type to **SMD** in both the board footprint and
`pico-wattmeter.pretty/QFN-16_L3.0-W3.0-P0.50-TL-EP1.8.kicad_mod`.
Regenerate the placement file and confirm U1 and U2, including pin-1 orientation,
in the assembler's placement preview. The custom footprint's zero rotation is
not a guarantee of the assembler's library rotation convention.

Evidence: `generated/full-review-2026-09-18/pos.csv` versus
`generated/full-review-2026-09-18/pos-smd-only.csv`.
[KiCad documents this SMD-attribute filter](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#component_placement_files).

### 2. The intended connector exclusions are not yet encoded

The native schematic BOM currently includes **J1, J2, and J3**. The placement
export includes **J1**. U3 already has BOM and position exclusions, and J2/J3 are
schematic-only socket procurement symbols. Excluding U3 does not exclude J2/J3.

For the requested assembly scope:

- Exclude J1, J2, and J3 from the schematic BOM.
- Exclude the placed J1 footprint from position files and from the PCB BOM.
- Retain U3's existing exclusions.
- Keep J1 and the U3 header footprint physically on the board; exclusion is an
  assembly/procurement attribute, not removal of their pads or holes.

The resulting populated component set should be **C1–C9, R1–R8, U1, U2: 19
components**, all on the front. Cross-check that same reference set in the final
BOM and placement file.

There is a related export trap: the saved **Shield purchasing BOM** preset does
not include the `LCSC` field. Manufacturer and MPN are blank for the 19 electronic
components, so this preset discards their exact supplier identifiers. The current
general BOM settings do include LCSC. Add LCSC to the preset actually used for
ordering, or populate and export manufacturer/MPN. C9's `0.1µF` is electrically
the same value as the other `100nF` parts with C60474; differing strings simply
split otherwise identical BOM groups.

Evidence: `bom.csv`, `bom-preset.csv`, and `pos.csv` in the review-output directory.
The existing socket documentation and schematic note still describe J2/J3 as BOM
items; update them when applying the exclusions.

### 3. Via filling/capping is now selected, but must reach the fabricator

The current board correctly marks **exactly five vias** beneath U1 with
`filling yes`, `capping yes`, and front/back tenting disabled. All five remain
GND, with 0.30 mm drills and 0.60 mm copper diameters. Their centers follow U1's
updated position:

| Location | Board X (mm) | Board Y (mm) |
| --- | ---: | ---: |
| Center | 133.081114 | 89.499999 |
| Left | 132.481114 | 89.499999 |
| Right | 133.681114 | 89.499999 |
| Top | 133.081114 | 88.899999 |
| Bottom | 133.081114 | 90.099999 |

The review Gerber/Excellon export contains the holes and mask openings, but does
not contain the User.Comments fabrication reminder or a selective fill/cap
instruction. There are **17 total 0.30 mm vias**, so an instruction to fill every
0.30 mm hole would include twelve unintended vias.

Supply a drawing identifying these five holes and the epoxy-fill, planarize,
copper-cap requirement, alongside the appropriate order option. Confirm that
the selected two-layer fabrication service accepts this selective process.
[JLCPCB explicitly requests a note or image identifying epoxy-filled vias](https://jlcpcb.com/help/article/pcb-via-covering).
Do not treat a CAD selection as confirmation that the ordered process includes it.

The solder paste geometry is intact: four 0.65 × 0.65 mm square apertures at
local coordinates (±0.55, ±0.55), totaling 1.69 mm², or 52.16% of the 1.8 mm square
PCB paddle. Gerber inspection found four corresponding flashes and no filled
region crossing the center paddle. The copper paddle remains continuous.
Retain these windows when the assembler generates the stencil.

`U1-PASTE-WINDOWS.md` now needs a current-state addendum: it still describes
unfilled vias with unchanged tenting. Its original validation can remain as a
dated historical record, but should not be mistaken for the current via process.

### 4. ERC still has a ground power-drive error

ERC reports one error: `power_pin_not_driven`, U1 pin 11 GND. The exported netlist
and passing DRC establish that U1 pins 11 and 17, U2 ground, and the Pico ground
pins are connected to the GND net. That net contains no power-output pin.

This is a schematic power-source declaration issue, not evidence of an open
ground trace. Add a `PWR_FLAG` to the externally supplied GND net and rerun ERC;
do not suppress the rule or change the ADL5904 pin type to hide the finding.
The 3.3 V net already has U3 pin 36 typed as a power output.

### 5. Record the input power limit before calling this a wattmeter

The saved descriptions rate R1/R3 at 125 mW and R2 at 125 mW. For an ideal
97.6 Ω / 71.5 Ω / 97.6 Ω pi attenuator terminated in 50 Ω, with C1/C2 treated
as RF shorts, the calculated input resistance is 50.481 Ω and R1 dissipates
51.72% of delivered input power. R1 reaches 125 mW at approximately **0.242 W
input (+23.8 dBm), before temperature/reliability derating**. At 1 W input it
would dissipate approximately 0.517 W.

This is a conditional circuit calculation using the saved ratings, not a
validated operating limit. R1/R3's C2960805 listing could not be independently
retrieved during this review, so confirm the actual purchased part's rating and
derating curve. Define the intended input range and any external coupler or
attenuator before assigning a wattage rating to the assembled board.

The ADL5904 nominal measurement range and RF response also require calibration
of the complete input network; the IC's frequency specification does not qualify
this layout. The RF traces are predominantly 0.20 mm wide on a 1.6 mm two-layer
board, with short discontinuities through pads/components. No controlled-
impedance stackup or RF measurement was supplied. This is a performance
qualification item, not a demonstrated manufacturing defect.

### 6. Silkscreen and hand assembly deserve minor cleanup

All 21 reference designators are hidden. There is no visible board revision or
clear text identifying the Pico orientation. Provide an assembly drawing with
references and add a small board ID/revision and orientation marking where space
allows. This will make inspection, manual connector installation, and rework less
error-prone.

The board contains 41 silkscreen graphics at 0.12 mm stroke and three at 0.10 mm.
The saved rules permit zero silk-to-pad clearance and 0.08 mm minimum text stroke.
[JLCPCB's published legend rules specify 0.15 mm minimum line width and
pad-to-silk clearance](https://jlcpcb.com/capabilities/pcb-capabilities).
These small marks can be clipped or poorly reproduced even though the current
DRC passes. Check the final CAM silkscreen against the actual fabricator's rules.

The back ground zone uses solid pad connections, including the eight Pico ground
holes. They will require more soldering heat than isolated pads. For hand-fitted
headers, consider thermal relief overrides on those header ground pads only;
retain the intentional low-impedance connections around the RF circuitry and U1.

Header holes remain 1.00 mm with 1.508 mm square pads, 2.54 mm pitch and
17.78 mm row spacing. Excluding the sockets from the factory BOM is fine, but
their actual lead size, body width, and mating height still need checking against
the parts installed by hand. No socket MPN or assembled clearance model is saved.

### 7. Reproducibility and source-state inconsistencies

- The footprint table still registers an EasyEDA library at an absolute path
  under this Mac's OneDrive Downloads. That file currently exists locally, but
  is not a portable project dependency. All placed custom footprints use the
  project-local `pico-wattmeter` library, so this unused registration can be
  removed after confirming it is no longer needed for editing/imports.
- U1, U3 and J1 have no 3D models. The pin/pad review is not a 3D collision or
  connector-stack fit check. The SMA remains intended for the documented
  Adafruit 1865 and nominal 1.6 mm board; no substitute is automatically qualified.
- Older notes record zero ERC errors and older object counts. The current ERC
  result is one error; current routing is 118 segments and 25 vias. Preserve the
  old results as dated evidence and use this review for the current snapshot.
- The project is still untracked in the repository. Identify a reviewed source
  revision before producing a release manufacturing package.

## Checks completed

| Check | Result |
| --- | --- |
| KiCad version | 10.0.1 |
| DRC, all severities, in-memory zone refill, schematic parity | 0 violations, 0 unconnected pads, 0 footprint/parity errors |
| DRC ignored checks / exclusions | None / none |
| ERC | 1 error, 0 warnings; ground power-drive issue above |
| Existing ERC ignored categories | Single global label, four-way junction, SPICE model issue, footprint-filter mismatch; unchanged |
| Board inventory | 21 footprints, 118 track segments, 25 vias |
| Drill output | 17 × 0.30 mm vias, 8 × 0.40 mm vias, 40 × 1.00 mm component holes |
| U1 paste | Four separate 0.65 mm square windows; no residual central paste region |
| U1 via treatment flags | Exactly five filled/capped vias, all on GND |
| BOM / placement | Exported normal BOM, named-preset BOM, ordinary placement and SMD-only placement; discrepancies above |
| Visual inspection | Complete schematic, front copper/mask/silk, rear copper/mask, outline/notch |

C6 is correctly connected between DECL and CRMS. CRMS now has approximately
2.153 mm of front routing and no vias. The DECL net has approximately 6.768 mm
of total routing, including its R5 branch, with two vias. The back ground fill
remains continuous around the DECL clearance. No further C6 relocation is
justified by this inspection.

The schematic's ADL5904 basic connections agree with the manufacturer's example:
R5/C3 provide the DECL bypass, C6 bridges DECL/CRMS, C7 bypasses VRMS, and C4/C5
are next to supply pin 5. U2 has local C9 bypassing; ADDR is grounded; SDA and
SCL have separate 4.7 kΩ pull-ups to 3.3 V and connect to Pico GP4/GP5. Pico
power is taken from pin 36. No pin-numbering mismatch was found for these
connections. Sources: [ADL5904 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/adl5904.pdf),
[ADS1115 datasheet](https://www.ti.com/lit/ds/symlink/ads1115.pdf),
[Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf).

U2's C468683 identifies ADS1115IDGST in the DGS/VSSOP-10 package. Its KiCad
footprint name contains TSSOP, but the checked dimensions are a 3 mm body,
0.5 mm pitch and 1.45 × 0.30 mm pads, consistent with the DGS package family.
The row-center spacing is 4.30 mm versus 4.40 mm in TI's example land pattern;
this small difference alone is not evidence of a wrong footprint. U1's C206813
identifies ADL5904ACPZN-R7, the 3 mm, 0.5 mm pitch LFCSP package. Exact supplier
identities were checked against [U2's listing](https://www.lcsc.com/product-detail/C468683.html)
and [U1's listing](https://www.lcsc.com/product-detail/C206813.html).

The retrieved capacitor listings match the saved values/packages for C1/C2,
C3/C5/C6/C9, C4, C7 and C8. Retrieved resistor listings match R4, R5, R6 and
R7/R8; R2's assembly listing identifies an 0805 part but did not provide a full
rating table. R1/R3's supplier listing could not be retrieved. This review does
not establish every part's current PCBA stock, full datasheet compliance, or an
approved substitute list. Retain the LCSC identifiers in the final BOM and
review the assembler's actual matched parts.

The antenna opening is a real 14 × 9 mm notch in the outline, with a matching
copper/component keepout. No new outline defect was found. Physical fit, routed
corner radius, socket stack clearance, solder-joint quality, and RF accuracy
remain untested.

## Evidence and preservation

Reports, raw exports, rendered views, and source snapshots are under
`generated/full-review-2026-09-18/` (ignored review output, not a release package).
`source-hashes.json` identifies the 22 reviewed source/documentation assets.
The reviewed PCB SHA-256 is:

`15cd94de60636d5eee3276da9c97e520f0a5a736b7a0c9a7346610328809c9f3`

All snapshotted source hashes remained unchanged through the review. The only
new durable artifact is this report. No schematic, PCB, library, project settings,
or exclusion rules were changed. No commit or push was performed.
