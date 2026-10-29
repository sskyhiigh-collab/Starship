import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
# Wii U WTA/WTP (PlatinumGames) texture decoder: GX2 untile (addrlib) + BC1/BC3 decode
import struct,sys,numpy as np
sys.path.insert(0,paths.GTX)
from addrlib import addrlib
def wta_entries(wta):
    ver,n,offOff,sizeOff,flagOff,idxOff,infoOff=struct.unpack_from('>7I',wta,4)
    offs=struct.unpack_from('>%dI'%n,wta,offOff); sizes=struct.unpack_from('>%dI'%n,wta,sizeOff)
    idx=struct.unpack_from('>%dI'%n,wta,idxOff)
    out=[]
    for i in range(n):
        h=struct.unpack_from('>16I',wta,infoOff+0xc0*i)
        dim,w,hgt,depth,mips,fmt,aa,use,isz,_,msz,_,tile,swz,align,pitch=h
        out.append(dict(i=i,id=idx[i],off=offs[i],size=sizes[i],w=w,h=hgt,mips=mips,fmt=fmt,tile=tile,swz=swz,isz=isz,pitch=pitch,dim=dim,use=use))
    return out
def bc1_block(b,alpha_from_c=True):
    c0,c1,bits=struct.unpack('<HHI',b)
def decode_bc(data,w,h,fmt):
    f=fmt&0x3f; bw,bh=(w+3)//4,(h+3)//4
    bs=8 if f in (0x31,0x34) else 16
    a=np.frombuffer(data[:bw*bh*bs],np.uint8).reshape(bh*bw,bs)
    col=a[:,-8:] if bs==16 else a
    c0=col[:,0].astype(np.uint32)|(col[:,1].astype(np.uint32)<<8); c1=col[:,2].astype(np.uint32)|(col[:,3].astype(np.uint32)<<8)
    def rgb(c): return np.stack([((c>>11)&31)*255//31,((c>>5)&63)*255//63,(c&31)*255//31],-1).astype(np.int32)
    p0,p1=rgb(c0),rgb(c1)
    four=(c0>c1)|(bs==16)
    p2=np.where(four[:,None],(2*p0+p1)//3,(p0+p1)//2); p3=np.where(four[:,None],(p0+2*p1)//3,0)
    pal=np.stack([p0,p1,p2,p3],1)                       # (N,4,3)
    bits=col[:,4].astype(np.uint32)|(col[:,5].astype(np.uint32)<<8)|(col[:,6].astype(np.uint32)<<16)|(col[:,7].astype(np.uint32)<<24)
    ix=np.stack([(bits>>(2*k))&3 for k in range(16)],1)  # (N,16)
    rgbpx=np.take_along_axis(pal,ix[:,:,None].repeat(3,2),1)
    alpha=np.full((len(a),16),255,np.int32)
    if bs==8: alpha=np.where((~four[:,None])&(ix==3),0,255)
    elif f==0x33:
        a0=a[:,0].astype(np.int32); a1=a[:,1].astype(np.int32)
        ab=np.zeros(len(a),np.uint64)
        for k in range(6): ab|=a[:,2+k].astype(np.uint64)<<np.uint64(8*k)
        ai=np.stack([((ab>>np.uint64(3*k))&np.uint64(7)).astype(np.int32) for k in range(16)],1)
        tab=[a0,a1]+[np.where(a0>a1,((7-j)*a0+j*a1)//7,((5-j)*a0+j*a1)//5) for j in range(1,7)]
        tab=np.stack(tab,1); tab[:,6]=np.where(a0>a1,tab[:,6],0); tab[:,7]=np.where(a0>a1,tab[:,7],255)
        alpha=np.take_along_axis(tab,ai,1)
    px=np.concatenate([rgbpx,alpha[:,:,None]],2).reshape(bh,bw,4,4,4).transpose(0,2,1,3,4).reshape(bh*4,bw*4,4)
    return px[:h,:w].astype(np.uint8)
def decode(wtp,e):
    data=wtp[e['off']:e['off']+e['isz']]
    surf=addrlib.getSurfaceInfo(e['fmt'],e['w'],e['h'],1,e['dim'],e['tile'],0,0)
    raw=addrlib.deswizzle(e['w'],e['h'],1,e['fmt'],0,e['use'],surf.tileMode,e['swz'],surf.pitch,surf.bpp,0,0,data)
    return decode_bc(raw,e['w'],e['h'],e['fmt'])
