# Raspberry Pi HAT broadband RF amplifier — proposed design

This proposal defines the amplifier architecture and engineering requirements. The schematic, component selection, and hardware validation are incomplete; all output and supply figures are provisional design targets.

## Goals and constraints

Build a compact, solid-state Raspberry Pi HAT that accepts a 3.3 V clock/RF source and supplies up to 1 W RF before the external low-pass filter (LPF).

- Cover **135 kHz–144 MHz** with one broadband amplifier circuit.
- Accept either the intended Pi GPIO clock output or a Si5351 clock output.
- Design for universal use with every Raspberry Pi model family having the
  standard 40-pin GPIO header. Testing every model is not required; measured
  results apply only to the identified hosts tested, and amateur-radio
  experimentation on other compatible hosts is expected.
- Use the Pi’s 5 V header supply, with sufficient system power headroom.
- Provide hardware transmit enable and a fixed full-power revision-one signal path.
- Require no end-user tuning: no adjustable resistors, capacitors, coils, or manual alignment.
- Use one fixed DC/DC supply and fixed broadband supply decoupling across the frequency range.
- Place one manually selected plug-in band LPF immediately after the PA using
  the existing J81/J82 interface; revision one has no automatic filter
  switching.
- Allow reduced maximum output at the upper end of the frequency range while preserving coverage and adjustment-free operation.

The proposed PA uses the same broadband circuit and supply decoupling across all bands. The downstream LPF is selected for the operating band.

## Proposed signal and power paths

```text
Pi GPIO clock OR Si5351 clock
              |
High-impedance input buffer/level conditioning
              |
Fixed full-power drive scaling
              |
THS3491-style wideband power amplifier
              |
Manually selected plug-in band LPF at J81/J82 — immediately after PA
              |
50-ohm load/antenna

Pi header 5 V -> fixed DC/DC -> approximately ±12 to ±15 V
                                -> local PA rail decoupling

WsprryPi -> hardware transmit enable
```

The candidate final stage is a THS3491 current-feedback power amplifier, with THS3491DDA proposed for the prototype. Final component selection, package thermal design, feedback values, input interface, and converter topology remain open.

## Input compatibility and drive conditioning

The intended inputs are approximately 3.3 V logic, with Pi GPIO drive settings of 2–16 mA and Si5351 settings of 2/4/6/8 mA. These are source-drive settings, not calibrated RF power levels or constant-current outputs. Pi capabilities and clock-generation methods depend on the exact Pi model; the input requirement does not establish that every Pi can generate every requested frequency.

Use a high-impedance input, so neither source must directly drive a 50-ohm termination. Input capacitance, trace length, edge quality, and protection loading still matter at 144 MHz. Select or connect only one source at a time.

The interface must remove or accommodate the logic signal’s DC offset and establish a suitable PA drive amplitude. A 3.3 V logic waveform cannot simply feed a gain-of-20 stage without substantial scaling. Any AC coupling must preserve the 135 kHz endpoint. Input conditioning and fixed drive scaling must tolerate the actual signal voltage and bias.

## Wideband PA and output target

The proposed circuit uses closed-loop gain around 18–20 V/V, bipolar rails around ±12 to ±15 V, and operation in a nominal 50-ohm output environment without an RF output transformer. These are starting points for design, not fixed component values.

TI lists the THS3491 with a ±7 to ±16 V supply range, typical ±420 mA linear output current, and 8000 V/µs slew rate. Its headline 900 MHz bandwidth applies at 2 Vpp and gain 5; the 320 MHz figure applies at 10 Vpp and gain 5. Those specifications do not establish full-power performance at gain 20 into 50 ohms. See the [TI THS3491 product information](https://www.ti.com/product/THS3491) and [datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf).

For a sine wave into 50 ohms:

| RF power | RMS voltage | Peak voltage | Peak-to-peak voltage |
| --- | ---: | ---: | ---: |
| 100 mW | 2.24 V | 3.16 V | 6.32 V |
| 250 mW | 3.54 V | 5.00 V | 10.0 V |
| 500 mW | 5.00 V | 7.07 V | 14.1 V |
| 1 W | 7.07 V | 10.0 V | 20.0 V |

At 1 W, the sinusoidal load current is 200 mA peak. A series output-termination resistor would consume voltage headroom and dissipate power; “50-ohm environment” does not mean a 50-ohm series resistor can be added without revisiting the output target.

The frozen pre-LPF fundamental-power targets into nominal 50 ohms are **1.0 W
from 135 kHz through 70 MHz** and **0.5 W above 70 MHz through 144 MHz** during
continuous transmission across the 4.75–5.25 V input range. A **0.75 W target
at 144 MHz** remains a stretch goal and shall not be published as a rating
unless physical testing demonstrates it. Delivered power at J83 is the
measured pre-LPF power minus the actual selected-filter and interconnect loss.

These ratings apply from 0 degrees C through 40 degrees C ambient at 100%
transmit duty in still air, without relying on a Pi fan, host airflow, or an
external heatsink. Board-owned copper, thermal vias, and heat spreading are
part of the design. Operation above 40 degrees C is experimental and has no
guaranteed power rating. Protect the THS3491 from exceeding 125 degrees C
junction temperature, using controlled shutdown when necessary.

Rated power is required only into nominal 50 ohms. The PA must remain stable
and undamaged during continuous operation below 3:1 VSWR at every reflection
phase, but reduced power or increased distortion under mismatch is acceptable.
Open- and short-circuit survival are outside the revision-one requirement.

Using the typical slew rate for an initial estimate:

```text
SR = 2πf × Vpeak
Vpeak ≈ 8 × 10^9 / (2π × 144 × 10^6) ≈ 8.84 V
P ≈ Vpeak² / (2 × 50) ≈ 0.78 W
```

This is an illustrative sinusoidal slew-rate estimate, not a guaranteed output ceiling or a low-distortion rating. Gain, load, supply headroom, temperature, and waveform affect actual performance.

The inputs are clock waveforms with harmonics. Define measured power consistently: distinguish total unfiltered RF power, fundamental power at the PA output, and delivered power after LPF loss. The sine-wave calculations above describe fundamental-power requirements, not total square-wave power.

## Fixed DC/DC rails and 5 V header power

Generate one fixed bipolar supply from 5 V, initially considering ±12 to ±15 V. Bipolar rails allow ground-centered input/output operation and may avoid a large output coupling capacitor, subject to DC-offset and fault analysis. Do not change supply rails or supply-filter components by band.

Physical header pins **2 and 4** are the only 5 V supply connections; there is
no separate amplifier power input. They are not programmable GPIO outputs. Use
both power pins and multiple ground pins with suitable copper and connector
current capacity. Power the GPIO receiver and control logic from the Pi 3.3 V
rail and the PA and converter from 5 V. Available HAT power depends on the Pi
supply, Pi workload, other peripherals, cable drop, board power path, and
connector limits.

No circuit may feed a GPIO or the Pi 3.3 V rail from 5 V or a PA rail. With
3.3 V absent and 5 V present, HAT-sourced current into GPIO4, GPIO20, GPIO23,
or the Pi 3.3 V rail shall not exceed 10 uA per connection. Use devices with
specified partial-power-down or `Ioff` behavior. A missing, falling, or
undervoltage 3.3 V rail must force the PA disabled while its power rails remain
energized.

The frozen input range is **4.75–5.25 V** at the HAT connector. Estimated
demand near 1 W RF is **0.4–0.7 A at 5 V**; use **700 mA** as the full-power
design target and **1.0 A** as the absolute board limit, both continuously and
during startup. These limits cover the amplifier, converter losses,
buffer/control loads, startup, and 100% transmit duty.

Use converter soft-start or input-current limiting so bulk capacitance does not
exceed the 1.0 A startup limit. An out-of-range or collapsing 5 V input must
disable the PA cleanly without uncontrolled RF, Pi undervoltage, or a Pi reboot
caused by the HAT.

For illustration, 1 W RF at 40% complete-chain efficiency requires 0.50 A from 5 V; at 30%, it requires 0.67 A. Efficiency must be established for the implemented circuit and each operating condition.

Raspberry Pi recommends 5 V/3 A for Pi 4 and 5 V/5 A for Pi 5. A Pi 5 system should use the official 27 W supply or an equivalent supporting the required 5 V/5 A mode, with overall load headroom checked. The Pi 5’s **600 mA restriction concerns downstream USB power** with a lower-power supply; it is not a published 600 mA limit on the HAT’s 5 V header pins. See [Raspberry Pi supply recommendations](https://www.raspberrypi.com/documentation/computers/getting-started.html) and [hardware power documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

Provide local bulk capacitance and the converter’s specified ceramic input network. An initial bulk-capacitance range is 470–1000 µF; size it against transient response and inrush. Select rail bypass components and placement for impedance across the operating spectrum. This is one fixed supply network, independent of band.

## Revision-one power control

Revision one uses fixed full-power drive scaling and contains no
software-selectable or switched attenuator. WsprryPi's GPIO `Power Level`
setting controls source-pad drive strength and is not calibrated RF-output
control; the qualified setting for this board is 2 mA.

Use a qualified external 50-ohm attenuator after J83 when less power is needed.
Optional unpopulated input-scaling footprints may be included for future
engineering only if they add no loading or discontinuity to the assembled
production path. Selectable attenuation would require a future hardware and
software revision plus a new RF qualification campaign.

Use fixed components and, if needed, stored manufacturing calibration
constants. Provide hardware transmit enable with a defined default-off state.
The disabled-state target is zero RF. Acceptance means no carrier, harmonic,
spur, or oscillation detectable above the calibrated conducted measurement
floor. Record that floor and the complete measurement configuration with each
result; amplifier power-down alone is not proof of zero output.

## Fail-safe hardware transmit enable

Use WsprryPi's active-high BCM GPIO23 on physical pin 16. Connect GPIO23 to the
input of a [TI SN74LVC1G17DBVR Schmitt buffer](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf),
powered from the Pi 3.3 V rail, and fit a 47 kOhm pull-down from that input to
ground. Connect the buffer output through 3.3 kOhm to the THS3491 PD pin, fit a
separate 10 kOhm pull-down directly from PD to ground, and tie THS3491 REF to
ground. Bypass the buffer supply locally with 100 nF.

Monitor the Pi 3.3 V rail with a
[TI TLV803EB29DBZR](https://www.ti.com/lit/ds/symlink/tlv803e.pdf), using its
2.93 V threshold and open-drain active-low reset output to clamp THS3491 PD
low. Bypass the supervisor supply locally with 100 nF. Its startup-release
delay applies only when the 3.3 V rail becomes valid, not to each transmission.

The noninverting buffer preserves the selected active-high polarity and has
specified partial-power-down `Ioff` behavior. If 3.3 V is absent, the buffer
output becomes high impedance and the 10 kOhm PD pull-down holds the PA off.
The THS3491's specified maximum 25 uA low-state PD bias develops no more than
0.25 V across that resistor, below its 0.8 V disable threshold. When enabled,
the 3.3 kOhm/10 kOhm network produces approximately 2.5 V at PD, above the
1.5 V enable threshold. The series resistor also limits current while the
supervisor clamps PD during startup or brownout.

This circuit adds no intentional delay to normal GPIO23 transmit switching;
the PA rails remain established. Qualify PD voltage margin, GPIO and Pi-rail
back-drive current, power sequencing, supervisor response, and turn-on/turn-off
timing over voltage, component tolerance, and temperature.

## LPF immediately after the PA

Retain the existing manual plug-in J81/J82 interface and place the selected LPF
directly after the amplifier with a short RF connection. J81 pins 2 and 3 carry
the pre-LPF PA output, J82 pins 2 and 3 carry the post-LPF signal to J83, and
pins 1 and 4 of both headers are ground. This matches J1 and J2 on the existing
Wsprry-Pi-LPF board.

Revision one accepts one manually selected, band-specific LPF at a time and
contains no relay, analog switch, selection GPIO, software selection, or
automatic filter identification. Disable transmission before installing,
removing, or changing the filter. Do not transmit without a filter or with a
filter that is not qualified for the selected frequency and power; revision
one provides no electronic interlock for this operator requirement.

The LPF rejects source harmonics and amplifier-generated distortion before the
antenna. It does not automatically correct an unstable PA or provide broadband
impedance matching. Treat J81 as the pre-LPF measurement plane and J83 as the
final post-LPF 50-ohm output plane. Record the installed filter identity during
qualification.

Verify the PA with the actual LPFs: a filter can present a reactive, reflective load outside its passband. The design must tolerate that load while meeting output and spectral requirements. The amplifier hardware remains broadband even though LPF selection is band-dependent.

## Required two-layer PCB construction

The amplifier must be implementable on a **two-copper-layer PCB**. The design
must not depend on internal power, RF-reference, shielding, or thermal planes.

| Layer | Intended use |
| --- | --- |
| **L1** | Components; short RF, PA-feedback, power, and control routes; local ground copper |
| **L2** | Essentially continuous RF ground reference, control return, shielding, and thermal spreading |

Keep L2 continuous beneath the input path, PA feedback and output paths, RF
connectors, and DC/DC switching-current loops. Route power and control on L1;
use L1 zero-ohm bridges where useful rather than cutting the L2 return plane.
Any unavoidable L2 route requires an explicit return-path review and must not
cross beneath an RF or fast-switching path.

Connect L1 ground copper to L2 with dense stitching vias, particularly near the
PA, RF connectors, board edges, and converter boundary. Use thermal vias and
back-side copper as permitted by the selected device's exposed-pad electrical
connection; do not assume that a thermal pad is ground.

Keep feedback components and rail bypass capacitors physically close to the PA.
Keep converter switching-current loops compact and away from sensitive RF
nodes. Calculate RF trace geometry from the selected two-layer fabrication
stackup and validate the implemented return paths, temperature, and RF behavior
on the physical board.

## Remaining engineering work

1. Select the exact Pi/source interface, buffer, PA package, fixed rails, and DC/DC topology; complete the component-level schematic.
2. Establish PA gain, fixed input scaling, coupling, feedback stability, and compatibility with the actual LPF impedances.
3. Measure fundamental power, harmonics, spurs, and transmit-enable leakage across 135 kHz–144 MHz with both source types.
4. Verify 5 V demand, startup/inrush, rail ripple, Pi voltage stability, and PA/converter temperature during sustained operation.
5. Confirm the upper-frequency derating and publish only measured power ratings.
