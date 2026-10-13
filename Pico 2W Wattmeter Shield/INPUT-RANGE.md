# Input range and measurement conditions

This is a **terminating low-power RF meter**, with external attenuation for amplifier outputs. Its intended frequency range is **136 kHz–450 MHz**, covering 2200 m through 70 cm. Assembled-board range, input match, and accuracy are unmeasured. The [experimental-use and warranty notice](../README.md#experimental-use-and-warranty) applies.

## Input circuit and matching

J30 feeds C30–C34: five parallel 100 nF Walsin 1206N104J500CT C0G capacitors ([LCSC C170182](https://www.lcsc.com/product-detail/C170182.html)), nominally **500 nF**. R30–R34 are five parallel **412 Ω**, 0402, ±0.1% thin-film resistors, Viking ARG02BTC4120 ([LCSC C2683017](https://www.lcsc.com/product-detail/C2683017.html)), nominally **82.4 Ω**. C40–C44 form a second 500 nF bank between this loaded node and U40 RFIN. These values and parts are present in both the schematic and PCB. Each capacitor has ±5% tolerance; bank worst-case tolerance remains ±5%.

The detector input branch loads the resistor bank. The assembled impedance is frequency-dependent and has no verified 50 Ω match. The [ADL5904 reference circuit](https://www.analog.com/media/en/technical-documentation/data-sheets/adl5904.pdf) specifies an **82.5 Ω external shunt**, with coupling between the shunt and RFIN. The fitted 82.4 Ω bank is approximately 0.12% below that nominal value. The complete capacitor-bank, bus, connector, and detector network has unmeasured input S11 and calibrated power response.

There is **no onboard attenuation pad**. Calibration includes both banks, the termination, connector launch, PCB conductors, and detector input.

## Nominal range

The [ADL5904 product specification](https://www.analog.com/en/products/adl5904.html) describes a nominal −30 to +15 dBm detector range, approximately 1 µW–31.6 mW. This is a reference for calibration, without establishing the same J30 range over the assessed bands. Absolute maximum ratings are not measurement limits. The shield has no qualified high-power overload protection.

The following current values use `I_RMS = sqrt(P / 50 Ω)`. They are **derived values for a nominal resistive 50 Ω reference**, not direct current measurements or a verified model of this board's input impedance.

| Power | Power in mW | Current in mA RMS at 50 Ω |
| --- | --- | --- |
| −30 dBm | 0.001 | 0.141 |
| −20 dBm | 0.010 | 0.447 |
| −10 dBm | 0.100 | 1.414 |
| 0 dBm | 1.000 | 4.472 |
| +10 dBm | 10.000 | 14.142 |
| +15 dBm | 31.623 | 25.149 |

An external attenuator must bring the source into the calibrated J30 range and have adequate RF power rating, band coverage, and connector match. Its measured attenuation at the operating frequency is added to the calibrated connector reading. No external attenuator is specified as part of this board's assembly.

## LF and UHF behavior

At 136 kHz, an ideal 500 nF bank has **2.34 Ω capacitive reactance**. The shunt lies between the two banks, so their behavior is determined by the complete loaded network. Paralleling reduces ideal capacitive reactance and independent branch inductance; common feed and bus inductance remain.

The banks have centered feeds and approximately 9.2 mm vertical bus spans. Their 1206 packages and shared conductors have no verified UHF impedance model. Input match and calibrated power response around 430–450 MHz are unmeasured, and the same limitation applies to LF accuracy at 136 kHz.

## Measurement meaning

This detector responds to broadband RF power; it does not isolate the transmitter's fundamental. A GPIO clock's harmonics contribute according to the input network and detector response. An ideal 50% square wave has approximately 81% of its AC power in the fundamental, so total AC power is about 0.91 dB greater. Actual edge shape, loading, and filtering affect the result.

GPIO drive strength does not establish calibrated RF power at J30. The source waveform, loading, and band filtering are part of the measurement conditions.

Fundamental transmitter power requires the intended band filter in the source path. Calibration applies to the complete board and requires an independent RF reference across the operating bands and power levels. Source filtering, external attenuation, supply, temperature, and Pico/Wi-Fi activity are measurement conditions.

Frequency or band coefficients apply to the complete board. External attenuation corrections are separate. Incident power at J30, power accepted by the meter, and fundamental power after filtering are different quantities when mismatch or harmonics are significant.

## Power and ADC filtering

U20 takes **VBUS**, rather than VSYS or the Pico's 3V3 output, and supplies the detector, ADC, and I²C pullups. A Pico powered only through VSYS leaves the analog section unpowered. See the [power requirements](README.md#power).

The saved R50 = **470 Ω** and C50 = **22 µF** give an ideal one-pole cutoff of **15.4 Hz**, a **10.34 ms** time constant, and approximately **47.6 ms** settling to 1%. Ideal 50/60 Hz attenuation is **10.6/12.1 dB**. The network passes DC. R50 ±1% and C50 ±20% alone allow about 12.7–19.4 Hz; bias, temperature, output resistance, and ADC loading also affect the response.

[Samsung's C50 data](https://product.samsungsem.com/mlcc/CL21A226MAYNNN.do) specifies X5R, 25 V, ±20%, 0805. Its capacitance is a filter parameter, not a DC gain-setting element, so C0G is not required. Its effective capacitance and settling under the actual detector voltage are unmeasured.

R63 = **47 Ω** and C61 = **1 µF X7R** form the routed pull-up supply filter, with a nominal **3.4 kHz** corner. C61 connects the common supply ends of R60/R61 to ground after R63. U40 and U60 retain direct connections to `ANALOG_3V3` and their own decoupling. This branch addresses I²C switching-current coupling; its nominal 50/60 Hz attenuation is negligible and its effect on measurement noise is unmeasured.

Mains interference is a system-level qualification limit. Averaging the detector's logarithmic output is not the same as averaging power in watts. No verified ADC configuration, timed averaging implementation, or system mains-rejection figure is supplied with this hardware design.
