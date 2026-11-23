# Project-local libraries

The independent `WsprryPi LPF` library supplies all used symbols, footprints, and available models. Library tables use `${KIPRJMOD}`; no sibling project or machine-specific path is required. Use KiCad 10.0.1 or newer; validation used 10.0.6.

| Asset | Location | Contents |
| --- | --- | --- |
| Symbols | [Symbol library](symbols/WsprryPi%20LPF.kicad_sym) | Six: C, L, GND, PWR_FLAG, Conn_Coaxial, and paired LPF header |
| Footprints | [Footprint library](footprints/WsprryPi%20LPF.pretty/) | Four types: capacitor, axial/toroid inductor, paired header, and Adafruit SMA |
| Models | [3D models](3dmodels/) | Three STEP files and one illustrative SMA VRML file |

## Adafruit 1865 SMA

`SMA_Adafruit_1865_EdgeMount` replaces the previous Samtec footprint. J2/J3 use the generic passive `Conn_Coaxial` symbol, with **pin 1 = RF center** and **pin 2 = shell/ground**. Instance values and purchasing fields select **Adafruit 1865**, a female edge-launch connector for 1.6 mm boards.

The footprint was copied from the repository's `WsprryPi Zero GPIO BS170` custom Adafruit footprint, checked against the [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library) `SMA_EDGELAUNCH` package and the [Adafruit 1865 drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) on 2026-11-22. The signal land is 1.27 mm wide, ground lands 1.524 mm wide, with ground centers at ±2.54 mm from RF. Relative to the source package's 4.064 mm lands, this local variant has 4.014 mm lands and a **0.05 mm copper setback**, retaining the inland end of the lands. It is hand soldered, without paste apertures.

The origin is the PCB-edge datum, and the connector points outward along local +Y. A project-local `.kicad_dru` rule permits 0 mm edge clearance only for pads of J2/J3. It does not alter the 0.50 mm global limit or clearances between copper nets. Copy that intentional rule when reusing this edge-launch implementation; do not disable the board-wide check.

The local `SMA_Adafruit_1865_Preview.wrl` follows the existing repository visualization, with approximate flange/barrel and rear-finger geometry. It is not supplier CAD or evidence of mechanical clearance. The model's dimensions, threads, internals, and tolerances are simplified. Connector fit and RF behavior remain unverified. No Samtec model is attached to the Adafruit connector, and unused Samtec footprint/model assets have been removed from this project.

## Other footprints

`C_Disc_D3.0mm_W1.6mm_P2.50mm` retains 2.50 mm lead pitch. Each board shunt provides a parallel pair and two 5.00 mm cross-pair spanning combinations. Ground is pad 1 and signal pad 2.

`L_Axial_Horiz_Torroid_Vert_12mm_D5mm_P10.2mm` retains the original axial/upright-toroid geometry and 0.8 mm holes, with two holes numbered 1 and two numbered 2. Use one hole of each electrical number for a winding. The generic axial STEP model does not represent a wound toroid or establish fit, core, turns, Q, or power handling.

`LPF_HeaderPair_Male_2x1x04_P2.54mm_S33.02mm` represents two underside male 1×4 headers with 2.54 mm pin pitch and 33.02 mm centerline spacing. It instances the local single-header STEP twice. Pads 1/4/5/8 are GND, 2/3 RF_IN, and 6/7 RF_OUT. This WsprryPi pinout is not directly compatible with unmodified QRP Labs LPFs. No header manufacturer/MPN is specified.

See the [project README](../README.md) and [validation record](../VALIDATION.md) for population, assembly, and limitations.

## Sources and licenses

KiCad-derived standard symbols, capacitor/header/inductor footprints, and STEP models retain Copyright KiCad Library Contributors and [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). Project-specific combined-header and axial/toroid geometry is inherited from the original LPF.

Adafruit's `SMA_EDGELAUNCH` library package is published as public domain by [Adafruit](https://github.com/adafruit/Adafruit-Eagle-Library). That attribution and source are retained here and in the footprint description. The local adaptation and original illustrative SMA VRML model use the repository MIT license; the model retains its license header. The MIT license does not replace third-party KiCad library terms.
