import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import struct,sys,glob,os,json
from gdb import GDB
from stream import node,children
def val(g,o):
    t,c,n=node(g,o); p=g.b+o+12
    if t==7: return {('%s'%node(g,ch)[2]):val(g,ch) for ch in children(g,o)} if len(set(node(g,ch)[2] for ch in children(g,o)))==c else [(node(g,ch)[2],val(g,ch)) for ch in children(g,o)]
    if t==9: n2=g.u32(o+12); return g.d[g.b+o+16:g.b+o+16+n2-1].decode('latin1')
    if t==4: return round(struct.unpack_from('<f',g.d,p)[0],4)
    if t==6: return [round(x,4) for x in struct.unpack_from('<12f',g.d,p)]
    if t in (3,5,15): return struct.unpack_from('<I',g.d,p)[0]
    return ('t%d'%t,g.d[p:p+16].hex())
def find(v,key,path=''):
    out=[]
    if isinstance(v,dict): it=v.items()
    elif isinstance(v,list) and v and isinstance(v[0],tuple): it=v
    else: return out
    for k,x in it:
        if k==key: out.append((path+'/'+k,x))
        out+=find(x,key,path+'/'+k)
    return out
def level(path):
    d=open(path,'rb').read(); g=GDB(d); root=val(g,g.hdr[6]); return root
if __name__=='__main__':
    R=paths.ROMFS
    res={}
    for f in sorted(glob.glob(R+'*.gameworldbin')):
        nm=os.path.basename(f).split('.')[0]
        try: root=level(f)
        except Exception as e: print(nm,'ERR',e); continue
        ng=find(root,'NewGround'); gm=find(root,'NewGroundModels')
        if not ng and not gm: continue
        print('==',nm)
        for p,x in ng: print('  ',p, json.dumps(x)[:700])
        for p,x in gm: print('  models',p, list(x.keys()) if isinstance(x,dict) else [k for k,_ in x])
        res[nm]={'ground':ng[0][1] if ng else None,'models':(list(gm[0][1].keys()) if gm and isinstance(gm[0][1],dict) else [k for k,_ in gm[0][1]]) if gm else []}
    json.dump(res,open(paths.f('ground_layout.json'),'w'),indent=1)
