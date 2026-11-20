"""Restore the full model when using the compact Claude starter."""
import hashlib,os,urllib.request,tempfile
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'models/kokoro-v1.0.int8.onnx'
digest='6e742170d309016e5891a994e1ce1559c702a2ccd0075e67ef7157974f6406cb'
def verify(f):
    with f.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()==digest
with (p.parent/'hindi-voices.bin').open('rb') as voice_file:
    if hashlib.file_digest(voice_file,'sha256').hexdigest()!='f9f26fb177dc97e19ec269a1f764ad9277b86372ce671a187663295dd84e900a':
        raise SystemExit('Hindi voice archive differs from the bundled release.')
if p.exists():
    if not verify(p):raise SystemExit('Existing model differs from this release. Restore the model from the full ZIP.')
else:
    url='https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx'
    with tempfile.NamedTemporaryFile(dir=p.parent,prefix='model-',delete=False) as f:tmp=Path(f.name)
    try:
        urllib.request.urlretrieve(url,tmp)
        if not verify(tmp):raise RuntimeError('Model checksum mismatch')
        os.replace(tmp,p)
    finally:tmp.unlink(missing_ok=True)
