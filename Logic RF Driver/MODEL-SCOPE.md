# Model scope

The comparison models the SN74LVC2T45 output stage and Samsung C4. It uses ideal supply rails, so the selected bypass capacitors and the physical supply wiring are outside the calculation.

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

The [manifest](docs/comparison-samsung-manifest.json) records ten source and script hashes and 65 amplifier-deck hashes; the saved files match those records. The [verification data](docs/simulation-samsung-verification.json) include numerical checks and failures. This identifies the inputs and the solver's consistency, not the devices' accuracy or the board's RF and thermal performance.