from pathlib import Path
import sys,json,os,argparse
ap=argparse.ArgumentParser();ap.add_argument('--research',type=Path,required=True);ap.add_argument('--runs',type=Path,required=True);args=ap.parse_args()
p=Path(__file__).resolve().parents[1];g=args.runs.resolve()
sys.path.insert(0,str(args.research/'python-packages'))
import numpy as np
os.environ.setdefault('MPLCONFIGDIR',str(g/'matplotlib-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rows=json.loads((g/'results.json').read_text());assert len(rows)==13, len(rows)
nom=[r for r in rows if (r['line_m']==.05 or r['first']=='bare') and r['inductor_Q']==50 and r['step_divisor']==1400]
fig,axs=plt.subplots(1,3,figsize=(13,4.4))
colors={'bare':'#7c8795','L':'#1767a6','C':'#d26a24'};labels={'bare':'No filter','L':'5-element L-first','C':'7-element C-first'}
for r in nom:
 k=r['first'];d=np.load(g/(r['case']+'.npz'));t=d['t_s'];sel=t<2/10.1401e6
 axs[0].plot(t[sel]*1e9,d['load_V'][sel],label=labels[k],color=colors[k],lw=1.5)
 h=np.arange(2,10);axs[1].plot(h,[r['harmonics_dBc'][str(x)] for x in h],'o-',label=labels[k],color=colors[k])
 axs[2].bar(labels[k],r['fundamental_mW'],color=colors[k]);axs[2].text(labels[k],r['fundamental_mW']+1,f"{r['fundamental_mW']:.1f}",ha='center')
axs[0].set(xlabel='Time (ns)',ylabel='Load voltage (V)',title='Waveform into 50 Ω');axs[0].legend()
axs[1].set_ylim(-110,0)
axs[1].axhline(-43,color='red',ls=':',label='FCC HF limit');axs[1].set(xlabel='Harmonic number',ylabel='Power relative to fundamental (dBc)',title='Predicted harmonics');axs[1].legend(fontsize=8)
axs[2].set(ylabel='Fundamental power (mW)',title='Useful RF output',ylim=(0,110))
for ax in axs:ax.grid(axis='y',alpha=.2)
axs[2].tick_params(axis='x',labelsize=8)
fig.suptitle('Logic RF Driver at 10.1401 MHz — 5-element L-first versus original 7-element C-first')
fig.text(.5,.025,'3.3 V clock; two paralleled outputs at 5 V; Samsung C4, detector and LEDs. Coil Q = 50; ideal filter capacitors.\nFiltered cases: 50 mm, 50 Ω line model. Nominal model only; no PCB extraction or measured RF qualification.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.13,1,.92]);fig.savefig(p/'docs/30m-transmitter.png',dpi=170)
(p/'docs/30m-transmitter-results.json').write_text(json.dumps({'frequency_Hz':10140100,'comparison':'Five-element minimum-loss L-first versus original workbook seven-element C-first','cases':rows,'limitations':['Behavioral IBIS-derived output model; not full transistor-level or complete IBIS simulation.','Ideal supply rails; 5 V estimate excludes internal switching/crossover power. 3.3 V estimate covers LEDs only, excluding VCCA internal power and the upstream clock source.','C4 uses the retained 10 MHz Samsung bias-dependent passive fit at 10.1401 MHz.','Filter capacitors are ideal; inductor ESR assumes constant resistance set by Q at the carrier. No SRF, coupling, tolerance, or PCB extraction.','50-ohm line is a ten-section lossless LC pi ladder, velocity 1.7e8 m/s, not measured board CPWG.','Nominal 50 percent duty cycle and matched outputs; actual source duty-cycle errors and semiconductor variation are not bounded.','Even-harmonic and deep-rejection values can be limited by model/numerical precision.']},indent=2)+'\n')
lines=['# Logic RF Driver with a 30 m low-pass filter','', 'This circuit simulation drives a 50-ohm load at 10.1401 MHz with the board’s two directly paralleled outputs. The source includes the retained IBIS-derived behavioral output model, package parasitics, the Samsung C4 fit, RF detector, and both LED branches. It is a simulation of the circuit, not a physical measurement or a PCB electromagnetic extraction.','', '![Transmitter simulation](docs/30m-transmitter.png)','', '| Configuration | Fundamental | Third harmonic | Fifth harmonic | Modeled 5 V pull-up current | Channel peak |','| --- | ---: | ---: | ---: | ---: | ---: |']
for r in nom:lines += [f"| {labels[r['first']]} | {r['fundamental_mW']:.2f} mW | {r['harmonics_dBc']['3']:.2f} dBc | {r['harmonics_dBc']['5']:.2f} dBc | {r['mean_5V_pullup_mA']:.2f} mA | {max(r['channel_peak_mA']):.2f} mA |"]
lines += ['', '## Sensitivity checks', '', '| Case | Fundamental | Third harmonic |', '| --- | ---: | ---: |']
for r in rows:
 if r['first']!='bare':lines += [f"| {labels[r['first']]}; Q {r['inductor_Q']}; {r['line_m']*1000:g} mm; step T/{r['step_divisor']} | {r['fundamental_mW']:.3f} mW | {r['harmonics_dBc']['3']:.3f} dBc |"]
for first in ['L','C']:
 aa=next(r for r in nom if r['first']==first)
 bb=next(r for r in rows if r['first']==first and r['step_divisor']==2800)
 dp=abs(100*(bb['fundamental_mW']/aa['fundamental_mW']-1));dh=abs(bb['harmonics_dBc']['3']-aa['harmonics_dBc']['3'])
 assert dp<.1 and dh<.1,(first,dp,dh)
 lines += ['', f"Halving the maximum timestep changes {labels[first]} fundamental power by {dp:.5f}% and third-harmonic level by {dh:.5f} dB."]
lines+=['','The L-first filter uses the LPF-LCL minimum-loss 30/40 m targets: 1.5934 µH end inductors, a 2.2398 µH center inductor, and 325.75 pF at each shunt position. The seven-element C-first filter uses the original workbook values: 681 pF, 866 nH, 976 pF, 909 nH, 976 pF, 866 nH, and 681 pF. These are different filter orders and tuning choices: L-first is tuned to a carrier transmission maximum, while the C-first values retain the original workbook tuning. This is a comparison of the two specified designs, not an isolated test of which component comes first. Nominal coil Q is 50 at the carrier. The sensitivity cases use Q of 25 and 100, line lengths of zero and 200 mm, and half the maximum timestep. The nominal filtered cases use a 50 mm, 50-ohm lossless line represented by ten LC pi sections with a propagation velocity of 1.7 × 10^8 m/s. These line dimensions are assumptions, not a verified board stackup or external cable specification.','','The filter is connected to the buffer through C4 without a source-matching resistor. The buffer’s output impedance follows its voltage-dependent pull-up and pull-down tables; it is not replaced with a 50-ohm generator. The clock timing uses the retained 3.3 V source model with an illustrative 50-ohm source resistance. It does not identify a specific GPIO drive setting.','','## Model limits','','The modeled output-pin peak and RMS currents appear in the result record. Large C-first charging-current pulses can lie outside a useful device qualification envelope. These behavioral sources do not enforce safe current or temperature limits; a completed numerical run does not establish that the real IC can sustain the predicted waveform. The L-first result also needs output-current and temperature checks on hardware.','','The Samsung C4 network is the retained bias-dependent passive fit for 10 MHz, applied at 10.1401 MHz. Filter capacitors are ideal and coil ESR is fixed from Q at the operating frequency. Component self-resonance, mutual coupling, tolerance, mounting parasitics, connector loss, and extracted board copper are absent. Supply rails are ideal. The 5 V estimate includes modeled output pull-up current but omits internal crossover and switching current. The 3.3 V estimate covers the LEDs, excluding internal VCCA consumption and the clock-source supply.','','The nominal source has 50% duty cycle and matched channel timing. Even harmonics and very deep modeled suppression do not bound real source asymmetry, component spread, layout coupling, or instrument limitations. These results do not establish FCC compliance or continuous-duty reliability.','','## Reproduction and checks','','Run `scripts/simulate_30m_filters.py` with `--research` pointing to the external helper and model dependencies used by the board study and `--output` pointing to an ignored generated directory. The retained board-rerun source deck and Samsung fit, plus the sibling LPF-LCL minimum-loss value table, are required. Raw decks, logs, and waveforms remain under the selected generated output directory. The optional `--reuse-l-first` argument retains the unchanged L-first and bare-load results only when source-deck, C4, filter-table, schematic, and PCB hashes match; their original raw runs remain in the referenced generated directory. Run `scripts/report_30m_filters.py` with `--research` and `--runs` to render this report and graph. The [result record](docs/30m-transmitter-results.json) includes all accepted sensitivity cases. No schematic, PCB, or BOM changes are part of this study.']
(p/'30M-TRANSMITTER.md').write_text('\n'.join(lines)+'\n')
print('Rendered report with',len(rows),'cases')
