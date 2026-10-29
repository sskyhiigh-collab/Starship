import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import json,numpy as np,ground
from modelfull import load
T=json.load(open(paths.f('gnd_table.json')))
from gw import level,find
R2=paths.ROMFS
def rids_for(gwname):
    root=level(R2+gwname+'.gameworldbin'); out={}
    for p,x in find(root,'NewGroundModels'):
        for k,v in (x.items() if isinstance(x,dict) else x):
            out[k]=(v if isinstance(v,dict) else dict(v))['ResourceID']
    return out
_cache={}
def is_local(r):
    gs,ms,ns=load(ground.seg(r,ground.GDB_SEG,'modelgdb'),ground.seg(r,ground.BIN_SEG,'modelbin'))
    import re as _re
    return any(_re.match(r'^sector\d+_ground$',x['Name'].lower()) for x in ns)
def placed_parts(lv,gwmod={'CORNERIA':'Corneria','MACBETH':'Macbeth','TITANIA':'Titania','AQUAS':'Aquas','VENOM_1':'VenomRes'}):
    info=T[lv]; rid=rids_for(gwmod[lv]); out=[]
    for i,row in enumerate(info['rows'],1):
        r=rid[row['name']]; ps=ground.parts_rid(r)
        ps=[p for p in ps if len(p['tris']) and p['rid'] is not None and 'shadow' not in (p['matname'] or '').lower()]
        zoff=-(info['start']+800.0+(i-1)*info['length']) if is_local(r) else 0.0
        for p in ps: p['pos']=p['pos']*100.0+np.array([0,0,zoff])
        out.append((row['name'],ps))
    return out
