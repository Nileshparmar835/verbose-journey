"""Render with Cairo + FFmpeg. Use --preview 4 for a quick motion test."""
import argparse,json,math,subprocess,os
from pathlib import Path
from bisect import bisect_right
from functools import lru_cache
import numpy as np
from direct import *
ROOT=Path(__file__).resolve().parents[1]
FPS=30
@lru_cache(4)
def noise_tile():
    rng=np.random.default_rng(311)
    a=rng.integers(0,14,(160,160),dtype=np.uint8)
    return cairo.ImageSurface.create_for_data(a,cairo.FORMAT_A8,160,160,160)
def film(c):
    c.save()
    mask=cairo.SurfacePattern(noise_tile());mask.set_extend(cairo.EXTEND_REPEAT);mask.set_filter(cairo.FILTER_NEAREST)
    c.set_source_rgba(.15,.1,.2,.85);c.mask(mask)
    v=cairo.RadialGradient(168,294,66,180,320,395)
    v.add_color_stop_rgba(0,0,0,0,0);v.add_color_stop_rgba(.65,.10,.07,.14,.03);v.add_color_stop_rgba(1,.09,.08,.16,.37)
    rect(c,0,0,360,640,v);c.restore()

def draw(c,t,tl,starts,ids):
    i=max(0,bisect_right(starts,t)-1);s=tl[i];sid=s['id'];dt=t-s['start'];p=clamp(dt/(s['end']-s['start']));cue=s['cue']-s['start']
    scale,cx,cy=SHOTS[sid];scale*=1+.028*ease(p)
    c.set_line_join(cairo.LINE_JOIN_ROUND);c.set_line_cap(cairo.LINE_CAP_ROUND)
    with transform(c,180,414,scale):
        c.translate(-cx,-cy)
        if sid in CINEMA:cinema(c,s,t,dt,p,cue)
        else:orchard(c,s,ids,t,dt,p,cue)
    film(c)
    mark=next((m for m in s['words'] if m['start']-.015<=t<m['end']+.045),None)
    if mark:
        highlight=abs(mark['start']-s['cue'])<.001 and sid in {'why','proof','name','choice','deeper','paid','return'}
        word=mark['text']
        sz=13.2 if not highlight else 14
        pop=ease((t-mark['start']+.02)/.08)
        label(c,word,180,177+(1-pop)*1.5,sz,'#ffb18d' if highlight else '#fff7e9',shadow=True)

def register_fonts():
    import ctypes
    from ctypes.util import find_library
    fc=ctypes.CDLL(find_library('fontconfig'))
    fc.FcConfigGetCurrent.restype=ctypes.c_void_p
    fc.FcConfigAppFontAddFile.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
    config=fc.FcConfigGetCurrent()
    for font in (ROOT/'assets/fonts').glob('*.ttf'):
        if not fc.FcConfigAppFontAddFile(config,os.fsencode(font)):
            raise RuntimeError(f'Font registration failed: {font.name}')

def main():
    register_fonts()
    parser=argparse.ArgumentParser();parser.add_argument('--width',type=int,default=720);parser.add_argument('--preview',type=float);parser.add_argument('--out',type=Path);parser.add_argument('--still',type=float);a=parser.parse_args()
    if a.width<=0 or a.width%18:parser.error('width must be a positive multiple of 18 for 9:16 yuv420p')
    tl=json.loads((ROOT/'episode/timeline.json').read_text());starts=[s['start'] for s in tl];ids=[s['id'] for s in tl]
    w=a.width;h=w*16//9
    out=a.out or ROOT/'output/The_Empty_Hole.mp4';out.parent.mkdir(parents=True,exist_ok=True)
    surf=cairo.ImageSurface(cairo.FORMAT_RGB24,w,h)
    def frame(t):
        c=cairo.Context(surf);c.scale(w/360,h/640);draw(c,t,tl,starts,ids);surf.flush()
    if a.still is not None:
        frame(a.still);surf.write_to_png(str(out));return
    length=min(a.preview or tl[-1]['end'],tl[-1]['end']);n=math.ceil(length*FPS)
    proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr0','-s',f'{w}x{h}','-r',str(FPS),'-i','pipe:0','-i',str(ROOT/'audio/mix.wav'),'-map','0:v:0','-map','1:a:0','-t',f'{n/FPS:.6f}','-c:v','libx264','-threads','3','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
    try:
        for k in range(n):
            frame(k/FPS);proc.stdin.write(surf.get_data())
            if k%600==0:print(f'{k}/{n}',flush=True)
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg encode failed')
if __name__=='__main__':main()
