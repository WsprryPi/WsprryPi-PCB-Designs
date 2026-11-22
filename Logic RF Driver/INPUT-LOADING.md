# Detector loading

The schematic connects the indicator to `RF_RAW` through R2 (220 ohms) and C5 (10 nF), on the U1 side of C4. It indicates driver-output activity. It does not establish RF power at the filtered output. The RF_RAW results are below; the CLK_IN cases describe the alternative input connection and its nonlinear loading of the clock source.

Increasing R2 reduces the detector branch current and improves the input waveform at 145 MHz, but it also reduces rectified base drive. For the alternative CLK_IN tap, the 120-ohm model has less clock loading and much less LED current than the 100-ohm model. At CLK_IN, the model does not support recommending 150 ohms or more as a dependable full-band indicator value. The design uses 220 ohms on RF_RAW.

## Simulation

The lumped transient study uses a 0–3.3 V, 50% duty-cycle source with 50 ohms series resistance, two U1 inputs represented by 14 pF total, and R1 at 10 kohms. The input capacitance comprises two typical 6 pF data-pin capacitances plus an assumed 2 pF for the board. The source rise and fall times in the table are 1.5 ns each, measured over the complete source-voltage excursion. These assumptions are sensitivity cases, not exact Pico, Pi, or Si5351 transistor models.

The detector includes R2, C5, both BAT54S diodes, the MMBT3904, C6 (10 nF), R3 (1 Mohm), R4 (680 ohms), and an illustrative red LED. Both supplies are ideal. The study uses the [Diodes Incorporated BAT54S model](https://www.diodes.com/spice/download/431/BAT54S.spice.txt) and the [MMBT3904 model](https://www.diodes.com/spice/download/2869/MMBT3904.spice.txt). The selected components are the Nexperia BAT54S,215 diode, CJ MMBT3904(RANGE:100-300) transistor, and KENTO KT-0603R LEDs. The Diodes Incorporated models and illustrative LED are surrogates for those parts; predicted LED current is not a brightness specification.

| R2 | CLK_IN minimum–maximum at 145 MHz | Predicted LED current | Interpretation |
| --- | --- | --- | --- |
| 100 ohms | 0.501–2.782 V | 1.41 mA | Strongest indicator drive of these cases |
| 120 ohms | 0.460–2.823 V | 0.103 mA | Modest clock improvement; much less LED current |
| 150 ohms | 0.410–2.874 V | Below 0.01 mA | Visibility is doubtful and part-dependent |
| 220 ohms | 0.328–2.956 V | Essentially off in this model | Unsuitable for assuming full-band indication |
| 470 ohms | 0.207–3.076 V | Essentially off in this model | Better isolation, insufficient detector drive |
| 1 kohm | 0.142–3.142 V | Essentially off in this model | Better isolation, insufficient detector drive |

At 137 kHz, the 100-, 150-, and 220-ohm cases all predict about 1.75 mA LED current. The restriction is at VHF, rather than at the bottom of the target range. Intermediate fast-edge cases at 7, 28, 50, and 100 MHz show that the loss of indication depends on frequency and resistance; a successful HF check does not establish 145 MHz operation.

[TI specifies](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf) a maximum LOW input level of 0.8 V and minimum HIGH input level of 2.0 V at the 3.3 V input supply. The tabulated voltage extrema cross those limits, but extrema alone do not establish timing margin, source compatibility, or RF output power. Increasing R2 improves the modeled waveform without eliminating the detector load.

## Limits and numerical checks

The diode model has 13.3 pF zero-bias capacitance and a 7.2 ns transit-time parameter. Setting that transit time to zero as a sensitivity check changes the 150-ohm LED prediction at 145 MHz to about 0.031 mA, with a similar 0.408–2.876 V clock swing. The modified transit time is a model parameter, not a different manufacturer's diode. It demonstrates why precise VHF brightness predictions require the selected parts and measurements. The [Nexperia BAT54S datasheet](https://assets.nexperia.com/documents/data-sheet/BAT54S.pdf) specifies up to 10 pF at 1 V reverse bias and 1 MHz; that capacitance specification alone does not characterize the complete detector at 145 MHz.

The primary study omits extracted PCB and package inductances. Cases with assumed package and capacitor inductances show numerical convergence failures and are excluded from the table. Those numerical failures do not establish a physical circuit failure. The source model also lacks pad current limiting, source-specific nonlinear output impedance, cable effects, supply impedance, and temperature or manufacturing spread. The 50-ohm assumption is based on the [Si5351's typical output impedance](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/data-sheets/Si5351-B.pdf); it does not identify a particular Pico or Pi drive setting.

The calculations use ngspice through the KiCad shared library. Periodic-state searches adjust the initial voltages of C5 and C6 and compare capacitor states one period-aligned window apart. The 100- and 120-ohm cases have final 20-period state changes below 20 nV; the 120-ohm case uses a maximum timestep of about 21.6 ps. The very dim cases have microvolt-scale state drift, which limits the precision of their leakage-scale LED currents. Short startup simulations can overstate sustained brightness because C6 retains base charge. The 100-microsecond transient check at 120 ohms predicts 0.309 mA, whereas the periodic result is 0.103 mA.

The [derived results](docs/input-loading-results.json) contain case assumptions, model and script hashes, and settling diagnostics. The [transient runner](scripts/check_input_loading.py) accepts external manufacturer model files, source parameters, and capacitor initial conditions. Manufacturer model text and diagnostic decks are in the ignored `generated/input-loading/` directory. The approximately 83 mW result in the output-stage [comparison](COMPARISON.md) excludes the nonlinear detector load.

The CLK_IN results depend on the actual clock source, diode, transistor, LED, and ambient light. The input waveform and LED brightness have no hardware measurements.

## Detector connected to RF_RAW

R2 connects to `RF_RAW` on the U1 side of C4. This removes the detector's direct nonlinear load from the clock source. The source drives U1's two inputs and R1. U1 supplies the detector branch current from the output stage; supply and ground coupling can affect the source in a physical assembly. C5 is in series with the detector to block RF_RAW's DC level. The detector and LED supply share ground, and R4 connects to 3.3 V.

The RF_RAW connection is evaluated with the comparison's nominal paralleled-output behavioral model, Samsung C4 bias-dependent network, and a resistive 50-ohm load. The detector uses the same manufacturer diode/transistor models and illustrative LED as the input study. The output model retains its assumed input-derived switching timing and package effects. It does not calculate reverse coupling into the clock source or complete supply current. Its source assumptions differ from the 1.5 ns input-study table, so the two tables are not a controlled comparison of source edge speed.

| Connection at 145 MHz | Fundamental power into 50 ohms | LED current | Peak current per U1 channel |
| --- | --- | --- | --- |
| No detector | 83.03 mW | — | 27.5 mA |
| RF_RAW through 100 ohms | 76.67 mW | 1.78 mA | 38.3 mA |
| RF_RAW through 220 ohms | 79.89 mW | 1.72 mA | 32.3 mA |
| RF_RAW through 470 ohms | 81.49 mW | 0.00070 mA | 29.5 mA |

At 137 kHz, 220 ohms gives 82.48 mW versus 84.32 mW without the detector, with about 1.76 mA LED current. At 7 MHz, it gives 82.13 mW versus 84.47 mW, with about 1.79 mA LED current. At 50 MHz, it gives 81.34 mW versus 84.22 mW, with about 1.79 mA LED current. The circuit uses the RF_RAW tap and a 220-ohm R2. The modeled results do not establish continuous full-band hardware operation. The 470-ohm case loses useful indication at 145 MHz despite adequate HF drive.

With 220 ohms, the modeled fundamental-power penalty is about 2.2% at 137 kHz and 3.8% at 145 MHz, or about 0.10 and 0.17 dB. The detector branch loads the amplifier output. LED current comes through R4 from 3.3 V; the RF branch separately loads the 5 V output stage. LED current alone therefore does not describe the additional supply burden.

The nominal equal-sharing model predicts a 32.3 mA peak per output at 145 MHz with 220 ohms, close to TI's 32 mA recommended output-current magnitude at a 5 V output supply. This peak includes switching effects; the data-sheet limit is not a pulse-performance guarantee, and the 50 mA absolute maximum must not be treated as a design target. Unequal sharing, reactive filter loading, and supply transients are outside the qualification. The modeled power and indication are promising, but the current margin is unmeasured.

The 145 MHz cases use periodic capacitor-state initialization. Halving the maximum timestep changes output power by less than 0.003% and LED current by less than 0.002%. The 137 kHz detector cases have approximately 13 microvolts of C5 state change across the final 20-period window, with substantially smaller C6 drift. Numerical agreement establishes solver consistency, not manufacturer-model accuracy. The [output-detector results](docs/output-detector-results.json) contain the case results and numerical checks. The schematic and PCB connect the detector to RF_RAW through 220 ohms.

## Reservoir placement

C6 is the 10 nF reservoir between D1's cathode and ground. It stores rectified charge and smooths Q1's base voltage. R3 provides a 1 Mohm discharge path. Their nominal RC time constant is 10 ms; Q1 base current and leakage also discharge C6, so the LED hold time is not simply 10 ms.

The board places C6 beside D1, with a 1.46 mm cathode trace and a ground via about 0.76 mm from the ground-pad center. The charging path reaches C6 directly; the longer base-node branch serves Q1 and R3. The simulation omits extracted trace and ground-return inductance, so the placement has no numerical RF-loss or brightness rating. See [PCB layout](PCB-LAYOUT.md).
