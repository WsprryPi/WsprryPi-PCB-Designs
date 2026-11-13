# Local 3D models

All model references in this project use `${KIPRJMOD}/relay-switched-lpf.3dshapes/`. No installed global 3D-library path, external repository, network lookup, or absolute machine path is needed to view the saved board.

## Coverage and population

| References | Model | Basis and limits |
| --- | --- | --- |
| RL1–RL5 | [TX2_5V_Nominal.wrl](TX2_5V_Nominal.wrl) | Original nominal 7.4 × 15 mm envelope, 8.2 mm overall body height, eight pins on the saved TX2 terminal pattern; not manufacturer CAD |
| D1–D5 | [D_DO-35_SOD27_P7.62mm_Horizontal.step](D_DO-35_SOD27_P7.62mm_Horizontal.step) | Unmodified KiCad DO-35 horizontal diode, 7.62 mm lead pitch; generic package geometry |
| J2–J11 | [PinSocket_1x04_P2.54mm_Vertical.step](PinSocket_1x04_P2.54mm_Vertical.step) | Unmodified KiCad four-position female socket; origin/pitch match the local footprints |
| J1 | [PinSocket_2x05_P2.54mm_Vertical.step](PinSocket_2x05_P2.54mm_Vertical.step) | Unmodified KiCad ten-position female socket, assigned to the underside; negative-X library columns match the project socket |
| X1 | [SMA_Vertical_Generic_Preview.wrl](SMA_Vertical_Generic_Preview.wrl) | Original generic 6 mm diameter, 7.8 mm above-board preview; pin locations match the footprint; no selected part or qualified mating geometry |
| X2 | [SMA_Edge_Generic_Preview.wrl](SMA_Edge_Generic_Preview.wrl) | Original generic edge-SMA preview, with top/bottom fingers around a nominal 1.6 mm board and outward barrel; no selected part, thread detail, or qualified fit |
| W1, W3–W7 | [Wire_Link_P2.54mm.wrl](Wire_Link_P2.54mm.wrl) | Original nominal 0.35 mm diameter hand-fit wire joining pins 1–2, about 0.9 mm above the board |

There are **29 assigned model instances**: the 21 required purchased carrier parts, two alternative SMA options, and six default fitted wire links. The SMA models show available options together; this does not specify that both should be assembled. No plug-in LPF boards are modeled because they are external assemblies whose bands/components have not been selected.

W2/W8/W9 are open in the default assembly, J21–J26 are bare wire terminals, and H1–H4 are mounting holes with no selected hardware. These thirteen bare footprints intentionally have no part-body model. They remain real copper/drill geometry in the 3D viewer. No arbitrary headers, jumpers, spacers, or screws were added to fill those positions.

## Rebuilding and rights

[generate_previews.py](generate_previews.py) regenerates the four original VRML files using only Python's standard library. These use KiCad's 0.1-inch VRML units. Cylindrical surfaces are explicit polygon meshes for compatibility with KiCad's renderer. Original previews and generator code use the repository [MIT license](../../LICENSE.md).

The three STEP files are copied byte-for-byte from **KiCad 10.0.6**. Their relative package paths and SHA-256 hashes are recorded in [sources.json](sources.json). The socket STEP headers retain their original `Copyright (C) 2024, KiCAD` notices. The diode header retains the original `kicad StepUp` / `ksu MCAD` metadata and 2017 creation record. See [KiCad model licensing and attribution](../KICAD-LIBRARY-LICENSE.md); these imported assets retain their KiCad library terms rather than the repository MIT license.

The TX2 preview dimensions follow the [Panasonic TX relay catalog](https://mediap.industry.panasonic.eu/assets/download-files/import/mech_eng_tx.pdf), standard PC-board-terminal family. Internal construction, exact markings, terminal bends, tolerances, and body chamfers are simplified. The two SMA models are explicitly generic. None of these models establishes assembly fit, tolerance clearance, connector compatibility, or RF performance. In particular, check the actual vertical SMA against the filter plugged into slot 1.

The [mechanical finishing tool](../design/finish_mechanics.py) installs model references into the library and saved PCB, creates fitted wire-link footprint variants with identical pads, localizes the mounting-hole footprint, and applies the R3 outline. The full project generator invokes it automatically. Run final ERC/DRC and visually inspect after any regeneration.
