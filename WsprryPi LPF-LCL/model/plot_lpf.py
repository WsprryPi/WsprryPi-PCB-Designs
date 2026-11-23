"""Render the circuit concept and analytic response comparison; requires Pillow."""
from pathlib import Path
import argparse
import math
from PIL import Image, ImageDraw, ImageFont
from model_lpf import prototype, network

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--minimum-loss", action="store_true", help="Compare the 1 dB five-element minimum tuning")
args = parser.parse_args()
im = Image.new("RGB", (1600, 1030), "white")
d = ImageDraw.Draw(im)
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
def font(size):
    return ImageFont.truetype(FONT, size)
def text(x, y, s, size=23, color="#202b3c"):
    d.text((x, y), s, font=font(size), fill=color)
def line(points, color="#202b3c", width=3):
    d.line(points, fill=color, width=width)

text(65, 30, "Five-element L-first LPF" + (": minimum-loss tuning" if args.minimum_loss else ""), 38)
text(65, 85, "One PCB layout, populated and tuned for the chosen band. 50 ohm source and load.", 23)
xs = [220, 490, 760, 1030, 1300]
y = 205
line([(85,y),(xs[0]-65,y)])
for x in (xs[0], xs[2], xs[4]):
    points = [(x-65+i, y-21*math.sin(i*math.pi/32.5)) for i in range(131)]
    line(points)
line([(xs[0]+65,y),(xs[2]-65,y)])
line([(xs[2]+65,y),(xs[4]-65,y)])
line([(xs[4]+65,y),(1490,y)])
for x in (xs[1], xs[3]):
    d.ellipse((x-5,y-5,x+5,y+5), fill="#202b3c")
    line([(x,y),(x,252)])
    line([(x-23,252),(x+23,252)])
    line([(x-23,264),(x+23,264)])
    line([(x,264),(x,295)])
    for delta, half in ((0,23),(9,15),(18,6)):
        line([(x-half,295+delta),(x+half,295+delta)])
for x,s in zip(xs, ("L1","C2","L3","C4","L5")):
    text(x-17, 145 if s.startswith("L") else 335, s, 25)
text(75, 240, "RF IN", 22)
text(1400, 240, "RF OUT", 22)
text(65, 395, "Ideal filter attenuation", 29)
text(65, 435, ("Operating frequency f0 = 1; all curves ideal, with 50 ohm source and load." if args.minimum_loss else
              "Same passband edge; component loss, coupling, self-resonance, and PCB parasitics excluded."), 21)

colors = ["#7b8798", "#0969a2", "#c05c1e"]
curves = ([(7,1,"7 elements, edge at f0",1),(5,1,"5 elements, edge at f0",1),
           (5,1,"5 elements, minimum at f0",math.cos(math.pi/10))] if args.minimum_loss else
          [(7,1,"7 elements, 1 dB ripple",1),(5,1,"5 elements, 1 dB ripple",1),(5,.1,"5 elements, 0.1 dB ripple",1)])
for xlim, ylim, rect, title in [((0,3),(0,100),(100,555,750,900),"Passband and harmonics"),
                                 ((0,1.1),(0,5),(900,555,1530,900),"Passband detail")]:
    x0,y0,x1,y1 = rect
    def xy(x,yv):
        return x0+(x-xlim[0])/(xlim[1]-xlim[0])*(x1-x0), y1-(yv-ylim[0])/(ylim[1]-ylim[0])*(y1-y0)
    text(x0,y0-45,title,24)
    for i in range(6):
        yy = ylim[1]*i/5
        _,py = xy(0,yy)
        line([(x0,py),(x1,py)],"#dde3e9",1)
        text(x0-48,py-12,f"{yy:g}",19)
    for xx in ([0,.5,1,1.5,2,2.5,3] if xlim[1]==3 else [0,.2,.4,.6,.8,1,1.1]):
        px,_=xy(xx,0)
        line([(px,y0),(px,y1)],"#dde3e9",1)
        text(px-12,y1+12,f"{xx:g}",19)
    for (n,ripple,label,scale), color in zip(curves,colors):
        vals = [scale*(g*50 if i%2==0 else g/50) for i,g in enumerate(prototype(n,ripple))]
        pts=[]
        for i in range(1001):
            x = xlim[1]*i/1000
            loss = network(vals,"L",x/(2*math.pi))[0]
            if loss > ylim[1]:
                break
            pts.append(xy(x,max(0,loss)))
        line(pts,color,4)
    line([(x0,y0),(x0,y1),(x1,y1)],width=2)
    text(x0+100,y1+46,"Frequency / " + ("operating frequency" if args.minimum_loss else "passband edge"),21)
text(35,510,"dB",21)
text(835,510,"dB",21)
for i,((_,_,label,_),color) in enumerate(zip(curves,colors)):
    x=65+i*510
    line([(x,1000),(x+45,1000)],color,5)
    text(x+55,985,label,21)
im.save(HERE/("minimum-loss-comparison.png" if args.minimum_loss else "five-element-comparison.png"))
