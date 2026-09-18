# WsprryPi PCB Designs

KiCad schematics, PCB layouts, local libraries, and engineering documentation for WsprryPi and Raspberry Pi Pico projects.

These designs require revision-specific validation before production. KiCad source files are authoritative; included PDFs are reference exports and may not match the current sources.

## Projects

| Project | Purpose | Reference export |
| --- | --- | --- |
| [Synth Universal](Wsprry-Pi-Synth-Univ/README.md) | Si5351-synthesized transmission board | [Schematic PDF](Wsprry-Pi-Synth-Univ/Wsprry-Pi-Synth-Univ.pdf) |
| [GPIO Universal](Wsprry-Pi-GPIO-Univ/README.md) | GPIO transmission board | [Schematic PDF](Wsprry-Pi-GPIO-Univ/Wsprry-Pi-GPIO-Univ.pdf) |
| [LPF](Wsprry-Pi-LPF/README.md) | Low-pass filter board and design workbook | [Schematic PDF](Wsprry-Pi-LPF/Wsprry-Pi-LPF.pdf) |
| [Pico 2W Wattmeter Shield](Pico%202W%20Wattmeter%20Shield/README.md) | ADL5904 RF detector and ADS1115 ADC shield | See project assembly drawings |
| [Pico 2W Shield Template](Pico%202W%20Shield%20Template/README.md) | Unwired shield interface, outline, and antenna notch | KiCad project template |

[Standalone Pico 2 W library assets](pico-2w-libs/README.md) include a symbol, footprints, and STEP model with documented compatibility and provenance limits. The shield projects use their own local libraries.

## Open a design

Clone [WsprryPi/WsprryPi-PCB-Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs) and open the project's `.kicad_pro` file in KiCad. Read its README for assembly requirements, dependencies, and validation limits. Follow the Shield Template's instructions to create a new shield project.

| Project | Saved schematic and PCB generator version |
| --- | --- |
| Synth Universal, Pico 2W Wattmeter Shield, Pico 2W Shield Template | KiCad 10.0 |
| GPIO Universal, LPF | KiCad 9.0 |

Project library tables use `${KIPRJMOD}` paths. Keep each project's local libraries together when copying it. Standard footprints and models require the corresponding installed KiCad libraries.

### Missing library assets

The following project-relative symbol libraries are referenced but absent:

| Project | Missing path |
| --- | --- |
| Synth Universal | `libraries/symbols/Wsprry-Pi.kicad_sym` |
| GPIO Universal | `libraries/symbols/Wsprry-Pi.kicad_sym` |
| LPF | `libraries/symbols/New_Library.kicad_sym` |
| LPF | `libraries/symbols/Wsprry-Pi-LPF.kicad_sym` |

The schematics contain embedded symbol definitions. Library editing and updates require the missing libraries or deliberate resolution of their references.

Custom footprints also reference absent STEP files under `EASYEDA_MODELS`: the large through-hole capacitor in Synth, GPIO, and LPF, plus the pushbutton and through-hole SMA connector in Synth and GPIO. These omissions affect 3D visualization. See each project's documentation for other model limitations.

## Design proposals

These documents describe proposed circuits and outstanding engineering requirements; they do not establish implemented or validated hardware.

- [GPS frequency calibration for Pi and Pico](Wsprry-Pi-Synth-Univ/GPS-FREQUENCY-CALIBRATION.md): LS7366R capture of Si5351 CLK2 against GPS PPS.
- [Broadband RF amplifier HAT](design/raspberry-pi-hat-broadband-rf-amplifier.md): a proposed clock-input amplifier, power control, and supply architecture.

## Repository contents

Track design sources, local libraries, reusable models, design calculations, intentional reference exports, and documentation. Preserve legacy cache or rescue libraries required by a design.

Git ignores KiCad local preferences, locks, caches, automatic backups, and `.history`. Put regenerable exports in `generated/`, `production/`, or `fabrication/`. Project-local `jlcpcb/` ignore rules cover plugin state where applicable. See [`.gitignore`](.gitignore).

Publish manufacturing packages with the corresponding GitHub release, identifying the source commit, board revision, KiCad version, and validation status. Keep assembly and fabrication requirements in the project's maintained documentation.

## Contributions and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for editing and validation requirements. Report problems through [GitHub Issues](https://github.com/WsprryPi/WsprryPi-PCB-Designs/issues). [AGENTS.md](AGENTS.md) contains shared agent guidance; [CLAUDE.md](CLAUDE.md) points to it.

Repository-owned work uses the [MIT license](LICENSE.md). Preserve third-party copyright, attribution, and license terms; project and library documentation identifies known exceptions and provenance limits.
