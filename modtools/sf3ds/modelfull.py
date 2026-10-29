# full 3DS model loader: all geometries, nodes (with local matrices), materials
import struct,numpy as np
from gdb import GDB
from stream import tree,children,node
def roots(b):
    g=GDB(b); n=g.hdr[3]>>8
    return g,{g.name(g.u32(o+4)):o for o in struct.unpack_from('<%dI'%n,g.d,0x18)}
def fields(g,o):
    f={}
    for c in children(g,o):
        t,cnt,nm=node(g,c)
        if t==13: f[nm]=struct.unpack_from('<4f',g.d,c+12)
        elif t==6: f[nm]=struct.unpack_from('<12f',g.d,c+12)
        elif t==7: f[nm]=('struct',c)
        elif t==9: f[nm]=tree(g,c)
        elif t==1: 
            cnt2=g.u32(c+12); f[nm]=struct.unpack_from('<%dI'%(cnt2+1),g.d,c+16) if cnt2<1000 else ()   # (type tag, entries...)
        else: f[nm]=g.u32(c+12)
    return f
def load(gdbb,binb):
    g,r=roots(gdbb)
    geoms=[fields(g,c) for c in children(g,r['Geometries'])]
    mats=[]
    for c in children(g,r['Materials']):
        m={}
        for cc in children(g,c):
            t,cnt,nm=node(g,cc)
            if t==7: m[nm]=tree(g,cc)
            elif t==9: m[nm]=tree(g,cc)
            else: m[nm]=g.u32(cc+12)
        mats.append(m)
    nodes=[fields(g,c) for c in children(g,r['Nodes'])] if 'Nodes' in r else []
    out=[]
    for gi,f in enumerate(geoms):
        fmt=f['VertexFormat']; nv=f['VertexNum']
        if nv==0: continue
        stride=f['VertexStreamSize']//nv
        raw=np.frombuffer(binb[f['VertexStreamOffset']:f['VertexStreamOffset']+nv*stride],np.uint8).reshape(nv,stride)
        ifmt=f['IndexFormat']
        if ifmt==2: idx=np.frombuffer(binb,'<u2',f['IndexNum'],f['IndexStreamOffset']).astype(int)
        else: idx=np.frombuffer(binb,'<u1',f['IndexNum'],f['IndexStreamOffset']).astype(int)
        out.append(dict(fmt=fmt,stride=stride,raw=raw,idx=idx,prim=f['PrimitiveType'],s0=f.get('AttrScale0'),s1=f.get('AttrScale1'),s2=f.get('AttrScale2'),mat=f['MaterialIndex'],gi=gi))
    return out,mats,nodes
