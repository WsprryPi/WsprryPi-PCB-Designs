# Pico 2W QRP Wattmeter Shield

A Raspberry Pi Pico 2 W shield with an ADL5904 RF power detector, ADS1115 ADC, and TPS7A2033 analog regulator. Open [Pico 2W Wattmeter Shield.kicad_pro](Pico%202W%20Wattmeter%20Shield.kicad_pro) in KiCad 10. Project libraries use `${KIPRJMOD}` paths.

The design is supplied **as is, without warranty**, under the repository's [MIT license](../LICENSE.md). It is an experimental system. Production use requires an operator who understands its limitations and requirements and verifies the assembled system's suitability. See the [repository notice](../README.md#experimental-use-and-warranty).

## Current design

The PCB is a two-layer, nominally 1.6 mm FR4 board with circuit components on F.Cu and U10's two female socket strips on B.Cu, matching the [Pico shield template](../Pico%202W%20Shield%20Template/README.md). It contains **37 footprints: 34 automatic SMT components, J30, U10, and one front silkscreen logo**. The components, including the R63/C61 pull-up supply filter, are placed and routed.

Assembled input match, accuracy, noise rejection, mechanical fit, and the soldering process are unqualified. ERC ignores single-use global labels, four-way junctions, simulation model issues, and footprint-filter mismatches; DRC has no ignored checks.

## Measurement path

`J30 → C30–C34 → RF_DET_IN → C40–C44 → RFIN/U40 → VRMS_RAW → R50/C50 → VRMS_FILTERED/U60 AIN0`

| Section | Saved design |
| --- | --- |
| RF input | J30; terminating low-power meter, with external attenuation for amplifier outputs |
| Coupling | Two banks of five parallel 100 nF C0G capacitors, nominally 500 nF per bank |
| Shunt load | R30–R34: five parallel 412 Ω resistors, nominally 82.4 Ω, plus the detector input branch |
| Input matching | The shunt is within 0.12% of ADI's 82.5 Ω reference; assembled input impedance is unmeasured |
| Intended frequency range | 136 kHz–450 MHz, covering 2200 m through 70 cm; assembled-board coverage is unqualified |
| Nominal detector range | −30 to +15 dBm, approximately 1 µW–31.6 mW; connector range requires calibration |
| ADC filter | R50 = 470 Ω, C50 = 22 µF X5R; nominal cutoff 15.4 Hz |

There is no onboard attenuation pad or qualified high-power overload protection. The two capacitor banks, buses, launch, and detector impedance form a frequency-dependent RF network. See [input range and measurement conditions](INPUT-RANGE.md). The printed current range is calculated for a nominal 50 Ω load, rather than a direct current measurement.

## Power

**The analog section requires VBUS.** U20 takes VBUS from Pico pin 40 and generates `ANALOG_3V3` for U40, U60, and the I²C pullups. C20 and C21 are 2.2 µF, 25 V X7R capacitors at the regulator input and output. C46/C47 decouple the detector, and C60 decouples the ADC. The Pico's 3V3 output is not connected to the analog rail.

USB normally supplies VBUS. Powering the Pico solely through VSYS leaves the analog section unpowered. An external VBUS source must respect the Pico's USB power arrangement and avoid conflicting supplies. Measurements require a valid analog rail and settled detector/filter output.

VBUS follows the lower perimeter, and the analog rail reaches the detector from below and the ADC/control branch from the right. Neither supply trace crosses the RF capacitor-bank area. R63/C61 isolate the pull-up supply branch. A common regulator and ground serve the analog and I²C loads; noise immunity to Pico activity is unmeasured.

## ADC and filtering

U60 uses AIN0 as a single-ended detector-voltage input. ADDR is grounded, giving I²C address 0x48. SDA uses GP4; SCL uses GP5 through the fitted R62 0 Ω jumper. R60/R61 are 4.7 kΩ pullups supplied through R63 = 47 Ω, with C61 = 1 µF X7R providing local bypass at their common supply node. This filter is present in both schematic and PCB. U40 and U60 receive `ANALOG_3V3` directly with their own decoupling. Unused ADC channels and ALERT/RDY have no-connect flags.

R63/C61 has a nominal **3.4 kHz** corner and approximately **65 mV** supply drop with both pull-ups low, assuming ideal low output levels. It provides local storage and supply isolation for switching currents. Its effect on the assembled noise floor is unmeasured; nominal attenuation at 50/60 Hz is negligible.

R50/C50 passes DC and attenuates changing voltage. Its ideal one-pole attenuation is about **10.6 dB at 50 Hz and 12.1 dB at 60 Hz**, with a 10.34 ms time constant and about 47.6 ms settling to 1%. Capacitor tolerance, bias, temperature, detector output impedance, and ADC loading affect these figures. It is not a mains notch filter, and there is no established system-level mains-rejection specification. C49 remains a separate 10 nF capacitor directly on VRMS.

The hardware provides one measurement channel. ADC range, conversion rate, timed averaging, and calibration coefficients are application settings; this repository does not establish a verified wattmeter firmware configuration.

## Current assembly and fabrication

Factory assembly comprises **34 components on F.Cu**: **C20–C21, C30–C34, C40–C50, C60–C61; R30–R34, R40, R50, R60–R63; U20, U40, U60**. This is 20 capacitors, 11 resistors, and three ICs. J30, two female sockets, and the Pico module are fitted by hand. U10 represents the combined 40-pad socket interface; schematic J10/J11 are pinless purchasing descriptions. The front logo and manual parts are excluded from automatic SMT assembly.

The **Shield purchasing BOM** preset uses `LCSC Part #`. All 34 schematic and PCB SMT parts have matching manufacturer, MPN, and LCSC identifiers. R30–R34 specify Viking ARG02BTC4120 / C2683017 in local 0402 footprints. R63 specifies YAGEO RC0402FR-0747RL / C137973 in 0402; C61 specifies YAGEO CC0603KRX7R8BB105 / C106858 in 0603. Factory BOM and placement exports must contain the same 34 references and correct U20/U40/U60 pin-1 orientation. The schematic contains the complete part selections. The input-range silkscreen displays J30 through a reference variable and follows reannotation.

Seven selected through vias use **0.60 mm copper / 0.25 mm drill** with filling/capping enabled, F-side untented, and B-side tented: five in U40's exposed ground pad and one each centered on R40 pad 1 and C48 pad 1. The unique drill size identifies this selective process. The 17 ordinary vias comprise five 0.50/0.20 mm, ten 0.60/0.30 mm, and two 0.80/0.40 mm vias. All 24 are through vias; the custom rules disallow blind, buried, and microvias. The ordinary ground-via drills beside C45/C47 have **0.15 mm nominal clearance** from the adjacent component solder-pad openings.

The required fabrication process is selective nonconductive epoxy filling, planarization, and copper capping. Its availability for this exact two-layer order is not confirmed. Four separate 0.65 × 0.65 mm F.Paste windows cover 52.16% of U40's 1.8 × 1.8 mm ground land. Supplier process acceptance, stencil thickness, and reflow conditions are assembly requirements.

- [Fabrication and assembly requirements](manufacturing-notes/ORDER-NOTES.txt)
- [Front assembly map](manufacturing-notes/ASSEMBLY-FRONT.svg)
- [Selective via-treatment drawing](manufacturing-notes/U1-VIA-TREATMENT.svg)
- [U40 exposed-pad and stencil geometry](U1-PASTE-WINDOWS.md)
- [SMA connector and board-edge fit](J1-CONNECTOR-NOTES.md)
- [Pico sockets and antenna notch](PICO-HEADERS-AND-NOTCH.md)

The manufacturing drawings identify their source PCB by SHA-256. Socket lead fit and mating height are unspecified. The PCB stackup's copper-finish field is `None`, and there are no dedicated board fiducials; finish and panel tooling belong in the order specification.

## Pico interface placement

U10 is locked at **(146.810, 90.750) mm, −90°, B.Cu**, and its `Raspberry Pi Pico 2W` group is locked. Its 40 pad positions match the template. The notch spans x = 164.46–173.46 mm and y = 82.86–96.86 mm, with a copper/component keepout on both layers.

In **Update PCB from Schematic**, leave **Re-link footprints to schematic symbols based on their reference designators** and **Override locks** unchecked. Normal symbol-ID matching preserves the interface identity and placement. [KiCad's update documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#updating_the_board_from_the_schematic) describes these options.

The two socket models belong to U10's combined footprint and use project-local paths. The reusable footprint contains the same references. The socket geometry is a generic preview, without a selected manufacturer or qualified mating stack.

## Libraries and 3D view

Local assets are in `pico-wattmeter.pretty/`, `pico-wattmeter.kicad_sym`, `pico-wattmeter.kicad_blocks/`, and `pico-wattmeter.3dshapes/`. See [footprint sources and licenses](pico-wattmeter.pretty/LIBRARY-SOURCES.md) and [model sources and limits](pico-wattmeter.3dshapes/README.md).

Select **View > 3D Viewer** in the PCB Editor. U40 uses the local CP-16-22 STEP model. U10 uses two local socket models. J30 uses the local illustrative Adafruit 1865 SMA model, pointing outward from the left board edge. Passives, U20, and U60 use installed KiCad models. All placed model references resolve in the checked KiCad installation.

The optional, unplaced Pico SMD footprint uses `${KIPRJMOD}/pico-2w-libs/Raspberrypi pico2 W.step`. That separate reference collection has [pin/pad, model-alignment, and provenance limitations](pico-2w-libs/README.md). It is not the placed socket interface.

`fabrication-toolkit-options.json` stores export preferences. KiCad sources contain the part identifiers, connectivity, layout, and assembly exclusions. Local preferences, backups, plugin state, and generated export directories are ignored by Git.
