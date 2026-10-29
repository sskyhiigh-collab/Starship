import zipfile,struct,numpy as np
_T=[0]*256
POLY=0x42F0E1EBA9EA3693
for i in range(256):
    c=i<<56
    for _ in range(8): c=((c<<1)^POLY) if c&(1<<63) else (c<<1)
    _T[i]=c&0xFFFFFFFFFFFFFFFF
def crc64(s):
    c=0xFFFFFFFFFFFFFFFF
    for b in s.encode():
        c=(_T[((c>>56)^b)&0xff]^(c<<8))&0xFFFFFFFFFFFFFFFF
    return c
class O2R:
    def __init__(s,path,prefix=''):
        s.z=zipfile.ZipFile(path); s.names=[n for n in s.z.namelist() if n.startswith(prefix)]
        s.h={crc64(n):n for n in s.names}
    def raw(s,n): return s.z.read(n)
    def body(s,n): return s.z.read(n)[0x40:]
    def skeleton(s,n):
        b=s.body(n); cnt=struct.unpack_from('<I',b)[0]
        hs=struct.unpack_from('<%dQ'%cnt,b,4)
        limbs=[]
        names=[s.h[x] for x in hs]
        for ln in names:
            lb=s.body(ln)
            dl,tx,ty,tz,rx,ry,rz,sib,ch=struct.unpack_from('<Q3f3hQQ',lb)
            limbs.append(dict(name=ln,dl=s.h.get(dl) if dl else None,trans=(tx,ty,tz),rot=(rx,ry,rz),sib=s.h.get(sib) if sib else None,child=s.h.get(ch) if ch else None))
        idx={l['name']:i for i,l in enumerate(limbs)}
        for l in limbs:
            l['sib']=idx.get(l['sib']); l['child']=idx.get(l['child'])
        return limbs
    def anim(s,n):
        b=s.body(n); fc,lc,js=struct.unpack_from('<hhI',b); p=8
        keys=np.frombuffer(b,'<u2',js*6,p).reshape(js,6); p+=js*12
        fs=struct.unpack_from('<I',b,p)[0]; p+=4
        fd=np.frombuffer(b,'<u2',fs,p)
        return dict(frames=fc,limbs=lc,keys=keys,data=fd)
    def vtx(s,n):
        b=s.body(n); cnt=struct.unpack_from('<I',b)[0]
        a=np.frombuffer(b,np.uint8,cnt*16,4).reshape(cnt,16)
        s16=a.view('>i2') if False else a.copy().view('<i2')
        return dict(pos=s16[:,0:3].astype(float),st=s16[:,4:6].astype(float),col=a[:,12:16])
    def dl(s,n,depth=0):
        """returns list of triangles in world (limb) coords, with st"""
        b=s.raw(n)
        if b[4:8]==b'LDOX' or b[4:8]==b'XODL' or b[0x40:0x41]==b'<':
            pass
        if b.lstrip()[:1]==b'<': return s._xml_dl(b)
        p=0x40+1
        while p%8: p+=1
        vb=[None]*64; tris=[]; texs=[]
        while p+8<=len(b):
            w0,w1=struct.unpack_from('<II',b,p); op=w0>>24; p+=8
            if op==0x33: p+=8; continue
            if op==0x32:
                h=struct.unpack_from('<II',b,p); p+=8; hh=(h[0]<<32)|h[1]
                nv=(w0>>12)&0xff; v0=((w0>>1)&0x7f)-nv
                v=s.vtx(s.h[hh]); off=w1//16
                for i in range(nv): vb[v0+i]=(v['pos'][off+i],v['st'][off+i])
            elif op==0x31:
                h=struct.unpack_from('<II',b,p); p+=8; hh=(h[0]<<32)|h[1]
                tris+=s.dl(s.h[hh],depth+1)
            elif op in (0x20,):
                h=struct.unpack_from('<II',b,p); p+=8; texs.append(s.h.get((h[0]<<32)|h[1]))
            elif op==0xbf:
                a,bb,c=((w1>>16)&0xff)//2,((w1>>8)&0xff)//2,(w1&0xff)//2; tris.append((vb[a],vb[bb],vb[c]))
            elif op==0xb1:
                a,bb,c=((w0>>16)&0xff)//2,((w0>>8)&0xff)//2,(w0&0xff)//2; tris.append((vb[a],vb[bb],vb[c]))
                a,bb,c=((w1>>16)&0xff)//2,((w1>>8)&0xff)//2,(w1&0xff)//2; tris.append((vb[a],vb[bb],vb[c]))
            elif op==0xb8: break
            elif op==0x01: print('raw G_VTX?',n)
        return tris
