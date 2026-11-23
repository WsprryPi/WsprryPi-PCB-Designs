"""Report the single-RGT impedance-transforming filter study and its limits."""
from pathlib import Path
import argparse,json,sys,hashlib,math,ast
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs',type=Path,required=True);a=ap.parse_args();sys.path.insert(0,str(a.research/'python-packages'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1];g=a.runs.resolve();rows=[json.loads(f.read_text()) for f in sorted(g.glob('f*.json'))];assert len(rows)==64,len(rows)
nom=lambda x:x['additional_loss_dB_each']==.5 and x['inductor_Q']==50 and x['step_divisor']==1000 and x['component_multipliers']==[1.]*7
sets={al:sorted([r for r in rows if nom(r) and r['divider_voltage_ratio']==al],key=lambda r:r['f_Hz']) for al in [.5,.55,.6]};assert all(len(v)==13 for v in sets.values())
network=json.loads((g/'network-check.json').read_text());checks=[]
for r in rows:
 assert max(map(abs,r['state_drift_V']))<5e-5
 assert abs(r['late_power_drift_percent'])<.1
 c=r['chip'][0]
 assert c['heat_W']>0 and c['plus_mA']>0 and c['minus_mA']>0
 expected=c['external_real_output_W']-r['branch_resistor_loss_W'][0]-.03*(c['rms_current_mA']/1000)**2
 # Coupling-capacitor state is not part of the initial-state solver; allow
 # residual storage flow, and expose its energy-balance discrepancy below.
 r['output_power_balance_difference_W']=r['filter_real_input_W']-expected
 if r['step_divisor']==2000:
  ref=next(z for z in sets[r['divider_voltage_ratio']] if z['f_Hz']==r['f_Hz'])
  checks.append({'case':r['case'],'power_change_percent':100*(r['fundamental_output_mW']/ref['fundamental_output_mW']-1),'heat_change_percent':100*(r['heat_total_W']/ref['heat_total_W']-1)})
current=max(max(abs(c['plus_mA']-c['plus_check_mA']),abs(c['minus_mA']-c['minus_check_mA'])) for r in rows for c in r['chip'])
design={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['Logic RF Driver.kicad_sch','Logic RF Driver.kicad_pcb','Logic RF Driver.kicad_pro','Logic RF Driver.kicad_dru','BOM.csv']}
inputs={}
for f in [g/'models/THS3491RGT.lib',g/'models/THS3491RGT-current-sign.lib',p/'scripts/simulate_ths3491_matching.py',p/'scripts/check_ths3491_matching_network.py',Path(__file__),p/'docs/ths3491-dual-results.json',a.research/'simulate.py']:
 key=str(f.relative_to(p)) if f.is_relative_to(p) else 'external-research/'+str(f.relative_to(a.research));inputs[key]=hashlib.sha256(f.read_bytes()).hexdigest()
for f in sorted((g/'runs').glob('f*.cir')):inputs[str(f.relative_to(p))]=hashlib.sha256(f.read_bytes()).hexdigest()
# Independent passive-network prediction driven by the measured PA fundamental.
env={'np':np}
for filename,function in [('simulate_ths3491_matching.py','matching_values'),('check_ths3491_matching_network.py','network')]:
 tree=ast.parse((p/'scripts'/filename).read_text())
 if function=='network':env['values']=env['matching_values']
 exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function],type_ignores=[]),filename,'exec'),env)
passive_checks=[]
for r in rows:
 if r['f_Hz'] not in [137e3,145e6] or r['additional_loss_dB_each']!=.5 or r['inductor_Q']!=50:continue
 d=np.load(g/(r['case']+'.npz'));t=d['t'];v=d['pa_out'];amp=2*abs(np.trapezoid(v*np.exp(-2j*np.pi*r['f_Hz']*t),t))/(t[-1]-t[0]);n=env['network'](r['f_Hz'],r['component_multipliers']);pred=amp*amp*n['load_W_per_Vpeak_squared']
 passive_checks.append({'case':r['case'],'power_error_percent':100*(pred/(r['fundamental_output_mW']/1000)-1)})
assert max(abs(x['power_error_percent']) for x in passive_checks)<.01
for f in sorted(g.glob('*_c4.mod')):inputs[str(f.relative_to(p))]=hashlib.sha256(f.read_bytes()).hexdigest()
record={'scope':'Single THS3491RGT with separately selected inductor-first input LPF and L-C plus fifth-order LPF output network, transforming 25 to 50 ohms at each test frequency','cases':rows,'network_corner_checks':network,'independent_transfer_checks':passive_checks,'timestep_checks':checks,'rail_current_check_max_error_mA':current,'output_power_balance_max_error_W':max(abs(r['output_power_balance_difference_W']) for r in rows),'design_sha256':design,'model_and_script_sha256':inputs,'conditions':{'supply_V':[15,-15],'electrical_model_temperature_C':25,'feedback_ohms':576,'gain_ohms':143,'input_deQ_ohms':24.9,'output_isolation_ohms':2.49,'input_divider_ratios':[.5,.55,.6],'nominal_inductor_Q_at_test_frequency':50,'Q_sensitivities':[25,100],'capacitor_Q_at_test_frequency':1000,'capacitor_ESL_H':.3e-9,'inductor_parallel_C_max_F':2e-12,'input_LPF_order':5,'input_LPF_cutoff_multiplier':1.5,'output_network_order':7,'output_network_topology':'L-C-L-C-L-C-L','output_50ohm_LPF_cutoff_multiplier':1.5,'additional_matched_loss_dB_per_filter':[0,.5,1],'output_capacitance_F':1e-6,'output_cap_ESR_ohms':.03,'output_cap_ESL_H':.5e-9,'output_component_tolerance_fraction':.05,'network_tolerance_corners_per_endpoint':128,'RGT_reference_RthetaJA_C_per_W':49.6,'long_term_junction_limit_C':125,'simulator':'ngspice 45.2, native XSPICE code models, PSpice compatibility'},'limitations':['Nominal electrical model, not a measured board or device/process/temperature corner.','Each spot frequency has a separately synthesized filter; this is not a single fixed broadband matching network or a verified practical relay/filter bank.','The all-sign tolerance check covers output L/C values at the operating fundamental only; selected extreme corners are replayed as complete transients. Input-filter tolerances, SRF spread, inductor saturation and PCB parasitics are not qualified.','TI linear-swing envelope and cooling must apply to the actual assembly. No electrothermal feedback or supply converter model.','The datasheet lists +/-100 mA continuous output current for electromigration; application of that rating to bipolar RF waveforms is not resolved here and the +/-420 mA linear-drive figure is not a lifetime guarantee.','The RGT macro-model FB-to-OUT path is 1 microohm; real package trace resistance and inductance are incompletely modeled.','Logic-stage rail estimates omit internal switching/crossover power; selected detector semiconductor models are illustrative.']}
(p/'docs/ths3491-matching-results.json').write_text(json.dumps(record,indent=2)+'\n')
fig,ax=plt.subplots(1,3,figsize=(14,4.2),layout='constrained')
for al,label in [(.5,'0.50 divider'),(.55,'0.55 divider'),(.6,'0.60 divider')]:
 r=sets[al];f=[z['f_Hz']/1e6 for z in r];ax[0].semilogx(f,[z['fundamental_output_mW'] for z in r],'-o',label=label);ax[1].semilogx(f,[z['heat_total_W'] for z in r],'-o',label=label);ax[2].semilogx(f,[z['plus_total_mA'] for z in r],'-o',label=label)
ax[0].axhline(500,color='gray',linestyle='--',label='500 mW target');ax[0].set(ylabel='Fundamental into filtered 50 Ω (mW)',title='25-to-50 Ω matching network');ax[1].set(ylabel='Single IC dissipation (W)',title='Heat at ±15 V');ax[2].set(ylabel='+15 V rail current (mA)',title='−15 V rail is similar')
for z in ax:z.set_xlabel('Frequency (MHz)');z.grid(alpha=.25);z.legend(fontsize=8)
fig.savefig(p/'docs/ths3491-matching.png',dpi=180);plt.close(fig)
full='\n'.join(f"| {r['f_Hz']/1e6:g} | {r['fundamental_output_mW']:.1f} | {r['chip'][0]['pin_Vpp']:.2f} | {r['chip'][0]['peak_current_mA']:.1f} | {r['plus_total_mA']:.1f} / {r['minus_total_mA']:.1f} | {r['heat_total_W']:.2f} |" for r in sets[.55])
nominal='\n'.join(f"| {al:g} | {min(r['fundamental_output_mW'] for r in rs):.1f}–{max(r['fundamental_output_mW'] for r in rs):.1f} | {max(r['chip'][0]['pin_Vpp'] for r in rs):.2f} | {max(r['heat_total_W'] for r in rs):.2f} |" for al,rs in sets.items())
variant=[]
for r in rows:
 if r['f_Hz'] not in [137e3,145e6] or r['step_divisor']!=1000:continue
 if nom(r):continue
 tags=[]
 if r['additional_loss_dB_each']!=.5:tags.append(f"{r['additional_loss_dB_each']:g} dB extra loss/filter")
 if r['inductor_Q']!=50:tags.append(f"Q = {r['inductor_Q']:g}")
 if r['component_multipliers']!=[1]*7:tags.append('±5% output L/C corner')
 variant.append(f"| {r['f_Hz']/1e6:g} | {r['divider_voltage_ratio']:g} | {', '.join(tags)} | {r['fundamental_output_mW']:.1f} | {r['chip'][0]['pin_Vpp']:.2f} | {r['chip'][0]['peak_current_mA']:.1f} | {r['heat_total_W']:.2f} |")
variants='\n'.join(variant)
vals='\n'.join(f"| {x['f_Hz']/1e6:g} | "+' | '.join(f'{v*scale:.3f}' for v,scale in zip(x['matching_values_SI'],[1e6,1e9,1e6,1e9,1e6,1e9,1e6]))+' |' for x in network)
heat=max(r['heat_total_W'] for r in sets[.55]);theta=(125-50)/heat
loss_table='\n'.join(f"| {r['f_Hz']/1e6:g} | {r['divider_voltage_ratio']:g} | {r['chip'][0]['external_real_output_W']*1000:.1f} | {r['branch_resistor_loss_W'][0]*1000:.1f} | {r['output_filter_and_pad_loss_W']*1000:.1f} | {r['fundamental_output_mW']:.1f} | {10*math.log10(r['filter_real_input_W']/(r['total_load_mW']/1000)):.2f} |" for al in [.5,.55] for r in sets[al] if r['f_Hz'] in [137e3,145e6])
text=f'''# THS3491 with 25-to-50-ohm matching filters

A single THS3491RGT with an inductor-first matching/output filter predicts approximately 500 mW at the 50-ohm load at the thirteen tested frequencies from 137 kHz to 145 MHz. The 0.50 divider predicts {min(r['fundamental_output_mW'] for r in sets[.5]):.1f}–{max(r['fundamental_output_mW'] for r in sets[.5]):.1f} mW. A 0.55 divider provides nominal adjustment headroom at {min(r['fundamental_output_mW'] for r in sets[.55]):.1f}–{max(r['fundamental_output_mW'] for r in sets[.55]):.1f} mW, with about {heat:.2f} W of IC heat. Filter matching makes 500 mW electrically plausible; these results do not establish a reliable continuous-duty, full-band amplifier.

![RF power, heat, and rail current](docs/ths3491-matching.png)

## Circuit and filter definition

The source is the Logic RF Driver circuit in the [single-chip study](THS3491-STUDY.md), including Samsung C4, the RF_RAW detector, and both LEDs. The PA uses TI's RGT macro-model, ±15 V ideal rails, gain-setting resistors of 576 and 143 ohms, a 24.9-ohm noninverting-input resistor, and a 2.49-ohm output isolation resistor. Feedback remains local to the amplifier, upstream of the isolation resistor. This candidate PA is absent from the KiCad schematic, PCB, and BOM.

```text
Logic RF Driver → input LPF → divider → THS3491RGT → 2.49 Ω → COUT → L-C-L-C-L-C-L → 50 Ω
```

The input is a fifth-order, 50-ohm, inductor-first Butterworth LPF with cutoff at 1.5 times the operating frequency. The output comprises an inductor-first L/C matching section and a fifth-order 50-ohm LPF with that same cutoff ratio. Its seven reactive elements are L-C-L-C-L-C-L. The matching section is synthesized against the complex input impedance of the complete lossless LPF, so the output network presents exactly 25 + j0 ohms at the selected fundamental with an ideal 50-ohm load. It contains no 25-ohm shunt termination and no output transformer.

Each test frequency uses a separate set of component values. This is a band-selected family of networks, not one fixed filter covering the entire frequency span. The matching applies at the operating frequency; the complete seven-element response is not a seventh-order Butterworth response. Its passband, harmonic rejection, and response across each actual operating band require evaluation with selected parts.

The table gives representative unrounded synthesis values in signal-path order. L values are in µH and C values in nF; these are calculation values, not an orderable parts list.

| Frequency (MHz) | L1 (µH) | C2 (nF) | L3 (µH) | C4 (nF) | L5 (µH) | C6 (nF) | L7 (µH) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{vals}

Inductor Q is 50 at the test frequency; winding capacitance is limited to 2 pF or a value corresponding to a self-resonance at 7.5 times the operating frequency. Capacitor Q is 1000, with 0.3 nH series inductance. Each filter also has a matched 0.5 dB loss pad, representing additional unmodeled loss. The output pad is on the 50-ohm side. The extra pads add to component loss; 0.5 dB is not the total output-filter loss. COUT is 1 µF with 0.03-ohm ESR and 0.5 nH ESL. Filter capacitors have no intended DC bias; the source Samsung C4 retains its DC-biased fit.

## Nominal power and drive

The divider presents a nominal 50-ohm input. For voltage ratio a, its input shunt is 50/(1−a) ohms, series resistor is 50(1/a−1) ohms, and output shunt is 50 ohms. The 0.55 ratio uses approximately 111.11, 40.91, and 50 ohms, respectively. It is a drive setting, not closed-loop output-power regulation.

| Divider voltage ratio | Filtered load power over thirteen frequencies (mW) | Largest pin swing (Vpp) | Largest IC heat (W) |
| --- | ---: | ---: | ---: |
{nominal}

The following table uses the 0.55 divider. Power is the fundamental delivered to the external 50-ohm load. Rail currents refer to the PA alone. The current peak is the external output current; the amplifier also supplies its feedback network.

| Frequency (MHz) | Load power (mW) | Amplifier pin swing (Vpp) | Output peak current (mA) | +15 V / −15 V current (mA) | IC heat (W) |
| --- | ---: | ---: | ---: | ---: | ---: |
{full}

The gain-of-five source chain has adequate nominal drive for the approximately 500 mW operating point. It uses the source's modeled voltage into its actual input filter and divider, rather than assuming that 80 mW is available unchanged at the PA input. These calculations do not establish source compatibility or power for every Pico, Pi, or Si5351 configuration.

## Loss and tolerance sensitivity

This nominal loss breakdown separates RF leaving the amplifier from resistor and filter dissipation. COUT adds less than 1 mW of ESR loss at these operating points. The filter-loss column includes finite-Q component loss and the extra output pad. IC heat is separate from all these external losses.

| Frequency (MHz) | Divider ratio | Real external PA output (mW) | 2.49 Ω loss (mW) | Output filter and pad loss (mW) | Fundamental load power (mW) | Output filter/pad loss (dB) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{loss_table}

Endpoint loss cases use 0 or 1 dB extra matched loss per filter. Q cases use 25 or 100 in both filters. The independent complex-impedance check evaluates all 128 sign combinations of ±5% output-network L/C tolerances at each endpoint, with the nominal finite-Q and parasitic assumptions. It verifies the ideal 25 + j0-ohm match and selects low-power, high-power, and high-current corners for complete source-plus-PA transient replay. This is a deterministic corner exercise, not a statistical production-yield prediction.

The output-network input resistance spans approximately 20–32 ohms in these corner checks. A fixed divider has limited output-power margin. Combined stresses use the low-power tolerance corner, Q = 25, and 1 dB extra loss in each filter. Input-filter tolerances, component self-resonance variation, and winding saturation are outside this exercise.

| Frequency (MHz) | Divider ratio | Sensitivity | Load power (mW) | Pin swing (Vpp) | Peak output current (mA) | IC heat (W) |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
{variants}

A nominal 500 mW result does not establish a guaranteed minimum. Band-by-band drive adjustment or power regulation, measured filter loss, and component selection determine the usable margin. Increasing drive to cover every loss corner also raises pin swing and dissipation; the 145 MHz setting must remain inside TI's permitted linear region.

## Current, heat, and reliability

TI's [datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf), Section 9.4.4 and Figure 9-4, restricts output swing at frequencies above 100 MHz. The approximately 12 Vpp nominal 500 mW operating point is below the roughly 14–15 Vpp envelope at 145 MHz. This is a useful voltage margin, not a guarantee of stability, distortion, or lifetime into a reactive filter. The higher 0.60-divider case approaches that envelope.

The datasheet also lists ±100 mA continuous output current with an electromigration footnote, separately from its ±420 mA typical linear-drive capability. TI's [load-sharing guide](https://www.ti.com/lit/ug/tidue75/tidue75.pdf) analyzes substantial sinusoidal currents, but the evidence here does not establish how the ±100 mA limit applies to this bipolar RF waveform. Peak, RMS, rectified, and signed-average currents are different quantities. The model's near-zero signed-average output current is not a lifetime qualification, and the 420 mA figure does not resolve this rating question.

At the 0.55 divider, PA-only power input is {min(r['dc_total_W'] for r in sets[.55]):.2f}–{max(r['dc_total_W'] for r in sets[.55]):.2f} W. An assumed 85%-efficient converter draws {min(r['dc_total_W'] for r in sets[.55])/4.25*1000:.0f}–{max(r['dc_total_W'] for r in sets[.55])/4.25*1000:.0f} mA from 5 V for the PA rails. The Logic RF Driver adds its own 5 V pull-up draw and 3.3 V load; those currents are included separately in the result record. Logic internal switching and crossover power, supply impedance, and converter losses beyond that illustrative efficiency are not simulated.

IC heat is rail power minus real external-output and feedback power. Isolation-resistor and filter losses are external to the chip. TI's 49.6 °C/W RGT reference-board value gives approximately {25+49.6*heat:.0f} °C junction temperature at 25 °C ambient and {50+49.6*heat:.0f} °C at 50 °C ambient for the largest nominal 0.55-divider dissipation. These are thermal-resistance estimates, not an electrothermal simulation. TI specifies 125 °C for continuous-operation, long-term reliability and 150 °C absolute maximum. The reference-board thermal resistance provides little or no useful margin here.

Keeping the junction below 125 °C at 50 °C ambient requires an effective junction-to-ambient resistance below approximately {theta:.1f} °C/W at this drive setting, with additional margin for actual dissipation and manufacturing variation. An illustrative 30 °C/W path gives approximately {50+30*heat:.0f} °C at that ambient. A soldered exposed pad, suitable copper and thermal vias, and possibly a heatsink require a dedicated PA layout; the existing Logic RF Driver board supplies no such validation.

The result is **nominal electrical feasibility, with reliability unqualified**. Real filter parts and band coverage, current-rating interpretation, hot operation, source variation, stability with the intended filters and cable/load mismatch, and measured harmonic output remain material constraints.

## Numerical checks and reproduction

The [result record](docs/ths3491-matching-results.json) contains 64 transient cases, 256 passive-network tolerance corners, source/model hashes, and the synthesis values. Four endpoint cases halve the maximum timestep; fundamental output power changes by at most {max(abs(x['power_change_percent']) for x in checks):.4g}%, and IC heat changes by at most {max(abs(x['heat_change_percent']) for x in checks):.4g}%. Each transient uses 60 periods and measures the final eight. The C4/C5/C6 state drift stays below 50 µV, and successive four-period power windows agree within 0.1%.

Independent complex-network calculations agree with the endpoint transient fundamental-power transfer within {max(abs(x['power_error_percent']) for x in passive_checks):.4g}% across {len(passive_checks)} comparisons.

The RGT model and its documented negative-rail current-source sign correction are the same as in the [dual study](THS3491-DUAL-STUDY.md). Independent half-wave output-plus-feedback current accounting agrees with rail measurements within {current:.4g} mA. Signal-path elements retain the vendor values. The model joins FB to OUT through 1 µohm and omits actual package trace resistance. The electrical model remains at 25 °C; its apparently low harmonic levels do not establish actual RF purity.

Run `scripts/check_ths3491_matching_network.py`, `scripts/simulate_ths3491_matching.py`, and `scripts/report_ths3491_matching.py`. All accept `--research` and an output location (`--output` for the checker/runner, `--runs` for the reporter). The runner also requires `--board-runs` and `--single-runs` as in the other THS3491 studies. The output directory needs TI's unmodified `THS3491RGT.lib` under `models/`; it retains the corrected current-accounting copy, C4 fits, generated decks, and per-case results in ignored storage. The source decks, external research helper, and ngspice/XSPICE setup are the retained dependencies described in the single-chip study. Vendor model text is not included in the published result record.

No KiCad design file or BOM is changed by this study. Numerical convergence is not RF, thermal, or manufacturing qualification.
'''
(p/'THS3491-MATCHING-STUDY.md').write_text(text)
print(json.dumps({'cases':len(rows),'nominal':{str(al):{'power_mW':[min(r['fundamental_output_mW'] for r in rs),max(r['fundamental_output_mW'] for r in rs)],'heat_W':[min(r['heat_total_W'] for r in rs),max(r['heat_total_W'] for r in rs)]} for al,rs in sets.items()},'timestep_checks':checks,'current_error_mA':current,'power_balance_error_W':record['output_power_balance_max_error_W']},indent=2))
