"""Original score and contact Foley, all synthesized, timed from the voice take."""
import wave,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
    with wave.open(str(ROOT/'audio/narration.wav')) as f:
        rate=f.getframerate();voice=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
    mix=voice.copy(); track={s['id']:s for s in json.loads((ROOT/'episode/timeline.json').read_text())};rng=np.random.default_rng(487)
    def add(at,a):
        i=max(0,round(at*rate));n=min(len(a),len(mix)-i)
        if n>0:mix[i:i+n]+=a[:n]
    def pluck(at,note,amp=.025,length=.95):
        t=np.arange(int(length*rate))/rate
        a=amp*np.minimum(1,t/.018)*np.exp(-4.6*t/length)*(np.sin(2*np.pi*note*t)+.25*np.sin(2*np.pi*note*2*t))
        add(at,a)
    for j,start in enumerate(np.arange(0,len(mix)/rate,4.8)):
        base=[146.83,130.81,164.81,110.0][j%4]
        t=np.arange(4*rate)/rate;env=np.sin(np.pi*t/4)**2
        add(start,.008*env*(np.sin(t*2*np.pi*base)+.4*np.sin(t*2*np.pi*base*1.501)))
        if j%3!=1:pluck(start+.33,base*3,.008,1.3)
    for key in ['dig','deeper','push','end','bargain']:
        t=np.arange(int(.12*rate))/rate
        n=rng.normal(0,.026,len(t));n=np.convolve(n,np.ones(5)/5,'same')*np.sin(np.pi*t/.12)**2
        add(track[key]['cue'],n)
    for key in ['rain','dusk','paid','test']:
        pluck(track[key]['cue'],[522,392,294,659][['rain','dusk','paid','test'].index(key)],.036,.32)
    pluck(track['hook']['cue'],392,.030,.31);pluck(track['end']['end']-.56,440,.03,.5)
    mix[-min(len(mix),rate//5):]*=np.linspace(1,0,min(len(mix),rate//5))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','f32le','-ar',str(rate),'-ac','1','-i','pipe:0','-af','highpass=f=65,loudnorm=I=-16:TP=-1.7:LRA=10','-ar','48000','-c:a','pcm_s16le',str(ROOT/'audio/mix.wav')],input=mix.astype('<f4').tobytes(),check=True)
if __name__=='__main__':main()
