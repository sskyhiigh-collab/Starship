import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import re
import os,json,struct,numpy as np
import cat3ds, texsel, build_all
from cat3ds import cat,chunk,R,GDB_SEG,BIN_SEG,TEXG,TEXB
from gdb import GDB
from modelfull import load
from geom3ds import decode
MISSING=set()
def seg(rid,sg,ext):
    e=cat.get(rid)
    if e and sg in e['chunks']: return chunk(e,sg)
    p=R+f'Resources/{rid:08x}.{ext}'
    if os.path.exists(p): return open(p,'rb').read()
    MISSING.add(f'{rid:08x}.{ext}'); return None
def texinfo(rid):
    d=seg(rid,TEXG,'texturegdb')
    if d is None: return None
    g=GDB(d); n=g.hdr[3]>>8; f={}
    for o in struct.unpack_from('<%dI'%n,g.d,0x18):
        f[g.name(g.u32(o+4))]=g.u32(o+12)
    f['name']=cat.get(rid,{}).get('name'); return f
texsel.texinfo=texinfo
def tex_rgba(rid,inf):
    data=seg(rid,TEXB,'texturebin')
    return build_all.etc_decode(data,inf['Width'],inf['Height'],alpha=inf['Format']==18)
build_all.tex_rgba=tex_rgba
def parts_rid(rid):
    gd=seg(rid,GDB_SEG,'modelgdb'); bd=seg(rid,BIN_SEG,'modelbin')
    if gd is None or bd is None: return None
    gs,ms,ns=load(gd,bd); W=build_all.node_world(ns); gmat={}
    geonodes=[i for i,n in enumerate(ns) if isinstance(n.get('geometryIndces'),tuple) and len(n['geometryIndces'])>1]
    local=any(re.match(r'^sector\d+_ground$',n['Name'].lower()) for n in ns)   # Corneria city chunk: only the ground hierarchy is terrain
    def under_ground(i):
        while i<len(ns) and i!=0xffffffff:
            if 'ground' in ns[i]['Name'].lower() and ns[i].get('ParentIndex',0xffffffff)!=0xffffffff: return True
            i=ns[i].get('ParentIndex',0xffffffff)
        return False
    keep=set()
    for i in geonodes:
        if local and not under_ground(i): continue   # city template objects placed by N64 scenery
        if local and ns[i]['Name'].lower().endswith('_bases'): continue   # building pads: don't line up with the buildings, z-fight with the ground
        for g in ns[i]['geometryIndces'][1:]: gmat[g]=W[i]; keep.add(g)
    # city sectors (multi-node): the s??_ground meshes carry an unstored vertical offset; level their floor to 0
    import re as _re
    groundg=set()
    for i in geonodes:
        if _re.match(r'^s\d+[a-z]?_ground$',ns[i]['Name'].lower()): groundg|=set(ns[i]['geometryIndces'][1:])
    roadg=set()
    for i in geonodes:
        if _re.match(r'^s\d+[a-z]?_road$',ns[i]['Name'].lower()): roadg|=set(ns[i]['geometryIndces'][1:])
    yoff=0.0
    if local and groundg:
        ys=[decode(g)['pos'][:,1] for g in gs if g['gi'] in groundg and 'grass' in (ms[g['mat']].get('Name') or '').lower()]
        if ys: yoff=-float(np.median(np.concatenate(ys)))
    parts=[]
    for g in gs:
        if g['gi'] not in keep and local: continue
        m=decode(g); M=gmat.get(g['gi'],np.eye(4))
        if not np.allclose(M,np.eye(4)):
            m['pos']=(M[:3,:3]@m['pos'].T).T+M[:3,3]
            if m['nrm'] is not None: m['nrm']=(M[:3,:3]@m['nrm'].T).T
        if g['gi'] in groundg and yoff: m['pos']=m['pos']+np.array([0,yoff,0])
        if g['gi'] in roadg and local: m['pos']=m['pos']+np.array([0,1.235,0])   # city-sector roads sit 123.5 below the N64 highway (measured)
        m['node']='road' if g['gi'] in roadg else ('ground' if g['gi'] in groundg else 'other')
        mat=ms[g['mat']]; rid2,inf,t=texsel.pick_diffuse(mat)
        # 3DS: translucent only when the material doesn't write depth; TranslucencyKind alone just means "has alpha"
        effect=mat.get('DepthMask',1)==0 or (mat.get('TranslucencyKind',0) in (1,3) and any(k in (mat.get('Name') or '').lower() for k in ('crater','shadow','decal','kage')))
        mode='xlu' if effect else ('cutout' if (mat.get('AlphaTest',0) and inf is not None and inf['Format']==18) else 'opaque')
        la=bool(effect and inf is not None and inf['Format']!=18)
        m.update(_mat=mat,rid=rid2,inf=inf,mode=mode,la=la,matname=mat.get('Name'),texslots={k:v.get('ResourceID') for k,v in mat.items() if k.startswith('Texture') and isinstance(v,dict)})
        parts.append(m)
    return parts
if __name__=='__main__':
    rids=json.load(open(paths.f('ground_rids.json')))
    for n,r in sorted(rids.items()):
        ps=parts_rid(r)
        if not ps: print(n,'NOGEOM'); continue
        P=np.concatenate([p['pos'] for p in ps])
        notex=[(p['matname'],{k:f'{v:08x}' for k,v in p['texslots'].items() if v}) for p in ps if p['rid'] is None]
        print(f'{n:26s} {len(ps)}p {sum(len(p["tris"]) for p in ps):6d}t x[{P[:,0].min():8.1f},{P[:,0].max():8.1f}] y[{P[:,1].min():6.1f},{P[:,1].max():6.1f}] z[{P[:,2].min():8.1f},{P[:,2].max():8.1f}]', 'NOTEX:'+str(notex[:2]) if notex else '')
    print('missing',sorted(MISSING))
