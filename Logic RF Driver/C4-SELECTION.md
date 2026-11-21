# C3/C4 selection and impedance

C3 and C4 are **Samsung Electro-Mechanics CL10A105KB8NNNC / C15849**: 1 uF, 10%, 50 V, X5R, in 0603. C3 is the 5 V bulk bypass capacitor; C4 is the output DC block. The [product page](https://product.samsungsem.com/mlcc/CL10A105KB8NNN.do) lists the electrical family as CL10A105KB8NNN, with C as the packaging suffix. The X5R temperature range is -55 to +85 C.

Samsung's model puts C4's impedance well below 50 ohms throughout 137 kHz–145 MHz. At 2.5 V bias, the endpoints are about 1.602 ohms and 0.1904 ohms. The largest calculated capacitor-only loss is 0.01145 dB for an ideal source feeding 50 ohms. This checks the reference data; it is not a measurement of the mounted part or a guaranteed production limit.

## Data and calculation

The [Samsung Component Library](https://weblib.samsungsem.com/mlcc/mlcc-ec.do?partNumber=CL10A105KB8NNN) provides precise-model graphs for this electrical family at 25 C, with 0, 2.5, and 5 V bias. Each export has 300 impedance-magnitude and ESR samples between 100 Hz and 6 GHz. The evidence here is those graph exports; the check has neither a retrieved Touchstone file nor an independently executed manufacturer SPICE netlist.

The [script](scripts/check_samsung_c4.py) uses log-log interpolation of impedance magnitude and ESR at 10,001 points across the band, plus the listed band frequencies. It does not extrapolate beyond the data. The [band CSV](docs/c4-samsung-band-check.csv) contains the results, and the [source record](docs/c4-samsung-source-manifest.json) identifies the inputs.

For a resistive load, X squared is the impedance magnitude squared minus ESR squared. The load-voltage ratio is 50 / sqrt((50 + ESR)^2 + X^2), relative to an ideal source connected directly to 50 ohms. The CSV also gives results for a matched 50-ohm source and load. Neither calculation includes mounting parasitics or external filter loss.

| DC bias, 25 C | Impedance at 137 kHz | ESR at 137 kHz | Impedance at 145 MHz | ESR at 145 MHz | Maximum added loss, ideal source into 50 ohms |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 V reference | 1.4932 ohms | 0.03935 ohms | 0.18872 ohms | 0.06501 ohms | 0.01134 dB |
| 2.5 V, C4 nominal | 1.6016 ohms | 0.04014 ohms | 0.19043 ohms | 0.06561 ohms | 0.01145 dB |
| 5 V, C3 supply | 1.8036 ohms | 0.04235 ohms | 0.19157 ohms | 0.06688 ohms | 0.01299 dB |

| Frequency | C4 impedance at 2.5 V, 25 C |
| --- | ---: |
| 0.137 MHz | 1.6016 ohms |
| 0.475 MHz | 0.46864 ohms |
| 1.8 MHz | 0.12052 ohms |
| 7 MHz | 0.015428 ohms |
| 28 MHz | 0.055125 ohms |
| 50 MHz | 0.081091 ohms |
| 145 MHz | 0.19043 ohms |

At 2.5 V bias, the impedance reaches about 0.0113 ohms near 8.26 MHz. Above resonance, the part is inductive, yet its impedance is still small compared with 50 ohms. That is enough for the resistive-load calculation; a reactive filter can interact with C4, so the figures are not a complete amplifier/filter response.

## Bias and limits

With a downstream DC return, a 0–5 V output at 50% duty cycle puts a nominal 2.5 V DC bias across C4. The 2.5 V curve fits that condition. The zero-bias curve is a reference, while the 5 V curve describes a different bias condition.

Samsung's typical capacitance curve at 1 kHz and 1 Vrms shows a drop of about 10.7% at 2.5 V and 34.4% at 5 V. The corresponding values are 0.893 uF and 0.656 uF relative to nominal. Those LCR readings are not substitutes for the RF curves. AC amplitude, aging, tolerance, temperature, and duty cycle also matter.

C3 operates at 5 V, alongside the 100 nF YAGEO C2. Its typical bias curve gives about 0.66 uF at that voltage. The supply sees more than the bare capacitor: pads, traces, vias, and return paths all contribute impedance, and they are outside this component model.

For an illustrative 45 mA RMS, the calculated RF voltage across C4 is about 72 mV RMS at 137 kHz. ESR dissipation is about 0.081 mW there and 0.133 mW at 145 MHz. Mounting matters at the upper end: just 2 nH adds about 1.82 ohms at 145 MHz. No current or thermal measurements support these estimates.

The available evidence has no biased S-parameter cross-check, worst-case temperature/tolerance/aging sweep, extracted-board model, or assembled-board RF measurement. The [amplifier comparison](COMPARISON.md) uses passive fits to these Samsung curves, with the coverage listed in [model scope](MODEL-SCOPE.md). C1/C2 bypassing is outside that amplifier model. See the [input/output coupling rationale](README.md#why-the-input-is-dc-coupled-and-c4-is-on-the-output).

C15849 is a JLCPCB Basic part; see [ordering information](LCSC-PARTS.md). The manufacturer files stay local under their own terms. Project files contain derived results and source identities.