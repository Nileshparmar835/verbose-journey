"""Shot-specific staging. The cue field comes from the actual voice take."""
from ink import *
from actors import *
from sets import grove,theatre,seat
from functools import lru_cache
import random
LAND=450
# Scale, focal x, focal y. Each focal point lands at (180,414).
SHOTS={
'hook':(1.46,132,411),'ignore':(1.45,158,405),'mark':(1.25,166,432),
'wind':(1.78,174,441),'guess':(1.18,159,409),'dig':(1.48,157,424),
'rain':(1.06,115,390),'look':(.98,169,414),'return':(1.72,146,405),
'bargain':(1.36,173,415),'deeper':(1.73,168,436),'push':(1.28,167,426),
'dusk':(.98,179,405),'visitor':(1.18,110,409),'shadow':(1.39,173,431),
'stay':(1.12,178,412),'why':(1.66,130,398),'proof':(1.43,173,453),
'human':(1.06,177,411),'ticket':(1.35,149,405),'paid':(1.05,185,409),
'refund':(1.5,156,405),'choice':(1.14,165,402),'name':(1,180,414),
'test':(.99,190,412),'end':(1.18,123,412)}
CINEMA={'human','ticket','paid','refund','choice','name','test'}
def marktime(s,word,default=None):
    for m in s['words']:
        if m['hi'].strip('।.,?!')==word:return m['start']-s['start']
    return s['cue']-s['start'] if default is None else default
@lru_cache(maxsize=4)
def background(key):
    scale=2
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,730*scale,980*scale)
    c=cairo.Context(surf);c.scale(scale,scale);c.translate(160,130)
    c.set_line_join(cairo.LINE_JOIN_ROUND);c.set_line_cap(cairo.LINE_CAP_ROUND)
    if key=='cinema':theatre(c)
    else:
        with transform(c,360,0,-1,1):grove(c,key)
    return surf
def display_set(c,key,alpha=1):
    with transform(c,-160,-130,.5):
        c.set_source_surface(background(key));c.paint_with_alpha(alpha)
def hole(c,stage):
    w=12+19*stage; h=2+9*stage
    ellipse(c,169,451,w+3,h+2,'#ce9d6f')
    ellipse(c,169,450,w,h,'#513a3a',INK,1)
    for k in range(1+int(4*stage)):
        x=198+k*3.2; y=450-k%2*1.3
        with transform(c,x,y,1+stage*.35):
            path(c,'M -6 0 Q -4 -4 -2 -3 Q 2 -9 5 -4 Q 8 -6 11 0 Z','#a57b59','#6d5249',.7)
def twig(c,delta=0):
    with transform(c,173,447):
        line(c,[(-8,-5),(9,3)],'#42392e',2.7);line(c,[(-7,-5),(7,2)],'#c3a175',.85)
        with transform(c,delta,0,rot=.1*delta):
            line(c,[(-8,3),(8,-5)],'#4b392e',2.4);line(c,[(4,-3),(5,-6)],'#5b4335',1)
def rock(c,x,y,angle=0):
    with transform(c,x,y,rot=angle):
        path(c,'M -11 2 L -9 -5 L -3 -9 L 7 -7 L 13 -1 L 9 4 Z','#929595',INK,1.2)
        path(c,'M -9 -4 L -3 -8 L 6 -6 L 0 -4 Z','#bdc2b1')
def sparkle(c,x,y,size):
    for k in range(5):
        a=k*TAU/5-.3
        line(c,[(x+math.cos(a)*size*.55,y+math.sin(a)*size*.55),(x+math.cos(a)*size,y+math.sin(a)*size)],'#f9e9bb',1.1)
def scatter(c,t,amount=1):
    for j in range(7):
        f=(t*1.55+j*.143)%1
        a=.7+j*.05
        x=159+(20+j*2)*f; y=444-25*math.sin(f*math.pi)*a+2*f
        r=(1-f)*amount
        if r>.08:ellipse(c,x,y,(1+j%2)*r,1.25*r,'#785640')
def fall(c,x,elapsed,offset=0):
    dist=219; u=clamp(elapsed/.52);bounce=max(0,elapsed-.52)
    y=229+dist*u*u-(math.sin(min(1,bounce/.26)*math.pi)*8 if bounce<.26 else 0)
    showx=x-11*(1-u)
    acorn(c,showx,y,.92,offset+.37*u)
    if 0<=bounce<.25:sparkle(c,showx,y,10+bounce*16)
def orchard(c,s,shots,t,local,p,cue):
    sid=s['id']; idx=shots.index(sid)
    if idx<shots.index('dusk'):phase=0
    elif idx<shots.index('why'):phase=1
    else:phase=2
    if sid in ('hook','ignore'):phase=1
    display_set(c,phase)
    if sid=='dusk':display_set(c,0,1-ease(local/2.4))
    # Wind lines, pollen, a few moving leaves. The clearing stays quiet during holds.
    for j in range(11):
        x=(j*53+t*(1.8+j%3))%405-18;y=267+math.sin(t*.28+j)*13+(j*23)%160
        ellipse(c,x,y,.65+j%2*.32,.65+j%2*.32,'#ffebbf58')
    stage=clamp((idx-2)/15)
    if sid in ('hook','ignore'):stage=.65
    hole(c,stage)
    if sid in ('mark','wind','guess'):twig(c,2.8*ease(local-cue) if sid=='wind' else 2.8 if sid=='guess' else 0)
    # Mark the opening as a glimpse ahead. Return to the same acorn on the closing beat.
    nutx=74
    if sid=='hook':fall(c,nutx,local-cue+.52)
    elif sid=='ignore':acorn(c,nutx,448,.78,.37)
    elif sid=='rain':
        # The acorn arrives on "tapka".
        fall(c,nutx,local-cue+.52)
    elif idx>shots.index('rain') and sid!='end':
        n=1
        if idx>shots.index('dusk'):n=4
        if idx>shots.index('visitor'):n=3
        if sid=='visitor' and local>marktime(s,'उठाया'):n=3
        for j in range(n):acorn(c,nutx+[0,13,23,-10][j],448+[0,-4,2,-3][j],.76,.37-j*.35)
    if sid=='dusk':
        for j in range(3):
            dt=local-cue-j*.16+.3
            if dt>0:fall(c,nutx+[13,23,-10][j],dt,j*.2)
    if sid=='end':
        pickup=marktime(s,'खाना')
        for j in range(3):
            if j==0 and local>=pickup:continue
            acorn(c,nutx+[0,13,23][j],448+[0,-4,2][j],.76,.2)
    dig=sid in ('hook','dig','deeper','push','dusk','stay')
    posx=128;posy=449
    pose='dig' if dig else 'look'
    direction=1; carrying=False
    if sid in ('return','bargain','why','proof','ignore'):pose='think'
    if sid=='look': # Looks past the pit toward food, then rocks back.
        direction=-1 if local>marktime(s,'मुड़ी')-.1 else 1
        posx-=3*math.sin(p*math.pi)
    if sid in ('deeper','push') or (idx>shots.index('push') and sid!='end'):
        if sid=='deeper' and local<cue:pass
        else:
            progress=ease((local-cue)/.72) if sid=='push' else 0 if sid=='deeper' else 1
            rock(c,168+46*progress,446-11*math.sin(progress*math.pi),progress*2.6)
    if sid=='end':
        move=marktime(s,'मुड़ी');pickup=marktime(s,'खाना');u=ease((local-move)/max(.25,pickup-move))
        direction=-1 if local>=move else 1
        posx-=35*u;posy-=abs(math.sin(u*math.pi*2))*12
        carrying=local>=pickup;pose='think' if carrying else 'look'
        if local<move:scatter(c,local,.5)
    if sid=='dig':
        worm=ease((local-cue+.15)/.26)*(1-ease((local-cue-.85)/.3))
        with transform(c,171,448,1,max(.01,worm)):
            path(c,'M 0 0 C 2 -6 -5 -9 -2 -13 Q 1 -16 3 -13',None,'#382d37',4)
            path(c,'M 0 0 C 2 -6 -5 -9 -2 -13 Q 1 -16 3 -13',None,'#d09580',2.5)
    if sid=='shadow':
        u=ease((local-cue+.4)/1.25)
        if 0<u<1:
            with transform(c,70+224*u,454,.8,.22):
                path(c,'M -25 -6 Q -12 -15 -3 -3 Q 7 -14 23 -13 Q 10 2 2 5 Q -7 7 -25 -6 Z','#302b3955')
    ellipse(c,posx,450,28,3,'#342b352f')
    squirrel(c,posx,posy,.90,t,pose,direction,.95,carrying)
    if dig:scatter(c,t,.95)
    if sid=='bargain':
        # Visualise the remembered effort: crumbs fall off the raised front paw.
        for j in range(4):
            f=(local*1.05+j/4)%1
            ellipse(c,posx+25+3*f,426+19*f*f,1.6-f,1.1-f*.4,'#6a4b3f')
    if sid=='wind':
        with transform(c,180+30*p,435-6*math.sin(p*math.pi)):
            path(c,'M -24 0 Q -13 -3 -5 0 Q 1 2 4 0',None,'#f6e5b98c',.9)
    if sid=='guess':
        u=ease((local-.2)/.55)*(1-ease((p-.87)/.13))
        if u>.01:
            with transform(c,177,362,u):
                for x,y,r in [(-18,22,2),(-14,17,3.5)]:ellipse(c,x,y,r,r,'#fff0cc',INK,.8)
                ellipse(c,0,0,30,17,'#fae9c9',INK,1.2)
                for j in range(3):acorn(c,-11+11*j,1,.65,j*.2-.2)
    if sid=='visitor':
        grab=marktime(s,'उठाया'); depart=marktime(s,'उड़');u=ease(local/max(.1,grab));v=ease((local-depart+.1)/max(.12,s['end']-s['start']-depart-.16))
        bx=mix(-30,82,u)-147*v;by=mix(345,435,u)-91*v
        with transform(c,bx,by,1 if local<depart else -1,1):bird(c,0,0,.67,t,local>=grab)
    if sid=='proof':
        # A cutaway makes the absence of buried food visible.
        u=ease(local/.7)
        with transform(c,168,450,1,max(.001,u)):
            path(c,'M -29 -1 Q -22 3 -17 30 Q -12 46 0 46 Q 14 44 20 25 Q 24 4 30 -1 Q 0 6 -29 -1 Z','#493b42','#735141',1.2)
            path(c,'M -17 12 Q -13 37 -4 40',None,'#b3856466',1.3)

def clock(c,x,y,s,minutes):
    with transform(c,x,y,s):
        ellipse(c,0,0,17,17,'#bda58a',INK,1.7);ellipse(c,0,0,14.4,14.4,'#f3e5c3','#796d68',.7)
        for j in range(12):
            a=j*TAU/12
            line(c,[(12*math.sin(a),-12*math.cos(a)),(13.4*math.sin(a),-13.4*math.cos(a))],'#777178',.8)
        for m,r,w in [(minutes,11,1.1),(minutes/12+40,7,1.6)]:
            a=m*TAU/60;line(c,[(0,0),(r*math.sin(a),-r*math.cos(a))],INK,w)
        ellipse(c,0,0,1.6,1.6,INK)
def cinema(c,s,t,local,p,cue):
    sid=s['id'];display_set(c,'cinema')
    elapsed=20
    if sid=='human':elapsed=0
    if sid=='ticket':elapsed=20*ease((local-cue+.25)/1.2)
    if sid=='choice':elapsed=20+60*ease((local-cue+.15)/1.25)
    clock(c,216,286,1,elapsed)
    # Very slight projected flicker, wall dust and rows of seats.
    rect(c,24,209,150,114,'#fbe0ab0a' if math.sin(t*11)>.3 else '#fff1ce03')
    for x in [20,73,140,202]:seat(c,x,458,1.1)
    rise=0;step=0
    if sid=='test':
        rise=ease((local-marktime(s,'मुफ़्त'))/.5);step=ease((local-marktime(s,'तो'))/max(.45,s['end']-s['start']-marktime(s,'तो')-.2))
    viewer(c,142+157*step,455-6*step,1.03,t,rise,math.sin(step*math.pi*6))
    for x in [-9,47,104,162,220]:seat(c,x,510,1.24)
    if sid=='refund' or sid=='paid' and local>=marktime(s,'टिकट'):
        u=ease(local/.35) if sid=='refund' else ease((local-marktime(s,'टिकट'))/.35)
        if u>.01:
            with transform(c,181,358,max(.02,u)):
                glow(c,0,0,41,'#ffcd87',.17);ticket(c,0,0,.82,-.12)
    if sid=='name':
        # Insert a visual analogy in the same world space.
        u=ease(local/.4)
        with transform(c,178,375,max(.01,u)):
            ellipse(c,-31,0,25,25,'#886d5e',INK,1.5);ellipse(c,-31,1,16,6,'#493b42',INK,1)
            line(c,[(-2,0),(9,0)],'#f5d6a0',1.5);ticket(c,40,0,.53,-.18)
    if sid=='refund':
        # A crease across the returned stub distinguishes a spent ticket.
        with transform(c,181,358,.82,rot=-.12):
            line(c,[(-14,-18),(-10,-6),(-15,2),(-11,16)],'#aa784a',.8)
    if sid=='human' and local<.56:
        u=ease(local/.56)
        with transform(c,166,401,1-u*.8):
            ellipse(c,0,0,26,26,'#75676b',INK,1.8)
            for j in range(5):
                a=t*3+j*TAU/5;ellipse(c,14*math.sin(a),14*math.cos(a),5,5,'#383341')
