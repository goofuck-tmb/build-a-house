import math
C={1:(-7.23,20.73),2:(31.27,20.77),3:(37.98,0.0),4:(0.0,0.0)}
S=22; W,H=60,30
def X(x): return (x+12)*S
def Y(y): return (H-4-y)*S
def rect(x,y,w,h,fill,stroke='#333',dash='',sw=1.5):
    return f'<rect x="{X(x)}" y="{Y(y+h)}" width="{w*S}" height="{h*S}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {("stroke-dasharray=\""+dash+"\"") if dash else ""}/>'
def txt(x,y,t,size=12,anchor='middle',fill='#222',bold=False,rot=0):
    out=[]
    for i,l in enumerate(t.split('\n')):
        tr=f' transform="rotate({rot} {X(x)} {Y(y)})"' if rot else ''
        out.append(f'<text x="{X(x)}" y="{Y(y)+i*size*1.2}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{" font-weight=\"600\"" if bold else ""}{tr}>{l}</text>')
    return ''.join(out)
def dim(x1,y1,x2,y2,label,off=0.5,lx=None,ly=None):
    lx=(x1+x2)/2 if lx is None else lx; ly=(y1+y2)/2+off if ly is None else ly
    return f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="#c2410c" stroke-width="1" stroke-dasharray="4 3"/>'+txt(lx,ly,label,10,fill='#c2410c')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W*S}" height="{H*S}" font-family="Segoe UI, Arial, sans-serif" style="background:#fff">']
svg.append(rect(-14,-4,W,4,'#e9e3d6','none')); svg.append(txt(16,-2.3,'УЛИЦА — юг (узкая)',13,fill='#6b5b45',bold=True))
svg.append(f'<polygon points="{X(-14)},{Y(-4)} {X(-12.2)},{Y(21)} {X(-7.23)},{Y(21)} {X(0)},{Y(0)}" fill="#e9e3d6"/>')
svg.append(txt(-10.3,9.5,'УЛИЦА — запад (широкая, парковка)',13,fill='#6b5b45',bold=True,rot=-70))
svg.append(txt(12,23.5,'Соседний участок :621 — север',12,fill='#777'))
svg.append(txt(36.5,10,'Соседи :623 / :624 — восток',12,fill='#777',rot=-72))
pts=' '.join(f'{X(x)},{Y(y)}' for x,y in [C[4],C[3],C[2],C[1]])
svg.append(f'<polygon points="{pts}" fill="#eef5e6" stroke="#2f6b2f" stroke-width="2.5"/>')
svg.append(f'<polygon points="{X(3.3)},{Y(5)} {X(33.4)},{Y(5)} {X(29.2)},{Y(17.75)} {X(-1.2)},{Y(17.75)}" fill="none" stroke="#2f6b2f" stroke-width="1" stroke-dasharray="6 4"/>')
svg.append(txt(12,18.2,'граница застройки: 5 м от улиц, 3 м от соседей',10,fill='#2f6b2f'))
for gx in range(0,40,5):
    svg.append(f'<line x1="{X(gx)}" y1="{Y(0)}" x2="{X(gx)}" y2="{Y(21)}" stroke="#2f6b2f" stroke-opacity=".12"/>'); svg.append(txt(gx,-0.9,str(gx),9,fill='#2f6b2f'))
for gy in range(0,25,5):
    svg.append(f'<line x1="{X(-8)}" y1="{Y(gy)}" x2="{X(38)}" y2="{Y(gy)}" stroke="#2f6b2f" stroke-opacity=".12"/>')
# compass
cx,cy=42.5,16
svg.append(f'<circle cx="{X(cx)}" cy="{Y(cy)}" r="{3*S}" fill="none" stroke="#999"/>')
svg.append(txt(cx,cy+3.6,'С',13,bold=True)); svg.append(txt(cx+3.7,cy-0.3,'В',11)); svg.append(txt(cx,cy-3.8,'Ю',11)); svg.append(txt(cx-3.8,cy-0.3,'З',11))
for az,lab,col in [(315,'закат июнь','#f59e0b'),(270,'закат март/сент','#f97316'),(230,'закат декабрь','#dc2626')]:
    r=math.radians(az); ex=cx+3*math.sin(r); ey=cy+3*math.cos(r)
    svg.append(f'<line x1="{X(cx)}" y1="{Y(cy)}" x2="{X(ex)}" y2="{Y(ey)}" stroke="{col}" stroke-width="2.5"/>')
    svg.append(txt(ex-0.3,ey+(0.5 if az==315 else -0.9 if az==230 else 0.0),lab,9,anchor='end',fill=col))
# garden zone (front, west)
svg.append(f'<polygon points="{X(-1.5)},{Y(5)} {X(10)},{Y(5)} {X(10)},{Y(19)} {X(-6.5)},{Y(19)}" fill="#e3efd6" stroke="#2f6b2f" stroke-width="1.5" stroke-dasharray="6 4"/>')
svg.append(txt(3,13.5,'САД перед террасой\n≈ 12–14 × 13 м',12,fill='#2f6b2f',bold=True))
svg.append(rect(24.5,5.5,7.5,12.5,'#f4efd6','#8a6d13','6 4')); svg.append(txt(28.2,8.6,'огород /\nхоз. зона',11,fill='#8a6d13'))
objs=[
 ('terr',10.5,6.5,3,10.5,'Терраса\n3×10,5\n→ запад','#f7e7cf'),
 ('house',13.5,6.5,8,10.5,'Дом 8×10,5\n(КР, повёрнут\nна 90°)','#f1d9b5'),
 ('porch',18,5,4,1.5,'крыльцо','#f7e7cf'),
 ('carport',1.5,1,6,3.6,'Навес 6×3,6\n1 машина','#d9dde3'),
 ('septic',1,7,2,2,'Септик','#bcd7c0'),
 ('well',27,18,1.2,1.2,'','#3b82f6'),
 ('cabin',25,13,6,3,'Бытовка 6×3','#e4e4e4'),
 ('post',-6.0,19.5,0.6,0.6,'','#444'),
]
for id,x,y,w,h,label,fill in objs:
    svg.append(rect(x,y,w,h,fill))
    if label: svg.append(txt(x+w/2,y+h/2+0.3*(len(label.split('\n'))),label,11 if w>3 else 9,bold=(id=='house')))
svg.append(txt(27.6,19.7,'скважина',9,fill='#1d4ed8',bold=True))
svg.append(txt(-5.7,18.6,'столб + щит',9,anchor='start',fill='#444'))
# gate + wicket on west street, SW
svg.append(f'<line x1="{X(-0.3)}" y1="{Y(0.9)}" x2="{X(-1.6)}" y2="{Y(4.5)}" stroke="#1d4ed8" stroke-width="5"/>'); svg.append(txt(-3.4,2.2,'ворота 4 м',10,anchor='end',fill='#1d4ed8'))
svg.append(f'<line x1="{X(-1.8)}" y1="{Y(5.2)}" x2="{X(-2.2)}" y2="{Y(6.3)}" stroke="#1d4ed8" stroke-width="5"/>'); svg.append(txt(-3.2,5.6,'калитка',9,anchor='end',fill='#1d4ed8'))
# driveway stub + path
svg.append(f'<polygon points="{X(-1.0)},{Y(1.2)} {X(1.5)},{Y(1.2)} {X(1.5)},{Y(4.4)} {X(-1.6)},{Y(4.4)}" fill="#d8d3ca"/>')
svg.append(f'<polyline points="{X(-1.8)},{Y(5.7)} {X(1)},{Y(5.3)} {X(18.5)},{Y(5.3)} {X(19.5)},{Y(5.6)}" fill="none" stroke="#9ca3af" stroke-width="5" stroke-opacity=".8"/>')
svg.append(txt(9,4.4,'тропинка к крыльцу ≈ 20 м',9,fill='#555'))
# pipes
svg.append(f'<polyline points="{X(14)},{Y(7.5)} {X(3)},{Y(8)}" fill="none" stroke="#15803d" stroke-width="1.5" stroke-dasharray="3 3"/>')
svg.append(txt(8.5,8.5,'канализация ≈ 12 м',9,fill='#15803d'))
svg.append(f'<polyline points="{X(27.6)},{Y(18)} {X(27.6)},{Y(9)} {X(21.5)},{Y(9)}" fill="none" stroke="#1d4ed8" stroke-width="1.5" stroke-dasharray="3 3"/>')
svg.append(txt(29.5,11,'вода ≈ 15 м',9,fill='#1d4ed8',anchor='start'))
svg.append(f'<polyline points="{X(-5.7)},{Y(19.5)} {X(-5.7)},{Y(18.5)} {X(17)},{Y(18.5)} {X(17)},{Y(17)}" fill="none" stroke="#b45309" stroke-width="1.5" stroke-dasharray="3 3"/>')
svg.append(txt(6,19.0,'кабель от щита ≈ 25 м (по северной границе)',9,fill='#b45309'))
# dims
svg.append(dim(10.5,12,-4.2,12,'≈ 14,7 м до улицы',0.4,lx=4,ly=12.4))
svg.append(dim(21.5,10.5,32.5,10.5,'11 м до соседа',0.4,lx=27,ly=10.9))
svg.append(dim(17,17,17,20.73,'3,7 м',0.4,lx=16.1,ly=18.4))
svg.append(dim(3,8,10.5,8,'7,5 м',0.4,lx=6.8,ly=7.3))
svg.append(dim(2,9,27.6,18.6,'',0)); svg.append(txt(12,16.2,'скважина ↔ септик ≈ 27 м (норма ≥ 20)',10,fill='#c2410c'))
svg.append(dim(21.5,14.5,25,14.5,'3,5',0.4))
svg.append(dim(1.5,2.8,-0.9,2.8,'',0)); svg.append(txt(0.3,3.3,'≈ 2 м',9,fill='#c2410c'))
svg.append(txt(-3,-3.3,'Вариант D: дом по центру, заезд и навес у западных ворот, сад перед террасой, хоз. зона сзади. Масштаб: 1 клетка = 5 м',10,anchor='start',fill='#555'))
svg.append('</svg>')
open('site-plan-v4.svg','w').write(''.join(svg))
