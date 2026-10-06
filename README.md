# WsprryPi PCB Designs

KiCad schematics, PCB layouts, local libraries, and engineering documentation for WsprryPi and Raspberry Pi Pico projects.

See each project's order status, assembly requirements, and validation limits before fabrication. KiCad source files are authoritative; included PDFs are reference exports and may not match the current sources.

## Projects

| Project | Purpose | Status / reference export |
| --- | --- | --- |
| [WsprryPi LPF](WsprryPi%20LPF/README.md) | Low-pass filter board and design workbook | Export from the KiCad source |
| [Pico 2W Wattmeter Shield](Pico%202W%20Wattmeter%20Shield/README.md) | ADL5904 RF detector and ADS1115 ADC shield | See project assembly drawings |
| [Pico 2W Shield Template](Pico%202W%20Shield%20Template/README.md) | Unwired shield interface, outline, and antenna notch | KiCad project template |
| [WsprryPico Shield](WsprryPico%20Shield/README.md) | Pico 2 W shield with the grouped BS170 amplifier circuit and independent local libraries | Pico bus connections and PCB layout pending |
| [RPi Full-Size HAT Template](RPi%20Full-Size%20HAT%20Template/README.md) | Official full-size HAT geometry and complete 40-pin interface | KiCad project template |
| [RPi Zero HAT Template](RPi%20Zero%20HAT%20Template/README.md) | Zero-size uHAT geometry and complete HAT+ capable 40-pin interface | KiCad project template |
| [WsprryPi Zero GPIO BS170](WsprryPi%20Zero%20GPIO%20BS170/README.md) | Zero-size Raspberry Pi GPIO RF amplifier with a single BS170 | **Ready for order:** headers and BS170 fitted by hand after manufacture; see [fabrication and assembly notes](WsprryPi%20Zero%20GPIO%20BS170/FABRICATION-NOTES.md) |

[Project-local Pico 2 W library assets](Pico%202W%20Wattmeter%20Shield/pico-2w-libs/README.md) include a symbol, footprints, and STEP model with documented compatibility and provenance limits. They are stored inside the Wattmeter Shield project; the Shield Template uses its own independent local libraries.

## Open a design

Clone [WsprryPi/WsprryPi-PCB-Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs) into a folder named `WsprryPi PCB Designs` and open the project's `.kicad_pro` file in KiCad. Read its README for assembly requirements, dependencies, and validation limits. Follow the applicable template's instructions to create a new shield or HAT project.

| Project | Saved schematic and PCB generator version |
| --- | --- |
| WsprryPi LPF, Pico 2W Wattmeter Shield, Pico 2W Shield Template, WsprryPico Shield, RPi Full-Size HAT Template, RPi Zero HAT Template, WsprryPi Zero GPIO BS170 | KiCad 10.0 |

Project library tables use `${KIPRJMOD}` paths. Keep each project's local libraries together when copying it. The Pico and HAT projects use their own local libraries and installed KiCad models where their project documentation specifies them.

### Project-local libraries

The LPF includes local copies of its symbols and footprints, plus available STEP models, resolved through `${KIPRJMOD}`. Its local library assets require KiCad 10.0.1 or newer; the generator version above describes its saved format. The other projects maintain their own independent local libraries as described in their READMEs.

- [LPF library contents and limits](WsprryPi%20LPF/libraries/README.md)
- [BS170 amplifier library sources and limits](WsprryPi%20Zero%20GPIO%20BS170/LIBRARY-SOURCES.md)

Project documentation records model gaps, assembly exclusions, and historical ERC/DRC findings. Order readiness does not establish measured electrical, thermal, or RF performance.

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
