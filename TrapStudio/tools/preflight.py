"""Check the active sandbox, including one real Hindi inference."""
from pathlib import Path
from ctypes.util import find_library
import shutil,subprocess,tempfile
import numpy as np, onnxruntime as ort, cairocffi
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1]
def main():
    for exe in ['ffmpeg','ffprobe']:
        if not shutil.which(exe):raise SystemExit(f'Missing {exe}. Run bash bootstrap.sh.')
    enc=subprocess.check_output(['ffmpeg','-hide_banner','-encoders'],stderr=subprocess.STDOUT,text=True)
    if 'libx264' not in enc or ' aac ' not in enc:raise SystemExit('FFmpeg needs libx264 and AAC encoders.')
    if not find_library('fontconfig'):raise SystemExit('Missing fontconfig')
    op=ort.SessionOptions();op.intra_op_num_threads=2;op.inter_op_num_threads=1
    sess=ort.InferenceSession(str(ROOT/'models/kokoro-v1.0.int8.onnx'),sess_options=op,providers=['CPUExecutionProvider'])
    engine=Kokoro.from_session(sess,str(ROOT/'models/hindi-voices.bin'))
    a,sr=engine.create('मेवा कहाँ है?',voice='hf_beta',lang='hi',speed=1.)
    if sr!=24000 or len(a)<5000 or not np.isfinite(a).all() or np.max(abs(a))<.01:raise RuntimeError('Kokoro smoke test failed')
    print(f'Voice test passed: hf_beta Hindi, {len(a)/sr:.2f}s at {sr} Hz. Cairo {cairocffi.cairo_version_string()}. FFmpeg H.264/AAC available.')
if __name__=='__main__':main()
