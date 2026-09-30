# Lower-cost BS170 amplifier proposal

Status: **proposed for design review; not implemented**. This independent KiCad project begins as a copy of `WsprryPi Zero GPIO`. Its saved schematic and PCB still contain the LTC6432-15 and two WBC2-1TLC transformers. This proposal does not qualify the copied board or authorize its fabrication.

## Decision and scope

The two-transformer implementation is too expensive for the intended board. Preserve the 135 kHz to 144 MHz operating range as the redesign target, but allow output power to vary by band. About 100 mW after the selected low-pass filter remains a useful goal where feasible, not a full-range guarantee. Keep the existing GPIO4/GPIO20 selection, software-controlled amplifier enable, Raspberry Pi 5 V supply, and J81/J82 plug-in LPF mechanical interface as redesign constraints.

The first candidate is a single 5 V BS170 RF stage with **no RF transformers**. This follows the simpler QRP Labs Ultimate3S and LA3JJ wiZPit approaches, with adaptations and measurements required for this board's Raspberry Pi GPIO source and LPF.

```text
GPIO4 or GPIO20 -> selection -> GPIO protection/damping -> AC coupling -> BS170 gate
switched 5 V -> adjustable gate bias and drain RF feed
BS170 drain -> DC blocking -> J81/J82 selected LPF -> SMA
BS170 source -> RF ground
```

The gate-bias network must have a defined off state, draw no DC from the GPIO, and be disabled when the switched amplifier supply is off. The drain feed needs adequate impedance at the low-frequency end without unacceptable loss or parasitic behavior at the high-frequency end. Choke, bias, coupling, and damping values are **not selected** here. The LPF remains mandatory for the square-wave drive and nonlinear output stage; the correct filter must be installed for each band.

## Evidence and limits

- QRP Labs describes its single-BS170, 5 V Ultimate3S as producing about 250 mW on 30 m, with output falling on higher bands. Its 2 m result is **17 mW**, so a transformer-free BS170 design must not promise 100 mW at 144 MHz. QRP Labs lists operation from the 137 kHz amateur band through 2 m, but does not establish power or spectral performance for this board at those endpoints.
- In QRP Labs' measured base circuit with a 50 ohm load after the LPF, the cooler-running bias setting produced 189 mW on 30 m, 123 mW on 10 m, and 58 mW on 6 m. Its experiments found that an added output transformer improved HF power but did not improve 6 m output. Those values belong to the QRP Labs circuit and drive source, not this proposed board.
- LA3JJ's wiZPit directly uses Raspberry Pi GPIO4 to drive a BS170 stage and reports more than 200 mW on 40 m after its LPF. This is a more directly relevant Pi precedent, but it does not establish performance on other bands or with this PCB.
- QRP Labs AC-couples its 3.3 V Si5351 drive and adds adjustable DC gate bias because a 3.3 V square wave alone did not switch its BS170 adequately. A Raspberry Pi GPIO waveform and drive capability must be checked on the exact supported Pi models before selecting gate parts or bias settings.
- The onsemi BS170 data sheet rates the TO-92 device at 830 mW dissipation at 25 °C and specifies 24 pF typical, 40 pF maximum input capacitance at its stated test point. Its switching-time figure uses a 10 V gate drive and therefore does not prove efficient switching from a 3.3 V GPIO at 144 MHz. Thermal and GPIO loading checks remain essential.

## Cost case

The saved schematic's two WBC2-1TLC transformers and LTC6432-15 alone represented roughly **$39.79 for a one-board purchase** in the LCSC product-page snapshots reviewed on 2026-09-30 ($10.3228 per transformer and $19.1431 for the amplifier), before passives, assembly, LPF, headers, or fabrication. Supplier prices and stock must be refreshed when ordering. The current QFN layout also calls for selective exposed-pad hole filling and capping; a redesigned BS170 board could avoid that process, pending a new PCB layout and fabrication review.

A BS170 is a low-cost discrete part, but the complete cost comparison must include its RF feed, bias trimmer or production bias components, coupling parts, any driver found necessary, hand winding or other assembly labor, and the LPF. The onsemi TO-92 BS170 LCSC listing reviewed on 2026-09-30 showed a reference price of $0.1689 at five pieces but was out of stock in that page snapshot; select an available exact part and assembly path before freezing the BOM. Do not substitute an SMD MMBF170 without reassessing its lower package dissipation and layout.

## Prototype and acceptance path

1. Draw a revised schematic with the single BS170 stage and its switched-supply, GPIO isolation, gate bias, drain feed, and LPF connections. Remove the differential amplifier and both RF transformers from that revision's BOM. Keep source assets and attribution in the project-local libraries.
2. Prototype the RF path from an actual supported Pi GPIO through a representative LPF into a 50 ohm dummy load. Record GPIO waveform/loading, bias, off-state drain current, keyed current, output power, harmonics and spurs, and device temperature.
3. Repeat at 135/137 kHz, representative MF/HF bands, 6 m, and 144 MHz. Check every supported GPIO source and Pi model intended for release. If the 2 m result is low, record the lower band-specific power target rather than assuming additional parallel BS170 devices solve it.
4. Only after the circuit and parts are selected, update and route the PCB, verify LPF header fit and Pi clearances, run KiCad ERC/DRC, and remeasure an exact assembled board revision. The current PCB's passing checks do not transfer to the redesign.

## References

- [QRP Labs Ultimate3S overview and 2 m result](https://qrp-labs.com/ultimate3/u3s.html)
- [QRP Labs Ultimate3S assembly manual and circuit](https://www.qrp-labs.com/images/ultimate3s/assembly.pdf)
- [QRP Labs measured PA bias and power](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html)
- [QRP Labs output-transformer comparison](https://qrp-labs.com/ultimate3/u3info/u3sbifilar.html)
- [QRP Labs 3.3 V drive and gate-bias modification](https://www.qrp-labs.com/ultimate3/u3mods/u3tou3s.html)
- [LA3JJ wiZPit Raspberry Pi BS170 transmitter manual](https://www.wsprnet.org/drupal/sites/wsprnet.org/files/wZPitmanual_v1.pdf)
- [onsemi BS170/MMBF170 data sheet](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)
- [LCSC WBC2-1TLC](https://www.lcsc.com/product-detail/C19191658.html), [LTC6432-15](https://www.lcsc.com/product-detail/C689344.html), and [BS170](https://lcsc.com/product-detail/MOSFET_FAIRCHILD_BS170_BS170_C111691.html) product pages
