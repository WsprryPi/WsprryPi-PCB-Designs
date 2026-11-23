"""Compare the saved C-first LPF values with a proposed L-first board.

Python 3 standard library.
Reads the workbook directly as OOXML, without changing or recalculating it.
Run: python3 model/model_lpf.py (from the LPF directory, or any directory).
"""

from pathlib import Path
from zipfile import ZipFile
import csv
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "reference"
Z0 = 50.0
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def workbook_rows():
    with ZipFile(REFERENCE / "LPF-Values.xlsx") as z:
        strings = ["".join(t.itertext()) for t in
                   ET.fromstring(z.read("xl/sharedStrings.xml"))]
        root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        rows = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            cells = {}
            for cell in row:
                val = cell.find("m:v", NS)
                inline = cell.find("m:is", NS)
                text = val.text if val is not None else (
                    "".join(inline.itertext()) if inline is not None else "")
                if cell.get("t") == "s":
                    text = strings[int(text)]
                cells[re.sub(r"\d", "", cell.get("r"))] = text
            if cells.get("A") and cells["A"] != "Band":
                rows.append(cells)
        return rows


def quantity(text):
    scales = {"pF": 1e-12, "nF": 1e-9, "µH": 1e-6,
              "nH": 1e-9, "kHz": 1e3, "MHz": 1e6}
    return sum(float(v.replace(",", "")) * scales[u] for v, u in
               re.findall(r"([\d.,]+)\s*(pF|nF|µH|nH|kHz|MHz)", text))


def network(values, first, f, q=None):
    """ABCD cascade; S21 is available-power normalized for equal real ports.

    Finite Q is a sensitivity model: each coil has Rseries = omega*L/Q.
    Capacitors remain ideal. No mutual coupling or self resonance.
    """
    a, b, c, d = 1+0j, 0j, 0j, 1+0j
    w = 2 * math.pi * f
    for i, value in enumerate(values):
        kind = first if i % 2 == 0 else ("L" if first == "C" else "C")
        if kind == "L":
            z = 1j*w*value + (w*value/q if q else 0)
            b, d = a*z+b, c*z+d
        else:
            y = 1j*w*value
            a, c = a+b*y, c+d*y
    den = a + b/Z0 + c*Z0 + d
    s21 = 2/den
    s11 = (a + b/Z0 - c*Z0 - d)/den
    zin = (a*Z0+b)/(c*Z0+d)
    return -20*math.log10(abs(s21)), s21, s11, zin


def cutoff(values, first, f):
    lo, hi = f*.8, f*2
    # Locate the final 3 dB crossing, beyond the passband ripple.
    assert network(values, first, lo)[0] < 3
    assert network(values, first, hi)[0] > 3
    for _ in range(70):
        mid = (lo+hi)/2
        if network(values, first, mid)[0] > 3:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2


def cap_pair(target):
    e24 = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30,
           33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
    options = [x*10.0**e for e in range(-13, -7) for x in e24]
    pairs = [(x, 0) for x in options] + [
        (x, y) for x in options for y in options if 0 < y <= x <= target*1.1]
    return min(pairs, key=lambda p: (abs(sum(p)-target), bool(p[1])))


def eng(v, kind):
    if kind == "L":
        return f"{v/1e-6:.5g} µH" if v >= 1e-6 else f"{v/1e-9:.5g} nH"
    return f"{v/1e-9:.5g} nF" if v >= 1e-9 else f"{v/1e-12:.5g} pF"


def prototype(n, ripple):
    gamma = math.sinh(math.asinh(1/math.sqrt(10**(ripple/10)-1))/n)
    aa = [math.sin((2*k-1)*math.pi/(2*n)) for k in range(1, n+1)]
    g = [2*aa[0]/gamma]
    for k in range(1, n):
        g.append(4*aa[k-1]*aa[k]/((gamma**2+math.sin(k*math.pi/n)**2)*g[-1]))
    return g


def main():
    results = []
    error = 0
    conservation = 0
    for row in workbook_rows():
        f = quantity(row["D"])
        old = [quantity(row[k]) for k in "KLMNOPQ"]
        dual = [v*Z0**2 if i % 2 == 0 else v/Z0**2
                for i, v in enumerate(old)]
        pairs = [cap_pair(dual[i]) for i in (1, 3, 5)]
        build = dual.copy()
        for i, pair in zip((1, 3, 5), pairs):
            build[i] = sum(pair)
        for j in range(401):
            testf = f * 10**(-2+j*3/400)
            x, y = network(old, "C", testf), network(dual, "L", testf)
            error = max(error, abs(x[1]-y[1]))
            conservation = max(conservation, abs(abs(x[1])**2+abs(x[2])**2-1))
        metric = lambda vals, first, q=None: [
            network(vals, first, f*n, q)[0] for n in (1, 2, 3, 4, 5)]
        results.append({
            "band": row["A"], "source_row": len(results)+2,
            "fundamental_Hz": f, "C_first_SI": old, "L_first_exact_SI": dual,
            "L_first_build_SI": build, "build_cap_pairs_F": pairs,
            "C_first_cutoff_Hz": cutoff(old, "C", f),
            "L_first_build_cutoff_Hz": cutoff(build, "L", f),
            "C_first_attenuation_dB_f_2f_3f_4f_5f": metric(old, "C"),
            "L_first_build_attenuation_dB_f_2f_3f_4f_5f": metric(build, "L"),
            "Q_sensitivity_fundamental_dB": {str(q): {
                "C_first": metric(old, "C", q)[0],
                "L_first_exact": metric(dual, "L", q)[0]} for q in (50, 100)},
            "input_impedance_ohms_f_2f_3f": {first: [
                [network(vals, first, f*n)[3].real, network(vals, first, f*n)[3].imag]
                for n in (1, 2, 3)] for first, vals in (("C", old), ("L", dual))},
            "workbook_cutoff_Hz": quantity(row["I"]), "workbook_fundamental_dB": float(row["J"])
        })
        candidates = {}
        for ripple in (1, .1):
            values = [v*Z0/(2*math.pi*f) if i % 2 == 0 else v/(Z0*2*math.pi*f)
                      for i, v in enumerate(prototype(5, ripple))]
            rounded = values.copy()
            pair = cap_pair(values[1])
            rounded[1] = rounded[3] = sum(pair)
            candidates[str(ripple)] = {
                "L_first_exact_SI": values, "L_first_build_SI": rounded,
                "build_cap_pair_F": pair,
                "exact_cutoff_Hz": cutoff(values, "L", f),
                "exact_attenuation_dB_f_2f_3f_4f_5f": metric(values, "L"),
                "build_attenuation_dB_f_2f_3f_4f_5f": metric(rounded, "L"),
                "Q_sensitivity_fundamental_dB": {str(q): metric(values, "L", q)[0]
                                                    for q in (50, 100)},
            }
        results[-1]["five_element_ripple_dB"] = candidates
    # Independent analytic 7th-order 1 dB Chebyshev prototype check.
    g = prototype(7, 1)
    analytic_error = 0
    for n, ripple in ((7, 1), (5, 1), (5, .1)):
        for k in range(1, 301):
            x = k/100
            t = math.cos(n*math.acos(x)) if x <= 1 else math.cosh(n*math.acosh(x))
            expected = 10*math.log10(1+(10**(ripple/10)-1)*t*t)
            analytic_error = max(analytic_error, abs(network(
                [v*Z0 if i % 2 == 0 else v/Z0 for i, v in enumerate(prototype(n, ripple))],
                "L", x/(2*math.pi))[0]-expected))
    checks = {"maximum_complex_S21_duality_error": error,
              "maximum_lossless_power_conservation_error": conservation,
              "maximum_analytic_Chebyshev_error_dB": analytic_error,
              "maximum_workbook_loss_difference_dB": max(abs(r["C_first_attenuation_dB_f_2f_3f_4f_5f"][0]-r["workbook_fundamental_dB"]) for r in results),
              "maximum_workbook_cutoff_difference_Hz": max(abs(r["C_first_cutoff_Hz"]-r["workbook_cutoff_Hz"]) for r in results)}
    assert error < 1e-10 and conservation < 1e-10 and analytic_error < 1e-9
    assert checks["maximum_workbook_loss_difference_dB"] < .00051
    assert checks["maximum_workbook_cutoff_difference_Hz"] < .51
    grouped = []
    for high, low in (("60 & 80m", "80m"), ("30 & 40m", "40m"),
                      ("20 & 22m", "22m"), ("15 & 17m", "17m"), ("10 & 12m", "12m")):
        upper = next(r for r in results if r["band"] == high)
        lower = next(r for r in results if r["band"] == low)
        vals = upper["five_element_ripple_dB"]["1"]["L_first_exact_SI"]
        grouped.append({"build": high, "lower_band": low,
                        "lower_fundamental_Hz": lower["fundamental_Hz"],
                        "attenuation_dB_f_2f_3f": [network(vals, "L", lower["fundamental_Hz"]*n)[0]
                                                   for n in (1, 2, 3)]})
    source_manifest = json.loads((REFERENCE/"source-manifest.json").read_text())
    assert hashlib.sha256((REFERENCE/"LPF-Values.xlsx").read_bytes()).hexdigest() == source_manifest["source_sha256"]["LPF-Values.xlsx"]
    data = {"reference_impedance_ohms": Z0, "prototype_g": g,
            "source_project": source_manifest["source_project"],
            "source_sha256": source_manifest["source_sha256"],
            "checks": checks, "bands": results, "five_element_shared_band_checks": grouped}
    (HERE/"results.json").write_text(json.dumps(data, indent=2)+"\n")
    with (HERE/"band-values.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["Band", "Fundamental_Hz", "L1_L7_H", "L3_L5_H", "C2_C6_F", "C4_F", "Build_C2_C6_pair", "Build_C4_pair", "C_first_fundamental_dB", "Build_fundamental_dB", "Build_2f_dB", "Build_3f_dB"])
        for r in results:
            d = r["L_first_exact_SI"]
            pair = lambda p: " + ".join(eng(v, "C") for v in p if v)
            writer.writerow([r["band"], r["fundamental_Hz"], d[0], d[2], d[1], d[3], pair(r["build_cap_pairs_F"][0]), pair(r["build_cap_pairs_F"][1]), r["C_first_attenuation_dB_f_2f_3f_4f_5f"][0], *r["L_first_build_attenuation_dB_f_2f_3f_4f_5f"][:3]])
    print(json.dumps(checks, indent=2))
    print("\n| Band | L1 = L7 | L3 = L5 | C2 = C6, exact | C4, exact |")
    for r in results:
        d = r["L_first_exact_SI"]
        print(f'| {r["band"]} | {eng(d[0], "L")} | {eng(d[2], "L")} | {eng(d[1], "C")} | {eng(d[3], "C")} |')
    with (HERE/"five-element-values.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["Band", "Fundamental_Hz", "Ripple_dB", "L1_L5_H", "L3_H", "C2_C4_F", "Build_cap_pair", "Build_fundamental_dB", "Build_2f_dB", "Build_3f_dB"])
        for r in results:
            for ripple, candidate in r["five_element_ripple_dB"].items():
                d = candidate["L_first_exact_SI"]
                pair = " + ".join(eng(v, "C") for v in candidate["build_cap_pair_F"] if v)
                writer.writerow([r["band"], r["fundamental_Hz"], ripple, d[0], d[2], d[1], pair,
                                 *candidate["build_attenuation_dB_f_2f_3f_4f_5f"][:3]])
    return results


if __name__ == "__main__":
    main()
