"""Publish the candidate THS3491 study with explicit model and thermal limits."""
from pathlib import Path
import argparse,sys,json,hashlib,re,math
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs',type=Path,required=True);a=ap.parse_args()
sys.path.insert(0,str(a.research/'python-packages'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1];g=a.runs.resolve();rows=json.loads((g/'results.json').read_text());plan=json.loads((g/'plan.json').read_text());assert len(rows)==len(plan)
base=sorted([x for x in rows if x['additional_loss_dB_each']==.5 and x['inductor_Q']==50 and x['divider_voltage_ratio']==.5 and x['step_divisor']==1000 and not x['original_vendor_current_sign'] and not x['input_shunt_first']],key=lambda x:x['f_Hz'])
boost=sorted([x for x in rows if x['additional_loss_dB_each']==.5 and x['inductor_Q']==50 and x['divider_voltage_ratio']==.6 and x['step_divisor']==1000 and not x['original_vendor_current_sign'] and not x['input_shunt_first']],key=lambda x:x['f_Hz'])
assert len(base)==len(boost)==13
checks=[]
for x in rows:
 if x['step_divisor']!=2000:continue
 ref=next(z for z in rows if z['f_Hz']==x['f_Hz'] and z['divider_voltage_ratio']==x['divider_voltage_ratio'] and z['step_divisor']==1000 and z['additional_loss_dB_each']==.5 and z['inductor_Q']==50 and not z['original_vendor_current_sign'] and not z['input_shunt_first'])
 checks.append({'case':x['case'],'fundamental_power_change_percent':100*(x['fundamental_output_mW']/ref['fundamental_output_mW']-1),'heat_change_percent':100*(x['pa_heat_W']/ref['pa_heat_W']-1),'peak_current_change_percent':100*(x['pa_pin_peak_current_mA']/ref['pa_pin_peak_current_mA']-1)})
orig=next(x for x in rows if x['original_vendor_current_sign']);ref=base[-1]
current_check=max(max(abs(x['pa_plus_mA']-x['pa_plus_independent_mA']),abs(x['pa_minus_mA']-x['pa_minus_independent_mA'])) for x in rows if not x['original_vendor_current_sign'])
source={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in ['Logic RF Driver.kicad_sch','Logic RF Driver.kicad_pcb','Logic RF Driver.kicad_pro','Logic RF Driver.kicad_dru','BOM.csv']}
inputs={}
for f in [g/'models/ti-dda.zip',g/'models/THS3491DDA.lib',g/'models/THS3491DDA-current-sign.lib',p/'scripts/simulate_ths3491.py',Path(__file__),p/'docs/board-simulation-results.json',a.research/'simulate.py']:
 key=str(f.relative_to(p)) if f.is_relative_to(p) else 'external-research/'+str(f.relative_to(a.research));inputs[key]=hashlib.sha256(f.read_bytes()).hexdigest()
# Retain exact run decks and C4 fits as evidence hashes; vendor text is not redistributed.
for f in sorted((g/'runs').glob('*_cp2p.cir')):inputs[str(f.relative_to(p))]=hashlib.sha256(f.read_bytes()).hexdigest()
result={'scope':'Candidate THS3491DDA amplifier driven by the unchanged Logic RF Driver circuit; no PA implemented in KiCad','cases':rows,'timestep_checks':checks,'native_peak_rechecks':json.loads((g/'peak-checks.json').read_text()),'rail_current_independent_check_max_difference_mA':current_check,'vendor_sign_control':{'original_case':orig['case'],'corrected_case':ref['case'],'output_power_change_percent':100*(ref['fundamental_output_mW']/orig['fundamental_output_mW']-1),'original_plus_mA':orig['pa_plus_mA'],'original_minus_mA':orig['pa_minus_mA']},'design_sha256':source,'model_and_script_sha256':inputs,'conditions':{'supplies_V':[15,-15],'nominal_temperature_C':25,'feedback_ohms':798,'gain_resistor_ohms':200,'output_isolation_ohms':1,'output_coupling_F':1e-6,'output_cap_ESR_ohms':.03,'output_cap_ESL_H':.5e-9,'load_ohms':50,'LPF_order_each':5,'LPF_type':'Butterworth L-C-L-C-L; capacitor-first input sensitivity C-L-C-L-C','LPF_cutoff_ratio':1.5,'inductor_Q_test_frequency':[25,50,100],'inductor_parallel_C_F':'min(2 pF, C for SRF = 5*fc)','capacitor_Q_test_frequency':1000,'capacitor_ESL_H':.3e-9,'additional_matched_pad_dB_each':[0,.5,1],'periods':60,'final_Fourier_periods':8,'periodic_capacitor_drift_limit_V':5e-5,'late_power_drift_limit_percent':.1,'reference_DDA_JEDEC_RthetaJA_C_per_W':44.5,'thermal_sensitivity_C_per_W':[40,60,80,100]},'limitations':['Representative separately selected filters, not measured or component-selected filter boards.','U1 is the retained nominal IBIS-derived behavioral surrogate; output pulse currents and full supply current are unqualified.','TI THS3491 model is nominal at 25 C and +/-15 V; no temperature-dependent device model or thermal feedback.','Vendor negative-rail load-current source sign is corrected explicitly; RF transfer is checked against original model.','Macro-model harmonic distortion is not specified as accurate; displayed harmonics are diagnostic.','No extracted PCB, connector, supply impedance, converter circuit, mismatch sweep, or process-corner model.','Datasheet maximum-linear-output envelope remains an independent constraint; a converged SPICE run does not override it.','3.3 V rail number covers LED branches only; U1 VCCA dynamic current and actual clock-source current are not simulated.']}
(p/'docs/ths3491-results.json').write_text(json.dumps(result,indent=2)+'\n')
fig,ax=plt.subplots(1,3,figsize=(14,4.1),layout='constrained')
for series,label in [(base,'Half-voltage divider'),(boost,'0.6-voltage divider')]:
 f=[x['f_Hz']/1e6 for x in series];ax[0].semilogx(f,[x['fundamental_output_mW'] for x in series],'-o',label=label);ax[1].semilogx(f,[x['pa_pin_Vpp'] for x in series],'-o',label=label);ax[2].semilogx(f,[x['pa_heat_W'] for x in series],'-o',label=label)
ax[1].errorbar([145],[14.5],yerr=[.5],fmt='s',color='gray',capsize=4,label='TI limit near 145 MHz (approx.)')
ax[1].plot([145],[boost[-1]['pa_pin_Vpp']*math.sqrt(500/boost[-1]['fundamental_output_mW'])],'rx',label='500 mW required at 145 MHz (scaled)')
ax[0].axhline(500,color='gray',linestyle='--');ax[0].set(ylabel='Fundamental power at 50 Ω load (mW)',title='Both filters included');ax[1].set(ylabel='THS3491 pin swing (Vpp)',title='Check against TI linear envelope');ax[2].set(ylabel='Estimated IC heat (W)',title='Nominal electrical dissipation')
for z in ax:z.set_xlabel('Frequency (MHz)');z.grid(alpha=.25);z.legend(fontsize=7)
fig.savefig(p/'docs/ths3491.png',dpi=180);plt.close(fig)
line=lambda x:f"| {x['f_Hz']/1e6:g} | {x['fundamental_output_mW']:.1f} | {x['pa_pin_Vpp']:.2f} | {x['pa_plus_mA']:.1f} / {x['pa_minus_mA']:.1f} | {x['pa_heat_W']:.2f} | {x['logic_5V_pullup_mA']:.1f} |"
full='\n'.join(line(x) for x in base)
endpoint=[x for x in rows if x['f_Hz'] in [137e3,145e6] and x['step_divisor']==1000 and x['inductor_Q']==50 and not x['original_vendor_current_sign'] and not x['input_shunt_first']]
loss_table='\n'.join(f"| {x['f_Hz']/1e6:g} | {x['additional_loss_dB_each']:g} | {x['divider_voltage_ratio']:g} | {x['fundamental_output_mW']:.1f} | {x['pa_pin_Vpp']:.2f} | {x['pa_heat_W']:.2f} |" for x in sorted(endpoint,key=lambda x:(x['f_Hz'],x['divider_voltage_ratio'],x['additional_loss_dB_each'])))
cap=[x for x in rows if x['input_shunt_first']]
cap_table='\n'.join(f"| {x['f_Hz']/1e6:g} | {'C first' if x['input_shunt_first'] else 'L first'} | {x['fundamental_output_mW']:.1f} | {max(x['logic_channel_peak_mA']):.1f} | {x['logic_5V_pullup_mA']:.1f} |" for x in sorted([base[0],base[-1],*cap],key=lambda x:(x['f_Hz'],x['input_shunt_first'])))
thermal='\n'.join(f"| {theta:g} | {25+max(x['pa_heat_W'] for x in base)*theta:.0f} | {50+max(x['pa_heat_W'] for x in base)*theta:.0f} |" for theta in [40,44.5,60,80,100])
text=f'''# THS3491 amplifier circuit study

The proposed gain-of-five THS3491DDA circuit with a half-voltage input divider predicts {min(x['fundamental_output_mW'] for x in base):.0f}–{max(x['fundamental_output_mW'] for x in base):.0f} mW of fundamental output across 137 kHz–145 MHz with both representative filters included. The 0.6-voltage divider predicts {min(x['fundamental_output_mW'] for x in boost):.0f}–{max(x['fundamental_output_mW'] for x in boost):.0f} mW. These are candidate-circuit calculations, not RF measurements or an implemented PA board.

This circuit does not establish 500 mW across the full range. At 145 MHz the higher-drive case gives {boost[-1]['fundamental_output_mW']:.1f} mW with {boost[-1]['pa_pin_Vpp']:.2f} Vpp at the PA output pin. Linear scaling to 500 mW would require approximately {boost[-1]['pa_pin_Vpp']*math.sqrt(500/boost[-1]['fundamental_output_mW']):.1f} Vpp, above TI's approximately 14–15 Vpp recommended linear envelope there. Different filter matching or another PA arrangement can change the result; this study does not prove that every THS3491 circuit is limited to these powers.

![Candidate output power, pin swing, and IC heat](docs/ths3491.png)

## Circuit

The unchanged Logic RF Driver circuit includes its directly joined SN74LVC2T45 outputs, Samsung C4 fit, RF_RAW detector, and both LEDs. Its output feeds an inductor-first low-pass filter, a matched loss network, and the input divider. The THS3491DDA uses 798 ohms of feedback and 200 ohms from the inverting input to ground, giving a nominal voltage gain of 4.99. REF is grounded and PD is held at 3.3 V. Supplies are ideal +15 V and −15 V.

The half-voltage divider has 100 ohms from its input to ground, 50 ohms in series to the noninverting input, and 50 ohms from that input to ground. Its nominal input resistance is 50 ohms. The higher-drive divider uses 125 ohms, 33.333 ohms, and 50 ohms, respectively. Input capacitance in TI's model is included.

The amplifier output has a 1-ohm isolation resistor and a 1 µF coupling capacitor with illustrative 0.03-ohm ESR and 0.5 nH ESL. A second inductor-first low-pass filter and a second matched loss network feed the grounded 50-ohm load. There is no 50-ohm series output termination. The small isolation resistor does not establish stability into arbitrary filters or cables.

## Filters and loss assumptions

Each filter is a fifth-order Butterworth L-C-L-C-L ladder designed for 50-ohm terminations, with cutoff at 1.5 times the test frequency. The normalized values are 0.618034, 1.618034, 2, 1.618034, and 0.618034. Every test frequency uses a separately scaled component set; these are representative band-selected filters, not a single filter covering the entire range.

Inductor series loss uses Q = 50 at the test frequency. Parallel winding capacitance is the smaller of 2 pF and the value giving self-resonance at five times cutoff. Capacitor Q is 1000, with 0.3 nH series inductance. Endpoint sensitivities use inductor Q = 25 and 100. These assumptions do not identify suitable actual inductors or guarantee their current rating, self-resonance, or loss.

The nominal matched loss network adds 0.5 dB to each filter's finite-Q loss. Endpoint cases add 0 or 1 dB instead. These networks represent additional dissipative loss; the actual LC networks determine reflection, harmonic loading, and the amplifier's load. Their 50-ohm design impedance does not make the THS3491 output a 50-ohm source.

## Full-band results

The table uses the half-voltage divider, nominal Q, and 0.5 dB of additional loss at each filter. Power is the fundamental at the final 50-ohm load, not total square-wave power. Rail currents are positive draw magnitudes.

| Frequency (MHz) | Load power (mW) | PA pin swing (Vpp) | +15 V / −15 V draw (mA) | IC heat (W) | Logic 5 V pull-up estimate (mA) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{full}

## Drive and loss sensitivity

The extra-loss column applies to each filter independently, in addition to finite-Q loss. The divider ratio is the voltage fraction at the amplifier input.

| Frequency (MHz) | Extra loss per filter (dB) | Divider ratio | Load power (mW) | PA pin swing (Vpp) | IC heat (W) |
| --- | ---: | ---: | ---: | ---: | ---: |
{loss_table}

TI's [maximum recommended output-voltage graph](https://www.ti.com/lit/ds/symlink/ths3491.pdf#page=29) is an independent constraint. Its ±15 V curve permits approximately 14–15 Vpp near 145 MHz. A model result above that envelope does not establish linear operation. The model's 9000 V/µs internal slew parameter also differs from the datasheet's 8000 V/µs typical headline specification. Neither the nominal small-signal bandwidth nor numerical convergence establishes 500 mW at the filtered load.

## Inductor-first and capacitor-first input filters

The capacitor-first sensitivity replaces only the input ladder with C-L-C-L-C using the same normalized values, cutoff, and loss assumptions. The output filter remains inductor-first.

| Frequency (MHz) | Input filter | Load power (mW) | Larger modeled U1 pin peak (mA) | Logic 5 V pull-up estimate (mA) |
| --- | --- | ---: | ---: | ---: |
{cap_table}

The four filter-topology comparisons extract U1 peaks from native adaptive solver samples. The result record also retains four replays of those cases; the largest fundamental-power difference is {max(abs(x['power_change_percent']) for x in json.loads((g/'peak-checks.json').read_text())):.4g}%. Other case peak fields use 2000 uniform samples per period and can miss narrow logic edges, especially at low frequency. Average power and current use the uniform Fourier window.

The pulse-current figures are sensitive to the IBIS-derived switching surrogate and assumed parasitics. They compare loading in this model and do not establish actual pulse-current ratings or a measured U1 defect. A capacitor-first input directly exposes the logic outputs to the filter's shunt capacitance. Inductor-first is the preferred starting topology for this switching source, with actual ringing and current checked on hardware.

## Current draw and heat

TI's [TINA-TI DDA model](https://www.ti.com/lit/zip/SBOMAI5) sets active quiescent current to 16.8 mA and estimates load-dependent supply current. Its GOUTN source has the opposite sign from a physical negative-rail sink-current load. The unmodified model gives {orig['pa_plus_mA']:.2f} mA on +15 V and {orig['pa_minus_mA']:.2f} mA on −15 V in the 145 MHz control case. That raw negative-rail value cannot support a power or heat estimate.

The working copy changes only the sign of GOUTN's negative-current term. The original download is retained. Changing that sign changes control-case output power by {100*(ref['fundamental_output_mW']/orig['fundamental_output_mW']-1):.6g}%. Independently calculating each rail's current as 16.8 mA plus the corresponding half-wave of total output-pin current agrees within {current_check:.5g} mA. Total output-pin current includes the feedback branch. This is a documented model correction, not evidence of a hardware defect.

IC heat is supply power minus real power delivered through the output pin, including the external feedback network. The separate filter/isolation loss is external dissipation. The model does not establish additional high-frequency internal losses, temperature-dependent current, converter loss, or real-board cooling.

The nominal circuit predicts {min(x['pa_plus_mA'] for x in base):.1f}–{max(x['pa_plus_mA'] for x in base):.1f} mA from +15 V and {min(x['pa_minus_mA'] for x in base):.1f}–{max(x['pa_minus_mA'] for x in base):.1f} mA from −15 V. Its THS3491 dissipation is {min(x['pa_heat_W'] for x in base):.2f}–{max(x['pa_heat_W'] for x in base):.2f} W. The higher-drive divider draws {min(x['pa_plus_mA'] for x in boost):.1f}–{max(x['pa_plus_mA'] for x in boost):.1f} mA from +15 V and {min(x['pa_minus_mA'] for x in boost):.1f}–{max(x['pa_minus_mA'] for x in boost):.1f} mA from −15 V, with {min(x['pa_heat_W'] for x in boost):.2f}–{max(x['pa_heat_W'] for x in boost):.2f} W of IC heat. The logic 5 V estimate covers the modeled pull-up currents, including their modeled capacitive load, but omits complete internal crossover and VCCA power. The logic 3.3 V result covers the two LED branches only.

The Logic RF Driver's existing input loads the clock source with approximately 14.64 pF in the existing input-timing surrogate plus R1's 10-kilohm pull-down. The ideal charge-current estimate C × 3.3 V × frequency spans 0.0066–7.01 mA, plus approximately 0.165 mA average through R1 at 50% duty. This is a clock-source load estimate, not measured Pico, Pi, or Si5351 supply current. The PA's divider and filters load U1's output, not those clock pins directly.

At 85% converter efficiency, the nominal ±15 V amplifier power alone corresponds to approximately {min(x['pa_dc_W'] for x in base)/(.85*5)*1000:.0f}–{max(x['pa_dc_W'] for x in base)/(.85*5)*1000:.0f} mA from a 5 V converter input. Add the Logic RF Driver's 5 V load and the separately powered 3.3 V circuitry. The higher-drive divider corresponds to {min(x['pa_dc_W'] for x in boost)/(.85*5)*1000:.0f}–{max(x['pa_dc_W'] for x in boost)/(.85*5)*1000:.0f} mA for the PA alone. This is an efficiency assumption; no converter is selected or simulated.

### Thermal estimate

The following temperatures use the largest nominal modeled IC dissipation, steady state, and Tj = Ta + Pd × thermal resistance. TI lists 44.5 °C/W junction-to-ambient for the DDA package on its reference test board. That value is not the thermal resistance of a new two-layer PA PCB. The other rows are illustrative cooling sensitivities. They are not a thermal simulation.

| Assumed junction-to-ambient (°C/W) | Junction at 25 °C ambient (°C) | Junction at 50 °C ambient (°C) |
| --- | ---: | ---: |
{thermal}

Using the largest higher-drive dissipation adds approximately {(max(x['pa_heat_W'] for x in boost)-max(x['pa_heat_W'] for x in base))*44.5:.0f} °C to the 44.5 °C/W reference-board estimate. These figures do not include unmodeled high-frequency internal loss.

The exposed pad needs a properly soldered ground connection, thermal vias, and adequate copper or a heatsink. Temperatures must be checked on the actual assembly. The electrical model remains at 25 °C; the thermal estimate is not fed back into its output response.

## Numerical validation and scope

The [result record](docs/ths3491-results.json) contains {len(rows)} cases, source/model hashes, and settling checks. Ngspice runs the unencrypted TI DDA model in PSpice compatibility mode with its native XSPICE code models. The signal model is unmodified; the supply-loading correction is explicit. Gear integration uses reltol 0.0001 and abstol 1e-12. Every case runs 60 periods and measures the final eight. The three searched capacitor states change by less than 50 µV over the final 20 periods, and successive four-period power windows differ by less than 0.1%.

Four endpoint checks halve the maximum timestep. The largest power change is {max(abs(x['fundamental_power_change_percent']) for x in checks):.4g}%, and the largest heat change is {max(abs(x['heat_change_percent']) for x in checks):.4g}%. These checks assess numerical consistency; they do not validate the device or filter models. The macro-model does not claim accurate harmonic distortion, temperature behavior, manufacturing corners, or an extracted PCB response.

The candidate PA is absent from the schematic, PCB, and BOM. The study makes no CAD changes. The [Logic RF Driver model scope](MODEL-SCOPE.md) and [board circuit study](BOARD-SIMULATION.md) describe the source-stage limitations.

## Reproduction

Run `scripts/simulate_ths3491.py` with `--research`, `--output`, and `--board-runs`, then run `scripts/report_ths3491.py` with `--research` and `--runs`. The output directory requires the unmodified TI `THS3491DDA.lib` under `models/`. Board runs require the retained detector-loaded source decks and their Samsung C4 fits. The external research directory supplies the ngspice helper and Python dependencies used by the existing project studies. These retained inputs are required; this is not a self-contained simulator installation. Vendor model text and raw runs remain in ignored `generated/` storage.
'''
text+='\nThe [dual-chip load-sharing study](THS3491-DUAL-STUDY.md) evaluates TI\'s parallel RGT arrangement with inductor-first input and output filters, including a matched single-RGT control and the published output-resistor networks.\n'
(p/'THS3491-STUDY.md').write_text(text)
print(json.dumps({'cases':len(rows),'nominal_power_mW':[min(x['fundamental_output_mW'] for x in base),max(x['fundamental_output_mW'] for x in base)],'boost_power_mW':[min(x['fundamental_output_mW'] for x in boost),max(x['fundamental_output_mW'] for x in boost)],'max_timestep_power_difference_percent':max(abs(x['fundamental_power_change_percent']) for x in checks)},indent=2))
