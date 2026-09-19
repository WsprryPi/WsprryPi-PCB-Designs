# GPIO Universal broadband amplifier development plan

This document preserves the development blocks, selected requirements, design
targets, and unresolved decisions for the proposed GPIO-driven broadband
amplifier. It is an engineering specification in progress, not evidence of an
implemented or physically validated amplifier.

The schematic and PCB remain authoritative once these requirements are
implemented. All power, spectral, thermal, and timing values below are design
targets until they are measured on an identified board revision and assembly.

## Development blocks

1. **Requirements and interfaces** — freeze the supported Raspberry Pi family,
   GPIO source, waveform, power, output, control, load, spectral, mechanical,
   and qualification contracts.
2. **GPIO selection** — route either GPIO4 or GPIO20 to one amplifier input with
   a user-set jumper and no electrical connection between the two GPIOs.
3. **Input protection and buffering** — provide a quantitatively high-impedance,
   low-capacitance, partial-power-down-safe 3.3 V input.
4. **DC removal and waveform conditioning** — establish the required bias and
   drive waveform from 135 kHz through 144 MHz without corrupting the low
   endpoint or overdriving the PA.
5. **Fixed drive scaling** — reduce the GPIO waveform to the safe full-scale PA
   drive for the fixed-power revision-one signal path.
6. **Fixed-power interface** — omit selectable attenuation from revision one;
   lower-power operation uses a qualified external 50-ohm attenuator after J83.
7. **Fail-safe amplifier enable** — implement a default-off hardware enable
   controlled by WsprryPi and independent of whether an RF clock is present.
8. **Wideband PA core** — select and implement the THS3491 package, gain,
   feedback, compensation, rail voltage, stability, and thermal layout.
9. **Output isolation and protection** — keep the PA stable with the selected
   LPFs and loads, control DC offset, and tolerate the specified mismatch.
10. **LPF interface** — retain the existing manual plug-in J81/J82 interface
    for one band-specific filter at a time; omit automatic filter switching.
11. **Bipolar DC/DC supply** — generate the fixed PA rails from the Raspberry Pi
    5 V header supply while controlling ripple, switching emissions, startup,
    and shutdown.
12. **Header power management** — distribute pins 2 and 4, grounds, bulk
    capacitance, inrush, undervoltage behavior, and no-backfeed behavior.
13. **Monitoring and protection** — define rail, current, junction-temperature,
    and fault handling needed to protect the PA and host.
14. **WsprryPi control interface** — assign amplifier enable and any status GPIO
    without conflicting with the RF source or other configured functions; the
    revision-one LPF requires no control GPIO.
15. **PCB, mechanical, and thermal implementation** — fit the Zero-sized HAT
    outline on a two-layer PCB, with RF, power, and control routing on L1 and an
    essentially continuous ground-reference and thermal-spreading plane on L2.
16. **Qualification fixtures and procedure** — measure input loading, output
    power, harmonics, spurs, leakage, switching, supply demand, temperature,
    stability, and load mismatch on each identified Pi model used for physical
    validation and across the tested bands.

### Remaining circuit building blocks

After the GPIO selection and GPIO clock input buffer, seven distinct circuit
building blocks remain. This is a circuit-level grouping of the development
roadmap above, not an additional sequence of work:

1. **Signal coupling and fixed drive conditioning** — combine development
   blocks 4 and 5 to remove DC, establish the required bias, and scale the
   buffered clock to the PA's safe full-drive level.
2. **Fail-safe amplifier enable and supervision** — combine development blocks
   7 and 14 around the GPIO23 control receiver, default-off behavior, 3.3 V
   supervision, and THS3491 power-down control.
3. **Wideband PA core** — implement development block 8 around the THS3491,
   including gain, feedback, compensation, stability, and thermal design.
4. **PA output conditioning and protection** — implement development block 9,
   including output isolation, DC blocking, stability with the plug-in LPFs,
   and the specified mismatch tolerance.
5. **Bipolar DC/DC supply** — implement development block 11 to generate the PA
   rails from the Pi's 5 V header supply.
6. **Header power input and distribution** — implement development block 12,
   including both 5 V pins, bulk capacitance, inrush, undervoltage, grounding,
   and no-backfeed behavior.
7. **Monitoring and protection** — implement development block 13 for the rail,
   current, temperature, and fault functions required to protect the PA and Pi.

Development block 6 is a fixed-power architectural constraint, block 10 uses
the existing J81/J82 LPF interface, block 15 is PCB/mechanical/thermal
implementation, and block 16 is qualification. They therefore do not add
separate circuit building blocks to the seven above.

## Block 1: requirements and interfaces

### Requirement status

| Requirement | Current specification | Status |
| --- | --- | --- |
| Supported hosts | Universal-use design target for all Raspberry Pi computers with the standard 40-pin GPIO header | Selected |
| Host qualification | Testing every Pi model is not required; record the exact models physically validated and treat other compatible models as an unverified design target | Selected |
| Mechanical outline | Zero-sized HAT outline; universal electrically across the 40-pin family | Selected |
| PCB construction | Two copper layers; the design must not depend on internal power or ground planes | Selected |
| RF source pins | GPIO4 on physical pin 7 or GPIO20 on physical pin 38 | Selected |
| GPIO selection | User-set jumper; the two GPIOs must never be electrically combined | Selected |
| Jumper states | GPIO4, GPIO20, or no jumper/safe open; selection is not changed during operation | Selected |
| RF input voltage | Nominal 0 V to 3.3 V GPIO waveform; 5 V is available for board power but is not a GPIO signal level | Selected |
| HAT supply voltage | 4.75 V through 5.25 V at header pins 2 and 4 | Selected |
| HAT current budget | 700 mA full-power design target; 1.0 A maximum continuous or during startup for the complete board | Selected |
| Input frequency | 135 kHz through 144 MHz | Selected |
| RF clock duty cycle | 50% nominal high/low duty cycle; actual tolerance is established from source measurements | Selected with validation pending |
| Transmitter duty cycle | 100% continuous-duty design requirement | Selected |
| GPIO drive | Qualify full performance at the 2 mA drive setting; tolerate the 16 mA setting without damage, instability, or invalid control behavior | Selected |
| Input resistance | At least 10 kOhm DC; target 47 kOhm to 100 kOhm in the implemented input | Selected |
| Input capacitance | No more than 3 pF total added HAT capacitance at the selected GPIO, including jumper, route, protection, and receiver | Selected |
| Output adjustment | Fixed full-power signal path in revision one; no software-selectable or switched attenuation | Selected |
| LPF arrangement | One manually installed, band-specific plug-in LPF on the existing J81/J82 interface; no automatic or software-controlled switching | Selected |
| Inactive source | The RF GPIO is an input when WsprryPi is not transmitting | Selected |
| Inactive amplifier | The PA is independently disabled when WsprryPi is not transmitting | Selected |
| Amplifier control | WsprryPi `Use Amp`, BCM GPIO23 on physical pin 16, active high | Selected |
| Enable receiver | SN74LVC1G17DBVR Schmitt buffer powered from Pi 3.3 V, with partial-power-down `Ioff` behavior | Selected |
| Enable pull-downs | 47 kOhm from the buffer input to ground; 10 kOhm from THS3491 PD to ground | Selected |
| 3.3 V supervision | TLV803EB29DBZR, 2.93 V threshold, open-drain active-low output clamping THS3491 PD | Selected |
| GPIO back-drive | No more than 10 uA into GPIO4, GPIO20, GPIO23, or the Pi 3.3 V rail from the HAT in any power state | Selected |
| Initial modes | WSPR and all WsprryPi QRSS modes | Selected |
| Future mode | Preserve a fast enough signal path for later Hellschreiber support | Selected |
| Output load | Nominal 50 ohms | Selected |
| Rated pre-LPF output | 1.0 W from 135 kHz through 70 MHz; 0.5 W above 70 MHz through 144 MHz | Selected |
| Load mismatch | Stable and undamaged during continuous operation below 3:1 VSWR at any phase; rated output is required only into nominal 50 ohms | Selected |
| Fault loads | Open- and short-circuit survival are outside the revision-one requirement | Selected |
| Ambient rating | Full rated output from 0 degrees C through 40 degrees C ambient in still air | Selected |
| External cooling | No assumed Pi fan, external airflow, or external heatsink; board-owned copper and heat spreading are permitted | Selected |
| Disabled RF | Functional target is zero; acceptance is no detectable output above the calibrated conducted measurement floor | Selected |

"All Raspberry Pi models" in this specification means models that expose the
standard 40-pin HAT connector. Original 26-pin Model A and Model B boards and
bare Compute Modules are outside the direct mechanical interface. Zero models
without a populated header require a header to be installed. Software clock
generation, frequency accuracy, and the highest usable frequency can vary by
model. Physical results apply only to the identified Pi models tested; they do
not convert the universal-use design target into evidence for every model.
This is amateur-radio equipment, so experimentation on otherwise compatible,
untested hosts is expected.

GPIO4 and GPIO20 both have GPCLK0 alternate functions in the Broadcom-family
and RP1 peripheral tables, although their alternate-function numbers and clock
providers differ by platform.

### GPIO selection jumper

Use one three-pin, 2.54 mm jumper header. Connect the center pin to the
high-impedance amplifier input and the two outer pins separately to GPIO4 and
GPIO20. A single shunt selects one source; removing the shunt is the safe-open
state. The jumper must never provide an electrical connection between the two
GPIOs and must not be moved during operation.

Fit a 100 kOhm pull-down on the amplifier-input side of the selector so the
safe-open state cannot leave the receiver input floating. This resistor is part
of the frozen RF-input loading contract, not the separate GPIO23 amplifier-
enable pull-down. Clearly identify GPIO4 and GPIO20 on the silkscreen.

### GPIO input-loading targets

The input shall be designed for:

- **10 kOhm minimum DC resistance**, with 47 kOhm to 100 kOhm preferred for the
  actual bias or pull network.
- **3 pF maximum total HAT input capacitance** at the selected GPIO, including
  the header/jumper route, ESD or clamp network, and receiver input.
- Full operation at the Raspberry Pi **2 mA drive setting** and safe operation
  at every supported setting through 16 mA.

At 3.3 V and 144 MHz, 3 pF represents an illustrative capacitive charging
current of:

```text
I = C x V x f
  = 3 pF x 3.3 V x 144 MHz
  = 1.43 mA
```

Its reactance at 144 MHz is approximately 368 ohms. A 10 kOhm DC load adds at
most 0.33 mA while the GPIO is high. These comparisons leave useful margin
around the 2 mA qualification setting, but the GPIO drive setting is not a
hard current limiter. Actual edge shape, thresholds, and loading must be
recorded for each Pi model that is physically tested.

### RF clock duty and transmitter duty

The two duty-cycle requirements are independent:

```text
RF clock duty cycle:   approximately 50% of every carrier cycle high
Transmitter duty cycle: up to 100% of elapsed time transmitting
```

For example, a continuous 144 MHz transmission contains a 3.3 V GPIO high
state for approximately half of each 6.94 ns RF period, while the transmitter
can remain active continuously.

### Input edge behavior

Rise time is the time required for a GPIO edge to move from low to high; fall
time is the reverse. Overshoot and undershoot are brief excursions above 3.3 V
or below ground caused by package, connector, trace, and jumper inductance.
They matter because repeated threshold crossings can create unwanted RF edges,
and excessive excursions can forward-bias input protection structures.

Block 1 does not impose an unsupported synthetic rise/fall-time number. The
input shall instead:

- accept the actual GPIO waveform produced at the 2 mA setting on each
  supported Pi family through 144 MHz;
- use an input device with suitable high-speed bandwidth, 3.3 V thresholds,
  partial-power-down protection, and margin beyond the expected GPIO swing;
- produce one clean internal transition for each source edge; and
- be qualified by measuring 10%-to-90% rise/fall time, overshoot, undershoot,
  and threshold crossings at the HAT input.

Source damping and protection values are selected after those measurements.
The design must not assume that a nominally digital waveform remains an ideal
square wave at 144 MHz and 2 mA.

### Revision-one power control

Revision one uses a fixed full-power signal path with no software-selectable
attenuator. WsprryPi's GPIO `Power Level` setting controls source-pad drive
strength and shall not be treated as calibrated amplifier-output control. The
qualified GPIO drive setting remains 2 mA.

When less RF power is required, use a qualified external 50-ohm attenuator
after J83. Optional unpopulated input-scaling footprints are permitted for
future engineering work only if they add no loading or discontinuity to the
assembled revision-one production path. Adding selectable attenuation later
requires a new hardware/software interface and its own RF qualification.

### Revision-one LPF interface

Retain the existing two-header plug-in filter interface. J81 is the PA-side,
pre-LPF connection and J82 is the post-LPF connection leading to final output
connector J83. The frozen pinout is:

| Header | Pins 1 and 4 | Pins 2 and 3 |
| --- | --- | --- |
| J81 | Ground | Pre-LPF PA output (`FINAL_OUT`) |
| J82 | Ground | Post-LPF output (`RF_OUT`) to J83 |

This pinout matches the existing Wsprry-Pi-LPF board: its J1 pins 2 and 3 are
the filter input, J2 pins 2 and 3 are the filter output, and pins 1 and 4 on
both headers are ground.

Revision one accepts exactly one manually selected, band-specific LPF at a
time. It includes no relay, analog switch, filter-selection GPIO, software
selection, or automatic filter identification. The transmitter must be
disabled before installing, removing, or changing a filter. Operation without
a filter, or with a filter not qualified for the selected frequency and power,
is prohibited; revision one provides no electronic interlock for this operator
requirement.

Treat the J81 transition as the pre-LPF measurement plane and J83 as the final
post-LPF 50-ohm output plane. Each filter assembly must be qualified for its
intended band, continuous power, insertion loss, harmonic rejection, return
loss, connector current, and effect on PA stability. Record the installed
filter identity during conducted qualification.

### GPIO and header power domains

The RF signal is always a 3.3 V GPIO signal. The board is powered only from the
Pi header: the GPIO-side receiver and control logic use the 3.3 V rail, while
the PA and DC/DC converter use the 5 V rail on physical pins 2 and 4 with
multiple ground pins. There is no separate amplifier power input. The 3.3 V
rail shall not power the PA or converter.

The frozen HAT allocation is 1.0 A maximum from the combined 5 V header pins
for the complete board, both continuously and during startup. The full-power
design target is no more than 700 mA, leaving 300 mA of board-level margin.
Use converter soft-start or input-current limiting so bulk capacitance does not
violate the startup limit. These limits apply at 100% transmit duty over a
4.75 V to 5.25 V input range.

The upstream supply must provide the host's own worst-case demand plus the HAT
allocation. A capable Pi supply does not remove the need to qualify the
connector, board power path, voltage drop, and temperature on each Pi family.
An out-of-range or collapsing 5 V input shall disable the PA cleanly without
uncontrolled RF, host undervoltage, or a host reboot caused by the HAT.

No amplifier, protection, clamp, pull-up, test connection, or control circuit
may provide a path from 5 V or a PA rail into a GPIO or the Pi 3.3 V rail. With
the 3.3 V rail absent and 5 V present, HAT-sourced current into each of GPIO4,
GPIO20, GPIO23, and the Pi 3.3 V rail shall not exceed 10 uA. Input parts shall
have specified partial-power-down or `Ioff` behavior.

A missing, falling, or undervoltage 3.3 V control rail shall force the PA
disabled even if the 5 V input and PA rails remain present. Qualification shall
cover power-up, normal shutdown, brownout, and every RF-selector jumper state.

### Thermal rating boundary

The full-power ratings apply from 0 degrees C through 40 degrees C ambient at
100% transmit duty in still air. They shall not depend on a Pi fan, host
airflow, or an external heatsink. PCB copper, thermal vias, and any heat
spreader supplied as part of the HAT are part of the board design.

Operation above 40 degrees C ambient is experimental and carries no guaranteed
power rating. The protection design shall prevent the THS3491 junction from
exceeding 125 degrees C; controlled shutdown is acceptable when that limit
cannot otherwise be maintained. These are design requirements until confirmed
on an identified assembly under a documented thermal setup.

### Rated RF output targets

Rated power means **fundamental RF power into a nominal 50-ohm load at the PA
output reference plane immediately before the LPF**. The ratings apply during
continuous transmission across the complete 4.75 V to 5.25 V input range.
Post-LPF delivered power at J83 is the measured pre-LPF power minus the actual
filter and interconnect loss.

| Frequency or band group | Pre-LPF fundamental design rating | Design note |
| --- | ---: | --- |
| 135 kHz through 70 MHz, including 2200 m through 4 m | 1.0 W | 20 Vpp and 200 mA peak into 50 ohms |
| Above 70 MHz through 144 MHz | 0.5 W | 14.1 Vpp and 141 mA peak into 50 ohms |
| 144 MHz / 2 m stretch goal | 0.75 W | 17.3 Vpp and 173 mA peak into 50 ohms |

The THS3491's typical 8000 V/us slew-rate figure gives an illustrative
sinusoidal limit near 0.78 W at 144 MHz. This supports 0.75 W as a stretch goal,
not as a guaranteed rating. It shall not be published as a rating unless
physical testing demonstrates it. The specified 0.5 W minimum preserves margin for
gain, loading, supply headroom, temperature, and distortion. All rows remain
design requirements until measured.

### WsprryPi amplifier enable

WsprryPi already supports a configurable amplifier GPIO, a configurable
active-high/active-low polarity, assertion at transmission start, and
deassertion on terminal, startup-quiesce, and process-shutdown paths.

The WsprryPi software/control contract and revision-one hardware interface are
frozen as follows.

| Item | Current value | Status |
| --- | --- | --- |
| Control GPIO | BCM GPIO23, physical pin 16 | Selected |
| WsprryPi setting | `Use Amp = true` | Selected |
| Polarity | Active high | Selected |
| Idle/default | Hardware pull-downs hold the amplifier disabled | Selected |
| GPIO-side pull-down | 47 kOhm at the control-buffer input | Selected |
| PD-side pull-down | 10 kOhm directly from THS3491 PD to ground | Selected |
| Enable buffer | SN74LVC1G17DBVR, powered from Pi 3.3 V | Selected |
| Buffer-to-PD resistor | 3.3 kOhm series resistor | Selected |
| 3.3 V supervisor | TLV803EB29DBZR; 2.93 V threshold; open-drain active-low reset | Selected |
| THS3491 reference | REF tied directly to ground | Selected |
| Converter state | PA rails remain established; TX enable does not start the DC/DC converter | Selected |

GPIO23 is not one of the RF outputs or the current default LED/shutdown pins.
WsprryPi's GPIO conflict validation must continue to prevent it from also being
assigned to LED, shutdown, or band-selection service.

Active-high control is selected even though WsprryPi's stock amplifier
polarity is active-low. A physical pull-down gives a simple default-off state
during boot, reset, program exit, or a disconnected control pin. The project
configuration must explicitly select active-high amplifier control.

Implement the control path as:

```text
GPIO23, pin 16 ----+----> SN74LVC1G17 A
                   |
                 47 kOhm
                   |
                  GND

Pi 3.3 V --------> SN74LVC1G17 VCC
SN74LVC1G17 Y ---- 3.3 kOhm ----+----> THS3491 PD
                                |
                              10 kOhm
                                |
                               GND

Pi 3.3 V --------> TLV803EB29DBZR VDD
TLV803EB29 RESET ----------------+  (open-drain undervoltage clamp)
THS3491 REF -------------------- GND
```

Place one 100 nF ceramic bypass capacitor directly at each logic or supervisor
VCC/VDD pin. The SN74LVC1G17 is a noninverting Schmitt buffer, so GPIO23 high
enables the PA. Its `Ioff` specification makes its output high impedance when
the Pi 3.3 V supply is absent. The separate 10 kOhm PD pull-down is mandatory:
the THS3491 otherwise defaults enabled when PD floats, and its specified
25 uA maximum low-state bias current develops no more than 0.25 V across
10 kOhm, below the 0.8 V disable threshold.

The 3.3 kOhm/10 kOhm network produces approximately 2.5 V at PD from a 3.3 V
high, above the THS3491's 1.5 V enable threshold, while limiting contention
current when the TLV803EB29 supervisor clamps PD low. The supervisor holds the
PA disabled until the Pi 3.3 V rail has crossed its 2.93 V threshold and release
delay, and reclamps PD during brownout. Below the supervisor's guaranteed
output range, the unpowered buffer and 10 kOhm pull-down provide the passive
default-off state.

The circuit intentionally adds no normal transmit-enable delay. Qualification
shall verify the PD voltage margins, GPIO23 and Pi-rail back-drive current,
power sequencing, brownout response, and timing over component tolerances and
temperature before the circuit is considered physically validated.

The THS3491 datasheet specifies a typical 50 ns turn-on delay to 90% and 4 us
turn-off delay to 10% with its rails already established. Therefore the board
targets are:

- no required WsprryPi software pre-enable delay;
- no more than 1 us from control assertion to usable PA operation; and
- no more than 10 us from control deassertion to the disabled output state.

These are board-level acceptance targets, not yet measured results. The design
must not use the comparatively slow DC/DC startup as the transmit enable.

### Modulation and keying

The amplifier-enable GPIO arms the PA for an entire transmission; it is not the
per-symbol modulator.

- WSPR presents a continuous clock whose frequency changes between symbols.
- FSKCW and DFCW can remain continuous while changing frequency.
- On/off-keyed QRSS starts and stops the RF clock while the PA remains armed.
- Future Hellschreiber uses the RF clock or a separately qualified fast signal
  gate, not repeated DC/DC startup or PA supply cycling.

Consequently, there is no QRSS minimum on/off interval requirement for the
amplifier-enable GPIO. There is a separate requirement that loss and return of
the RF input while the PA is armed must not cause oscillation, unintended RF,
or unacceptable keying transients.

### Disabled-state RF

The functional target is zero RF output. Physical hardware cannot demonstrate
mathematical zero, so acceptance shall be expressed as:

> No discrete carrier, harmonic, switching spur, or self-oscillation is
> detectable above the calibrated conducted measurement floor at the PA output
> or final output while the amplifier is disabled.

Qualification must test both the normal idle condition, where the selected RF
GPIO is an input, and an adversarial condition with an input clock present
while amplifier enable is inactive. The THS3491 power-down function alone is
not a guaranteed RF isolator or high-impedance output, so the input scaling and
enable architecture must keep the disabled device from being driven back on.
Record the calibrated floor, receiver settings, attenuation, bandwidth, and
reference planes with each result. The numerical floor is a property of the
qualification setup, not a remaining user-facing design choice.

### Load mismatch

The PA shall remain stable and undamaged during continuous operation into any
load having VSWR below 3:1 at any reflection phase. The rated-power table
applies only into nominal 50 ohms; reduced power or increased distortion under
mismatch is acceptable provided the PA remains stable and undamaged.
Open-circuit and short-circuit survival are outside the revision-one
requirement because those conditions exceed the specified mismatch boundary.

### Spectral reference planes and limits

The GPIO waveform is approximately square and therefore contains strong odd
harmonics before amplification. Two measurement planes are required:

1. **Pre-LPF, at the PA output:** characterize fundamental power, harmonics,
   non-harmonic spurs, converter products, and stability. Strong source
   harmonics are expected here, so this plane does not carry the final
   emissions mask. It must show no autonomous oscillation or unexpected
   non-harmonic output.
2. **Post-LPF, at the final 50-ohm output:** apply the transmitter emissions
   requirements because this is the signal delivered to the antenna system.

For United States amateur operation, the board-level post-LPF design target is
at least 50 dB suppression of every harmonic and discrete spurious emission
relative to the fundamental, and no individual spur above 10 uW. This provides
margin beyond the current 43 dB requirement below 30 MHz and meets the 10 uW
floor referenced for low-power transmitters from 30 MHz through 225 MHz. Keying
must also avoid unnecessary bandwidth, splatter, and key clicks.

Regulatory compliance belongs to the complete transmitter and selected LPF,
not the PA alone. Requirements must be rechecked for the jurisdiction and rules
applicable when the product is used.

## Block 1 status

Block 1 is frozen. Numerical values that depend on the implemented circuit or
test equipment, such as the disabled-output measurement floor and measured
thermal margin, are qualification results rather than unresolved requirements.

## Primary references

- [Raspberry Pi computer hardware and 40-pin GPIO](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [BCM2835 ARM Peripherals](https://datasheets.raspberrypi.com/bcm2835/bcm2835-peripherals.pdf)
- [BCM2711 ARM Peripherals](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf)
- [RP1 Peripherals](https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf)
- [TI THS3491 datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf)
- [TI SN74LVC1G17 datasheet](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf)
- [TI TLV803E datasheet](https://www.ti.com/lit/ds/symlink/tlv803e.pdf)
- [47 CFR 97.307, Emission standards](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97/subpart-D/section-97.307)
- [Repository-level broadband amplifier proposal](../design/raspberry-pi-hat-broadband-rf-amplifier.md)
