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
   drive independently of selectable power control.
6. **Digitally switched attenuation** — provide fixed, repeatable power steps
   ahead of the PA and define their calibration contract.
7. **Fail-safe amplifier enable** — implement a default-off hardware enable
   controlled by WsprryPi and independent of whether an RF clock is present.
8. **Wideband PA core** — select and implement the THS3491 package, gain,
   feedback, compensation, rail voltage, stability, and thermal layout.
9. **Output isolation and protection** — keep the PA stable with the selected
   LPFs and loads, control DC offset, and tolerate the specified mismatch.
10. **LPF interface** — define the immediate post-PA 50-ohm transition, filter
    arrangement, and band-selection boundary.
11. **Bipolar DC/DC supply** — generate the fixed PA rails from the Raspberry Pi
    5 V header supply while controlling ripple, switching emissions, startup,
    and shutdown.
12. **Header power management** — distribute pins 2 and 4, grounds, bulk
    capacitance, inrush, undervoltage behavior, and no-backfeed behavior.
13. **Monitoring and protection** — define rail, current, junction-temperature,
    and fault handling needed to protect the PA and host.
14. **WsprryPi control interface** — assign amplifier enable, attenuation, LPF,
    and status GPIO without conflicting with the RF source or other configured
    functions.
15. **PCB, mechanical, and thermal implementation** — fit the Zero-sized HAT
    outline and preserve the L1 RF, L2 primary ground, L3 power/control, and L4
    secondary ground/thermal layer roles.
16. **Qualification fixtures and procedure** — measure input loading, output
    power, harmonics, spurs, leakage, switching, supply demand, temperature,
    stability, and load mismatch across the supported bands and Pi families.

## Block 1: requirements and interfaces

### Requirement status

| Requirement | Current specification | Status |
| --- | --- | --- |
| Supported hosts | All Raspberry Pi computers with the standard 40-pin GPIO header | Selected |
| Mechanical outline | Zero-sized HAT outline; universal electrically across the 40-pin family | Selected |
| RF source pins | GPIO4 on physical pin 7 or GPIO20 on physical pin 38 | Selected |
| GPIO selection | User-set jumper; the two GPIOs must never be electrically combined | Selected |
| Jumper states | GPIO4, GPIO20, or no jumper/safe open; selection is not changed during operation | Proposed detail |
| RF input voltage | Nominal 0 V to 3.3 V GPIO waveform; 5 V is available for board power but is not a GPIO signal level | Selected |
| Input frequency | 135 kHz through 144 MHz | Selected |
| RF clock duty cycle | 50% nominal high/low duty cycle; actual tolerance is established from source measurements | Selected with validation pending |
| Transmitter duty cycle | 100% continuous-duty design requirement | Selected |
| GPIO drive | Qualify full performance at the 2 mA drive setting; tolerate the 16 mA setting without damage, instability, or invalid control behavior | Selected |
| Input resistance | At least 10 kOhm DC; target 47 kOhm to 100 kOhm in the implemented input | Selected |
| Input capacitance | No more than 3 pF total added HAT capacitance at the selected GPIO, including jumper, route, protection, and receiver | Selected |
| Inactive source | The RF GPIO is an input when WsprryPi is not transmitting | Selected |
| Inactive amplifier | The PA is independently disabled when WsprryPi is not transmitting | Selected |
| Amplifier control | WsprryPi `Use Amp`, BCM GPIO23 on physical pin 16, active high | Selected |
| GPIO back-drive | No deliberate or parasitic back-powering of GPIO4, GPIO20, or the Pi 3.3 V rail in any power state | Proposed engineering requirement |
| Initial modes | WSPR and all WsprryPi QRSS modes | Selected |
| Future mode | Preserve a fast enough signal path for later Hellschreiber support | Selected |
| Output load | Nominal 50 ohms | Selected |
| Load mismatch | Stable, continuous operation for load VSWR below 3:1 at any phase; no oscillation or damage | Selected with output derating unresolved |
| External cooling | No assumed Pi fan or external airflow; board ratings must not depend on host cooling | Proposed interpretation |
| Disabled RF | Functional target is zero output | Selected; measurable acceptance criterion remains open |

"All Raspberry Pi models" in this specification means models that expose the
standard 40-pin HAT connector. Original 26-pin Model A and Model B boards and
bare Compute Modules are outside the direct mechanical interface. Zero models
without a populated header require a header to be installed. Software clock
generation, frequency accuracy, and the highest usable frequency still require
model-specific qualification even though the HAT interface is universal.

GPIO4 and GPIO20 both have GPCLK0 alternate functions in the Broadcom-family
and RP1 peripheral tables, although their alternate-function numbers and clock
providers differ by platform.

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
measured on representative hosts.

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

### GPIO and header power domains

The RF signal is always a 3.3 V GPIO signal. The HAT main-power source is the
5 V header rail on physical pins 2 and 4, using multiple ground pins. The 3.3 V
header rail may power the GPIO-side receiver and control logic, but shall not
power the PA or converter.

The provisional HAT allocation remains 1 A maximum from the 5 V header. The
upstream supply must provide the host's own worst-case demand plus the HAT
allocation. A capable external Pi supply does not remove the need to qualify
the connector, board power path, voltage drop, and temperature on each Pi
family.

No amplifier or control circuit may inject current into a GPIO or the Pi 3.3 V
rail when that rail is absent. Input parts shall be selected for specified
partial-power-down behavior, and this behavior shall be measured with 5 V
present and the Pi 3.3 V rail absent.

### Rated RF output targets

Rated power means **fundamental RF power into a nominal 50-ohm load at the PA
output reference plane immediately before the LPF**. Post-LPF delivered power
is the measured pre-LPF power minus the actual filter and interconnect loss.

| Frequency or band group | Pre-LPF fundamental design rating | Design note |
| --- | ---: | --- |
| 135 kHz through 70 MHz, including 2200 m through 4 m | 1.0 W | 20 Vpp and 200 mA peak into 50 ohms |
| 144 MHz / 2 m | 0.5 W minimum | 14.1 Vpp and 141 mA peak into 50 ohms |
| 144 MHz / 2 m stretch goal | 0.75 W | 17.3 Vpp and 173 mA peak into 50 ohms |

The THS3491's typical 8000 V/us slew-rate figure gives an illustrative
sinusoidal limit near 0.78 W at 144 MHz. This supports 0.75 W as a stretch goal,
not as a guaranteed rating. The specified 0.5 W minimum preserves margin for
gain, loading, supply headroom, temperature, and distortion. All rows remain
design requirements until measured.

### WsprryPi amplifier enable

WsprryPi already supports a configurable amplifier GPIO, a configurable
active-high/active-low polarity, assertion at transmission start, and
deassertion on terminal, startup-quiesce, and process-shutdown paths.

The WsprryPi software/control contract is frozen. Its hardware realization is
shown separately so that choosing the pin and polarity does not prematurely
select a receiver or PA-enable circuit.

| Item | Current value | Status |
| --- | --- | --- |
| Control GPIO | BCM GPIO23, physical pin 16 | Selected |
| WsprryPi setting | `Use Amp = true` | Selected |
| Polarity | Active high | Selected |
| Idle/default | External pull-down holds the amplifier disabled | Proposed engineering requirement |
| Pull-down | 47 kOhm to 100 kOhm at the control receiver | Value remains open |
| PA control | Drive the THS3491 PD function or an equivalent default-off enable stage | Implementation remains open |
| Converter state | PA rails remain established; TX enable does not start the DC/DC converter | Proposed architecture |

GPIO23 is not one of the RF outputs or the current default LED/shutdown pins.
WsprryPi's GPIO conflict validation must continue to prevent it from also being
assigned to LED, shutdown, or band-selection service.

Active-high control is selected even though WsprryPi's stock amplifier
polarity is active-low. A physical pull-down gives a simple default-off state
during boot, reset, program exit, or a disconnected control pin. The project
configuration must explicitly select active-high amplifier control.

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
A numeric leakage limit can be added after the qualification receiver and
attenuation floor are selected.

### Load mismatch

The PA shall remain stable and undamaged during continuous operation into any
50-ohm load having VSWR below 3:1 at any reflection phase. Rated output power
and distortion under mismatch remain to be defined. Open-circuit and
short-circuit survival are not implied by the 3:1 operating requirement and
must be addressed separately if desired.

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

## Remaining Block 1 decisions

- Select the exact external pull-down value and the default-off enable-stage
  implementation for the frozen GPIO23 active-high control interface.
- Select the exact representative Pi revisions used for universal-source
  qualification.
- Set the ambient-temperature boundary for the 100% duty power ratings. No
  external cooling is assumed, but PCB copper, thermal vias, and any board-owned
  heat spreader remain part of the electrical design.
- Decide whether rated output must be maintained throughout the VSWR below 3:1
  region or whether controlled power reduction is acceptable.
- Establish the conducted measurement floor that converts the functional
  zero-output target into a numeric disabled-leakage limit.
- Decide whether open- and short-circuit survival is required in addition to
  the specified VSWR operating region.

## Primary references

- [Raspberry Pi computer hardware and 40-pin GPIO](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [BCM2835 ARM Peripherals](https://datasheets.raspberrypi.com/bcm2835/bcm2835-peripherals.pdf)
- [BCM2711 ARM Peripherals](https://datasheets.raspberrypi.com/bcm2711/bcm2711-peripherals.pdf)
- [RP1 Peripherals](https://datasheets.raspberrypi.com/rp1/rp1-peripherals.pdf)
- [TI THS3491 datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf)
- [47 CFR 97.307, Emission standards](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-97/subpart-D/section-97.307)
- [Repository-level broadband amplifier proposal](../design/raspberry-pi-hat-broadband-rf-amplifier.md)
