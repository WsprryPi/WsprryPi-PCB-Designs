"""Report TI THS3491RGT load sharing in the Logic RF Driver filter chain."""
from pathlib import Path
import argparse,json,sys,hashlib,math
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs',type=Path,required=True);a=ap.parse_args();sys.path.insert(0,str(a.research/'python-packages'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1];g=a.runs.resolve();rows=json.loads((g/'results.json').read_text());plan=json.loads((g/'plan.json').read_text());assert len(rows)==len(plan)==58
nom=lambda x:x['branch_ohms']==2.49 and not x['common_ohms'] and not x['shunt_ohms'] and x['additional_loss_dB_each']==.5 and x['step_divisor']==1000 and not x['hypothetical_output_offset_each_V']
one=sorted([x for x in rows if nom(x) and x['chips']==1 and x['divider_voltage_ratio']==.6],key=lambda x:x['f_Hz']);two=sorted([x for x in rows if nom(x) and x['chips']==2 and x['divider_voltage_ratio']==.6],key=lambda x:x['f_Hz']);half=sorted([x for x in rows if nom(x) and x['chips']==2 and x['divider_voltage_ratio']==.5],key=lambda x:x['f_Hz']);assert len(one)==len(two)==len(half)==13
checks=[]
for x in rows:
 if x['step_divisor']!=2000:continue
 ref=next(z for z in rows if nom(z) and z['chips']==x['chips'] and z['f_Hz']==x['f_Hz'] and z['divider_voltage_ratio']==x['divider_voltage_ratio'])
 checks.append({'case':x['case'],'power_change_percent':100*(x['fundamental_output_mW']/ref['fundamental_output_mW']-1),'heat_change_percent':100*(x['heat_total_W']/ref['heat_total_W']-1),'peak_current_change_percent':100*(max(y['peak_current_mA'] for y in x['chip'])/max(y['peak_current_mA'] for y in ref['chip'])-1)})
current_check=max(max(abs(c['plus_mA']-c['plus_check_mA']),abs(c['minus_mA']-c['minus_check_mA'])) for x in rows for c in x['chip'])
source={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['Logic RF Driver.kicad_sch','Logic RF Driver.kicad_pcb','Logic RF Driver.kicad_pro','Logic RF Driver.kicad_dru','BOM.csv']}
inputs={}
for f in [g/'models/ti-rgt.zip',g/'models/THS3491RGT.lib',g/'models/THS3491RGT-current-sign.lib',g/'models/tidue75.pdf',g/'models/tidrxg3.pdf',p/'scripts/simulate_ths3491_dual.py',Path(__file__),p/'docs/ths3491-results.json',a.research/'simulate.py']:
 key=str(f.relative_to(p)) if f.is_relative_to(p) else 'external-research/'+str(f.relative_to(a.research));inputs[key]=hashlib.sha256(f.read_bytes()).hexdigest()
for f in sorted((g/'runs').glob('f*.cir')):inputs[str(f.relative_to(p))]=hashlib.sha256(f.read_bytes()).hexdigest()
record={'scope':'TI THS3491RGT parallel load-sharing core adapted to the Logic RF Driver with inductor-first input and output filters; not an exact reproduction of the entire TIDA-060002 board','cases':rows,'timestep_checks':checks,'rail_current_independent_check_max_difference_mA':current_check,'design_sha256':source,'model_and_script_sha256':inputs,'conditions':{'simulator':'ngspice 45.2 shared library, PSpice compatibility, native XSPICE models','supply_V':[15,-15],'model_temperature_C':25,'feedback_ohms_each':576,'gain_ohms_each':143,'input_deQ_ohms_each':24.9,'nominal_output_branch_ohms':2.49,'input_divider_ratios':[.5,.6,.75],'output_load_ohms':50,'filter_type':'Inductor-first fifth-order Butterworth on input and output, separately scaled for each test frequency','filter_cutoff_multiplier':1.5,'inductor_Q_at_test_f':50,'capacitor_Q_at_test_f':1000,'capacitor_ESL_H':.3e-9,'inductor_parallel_C_limit_F':2e-12,'additional_loss_dB_each':[0,.5,1],'output_capacitance_F':1e-6,'output_cap_ESR_ohms':.03,'output_cap_ESL_H':.5e-9,'RGT_reference_JEDEC_RthetaJA_C_per_W':49.6,'hypothetical_output_offset_each_V':.0225,'periods':60,'measurement_periods':8,'periodic_state_drift_limit_V':5e-5,'late_power_drift_limit_percent':.1},'limitations':['TI has demonstrated the load-sharing topology; these results are simulations of its adaptation to a different source, filter network, and load.','Identical nominal RGT macro-models do not establish actual AC phase/gain/current matching; offset sensitivity is one explicit stress, not a complete process corner.','Supply-current sign correction is explicit; nominal 25 C model is not an electrothermal or extracted-PCB model.','TI maximum linear output envelope applies to each chip; more output current does not double the permitted voltage swing.','The RGT model joins FB to OUT through 1 microohm and is not a complete package-parasitic extraction.','Filter and source limitations from the single-chip study apply; no capacitor-first filters are used in this study.']}
(p/'docs/ths3491-dual-results.json').write_text(json.dumps(record,indent=2)+'\n')
fig,ax=plt.subplots(1,3,figsize=(14,4.2),layout='constrained')
for values,label in [(one,'One RGT'),(two,'Two RGT, load sharing')]:
 f=[x['f_Hz']/1e6 for x in values];ax[0].semilogx(f,[x['fundamental_output_mW'] for x in values],'-o',label=label);ax[1].semilogx(f,[max(c['heat_W'] for c in x['chip']) for x in values],'-o',label=label);ax[2].semilogx(f,[x['plus_total_mA'] for x in values],'-o',label=label)
ax[0].axhline(500,color='gray',linestyle='--',label='500 mW target');ax[0].set(ylabel='Fundamental at filtered 50 Ω load (mW)',title='Same input drive and filters');ax[1].set(ylabel='Largest IC dissipation (W)',title='Heat per chip');ax[2].set(ylabel='Total +15 V rail draw (mA)',title='DC draw; −15 V is similar')
for z in ax:z.set_xlabel('Frequency (MHz)');z.grid(alpha=.25);z.legend(fontsize=8)
fig.savefig(p/'docs/ths3491-dual.png',dpi=180);plt.close(fig)
full='\n'.join(f"| {x['f_Hz']/1e6:g} | {x['fundamental_output_mW']:.1f} | {y['fundamental_output_mW']:.1f} | {max(c['pin_Vpp'] for c in y['chip']):.2f} | {y['plus_total_mA']:.1f} / {y['minus_total_mA']:.1f} | {max(c['heat_W'] for c in y['chip']):.2f} | {y['heat_total_W']:.2f} |" for x,y in zip(one,two))
variant=[]
for x in rows:
 if x['chips']!=2 or x['f_Hz'] not in [137e3,145e6] or x['step_divisor']!=1000 or x['hypothetical_output_offset_each_V']:continue
 if x['divider_voltage_ratio']==.5:continue
 name='2.49 Ω branches' if x['branch_ohms']==2.49 else f"{x['branch_ohms']:g} Ω branches"
 if x['common_ohms']==30:name='Datasheet AWG output network'
 if x['shunt_ohms']==50:name='TIDA Table 3, total RLOAD = 50 Ω'
 variant.append((x,name))
variants='\n'.join(f"| {x['f_Hz']/1e6:g} | {name} | {x['divider_voltage_ratio']:g} | {x['additional_loss_dB_each']:g} | {x['fundamental_output_mW']:.1f} | {max(c['pin_Vpp'] for c in x['chip']):.2f} | {x['heat_total_W']:.2f} |" for x,name in sorted(variant,key=lambda a:(a[0]['f_Hz'],a[1],a[0]['divider_voltage_ratio'],a[0]['additional_loss_dB_each'])))
offsets=[x for x in rows if x['hypothetical_output_offset_each_V']]
offset_table='\n'.join(f"| {x['f_Hz']/1e6:g} | {x['fundamental_output_mW']:.1f} | {x['circulating_peak_mA']:.2f} | {x['chip'][0]['mean_current_mA']:.2f} / {x['chip'][1]['mean_current_mA']:.2f} | {x['heat_total_W']:.2f} |" for x in sorted(offsets,key=lambda x:x['f_Hz']))
maxheat=max(max(c['heat_W'] for c in x['chip']) for x in two);totalheat=max(x['heat_total_W'] for x in two)
thermal='\n'.join(f"| {theta:g} | {25+theta*maxheat:.0f} | {50+theta*maxheat:.0f} |" for theta in [40,49.6,60,80,100])
strong=[x for x in rows if x['chips']==2 and nom(x) and x['divider_voltage_ratio']==.75];strong145=next(x for x in strong if x['f_Hz']==145e6)
text=f'''# Dual THS3491 load-sharing study

Two THS3491RGT devices in TI's parallel load-sharing arrangement predict {min(x['fundamental_output_mW'] for x in two):.0f}–{max(x['fundamental_output_mW'] for x in two):.0f} mW at the filtered 50-ohm load across 137 kHz–145 MHz with the 0.6 input divider. The matched single-RGT control predicts {min(x['fundamental_output_mW'] for x in one):.0f}–{max(x['fundamental_output_mW'] for x in one):.0f} mW. The pair shares output current and reduces dissipation per chip; it does not double RF output with this voltage gain, input drive, and load.

![Single and dual RGT output power, chip heat, and supply draw](docs/ths3491-dual.png)

## TI circuit and scope

TI's [TIDA-060002 reference design](https://www.ti.com/tool/TIDA-060002) demonstrates two or more THS3491RGT amplifiers sharing a low-resistance or capacitive load. Its [design guide](https://www.ti.com/lit/ug/tidue75/tidue75.pdf) provides the dual circuit in Figure 20 and output resistor values in Table 3. The THS3491 [datasheet](https://www.ti.com/lit/ds/symlink/ths3491.pdf) also shows two gain-of-five channels with 24.9-ohm input resistors and separate 2.49-ohm output resistors in Figure 10-2.

The nominal model uses that parallel core: both noninverting inputs receive the same signal through individual 24.9-ohm resistors. Each RGT device has its own feedback resistor of 576 ohms from FB to the inverting input, and 143 ohms from that input to ground. Each output feeds a 2.49-ohm resistor; the two resistors join at the shared output. Feedback is local to each amplifier, upstream of its output resistor. Both chips use ideal ±15 V supplies and enabled PD inputs. The single-RGT control has the same gain, input resistor, and 2.49-ohm output resistor.

```text
                                      THS3491RGT A ── 2.49 Ω ──┐
Logic RF Driver ── input LPF ── divider ──┤                     ├── COUT ── output LPF ── 50 Ω
                                      THS3491RGT B ── 2.49 Ω ──┘
```

This is TI's load-sharing core adapted to the Logic RF Driver and its band-selected filters. It is not an exact model of the complete TIDA board. The modeled input uses the representative band-selected filters described here; TI's board uses a fixed 150-MHz Bessel filter. The output network variants use TI's published resistor values with this same filter chain, not TI's full measurement fixture. No amplifier outputs are directly shorted together, and no capacitor-first filters are used.

## Source, filters, and models

The source is the detector-loaded Logic RF Driver circuit from the [single-chip study](THS3491-STUDY.md), including Samsung C4 and both LEDs. Input and output filters are fifth-order inductor-first Butterworth ladders designed for 50-ohm terminations. Each test frequency uses its own scaled component values, with cutoff at 1.5 times that frequency. The nominal inductor Q is 50, capacitor Q is 1000, capacitor ESL is 0.3 nH, and winding capacitance is limited to 2 pF as in the single-chip study. An extra matched loss network adds 0.5 dB at each filter; endpoint cases use 0 or 1 dB. These are representative networks, not selected or measured filter parts.

The divider presents a nominal 50-ohm input. The 0.6 ratio uses 125 ohms to ground at its input, 33.333 ohms in series, and 50 ohms to ground at the amplifier-input node. The 0.5 ratio uses 100, 50, and 50 ohms. A 0.75 ratio is a higher-drive sensitivity with the corresponding matched divider values. The output coupling capacitor is 1 µF with illustrative 0.03-ohm ESR and 0.5 nH ESL.

The simulation uses TI's [RGT model](https://www.ti.com/lit/zip/SBOMAN4), with its separate FB and OUT pins connected as specified. It joins these pins internally through 1 microohm; it is not a complete model of package trace resistance. The model's negative-rail load-current source has the same sign issue described in the single-chip study. Only that source's sign is corrected. Independent half-wave output-current accounting agrees with the corrected rail currents within {current_check:.5g} mA. Signal-path elements remain unchanged.

## Full-band comparison

Both configurations use the 0.6 divider, nominal filters, and the same RGT model. Rail currents are the total for the entire PA, not per chip. The RGT control separates load sharing from the package and feedback-value differences relative to the DDA circuit.

| Frequency (MHz) | One RGT load power (mW) | Two RGT load power (mW) | Largest dual pin swing (Vpp) | Dual +15 V / −15 V draw (mA) | Largest dual IC heat (W) | Total dual IC heat (W) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{full}

With the 0.5 divider, the dual circuit predicts {min(x['fundamental_output_mW'] for x in half):.0f}–{max(x['fundamental_output_mW'] for x in half):.0f} mW. With identical nominal chips, each carries approximately half the external output current. This equal split is a model result, not a bound on actual device matching.

## Output networks, loss, and higher drive

The datasheet AWG output network uses 40.2 ohms per branch and 30 ohms between the join and the output. TIDA Table 3's total-RLOAD = 50-ohm row uses 40-ohm branch resistors, 5 ohms after the join, and a 50-ohm shunt load in addition to the external load. These networks trade output voltage for load isolation, matching, or a defined test load. TI's reference-guide 20-Vpp test level is referred to the amplifier outputs; it is not automatically the voltage at the external 50-ohm instrument. The datasheet front-page example labels 13 Vpp maximum at its matched 50-ohm load. A sinusoidal 13 Vpp there corresponds to 423 mW, excluding external filter loss; that label does not establish the same swing at 145 MHz. They are included without removing their resistor losses. Branch values of 1 and 10 ohms are explicit RF sensitivity cases, not declarations that TI qualifies those values for every filter and layout.

| Frequency (MHz) | Output network | Divider ratio | Extra loss per filter (dB) | Load power (mW) | Largest chip pin swing (Vpp) | Total IC heat (W) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
{variants}

The 145 MHz, 0.75-divider case predicts {strong145['fundamental_output_mW']:.1f} mW at the load, but requires {max(c['pin_Vpp'] for c in strong145['chip']):.2f} Vpp at each chip. TI's maximum recommended linear-output graph permits approximately 14–15 Vpp there on ±15 V supplies. A nominal model producing more RF power above that envelope does not establish acceptable linear operation.

The pair increases available output current. Both chips still produce essentially the same output voltage, so sharing does not multiply the permitted voltage swing or eliminate internal large-signal limitations. TI's demonstrated heavy-load results establish a useful topology; they do not establish this source/filter chain at 500 mW through 145 MHz. Different impedance matching or another PA arrangement can change that conclusion.

## Offset and current sharing

TI's design guide calculates a worst-case output-referred DC offset of ±22.5 mV for its stated gain, source resistance, input offset, and input-bias assumptions. The endpoint sensitivities impose equal and opposite additional input offsets scaled to that output level. The nominal model's own offset remains present. These cases are an explicit offset stress, not a full process or temperature corner and not a model of AC gain/phase mismatch.

| Frequency (MHz) | Load power (mW) | Modeled opposing-current peak (mA) | Mean external current A / B (mA) | Total IC heat (W) |
| --- | ---: | ---: | ---: | ---: |
{offset_table}

The output resistors limit mismatch current. Identical nominal models with no imposed offset cannot establish actual current sharing. AC gain and phase mismatch remain unmodeled.

## Supply and thermal estimates

The dual PA draws {min(x['plus_total_mA'] for x in two):.1f}–{max(x['plus_total_mA'] for x in two):.1f} mA from +15 V and {min(x['minus_total_mA'] for x in two):.1f}–{max(x['minus_total_mA'] for x in two):.1f} mA from −15 V. Its electrical input is {min(x['dc_total_W'] for x in two):.2f}–{max(x['dc_total_W'] for x in two):.2f} W. With an assumed 85%-efficient converter, that is approximately {min(x['dc_total_W'] for x in two)/4.25*1000:.0f}–{max(x['dc_total_W'] for x in two)/4.25*1000:.0f} mA from a 5 V converter input for the PA alone. Add the Logic RF Driver's modeled 5 V pull-up current and its separate 3.3 V circuitry. The source-stage current and clock-load limitations in the single-chip study apply.

IC heat is supply input power minus real power leaving each chip through its output and feedback pins. Output-resistor, coupling-capacitor, and filter dissipation are external to the IC heat numbers. The two-chip circuit dissipates up to {maxheat:.2f} W per chip and {totalheat:.2f} W in the chips together at nominal drive. Each extra amplifier adds quiescent power, so lower per-chip dissipation does not imply lower total dissipation.

TI lists 49.6 °C/W junction-to-ambient for the RGT package on its reference test board. The table applies the largest nominal per-chip heat to Tj = Ta + Pd × thermal resistance. It assumes no mutual thermal coupling and is only a cooling sensitivity, not a prediction for a compact two-chip PCB.

| Assumed per-chip thermal resistance (°C/W) | Junction at 25 °C ambient (°C) | Junction at 50 °C ambient (°C) |
| --- | ---: | ---: |
{thermal}

At the 49.6 °C/W reference value, an illustrative mutual coupling of 10 °C/W adds approximately {maxheat*10:.0f} °C from the other chip's heat. Actual pad soldering, thermal vias, copper area, chip spacing, and heatsinking determine the temperatures. The electrical models stay at 25 °C; neither self-heating nor temperature-dependent device response is simulated.

## Validation and reproduction

The [result record](docs/ths3491-dual-results.json) contains 58 cases, source/model hashes, individual chip currents and power, settling checks, and numerical comparisons. All cases use inductor-first input and output filters. Every transient runs 60 periods, measures the final eight, and checks the three source capacitor states for less than 50 µV change over the final 20 periods. Successive four-period power windows differ by less than 0.1%. Ngspice uses Gear integration, reltol 0.0001, and abstol 1e-12.

Three endpoint checks halve the maximum timestep. Output power changes by at most {max(abs(x['power_change_percent']) for x in checks):.4g}%, and total IC heat changes by at most {max(abs(x['heat_change_percent']) for x in checks):.4g}%. Numerical consistency does not validate the actual devices, filters, PCB stability, harmonic distortion, or thermal behavior. The models do not establish real AC mismatch, manufacturing corners, or output-filter mismatch tolerance.

Run `scripts/simulate_ths3491_dual.py` with `--research`, `--output`, `--board-runs`, and `--single-runs`, then run `scripts/report_ths3491_dual.py` with `--research` and `--runs`. The output directory needs TI's unmodified `THS3491RGT.lib` under `models/`; the report also expects the downloaded TI guide, schematic, and model archive. The retained source decks, C4 fits, retained periodic-state estimates, and external research helper are required as described in the single-chip study. Vendor model text and raw runs remain in ignored `generated/` storage.

The candidate PA is absent from the project schematic, PCB, and BOM. This study changes no CAD assets and makes no measured RF or thermal claim.
'''
(p/'THS3491-DUAL-STUDY.md').write_text(text)
print(json.dumps({'cases':len(rows),'single_mW':[min(x['fundamental_output_mW'] for x in one),max(x['fundamental_output_mW'] for x in one)],'dual_mW':[min(x['fundamental_output_mW'] for x in two),max(x['fundamental_output_mW'] for x in two)],'max_per_chip_heat_W':maxheat,'total_heat_W':totalheat,'current_check_mA':current_check,'timestep':checks},indent=2))
