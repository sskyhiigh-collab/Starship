# 3DS city buildings exist only as template nodes inside the Corneria terrain chunks; extract them as models.
import numpy as np, ground, texsel, build_all
from modelfull import load
from geom3ds import decode
from gen_ground_lib import rids_for
_cache={}
def find(name,gw='Corneria'):
    R=rids_for(gw)
    for sec in sorted(R):
        try: gs,ms,ns=load(ground.seg(R[sec],ground.GDB_SEG,'modelgdb'),ground.seg(R[sec],ground.BIN_SEG,'modelbin'))
        except Exception: continue
        for x in ns:
            gi=x.get('geometryIndces')
            if x['Name']==name and x.get('ParentIndex')==0 and isinstance(gi,tuple) and len(gi)>1: return gs,ms,set(gi[1:])
    raise KeyError(name)
def parts(name):
    if name in _cache: return _cache[name]
    gs,ms,keep=find(name); out=[]
    for g in gs:
        if g['gi'] not in keep: continue
        m=decode(g); mat=ms[g['mat']]; rid,inf,t=texsel.pick_diffuse(mat)
        # 3DS: translucent only when the material doesn't write depth; TranslucencyKind alone just means "has alpha"
        effect=mat.get('DepthMask',1)==0 or (mat.get('TranslucencyKind',0) in (1,3) and any(k in (mat.get('Name') or '').lower() for k in ('crater','shadow','decal','kage')))
        mode='xlu' if effect else ('cutout' if (mat.get('AlphaTest',0) and inf is not None and inf['Format']==18) else 'opaque')
        la=bool(effect and inf is not None and inf['Format']!=18)
        m.update(rid=rid,inf=inf,mode=mode,la=la,matname=mat.get('Name'))
        out.append(m)
    _cache[name]=build_all.post_parts(name,out); return _cache[name]
