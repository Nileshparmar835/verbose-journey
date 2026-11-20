"""Expose token lengths already computed in the bundled Kokoro INT8 graph."""
def varint(n):
    out=bytearray()
    while n>=128:
        out.append((n & 127)|128)
        n >>= 7
    out.append(n)
    return bytes(out)

def fields(data):
    def integer(i):
        v=0
        shift=0
        while True:
            byte=data[i];i+=1
            v|=(byte&127)<<shift
            if byte<128:return v,i
            shift+=7
    i=0
    while i<len(data):
        start=i
        tag,i=integer(i)
        wire=tag & 7
        if wire==2:
            size,i=integer(i); end=i+size
        elif wire==0:
            _,end=integer(i)
        else:
            end=i+{1:8,5:4}[wire]
        yield tag>>3,data[i:end],data[start:end]
        i=end

def message(key,data):
    return varint(key*8+2)+varint(len(data))+data

def timing_model(model_path,dest):
    # The pinned INT8 model already calculates rounded/clamped per-token lengths.
    # Promote its existing ValueInfo from graph.value_info(13) to graph.output(12)
    # in a temporary copy. The recorded voice model itself is preserved.
    data=model_path.read_bytes()
    with dest.open('wb') as result:
        for key,body,raw in fields(data):
            if key!=7:
                result.write(raw)
                continue
            info=next(value for k,value,_ in fields(body) if k==13 and
                      any(i==1 and name==b'/encoder/Clip_output_0' for i,name,_ in fields(value)))
            result.write(message(7,body+message(12,info)))

