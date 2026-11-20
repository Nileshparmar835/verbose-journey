"""Make natural Hindi takes and time words from the same Kokoro inference."""
import json
from pathlib import Path
import tempfile
import wave

import numpy as np
import onnxruntime as ort
from kokoro_onnx import Kokoro
from kokoro_onnx.sliding import token_edges
from duration_graph import timing_model

ROOT = Path(__file__).resolve().parents[1]
SR = 24000
# The user's selected Hindi Voice A preset applies to every line of the episode.
VOICE = 'hf_beta'
SPEED = 1.01
def clean(s):
    return s.strip('“”‘’!?,.।…')
def timestamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def take(engine,session,phrase):
    hi=phrase['hi'].split();roman=phrase['roman'].split()
    spoken=phrase['hi'].replace('।','.')
    # Contextual Hindi stress and reduced connective words are computed together.
    phones=engine.tokenizer.phonemize(spoken,'hi')
    groups=phones.split()
    if len(groups)!=len(hi) or len(hi)!=len(roman):
        raise ValueError(f"Check word mapping for {spoken!r}: {groups}")
    # A few loanwords gain an extra final vowel with the Hindi phonemizer.
    override={'फ़िल्म':'fˈɪlm','संक':'sˈʌŋk','कॉस्ट':'kˈɔːst'}
    for i,w in enumerate(hi):
        if clean(w) in override:
            punctuation=''.join(ch for ch in groups[i] if ch in ',.?!')
            groups[i]=engine.tokenizer.known(override[clean(w)]+punctuation)
    phones=' '.join(groups)
    tokens=engine.tokenizer.tokenize(phones)
    key=engine._tokens_input
    samples,durations=session.run(None,{key:np.array([[0,*tokens,0]],dtype=engine._input_dtypes[key]),'style':engine._style_for(engine.get_voice_style(VOICE),len(tokens)),'speed':np.array([SPEED],dtype=engine._input_dtypes['speed'])})
    y=samples.ravel();edges=token_edges(durations.ravel(),len(y))[1:]
    active=np.flatnonzero(abs(y)>.003)
    if not len(active):raise ValueError(f'Silent take for {spoken}')
    lo=max(0,active[0]-576);hi_sample=min(len(y),active[-1]+960)
    y=y[lo:hi_sample].copy();marks=[];idx=0
    for word,caption,p in zip(hi,roman,groups):
        last=idx+len(p)
        def seconds(i):return float(np.clip(edges[i]-lo,0,len(y)))/SR
        marks.append(dict(hi=word,text=caption,start=seconds(idx),end=seconds(last)))
        idx=last+1
    y[:96]*=np.linspace(0,1,96);y[-144:]*=np.linspace(1,0,144)
    return y,marks
def main():
    story=json.loads((ROOT/'episode/story.json').read_text())
    opts=ort.SessionOptions();opts.intra_op_num_threads=3;opts.inter_op_num_threads=1
    timeline=[];pieces=[];cursor=0
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'timed.onnx';timing_model(ROOT/'models/kokoro-v1.0.int8.onnx',p)
        session=ort.InferenceSession(str(p),sess_options=opts,providers=['CPUExecutionProvider'])
        engine=Kokoro.from_session(session,str(ROOT/'models/hindi-voices.bin'))
        for line in story:
            start=cursor;words=[]
            phrases=line.get('phrases') or [dict(hi=line['speech'],roman=line['roman'],hold=0)]
            for phrase in phrases:
                y,marks=take(engine,session,phrase)
                for m in marks:
                    words.append(dict(hi=m['hi'],text=m['text'],start=round(cursor/SR+m['start'],5),end=round(cursor/SR+m['end'],5)))
                pieces.append(y);cursor+=len(y);speech_end=cursor/SR
                hold=round(SR*phrase['hold']);pieces.append(np.zeros(hold));cursor+=hold
            pause=round(SR*line['pause']);pieces.append(np.zeros(pause));cursor+=pause
            cue=next(m['start'] for m in words if clean(m['hi'])==line['cue_word'])
            if ' '.join(m['hi'] for m in words)!=line['speech']:raise ValueError(line['id'])
            timeline.append(dict(**line,start=start/SR,speech_end=speech_end,end=cursor/SR,cue=cue,words=words))
            print(line['id'],round(cursor/SR,2),flush=True)
    audio=np.concatenate(pieces)
    # A single recording gain preserves the original relative levels.
    audio*=.86/np.abs(audio).max()
    with wave.open(str(ROOT/'audio/narration.wav'),'wb') as f:
        f.setparams((1,2,SR,0,'NONE',''));f.writeframes((audio*32767).astype('<i2').tobytes())
    (ROOT/'episode/timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2))
    for lang in ('speech','roman'):
        (ROOT/f'output/{lang}.srt').write_text('\n\n'.join(f"{i}\n{timestamp(s['start'])} --> {timestamp(s['speech_end'])}\n{s[lang]}" for i,s in enumerate(timeline,1))+'\n')
if __name__=='__main__':main()
