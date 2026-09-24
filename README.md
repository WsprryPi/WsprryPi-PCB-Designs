# WsprryPi PCB Designs

KiCad schematics, PCB layouts, local libraries, and engineering documentation for WsprryPi and Raspberry Pi Pico projects.

These designs require revision-specific validation before production. KiCad source files are authoritative; included PDFs are reference exports and may not match the current sources.

## Projects

| Project | Purpose | Reference export |
| --- | --- | --- |
| [Synth Universal](Wsprry-Pi-Synth-Univ/README.md) | Si5351-synthesized transmission board | [Schematic PDF](Wsprry-Pi-Synth-Univ/Wsprry-Pi-Synth-Univ.pdf) |
| [GPIO Universal](WsprryPi-GPIO-Univ/README.md) | GPIO transmission board | Export from the KiCad source |
| [LPF](Wsprry-Pi-LPF/README.md) | Low-pass filter board and design workbook | Export from the KiCad source |
| [Pico 2W Wattmeter Shield](Pico%202W%20Wattmeter%20Shield/README.md) | ADL5904 RF detector and ADS1115 ADC shield | See project assembly drawings |
| [Pico 2W Shield Template](Pico%202W%20Shield%20Template/README.md) | Unwired shield interface, outline, and antenna notch | KiCad project template |
| [RPi Full-Size Hat](RPi%20Full-Size%20Hat/README.md) | Official full-size HAT geometry and complete 40-pin interface | KiCad project template |
| [RPi Zero HAT](RPi%20Zero%20HAT/README.md) | Zero-size uHAT geometry and complete HAT+ capable 40-pin interface | KiCad project template |
| [WsprryPi Amplified GPIO](WsprryPi%20Amplified%20GPIO/README.md) | Full-size Raspberry Pi HAT project for amplified GPIO development | In development |
| [WsprryPi Zero GPIO](WsprryPi%20Zero%20GPIO/README.md) | Zero-size Raspberry Pi GPIO RF-amplifier project using uHAT geometry | **Not ready for order:** `YA9308-AEC` sourcing blocker |

[Standalone Pico 2 W library assets](pico-2w-libs/README.md) include a symbol, footprints, and STEP model with documented compatibility and provenance limits. The shield projects use their own local libraries.

## Open a design

Clone [WsprryPi/WsprryPi-PCB-Designs](https://github.com/WsprryPi/WsprryPi-PCB-Designs) and open the project's `.kicad_pro` file in KiCad. Read its README for assembly requirements, dependencies, and validation limits. Follow the applicable template's instructions to create a new shield or HAT project.

| Project | Saved schematic and PCB generator version |
| --- | --- |
| Synth Universal, LPF, Pico 2W Wattmeter Shield, Pico 2W Shield Template, RPi Full-Size Hat, RPi Zero HAT, WsprryPi Amplified GPIO, WsprryPi Zero GPIO | KiCad 10.0 |
| GPIO Universal | KiCad 10.0 |

Project library tables use `${KIPRJMOD}` paths. Keep each project's local libraries together when copying it. The Pico and HAT projects use their own local libraries and installed KiCad models where their project documentation specifies them.

### Project-local libraries

Synth, GPIO, and LPF include local copies of every symbol and footprint used by their designs, plus available STEP models. Each folder resolves its libraries independently through `${KIPRJMOD}`. Their local library assets require KiCad 10.0.1 or newer; the board and schematic generator versions above describe their saved formats.

- [Synth library contents and limits](Wsprry-Pi-Synth-Univ/libraries/README.md)
- [GPIO library contents and limits](WsprryPi-GPIO-Univ/libraries/README.md)
- [LPF library contents and limits](Wsprry-Pi-LPF/libraries/README.md)

The edge-launch SMA option in each library is the wattmeter's Adafruit 1865 part. GPIO now uses it as J83; Synth still uses a different through-hole SMA connector. The switch and through-hole SMA models are included locally. GPIO C11 now uses a local generic KiCad electrolytic model. Remaining model gaps are the unplaced large through-hole capacitor footprint and Synth's Y21 oscillator; LPF's toroid uses a generic axial-inductor visualization.

GPIO C11 is consistently specified as the 47 µF Panasonic part. Synth C11 still carries a 100 µF value with a 47 µF LCSC part number; resolve that purchasing conflict before assembly. Library documentation also records the remaining ERC/DRC findings.

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
