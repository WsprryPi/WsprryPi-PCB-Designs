# WsprryPi Zero GPIO fabrication notes

Status: candidate JLCPCB process instructions for the current two-layer, 1.6 mm board. The board is not ready for order; JLCPCB has not accepted this selective process for the exact fabrication package.

## U31 exposed-pad thermal holes

The U31 footprint has nine plated 0.20 mm drill holes with 0.50 mm copper pads beneath its exposed ground pad. Their centers form a 3 × 3 grid at X = 136.479505, 137.454505, and 138.429505 mm and Y = 82.404256, 83.379256, and 84.354256 mm in board coordinates.

The PCB's `User.1` layer is named `sk` and contains nine filled 0.50 mm diameter circles at exactly those centers. This is a **process-selection layer only**: its graphics are not copper, solder mask, silkscreen, or additional drills. Export it separately as a Gerber alongside the usual fabrication and drill files. KiCad 10 exports it as `WsprryPi Zero GPIO-sk.gbr` when `User.1` is included in the plotted layers. Overlay it with the plated-drill and copper Gerbers to verify that it marks only the nine U31 holes.

Request **epoxy-filled and copper-capped via-in-pad treatment** for only these nine holes, leaving U31's top exposed pad solderable. The other board vias inherit front- and back-side tenting from Board Setup. Other plated component holes must remain open for assembly. Do not select holes by 0.20 mm drill diameter: many ordinary vias also have that drill size.

These nine holes are currently modeled as through-hole pads in the footprint, not KiCad via objects. KiCad's per-via protection properties therefore do not identify them as filled and capped. Have JLCPCB confirm that its CAM process will treat the nine `sk` marks as the requested via-in-pad holes on this **two-layer** board, while preserving the component holes and ordinary via tenting. If JLCPCB requires native via objects or a different drill/pad structure, revise the footprint and PCB before preparing the order package.

## JLCPCB package and order review

1. Export and inspect the copper, mask, plated and non-plated drill, board-outline, and `sk` Gerbers. Include an annotated U31 image or drill drawing identifying the same nine holes.
2. Choose JLCPCB's **Epoxy-filled & Capped** via-covering process if offered for the quoted two-layer configuration. In PCB Order Notes, enter:

   > Epoxy-fill and copper-cap only the nine 0.20 mm holes marked on the `sk` Gerber beneath U31's exposed pad. Keep its front pad solderable. Tent all other vias on both sides. Leave all component through-holes open. These nine holes are modeled as through-hole pads in KiCad; please confirm selective via-in-pad treatment for this two-layer, 1.6 mm board before production.

3. Select **Confirm Production Files**. Check JLCPCB's prepared `sk`, drill, copper, and mask layers against the submitted package before approving production. Obtain explicit CAM acceptance of the selective treatment and U31's stencil/paste apertures.

JLCPCB's [via-covering guidance](https://jlcpcb.com/help/article/pcb-via-covering) distinguishes epoxy-filled/capped via-in-pad from ink plugging and asks customers to identify the selected holes. Its [Gerber preparation guide](https://jlcpcb.com/help/article/gerber-files-preparation) specifies an `sk` layer for holes to be filled. Its [production-file review guide](https://jlcpcb.com/help/article/how-to-confirm-the-production-file) explains how to inspect the CAM files before release.

The separate `YA9308-AEC` transformer procurement and physical/RF qualification gates in [README.md](README.md) and [AMPLIFIER-DESIGN.md](AMPLIFIER-DESIGN.md) still apply.
