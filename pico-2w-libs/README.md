# Pico 2 W KiCad library assets

Standalone symbol, footprint, and STEP files for Pico-family designs. These files are reference assets, not a validated drop-in library. The supplied KiCad files use version 8 formats. The Wattmeter Shield and Shield Template have their own project-local libraries and do not depend on this directory.

## Files

| File | Contents |
| --- | --- |
| [Raspberrypi pico2 W.kicad_sym](Raspberrypi%20pico2%20W.kicad_sym) | Symbol named `U`, with 40 numbered interface pins and three unnumbered debug pins |
| [Raspberrypi pico2 THT.kicad_mod](Raspberrypi%20pico2%20THT.kicad_mod) | Through-hole footprint with 40 pads identified by signal names |
| [Raspberrypi pico2 w SMD.kicad_mod](Raspberrypi%20pico2%20w%20SMD.kicad_mod) | Footprint marked SMD, with 40 pads of type `connect`, numbered 1–40 |
| [Raspberrypi pico2 W.step](Raspberrypi%20pico2%20W.step) | STEP model whose internal filename identifies a Raspberry Pi Pico 2 model |

## Use in a project

1. Copy the required assets into the destination project's local library directories.
2. Add the `.kicad_sym` file through **Preferences → Manage Symbol Libraries**, using a project-specific library table and a `${KIPRJMOD}` path. Select its symbol `U` and assign the intended value and footprint.
3. Create a project-local footprint library with a `.pretty` directory, copy the required `.kicad_mod` files into it, and register that directory through **Preferences → Manage Footprint Libraries**. This directory itself is a collection of loose files, not a packaged `.pretty` library.
4. In the footprint's 3D-model settings, select the copied STEP file using a `${KIPRJMOD}` path. Check its alignment and dimensions in the 3D Viewer.
5. Resolve the pin and pad issues below, compare the result with the exact module's pinout and mechanical drawing, then run ERC and DRC in the destination project.

## Compatibility limits

- The THT pad identifiers are signal names such as `GP0`, `GND`, and `3V3`; the symbol's interface pins are numbered 1–40. KiCad connects by pin/pad identifier, so these definitions do not match. Verify and correct the mapping in the destination library before using this pair.
- The symbol's GND, SWCLK, and SWDIO debug pins have empty pin numbers. Neither footprint includes three additional debug pads. Define the intended debug connection and numbering before using those pins.
- The SMD footprint's `connect` pads require review for the intended mounting and paste process. Its 1–40 numbering alone does not establish correct physical pin mapping or assembly compatibility.
- The SMD model reference is `${KICAD_LIB_TEMPLATE}/Raspberrypi PICO 2W/Raspberrypi pico2 W.step`. It does not resolve relative to this directory automatically. Its saved transform is offset `(1, −7, 0)` mm, scale `(1, 1, 1)`, and rotation `(90, 180, −180)` degrees; alignment is unverified. The THT footprint has no attached model.
- The STEP file's internal filename is `Raspberry Pi Pico 2 3D CAD Model 24 07 24.STEP`, despite the external filename containing `W`. Compatibility with the Pico 2 W, including antenna geometry, is unverified.

There is no complete schematic or PCB in this directory on which to run ERC or DRC. Physical fit, assembly, pin mapping, and RF suitability remain unverified.

## Source and license

The supplied README identifies the assets as MIT-licensed, but the files include no accompanying author attribution, upstream URL, or full license notice. Their provenance and applicable copyright notice remain unverified. The repository's [MIT license](../LICENSE.md) covers repository-owned work; it does not establish ownership or licensing of these supplied assets. Preserve any original attribution and license notice obtained from their source.

## Repository contents

Keep the symbol, footprints, STEP model, and documentation in Git. The repository's root ignore rules exclude KiCad caches, backups, local preferences, and outputs under `generated/`, `production/`, or `fabrication/`. The local ignore rule excludes `jlcpcb/` plugin state and output. Reusable library and model files remain tracked.
