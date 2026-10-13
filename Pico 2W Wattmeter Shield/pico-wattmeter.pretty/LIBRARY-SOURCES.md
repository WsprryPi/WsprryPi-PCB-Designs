# Footprint sources and licenses

## KiCad footprints

`C_0402_1005Metric`, `R_0402_1005Metric`, `R_0805_2012Metric`, and `TSSOP-10_3x3mm_P0.5mm` derive from the KiCad 10.0.1 standard libraries: `Capacitor_SMD.pretty`, `Resistor_SMD.pretty`, and `Package_SO.pretty`. Their pads, apertures, pitch, bodies, courtyards, and model references follow those sources. Local graphics use 0.15 mm silkscreen strokes; 0402 outline marks are on F.Fab.

[C_1206_3216Metric.kicad_mod](C_1206_3216Metric.kicad_mod) is the KiCad 10.0.6 standard capacitor footprint used by C30–C34, C40–C44, and C48. It retains the upstream pads, mask/paste apertures, courtyard, metadata, and installed-library model reference.

[C_0603_1608Metric.kicad_mod](C_0603_1608Metric.kicad_mod) is an unchanged copy of the KiCad 10.0.6 `Capacitor_SMD.pretty` footprint for C61, YAGEO CC0603KRX7R8BB105 / LCSC C106858. It retains the upstream geometry, dynamic reference text, and installed KiCad model path and follows the KiCad library license described below.

Copyright KiCad Library Contributors. These footprints use [CC BY-SA 4.0 with the KiCad library exception](https://www.kicad.org/libraries/license/). The exception permits electronic-design use without imposing that library license on the resulting design. [Upstream footprint libraries](https://gitlab.com/kicad/libraries/kicad-footprints).

## Adafruit SMA connector

[SMA_Adafruit_1865_EdgeMount.kicad_mod](SMA_Adafruit_1865_EdgeMount.kicad_mod) derives from `SMA_EDGELAUNCH` in the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library). Adafruit attribution and its source URL are included in the footprint. See [J30 connector geometry](../J1-CONNECTOR-NOTES.md).

Both the local footprint and placed J30 reference the original repository SMA preview through `${KIPRJMOD}/pico-wattmeter.3dshapes/`, with zero offset, unit scale, and zero additional rotation. The footprint's placement determines the orientation. See [model source, generator, and license](../pico-wattmeter.3dshapes/README.md#sma-connector-model).

## Logo

[Wsprry_Pi_Synth_Logo.kicad_mod](Wsprry_Pi_Synth_Logo.kicad_mod) contains two filled polygons in a 4.405354 × 5.584516 mm outline, within one unlocked footprint. It has a courtyard, hidden reference/value fields, and no copper pads or soldermask openings. It is excluded from BOM and placement files. The saved PCB contains one front-side logo instance, LOGO2.

## Pico interface

[Raspberry_Pi_Pico_2W_Header.kicad_mod](Raspberry_Pi_Pico_2W_Header.kicad_mod) provides the combined 40-pad interface used by U10. The two model references and transforms match the independent [Pico shield template footprint](../../Pico%202W%20Shield%20Template/pico-shield.pretty/Raspberry_Pi_Pico_2W_Header.kicad_mod). The socket STEP asset is local to this project and uses `${KIPRJMOD}`. Geometry, thermal reliefs, numbering, and exclusions are described in the [socket and notch documentation](../PICO-HEADERS-AND-NOTCH.md). See [socket model provenance and limits](../pico-wattmeter.3dshapes/README.md#pico-interface-socket-models).

## LDO assets

`SOT-23-5` and `C_0805_2012Metric` are independent copies of the Synth Shield's KiCad 10.0.6 library assets. They are used by U20 and C20/C21; C50 also uses the 0805 capacitor footprint. Their sources and KiCad library terms are recorded in the [source footprint documentation](../../WsprryPico%20Synth%20Shield%20with%20GPS/LIBRARY-SOURCES.md). Installed KiCad model references are retained.

The local `TPS7A2033PDBVR` and generic `C` symbols derive from that project's definitions. Their pin numbering, geometry, provenance, and library terms are documented in the [source symbol documentation](../../WsprryPico%20Synth%20Shield%20with%20GPS/SYMBOL-SOURCES.md). The wattmeter uses its own registered `pico-wattmeter` symbol library.

## Detector and other assets

The local QFN footprint gives U40 its 16 lead pads, 1.8 × 1.8 mm exposed ground land, and four F.Paste windows. See [pad, stencil, and via geometry](../U1-PASTE-WINDOWS.md) and the [CP-16-22 STEP model](../pico-wattmeter.3dshapes/README.md).

Other supplied/imported assets retain their source metadata and documented compatibility limits. Repository-owned work uses the [MIT license](../../LICENSE.md); third-party assets retain their own notices and terms.
