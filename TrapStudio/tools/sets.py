"""Painted scenery for the two sets. All art is original vector geometry."""
from ink import *
from actors import acorn
import random

def leaf(c,x,y,s,a,fill):
    with transform(c,x,y,s,rot=a):
        path(c,'M 0 0 Q 0 -9 12 -11 Q 12 -1 0 0 Z',fill)
        line(c,[(2,-2),(8,-8)],'#432f341e',.6)

def grove(c,phase):
    rng=random.Random(122)
    palettes=[
      ('#507d86','#f8d29a','#fce4a4','#8fada1','#648a82','#416b64','#415c53','#aa845d','#5d4550'),
      ('#786a86','#ffb683','#ffdda1','#b39490','#958286','#606d70','#485a55','#af7d5f','#60424b'),
      ('#303c59','#b57c7d','#f7c8a0','#797589','#64687d','#475a68','#3c4c51','#966d59','#423948')]
    top,bot,sun,far,mid,tree,field,soil,dark=palettes[phase]
    rect(c,-400,-450,1200,1510,gradient(top,bot,-15,432))
    sx,sy=[(88,240),(79,332),(63,386)][phase]
    glow(c,sx,sy,116,sun,.5);ellipse(c,sx,sy,27,27,sun+'ee')
    for x,y in [(-24,162),(223,226),(49,298),(89,125)]:
        pathstr='M -31 0 Q -23 -3 -16 -3 Q -8 -13 0 -6 Q 12 -9 17 -3 Q 28 -3 35 0 Z'
        with transform(c,x,y,.8):path(c,pathstr,'#ffebca28')
    for k,col in enumerate([far,mid,tree]):
        base=343+k*34
        c.new_path();c.move_to(-220,700);c.line_to(-220,base)
        for x in range(-220,620,4):
            y=base+math.sin(x/72+k*2)*15+math.cos(x/41+k)*5
            c.line_to(x,y)
        c.line_to(620,700);c.close_path();finish(c,col)
        for x in range(-180,560,9+k*2):
            if rng.random()<.47:continue
            y=base+math.sin(x/72+k*2)*15+math.cos(x/41+k)*5
            sz=rng.uniform(3,9)*(1+k*.18)
            ellipse(c,x,y-3,sz,sz*(.9+rng.random()*.65),col)
    # Oak trunk, gnarly branch silhouette and leaf clusters frame the empty caption area.
    path(c,'M 343 461 C 318 420 339 345 323 294 Q 318 269 295 255 Q 270 242 245 215 Q 239 207 247 206 Q 276 229 313 241 Q 329 243 329 229 C 332 179 304 148 300 121 Q 317 141 335 163 Q 342 173 348 155 L 370 74 L 438 75 L 408 227 Q 367 327 373 396 Q 370 438 397 455 Z','#634e49',INK,2.2)
    path(c,'M 347 440 C 332 397 353 329 342 279 Q 338 261 326 249 M 347 232 Q 355 190 366 166 M 356 403 Q 350 372 362 330',None,'#a88062',2.2)
    path(c,'M 270 233 Q 236 230 213 217 Q 246 238 279 240', '#70594b',INK,1)
    for i in range(48):
        x=rng.uniform(215,435); y=rng.uniform(57,194)
        if (x-338)**2/125**2+(y-107)**2/105**2>1:continue
        r=rng.uniform(15,31);ellipse(c,x,y,r,r*.87,rng.choice(['#344e4d','#3e6058','#4b6b59','#58775f']), '#394e491e',.8)
    for i in range(86):
        x=rng.uniform(229,420);y=rng.uniform(77,198)
        if (x-330)**2/111**2+(y-110)**2/95**2<1:leaf(c,x,y,rng.uniform(.36,.9),rng.uniform(-1,1),rng.choice(['#859267','#607f63','#b4a477','#486b5b']))
    for x,y in [(246,217),(261,230),(281,236)]:
        leaf(c,x,y,1.1,2.8,'#678067');leaf(c,x,y,.85,-.43,'#8b9a6f')
    for x,y in [(250,224),(274,237)]:acorn(c,x,y,.62,-.25)
    # Grass lip and strata protect a consistent ground line for feet and falling props.
    path(c,'M -200 447 Q -65 411 53 434 Q 135 451 220 440 Q 302 427 399 439 L 599 424 L 599 950 L -200 950 Z',gradient(field,soil,424,510))
    path(c,'M -200 471 Q -48 447 54 459 Q 148 476 233 464 Q 310 448 419 461 L 600 442 L 600 950 L -200 950 Z',gradient(soil,dark,454,710))
    for i in range(240):
        x=rng.uniform(-130,515);y=rng.uniform(481,829);r=rng.uniform(.5,2.1)
        ellipse(c,x,y,r*1.7,r,rng.choice(['#281d341c','#ffe6b51c','#4b37372a']))
    for i in range(135):
        x=rng.uniform(-80,470);y=rng.uniform(437,459)+math.cos(x/51)*3
        pathstr='M 0 0 Q -1 -4 -3 -6 M 0 0 Q 0 -5 3 -8'
        with transform(c,x,y,rng.uniform(.27,.95)):path(c,pathstr,None,rng.choice(['#a1a078','#41574f','#c6b382']),1.1)
    for x,y in [(28,485),(328,508),(-20,544),(283,608)]:
        with transform(c,x,y):path(c,'M 0 0 Q 9 8 24 4 Q 38 -1 43 7 M 23 4 Q 30 9 29 14',None,'#593f493c',1.5)

def theatre(c):
    rect(c,-300,-250,1000,1250,gradient('#25263a','#71485b',0,520))
    for x in range(-180,640,17):
        rect(c,x,-40,2,515,'#d3b99d0a');line(c,[(x+5,45),(x+5,450)],'#1115252b',1)
    # Projected abstract moon landscape, border and beam.
    rect(c,18,202,162,129,'#222132',INK,2.2);rect(c,24,209,150,114,gradient('#88a8ac','#dfb988',209,323))
    ellipse(c,124,244,18,18,'#f7db9f')
    path(c,'M 24 309 L 63 275 L 88 289 L 125 266 L 174 308 L 174 323 L 24 323 Z','#647e82')
    path(c,'M 24 315 L 97 289 L 134 306 L 174 294 L 174 323 L 24 323 Z','#4e626c')
    rect(c,10,330,179,6,'#c5a48a',INK,1)
    path(c,'M -110 65 L 173 209 L 174 323 Z','#fbe2b20a')
    rect(c,264,312,76,141,'#29283a',INK,2);rect(c,270,318,62,132,gradient('#b9cca7','#fbd6a0',318,445))
    path(c,'M 270 319 L 293 325 L 293 443 L 270 449 Z','#625e65',INK,1.4)
    ellipse(c,287,386,1.3,1.3,'#dcb787')
    rect(c,280,299,39,11,'#a7c7a7',INK,.7);label(c,'EXIT',300,305,6.2,'#344b4d',True)
    rect(c,-120,454,640,390,gradient('#60444e','#252332',454,680))
    for x in range(-112,488,45):
        line(c,[(170+(x-170)*.5,456),(x,750)],'#312a3a',1)
    for y in [469,494,538,609]:line(c,[(-100,y),(510,y)],'#7b5660',1)
    for x in [23,72,121,170]: seat(c,x,421,.75)

def seat(c,x,y,s):
    with transform(c,x,y,s):
        line(c,[(-11,0),(-12,16)],INK,3);line(c,[(10,0),(9,16)],INK,3)
        path(c,'M -14 -3 L -18 -26 Q -19 -38 -8 -39 L 3 -39 Q 12 -38 12 -30 L 15 -7 Q 10 0 -14 -3 Z','#93555c',INK,1.7)
        path(c,'M -14 -24 Q -15 -34 -9 -34 L 0 -34',None,'#ba7676',1.3)
        path(c,'M -12 -6 Q 3 -10 17 -6 L 17 0 Q -2 5 -12 0 Z','#b66b69',INK,1.5)
