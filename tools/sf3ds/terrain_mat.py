# Converts 3DS terrain materials (multi-texture TEV) into N64-friendly parts:
# one tiled colour texture per part + shade baked from the sector AO/light map and vertex colour.
import numpy as np
import ground, build_all
from geom3ds import decode
from modelfull import load
_tex={}
def texrgba(rid,inf):
    if rid not in _tex: _tex[rid]=build_all.tex_rgba(rid,inf).astype(np.float32)/255.0
    return _tex[rid]
def sample(img,uv):
    h,w=img.shape[:2]
    x=(uv[:,0]%1.0)*w-0.5; y=((1-uv[:,1])%1.0)*h-0.5
    x0=np.floor(x).astype(int); y0=np.floor(y).astype(int); fx=x-x0; fy=y-y0
    def g(xx,yy): return img[yy%h,xx%w]
    return (g(x0,y0)*((1-fx)*(1-fy))[:,None]+g(x0+1,y0)*(fx*(1-fy))[:,None]+g(x0,y0+1)*((1-fx)*fy)[:,None]+g(x0+1,y0+1)*(fx*fy)[:,None])
def inrange(uv): return uv is not None and uv.min()>-0.02 and uv.max()<1.02
def classify(mat):
    slots=[]
    for k in range(4):
        t=mat.get(f'Texture{k}')
        if not isinstance(t,dict) or not t.get('ResourceID'): continue
        inf=ground.texinfo(t['ResourceID'])
        if not inf: continue
        nm=(inf.get('name') or '').lower()
        if inf['Format'] in (16,14) or nm.endswith(('_n','_nor','_normal','_sdw','_spec')): kind='skip'
        elif '_ao' in nm or nm.endswith('ao') or 'light' in nm: kind='ao'
        else: kind='color'
        slots.append((k,t['ResourceID'],inf,kind))
    return slots
def scale_of(mat):
    s=0
    for i in range(6):
        c=mat.get(f'Combiner{i}')
        if c: s+=c.get('ColorScale',0)
    return 2.0**s
def splat_of(mat):
    c=mat.get('Combiner0') or {}
    if c.get('ColorFunc')==4 and c.get('ColorSource2')==5 and c.get('ColorOperand2')==2:
        return c.get('ColorSource0'),c.get('ColorSource1')
    return None
ATTRS=('pos','nrm','col','uvc')
SKIPMAT={'mat_new_water','mat_wave','mat_foam2'}      # 3DS sea surfaces: the N64 water is drawn instead
WATERFALL={'mat_water','mat_water_foam'}             # scrolling waterfall sheets, drawn by fox_terrain3ds.c
SHADE={}                                             # rid -> [sum of 3DS shade, count] (texture brightness for lit mode)
FRAGLIT=0.6
def fraglit(mat):
    return any((mat.get(f'Combiner{i}') or {}).get(f'ColorSource{k}') in (8,9) for i in range(6) for k in range(3))
def soup(m,tris):
    idx=np.asarray(tris).reshape(-1)
    return {k:(m[k][idx] if m.get(k) is not None else None) for k in ATTRS+('w',)}
def split(d,lo):
    # split triangle soup by w>=0.5 (side A) / w<0.5 (side B) along the isoline
    keys=[k for k in ATTRS if d.get(k) is not None]
    V={k:d[k].reshape(len(d['pos'])//3,3,-1) for k in keys}; W=d['w'].reshape(-1,3)
    outA=[];outB=[]
    for ti in range(len(W)):
        w=W[ti]; ins=w>=0.5; vv=[{k:V[k][ti][i] for k in keys} for i in range(3)]
        if ins.all(): outA.append(vv); continue
        if (~ins).all(): outB.append(vv); continue
        for side,out in ((ins,outA),(~ins,outB)):
            poly=[]
            for i in range(3):
                j=(i+1)%3
                if side[i]: poly.append(vv[i])
                if side[i]!=side[j]:
                    t=(0.5-w[i])/(w[j]-w[i]); poly.append({k:vv[i][k]+(vv[j][k]-vv[i][k])*t for k in keys})
            for k in range(1,len(poly)-1): out.append([poly[0],poly[k],poly[k+1]])
    def pack(lst):
        if not lst: return None
        return {k:np.array([v[k] for tri in lst for v in tri]) for k in keys}
    return pack(outA),pack(outB)
def parts(rid,keep_geom=None,light=None,level_shade=1.0):
    # light: (unit direction towards the sun, ambient, diffuse) -> baked directional shading, flat ground = 1.0
    base=ground.parts_rid(rid)    # positions with node transforms + filtering already applied
    out=[]
    for p in base:
        mat=p['_mat']
        if p['matname'] in SKIPMAT: continue
        slots=classify(mat)
        colors=[s for s in slots if s[3]=='color']; aos=[s for s in slots if s[3]=='ao']
        if not colors and aos: colors,aos=aos[:1],[]
        if not colors: continue
        uvs=[p['uv'],p.get('uv1')]
        aouv=next((u for u in uvs if inrange(u)),None)
        cuv=next((u for u in uvs if u is not None and not inrange(u)),None)
        if cuv is None: cuv=p['uv1'] if (aos and p.get('uv1') is not None and aouv is p['uv']) else p['uv']
        n=len(p['pos'])
        vc=p['col']
        common=dict(mode=p['mode'],la=p['la'],matname=p['matname'],node=p.get('node','other'))
        if p['matname'] in WATERFALL:
            # 3DS: white streak texture x texture, alpha = vertex alpha x texture alpha; scrolled by code
            a=vc[:,3] if vc is not None and vc.shape[1]>3 else np.ones(n)
            if p['matname']=='mat_water':
                # water body under the streaks: the N64 water texture, tiled finer, mostly opaque
                out.append(dict(common,pos=p['pos'],nrm=None,uv=cuv*4.0,col=np.c_[np.full((n,3),0.85),np.full(n,0.9)],tris=p['tris'],rid=None,inf=None,
                                texpath='ast_corneria/D_CO_6028A60',decl=(32,32),valpha=True,wf=True,mode='xlu',la=False))
            out.append(dict(common,pos=p['pos'],nrm=None,uv=cuv,col=np.c_[np.ones((n,3)),a],tris=p['tris'],rid=colors[0][1],inf=colors[0][2],valpha=True,wf=True,mode='xlu',la=False))
            continue
        shade=np.ones((n,3),np.float32)
        if aos and aouv is not None:
            k,r,inf,_=aos[0]; shade*=sample(texrgba(r,inf),aouv)[:,:3]
        if vc is not None and not fraglit(mat): shade*=vc[:,:3]   # per-pixel-lit 3DS materials use vertex colour for something else
        shade=shade*scale_of(mat)
        nrm=p['nrm'] if p.get('nrm') is not None else np.tile([0.0,1.0,0.0],(n,1))
        if light is not None:
            L,A,D=light
            nn=nrm/np.maximum(np.linalg.norm(nrm,axis=1,keepdims=True),1e-6)
            nn=np.where(np.isfinite(nn),nn,[0.0,1.0,0.0])
            shade=shade*((A+D*np.clip(nn@L,0,1))/(A+D*max(L[1],0.0)))[:,None]
        if fraglit(mat): shade=shade*FRAGLIT   # 3DS per-pixel lit material: darker than our bake
        shade=shade*level_shade
        sp=splat_of(mat); bym={s[0]:s for s in colors}
        m=dict(pos=p['pos'],nrm=nrm,col=shade,uvc=cuv,w=(vc[:,3] if vc is not None and vc.shape[1]>3 else None))
        def emit(pos,nr,uv,col,tris,s):
            if 'scorc' in (p['matname'] or '').lower() and 'detriti' in (s[2].get('name') or ''):
                col=col*np.array([1.7,0.95,0.6])   # 3DS adds a runtime ember colour (combiner constant) to scorched ground
            SHADE.setdefault(s[1],[0.0,0]); SHADE[s[1]][0]+=float(col.mean())*len(col); SHADE[s[1]][1]+=len(col)
            out.append(dict(common,pos=pos,nrm=nr,uv=uv,col=np.c_[np.clip(col,0,4),np.ones(len(col))],tris=tris,rid=s[1],inf=s[2]))
        if sp and sp[0] in bym and sp[1] in bym and m['w'] is not None and m['w'].min()<0.5<=m['w'].max():
            d=soup(m,p['tris']); A,B=split(d,0.5)
            for side,s in ((A,bym[sp[0]]),(B,bym[sp[1]])):
                if side is None: continue
                nt=len(side['pos'])//3
                emit(side['pos'],side['nrm'],side['uvc'],side['col'],np.arange(nt*3).reshape(-1,3),s)
        else:
            s=bym[sp[0]] if sp and sp[0] in bym and m['w'] is not None and m['w'].mean()>=0.5 else (bym[sp[1]] if sp and sp[1] in bym else colors[0])
            emit(p['pos'],nrm,cuv,shade,p['tris'],s)
    return out
