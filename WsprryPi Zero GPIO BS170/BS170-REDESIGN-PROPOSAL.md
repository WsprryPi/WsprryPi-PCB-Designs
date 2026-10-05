# BS170 amplifier design rationale and qualification plan

**Status: implemented BS170 board, ready for order as confirmed by the project owner on 2026-10-05.** The saved schematic and PCB contain the single-BS170 stage, switched supply, adjustable gate bias, and LPF interface. The LTC6432-15 and two WBC2-1TLC transformers are absent from both designs. Headers and Q41 BS170 will be fitted by hand after manufacture; L41 and J51 also remain manual assembly items. See the [fabrication and assembly notes](FABRICATION-NOTES.md). Physical, thermal, electrical, and RF qualification remain open.

## Decision and scope

The two-transformer implementation was rejected on cost. The 135 kHz to 144 MHz operating range remains the design target, with output power allowed to vary by band. About 100 mW after the selected low-pass filter remains a useful goal where feasible, not a full-range guarantee. The selected design retains GPIO4/GPIO20 selection, software-controlled amplifier enable, the Raspberry Pi 5 V supply, and the grouped J52 plug-in LPF interface.

The implemented circuit is a single 5 V BS170 RF stage with **no RF transformers**. This follows the QRP Labs Ultimate3S and LA3JJ wiZPit approaches, with measurements required for this board's Raspberry Pi GPIO source and LPF.

```text
GPIO4 or GPIO20 -> selection -> GPIO protection/damping -> AC coupling -> BS170 gate
switched 5 V -> adjustable gate bias and drain RF feed
BS170 drain -> DC blocking -> J52 selected LPF -> SMA
BS170 source -> RF ground
```

The gate-bias network must have a defined off state, draw no DC from the GPIO, and be disabled when the switched amplifier supply is off. The drain feed needs adequate impedance at the low-frequency end without unacceptable loss or parasitic behavior at the high-frequency end. The [implemented-parts table](README.md#implemented-rf-parts) records the saved bias, coupling, damping, and bypass values; their performance remains subject to RF measurement. L41 selects the hand-wound FT37-43 choke described below. The LPF remains mandatory for the square-wave drive and nonlinear output stage; the correct filter must be installed for each band.

## Selected hand-wound choke and trimmer

On 2026-10-01, the user selected **25 turns on a hand-wound FT37-43 core** for L41. Each pass through the core center counts as one turn. The schematic value is `25T FT37-43`. The [Amidon core specification](https://www.amidoncorp.com/ft-37-43/) gives nominal A_L = 350 nH/turn², so 25 turns estimates 218.75 µH at low frequency. RF impedance under drain current and performance at 137 kHz and 144 MHz remain measurement requirements. The winding follows the [QRP Labs Ultimate3S assembly manual](https://www.qrp-labs.com/images/ultimate3s/assembly.pdf); its [LF modifications](https://www.qrp-labs.com/ultimate3/u3mods.html) also document a different R10/N30 core for improved LF output.

L41 uses the local `L_Toroid_FT37-43_Vertical_P5.08mm` footprint, adapted from KiCad's generic 10 × 5 mm vertical toroid pattern. On 2026-10-01, the user selected upright mounting. The hand-formed leads use 5.08 mm pad-center spacing, with 2.4 mm pads and 1.2 mm drills; pad 1 connects to `SW_5V` and pad 2 to `PA_DRAIN`. The fabrication outline depicts the bare core's 9.525 × 3.175 mm board projection; `Dwgs.User` marks an 11 × 5 mm maximum wound-body projection. The courtyard reserves 11.5 × 7.98 mm including the lead pads. Reserve up to 11 mm wound-body height plus the mounting gap. Start with approximately 0.32 mm (AWG 28) enamelled wire, form the leads to the footprint pitch, and strip/tin them before hand soldering. Wound fit, stability, height clearance, and RF behavior require physical verification.

RV31 retains 5 kΩ and selects Bourns `TC33X-2-502E`, `LCSC Part #` C719177, with the local `Potentiometer_Bourns_TC33X_Vertical` footprint. Pin/pad 2 is the wiper; pins 1/3 are the CCW/CW resistance ends. L41 and RV31 have project-local illustrative 3D models; see [library sources and model limits](LIBRARY-SOURCES.md#selected-choke-and-trimmer-footprints).

## Evidence and limits

- QRP Labs describes its single-BS170, 5 V Ultimate3S as producing about 250 mW on 30 m, with output falling on higher bands. Its 2 m result is **17 mW**, so a transformer-free BS170 design must not promise 100 mW at 144 MHz. QRP Labs lists operation from the 137 kHz amateur band through 2 m, but does not establish power or spectral performance for this board at those endpoints.
- In QRP Labs' measured base circuit with a 50 ohm load after the LPF, the cooler-running bias setting produced 189 mW on 30 m, 123 mW on 10 m, and 58 mW on 6 m. Its experiments found that an added output transformer improved HF power but did not improve 6 m output. Those values belong to the QRP Labs circuit and drive source, not this proposed board.
- LA3JJ's wiZPit directly uses Raspberry Pi GPIO4 to drive a BS170 stage and reports more than 200 mW on 40 m after its LPF. This is a more directly relevant Pi precedent, but it does not establish performance on other bands or with this PCB.
- QRP Labs AC-couples its 3.3 V Si5351 drive and adds adjustable DC gate bias because a 3.3 V square wave alone did not switch its BS170 adequately. A Raspberry Pi GPIO waveform and drive capability must be checked on the exact supported Pi models before selecting gate parts or bias settings.
- The onsemi BS170 data sheet rates the TO-92 device at 830 mW dissipation at 25 °C and specifies 24 pF typical, 40 pF maximum input capacitance at its stated test point. Its switching-time figure uses a 10 V gate drive and therefore does not prove efficient switching from a 3.3 V GPIO at 144 MHz. Thermal and GPIO loading checks remain essential.

## Cost case

The historical baseline's two WBC2-1TLC transformers and LTC6432-15 alone represented roughly **$39.79 for a one-board purchase** in the LCSC product-page snapshots reviewed on 2026-09-30 ($10.3228 per transformer and $19.1431 for the amplifier), before passives, assembly, LPF, headers, or fabrication. Supplier prices and stock must be refreshed when ordering. The implemented BS170 board removes that QFN and its selective exposed-pad hole-filling/capping requirement.

A BS170 is a low-cost discrete part, but the complete cost comparison must include its RF feed, bias trimmer or production bias components, coupling parts, any driver found necessary, hand winding or other assembly labor, and the LPF. The onsemi TO-92 BS170 LCSC listing reviewed on 2026-09-30 showed a reference price of $0.1689 at five pieces but was out of stock in that page snapshot. Q41 now has a separate hand-purchasing and hand-fitting path; confirm the exact part's availability when purchasing. Do not substitute an SMD MMBF170 without reassessing its lower package dissipation and layout.

## Prototype and acceptance path

1. Order the current BS170 board using the [fabrication and assembly notes](FABRICATION-NOTES.md), then fit the headers, Q41, L41, and J51 by hand. Verify connector fit, BS170 pin orientation, the wound choke, and the trimmer adjustment. The historical differential-amplifier and transformer assets remain attributed in the project-local libraries but are not current assembly items.
2. Test the assembled RF path from an actual supported Pi GPIO through a representative LPF into a 50 ohm dummy load. Record GPIO waveform/loading, bias, off-state drain current, keyed current, output power, harmonics and spurs, and device temperature.
3. Repeat at 135/137 kHz, representative MF/HF bands, 6 m, and 144 MHz. Check every supported GPIO source and Pi model intended for release. If the 2 m result is low, record the lower band-specific power target rather than assuming additional parallel BS170 devices solve it.
4. Record results against the exact assembled board revision, Pi, supply, LPF, and load. If measurements require a circuit or layout change, update the sources, rerun KiCad ERC/DRC, and repeat physical/RF checks. Earlier validation does not transfer automatically to a changed revision.

## References

- [QRP Labs Ultimate3S overview and 2 m result](https://qrp-labs.com/ultimate3/u3s.html)
- [QRP Labs Ultimate3S assembly manual and circuit](https://www.qrp-labs.com/images/ultimate3s/assembly.pdf)
- [QRP Labs measured PA bias and power](https://www.qrp-labs.com/ultimate3/u3info/u3pa.html)
- [QRP Labs output-transformer comparison](https://qrp-labs.com/ultimate3/u3info/u3sbifilar.html)
- [QRP Labs 3.3 V drive and gate-bias modification](https://www.qrp-labs.com/ultimate3/u3mods/u3tou3s.html)
- [LA3JJ wiZPit Raspberry Pi BS170 transmitter manual](https://www.wsprnet.org/drupal/sites/wsprnet.org/files/wZPitmanual_v1.pdf)
- [onsemi BS170/MMBF170 data sheet](https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf)
- [LCSC WBC2-1TLC](https://www.lcsc.com/product-detail/C19191658.html), [LTC6432-15](https://www.lcsc.com/product-detail/C689344.html), and [BS170](https://lcsc.com/product-detail/MOSFET_FAIRCHILD_BS170_BS170_C111691.html) product pages
