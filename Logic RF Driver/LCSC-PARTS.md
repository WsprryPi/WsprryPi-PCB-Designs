# Parts and procurement

All sixteen BOM positions have selected manufacturer ordering codes. Fourteen positions are JLCPCB Basic parts; U1 and D1 are Extended. J1/J2/J3 are excluded from the BOM. The inventory figures below are JLCPCB assembly stock, separate from LCSC storefront stock. Availability and classification can change.

| References | Manufacturer | Ordering code | Specification | JLCPCB class | Assembly stock |
| --- | --- | --- | --- | --- | ---: |
| U1 | Texas Instruments | [SN74LVC2T45DCUR / C15741](https://jlcpcb.com/partdetail/C15741) | VSSOP-8; dual-supply translator | Extended | 53,962 |
| R1 | UNI-ROYAL(Uniroyal Elec) | [0603WAF1002T5E / C25804](https://jlcpcb.com/partdetail/C25804) | 10 kohms; 1%; 0.1 W; 0603 | Basic | 42,504,788 |
| R2 | UNI-ROYAL(Uniroyal Elec) | [0603WAF2200T5E / C22962](https://jlcpcb.com/partdetail/C22962) | 220 ohms; 1%; 0.1 W; 0603 | Basic | 2,317,652 |
| R3 | UNI-ROYAL(Uniroyal Elec) | [0603WAF1004T5E / C22935](https://jlcpcb.com/partdetail/C22935) | 1 Mohm; 1%; 0.1 W; 0603 | Basic | 5,656,717 |
| R4/R5 | UNI-ROYAL(Uniroyal Elec) | [0603WAF6800T5E / C23228](https://jlcpcb.com/partdetail/C23228) | 680 ohms; 1%; 0.1 W; 0603 | Basic | 1,301,911 |
| C1/C2 | YAGEO | [CC0603KRX7R9BB104 / C14663](https://jlcpcb.com/partdetail/C14663) | 100 nF; 10%; 50 V; X7R; 0603 | Basic | 53,165,414 |
| C3/C4 | Samsung Electro-Mechanics | [CL10A105KB8NNNC / C15849](https://jlcpcb.com/partdetail/C15849) | 1 uF; 10%; 50 V; X5R; 0603 | Basic | 12,229,171 |
| C5/C6 | FH (Guangdong Fenghua Advanced Tech) | [0603B103K500NT / C57112](https://jlcpcb.com/partdetail/C57112) | 10 nF; 10%; 50 V; X7R; 0603 | Basic | 4,618,632 |
| D1 | Nexperia | [BAT54S,215 / C47546](https://jlcpcb.com/partdetail/C47546) | 30 V; 200 mA; dual series Schottky; SOT-23 | Extended | 429,437 |
| D2/D3 | Hubei KENTO Elec | [KT-0603R / C2286](https://jlcpcb.com/partdetail/C2286) | Red LED; 0603 | Basic | 8,402,771 |
| Q1 | Jiangsu Changjing Electronics Technology Co., Ltd. | [MMBT3904(RANGE:100-300) / C20526](https://jlcpcb.com/partdetail/C20526) | NPN; 40 V; 200 mA; SOT-23 | Basic | 4,177,051 |

The [supplier records](docs/lcsc-parts.json) contain the selected ordering codes, datasheet URLs, assembly classifications, stock counts, and public JLCPCB API sources. The assembly order uses these ordering codes.

R1 holds an undriven input low. R2 isolates the RF_RAW detector branch and is 220 ohms. R3 discharges the detector reservoir. R4 limits the activity LED current; R5 independently limits the 3.3 V power LED current. D3 indicates only the 3.3 V rail, so it cannot confirm that the 5 V supply is present.

C1/C2 provide local supply bypassing. C3 provides bulk bypassing, and C4 blocks output DC; the [C4 model evidence](C4-SELECTION.md) covers the Samsung part. C5 blocks DC in the detector branch; C6 is the rectified-voltage reservoir. C5/C6 are 50 V X7R parts with nominal 10 nF capacitance. Their mounted RF impedance is unmeasured and outside the detector model.

D1 is Nexperia BAT54S,215 / C47546, an Extended part with strong assembly stock. Its series-diode SOT-23 pinout matches the local symbol and footprint: pin 1 is the grounded anode, pin 3 is the RF common node, and pin 2 feeds Q1. Q1 is the CJ MMBT3904 with hFE 100-300 at its specified test point; pins 1/2/3 are base/emitter/collector. Both LEDs use Hubei KENTO KT-0603R / C2286; the local LED footprint uses pad 1 for the anode and pad 2 for the cathode. Confirm polarity in the assembly preview.

The [detector study](INPUT-LOADING.md) uses Diodes Incorporated transistor/diode models and an illustrative red LED. Those models are not exact models of the selected Nexperia diode, CJ transistor, or KENTO LED. Package and pin compatibility do not establish identical VHF behavior, gain, brightness, or supply current.

All selected parts use the existing project-local symbols, footprints, and STEP models. The schematic and PCB hide the manufacturer, MPN, `LCSC Part #`, datasheet, and assembly-class fields. [BOM.csv](BOM.csv) includes all sixteen assembly positions. The schematic, PCB, and rendering show the connectors. They are on the board, excluded from the BOM, and not marked DNP.

## JLCPCB BOM export

The schematic and PCB store each supplier code in the hidden `LCSC Part #` field. The project’s **JLCPCB** BOM preset exports [BOM.csv](BOM.csv) with `Comment`, `Designator`, `Footprint`, and `LCSC Part #` columns, plus quantity, manufacturer, and MPN. Rows group only when the value, footprint, supplier code, manufacturer, and MPN match. J1/J2/J3 carry the Exclude from BOM flag, and the preset excludes DNP components.

In the Schematic Editor, open **Tools → Edit Symbol Fields Table**, select the **JLCPCB** preset and CSV format, and export to `BOM.csv`. The command-line equivalent, run from this project directory, is:

```sh
kicad-cli sch export bom --preset JLCPCB --output BOM.csv "Logic RF Driver.kicad_sch"
```

JLCPCB uses the `C…` ordering codes to match parts in its assembly catalog. Check the matched parts and placement preview in the order interface. The BOM supplies part selection; assembly also requires a component placement (CPL) file. See [JLCPCB’s KiCad export guide](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad).

J2 is hand-fitted as [Adafruit product 2136](https://www.adafruit.com/product/2136). Its local footprint and model remain visible in the design and assembly image. It has no LCSC ordering code and is excluded from the JLCPCB BOM.

The [connector notes](CONNECTORS.md) identify J1/J3 as Adafruit 1865 SMA jacks and describe J2's shared Adafruit 2136 screw-terminal/header footprint. J1/J2/J3 are hand-fit parts excluded from the factory BOM.
