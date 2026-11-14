#!/usr/bin/env python3
"""Render the proposed transformer study; does not open or edit KiCad files."""
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT/'calculations.json').read_text())
A, B = D['cores'][:2]
OUT = ROOT/'output/pdf/bifilar-transformer-study.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
C = canvas.Canvas(str(OUT), pagesize=(612,792))
C.setTitle('WsprryPico GPIO Shield with GPS - Torroid Edition - bifilar schematic design')
C.setAuthor('WsprryPi PCB Designs engineering study')
BLUE=colors.HexColor('#144d71'); INK=colors.HexColor('#172b3a'); GRAY=colors.HexColor('#52626d')
STYLE=ParagraphStyle('body', fontName='Helvetica',fontSize=10,leading=14,textColor=INK)
SMALL=ParagraphStyle('small',parent=STYLE,fontSize=8.5,leading=11)

def page(number,title):
    C.setFillColor(BLUE); C.rect(0,750,612,42,fill=1,stroke=0)
    C.setFillColor(colors.white); C.setFont('Helvetica-Bold',11)
    C.drawString(36,766,'WsprryPico GPIO Shield with GPS - Torroid Edition')
    C.setFillColor(INK); C.setFont('Helvetica-Bold',19); C.drawString(36,715,title)
    C.setFillColor(GRAY); C.setFont('Helvetica',8)
    C.drawString(36,28,'2026-10-20 | Transformer circuit routed on main PCB; physical/RF tests pending')
    C.drawRightString(576,28,f'{number} / 3')

def para(text,y,x=36,width=540,small=False,gap=10):
    p=Paragraph(text,SMALL if small else STYLE); _,h=p.wrap(width,700)
    p.drawOn(C,x,y-h); return y-h-gap

def heading(text,y):
    C.setFillColor(BLUE); C.setFont('Helvetica-Bold',11); C.drawString(36,y,text); return y-14

def table(rows,y,widths):
    data=[[Paragraph(str(v),SMALL) for v in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eff4')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.8,BLUE),
        ('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#cbd6dd'))]))
    _,h=t.wrap(540,700); t.drawOn(C,36,y-h); return y-h-12

def label(text,x,y,size=9,bold=False,color=INK):
    C.setFillColor(color);C.setFont('Helvetica-Bold' if bold else 'Helvetica',size);C.drawString(x,y,text)

def line(x1,y1,x2,y2):
    C.setStrokeColor(INK);C.setLineWidth(1.4);C.line(x1,y1,x2,y2)

def dot(x,y,r=3):
    C.setFillColor(INK);C.circle(x,y,r,fill=1,stroke=0)

def ground(x,y):
    line(x,y,x,y-6)
    for dy,w in [(6,12),(10,8),(14,4)]:line(x-w/2,y-dy,x+w/2,y-dy)

def vcap(x,y):
    line(x,y+15,x,y+3);line(x-8,y+3,x+8,y+3)
    line(x-8,y-3,x+8,y-3);line(x,y-3,x,y-17)

def coil(x,top):
    line(x,top,x,top-8)
    p=C.beginPath();p.moveTo(x,top-8)
    for k in range(4):
        yy=top-8-16*k
        p.curveTo(x+15,yy,x+15,yy-16,x,yy-16)
    C.drawPath(p,stroke=1,fill=0);line(x,top-72,x,top-84)

page(1,'Bifilar transformer: schematic design')
y=para('<b>Selected prototype:</b> coated Fair-Rite 5977000621, type 77, with 15 bifilar turns '
       '(15 turns in each wire). Compare against type 43 Fair-Rite 5943000621 with 24 bifilar turns. '
       'This is a 1:2 voltage / 1:4 impedance autotransformer for a 50-ohm external LPF/load. '
       'Design screening covers 135.7 kHz through 29.7 MHz.',690)
y=table([
 ['Parameter','Type 77 - first prototype','Type 43 - comparison'],
 ['Exact core','5977000621 (coated)','5943000621'],
 ['Core exterior, OD / ID / height','21.85 max / 12.4 min / 7.1 max mm','21.85 max / 12.4 min / 7.1 max mm'],
 ['AL and turns per wire','1270 nH/turn2 +25/-30%; 15 turns','470 nH/turn2 +20/-25%; 24 turns'],
 ['Primary L, nominal / AL minimum',f"{A['l_nominal_h']*1e6:.2f} / {A['l_al_minimum_h']*1e6:.2f} uH",f"{B['l_nominal_h']*1e6:.1f} / {B['l_al_minimum_h']*1e6:.1f} uH"],
 ['Primary XL at 135.7 kHz, nominal',f"{A['x_low_nominal_ohm']:.1f} ohms",f"{B['x_low_nominal_ohm']:.1f} ohms"],
 ['50% retention of AL-minimum L',f"{A['l_assumed_50pct_retained_h']*1e6:.1f} uH; XL {A['x_low_scenario_ohm']:.1f} ohms",f"{B['l_assumed_50pct_retained_h']*1e6:.1f} uH; XL {B['x_low_scenario_ohm']:.1f} ohms"],
 ['DC H at 200 / 300 mA',f"{A['hdc_200ma_oe']:.3f} / {A['hdc_300ma_oe']:.3f} Oe",f"{B['hdc_200ma_oe']:.3f} / {B['hdc_300ma_oe']:.3f} Oe"],
 ['Peak RF flux at 0.5 W sine output',f"{A['ac_flux_500mw_sine_peak_t']*1e3:.2f} mT",f"{B['ac_flux_500mw_sine_peak_t']*1e3:.2f} mT"],
 ['Estimated twisted-pair axis length',f"About {A['estimated_pair_length_m']:.2f} m, including ends",f"About {B['estimated_pair_length_m']:.2f} m, including ends"],
 ],y,[178,181,181])
y=para('L = AL x N2; XL = 2 pi f L; Hdc = N Idc / le. Flux uses 0.5 W into 50 ohms, '
       '2.5 Vrms at the drain-side winding, and Bpk = Vrms / (4.44 f N Ae). The power value is '
       'a calculation scenario, not a measured output rating. The 50% retention row is an explicit '
       'engineering reserve assumption; it is not a manufacturer guarantee.',y,small=True)
y=para('The reflected fundamental load is 50 / 4 = <b>12.5 ohms</b>. Even the 100 uH scenario '
       'has about six times that reactance at the LF edge. A 20-24 turn type 77 winding is '
       'therefore unnecessary as the first transformer trial. Type 77 allows fewer turns and '
       'less DC magnetizing field; type 43 provides the HF comparison supported by the QRP Labs topology.',y)
y=para('<b>Material choice:</b> Fair-Rite recommends high permeability at the lower cutoff for '
       'broadband transformers, with tight or bifilar coupling and minimum practical turns. Its '
       '100 kHz inductive-application description for material 77 is not an absolute upper cutoff '
       'for a transmission-line transformer. DC bias and HF parasitics still require measurement. [1-4]',y)
assert y>43, y
C.showPage()

page(2,'Connections, phasing and circuit changes')
para('Two equal wires A and B are twisted together and wound in the same direction. '
     'The dots identify the two starts. Join <b>A finish to B start</b> at the drain; '
     'the two windings then add toward the output.',690)

# A single series-aiding winding stack makes the supply / tap / RF end explicit.
C.saveState(); C.transform(1,0,0,0.90,0,61.4)
label('AMP_5V_SW',40,626,9,True)
line(40,614,160,614);C.rect(160,607,60,14,stroke=1,fill=0);line(220,614,330,614)
label('R64 1 ohm',158,632,9,True);label('1%, >=0.25 W',153,594,8)
dot(120,614);label('TP61 (+)',99,647,8)
dot(285,614);label('TP62 (-)',264,647,8)
line(330,614,330,594);label('AMP_XFMR_FEED',340,628,9,True)
line(330,614,455,614);line(455,614,455,591);vcap(455,576);ground(455,559)
line(455,614,525,614);line(525,614,525,591);vcap(525,576);ground(525,559)
label('C62',441,540,8,True);label('100 nF',436,528,8)
label('C63',510,540,8,True);label('10 uF',507,528,8)
coil(330,594);dot(317,580,3);label('1: A start',342,585,9)
label('A: 15 turns',354,555,9,True)
label('2: A finish',342,516,9)
dot(330,510);line(330,510,180,510);line(180,510,180,477)
label('AMP_DRAIN',191,488,9,True)
coil(330,510);dot(317,496,3);label('3: B start',342,490,9)
label('B: 15 turns',354,463,9,True)
label('4: B finish',342,431,9)
line(330,426,330,405);line(330,405,428,405)
line(428,394,428,416);line(435,394,435,416);line(435,405,550,405)
label('AMP_RF_XFMR',340,390,8)
label('C64, C66-C69',385,374,9,True);label('5 x 100 nF C0G, 50 V',378,360,8)
label('J61 SMA',500,425,9,True);label('to band LPF',491,390,8);label('and 50 ohms',490,378,8)
C.rect(143,432,74,45,stroke=1,fill=0);label('Q61',163,459,10,True);label('BS170',160,444,9)
line(180,432,180,417);ground(180,417);label('S: pin 3',192,416,8)
line(90,454,143,454);label('G: pin 2',92,465,8)
label('C61 / R61',40,440,8);label('RF drive retained',40,428,8)
line(75,614,75,535);label('RV61 bias divider',40,522,8);label('stays upstream',40,510,8)
label('T61 (schematic)',150,576,11,True);label('15+15 turns on coated type 77',150,559,8)
C.restoreState()

y=table([
 ['Schematic change','Electrical purpose'],
 ['Replace L61 with T61','Pin 1 = supply start A; pin 2 = drain finish A; pin 3 = drain start B; pin 4 = RF finish B. Pins 2 and 3 join.'],
 ['Move C64 input','From AMP_DRAIN to the free transformer end AMP_RF_XFMR. Retain DC blocking before J61.'],
 ['C64, C66-C69: 500 nF','Five parallel Walsin 1206N104J500CT, 100 nF C0G, 50 V each; 2.346 ohms total at 135.7 kHz, versus 11.73 ohms for one 100 nF.'],
 ['Add R64; reassign TP62','Drain-feed branch only. TP61 stays AMP_5V_SW; TP62 moves to AMP_XFMR_FEED. 1 mV means 1 mA, with RF off.'],
 ['C63 to 10 uF; keep C62','After R64. Require at least 4.7 uF effective at 5 V; its ideal LF reactance is <=0.25 ohm. Keep the short HF bypass return.'],
 ],375,[160,380])
y=para('Keep Q61, the stocked 10 kohm RV61, R61-R63, C61/C65 and U31 for the first trial. The latest saved design removes GNSS. '
     'Restart RF-off bias near the existing approximately 3.5 mA initial target, now measured as '
     '3.5 mV across R64. Do not reuse the old 5 mV-across-L61 procedure. '
     'Clockwise on RV61 still reduces bias.',y,small=True)
assert y>43, y
C.showPage()

page(3,'Winding recipe and acceptance limits')
y=heading('Build the first comparison',685)
y=para('Use two differently identified AWG 26 enamelled copper wires, about 0.65 m each for '
       'the 15-turn prototype. Inspect the coated core for insulation damage. Twist the pair '
       'uniformly about 8-10 twists per inch (3-4 per cm), then pass the pair through the hole '
       '15 times in one layer. Each passage is one turn in each wire. Distribute around about '
       '330 degrees, leaving a 30-degree bare support gap. Dress separate 1/4 to the +Y face and common 2/3 to -Y, without another window passage. '
       'Use about 0.90 m per wire for the 24-turn comparison. Final cut lengths depend on twist lay. [5]',y)
y=para('Identify 1=A start, 2=A finish, 3=B start and 4=B finish. Join 2/3; keep 1/4 separate. '
       'With low-level RF and no DC, verify the output is approximately twice the tap voltage; '
       'a subtractive connection can cancel the output. Target twisted-pair Z0 near 25 ohms, '
       'the geometric mean of 12.5 and 50 ohms. Twist pitch alone does not establish Z0 or velocity factor. [6]',y)
y=heading('What the calculations establish',y-3)
y=para('The zero-DC, small-signal material model gives magnetizing |Z| near 2.5 kohms at 29.7 MHz '
       'for the type 77 candidate, versus about 14.9 kohms for type 43. These are material-only '
       'estimates, excluding winding capacitance, leakage and DC-dependent RF properties. '
       'They support testing type 77 through HF, but do not establish transformer insertion loss.',y)
y=para('At 0.5 W output the drain-side fundamental is 2.5 Vrms and 0.20 Arms into 12.5 ohms. '
       'Using illustrative 40-70% efficiency and 4.8 V at the feed gives 149-260 mA average '
       'supply current. At 40%, total PA dissipation is 0.75 W, already close to the BS170 '
       '25 C 0.83 W package limit before ambient derating. More power is conditional on '
       'measured efficiency and temperature; the transformer does not supply extra power. [7]',y)
y=heading('Bench gates before choosing the final winding',y-3)
y=para('1. Measure primary inductance with the other winding open at 0, 50, 100, 200 and '
       '300 mA DC through the supply winding. An initial gate is >=100 uH at 200 mA; inspect '
       'the complete curve rather than relying on this one threshold. 300 mA is a core screening '
       'point, not an approved continuous operating current for Q61.',y)
y=para('2. Sweep 0.10-50 MHz with the transformer correctly matched or renormalized to '
       '12.5/50 ohms, at representative DC bias. Initial goals: <=0.5 dB loss, <=1 dB at '
       'band edges, return loss >=15 dB with resistive termination, and no deep resonant dips '
       'from 135.7 kHz to 29.7 MHz. These are proposed acceptance targets, not measured results.',y)
y=para('A perfect 1:4 transformer between two uncorrected 50-ohm VNA ports already shows '
       'about 1.94 dB apparent S21 loss. Use proper renormalization or two transformers '
       'back-to-back; do not mistake impedance mismatch for dissipation.',y,small=True)
y=para('3. Test the actual PA at LF, MF and each HF band with its external LPF and load: '
       'power, DC current, efficiency, harmonics, drain/gate ringing and full-transmission '
       'thermal stability. Recheck Pico/Wi-Fi coexistence. Preserve the established AMP_EN/RF '
       'startup and shutdown sequence. Add damping only from observed ringing.',y)
y=heading('Primary sources and reproducibility',y-3)
links=[
 ('[1] Fair-Rite coated type 77 core: geometry, AL and material','https://fair-rite.com/product/toroids-5977000621/'),
 ('[2] Fair-Rite type 43 comparison core','https://fair-rite.com/product/toroids-5943000621/'),
 ('[3] Fair-Rite broadband transformer design, printed pp. 140-143','https://www.fair-rite.com/wp-content/uploads/2023/05/Fair-Rite_Catalog_17th_Edition.pdf#page=142'),
 ('[4] Fair-Rite material CSVs: linked from material datasheets','https://fair-rite.com/77-material-data-sheet/'),
 ('[5] QRP Labs: single-BS170, 5 V bifilar experiments and winding','https://qrp-labs.com/ultimate3/u3info/u3sbifilar.html'),
 ('[6] C. L. Ruthroff, Some Broad-Band Transformers, 1959','https://www.qsl.net/kp4md/ruthroff.pdf'),
 ('[7] onsemi BS170 datasheet, ratings and test conditions','https://www.onsemi.com/pdf/datasheet/mmbf170-d.pdf')]
for text,url in links:
    y=para(f'<link href="{url}" color="#144d71">{text}</link>',y,small=True,gap=3)
y=para('Reproduce numerical results with calculate.py; inputs and calculations.json are adjacent. '
       'SHA-256 source identities are recorded there. No circuit simulation or hardware measurement '
       'was performed. The circuit is placed and routed on the main PCB with all SMT underneath.',y,small=True)
assert y>43, y
C.save()
print(OUT)
