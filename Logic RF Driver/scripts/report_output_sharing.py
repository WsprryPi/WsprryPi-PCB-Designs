"""Report per-output ballast resistor circuit simulations without PCB changes."""
from pathlib import Path
import argparse,json,sys,hashlib,math
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);a=ap.parse_args()
p=Path(__file__).resolve().parents[1];g=p/'generated/output-sharing';research=a.research.resolve();sys.path.insert(0,str(research/'python-packages'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rows=json.loads((g/'results.json').read_text());plan=json.loads((g/'full-plan.json').read_text());assert len(rows)==len(plan)==92
keys=lambda x:(x['f_Hz'],x['series_ohms'],x['skew_s'],x['step_factor'],x['strength_mismatch_fraction'],x['resistor_parasitics'])
assert {keys(x) for x in rows}=={tuple(x) for x in plan}
def get(f,r,sk=0,step=1400,mismatch=0,paras=False):return next(x for x in rows if keys(x)==(f,r,sk,step,mismatch,paras))
freq=sorted({x['f_Hz'] for x in rows});rs=[0,1,2.2,4.7,10,22,33,47,68,100];skews=[0,.1e-9,.5e-9,1e-9]
base_record=json.loads((p/'docs/board-simulation-results.json').read_text());base={x['f_Hz']:x for x in base_record['cases'] if x['detector'] and not x['skew_s'] and x['step_factor']==1400}
chosen=[get(f,10) for f in freq];higher=[get(f,22) for f in freq]
retention=[x['fundamental_mW']/base[x['f_Hz']]['fundamental_mW'] for x in chosen]
checks=[]
for x in rows:
 if x['step_factor']!=2800:continue
 ref=get(x['f_Hz'],x['series_ohms'],x['skew_s'])
 checks.append({'f_Hz':x['f_Hz'],'series_ohms':x['series_ohms'],'skew_s':x['skew_s'],'power_change_percent':100*(x['fundamental_mW']/ref['fundamental_mW']-1),'peak_current_change_percent':100*(max(x['channel_peak_mA'])/max(ref['channel_peak_mA'])-1)})
paras=[]
for r in [4.7,10,22]:
 x=get(145e6,r,.1e-9,paras=True);ref=get(145e6,r,.1e-9)
 paras.append({'series_ohms':r,'power_change_percent':100*(x['fundamental_mW']/ref['fundamental_mW']-1),'peak_current_change_percent':100*(max(x['channel_peak_mA'])/max(ref['channel_peak_mA'])-1)})
fig,axes=plt.subplots(1,3,figsize=(14,4.2),layout='constrained')
for r,data in [(0,[base[f] for f in freq]),(10,chosen),(22,higher)]:axes[0].semilogx([x['f_Hz']/1e6 for x in data],[x['fundamental_mW'] for x in data],marker='o',label=f'{r:g} Ω per output')
axes[0].set(xlabel='Frequency (MHz)',ylabel='Fundamental power into 50 Ω (mW)',title='Aligned channels, detector connected');axes[0].legend(fontsize=8);axes[0].grid(alpha=.25)
for sk in skews:axes[1].plot(rs,[max(get(145e6,r,sk)['channel_peak_mA']) for r in rs],marker='o',label=f'{sk*1e9:g} ns skew')
axes[1].set_xscale('symlog',linthresh=1);axes[1].axhline(32,color='gray',linestyle='--',linewidth=1,label='32 mA operating reference');axes[1].axvline(10,color='gray',linestyle=':',linewidth=1);axes[1].set(xlabel='Series resistance per output (Ω)',ylabel='Modeled peak pin current (mA)',title='145 MHz: timing sensitivity');axes[1].legend(fontsize=8);axes[1].grid(alpha=.25)
axes[2].plot(rs,[get(145e6,r)['activity_led_mA'] for r in rs],marker='o');axes[2].set_xscale('symlog',linthresh=1);axes[2].set_yscale('log');axes[2].axvline(10,color='gray',linestyle=':',linewidth=1);axes[2].set(xlabel='Series resistance per output (Ω)',ylabel='Activity LED current (mA)',title='145 MHz: illustrative detector model');axes[2].grid(alpha=.25)
fig.savefig(p/'docs/output-sharing.png',dpi=180);plt.close(fig)
review=json.loads((g/'current-review.json').read_text()) if (g/'current-review.json').exists() else None
source=review['source_sha256'] if review else json.loads((g/'design-inputs.json').read_text())
for f,h in source.items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h,(f,'design changed')
inputs=json.loads((g/'inputs.json').read_text());hashes={}
for f,h in inputs.items():
 path=Path(f)
 if path.is_relative_to(p.resolve()):key=str(path.relative_to(p.resolve()))
 elif path.is_relative_to(research):key='external-research/'+str(path.relative_to(research))
 else:raise ValueError(f)
 hashes[key]=h
for f in ['scripts/report_output_sharing.py','docs/board-simulation-results.json']:hashes[f]=hashlib.sha256((p/f).read_bytes()).hexdigest()
result={'scope':'Candidate independent resistors between U1 B1/B2 pins and RF_RAW join; schematic and PCB retain direct parallel connection','baseline_connection':'direct_parallel','series_resistor_candidate_ohms_each':10,'choice_basis':'Optional resistive isolation within a roughly 1 dB power-loss budget; hypothetical skew tests do not demonstrate a need for resistors','cases':rows,'timestep_checks':checks,'resistor_parasitic_checks':paras,'design_sha256':source,'model_and_script_sha256':hashes,'cad_review':review,'conditions':{'VCCA_V':3.3,'VCCB_V':5,'load_ohms':50,'R2_ohms':220,'C5_C6_F':1e-8,'clock_duty_cycle':.5,'source_edge_s':.5e-9,'illustrative_source_ohms':50,'temperature_C':25,'periods':60,'measurement_periods':8,'nominal_max_timestep_divisor':1400,'fine_max_timestep_divisor':2800,'relative_tolerance':.0001,'absolute_tolerance':1e-12,'periodic_state_drift_limit_V':5e-5,'skew_s':skews,'hypothetical_strength_mismatch':[1.1,.9],'mismatch_resistor_multipliers':[.99,1.01],'illustrative_resistor_inductance_H':.5e-9,'illustrative_resistor_parallel_capacitance_F':.05e-12},'limitations':['Nominal IBIS-derived behavioral surrogate; large current peaks are especially model-dependent.','Skew values and +/-10 percent drive strength are assumed stress tests, not TI limits or measured distributions.','Diodes semiconductor models and illustrative LED do not exactly model selected detector parts.','No extracted PCB, supply impedance, connector, external filter, internal crossover-loss, or thermal model.','C4 is a passive fit linearized near 2.515 V, with initial charge adjusted for periodic operation.','Parasitic RLC values are illustrative, not a selected resistor manufacturer model.']}
(p/'docs/output-sharing-results.json').write_text(json.dumps(result,indent=2)+'\n')
summary='\n'.join(f"| {r:g} Ω | {get(145e6,r)['fundamental_mW']:.2f} mW | {max(get(145e6,r,.1e-9)['channel_peak_mA']):.1f} mA | {max(get(145e6,r,.5e-9)['channel_peak_mA']):.1f} mA | {get(145e6,r)['activity_led_mA']:.4g} mA |" for r in rs)
band='\n'.join(f"| {f/1e6:g} | {base[f]['fundamental_mW']:.2f} | {get(f,10)['fundamental_mW']:.2f} | {get(f,22)['fundamental_mW']:.2f} | {max(get(f,10,.1e-9)['channel_peak_mA']):.1f} |" for f in freq)
strength='\n'.join(f"| {r:g} Ω | {get(145e6,r,mismatch=.1)['channel_rms_mA'][0]:.2f} mA | {get(145e6,r,mismatch=.1)['channel_rms_mA'][1]:.2f} mA | {100*abs(get(145e6,r,mismatch=.1)['channel_rms_mA'][0]-get(145e6,r,mismatch=.1)['channel_rms_mA'][1])/(sum(get(145e6,r,mismatch=.1)['channel_rms_mA'])/2):.1f}% |" for r in [0,4.7,10,22,33])
nom10=get(145e6,10);zero10=get(145e6,0,.1e-9);sk10=get(145e6,10,.1e-9)
maxR=max(max(x['resistor_mean_mW']) for x in rows if x['series_ohms']==10)
text=f'''# Output sharing resistors

[TI explicitly permits connecting the two outputs for stronger drive](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf). With A1/A2 driven by the same clock, direct paralleling is the supported baseline, subject to electrical and thermal limits. The assumed-skew tests do not establish an actual timing problem or a need for series resistors; their transient current peaks are not validated predictions of this IC.

**For optional resistive isolation, 10 ohms on each output is a candidate within a roughly 1 dB power-loss budget.** With the detector connected and aligned channels, it gives {chosen[0]['fundamental_mW']:.1f} mW at 137 kHz and {nom10['fundamental_mW']:.1f} mW at 145 MHz into 50 ohms. It retains {min(retention)*100:.1f}–{max(retention)*100:.1f}% of the direct-parallel model's nominal power across the 13-frequency sweep, a loss of about {max(-10*math.log10(x) for x in retention):.2f} dB. This choice gives roughly a 1 dB RF-power-loss budget priority over stronger isolation; it is not a unique optimum or a pulse-current guarantee.

At 145 MHz with an assumed 0.1 ns skew, 10 ohms lowers the larger modeled pin-current peak from {max(zero10['channel_peak_mA']):.1f} mA to {max(sk10['channel_peak_mA']):.1f} mA. Peak opposing current falls from {zero10['circulating_peak_mA']:.1f} mA to {sk10['circulating_peak_mA']:.1f} mA. TI's 32 mA recommended output-current magnitude at a 5 V output supply is a DC reference, not a pulse-current specification. Comparing it with an approximate transient peak does not establish a device-limit violation. The model does not establish acceptable pulse operation or junction temperature.

![Power, output current, and activity indication](docs/output-sharing.png)

## Candidate circuit

Each output has its own resistor, located between its U1 pin and the RF_RAW join. C4 and the R2 detector tap connect to the shared node. A resistor on the shared output cannot isolate the two pins from each other. The schematic and PCB have directly paralleled outputs; these resistors are simulation candidates and are absent from the design and BOM. The PCB's component pad nets match the unchanged schematic. The [CAD validation record](VALIDATION.md) describes the configured checks and results. Geometry and copper-fill defects are outside this circuit model.

```text
U1.7 B1 ── RisoA ──┐
                   ├── RF_RAW ── C4 ── RF_OUT ── 50 Ω
U1.6 B2 ── RisoB ──┘      └──── R2 ── detector
```

Equal 10-ohm resistors appear as about 5 ohms of added source resistance to the common load while the outputs agree. Opposing output currents pass through both resistors. The resistors therefore trade output amplitude for isolation and sharing; their effect depends on switching time, device impedance, and load.

## Resistance sweep at 145 MHz

Nominal power and LED current use aligned channels. Current peaks use the skew shown in each column. They are the larger absolute current at either output pin. All cases retain Samsung C4, the 220-ohm R2, and the detector.

| Resistance on each output | Nominal fundamental power | Peak pin current, 0.1 ns skew | Peak pin current, 0.5 ns skew | Nominal activity LED |
| --- | ---: | ---: | ---: | ---: |
{summary}

The 1–2.2 ohm values preserve power but provide little isolation. The 4.7-ohm option has a smaller power cost than 10 ohms and also a smaller current reduction. The 22- and 33-ohm options provide stronger isolation at a substantial RF-power cost, with much lower modeled LED current at 145 MHz. LED visibility depends on the actual selected parts and ambient light; the illustrative LED model does not rate brightness.

The hypothetical larger-skew tests with 10 ohms give {max(get(145e6,10,.5e-9)['channel_peak_mA']):.1f} mA at 0.5 ns and {max(get(145e6,10,1e-9)['channel_peak_mA']):.1f} mA at 1 ns. Those cases are stress diagnostics, not qualified operating points. Much larger resistors suppress those currents further, at the expense of RF output and detector drive. These tests compare sensitivity within the model; they do not justify a guaranteed operating envelope or establish that direct paralleling needs correction. The assumed skew values are not TI specifications or measured probabilities.

## Frequency sweep

The direct-parallel reference is the aligned-channel detector-loaded [board circuit model](BOARD-SIMULATION.md). The 10- and 22-ohm candidates use 13 frequencies from 137 kHz through 145 MHz. The 10-ohm candidate also has the same full-band sweep at 0.1 ns skew. Fundamental power excludes external-filter and connector loss.

| Frequency (MHz) | Direct parallel (mW) | 10 Ω each (mW) | 22 Ω each (mW) | 10 Ω each: peak pin current at 0.1 ns skew (mA) |
| --- | ---: | ---: | ---: | ---: |
{band}

With 10 ohms and aligned channels, activity-LED current spans {min(x['activity_led_mA'] for x in chosen):.2f}–{max(x['activity_led_mA'] for x in chosen):.2f} mA. The full-band power response remains broad in this circuit model. Neither the source timing surrogate nor the flat response establishes compatibility with every Pico, Pi, or Si5351 configuration.

## Sharing between unequal outputs

The mismatch cases multiply channel 0's nominal drive tables by 1.10 and channel 1's by 0.90, with aligned timing. The added resistors use −1% on the stronger channel and +1% on the weaker channel. These are deliberately opposed hypothetical errors, not a manufacturer process corner. The RMS-current imbalance is the absolute difference divided by the mean of the two RMS currents. It measures sharing in these aligned-waveform cases, separately from timing-induced opposing current.

| Resistance on each output | Channel 0 RMS current | Channel 1 RMS current | RMS-current imbalance |
| --- | ---: | ---: | ---: |
{strength}

The series resistors reduce sensitivity to the assumed drive-strength difference. They do not force equal current during transitions or eliminate on-die switching loss.

Skew-driven pulses also occur at low frequency; their repetition rate changes the average loss. With 10 ohms and 1 ns skew, the larger resistor loss is {max(get(137e3,10,1e-9)['resistor_mean_mW']):.1f} mW at 137 kHz and {max(get(145e6,10,1e-9)['resistor_mean_mW']):.1f} mW at 145 MHz. This is resistor heating in the model, not U1 junction heating.

## Resistor loss and parasitics

At 145 MHz with aligned channels, each 10-ohm resistor dissipates about {max(nom10['resistor_mean_mW']):.1f} mW. The largest modeled loss for either 10-ohm resistor among all cases is {maxR:.1f} mW. These are mean I-squared-R losses under the stated conditions, not a pulse-overload qualification. A chosen physical resistor also needs suitable continuous-power derating, pulse capability, and RF characteristics.

Separate 145 MHz, 0.1 ns-skew checks add an illustrative 0.5 nH in series and 0.05 pF across each resistor branch for 4.7, 10, and 22 ohms. They change power by at most {max(abs(x['power_change_percent']) for x in paras):.2f}% and peak pin current by {max(abs(x['peak_current_change_percent']) for x in paras):.2f}%. These RLC values are sensitivity assumptions, not a selected component's model or a PCB extraction.

## Numerical checks and model limits

The [result record](docs/output-sharing-results.json) contains 92 cases, source-design and model hashes, and individual settling checks. The cases cover the 145 MHz resistance/skew screen, full-band candidate sweeps, low-frequency skew checks, drive-strength mismatch, resistor parasitics, and four finer-timestep checks. Ngspice uses Gear integration at 25 C, reltol 0.0001, and abstol 1e-12. Each case runs for 60 periods and measures the final eight. C4, C5, and C6 initial states are searched for final 20-period changes below 50 microvolts. A nearby completed case supplies a starting estimate where available; each accepted case independently meets the settling checks.

The maximum timestep is one period divided by 1400, or 2800 for the finer checks. Halving it changes power by at most {max(abs(x['power_change_percent']) for x in checks):.4f}% and peak pin current by {max(abs(x['peak_current_change_percent']) for x in checks):.3f}%. The late-window power check permits less than 0.1% change. These checks establish numerical consistency within the model.

U1 uses nominal IBIS-derived behavioral output tables with simplified timing and package effects. Transition weighting can double-count capacitive effects, so current spikes are especially uncertain. Complete internal crossover, supply-current transients, process corners, heating, and actual channel skew are absent. The diode and transistor models are Diodes Incorporated surrogates; the LED model is illustrative. They are not exact models of the selected Nexperia diode, CJ transistor, or KENTO LEDs.

The source is a raw 0–3.3 V clock with 50% duty cycle, 0.5 ns source transitions, and an illustrative 50-ohm source impedance. Supplies are ideal 3.3 V and 5 V rails. C4 uses the Samsung passive fit linearized near 2.515 V with periodic initial-charge adjustment. C1/C2/C3, supply wiring, real input-driver stages, extracted PCB traces and returns, SMA launches, and an external filter are absent. Power and current are simulated estimates; acceptable full-band operation and component temperatures remain unmeasured.
'''
(p/'OUTPUT-SHARING.md').write_text(text)
print(json.dumps({'cases':len(rows),'power_retention_percent':[min(retention)*100,max(retention)*100],'10ohm_endpoints_mW':[chosen[0]['fundamental_mW'],nom10['fundamental_mW']],'max_10ohm_resistor_mW':maxR,'checks':checks,'parasitics':paras},indent=2))
