# WsprryPi PCB Designs

KiCad schematics, PCB layouts, local libraries, and engineering documentation for WsprryPi and Raspberry Pi Pico projects.

See each project's order status, assembly requirements, and validation limits before fabrication. KiCad source files are authoritative; included PDFs are reference exports and may not match the current sources.

## Experimental use and warranty

All designs are provided **as is, without warranty**, as stipulated by the [MIT license](LICENSE.md) for repository-owned work. These are experimental hardware systems. They should not be used for production work unless the operator understands the design's limitations, assembly and power requirements, calibration needs, and the validation required for the actual system and operating conditions.

The operator is responsible for determining suitability and verifying the assembled hardware. A clean CAD check or a fabrication-ready layout does not establish electrical, RF, thermal, mechanical, or system performance. Third-party assets retain their documented licenses and notices.

## Projects

| Project | Purpose | Status / reference export |
| --- | --- | --- |
| [WsprryPi LPF](WsprryPi%20LPF/README.md) | Low-pass filter board and design workbook | Export from the KiCad source |
| [WsprryPi LPF-LCL](WsprryPi%20LPF-LCL/README.md) | Five-element L-first LPF with minimum-loss WSPR/QRSS tuning | Independent routed development board; physical/RF qualification pending |
| [Relay-Switched LPF](Relay-Switched%20LPF/README.md) | Independent reconstruction of the QRP Labs Rev. 5 five-filter relay carrier | Schematic and two-layer PCB; unqualified, see project validation |
| [Pico 2W Wattmeter Shield](Pico%202W%20Wattmeter%20Shield/README.md) | ADL5904 RF detector and ADS1115 ADC shield | See project assembly drawings |
| [Pico 2W Shield Template](Pico%202W%20Shield%20Template/README.md) | Unwired shield interface, outline, and antenna notch | KiCad project template |
| [Logic RF Driver](Logic%20RF%20Driver/README.md) | Compact SN74LVC2T45 clock driver with paralleled outputs | Routed two-layer prototype for the 137 kHz–145 MHz target; RF performance unqualified |
| [RF Indicator LED](RF%20Indicator%20LED/README.md) | RF indicator circuit draft | Incomplete component selection; empty PCB, see project validation |
| [Quad Logic Buffer Amp](Quad%20Logic%20Buffer%20Amp/README.md) | Logic buffer RF amplifier schematic | Standalone 80 × 30 mm estimated PCB, placed and unrouted |
| [WsprryPico Quad Logic Buffer Amp](WsprryPico%20Quad%20Logic%20Buffer%20Amp/README.md) | Independent Pico shield copy of Quad Logic Buffer Amp with project-local libraries | Placement review pending, unrouted |
| [WsprryPi Quad Logic Buffer Amp](WsprryPi%20Quad%20Logic%20Buffer%20Amp/README.md) | Raspberry Pi Zero HAT logic buffer amplifier with local LPF header assets | Placement review pending, unrouted |
| [WsprryPico GPIO Shield with GPS](WsprryPico%20GPIO%20Shield%20with%20GPS/README.md) | Direct Pico GP2 BS170 RF amplifier with onboard GNSS and independent local libraries | Placed and routed GPIO/GNSS design; see current validation |
| [WsprryPico GPIO Shield with GPS - Torroid Edition](WsprryPico%20GPIO%20Shield%20with%20GPS%20-%20Torroid%20Edition/README.md) | GPIO amplifier with a bifilar transformer | Placed and routed within the original outline; all SMT on the underside; physical/RF qualification pending |
| [WsprryPico Synth Shield with GPS](WsprryPico%20Synth%20Shield%20with%20GPS/README.md) | Pico 2 W TCXO/Si5351A shield with a BS170 amplifier and onboard GNSS | Implemented PCB for the 2200 m–10 m target; see current validation and bias setup |
| [QRP Labs Modules](QRP%20Labs%20Modules/README.md) | Electrical models of the photographed 25 MHz TCXO and Rev6 synthesizer, with their interconnection | [Reference schematic PDF](QRP%20Labs%20Modules/QRP%20Labs%20Modules.pdf); separate from the proposed synth shield |
| [RPi Full-Size HAT Template](RPi%20Full-Size%20HAT%20Template/README.md) | Official full-size HAT geometry and complete 40-pin interface | KiCad project template |
| [RPi Zero HAT Template](RPi%20Zero%20HAT%20Template/README.md) | Zero-size uHAT geometry and complete HAT+ capable 40-pin interface | KiCad project template |
| [WsprryPi Zero GPIO BS170](WsprryPi%20Zero%20GPIO%20BS170/README.md) | Zero-size Raspberry Pi GPIO RF amplifier with a single BS170 | **Ready for order:** headers and BS170 fitted by hand after manufacture; see [fabrication and assembly notes](WsprryPi%20Zero%20GPIO%20BS170/FABRICATION-NOTES.md) |

[Project-local Pico 2 W library assets](Pico%202W%20Wattmeter%20Shield/pico-2w-libs/README.md) include a symbol, footprints, and STEP model with documented compatibility and provenance limits. They are stored inside the Wattmeter Shield project; the Shield Template uses its own independent local libraries.

## Open a design

Clone [WsprryPi/WsprryPi-PCB-Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs) into a folder named `WsprryPi PCB Designs` and open the project's `.kicad_pro` file in KiCad. Read its README for assembly requirements, dependencies, and validation limits. Follow the applicable template's instructions to create a new shield or HAT project.

| Project | Saved schematic and PCB generator version |
| --- | --- |
| WsprryPi LPF, WsprryPi LPF-LCL, Pico 2W Wattmeter Shield, Pico 2W Shield Template, Logic RF Driver, RF Indicator LED, Quad Logic Buffer Amp, WsprryPico Quad Logic Buffer Amp, WsprryPi Quad Logic Buffer Amp, WsprryPico GPIO Shield with GPS, WsprryPico GPIO Shield with GPS - Torroid Edition, WsprryPico Synth Shield with GPS, RPi Full-Size HAT Template, RPi Zero HAT Template, WsprryPi Zero GPIO BS170 | KiCad 10.0 |

Project library tables use `${KIPRJMOD}` paths. Keep each project's local libraries together when copying it. The Pico and HAT projects use their own local libraries and installed KiCad models where their project documentation specifies them.

### Project-local libraries

The LPF includes local copies of its symbols and footprints, plus available STEP models, resolved through `${KIPRJMOD}`. Its local library assets require KiCad 10.0.1 or newer; the generator version above describes its saved format. The other projects maintain their own independent local libraries as described in their READMEs.

- [LPF library contents and limits](WsprryPi%20LPF/libraries/README.md)
- [BS170 amplifier library sources and limits](WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md)

Project documentation records model gaps, assembly exclusions, and the applicability of ERC/DRC findings to the identified source revision. Order readiness does not establish measured electrical, thermal, or RF performance.

## Design proposals

These documents describe proposed circuits and outstanding engineering requirements; they do not establish implemented or validated hardware.

- [GPS frequency calibration for Pi and Pico](design/GPS-FREQUENCY-CALIBRATION.md): LS7366R capture of Si5351 CLK2 against GPS PPS.
- [Broadband RF amplifier HAT](design/raspberry-pi-hat-broadband-rf-amplifier.md): a proposed clock-input amplifier, power control, and supply architecture.

## Repository contents

Track design sources, local libraries, reusable models, design calculations, intentional reference exports, and documentation. Preserve legacy cache or rescue libraries required by a design.

The root [`.gitignore`](.gitignore) covers KiCad local preferences, locks, caches, automatic backups, `.history`, and `jlcpcb/` plugin state and output throughout the repository. Put regenerable exports in `generated/`, `production/`, or `fabrication/`.

Publish manufacturing packages with the corresponding GitHub release, identifying the source commit, board revision, KiCad version, and validation status. Keep assembly and fabrication requirements in the project's maintained documentation.

## Contributions and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for editing and validation requirements. Report problems through [GitHub Issues](https://github.com/WsprryPi/WsprryPi-PCB-Designs/issues). [AGENTS.md](AGENTS.md) contains shared agent guidance; [CLAUDE.md](CLAUDE.md) points to it.

Repository-owned work uses the [MIT license](LICENSE.md). Preserve third-party copyright, attribution, and license terms; project and library documentation identifies known exceptions and provenance limits.
