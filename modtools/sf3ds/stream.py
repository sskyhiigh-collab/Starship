import struct,sys,os
from gdb import GDB
def node(g,o):
    w0=g.u32(o); return w0&0xff,(w0>>8)&0xffffff,g.name(g.u32(o+4))
def children(g,o):
    t,c,n=node(g,o); return [g.u32(o+12+4*i) for i in range(c)]
def tree(g,o):
    t,c,n=node(g,o)
    if t==7: return {node(g,ch)[2]+('#%d'%i if False else ''):tree(g,ch) for i,ch in enumerate(children(g,o))} if len(set(node(g,ch)[2] for ch in children(g,o)))==c else [ (node(g,ch)[2],tree(g,ch)) for ch in children(g,o)]
    if t==9: n2=g.u32(o+12); return g.d[g.b+o+16:g.b+o+16+n2-1].decode('latin1')
    return g.u32(o+12)
def load_stream(prefix):
    g=GDB(open(prefix+'.resourcestreamgdb','rb').read())
    t=tree(g,g.hdr[6])
    chunks={}
    for name,ch in t['Chunks']:
        chunks.setdefault(ch['ResourceID'],[]).append((ch['SegmentNameHash'],ch['Offset'],ch['Size']))
    return chunks
if __name__=='__main__':
    prefix,out=sys.argv[1],sys.argv[2]
    ch=load_stream(prefix); data=open(prefix+'.resourcestreambin','rb').read()
    os.makedirs(out,exist_ok=True)
    for rid,lst in ch.items():
        for seg,off,size in lst:
            open(f'{out}/{rid:08x}_{seg:08x}.bin','wb').write(data[off:off+size])
    print(len(ch),'resources')
