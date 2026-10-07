# J1 SMA connector

J1 specifies the [Adafruit 1865](https://www.adafruit.com/product/1865), a standard-polarity SMA female edge-launch connector for a 1.6 mm PCB. The board thickness is 1.6 mm. J1 is fitted by hand and excluded from the factory BOM and machine placement.

## Footprint

The [local footprint](pico-wattmeter.pretty/SMA_Adafruit_1865_EdgeMount.kicad_mod) uses the `SMA_EDGELAUNCH` land pattern from the public-domain [Adafruit Eagle Library](https://github.com/adafruit/Adafruit-Eagle-Library), with edge-facing copper clearance adapted for this board. The [connector drawing](https://cdn-shop.adafruit.com/product-files/1865/C2387-001_datasheet.pdf) specifies the body and contact dimensions. Adafruit attribution is included in the footprint description.

| Feature | Geometry |
| --- | --- |
| Signal | Pad 1, front copper/mask, 1.27 mm wide |
| Ground | Four pads numbered 2, two per board face, 1.524 mm wide |
| Ground pad centers | ±2.54 mm from the signal centerline |
| Land extent from seating edge | 0.500–4.064 mm; length 3.564 mm |
| Footprint origin | Connector seating edge on the signal centerline |
| Board placement | (120.130, 89.688) mm, rotation −90° |
| Soldering | Hand soldering; no stencil-paste apertures |

The seating edge coincides with the board's left edge. The lands provide 0.5 mm copper-to-edge clearance and at least 3.3 mm nominal contact overlap.

The connector drawing places the ground-leg centers at ±2.75 mm, while the published land centers are ±2.54 mm. The 1.524 mm lands cover the nominal 1.0 mm legs: one land spans 1.778–3.302 mm and its leg spans 2.250–3.250 mm from the centerline.

Physical fit and RF performance are unverified. Confirm the supplied connector against the drawing before assembly. The footprint's barrel outline is simplified; no 3D model is attached.

## Probable Amazon alternative: Superbat B09V5811S7

Recorded on 2026-10-06 as a **probable solution, pending sample fit and RF verification**: [Superbat SMA female PCB edge-mount connector, 10-pack](https://www.amazon.com/dp/B09V5811S7?th=1), ASIN **B09V5811S7**. Select **“0.062 inch Straight Connector”**. The listing identifies a standard-polarity SMA female, 50 Ω, soldered end-launch connector for a nominal 0.062 inch (1.57 mm) PCB, the same thickness class as these 1.6 mm boards.

The [seller's dimension drawing](https://m.media-amazon.com/images/I/61nZ0VUoLFL._AC_SL1500_.jpg) supports the following nominal land-pattern comparison:

| Feature | Superbat drawing / listing | Existing Adafruit-derived footprint |
| --- | --- | --- |
| Ground-leg center spacing | 5.06 mm, calculated from 4.10 mm inner spacing + 0.96 mm leg width | 5.08 mm between land centers |
| Ground-leg / land width | 0.96 mm leg | 1.524 mm land |
| Rear soldering-finger length | 3.94 mm | Approximately 3.9 mm intended contact length; copper extends 0.500–4.064 mm from the seating edge |
| PCB thickness class | 0.062 inch / 1.57 mm | 1.6 mm |

This makes the Superbat part a probable mechanical substitute for **J1 on Pico 2W Wattmeter Shield**, **J51 on WsprryPi Zero GPIO BS170**, and **J51 on WsprryPico GPIO Shield**, which use independent copies of `SMA_Adafruit_1865_EdgeMount`. It is not yet a qualified replacement or a change to the selected KiCad symbol, footprint, supplier fields, or assembly exclusions.

The Superbat has a longer bulkhead barrel and a nut; the existing Adafruit outline/model does not establish clearance for that body. Before accepting the substitute, check a sample on the exact board revision for seating on the 1.6 mm edge, signal and all four ground-finger contact, barrel/nut/cable clearance, and solder-joint support. Confirm continuity and absence of a signal-to-ground short, then verify RF performance in the assembled board's intended frequency range. Record the received variant, board revision, assembly, and measurement setup with the results. Seller dimensions and impedance claims are not measured assembly evidence.

Do not confuse this option with the previously reviewed **bnafes B09N1RBBFX “4 Pins Stand”** part: its photos show a square through-hole leg arrangement with a centered signal pin, so it was not accepted as a substitute for these edge-launch footprints. The Superbat listing's 0.051 inch and other mounting variants are also outside this candidate record.
