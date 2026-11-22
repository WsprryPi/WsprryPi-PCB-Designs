from pathlib import Path
import sys,json,hashlib,math,re
import argparse
ap=argparse.ArgumentParser(description='Report circuit-model board results; no extracted PCB model.');ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs-directory',type=Path);a=ap.parse_args()
p=Path(__file__).resolve().parents[1];g=a.runs_directory.resolve() if a.runs_directory else p/'generated/board-simulation';r=a.research.resolve();sys.path.insert(0,str(r/'python-packages'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
rows=json.loads((g/'results.json').read_text());assert len(rows)==32
for row in rows:
 if not row['detector']:row['state_drift_V']=None
nom=sorted([x for x in rows if x['detector'] and not x['skew_s'] and x['step_factor']==1400],key=lambda x:x['f_Hz'])
base=sorted([x for x in rows if not x['detector']],key=lambda x:x['f_Hz']);assert len(nom)==len(base)==13
skews=sorted([x for x in rows if x['f_Hz']==145e6 and x['detector'] and x['step_factor']==1400],key=lambda x:x['skew_s'])
checks=[]
for x in rows:
 if x['step_factor']!=2800:continue
 ref=next(q for q in rows if q['detector'] and q['step_factor']==1400 and q['f_Hz']==x['f_Hz'] and q['skew_s']==x['skew_s'])
 checks.append({'f_Hz':x['f_Hz'],'skew_s':x['skew_s'],'power_change_percent':100*(x['fundamental_mW']/ref['fundamental_mW']-1),'activity_led_change_percent':100*(x['activity_led_mA']/ref['activity_led_mA']-1),'channel_peak_change_percent':100*(max(x['channel_peak_mA'])/max(ref['channel_peak_mA'])-1)})
fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained');ax=axes[0]
for data,label in [(base,'Detector disconnected'),(nom,'220 Ω detector connected')]:ax.semilogx([x['f_Hz']/1e6 for x in data],[x['fundamental_mW'] for x in data],marker='o',label=label)
ax.set(xlabel='Frequency (MHz)',ylabel='Fundamental into 50 Ω (mW)',title='Circuit model: nominal aligned channels',ylim=(75,87));ax.grid(alpha=.25);ax.legend(fontsize=8)
ax=axes[1]
ax.plot([x['skew_s']*1e9 for x in skews],[max(x['channel_peak_mA']) for x in skews],marker='o',color='tab:red',label='Modeled pin-current peak')
ax.axhline(32,color='gray',linestyle='--',label='32 mA DC operating reference')
ax.set(xlabel='Assumed channel skew (ns)',ylabel='Peak pin current (mA)',title='145 MHz: assumed-skew stress test');ax.grid(alpha=.25);ax.legend(fontsize=7)
fig.savefig(p/'docs/board-simulation.png',dpi=180);plt.close(fig)
source_hashes=json.loads((g/'board-inputs.json').read_text())
for f,h in source_hashes.items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h,(f,'design changed during simulation')
inputs=json.loads((g/'inputs.json').read_text());model_hashes={}
for f,h in inputs.items():
 path=Path(f)
 if path.is_relative_to(p.resolve()):key=str(path.relative_to(p.resolve()))
 elif path.is_relative_to(r):key='external-research/'+str(path.relative_to(r))
 else:raise ValueError(f)
 model_hashes[key]=h
model_hashes['scripts/report_board_simulation.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
result={'scope':'Circuit-level behavioral simulation matched to saved Logic RF Driver schematic; no PCB electromagnetic or supply-network extraction','conditions':{'VCCA_V':3.3,'VCCB_V':5,'duty_cycle':.5,'source_transition_s':.5e-9,'illustrative_source_ohms':50,'load_ohms':50,'temperature_C':25,'output_pcb_capacitance_F':2e-12,'R2_ohms':220,'C5_F':1e-8,'C6_F':1e-8,'R3_ohms':1e6,'R4_R5_ohms':680,'periods':60,'measurement_periods':8,'solver':'ngspice, Gear, reltol=0.0001, abstol=1e-12','periodic_initialization':'C5, C6, and C4 main capacitor state; loaded cases below 50 microvolts state change over final 20 periods','C4_fit_bias_V':2.51458238133},'cases':rows,'timestep_checks':checks,'design_sha256':source_hashes,'model_and_script_sha256':model_hashes,'limitations':['Nominal IBIS-derived behavioral U1 model; incomplete internal switching loss and no measured channel skew distribution.','Diodes Incorporated diode/transistor models and illustrative LED do not exactly represent selected Nexperia BAT54S, CJ transistor, or KENTO LEDs.','Ideal rails omit C1/C2/C3, supply wiring, ground bounce, and thermal response.','No extracted PCB traces, connector model, external filter, or impedance-mismatch sweep.','R1 and actual Pico/Pi/Si5351 source drivers are absent from switching-timing surrogate.','C4 fit is linear at selected DC bias; fitted initial charge is not an instantaneous nonlinear dielectric model.']}
(p/'docs/board-simulation-results.json').write_text(json.dumps(result,indent=2)+'\n')
mtable='\n'.join(f"| {x['f_Hz']/1e6:g} | {x['fundamental_mW']:.2f} mW | {x['activity_led_mA']:.2f} mA | {max(x['channel_peak_mA']):.1f} mA |" for x in nom)
stable='\n'.join(f"| {x['skew_s']*1e9:g} ns | {x['fundamental_mW']:.2f} mW | {max(x['channel_peak_mA']):.1f} mA |" for x in skews)
powerdelta=max(abs(x['power_change_percent']) for x in checks);leddelta=max(abs(x['activity_led_change_percent']) for x in checks);peakdelta=max(abs(x['channel_peak_change_percent']) for x in checks)
text=f'''# Board circuit simulation

The nominal circuit model predicts {nom[0]['fundamental_mW']:.1f} mW at 137 kHz and {nom[-1]['fundamental_mW']:.1f} mW at 145 MHz into 50 ohms with the 220-ohm detector connected. The activity LED draws about {min(x['activity_led_mA'] for x in nom):.2f}–{max(x['activity_led_mA'] for x in nom):.2f} mA. These are circuit-model predictions, not measured ratings or an electromagnetic simulation of the PCB.

[TI explicitly permits connecting the two outputs for stronger drive](https://www.ti.com/lit/ds/symlink/sn74lvc2t45.pdf), subject to the device's electrical and thermal limits. That supports the direct-parallel topology with A1/A2 driven by the same clock. The assumed-skew cases do not establish an actual timing defect or a need for series resistors. The behavioral model's current peaks are not validated predictions of this IC. The 32 mA recommended operating-current magnitude is a DC reference, not a pulse-current specification; comparing it with an approximate transient peak does not establish a device-limit violation. RF loading, supply integrity, and temperature with the actual filter remain unmeasured.

![Circuit-model power and channel-skew sensitivity](docs/board-simulation.png)

## Circuit and conditions

The exported schematic netlist connects U1 A1/A2 to CLK_IN, B1/B2 directly together at RF_RAW, and DIR to 3.3 V. C4 couples RF_RAW to RF_OUT and the 50-ohm load. R2 is 220 ohms, C5/C6 are 10 nF, R3 is 1 Mohm, and R4/R5 are 680 ohms. The detector uses the RF_RAW tap. D2 indicates RF activity, and D3 indicates the 3.3 V rail. J1/J3 are Adafruit 1865 SMA connectors, and J2 is the shared terminal/header footprint. The [result record](docs/board-simulation-results.json) ties the calculation to hashes of the saved design and model inputs.

The source is a raw 0–3.3 V, 50% duty-cycle clock with 0.5 ns transitions and an illustrative 50-ohm source impedance. The timing surrogate represents the two logic inputs. U1 has ideal 3.3 V and 5 V rails, nominal IBIS-derived output tables, simplified package parasitics, and 2 pF of output-board capacitance. The Samsung C4 model uses the retained bias-dependent passive fit, linearized at about 2.515 V. Its initialized charge is adjusted for periodic operation; its network coefficients remain fixed within each transient.

Ngspice uses Gear integration at 25 C, reltol 0.0001, and abstol 1e-12. Each case runs for 60 clock periods and measures the final eight. Loaded cases search initial states for C5, C6, and C4's main capacitor. Their final 20-period state changes are below 50 microvolts. The primary sweep uses a maximum timestep of one period divided by 1400. Endpoint checks and the 0.1 ns skew check use one period divided by 2800.

## Frequency sweep

Power is the Fourier fundamental at the 50-ohm load, excluding filter and connector loss. Current peaks are the larger magnitude at either modeled output pin, including package and switching effects.

| Frequency (MHz) | Fundamental power | Activity LED | Peak per U1 output |
| --- | ---: | ---: | ---: |
{mtable}

The detector costs about {100*(1-nom[0]['fundamental_mW']/base[0]['fundamental_mW']):.1f}% of fundamental power at 137 kHz and {100*(1-nom[-1]['fundamental_mW']/base[-1]['fundamental_mW']):.1f}% at 145 MHz. R2 dissipates about {min(x['R2_mean_mW'] for x in nom):.1f}–{max(x['R2_mean_mW'] for x in nom):.1f} mW in these cases, below its selected 100 mW rating under the model's conditions.

The illustrative power LED draws {nom[0]['power_led_mA']:.2f} mA from 3.3 V. Both LED branches together draw approximately {min(x['led_rail_mA'] for x in nom):.2f}–{max(x['led_rail_mA'] for x in nom):.2f} mA. That is LED-branch current, not total board current: U1's internal 3.3 V consumption and the separate 5 V RF-stage burden are additional. Actual LED current and visibility depend on the selected components.

At 137 kHz, the third harmonic is {nom[0]['third_harmonic_dBc']:.1f} dBc and the fifth is {nom[0]['fifth_harmonic_dBc']:.1f} dBc into the resistive load. The switching waveform therefore needs the selected-band output filter. Filter loading can change both output power and pin current; no filter is present in this calculation.

## Channel timing sensitivity at 145 MHz

The sensitivity cases delay one channel's output weighting waveform relative to the other. These offsets are assumptions, not TI skew specifications or a probability distribution. They model disagreement between the two channels at transitions, while retaining the same nominal device tables.

| Assumed channel skew | Fundamental power | Peak per U1 output |
| --- | ---: | ---: |
{stable}

The shifted waveforms can create opposing currents in this model. The offsets are neither a measured same-chip mismatch nor a manufacturer limit, and the model does not establish their likelihood. Its large peaks cannot establish a fault in the actual directly paralleled device. Numerical convergence validates the solver's consistency, not those current predictions. TI's explicit support for paralleling is the stronger evidence for selecting the topology. The RF application still requires electrical and thermal validation with its intended load and filter.

## Numerical checks and limits

There are 32 numerically accepted cases: 13 frequencies with and without the detector, three nonzero skew cases at 145 MHz, two finer-timestep endpoint checks, and a finer-timestep check of the 0.1 ns skew case. Halving the maximum timestep changes fundamental power by at most {powerdelta:.4f}%, activity-LED current by {leddelta:.4f}%, and peak output current by {peakdelta:.3f}%. The result record contains individual state and late-window power checks. These checks establish numerical consistency within this model.

The diode and transistor models are from Diodes Incorporated, and the LED model is illustrative. They are not exact models for the selected Nexperia BAT54S, CJ MMBT3904, or KENTO LEDs. The periodic-state calculation does not characterize power-up or LED hold time. The U1 surrogate uses nominal IBIS tables and approximate timing; it is not a full IBIS or transistor-level implementation. Transition weighting can double-count capacitive effects, making current spikes particularly uncertain. It does not represent process corners, asymmetric output strengths, on-die crossover, or a measured skew distribution.

C1/C2/C3 and real supply wiring are outside the ideal-rail calculation. There is no extracted PCB trace, ground-return, connector, solder-finish, or external-filter model. The short RF paths, stitching, C6 placement, and SMA launch geometry therefore have no simulated RF-loss or ringing qualification. R1's explicit input loading and actual Pico, Pi, and Si5351 output stages are absent from the timing surrogate. This study assumes a source that supplies a valid clock at the requested frequency.

The direct-parallel topology has manufacturer support, and the circuit model predicts roughly 80 mW of fundamental RF power with useful activity indication. Full-band reliability, thermal margin, supply integrity, filter interaction, and source compatibility remain unmeasured. See the [model scope](MODEL-SCOPE.md), [C4 analysis](C4-SELECTION.md), and [detector study](INPUT-LOADING.md).
'''
text+='\nThe [output-sharing resistor study](OUTPUT-SHARING.md) compares optional isolation-resistor candidates. Its hypothetical skew cases do not demonstrate that the board requires those resistors.\n'
(p/'BOARD-SIMULATION.md').write_text(text)
print(json.dumps({'cases':len(rows),'nominal_endpoints_mW':[nom[0]['fundamental_mW'],nom[-1]['fundamental_mW']],'skew':skews,'checks':checks},indent=2))
