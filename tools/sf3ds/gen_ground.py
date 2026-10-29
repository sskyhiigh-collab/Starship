import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
# Builds 3DS terrain DLs + C sector table for Starship
import json,os,sys,numpy as np
import ground, build_all, terrain_mat
from gw import level,find
R2=paths.ROMFS
def rids_for(gwname):
    root=level(R2+gwname+'.gameworldbin'); out={}
    for p,x in find(root,'NewGroundModels'):
        for k,v in (x.items() if isinstance(x,dict) else x):
            out[k]=(v if isinstance(v,dict) else dict(v))['ResourceID']
    return out
# level -> (LEVEL enum, gameworld with layout, gameworld with models, mode)
LV=[('CORNERIA','Corneria','Corneria','rails'),
    ('MACBETH','Macbeth','Macbeth','rails'),
    ('TITANIA','Titania','Titania','rails'),
    ('AQUAS','Aquas','Aquas','rails'),
    ('VENOM_1','Venom','VenomRes','rails'),
    ('VENOM_2','Venom','Venom','allrange:VenomAllRange'),
    ('TRAINING','Training','Training','allrange:CorneriaGroundBossStage')]
DLDIR='ast_sf3ds_gnd'
sectors={}   # level -> dict(params, list of sectors)
mapping={}; spec={}
for lv,lay,mod,mode in LV:
    L=find(level(R2+lay+'.gameworldbin'),'ForwardScrollGround')[0][1]
    rid=rids_for(mod)
    info=dict(start=L.get('StartOffset',0.0),length=L['SectorLength'],repeat=L.get('RepeatLastSector',0),
              hideafter=L.get('ProgressForceHideGroundAfter',0.0) if L.get('EnableForceHideGroundAfterProgress') else 0.0,secs=[])
    if mode=='rails':
        names=sorted([n for n in rid if n[-2:].isdigit()])
        for i,n in enumerate(names,1):
            spec[(lv,n)]=dict(rid=rid[n],scale=100.0,local=None)
            info['secs'].append(n)
    else:
        n=mode.split(':')[1]; spec[(lv,n)]=dict(rid=rid[n],scale=1.0); info['secs'].append(n); info['allrange']=1
    sectors[lv]=info
json.dump({k:{**v} for k,v in sectors.items()},open(paths.f('gnd_levels.json'),'w'),indent=1)
print({k:len(v['secs']) for k,v in sectors.items()})

if __name__!='__main__':
    pass
from modelfull import load
def is_local(r):
    gs,ms,ns=load(ground.seg(r,ground.GDB_SEG,'modelgdb'),ground.seg(r,ground.BIN_SEG,'modelbin'))
    import re as _re
    return any(_re.match(r'^sector\d+_ground$',x['Name'].lower()) for x in ns)
prepared={}; table={}
# sun direction per level from the N64 environment rotations (x,y degrees), as Play sets gLight1 from them
def sundir(rx,ry):
    a,b=np.radians(rx),np.radians(ry)
    v=np.array([np.sin(b),0.0,np.cos(b)])                       # RotY on (0,0,1)
    v=np.array([v[0],v[1]*np.cos(a)-v[2]*np.sin(a),v[1]*np.sin(a)+v[2]*np.cos(a)])
    if v[1]<0: v[1]=-v[1]
    return v/np.linalg.norm(v)
ENVROT={'CORNERIA':(-80,60),'MACBETH':(-106,30),'TITANIA':(-80,60),'AQUAS':(-59,58),'VENOM_1':(-80,60),'VENOM_2':(-80,60),'TRAINING':(-106,-5)}
SHADE_A,SHADE_D=0.5,0.5
LEVEL_SHADE={'AQUAS':0.55}   # overall terrain brightness per level (Aquas is underwater)
LIGHT={k:(sundir(*v),SHADE_A,SHADE_D) for k,v in ENVROT.items()}
print('sun',{k:v[0].round(2).tolist() for k,v in LIGHT.items()})
for lv,info in sectors.items():
    rows=[]; extras=[]
    for i,n in enumerate(info['secs'],1):
        sp=spec[(lv,n)]; ps=terrain_mat.parts(sp['rid'],light=LIGHT[lv],level_shade=LEVEL_SHADE.get(lv,1.0))
        ps=[p for p in ps if len(p['tris']) and (p['rid'] is not None or p.get('texpath')) and 'shadow' not in (p['matname'] or '').lower()]
        far=[]
        if ps:
            # parts far outside their chunk would stretch its bounds, so the whole chunk would be drawn far beyond the
            # camera's depth range (where it renders over everything). They become a separate chunk with their own bounds.
            main=max(ps,key=lambda p:len(p['tris'])); mz=main['pos'][:,2]*sp['scale']
            isfar=lambda p: (p['pos'][:,2]*sp['scale']).max()<mz.min()-5000 or (p['pos'][:,2]*sp['scale']).min()>mz.max()+5000
            far=[p for p in ps if isfar(p) and not p.get('wf')]; fid={id(p) for p in far}
            ps=[p for p in ps if id(p) not in fid]
            for p in far: print('separate chunk for far part',lv,n,p['matname'],len(p['tris']))
        if not ps:
            print('EMPTY',lv,n)
            if i==len(info['secs']): info['repeat']=0   # last sector was only 3DS sea: N64 water continues instead
            continue
        zoff=0.0; xoff=0.0; pofs=None
        if not info.get('allrange'):
            # SF64 3D terrain lives in object-spawn coordinates, i.e. before Scenery_Load's -3000 z offset
            zoff=-3000.0
            if is_local(sp['rid']):
                # city sectors carry no placement. Roads: fitted against the N64 highway.
                # Ground/other nodes: fitted so their edges weld to the neighbouring sectors (seam vertices match).
                ROAD={('CORNERIA',4):(-150.0,-250.0),('CORNERIA',5):(-100.0,-200.0)}
                GRND={('CORNERIA',2):(19.2,-856.9),('CORNERIA',3):(18.5,-877.5),('CORNERIA',4):(21.3,-877.6),('CORNERIA',5):(22.9,-851.4)}
                base=-(info['start']+(i-1)*info['length'])
                rd=ROAD.get((lv,i),(-125.0,-225.0)); gr=GRND.get((lv,i),rd)
                pofs=[np.array([(rd if p.get('node')=='road' else gr)[0],0,zoff+base+(rd if p.get('node')=='road' else gr)[1]]) for p in ps]
        allp=ps+far
        if pofs is None: pofs=[np.array([xoff,0,zoff])]*len(allp)
        else: pofs=pofs+[np.array([(rd if p.get('node')=='road' else gr)[0],0,zoff+base+(rd if p.get('node')=='road' else gr)[1]]) for p in far]
        groups=[('',ps,pofs[:len(ps)])]+([('_x',far,pofs[len(ps):])] if far else [])
        for suffix,ps,pofs in groups:
            W=[p['pos']*sp['scale']+po for p,po in zip(ps,pofs)]
            A=np.concatenate(W); lo=A.min(0); hi=A.max(0)
            o=np.array([(lo[0]+hi[0])/2,0.0,(lo[2]+hi[2])/2]); o=np.rint(o)
            m=np.abs(A-o).max(); f=1.0
            while m/f>30000: f*=2
            for p,w in zip(ps,W):
                p['pos']=(w-o)/f
                uv=p['uv']
                if uv is not None and np.abs(uv).max()>15:
                    t=np.asarray(p['tris']); idx=t.reshape(-1)
                    for k in ('pos','nrm','col','uv'):
                        if p.get(k) is not None: p[k]=p[k][idx]
                    tu=p['uv'].reshape(-1,3,2); tu-=np.floor(tu.min(1,keepdims=True)); p['uv']=tu.reshape(-1,2)
                    p['tris']=np.arange(len(idx)).reshape(-1,3)
            dl=f'{DLDIR}/{lv.lower()}_{i:02d}{suffix}'
            wf=[p for p in ps if p.get('wf')]; ps=[p for p in ps if not p.get('wf')]
            prepared[dl]=ps; mapping[dl]=dl
            row=dict(dl=dl,ox=float(o[0]),oz=float(o[2]),f=f,zmin=float(lo[2]),zmax=float(hi[2]),name=n+suffix)
            if wf:
                prepared[dl+'_wf']=wf; mapping[dl+'_wf']=dl+'_wf'
                row['wf']=dict(dl=dl+'_wf',parts=[list(p.get('decl') or build_all.decl_size(p['inf']['Width'],p['inf']['Height'],p['rid'])) for p in wf],speeds=[1.0 if p.get('texpath') else (1.5 if p['matname']=='mat_water' else 0.5) for p in wf])
            if suffix: extras.append(row)   # kept in front: the level's last row is the one RepeatLastSector repeats
            else: rows.append(row)
    rows=extras+rows
    table[lv]=dict(info,rows=rows)
json.dump(table,open(paths.f('gnd_table.json'),'w'),indent=1)
for ps in prepared.values():
    for p in ps:
        if p['uv'] is None: continue
        span=np.abs(p['uv']).max()+1
        if span>15: build_all.DECL_MAX[p['rid']]=min(build_all.DECL_MAX.get(p['rid'],64),int(2**np.floor(np.log2(1000/span))))
print('decl overrides',{hex(k):v for k,v in build_all.DECL_MAX.items()})
build_all.model_parts=lambda k: prepared[k]
build_all.litness=lambda dl: 'unlit'
build_all.TEXDIR='ast_sf3ds_gndtex'
# baked shade can exceed 1 (3DS combiner x2): fold the excess into the texture brightness per texture
import collections
hi=collections.defaultdict(list); flat=collections.defaultdict(list)
for ps in prepared.values():
    for p in ps:
        if p.get('rid') is None or p.get('wf'): continue
        c=p['col'][:,:3]; hi[p['rid']].append(np.percentile(c,98)); flat[p['rid']].append(np.median(c))
for r,v in hi.items(): build_all.BRIGHT[r]=float(np.clip(max(v),1.0,2.0))
for ps in prepared.values():
    for p in ps:
        if p.get('rid') in build_all.BRIGHT and not p.get('wf'): p['col'][:,:3]=np.clip(p['col'][:,:3]/build_all.BRIGHT[p['rid']],0,1)
FLATSHADE={r:float(np.median(v))/build_all.BRIGHT.get(r,1.0) for r,v in flat.items()}
print('bright',{hex(k):round(v,2) for k,v in build_all.BRIGHT.items() if v>1.01})
build_all.vanilla_alpha=lambda dl: False
plan=build_all.build(mapping,sys.argv[1] if len(sys.argv)>1 else 'out/4 SF64 3D Terrain.o2r')
print('built',len(plan))

# ---- static ground-plane tiles that replace the scrolling N64 ground under the terrain ----
FILL=json.load(open(paths.f('fill_tex.json'))); TILE=15000.0; Q=6
fillmap={}; fillprep={}
for lv,f in FILL.items():
    rid=f['rid']; inf=ground.texinfo(rid)
    # texture period in world units, measured from the terrain itself
    per=[]
    for row in table[lv]['rows'][::4]:
        for p in prepared[row['dl']]:
            if p['rid']!=rid: continue
            t=np.asarray(p['tris'])[:200]; P=p['pos'][t]*row['f']; U=p['uv'][t]
            dp=np.linalg.norm((P[:,1]-P[:,0])[:,[0,2]],axis=1); du=np.linalg.norm(U[:,1]-U[:,0],axis=1)
            ok=du>1e-4; per+=list(dp[ok]/du[ok])
    period=float(np.median(per)) if per else 1500.0
    period=TILE/max(1,round(TILE/period))
    q=TILE/Q; pos=[];uv=[];tris=[]
    for ix in range(Q):
        for iz in range(Q):
            x0=-TILE/2+ix*q; z0=-TILE/2+iz*q
            P=np.array([[x0,0,z0],[x0+q,0,z0],[x0+q,0,z0+q],[x0,0,z0+q]])
            U=np.c_[P[:,0]/period,-P[:,2]/period]; U-=np.floor(U.min(0))
            b=len(pos)*4; pos.append(P); uv.append(U); tris+= [(b,b+2,b+1),(b,b+3,b+2)]
    P=np.concatenate(pos); U=np.concatenate(uv); n=len(P)
    col=np.c_[np.full((n,3),min(1.0,FLATSHADE.get(rid,0.85))),np.ones(n)]
    dl=f'{DLDIR}/{lv.lower()}_fill'
    fillprep[dl]=[dict(pos=P,nrm=None,col=col,uv=U,tris=np.array(tris),rid=rid,inf=inf,mode='opaque',la=False,matname='fill')]
    fillmap[lv]=dict(dl=dl,tile=TILE,period=period)
    print('fill',lv,f['name'],'period',round(period,1))
json.dump(fillmap,open(paths.f('gnd_fill.json'),'w'),indent=1)
prepared.update(fillprep); mapping.update({k:k for k in fillprep})
plan=build_all.build(mapping,sys.argv[1] if len(sys.argv)>1 else 'out/4 SF64 3D Terrain.o2r')
print('built with fill',len(plan))
