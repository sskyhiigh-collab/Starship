import struct,sys
class GDB:
    def __init__(s,data,base=0):
        s.d=data; s.b=base
        assert data[base:base+4]==b'GDB1',data[base:base+4]
        s.hdr=struct.unpack_from('<8I',data,base)
    def u32(s,o): return struct.unpack_from('<I',s.d,s.b+o)[0]
    def name(s,off):
        nt=s.hdr[2]
        p=s.b+nt+4+off; e=s.d.index(b'\0',p); return s.d[p:e].decode('latin1')
    def dump(s,o=None,depth=0,maxd=99,out=print,lim=[0]):
        if o is None: o=s.hdr[6]
        w0=s.u32(o); t=w0&0xff; cnt=(w0>>8)&0xffffff
        try: nm=s.name(s.u32(o+4))
        except Exception as e: nm='?%x'%s.u32(o+4)
        ind='  '*depth
        if t==7:
            out(f'{ind}{nm} {{{cnt}}} @{o:x}')
            if depth<maxd:
                for i in range(cnt): s.dump(s.u32(o+12+4*i),depth+1,maxd,out)
        elif t==9:
            n=s.u32(o+12); out(f'{ind}{nm} = "{s.d[s.b+o+16:s.b+o+16+n-1].decode("latin1")}"')
        else:
            raw=s.d[s.b+o+12:s.b+o+12+16]
            out(f'{ind}{nm} t{t} c{cnt} : {raw.hex()} @{o:x}')
if __name__=='__main__':
    d=open(sys.argv[1],'rb').read(); base=int(sys.argv[2],0) if len(sys.argv)>2 else 0
    g=GDB(d,base); print([hex(x) for x in g.hdr]); g.dump(maxd=int(sys.argv[3]) if len(sys.argv)>3 else 99)
