# Project libraries

This folder contains the project's symbol library, footprint library, and available 3D models. Library tables use `${KIPRJMOD}` paths; no sibling project folder is required. Open the project with KiCad 10.0.1 or newer to edit the local library assets.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/Wsprry-Pi.kicad_sym) | 27 symbols, including all definitions used by the schematic and the amplifier parts below |
| Footprints | [Footprint library](footprints/Wsprry-Pi.pretty/) | 37 footprints, including all footprints used by the board and the amplifier packages below |
| Models | [3D models](3dmodels/) | 26 local STEP files |

The registered library nickname is `Wsprry Pi`. Instance values and purchasing fields remain the design's responsibility; a generic library symbol does not select a component value or supplier part.

The schematic and PCB use only the `Wsprry Pi` library nickname for placed
symbols and assigned footprints. Project-local copies include the standard
`+3V3`, `+5V`, `C_Small`, `Conn_01x03`, `BLM21PG221SN1D`, and `TestPoint` symbols;
the 0402, 0603, and 1206 passive footprints; the 1.00 mm three-pin header; and
the 1.0 mm single-pad test point. The 0805 ferrite, 1206 capacitor, 1206
inductor, 1206 resistor, and 1.00 mm header footprints reference their
project-local KiCad STEP models. The bare test-point pad has no 3D model.

## SMA connectors

[SMA_Adafruit_1865_EdgeMount](footprints/Wsprry-Pi.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod) is the same edge-launch footprint used by the Pico 2W Wattmeter Shield and is placed as J83 on this board. Select `Wsprry Pi:SMA_Adafruit_1865` for the matching symbol. Pin 1 is signal and pin 2 is ground. The part is an Adafruit 1865 standard-polarity female SMA connector for a 1.6 mm board, fitted by hand with no paste apertures. Its symbol and footprint are excluded from the assembly BOM, and its footprint is excluded from position files.

The footprint origin is the board seating edge on the signal centerline. Copper extends 0.500–4.064 mm into the board. Place the origin at the board edge and check physical fit against the [Adafruit connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf). It has no attached 3D model.

## Model limits

The project library includes unplaced assets for the proposed amplifier input:

- `C689467` is Analog Devices `LTC6752HS5#TRMPBF`. Its local symbol follows the
  manufacturer's TSOT-23-5 pinout, and `TSOT-23-5` plus its STEP model are
  project-local copies of the KiCad library assets. See the
  [Analog Devices datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/6752fc.pdf).
- `C42400210` is ElecSuper `PESD3V6Z1BCSF(ES)`. Its bidirectional TVS symbol
  identifies the exact MPN and LCSC number. The
  `DFN0603-2L_L0.62-W0.32-P0.40` footprint implements the 0.40 mm-pitch,
  0.25 mm by 0.32 mm pad recommendation in the manufacturer's Rev 1.2
  [datasheet](https://www.lcsc.com/datasheet/C42400210.pdf). Its supplier STEP
  model is stored locally.

These assets are not placed on the schematic or board. The DFN0603-2L package
is exceptionally small; verify stencil capability, assembly yield, model
alignment, and physical fit before production. The STEP models are
visualization aids, not physical-fit evidence.

The project library also includes the proposed wideband PA device:

- `C2058688` is Texas Instruments `THS3491IRGTR`. The local symbol implements
  the RGT0016C VQFN-16 pinout, including the dedicated `FB`, `TJ_SENSE`, two
  `VOUT`, two `+VS`, two `-VS`, and exposed-pad connections. The footprint uses
  TI's 0.24 mm by 0.60 mm perimeter lands, 1.68 mm exposed pad, 1.55 mm paste
  aperture, and four 0.20 mm thermal vias. See the
  [TI datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf) and
  [LCSC listing](https://www.lcsc.com/product-detail/C2058688.html).

The thermal vias follow TI's example. TI recommends that vias beneath paste be
filled, plugged, or tented; confirm the board fabricator and assembler's
capabilities before release. The supplier STEP model is stored locally as a
visualization aid and has not been validated against an assembled component.

The proposed PA supply filters use Murata `BLM21PG221SN1D` (`C85840`) ferrite
beads. The exact local symbol records the 220 ohm at 100 MHz impedance, 2 A
current rating, 45 milliohm maximum DCR, MPN, and supplier number. Its
`L_0805_2012Metric` footprint and STEP model are project-local copies of the
KiCad library assets. See the
[LCSC listing](https://www.lcsc.com/product-detail/C85840.html). The STEP model
is a generic 0805 inductor visualization and is not physical-fit evidence.

The proposed bipolar DC/DC converter assets are also project-local and are not
yet placed on the schematic or board:

- U61 is Texas Instruments `TPS65131RGER` (`C87663`). Its symbol follows the
  TPS65131 RGE0024B pinout, including exposed pad 25. The local
  `VQFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm_ThermalVias` footprint follows TI's
  0.25 mm by 0.60 mm perimeter lands, 2.45 mm exposed pad, and optional
  0.20 mm thermal-via locations. See the
  [TI datasheet](https://www.ti.com/lit/ds/symlink/tps65131.pdf) and
  [LCSC listing](https://www.lcsc.com/product-detail/C87663.html).
- L61 and L62 use the same TDK `B82462G4472M000` (`C2041780`) symbol and
  `L_6.3x6.3_H3` footprint: 4.7 uH, +/-20%, 2 A temperature-rise current,
  40 milliohm maximum DCR, and a 6.3 mm by 6.3 mm by 3.0 mm package. See the
  [TDK product page](https://product.tdk.com/en/search/inductor/inductor/smd/info?part_no=B82462G4472M000)
  and [LCSC listing](https://www.lcsc.com/product-detail/C2041780.html).
- D61 and D62 use the same Nexperia `PMEG3020EP,115` (`C513108`) symbol and
  `D_SOD-128` footprint. Pin 1 is cathode and pin 2 is anode. See the
  [Nexperia datasheet](https://assets.nexperia.com/documents/data-sheet/PMEG3020EP.pdf)
  and [LCSC listing](https://www.lcsc.com/product-detail/C513108.html).
- C63 and C64 use the same Samsung Electro-Mechanics `CL32B226KAJNNNE`
  (`C309062`) symbol and `C_1210_3225Metric` footprint: 22 uF, +/-10%, 25 V,
  X7R, 1210. See the
  [Samsung product page](https://product.samsungsem.com/mlcc/CL32B226KAJNNN.do)
  and [LCSC listing](https://www.lcsc.com/product-detail/C309062.html).

The SOD-128 and 1210 STEP models are generic KiCad package visualizations. The
VQFN model is a same-body-size TI RGE0024 visualization whose hidden exposed
pad differs from the TPS65131 land pattern, and the inductor model is a similar
6 mm-class, 3 mm-height visualization. Use the footprints and manufacturer
drawings, not these two approximate models, for physical-fit decisions.

The proposed Pi-header power switch is Texas Instruments `TPS2553DBVR`
(`C55266`). Its local symbol follows the DBV0006A pinout: pin 1 `IN`, pin 2
`GND`, pin 3 `EN`, pin 4 active-low open-drain `FAULT`, pin 5 `ILIM`, and pin 6
`OUT`. The `SOT-23-6_TI-DBV0006A` footprint implements TI's example board
layout with 1.10 mm by 0.60 mm lands, 0.95 mm pitch, and 2.60 mm pad-row
spacing. See the [TI datasheet](https://www.ti.com/lit/ds/symlink/tps2553.pdf)
and [LCSC listing](https://www.lcsc.com/product-detail/C55266.html). The local
STEP model is the generic KiCad SOT-23-6 visualization and is not physical-fit
evidence. These assets are not yet placed on the schematic or board.

The optional `CAP-TH_L17.5-W11.1-P7.50-D0.8` footprint references an unavailable `EASYEDA_MODELS/CAP-TH_L17.5-W11.1-P7.50-D0.8.step` file. That footprint is not placed on this board.

The C11 footprint references the local [CP_Elec_6.3x5.8 STEP model](3dmodels/Capacitor_SMD.3dshapes/CP_Elec_6.3x5.8.step), copied from the KiCad 3D model library. It represents the nominal 6.3 mm diameter by 5.8 mm package of the selected 47 µF capacitor, but it is a generic visualization and has not been validated against an assembled board.

The switch and through-hole SMA models correspond to [C318884](https://www.lcsc.com/product-detail/C318884.html) and [C496551](https://www.lcsc.com/product-detail/C496551.html). Verify model alignment and physical fit before using the 3D view for mechanical design.

See the [project README](../README.md) for assembly requirements and ERC/DRC findings.

## Sources and licenses

Standard symbols, footprints, and STEP models derive from KiCad libraries. Local footprints include project-specific geometry. Part names and descriptions identify their original library families. Copyright KiCad Library Contributors; [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/) applies to those assets.

The Adafruit land pattern derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). Its description retains attribution. Its matching coaxial symbol derives from KiCad's `Conn_Coaxial_Small` symbol under the KiCad library license.

The custom BWSMA-KWE-Z001, EEEFK1V470P, TS-1187A-B-A-B,
LTC6752HS5#TRMPBF, PESD3V6Z1BCSF(ES), THS3491IRGTR, BLM21PG221SN1D,
TPS65131RGER, B82462G4472M000, PMEG3020EP,115, CL32B226KAJNNNE, and
TPS2553DBVR symbols include supplier metadata and
datasheet links. The LTC6752 symbol and TSOT-23-5 package assets derive from the
KiCad libraries and the Analog Devices datasheet. The PESD3V6Z1BCSF(ES) symbol
derives from KiCad's bidirectional TVS symbol, and its footprint dimensions
come from the ElecSuper datasheet. The THS3491IRGTR symbol pinout and footprint
dimensions come from the TI datasheet. The BLM21PG221SN1D symbol metadata comes
from the Murata datasheet and its LCSC listing; its footprint and model derive
from the KiCad libraries. The TPS65131RGER symbol pinout and VQFN footprint
derive from the KiCad libraries and TI datasheet; the B82462G4472M000,
PMEG3020EP,115, and CL32B226KAJNNNE symbols combine standard KiCad graphics with
the manufacturers' electrical and package data. Their footprints and STEP
visualizations derive from the KiCad libraries as qualified above. The
TPS2553DBVR symbol pinout and `SOT-23-6_TI-DBV0006A` land pattern derive from
the TI datasheet; its STEP visualization derives from the KiCad library.
Switch, through-hole SMA,
PESD3V6Z1BCSF(ES), and THS3491IRGTR STEP assets are supplied by EasyEDA/LCSC
for the identified part numbers. Supplier attribution and embedded notices
apply to those models.

The repository MIT license does not replace third-party license terms.
