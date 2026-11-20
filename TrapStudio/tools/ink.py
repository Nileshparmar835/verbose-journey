"""Small Cairo drawing primitives. Design coordinates use a 360 x 640 canvas."""
import math, re
try:
    import cairo
except ImportError:
    import cairocffi as cairo
from functools import lru_cache
from contextlib import contextmanager
TAU=2*math.pi
INK='#28272d'
@lru_cache(4096)
def color(h):
    h=h.lstrip('#');h=h+'ff' if len(h)==6 else h
    return tuple(int(h[i:i+2],16)/255 for i in range(0,len(h),2))
def paint(c,col):
    if isinstance(col,str): c.set_source_rgba(*color(col))
    else:c.set_source(col)
def finish(c,fill,stroke=None,w=1.2):
    if fill:
        paint(c,fill)
        if stroke:c.fill_preserve()
        else:c.fill()
    if stroke:paint(c,stroke);c.set_line_width(w);c.stroke()
@contextmanager
def transform(c,x=0,y=0,sx=1,sy=None,rot=0):
    c.save();c.translate(x,y);c.rotate(rot);c.scale(sx,sy if sy is not None else sx)
    try:yield
    finally:c.restore()
@lru_cache(2048)
def commands(s):
    toks=re.findall(r'[MCLQZ]|-?\d+(?:\.\d+)?',s)
    n={'M':2,'L':2,'C':6,'Q':4,'Z':0}; i=0;out=[]
    while i<len(toks):
        code=toks[i];end=i+1+n[code];out.append((code,tuple(map(float,toks[i+1:end]))));i=end
    return out
def path(c,s,fill,stroke=None,w=1.2):
    c.new_path()
    for k,v in commands(s):
        if k=='M':c.move_to(*v)
        elif k=='L':c.line_to(*v)
        elif k=='C':c.curve_to(*v)
        elif k=='Q':
            x,y=c.get_current_point();a,b,e,f=v
            c.curve_to(x+(a-x)*2/3,y+(b-y)*2/3,e+(a-e)*2/3,f+(b-f)*2/3,e,f)
        else:c.close_path()
    finish(c,fill,stroke,w)
def ellipse(c,x,y,rx,ry,fill,stroke=None,w=1):
    c.new_path()
    with transform(c,x,y,max(.01,rx),max(.01,ry)):c.arc(0,0,1,0,TAU)
    finish(c,fill,stroke,w)
def rect(c,x,y,w,h,fill,stroke=None,lw=1):
    c.new_path();c.rectangle(x,y,w,h);finish(c,fill,stroke,lw)
def line(c,pts,col,w=1):
    c.new_path();c.move_to(*pts[0])
    for p in pts[1:]:c.line_to(*p)
    finish(c,None,col,w)
def gradient(a,b,y0,y1):
    g=cairo.LinearGradient(0,y0,0,y1);g.add_color_stop_rgba(0,*color(a));g.add_color_stop_rgba(1,*color(b));return g
def glow(c,x,y,r,col,alpha=.3):
    g=cairo.RadialGradient(x,y,0,x,y,r);g.add_color_stop_rgba(0,*color(col)[:3],alpha);g.add_color_stop_rgba(1,*color(col)[:3],0)
    ellipse(c,x,y,r,r,g)
def label(c,txt,x,y,sz,col='#fff8e8',mono=False,shadow=False):
    c.select_font_face('DejaVu Sans Mono' if mono else 'DejaVu Sans',cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(sz);e=c.text_extents(txt);left=x-e[0]-e[2]/2;base=y-e[1]-e[3]/2
    if shadow:
        c.move_to(left,base+.8);c.text_path(txt);finish(c,'#20202099','#31282f88',1.45)
    c.move_to(left,base);paint(c,col);c.show_text(txt)
def clamp(x):return max(0,min(1,x))
def ease(x):
    u=clamp(x);return u*u*(3-2*u)
def mix(a,b,u):return a+(b-a)*u
