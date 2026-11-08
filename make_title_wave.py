import io, math, random, sys
import numpy as np
from PIL import Image
sys.path.insert(0,'/home/claude/work')
import glyphs as g

TEXT="Chres' Castle"
SCALE=1; SHOW=3; A=2; LAM=34.0; SLOPE=3.0; N=24; DUR=100
CREAM=(233,223,184)
EARTH=[(150,118,52),(112,84,38),(176,146,70),(128,96,44)]
random.seed(7)

# ---- 1x art-pixel layer, unwarped ----
pad=3
W=sum(g.SPACE+1 if c==' ' else g.advance(c)+1 for c in TEXT)+1
H=12
fill=np.zeros((H+2*pad,W+2*pad),bool); word=np.zeros(fill.shape,np.int8)   # word 0 = Chres', 1 = Castle
x=pad; w_i=0
for c in TEXT:
    if c==' ': x+=g.SPACE+1; w_i=1; continue
    b=g.G[c]; fill[pad:pad+H,x:x+b.shape[1]]|=b; word[pad:pad+H,x:x+b.shape[1]]=w_i; x+=g.advance(c)+1
# thicken strokes to 2px so the colour reads inside the halo
thick=fill|np.roll(fill,1,1)|np.roll(fill,1,0)
word=np.where(thick&(word==0)&~fill,np.roll(word,1,1),word)
fill=thick
d=np.zeros_like(fill)
for dy in (-1,0,1):
    for dx in (-1,0,1):
        d|=np.roll(np.roll(fill,dy,0),dx,1)
outline=d&~fill
h,w=fill.shape
img=np.zeros((h,w,4),np.uint8)
img[outline]=CREAM+(255,)
cx0=[xx for xx in range(w) if (fill[:,xx]&(word[:,xx]==1)).any()]
c0,c1=min(cx0),max(cx0)
STEPS=8
for yy in range(h):
    for xx in range(w):
        if not fill[yy,xx]: continue
        row=yy-pad
        if word[yy,xx]==0:
            col=EARTH[random.randrange(len(EARTH))]
            if row>=8: col=tuple(int(v*.74) for v in col)
        else:
            t=min(STEPS-1,int((xx-c0)/(c1-c0+1)*STEPS))/(STEPS-1)
            col=tuple(int(a+(b-a)*t) for a,b in zip((176,34,66),(54,28,34)))
            if row<4: col=tuple(min(255,int(v*1.22+10)) for v in col)
        img[yy,xx]=col+(255,)

# ---- warp columns per frame ----
extra=2*A+int(SLOPE)+1
def frame(k):
    out=np.zeros((h+extra,w,4),np.uint8)
    for xx in range(w):
        off=A+int(round(A*math.sin(2*math.pi*(xx/LAM-k/N))))+int(round(SLOPE*xx/w))
        out[off:off+h,xx]=img[:,xx]
    im=Image.fromarray(out,'RGBA')
    return im.resize((w*SCALE,(h+extra)*SCALE),Image.NEAREST)

frames=[frame(k) for k in range(N)]
# ---- exact palette (no quantising) ----
cols={}
for f in frames:
    for p in set(map(tuple,np.array(f).reshape(-1,4))):
        if p[3]: cols.setdefault(p[:3],len(cols)+1)
print('colours',len(cols))
pal=[0]*768
for c,i in cols.items(): pal[i*3:i*3+3]=list(c)
gifs=[]
for f in frames:
    a=np.array(f); idx=np.zeros(a.shape[:2],np.uint8)
    for c,i in cols.items(): idx[(a[:,:,0]==c[0])&(a[:,:,1]==c[1])&(a[:,:,2]==c[2])&(a[:,:,3]>0)]=i
    p=Image.fromarray(idx,'P'); p.putpalette(pal); gifs.append(p)
buf=io.BytesIO()
gifs[0].save(buf,'GIF',save_all=True,append_images=gifs[1:],duration=DUR,loop=0,transparency=0,disposal=2,optimize=False)
data=buf.getvalue(); print('gif bytes',len(data),'size',frames[0].size)
open('/tmp/wavelogo.gif','wb').write(data)
# preview: 3 frames on header green
sheet=Image.new('RGBA',(frames[0].width*SHOW,(frames[0].height*SHOW+8)*3),(36,64,31,255))
for i,k in enumerate((0,10,21)):
    sheet.alpha_composite(frames[k].resize((frames[k].width*SHOW,frames[k].height*SHOW),Image.NEAREST),(0,i*(frames[0].height*SHOW+8)))
sheet.save('/tmp/wave_preview.png')
