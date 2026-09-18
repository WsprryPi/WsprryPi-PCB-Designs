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
