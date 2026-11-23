"""Compare single and dual THS3491RGT stages using identical matching filters."""
from pathlib import Path
import argparse,json,sys,hashlib,math,ast
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs',type=Path,required=True);a=ap.parse_args();sys.path.insert(0,str(a.research/'python-packages'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1];g=a.runs.resolve();rows=[json.loads(f.read_text()) for f in sorted(g.glob('f*.json'))];assert len(rows)==66,len(rows)
single=json.loads((p/'docs/ths3491-matching-results.json').read_text())
nom=lambda x:x['additional_loss_dB_each']==.5 and x['inductor_Q']==50 and x['step_divisor']==1000 and x['component_multipliers']==[1.]*7 and not x['hypothetical_output_offset_each_V']
sets={al:sorted([r for r in rows if nom(r) and r['divider_voltage_ratio']==al],key=lambda r:r['f_Hz']) for al in [.5,.55,.6]};ones={al:sorted([r for r in single['cases'] if nom(r) and r['divider_voltage_ratio']==al],key=lambda r:r['f_Hz']) for al in [.5,.55,.6]};assert all(len(v)==13 for v in [*sets.values(),*ones.values()])
for r in rows:
 assert r['chips']==2 and not r['input_shunt_first']
 assert max(map(abs,r['state_drift_V']))<5e-5 and abs(r['late_power_drift_percent'])<.1
 assert all(c['heat_W']>0 and c['plus_mA']>0 and c['minus_mA']>0 for c in r['chip'])
 ref=next(z for z in single['cases'] if z['f_Hz']==r['f_Hz'])
 assert r['matching_values_SI']==ref['matching_values_SI']
checks=[]
for r in rows:
 if r['step_divisor']!=2000:continue
 ref=next(z for z in sets[r['divider_voltage_ratio']] if z['f_Hz']==r['f_Hz'])
 checks.append({'case':r['case'],'power_change_percent':100*(r['fundamental_output_mW']/ref['fundamental_output_mW']-1),'heat_change_percent':100*(r['heat_total_W']/ref['heat_total_W']-1)})
current=max(max(abs(c['plus_mA']-c['plus_check_mA']),abs(c['minus_mA']-c['minus_check_mA'])) for r in rows for c in r['chip'])
# Check measured output power against an independent passive network calculation.
env={'np':np}
for filename,function in [('simulate_ths3491_dual_matching.py','matching_values'),('check_ths3491_dual_matching_network.py','network')]:
 tree=ast.parse((p/'scripts'/filename).read_text())
 if function=='network':env['values']=env['matching_values']
 exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function],type_ignores=[]),filename,'exec'),env)
transfer=[];balance=[]
for r in rows:
 cs=r['chip']
 if r['f_Hz'] in [137e3,145e6]:
  d=np.load(g/(r['case']+'.npz'));t=d['t'];total_rms2=float(np.trapezoid(d['current']**2,t)/(t[-1]-t[0]))
 else:total_rms2=(sum(c['rms_current_mA'] for c in cs)/1000)**2
 expected=sum(c['external_real_output_W'] for c in cs)-sum(r['branch_resistor_loss_W'])-.03*total_rms2
 balance.append({'case':r['case'],'difference_W':r['filter_real_input_W']-expected})
 if r['f_Hz'] not in [137e3,145e6] or r['additional_loss_dB_each']!=.5 or r['inductor_Q']!=50 or r['hypothetical_output_offset_each_V']:continue
 v=d['pa_out'];amp=2*abs(np.trapezoid(v*np.exp(-2j*np.pi*r['f_Hz']*t),t))/(t[-1]-t[0]);n=env['network'](r['f_Hz'],r['component_multipliers']);pred=amp*amp*n['load_W_per_Vpeak_squared'];transfer.append({'case':r['case'],'power_error_percent':100*(pred/(r['fundamental_output_mW']/1000)-1)})
assert max(abs(x['power_error_percent']) for x in transfer)<.01
assert max(abs(x['difference_W']) for x in balance)<5e-5
source={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['Logic RF Driver.kicad_sch','Logic RF Driver.kicad_pcb','Logic RF Driver.kicad_pro','Logic RF Driver.kicad_dru','BOM.csv']}
inputs={}
for f in [g/'models/THS3491RGT.lib',g/'models/THS3491RGT-current-sign.lib',p/'scripts/simulate_ths3491_dual_matching.py',p/'scripts/check_ths3491_dual_matching_network.py',Path(__file__),p/'docs/ths3491-matching-results.json',a.research/'simulate.py',*sorted((g/'runs').glob('f*.cir')),*sorted(g.glob('*_c4.mod'))]:
 key=str(f.relative_to(p)) if f.is_relative_to(p) else 'external-research/'+str(f.relative_to(a.research));inputs[key]=hashlib.sha256(f.read_bytes()).hexdigest()
record={'scope':'TI parallel load-sharing core with two RGT amplifiers, independent feedback and 2.49-ohm output resistors; identical 25-to-50-ohm inductor-first filters to the single-RGT comparison','cases':rows,'single_comparison':'ths3491-matching-results.json','network_corner_checks':json.loads((g/'network-check.json').read_text()),'independent_transfer_checks':transfer,'power_balance_checks':balance,'timestep_checks':checks,'rail_current_check_max_error_mA':current,'design_sha256':source,'model_and_script_sha256':inputs,'conditions':dict(single['conditions'],chips=2,output_resistor_each_ohms=2.49,effective_parallel_output_resistance_ohms=1.245,opposing_output_offset_each_V=.0225),'limitations':single['limitations']+['Nominal matched models do not establish real device gain or phase matching; opposing DC offsets are one explicit current-sharing sensitivity.','Mutual thermal coupling and the actual two-chip layout are not simulated; thermal calculations are sensitivities.','No output-power regulation or mismatch protection is implemented.']}
(p/'docs/ths3491-dual-matching-results.json').write_text(json.dumps(record,indent=2)+'\n')
fig,ax=plt.subplots(1,3,figsize=(14,4.2),layout='constrained')
for rs,label in [(ones[.55],'One chip'),(sets[.55],'Two chips')]:
 f=[r['f_Hz']/1e6 for r in rs];ax[0].semilogx(f,[r['fundamental_output_mW'] for r in rs],'-o',label=label);ax[1].semilogx(f,[max(c['heat_W'] for c in r['chip']) for r in rs],'-o',label=label);ax[2].semilogx(f,[r['plus_total_mA'] for r in rs],'-o',label=label)
ax[0].axhline(500,color='gray',linestyle='--',label='500 mW target');ax[0].set(ylabel='Fundamental into filtered 50 Ω (mW)',title='Same filters and 0.55 divider');ax[1].set(ylabel='Largest IC dissipation (W)',title='Heat per chip');ax[2].set(ylabel='Total +15 V rail current (mA)',title='−15 V rail is similar')
for z in ax:z.set_xlabel('Frequency (MHz)');z.grid(alpha=.25);z.legend(fontsize=8)
fig.savefig(p/'docs/ths3491-dual-matching.png',dpi=180);plt.close(fig)
nominal='\n'.join(f"| {al:g} | {min(r['fundamental_output_mW'] for r in ones[al]):.1f}–{max(r['fundamental_output_mW'] for r in ones[al]):.1f} | {min(r['fundamental_output_mW'] for r in sets[al]):.1f}–{max(r['fundamental_output_mW'] for r in sets[al]):.1f} | {max(c['pin_Vpp'] for r in sets[al] for c in r['chip']):.2f} | {max(c['heat_W'] for r in sets[al] for c in r['chip']):.2f} | {max(r['heat_total_W'] for r in sets[al]):.2f} |" for al in [.5,.55,.6])
full='\n'.join(f"| {r['f_Hz']/1e6:g} | {o['fundamental_output_mW']:.1f} / {r['fundamental_output_mW']:.1f} | {o['plus_total_mA']:.1f} / {r['plus_total_mA']:.1f} | {o['heat_total_W']:.2f} / {r['heat_total_W']:.2f} | {max(c['heat_W'] for c in r['chip']):.2f} | {max(c['peak_current_mA'] for c in r['chip']):.1f} |" for o,r in zip(ones[.5],sets[.5]))
variants=[]
for r in rows:
 if nom(r) or r['step_divisor']!=1000 or r['hypothetical_output_offset_each_V']:continue
 tags=[]
 if r['additional_loss_dB_each']!=.5:tags.append(f"{r['additional_loss_dB_each']:g} dB extra loss/filter")
 if r['inductor_Q']!=50:tags.append(f"Q = {r['inductor_Q']:g}")
 if r['component_multipliers']!=[1]*7:tags.append('±5% output L/C corner')
 o=next(z for z in single['cases'] if z['f_Hz']==r['f_Hz'] and z['divider_voltage_ratio']==r['divider_voltage_ratio'] and z['additional_loss_dB_each']==r['additional_loss_dB_each'] and z['inductor_Q']==r['inductor_Q'] and z['component_multipliers']==r['component_multipliers'] and z['step_divisor']==1000)
 variants.append(f"| {r['f_Hz']/1e6:g} | {r['divider_voltage_ratio']:g} | {', '.join(tags)} | {o['fundamental_output_mW']:.1f} / {r['fundamental_output_mW']:.1f} | {max(c['pin_Vpp'] for c in r['chip']):.2f} | {max(c['heat_W'] for c in r['chip']):.2f} |")
variant='\n'.join(variants)
offset='\n'.join(f"| {r['f_Hz']/1e6:g} | {r['fundamental_output_mW']:.1f} | {r['circulating_peak_mA']:.2f} | {max(c['heat_W'] for c in r['chip']):.2f} | {r['heat_total_W']:.2f} |" for r in rows if r['hypothetical_output_offset_each_V'])
heat=max(c['heat_W'] for r in sets[.55] for c in r['chip']);totalheat=max(r['heat_total_W'] for r in sets[.55]);dc=[r['dc_total_W'] for r in sets[.55]]
loss='\n'.join(f"| {r['f_Hz']/1e6:g} | {r['divider_voltage_ratio']:g} | {sum(c['external_real_output_W'] for c in r['chip'])*1000:.1f} | {sum(r['branch_resistor_loss_W'])*1000:.1f} | {r['output_filter_and_pad_loss_W']*1000:.1f} | {r['fundamental_output_mW']:.1f} |" for al in [.5,.55] for r in sets[al] if r['f_Hz'] in [137e3,145e6])
text=f'''# Dual THS3491 with 25-to-50-ohm matching filters

Two THS3491RGT amplifiers in TI's parallel load-sharing arrangement predict {min(r['fundamental_output_mW'] for r in sets[.5]):.1f}–{max(r['fundamental_output_mW'] for r in sets[.5]):.1f} mW at the filtered 50-ohm load across thirteen test frequencies from 137 kHz to 145 MHz with the 0.50 divider. The same divider and filters give approximately 500 mW with one chip. The pair reduces heat and output current per chip, while increasing total supply draw and total heat. It improves nominal 500 mW operating margin, but does not guarantee 500 mW under all tested loss and tolerance conditions.

![RF power, per-chip heat, and total rail current](docs/ths3491-dual-matching.png)

## Circuit and comparison

The circuit uses the parallel core in TI's [THS3491 datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf), Figure 10-2, and [TIDA-060002 guide](https://www.ti.com/lit/ug/tidue75/tidue75.pdf). Each RGT has its own 24.9-ohm input resistor, 576-ohm feedback resistor, 143-ohm gain resistor, and 2.49-ohm output resistor. Feedback is local to each chip. The resistors join at the shared output; the amplifier pins are not directly tied together. Both devices use ideal ±15 V supplies and enabled PD inputs.

```text
                                           THS3491RGT A → 2.49 Ω ─┐
Logic RF Driver → input LPF → divider ──────┤                      ├→ COUT → matching/output LPF → 50 Ω
                                           THS3491RGT B → 2.49 Ω ─┘
```

The Logic RF Driver source, Samsung C4, detector, LEDs, divider ratios, input LPF, output coupling capacitor, and all seven output-network component values are identical to the [single-chip matching study](THS3491-MATCHING-STUDY.md). Each test frequency has its own synthesized L-C-L-C-L-C-L network. Its ideal input impedance is 25 + j0 ohms at that fundamental with a grounded 50-ohm load. There is no 25-ohm shunt load and no output transformer. This is a separate candidate PA; it is absent from the project schematic, PCB, and BOM.

Nominal inductors have Q = 50, capacitor Q is 1000, capacitor ESL is 0.3 nH, and winding capacitance is limited as in the single-chip study. Each filter has an additional matched 0.5 dB loss pad. The pads add to component loss. Endpoint cases use 0 or 1 dB extra loss per filter, Q = 25 or 100, and the same ±5% output L/C corner vectors as the single-chip comparison. All filters are inductor-first. These are synthesized values and illustrative losses, not selected or measured filter parts.

The second output branch reduces effective isolation resistance from 2.49 to 1.245 ohms and shares load current. That explains the modest RF power increase with the same drive. Parallel operation does not double output voltage or remove TI's high-frequency voltage-swing limit. The extra input and feedback network also contribute load and dissipation.

## Nominal RF power

| Divider voltage ratio | Single-chip load power (mW) | Dual-chip load power (mW) | Largest dual pin swing (Vpp) | Largest dual heat per chip (W) | Largest total dual heat (W) |
| --- | ---: | ---: | ---: | ---: | ---: |
{nominal}

The following table compares identical 0.50 dividers. Single/dual columns refer to complete PA stages. The dual stage delivers somewhat more RF power, so this is a same-drive comparison, not an exactly equal-output-power comparison. Small downward drive adjustment sets a nominal 500 mW point; the table retains the actual simulated settings.

| Frequency (MHz) | Single / dual load power (mW) | Single / dual total +15 V current (mA) | Single / dual total IC heat (W) | Largest dual heat per chip (W) | Largest dual external peak current per chip (mA) |
| --- | ---: | ---: | ---: | ---: | ---: |
{full}

The negative-rail current is approximately the same magnitude as the positive-rail current. Individual chip currents, separate rail measurements, RMS output currents, source loading, and detector/LED draw are in the [result record](docs/ths3491-dual-matching-results.json). Current figures are estimates from the models; they do not qualify the Logic RF Driver or a particular clock source.

## External RF losses

RF leaving the amplifiers includes energy dissipated in the branch resistors, coupling capacitor, matching network, and output pad. The table separates these external losses from IC heat. COUT ESR adds approximately 1 mW or less at these nominal settings.

| Frequency (MHz) | Divider ratio | Total real external PA output (mW) | Both branch resistors (mW) | Output filter and pad (mW) | Fundamental load power (mW) |
| --- | ---: | ---: | ---: | ---: | ---: |
{loss}

## Loss and tolerance margin

The independent passive-network check evaluates all 128 sign combinations of ±5% output L/C tolerance at each endpoint. Its selected low-power, high-power, and high-current vectors are identical to those in the single-chip study. The complete transient cases replay those corners with the source and PA. This is an endpoint corner exercise, not a statistical yield prediction or a continuous sweep of a practical filter bank.

| Frequency (MHz) | Divider ratio | Sensitivity | Single / dual load power (mW) | Largest dual pin swing (Vpp) | Largest dual heat per chip (W) |
| --- | ---: | --- | ---: | ---: | ---: |
{variant}

The pair improves current sharing and cooling per chip. It does not restore voltage lost in the filters or compensate for source-amplitude variation. The combined low-power tolerance, Q = 25, and 1 dB-per-filter loss cases remain below 500 mW with the highest tested divider ratio. A guaranteed fixed-drive 500 mW output is therefore not established.

Band-specific adjustment or power regulation can address some variation, but the required drive and output swing must remain within TI's linear region at 145 MHz. Input-filter tolerances, actual component self-resonance and saturation, source/process/temperature spread, PCB stability, and mismatched loads remain unqualified. The model's low harmonics do not establish measured spectral purity.

## Offset and current sharing

The offset sensitivity uses additional opposing ±22.5 mV output-referred offsets, imposed at the two inputs through the closed-loop gain. This is the same stated offset scale as the load-sharing study. The nominal macro-model offsets remain present.

| Frequency (MHz) | Load power (mW) | Modeled opposing-current peak (mA) | Largest IC heat (W) | Total IC heat (W) |
| --- | ---: | ---: | ---: | ---: |
{offset}

The two nominal models share current closely because their signal paths are identical. The offset cases test one source of circulating current; they do not bound real AC gain or phase mismatch. The 2.49-ohm resistors provide finite isolation. A near-zero signed-average RF current is not proof of device lifetime.

## Supply and thermal requirements

At the 0.55 divider, PA-only DC power is {min(dc):.2f}–{max(dc):.2f} W, and total IC heat reaches {totalheat:.2f} W. The largest nominal per-chip dissipation is {heat:.2f} W. An assumed 85%-efficient converter draws approximately {min(dc)/4.25*1000:.0f}–{max(dc)/4.25*1000:.0f} mA from 5 V for the PA rails alone. Add the Logic RF Driver's 5 V and 3.3 V loads. Internal logic switching/crossover power and actual converter behavior remain outside the current model.

TI's RGT reference-board junction-to-ambient value of 49.6 °C/W gives approximately {25+49.6*heat:.0f} °C junction temperature at 25 °C ambient and {50+49.6*heat:.0f} °C at 50 °C ambient, ignoring heat from the other chip. An illustrative 10 °C/W mutual thermal coupling adds approximately {10*heat:.0f} °C, giving about {50+59.6*heat:.0f} °C at the higher ambient. These are separate thermal-resistance calculations, not simulated temperatures or a qualified two-chip layout.

TI lists 125 °C for continuous-operation, long-term junction reliability and 150 °C absolute maximum. The two-chip arrangement offers substantially better per-chip cooling margin than one device, but copper, exposed-pad soldering, thermal vias, chip spacing, and any heatsink must support the combined heat. Thermal coupling can consume that margin.

TI also lists ±100 mA continuous output current with an electromigration footnote, separately from its typical ±420 mA linear-drive capability. The interpretation for this RF waveform remains unresolved here. Splitting the load reduces peak and RMS current per chip, but the headline drive capability and a nominal model are not a lifetime guarantee. TI's output-voltage envelope still applies to each device.

## Validation and reproduction

The study contains 66 transient cases and 256 passive-network tolerance corners. Four cases halve the maximum timestep; RF power changes by at most {max(abs(c['power_change_percent']) for c in checks):.4g}%, and total IC heat by at most {max(abs(c['heat_change_percent']) for c in checks):.4g}%. Independent passive-network power transfer agrees within {max(abs(c['power_error_percent']) for c in transfer):.4g}%, and independent half-wave output-plus-feedback current accounting agrees with the rail measurements within {current:.4g} mA. The largest output-path power-balance discrepancy is {max(abs(c['difference_W']) for c in balance)*1e6:.2f} µW.

Each transient uses 60 periods, measures the final eight, and checks source capacitor-state drift below 50 µV and successive four-period power drift below 0.1%. The electrical models remain at 25 °C with ideal supplies. They do not include electrothermal feedback, extracted PCB parasitics, all device corners, or real filter parts. The documented negative-rail current-source sign correction and RGT package-model limitations are the same as in the single-chip study; signal-path model elements retain the vendor values.

Run `scripts/check_ths3491_dual_matching_network.py`, `scripts/simulate_ths3491_dual_matching.py`, and `scripts/report_ths3491_dual_matching.py` with the same `--research` and output arguments as the single-chip matching study. The runner requires `--board-runs` and uses the single-chip matching raw-run directory for `--single-runs` initial-state estimates. TI's unmodified RGT model is required under the output directory's `models/` folder. Generated decks, C4 fits, raw waveforms, and vendor models remain in ignored storage. Source and model hashes identify the retained inputs.

**The pair improves nominal 500 mW current and thermal margin; full-band reliability remains unqualified.** No KiCad source or BOM is changed, and no hardware performance is claimed.
'''
(p/'THS3491-DUAL-MATCHING-STUDY.md').write_text(text)
print(json.dumps({'cases':len(rows),'nominal':{str(al):{'output_mW':[min(r['fundamental_output_mW'] for r in rs),max(r['fundamental_output_mW'] for r in rs)],'total_plus_mA':[min(r['plus_total_mA'] for r in rs),max(r['plus_total_mA'] for r in rs)],'max_per_chip_heat_W':max(c['heat_W'] for r in rs for c in r['chip']),'max_total_heat_W':max(r['heat_total_W'] for r in rs)} for al,rs in sets.items()},'timestep_checks':checks,'rail_current_error_mA':current,'transfer_max_error_percent':max(abs(c['power_error_percent']) for c in transfer)},indent=2))
