"""Validate final encode, cue timings, and its relation to the narration stem."""
from pathlib import Path
import json,subprocess,wave,re
ROOT=Path(__file__).resolve().parents[1]
def main():
    file=ROOT/'output/The_Empty_Hole.mp4'; tl=json.loads((ROOT/'episode/timeline.json').read_text())
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert (v['codec_name'],v['pix_fmt'],v['r_frame_rate'])==('h264','yuv420p','30/1')
    assert v['width']*16==v['height']*9 and a['codec_name']=='aac'
    assert abs(float(v['duration'])-float(a['duration']))<.05
    assert len({s['id'] for s in tl})==len(tl)
    with wave.open(str(ROOT/'audio/narration.wav')) as f:duration=f.getnframes()/f.getframerate()
    assert abs(duration-tl[-1]['end'])<.001 and abs(float(v['duration'])-duration)<.05
    for i,s in enumerate(tl):
        assert abs(s['start']-(tl[i-1]['end'] if i else 0))<.001
        assert s['start']<=s['cue']<=s['speech_end']<=s['end']
        assert len(s['words'])==len(s['speech'].split())==len(s['roman'].split())
        for j,m in enumerate(s['words']):
            assert s['start']-.001<=m['start']<=m['end']<=s['speech_end']+.001
            if j:assert m['start']>=s['words'][j-1]['end']-.001
    for lang in ['speech','roman']:
        entries=(ROOT/f'output/{lang}.srt').read_text().strip().split('\n\n')
        assert len(entries)==len(tl)
        for k,e in enumerate(entries):assert e.splitlines()[-1]==tl[k][lang]
    # Decode both streams and measure loudness on the final AAC track.
    res=subprocess.run(['ffmpeg','-nostats','-hide_banner','-xerror','-i',str(file),'-af','loudnorm=I=-16:TP=-1.6:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    loud=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',res.stderr).group())
    assert -21<float(loud['input_i'])<-12 and float(loud['input_tp'])<0
    report=dict(width=v['width'],height=v['height'],fps=30,frames=int(v['nb_frames']),video_seconds=float(v['duration']),audio_seconds=float(a['duration']),codec='H.264 + AAC',voice='Kokoro v1.0 INT8 / hf_beta / hi',scenes=len(tl),timed_words=sum(len(s['words']) for s in tl),human_pivot=next(s['start'] for s in tl if s['id']=='human') if any(s['id']=='human' for s in tl) else None,lufs=float(loud['input_i']),true_peak_dbtp=float(loud['input_tp']),full_decode='passed')
    (ROOT/'docs/export-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
