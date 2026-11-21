# Parts and procurement

Four ordering codes cover the six BOM positions. The five passives are JLCPCB Basic parts; U1 is Extended.

| References | Manufacturer | Ordering code | Specification | JLCPCB class |
| --- | --- | --- | --- | --- |
| U1 | Texas Instruments | [SN74LVC2T45DCUR / C15741](https://jlcpcb.com/partdetail/C15741) | VSSOP-8, dual-supply translator | Extended |
| R1 | UNI-ROYAL | [0603WAF1002T5E / C25804](https://jlcpcb.com/partdetail/C25804) | 10 kohms, 1%, 0.1 W, 75 V, 0603 | Basic |
| C1/C2 | YAGEO | [CC0603KRX7R9BB104 / C14663](https://jlcpcb.com/partdetail/C14663) | 100 nF, 10%, 50 V, X7R, 0603 | Basic |
| C3/C4 | Samsung Electro-Mechanics | [CL10A105KB8NNNC / C15849](https://jlcpcb.com/partdetail/C15849) | 1 uF, 10%, 50 V, X5R, 0603 | Basic |

All four codes have JLCPCB stock listings. Check the assembly order for available quantities and part classification: neither is fixed, and JLCPCB assembly stock is separate from LCSC storefront stock. The [supplier records](docs/lcsc-parts.json) include the API sources.

The 10-kilohm R1 holds an undriven input low. At a steady 3.3 V HIGH, it dissipates about 1.09 mW. It is a pull-down, not a series damping or attenuation resistor. See the [resistor datasheet](https://www.lcsc.com/datasheet/lcsc_datasheet_2206010045_UNI-ROYAL-Uniroyal-Elec-0603WAF1002T5E_C25804.pdf).

C1 and C2 bypass the 3.3 V and 5 V supplies. Each is 100 nF, X7R, and rated for 50 V. Their mounted impedance and response to supply transients are unmeasured. The [capacitor datasheet](https://www.lcsc.com/datasheet/lcsc_datasheet_2211101700_YAGEO-CC0603KRX7R9BB104_C14663.pdf) gives the part specifications. C3 adds bulk bypassing, while C4 blocks output DC; their [model evidence](C4-SELECTION.md) covers the selected Samsung part.

The schematic and PCB store Manufacturer, MPN, LCSC, and datasheet information in hidden fields. [BOM.csv](BOM.csv) groups C1/C2 and lists U1, R1, and C1–C4. J1/J2/J3 are on the board and visible in the symbols, footprints, and models. They are excluded from the BOM and are not DNP.