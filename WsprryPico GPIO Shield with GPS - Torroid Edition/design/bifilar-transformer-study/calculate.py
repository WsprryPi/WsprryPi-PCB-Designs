#!/usr/bin/env python3
"""Calculated screening of a proposed 12.5-to-50-ohm drain autotransformer.

Run with Python 3. No third-party packages. This is not a measured RF model.
Manufacturer material CSVs are small-signal, zero-DC data. Winding capacitance,
leakage, nonlinearity, temperature, DC-dependent RF permeability, PCB parasitics,
the BS170, and the actual LPF are not included in the material-only model.
The 50% inductance retention scenario is an assumption, not a guaranteed rating.
"""
import bisect
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
F_LOW = 135700.0
F_HIGH = 29.7e6
R_DRAIN = 12.5
AE = 24.3e-6
LE = 0.052
CORES = [
    dict(material='77', part='5977000621', turns=15, al=1270e-9,
         tolerance=0.30, positive_tolerance=0.25, mu_reference=2000,
         outer_m=0.02185, inner_m=0.0124, height_m=0.0071,
         ae_m2=24.3e-6,le_m=0.052,role='Selected within-outline prototype',
         source='https://fair-rite.com/product/toroids-5977000621/'),
    dict(material='43', part='5943000621', turns=24, al=470e-9,
         tolerance=0.25, positive_tolerance=0.20, mu_reference=800,
         outer_m=0.02185, inner_m=0.0124, height_m=0.0071,
         ae_m2=24.3e-6,le_m=0.052,role='Same-size HF comparison',
         source='https://fair-rite.com/product/toroids-5943000621/'),
    dict(material='77', part='5977004921', turns=14, al=1400e-9,
         tolerance=0.30,positive_tolerance=0.25,mu_reference=2000,
         outer_m=0.0169,inner_m=0.0088,height_m=0.0071,
         ae_m2=20e-6,le_m=0.039,role='Smaller; higher DC magnetic stress',
         source='https://fair-rite.com/product/toroids-5977004921/'),
    dict(material='77', part='5977002721', turns=11, al=2250e-9,
         tolerance=0.30,positive_tolerance=0.25,mu_reference=2000,
         outer_m=0.0368,inner_m=0.02195,height_m=0.0137,
         ae_m2=78e-6,le_m=0.089,role='Superseded overhanging mount',
         source='https://fair-rite.com/product/toroids-5977002721/'),
]
FREQUENCIES = [135700, 472000, 1.8e6, 3.5e6, 5.3e6, 7e6,
               10.1e6, 14e6, 18.1e6, 21e6, 24.9e6, 28e6, 29.7e6]

def read_material(material):
    rows = []
    path = ROOT / 'inputs' / f'fair-rite-{material}.csv'
    for row in csv.reader(path.read_text(errors='replace').splitlines()):
        try:
            values = tuple(float(x) for x in row[:3])
        except ValueError:
            continue
        if len(values) == 3:
            rows.append(values)
    return sorted(rows)

def permeability(rows, frequency):
    fs = [r[0] for r in rows]
    if not fs[0] <= frequency <= fs[-1]:
        raise ValueError('Frequency outside material data')
    i = min(max(bisect.bisect_left(fs, frequency), 1), len(fs)-1)
    a, b = rows[i-1], rows[i]
    t = math.log(frequency/a[0]) / math.log(b[0]/a[0])
    return tuple(a[k] + t*(b[k]-a[k]) for k in (1, 2))

def material_impedance(core, frequency):
    u, v = permeability(read_material(core['material']), frequency)
    scale = 2*math.pi*frequency*core['al']*core['turns']**2/core['mu_reference']
    return scale*complex(v, u)

def matched_shunt_loss(z):
    # Ideal transformer with magnetizing Z shunting a 12.5-ohm matched port.
    return 20*math.log10(abs(1 + R_DRAIN/(2*z)))

def ruthroff_delay_loss(frequency, length, velocity_factor):
    # Ruthroff 1959, matched 1:4 unbalanced transformer, equation (1).
    theta = 2*math.pi*frequency*length/(299792458*velocity_factor)
    ratio = ((1+3*math.cos(theta))**2 + 4*math.sin(theta)**2)/(4*(1+math.cos(theta))**2)
    return 10*math.log10(ratio)

def hash_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

results = dict(f_low_hz=F_LOW, f_high_hz=F_HIGH, r_drain_ohm=R_DRAIN,
               ae_m2=AE, le_m=LE, cores=[], material_only_sweep=[])
for core in CORES:
    n = core['turns']
    ae=core['ae_m2'];le=core['le_m']
    l0 = core['al']*n*n
    lmin = l0*(1-core['tolerance'])
    scenario = lmin*0.5
    # Rectangular path around core cross-section, plus an approximate wire bend
    # allowance. Actual twist lay and lead length must be measured.
    # Catalog exterior limits give a conservative coated-core wire length.
    # Magnetic effective area/path above exclude the coating.
    pair_length = n*(2*core['height_m'] + core['outer_m']-core['inner_m'] + 0.002) + 0.030
    item = dict(**core, l_nominal_h=l0, l_al_minimum_h=lmin,
                l_assumed_50pct_retained_h=scenario,
                x_low_nominal_ohm=2*math.pi*F_LOW*l0,
                x_low_scenario_ohm=2*math.pi*F_LOW*scenario,
                matched_loss_scenario_db=matched_shunt_loss(1j*2*math.pi*F_LOW*scenario),
                estimated_pair_length_m=pair_length,
                estimated_winding_dcr_ohm=pair_length*1.14*0.1339,
                assumed_twist_wire_length_factor=1.14,
                hf_delay_only_loss_db=ruthroff_delay_loss(F_HIGH, pair_length, 0.65),
                hdc_200ma_oe=n*0.2/le/(1000/(4*math.pi)),
                hdc_300ma_oe=n*0.3/le/(1000/(4*math.pi)),
                ac_flux_500mw_sine_peak_t=math.sqrt(0.5*R_DRAIN)/(4.44*F_LOW*n*ae),
                ac_flux_5v_bipolar_square_peak_t=5/(4*F_LOW*n*ae),
                linear_bdc_200ma_t=l0*0.2/(n*ae))
    results['cores'].append(item)
    for f in FREQUENCIES:
        z = material_impedance(core, f)
        results['material_only_sweep'].append(dict(
            part=core['part'],material=core['material'], frequency_hz=f, r_ohm=z.real,
            x_ohm=z.imag, magnitude_ohm=abs(z),
            matched_shunt_loss_db=matched_shunt_loss(z)))
results['c64'] = [dict(capacitance_f=c, x_output_low_ohm=1/(2*math.pi*F_LOW*c),
                       x_referred_low_ohm=1/(8*math.pi*F_LOW*c))
                  for c in (100e-9, 500e-9)]
results['selected_output_capacitor'] = dict(references=['C64','C66','C67','C68','C69'], manufacturer='Walsin', mpn='1206N104J500CT', lcsc='C170182', each_capacitance_f=100e-9, capacitance_f=500e-9, voltage_v=50, dielectric='C0G', package='1206')
results['source_hashes'] = {
    p.name: hash_file(p) for p in [
        PROJECT / 'WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_sch',
        PROJECT / 'WsprryPico GPIO Shield with GPS - Torroid Edition.kicad_pcb',
        ROOT / 'inputs/fair-rite-43.csv', ROOT / 'inputs/fair-rite-77.csv']}
results['sources'] = [c['source'] for c in CORES] + [
    'https://fair-rite.com/43-material-data-sheet/',
    'https://fair-rite.com/77-material-data-sheet/',
    'https://www.fair-rite.com/wp-content/uploads/2020/11/43-Material-publish.csv',
    'https://www.fair-rite.com/wp-content/uploads/2015/04/77-Material-Fair-Rite.csv',
    'https://www.fair-rite.com/wp-content/uploads/2023/05/Fair-Rite_Catalog_17th_Edition.pdf',
    'https://qrp-labs.com/ultimate3/u3info/u3sbifilar.html',
    'https://www.qsl.net/kp4md/ruthroff.pdf',
    'https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf']

# Independent dimensional and limiting-case checks on the calculation code.
assert math.isclose(CORES[0]['al']*225, 285.75e-6)
assert math.isclose(results['cores'][0]['l_al_minimum_h'], 200.025e-6)
assert results['cores'][0]['l_al_minimum_h'] >= 240e-6*0.75
assert math.isclose(50/2**2, R_DRAIN)
assert math.isclose(ruthroff_delay_loss(1e-6, 0.4, 0.65), 0, abs_tol=1e-12)
quarter_wave = 299792458*0.65/(4*F_HIGH)
assert math.isclose(ruthroff_delay_loss(F_HIGH, quarter_wave, 0.65),
                    10*math.log10(1.25), rel_tol=1e-10)
assert results['cores'][0]['x_low_scenario_ohm'] > 6*R_DRAIN
(ROOT / 'calculations.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps({k: results[k] for k in ('cores', 'c64')}, indent=2))
