from ink import *

def acorn(c,x,y,size=1,rot=0):
    with transform(c,x,y,size,rot=rot):
        path(c,'M -6 -2 C -6 4 -3 8 0 9 C 3 8 7 4 6 -2 Z','#c98a47',INK,1)
        path(c,'M 2 6 Q 6 2 4 0',None,'#f5be74',1.2)
        path(c,'M -8 -1 C -8 -9 6 -10 8 -2 Q 4 1 -8 -1 Z','#755044',INK,1.1)
        line(c,[(0,-7),(1,-11),(3,-13)],INK,1.6)
        for i in [-5,-1,3]:line(c,[(i,-4),(i+1,-5)],'#c29b73',.9)

def squirrel(c,x,y,s,t,pose='dig',face=1,activity=1,holding=False):
    # Feet are the anchor. Animate tail, torso, near/far paws and eyes separately.
    cycle=math.sin(t*8.5); active=activity if pose=='dig' else 0
    tilt=.24*active*cycle+(.78 if pose=='dig' else -.12 if pose=='think' else 0)
    with transform(c,x,y,s*face,s):
        with transform(c,-16,-22,rot=.07*math.sin(t*2.1)-tilt*.32):
            path(c,'M 7 14 C -8 24 -33 17 -38 -2 C -44 -20 -34 -26 -42 -43 C -50 -67 -38 -86 -19 -84 C -2 -84 8 -71 5 -60 C 0 -66 -7 -67 -11 -61 C -16 -54 -9 -46 -8 -38 C -5 -25 -21 -11 -8 -5 Q -2 -2 7 -4 Z','#ba5945',INK,1.8)
            path(c,'M -35 -15 C -41 -34 -35 -36 -42 -51 C -47 -66 -35 -82 -21 -81 C -28 -77 -31 -73 -31 -66 C -24 -72 -17 -73 -10 -69 C -23 -65 -25 -53 -23 -44 C -21 -35 -23 -24 -30 -18 Z','#e8a16f')
            path(c,'M -30 -27 C -22 -45 -40 -59 -21 -73',None,'#f6bf8b',1.4)
        with transform(c,0,-8,rot=tilt):
            path(c,'M -18 4 C -28 -2 -25 -23 -13 -36 C -7 -43 3 -45 11 -43 C 23 -37 24 -21 21 -7 Q 10 8 -18 4 Z','#c5754b',INK,1.8)
            path(c,'M 5 -37 C 17 -43 22 -33 22 -18 Q 21 -3 13 -2 C 6 -7 -1 -24 5 -37 Z','#f3cb98')
            path(c,'M -23 -11 C -13 -25 -4 -19 -3 -10',None,'#91513e',1.6)
            # Head, ear tufts and cheek
            with transform(c,14,-44,rot=-.23 if pose=='look' else .1*cycle*active):
                path(c,'M -15 -8 Q -22 -18 -17 -28 Q -11 -24 -8 -17 L -5 -29 Q 2 -25 3 -16 C 15 -15 17 -7 20 -4 Q 30 -2 23 5 C 16 14 0 15 -10 10 Q -18 6 -17 0 L -21 1 Z','#ce8052',INK,1.65)
                path(c,'M -15 -22 Q -14 -17 -11 -15 L -12 -20 Z','#763f3a')
                path(c,'M -4 -24 L -3 -16 L 0 -17 Z','#884d40')
                path(c,'M -4 6 Q 5 -2 17 0 Q 27 -4 24 3 Q 20 12 5 12 Z','#f8d8a7')
                blink=(t%3.1)>.0 and (t%3.1)<.12
                if blink:line(c,[(5,-7),(12,-7)],INK,2)
                else:
                    ellipse(c,9,-7,4.6,5.7,'#fff4dc',INK,1)
                    ellipse(c,10.7,-7,2.3,3.5,INK);ellipse(c,11.2,-8.5,.9,1,'#ffffff')
                line(c,[(4,-14),(11,-15 if pose!='think' else -12)],INK,1.35)
                ellipse(c,23,-1,3,2.1,INK)
                path(c,'M 18 5 Q 20 6 22 4',None,INK,.9)
                line(c,[(17,4),(28,5)],'#6b4e46',.65)
            for k in [0,1]:
                angle=(.55*math.sin(t*8.5+k*2.5)*active)+(.65 if active else -.45 if pose=='think' or holding else .14)
                with transform(c,13+k*3,-24+k*3,rot=angle):
                    path(c,'M -2 -2 Q 5 0 9 6 L 17 7 Q 21 9 17 12 L 7 11 Q 0 9 -3 4 Z','#a15b43' if k==0 else '#dc9463',INK,1.35)
                    if pose=='think' or pose=='dig':line(c,[(13,8),(18,9)],'#694a3a',2.2)
        path(c,'M -16 -4 Q -9 -9 -5 -5 L 3 -3 Q 7 -1 4 1 L -17 1 Z','#a55c44',INK,1.5)
        if holding:
            bite=.5+.5*math.sin(t*5)
            acorn(c,34,-38-8*bite,.72,-.32)
            if bite>.68:
                for j in range(3):ellipse(c,38+j*2,-40+j*3,1,.7,'#e9c88a')

def bird(c,x,y,s,t,carrying=False):
    with transform(c,x,y,s):
        path(c,'M -18 4 L -29 0 L -19 11 Q -5 17 9 8 C 20 6 20 -9 10 -10 Q 4 -12 -1 -4 Z','#43797b',INK,1.5)
        path(c,'M -14 7 Q -5 13 7 8 Q 4 13 -5 13 Z','#f2d8aa')
        with transform(c,-3,2,rot=math.sin(t*16)*.56):
            path(c,'M 0 0 Q -9 -14 -25 -15 Q -22 -3 -9 3 Q -3 5 0 0 Z','#527e81',INK,1.25)
            line(c,[(-19,-10),(-7,-2)],'#9cb6a4',1)
        path(c,'M 16 -5 L 26 -2 L 17 0 Z','#edb66c',INK,1)
        ellipse(c,12,-5,2.5,2.5,'#f5e9ce');ellipse(c,12.8,-5,1.4,1.6,INK)
        if carrying:acorn(c,22,5,.55,.22)

def ticket(c,x,y,s=1,rot=0):
    with transform(c,x,y,s,rot=rot):
        path(c,'M -48 -19 L 46 -19 L 46 -12 Q 39 -10 46 -6 L 46 1 Q 39 4 46 8 L 46 18 L -48 18 L -48 10 Q -40 7 -48 3 L -48 -4 Q -41 -7 -48 -11 Z','#edc980',INK,1.5)
        rect(c,-42,-14,68,27,None,'#9c623e',.7)
        for j in range(-15,15,5):line(c,[(31,j),(31,j+2)],'#865a43',1)
        label(c,'ADMIT ONE',-8,-8,5.2,'#704b3a',True);label(c,'₹300',-8,3.5,12,'#443239',True)
        for j in range(5):line(c,[(35+j*1.5,-6),(35+j*1.5,8)],'#75533e',.7)

def viewer(c,x,y,s,t,stand=0,walk=0):
    with transform(c,x,y,s):
        h=stand
        # Limbs unfold from a seated pose into a standing pose.
        for side in [-1,1]:
            hip=(side*6,-33-21*h);knee=(side*8+17*(1-h)+walk*side*5,-28-2*h);foot=(side*8+16*(1-h)-walk*side*9,0)
            line(c,[hip,knee,foot],INK,4);line(c,[foot,(foot[0]+6,0)],'#201f2a',4)
        with transform(c,0,-22*h,rot=.04*math.sin(t*1.6)):
            path(c,'M -12 -61 Q 0 -65 10 -60 L 15 -32 Q 0 -28 -14 -33 Z','#d59a51',INK,1.8)
            path(c,'M -10 -60 Q -3 -50 3 -60',None,'#f2cb83',2)
            line(c,[(0,-53),(1,-34)],'#9b693f',.8)
            ellipse(c,-1,-73,12.2,13.8,'#34303b',INK,1.7)
            path(c,'M -12 -80 Q -14 -91 -3 -88 Q 2 -95 8 -87 Q 16 -86 10 -80', '#34303b',INK,1.4)
            for j in [-6,3]:
                line(c,[(j,-74),(j+3,-74.6)],'#f6dec6',1.4)
            path(c,'M -3 -66 Q 1 -68 4 -66',None,'#e3c2aa',1)
            line(c,[(-9,-56),(-14,-45),(-5,-39)],INK,3.2)
            line(c,[(9,-56),(17,-46),(24,-50+5*h)],INK,3.2)
            ticket(c,25,-49+5*h,.23,-.23)
