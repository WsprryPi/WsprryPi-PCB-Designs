"""Check locally exported Samsung precise |Z|/ESR CSVs, without vendor model redistribution.
Usage: python3 scripts/check_samsung_c4.py generated/samsung-c4-check docs
"""
import bisect, csv, hashlib, json, math, sys
from pathlib import Path
source, output = map(Path, sys.argv[1:]); output.mkdir(parents=True, exist_ok=True)
bands = [137e3,475e3,1.8e6,3.5e6,7e6,10e6,14e6,21e6,28e6,50e6,70e6,100e6,145e6]
freqs = sorted(set(bands + [137e3*(145e6/137e3)**(i/10000) for i in range(10001)]))
rows=[]; summary={}; hashes={}
for bias in (0,2.5,5):
    name=f'graph-{bias}V.csv'; raw=(source/name).read_bytes(); text=raw.decode('utf-8-sig').replace('\r\n','\n')
    assert f'DC bias value = {float(bias):.1f}Vdc' in text and '25.0degC' in text
    data=list(csv.reader(text.split('Frequency(MHz),|Z|(ohm),ESR(ohm)\n',1)[1].splitlines()))
    data=[[float(x) for x in r] for r in data if len(r)==3]
    fs=[r[0]*1e6 for r in data]; assert fs[0]<=freqs[0] and fs[-1]>=freqs[-1]
    def interp(f,col):
        k=bisect.bisect_right(fs,f); t=math.log(f/fs[k-1])/math.log(fs[k]/fs[k-1])
        return math.exp(math.log(data[k-1][col])*(1-t)+math.log(data[k][col])*t)
    subset=[]
    for f in freqs:
        z,r=interp(f,1),interp(f,2)
        # Separate log interpolation can produce tiny |Z|<R near resonance.
        # Clamp only this interpolation artifact; do not invent reactance sign.
        x2=max(0,z*z-r*r)
        row=dict(bias_V=bias,frequency_Hz=f,Z_magnitude_ohm=z,ESR_ohm=r,
                 added_loss_ideal_source_50ohm_dB=10*math.log10(((50+r)**2+x2)/2500),
                 added_loss_matched_50ohm_dB=10*math.log10(((100+r)**2+x2)/10000))
        subset.append(row)
    rows.extend(r for r in subset if r['frequency_Hz'] in bands)
    minimum=min(subset,key=lambda r:r['Z_magnitude_ohm'])
    summary[str(bias)]={'max_impedance_ohm':max(r['Z_magnitude_ohm'] for r in subset),
      'max_added_loss_ideal_source_50ohm_dB':max(r['added_loss_ideal_source_50ohm_dB'] for r in subset),
      'minimum_impedance_ohm':minimum['Z_magnitude_ohm'],'minimum_frequency_Hz':minimum['frequency_Hz'],
      'endpoint_rows':[subset[0],subset[-1]]}
    hashes[name]=hashlib.sha256(raw).hexdigest()
with (output/'c4-samsung-band-check.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n'); writer.writeheader(); writer.writerows(rows)
manifest={'part':'CL10A105KB8NNNC','electrical_family':'CL10A105KB8NNN',
 'source':'https://weblib.samsungsem.com/mlcc/mlcc-ec.do?partNumber=CL10A105KB8NNN',
 'method':'Samsung Component Library precise-model graph CSV export at 25 C, 0/2.5/5 V; log-log interpolation of magnitude and ESR; 10001-point full-band check plus band frequencies; no extrapolation. Capacitor-only loss into resistive load, no mounting parasitics.',
 'sha256':hashes,'summary':summary}
(output/'c4-samsung-source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(summary,indent=2))
