# Raspberry Pi HAT broadband RF amplifier — proposed design

This proposal defines the amplifier architecture and engineering requirements. The schematic, component selection, and hardware validation are incomplete; all output and supply figures are provisional design targets.

## Goals and constraints

Build a compact, solid-state Raspberry Pi HAT that accepts a 3.3 V clock/RF source and supplies up to 1 W RF before the external low-pass filter (LPF).

- Cover **135 kHz–144 MHz** with one broadband amplifier circuit.
- Accept either the intended Pi GPIO clock output or a Si5351 clock output.
- Use the Pi’s 5 V header supply, with sufficient system power headroom.
- Provide software-selectable power levels and transmit enable.
- Require no end-user tuning: no adjustable resistors, capacitors, coils, or manual alignment.
- Use one fixed DC/DC supply and fixed broadband supply decoupling across the frequency range.
- Place the selected band LPF immediately after the PA.
- Allow reduced maximum output at the upper end of the frequency range while preserving coverage and adjustment-free operation.

The proposed PA uses the same broadband circuit and supply decoupling across all bands. The downstream LPF is selected for the operating band.

## Proposed signal and power paths

```text
Pi GPIO clock OR Si5351 clock
              |
High-impedance input buffer/level conditioning
              |
Fixed drive scaling + digitally switched attenuation
              |
THS3491-style wideband power amplifier
              |
Selected band LPF — immediately after PA
              |
50-ohm load/antenna

Pi header 5 V -> fixed DC/DC -> approximately ±12 to ±15 V
                                -> local PA rail decoupling

Software -> attenuation selection and hardware transmit enable
```

The candidate final stage is a THS3491 current-feedback power amplifier, with THS3491DDA proposed for the prototype. Final component selection, package thermal design, feedback values, input interface, and converter topology remain open.

## Input compatibility and drive conditioning

The intended inputs are approximately 3.3 V logic, with Pi GPIO drive settings of 2–16 mA and Si5351 settings of 2/4/6/8 mA. These are source-drive settings, not calibrated RF power levels or constant-current outputs. Pi capabilities and clock-generation methods depend on the exact Pi model; the input requirement does not establish that every Pi can generate every requested frequency.

Use a high-impedance input, so neither source must directly drive a 50-ohm termination. Input capacitance, trace length, edge quality, and protection loading still matter at 144 MHz. Select or connect only one source at a time.

The interface must remove or accommodate the logic signal’s DC offset and establish a suitable PA drive amplitude. A 3.3 V logic waveform cannot simply feed a gain-of-20 stage without substantial scaling. Any AC coupling must preserve the 135 kHz endpoint. Input conditioning and any attenuation switches must tolerate the actual signal voltage and bias.

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

The output target is **up to 1 W nominal, with approximately 0.5–0.75 W at 144 MHz**. Frequency-dependent ratings require measurement.

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

Physical header pins **2 and 4** are the 5 V supply connections; they are not programmable GPIO outputs. Use both power pins and multiple ground pins with suitable copper and connector current capacity. Available HAT power depends on the Pi supply, Pi workload, other peripherals, cable drop, board power path, and connector limits.

Estimated demand near 1 W RF is **0.4–0.7 A at 5 V**; reserve **about 1 A for the HAT** as a provisional design budget. Include amplifier quiescent consumption, converter losses, buffer/control loads, startup, and sustained transmit duty cycle when establishing the measured requirement.

For illustration, 1 W RF at 40% complete-chain efficiency requires 0.50 A from 5 V; at 30%, it requires 0.67 A. Efficiency must be established for the implemented circuit and each operating condition.

Raspberry Pi recommends 5 V/3 A for Pi 4 and 5 V/5 A for Pi 5. A Pi 5 system should use the official 27 W supply or an equivalent supporting the required 5 V/5 A mode, with overall load headroom checked. The Pi 5’s **600 mA restriction concerns downstream USB power** with a lower-power supply; it is not a published 600 mA limit on the HAT’s 5 V header pins. See [Raspberry Pi supply recommendations](https://www.raspberrypi.com/documentation/computers/getting-started.html) and [hardware power documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

Provide local bulk capacitance and the converter’s specified ceramic input network. An initial bulk-capacitance range is 470–1000 µF; size it against transient response and inrush. Select rail bypass components and placement for impedance across the operating spectrum. This is one fixed supply network, independent of band.

## Power control

Use digitally switched resistive attenuation ahead of the PA instead of treating source drive-strength settings as calibrated output control.

| Control bits | Additional attenuation | Relative power | Nominal power if full scale is 1 W |
| --- | ---: | ---: | ---: |
| 00 | 0 dB | 100% | 1 W |
| 01 | 6 dB | 25.1% | 251 mW |
| 10 | 12 dB | 6.31% | 63 mW |
| 11 | 18 dB | 1.58% | 16 mW |

The zero-dB setting means no additional selectable attenuation; fixed input scaling is still required. A 3/6/12 dB arrangement could provide eight settings spanning 21 dB. Actual power scales with the measured full-scale output at each frequency and need not track ideal ratios near compression.

Use fixed components and, if needed, stored manufacturing calibration constants. Provide hardware transmit enable with a defined default-off state. Verify off-state RF leakage and switching behavior; amplifier power-down alone is not proof of zero output.

## LPF immediately after the PA

Place the selected LPF directly after the amplifier with a short RF connection. Its role is to reject source harmonics and amplifier-generated distortion before the antenna. It does not automatically correct an unstable PA or provide broadband impedance matching.

Verify the PA with the actual LPFs: a filter can present a reactive, reflective load outside its passband. The design must tolerate that load while meeting output and spectral requirements. The amplifier hardware remains broadband even though LPF selection is band-dependent.

## Proposed four-layer PCB stackup

| Layer | Intended use |
| --- | --- |
| **L1** | RF components, short RF traces, PA feedback and local decoupling |
| **L2** | **Primary uninterrupted RF ground reference plane immediately under L1** |
| **L3** | Power distribution and slow control signals |
| **L4** | **Secondary ground/shield/thermal/control-return plane**, predominantly ground |

**L2 is the critical RF reference.** Keep it close to L1 and continuous beneath RF routes so high-frequency return currents have short paths directly under those routes. Do not route signals through L2 or split it into power islands. L1-to-L2 dielectric thickness and copper geometry determine RF trace impedance and return-path behavior. At 144 MHz, this geometry is part of the circuit.

**L4 supplements L2.** It provides secondary shielding, ground connectivity, thermal spreading, and a nearby return plane for appropriate L3 control routing. It does not replace the adjacent L2 reference for L1 RF traces or the PA feedback/output loop. A few slow signals may use L4 if necessary without compromising required ground continuity.

Connect L1 ground copper, L2, and L4 with **stitching vias**, particularly near the PA, RF connectors, board edges, and converter boundary. Add nearby ground-return vias wherever an RF route changes layers, and use thermal vias as required by the selected PA package.

Keep feedback components and rail bypass capacitors physically close to the PA. Keep converter switching-current loops compact and away from sensitive RF nodes. Preserve L2 return continuity while following device-specific layout guidance for any strictly local clearance needed beneath sensitive pads; review such clearances explicitly rather than introducing broad plane breaks.

## Remaining engineering work

1. Select the exact Pi/source interface, buffer, attenuation switches, PA package, fixed rails, and DC/DC topology; complete the component-level schematic.
2. Establish PA gain, fixed input scaling, coupling, feedback stability, and compatibility with the actual LPF impedances.
3. Measure fundamental power, harmonics, spurs, attenuation accuracy, and transmit-enable leakage across 135 kHz–144 MHz with both source types.
4. Verify 5 V demand, startup/inrush, rail ripple, Pi voltage stability, and PA/converter temperature during sustained operation.
5. Confirm the upper-frequency derating and publish only measured power ratings.
