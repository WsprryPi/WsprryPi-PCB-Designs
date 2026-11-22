# Model scope

The comparison models the SN74LVC2T45 output stage and Samsung C4. The RF_RAW indicator branch connects through 220 ohms. Its loading, LED current, and detector behavior are outside that output-stage model. The separate [input-loading study](INPUT-LOADING.md) evaluates the detector with an illustrative source and LED. It uses ideal supply rails, so the selected bypass capacitors and the physical supply wiring are outside the calculation.

| Item | Selected part | Model coverage |
| --- | --- | --- |
| U1 | TI SN74LVC2T45DCUR / C15741 | IBIS-derived behavioral surrogate with nominal output tables and simplified timing and package effects |
| R1 | UNI-ROYAL 0603WAF1002T5E / C25804 | Explicit 10-kilohm pull-down loading and resistor parasitics are absent from the logic-input timing surrogate |
| C1/C2 | YAGEO CC0603KRX7R9BB104 / C14663 | Supply bypass capacitors are absent from the ideal-supply amplifier model |
| C3 | Samsung CL10A105KB8NNNC / C15849 | Bulk bypass and supply impedance are absent from the ideal-supply amplifier model |
| C4 | Samsung CL10A105KB8NNNC / C15849 | Passive fits to impedance and ESR curves at 0, 2.5, and 5 V bias, with interpolation between bias points |
| PCB, connectors, and external filter | Project-local footprints and an external selected-band filter | No extracted layout, connector, supply-return, or filter model |

The [comparison](COMPARISON.md) has 78 accepted logic and resistor-fed BS170 cases. Ideal-choke results are kept as diagnostics because they are sensitive to timestep and bias. The [C4 analysis](C4-SELECTION.md) separately checks capacitor impedance and loss into a resistive load.

Matching nominal resistance, capacitance, dielectric, and package size does not make two parts' physical impedance or bias behavior identical. Nor does a higher voltage rating, by itself, make a capacitor a better VHF bypass. The ideal rails and incomplete supply-current model leave the bypass network's effect on output power unanswered.

The [manifest](docs/comparison-samsung-manifest.json) records ten source and script hashes and 65 amplifier-deck hashes; the source files match those records. The [verification data](docs/simulation-samsung-verification.json) include numerical checks and failures. This identifies the inputs and the solver's consistency, not the devices' accuracy or the board's RF and thermal performance.

The [parts and procurement page](LCSC-PARTS.md) lists the selected indicator parts. The separate detector study uses Diodes Incorporated models and an illustrative LED; it does not exactly simulate the selected Nexperia BAT54S, CJ MMBT3904, and KENTO KT-0603R.

C6 sits beside D1 with a short cathode connection and a local ground via. The detector model uses lumped capacitors and omits extracted routing inductance; it does not assign a measured VHF benefit to the placement.

The [board circuit study](BOARD-SIMULATION.md) includes the RF_RAW detector, the power LED branch, a 13-frequency sweep, and channel-skew sensitivity at 145 MHz. It searches periodic initial states for C4, C5, and C6 and retains the ideal-rail and surrogate-device limitations. Its current peaks are model-dependent stress indicators, not validated device predictions, pulse-current ratings, or thermal qualification. TI explicitly supports joining the two outputs; these hypothetical tests do not demonstrate a need for isolation resistors.

The [output-sharing study](OUTPUT-SHARING.md) evaluates per-output resistance, channel skew, hypothetical drive-strength mismatch, resistor parasitics, and numerical sensitivity. It covers a candidate circuit; the design retains directly paralleled outputs. Its current and LED estimates share the board study's behavioral-device, ideal-supply, and detector-model limitations.
