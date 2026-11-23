"""Place the top 5th-order Chebyshev transmission maximum over WSPR/QRSS.

Uses the source workbook's B/C frequency windows through model_lpf; no edits
to the workbook or CAD. Python standard library only.
"""
import csv
import hashlib
import json
import math
import re
from model_lpf import HERE, REFERENCE, Z0, cap_pair, eng, network, prototype, workbook_rows

TOP_ZERO = math.cos(math.pi/10)


def frequency_window(text):
    """Workbook forms: center kHz +/- width Hz, or low - high kHz."""
    text = text.replace(",", "").strip()
    match = re.fullmatch(r"([\d.]+)\s*(kHz|MHz)\s*\+/-\s*([\d.]+)\s*Hz", text)
    if match:
        center = float(match[1]) * {"kHz": 1e3, "MHz": 1e6}[match[2]]
        halfwidth = float(match[3])
        return center-halfwidth, center+halfwidth
    match = re.fullmatch(r"([\d.]+)\s*-\s*([\d.]+)\s*(kHz|MHz)", text)
    if match:
        scale = {"kHz": 1e3, "MHz": 1e6}[match[3]]
        return float(match[1])*scale, float(match[2])*scale
    raise ValueError(f"Unrecognized frequency window: {text!r}")


def sample_window(values, window, harmonic=1, q=None):
    lo, hi = window
    losses = [network(values, "L", (lo+(hi-lo)*i/200)*harmonic, q)[0]
              for i in range(201)]
    return {"minimum_dB": min(losses), "maximum_dB": max(losses)}


def main():
    rows = []
    exact_zero_error = 0
    impedance_error = 0
    analytic_error = 0
    for source in workbook_rows():
        windows = {mode: frequency_window(source[col]) for mode, col in
                   (("WSPR", "B"), ("QRSS", "C")) if source.get(col)}
        envelope = [min(w[0] for w in windows.values()), max(w[1] for w in windows.values())]
        f0 = sum(envelope)/2
        fp = f0/TOP_ZERO
        edge = [g*Z0/(2*math.pi*f0) if i % 2 == 0 else g/(Z0*2*math.pi*f0)
                for i, g in enumerate(prototype(5, 1))]
        tuned = [v*TOP_ZERO for v in edge]
        pair = cap_pair(tuned[1])
        rounded = tuned.copy()
        rounded[1] = rounded[3] = sum(pair)
        attenuation = lambda values, q=None: [network(values, "L", f0*n, q)[0]
                                             for n in (1, 2, 3, 4, 5)]
        exact_zero_error = max(exact_zero_error, abs(attenuation(tuned)[0]))
        impedance_error = max(impedance_error, abs(network(tuned, "L", f0)[3]-Z0))
        assert network(tuned, "L", f0*.999)[0] > 1e-6
        assert network(tuned, "L", f0*1.001)[0] > 1e-6
        for n, loss in enumerate(attenuation(tuned), 1):
            x = n*TOP_ZERO
            t = math.cos(5*math.acos(x)) if x <= 1 else math.cosh(5*math.acosh(x))
            expected = 10*math.log10(1+(10**.1-1)*t*t)
            analytic_error = max(analytic_error, abs(expected-loss))
        rows.append({
            "band": source["A"], "source_frequency_text": {mode: source[col] for mode, col in
                (("WSPR", "B"), ("QRSS", "C")) if source.get(col)},
            "mode_windows_Hz": windows, "combined_envelope_Hz": envelope,
            "target_minimum_Hz": f0, "ripple_edge_Hz": fp,
            "edge_design_SI": edge, "minimum_design_SI": tuned,
            "rounded_cap_design_SI": rounded, "cap_pair_F": pair,
            "edge_attenuation_dB_f0_2f0_3f0_4f0_5f0": attenuation(edge),
            "minimum_attenuation_dB_f0_2f0_3f0_4f0_5f0": attenuation(tuned),
            "rounded_attenuation_dB_f0_2f0_3f0_4f0_5f0": attenuation(rounded),
            "exact_modes": {mode: {"fundamental": sample_window(tuned, window),
                                  "second_harmonic": sample_window(tuned, window, 2),
                                  "third_harmonic": sample_window(tuned, window, 3)}
                            for mode, window in windows.items()},
            "rounded_modes": {mode: sample_window(rounded, window) for mode, window in windows.items()},
            "Q_sensitivity": {str(q): {"edge_fundamental_dB": attenuation(edge, q)[0],
                                        "minimum_fundamental_dB": attenuation(tuned, q)[0],
                                        "minimum_mode_windows": {mode: sample_window(tuned, window, q=q)
                                                                 for mode, window in windows.items()}}
                              for q in (50, 100)},
            "common_LC_scaling_sensitivity": {str(scale): attenuation([v*scale for v in tuned])[0]
                                             for scale in (.95, .98, .99, 1.01, 1.02, 1.05)}
        })
    assert len(rows) == 15 and sum("QRSS" in r["mode_windows_Hz"] for r in rows) == 13
    assert frequency_window("475.700 kHz +/- 100 Hz") == (475600, 475800)
    assert frequency_window("13,555.275 - 13,555.675 kHz") == (13555275, 13555675)
    assert exact_zero_error < 1e-10 and impedance_error < 1e-9 and analytic_error < 1e-9
    worst = max(v["fundamental"]["maximum_dB"] for r in rows for v in r["exact_modes"].values())
    data = {"scope": "5-element L-first, 1 dB ripple, 50 ohm ports; minimum over listed WSPR/QRSS windows",
            "normalized_top_zero": TOP_ZERO, "edge_to_target_ratio": 1/TOP_ZERO,
            "workbook_sha256": hashlib.sha256((REFERENCE/"LPF-Values.xlsx").read_bytes()).hexdigest(),
            "checks": {"maximum_ideal_target_attenuation_magnitude_dB": exact_zero_error,
                       "maximum_input_match_error_ohms": impedance_error,
                       "maximum_analytic_harmonic_error_dB": analytic_error,
                       "maximum_ideal_loss_across_all_listed_modes_dB": worst,
                       "rows": len(rows), "QRSS_rows": 13}, "bands": rows}
    (HERE/"minimum-loss-results.json").write_text(json.dumps(data, indent=2)+"\n")
    with (HERE/"minimum-loss-values.csv").open("w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["Band", "Target_minimum_Hz", "WSPR_low_Hz", "WSPR_high_Hz", "QRSS_low_Hz", "QRSS_high_Hz",
                         "L1_L5_H", "L3_H", "C2_C4_F", "Candidate_cap_pair", "Rounded_target_loss_dB",
                         "Worst_ideal_mode_loss_dB", "Worst_rounded_mode_loss_dB", "Worst_mode_2f_attenuation_dB",
                         "Worst_mode_3f_attenuation_dB"])
        for r in rows:
            v = r["minimum_design_SI"]
            pair = " + ".join(eng(p,"C") for p in r["cap_pair_F"] if p)
            writer.writerow([r["band"],r["target_minimum_Hz"], *r["mode_windows_Hz"]["WSPR"],
                             *r["mode_windows_Hz"].get("QRSS", ("", "")), v[0],v[2],v[1],pair,
                             r["rounded_attenuation_dB_f0_2f0_3f0_4f0_5f0"][0],
                             max(x["fundamental"]["maximum_dB"] for x in r["exact_modes"].values()),
                             max(x["maximum_dB"] for x in r["rounded_modes"].values()),
                             min(x["second_harmonic"]["minimum_dB"] for x in r["exact_modes"].values()),
                             min(x["third_harmonic"]["minimum_dB"] for x in r["exact_modes"].values())])
    print(json.dumps(data["checks"], indent=2))
    for r in rows:
        v = r["minimum_design_SI"]
        print(r["band"], r["target_minimum_Hz"], eng(v[0],"L"),eng(v[2],"L"),eng(v[1],"C"))
    return data


if __name__ == "__main__":
    main()
