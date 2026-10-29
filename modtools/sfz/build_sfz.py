import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
# Star Fox Zero models -> Starship mod (.o2r) replacing N64 display lists.
import sys,os,json,numpy as np
sys.path.insert(0,os.path.join(paths.TOOLS,'sfz')); sys.path.insert(0,os.path.join(paths.TOOLS,'sf3ds'))
from dat import read_dat; import wmb, wtex
import build_all
U=paths.SFZ_CONTENT
# N64 display list -> Zero source: archive, meshes to keep, uniform scale, translation, translucent materials
MODELS={
 'ast_star_wolf/aStarWolfStandardShipDL': dict(dat='data000/em/em5100.dat',meshes=['Body','Glass'],scale=96.5,xlu_meshes=['Glass']),
 'ast_star_wolf/aStarWolfUpgradedShipDL': dict(dat='data000/em/em5100.dat',meshes=['Body','Glass'],scale=96.5,xlu_meshes=['Glass']),
}
TEX_MAX=1024
IMG={}; build_all.tex_rgba=lambda rid,inf: IMG[rid]
def vertex_normals(P,T):
    N=np.zeros_like(P); fn=np.cross(P[T[:,1]]-P[T[:,0]],P[T[:,2]]-P[T[:,0]])
    for k in range(3): np.add.at(N,T[:,k],fn)
    return N/np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-9)
prepared={}; cache={}
for dl,cfg in MODELS.items():
    if cfg['dat'] not in cache:
        fs=dict(read_dat(open(f"{U}/{cfg['dat']}",'rb').read()))
        base=os.path.basename(cfg['dat'])[:-4]
        cache[cfg['dat']]=(fs,base,wmb.meshes(fs[base+'.wmb']),wmb.material_textures(fs[base+'.wmb']),wtex.wta_entries(fs[base+'.wta']))
    fs,base,M,mats,W=cache[cfg['dat']]; ids=[e['id'] for e in W]
    parts=[]
    for m in M['meshes']:
        if m['name'] not in cfg['meshes']: continue
        for b in m['batches']:
            T=b['tris']; used=np.unique(T); remap=-np.ones(len(M['P']),int); remap[used]=np.arange(len(used))
            P=M['P'][used]*cfg['scale']+np.array(cfg.get('offset',(0,0,0)))
            Tl=remap[T]
            texi=next((ids.index(t) for t in mats[b['mat']] if t in ids),None)
            rid=None; inf=None
            if texi is not None:
                rid=(hash((base,texi))&0x7fffffff)|0x20000000
                if rid not in IMG:
                    img=wtex.decode(fs[base+'.wtp'],W[texi])
                    if max(img.shape[:2])>TEX_MAX:
                        from PIL import Image
                        s=max(img.shape[:2])//TEX_MAX; img=np.array(Image.fromarray(img).resize((img.shape[1]//s,img.shape[0]//s),Image.LANCZOS))
                    IMG[rid]=img
                xlu=m['name'] in cfg.get('xlu_meshes',[])
                if not xlu: IMG[rid]=IMG[rid].copy(); IMG[rid][...,3]=255
                inf={'Width':IMG[rid].shape[1],'Height':IMG[rid].shape[0],'Format':18 if xlu else 0}
            uv=M['UV'][used]
            parts.append(dict(pos=P,nrm=vertex_normals(P,Tl),col=M['C'][used],uv=np.c_[uv[:,0],1-uv[:,1]],tris=Tl,rid=rid,inf=inf,
                              mode='xlu' if m['name'] in cfg.get('xlu_meshes',[]) else 'opaque',la=False,matname=m['name']))
    prepared[dl]=parts
    print(dl,'parts',len(parts),'tris',sum(len(p['tris']) for p in parts))
build_all.model_parts=lambda k: prepared[k]
build_all.TEXDIR='ast_sfz_mdl'
out=sys.argv[1]
plan=build_all.build({k:k for k in prepared},out)
print('built',len(plan),out,os.path.getsize(out)//2**20,'MB')
