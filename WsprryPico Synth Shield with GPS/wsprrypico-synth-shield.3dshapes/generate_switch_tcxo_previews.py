#!/usr/bin/env python3
"""Regenerate original MIT-licensed SW11/Y41 visual previews, not supplier CAD.

XUNPU drawing: https://datasheet.lcsc.com/datasheet/pdf/d36ef8d43e89de62c59fa43456d00a3f.pdf?productCode=C455280
KDS drawing: https://www.kds.info/wp-content/uploads/2015/11/dsb321sdn-1-d_pdf_en-1.pdf
Body envelopes follow nominal package dimensions; internal geometry, colors,
terminal detail and tolerances are simplified. KiCad VRML units are 2.54 mm.
The footprint's positive Y axis points down; model positive Y points up.
"""

from pathlib import Path
import math

ROOT = Path(__file__).resolve().parent
UNIT = 2.54
BLACK = (0.08, 0.09, 0.10)
METAL = (0.73, 0.75, 0.77)
GOLD = (0.72, 0.57, 0.24)
CERAMIC = (0.70, 0.67, 0.58)


def vector(values):
    return " ".join(f"{v / UNIT:.9f}" for v in values)


def shape(center, geometry, color, rotation=""):
    appearance = " ".join(str(v) for v in color)
    return (
        "Transform {\n"
        f"  translation {vector(center)}\n"
        f"  {rotation}\n"
        "  children [ Shape {\n"
        "    appearance Appearance { material Material { "
        f"diffuseColor {appearance} specularColor 0.25 0.25 0.25 "
        "shininess 0.4 } }\n"
        f"    geometry {geometry}\n"
        "  } ]\n"
        "}\n"
    )


def box(center, size, color):
    return shape(center, f"Box {{ size {vector(size)} }}", color)


def cylinder(x, y, z_bottom, height, radius, color):
    # Explicit faces keep the actuator and pin marker visible in KiCad's loader.
    count = 48
    points = []
    for z in (-height / 2, height / 2):
        for i in range(count):
            angle = i * 2 * math.pi / count
            points.append((radius * math.cos(angle), radius * math.sin(angle), z))
    points += [(0, 0, -height / 2), (0, 0, height / 2)]
    faces = []
    for i in range(count):
        j = (i + 1) % count
        faces += [
            (i, j, count + j, count + i),
            (2 * count, j, i),
            (2 * count + 1, count + i, count + j),
        ]
    coordinates = ",\n".join(vector(point) for point in points)
    indices = ",\n".join(" ".join(str(i) for i in face) + " -1" for face in faces)
    geometry = (
        "IndexedFaceSet { solid TRUE creaseAngle 0.6 "
        f"coord Coordinate {{ point [\n{coordinates}\n] }} "
        f"coordIndex [\n{indices}\n] }}"
    )
    return shape((x, y, z_bottom + height / 2), geometry, color)


def write(name, description, parts):
    header = (
        "#VRML V2.0 utf8\n"
        "# Original repository model; MIT license.\n"
        f"# {description}\n"
        "# Visual preview only; not supplier CAD or physical-fit qualification.\n"
        "# Coordinates use KiCad 0.1-inch VRML units.\n"
    )
    (ROOT / name).write_text(header + "".join(parts))


def main():
    switch = [
        box((0, 0, 0.775), (3.90, 3.00, 1.25), BLACK),
        box((0, 0, 1.45), (3.90, 3.00, 0.10), METAL),
        cylinder(0, 0, 1.50, 0.50, 0.90, BLACK),
    ]
    for x in (-2.15, 2.15):
        switch.append(box((x, 0, 0.075), (0.70, 1.30, 0.15), METAL))
    for x in (-1.91, 1.91):
        for y in (-1.0, 1.0):
            switch.append(box((x, y, 1.0), (0.08, 0.40, 0.80), METAL))
    write(
        "XUNPU_TS1088R_3.9x3x2_Preview.wrl",
        "TS-1088R-02026: 3.90 x 3.00 mm body, 2.00 mm total height, 1.80 mm actuator.",
        switch,
    )

    tcxo = [
        box((0, 0, 0.19), (3.20, 2.50, 0.30), CERAMIC),
        box((0, 0, 0.62), (3.12, 2.42, 0.56), METAL),
        cylinder(-1.02, -0.73, 0.900, 0.005, 0.13, BLACK),
    ]
    for x in (-1.25, 1.25):
        for y in (-0.70, 0.70):
            tcxo.append(box((x, y, 0.02), (0.70, 0.80, 0.04), GOLD))
    write(
        "KDS_DSB321SDN_3.2x2.5x0.9_Preview.wrl",
        "DSB321SDN family: nominal 3.20 x 2.50 x 0.90 mm; pin-1 dot at local lower left.",
        tcxo,
    )


if __name__ == "__main__":
    main()
