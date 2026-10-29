import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import struct,numpy as np
from sf64res import O2R
o=O2R(paths.SF64_O2R,'ast_')
def scan(n,acc,depth=0):
    b=o.raw(n); p=0x40+1
    while p%8: p+=1
    while p+8<=len(b):
        w0,w1=struct.unpack_from('<II',b,p); op=w0>>24; p+=8
        if op in (0x33,0x20): p+=8; continue
        if op==0x32:
            h=struct.unpack_from('<II',b,p); p+=8; v=o.vtx(o.h[(h[0]<<32)|h[1]])
            nv=(w0>>12)&0xff; off=w1//16; acc['col'].append(v['col'][off:off+nv])
        elif op==0x31:
            h=struct.unpack_from('<II',b,p); p+=8
            if depth<4: scan(o.h[(h[0]<<32)|h[1]],acc,depth+1)
        elif op==0xB7:
            if w1&0x20000: acc['set_light']=True
        elif op==0xB6:
            if w1&0x20000: acc['clr_light']=True
        elif op==0xB8: break
def litness(n):
    acc={'col':[]}; scan(n,acc)
    if acc.get('set_light'): return 'lit'
    if acc.get('clr_light'): return 'unlit'
    if not acc['col']: return 'lit'
    c=np.concatenate(acc['col'])[:,:3].astype(np.int8).astype(float)
    L=np.linalg.norm(c,axis=1)
    return 'lit' if ((L>100)&(L<140)).mean()>0.8 else 'unlit'
