import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
# Star Fox Zero space backdrops -> Starship mod (.o2r): sky sphere + nebula/galaxy/planet layers per backdrop
import sys,struct,json,numpy as np
sys.path.insert(0,os.path.join(paths.TOOLS,'sfz')); sys.path.insert(0,os.path.join(paths.TOOLS,'sf3ds'))
from dat import read_dat; import scr, wtex
import build_all
U=paths.SFZ_CONTENT
SRC={'st2':'data002/st2/r200.dat','st4':'data002/st4/r400.dat','st6':'data002/st6/r600.dat','st7':'data002/st7/r700.dat','stb':'data003/stb/rb00.dat'}
RADIUS=6000.0          # sky sphere radius in Starship units (inside the far plane, 12800)
LAYER_MAX=1024         # nebula/galaxy/planet textures are downsized to at most this
def euler(r):
    x,y,z=r
    Rx=np.array([[1,0,0],[0,np.cos(x),-np.sin(x)],[0,np.sin(x),np.cos(x)]])
    Ry=np.array([[np.cos(y),0,np.sin(y)],[0,1,0],[-np.sin(y),0,np.cos(y)]])
    Rz=np.array([[np.cos(z),-np.sin(z),0],[np.sin(z),np.cos(z),0],[0,0,1]])
    return Rz@Ry@Rx
IMG={}
def deblock(img):
    # the sky is BC1-compressed: smooth the 4x4 block artefacts in the nebula colour, keep the stars crisp
    from scipy import ndimage
    f=img[...,:3].astype(np.float32); lum=f.mean(-1)
    stars=(lum-ndimage.gaussian_filter(lum,3))>18
    stars=ndimage.binary_dilation(stars,iterations=1)
    smooth=np.stack([ndimage.gaussian_filter(f[...,c],1.6) for c in range(3)],-1)
    out=np.where(stars[...,None],f,smooth)
    out+=np.random.default_rng(1).uniform(-0.5,0.5,out.shape)   # light dither against banding
    img=img.copy(); img[...,:3]=np.clip(np.rint(out),0,255).astype(np.uint8); return img
def tex_rgba(rid,inf): return IMG[rid]
build_all.tex_rgba=tex_rgba
prepared={}; mapping={}; info={}
for bd,f in SRC.items():
    fs=dict(read_dat(open(f"{U}/{f}",'rb').read())); k=[x for x in fs if x.endswith('.scr')][0]; d=fs[k]
    W=wtex.wta_entries(fs[k.replace('.scr','scr.wta')]); wtp=fs[k.replace('.scr','scr.wtp')]
    ents=scr.entries(d)
    sph=[e for e in ents if 'universe_sphere' in e['name']][0]
    sr=np.linalg.norm(scr.meshes(d,sph)[0]['pos'],axis=1).max()*max(sph['scl'])
    f_=RADIUS/sr
    sky=[]; fx=[]
    for e in ents:
        tex=[i for i,w in enumerate(W) if struct.pack('>I',w['id']) in d[e['o']:e['end']]]
        R=euler(e['rot']); S=np.array(e['scl']); T=np.array(e['pos'])
        if e['name'].endswith(('PlanetA','planetA_ring2')): continue   # this planet mesh doesn't decode cleanly yet
        for m in scr.meshes(d,e):
            if not tex or not len(m['idx']): continue
            w=W[tex[0]]; rid=(hash((bd,tex[0]))&0x7fffffff)|0x10000000
            if rid not in IMG:
                img=wtex.decode(wtp,w)
                is_sky=e is sph
                if not is_sky and max(img.shape[:2])>LAYER_MAX:
                    from PIL import Image
                    s=max(img.shape[:2])//LAYER_MAX; img=np.array(Image.fromarray(img).resize((img.shape[1]//s,img.shape[0]//s),Image.LANCZOS))
                if is_sky or (w['fmt']&0x3f)==0x31: img=img.copy(); img[...,3]=255
                if is_sky: img=deblock(img)
                IMG[rid]=img
            img=IMG[rid]; alpha=(w['fmt']&0x3f)==0x33 and e is not sph
            P=((R@(m['pos']*S).T).T+T)*f_
            part=dict(pos=P,nrm=None,col=m['col'],uv=np.c_[m['uv'][:,0],1-m['uv'][:,1]],tris=m['idx'].reshape(-1,3),rid=rid,
                      inf={'Width':img.shape[1],'Height':img.shape[0],'Format':18 if alpha else 0},mode='xlu' if e is not sph else 'opaque',la=False,matname=e['name'])
            (sky if e is sph else fx).append(part)
    prepared[f'ast_sfz_sky/{bd}_sky']=sky; mapping[f'ast_sfz_sky/{bd}_sky']=f'ast_sfz_sky/{bd}_sky'
    if fx: prepared[f'ast_sfz_sky/{bd}_fx']=fx; mapping[f'ast_sfz_sky/{bd}_fx']=f'ast_sfz_sky/{bd}_fx'
    info[bd]=dict(fx=bool(fx),layers=[p['matname'] for p in fx])
    print(bd,'sky r',round(sr),'scale',round(f_,3),'layers',info[bd]['layers'])
build_all.model_parts=lambda k: prepared[k]
build_all.litness=lambda dl:'unlit'
build_all.vanilla_alpha=lambda dl: True        # no render-mode toggles: the C code sets the modes
build_all.TEXDIR='ast_sfz_sky'
build_all.GAMMA=1.0
out=sys.argv[1]
plan=build_all.build(mapping,out)
json.dump(info,open(paths.f('sky_info.json'),'w'),indent=1)
# settings file (read by Starship at runtime)
L=['# Star Fox Zero space backdrops (read by Starship at runtime)',
   '# bd <name> <sky DL> [<layers DL>] / level <id> <name> / menus <name> / dots 0|1 / roll 1|-1']
for bd,i in info.items(): L.append(f'bd {bd} ast_sfz_sky/{bd}_sky'+(f' ast_sfz_sky/{bd}_fx' if i['fx'] else ''))
for lid,bd,nm in [(2,'st2','Sector X'),(1,'st4','Meteo'),(5,'st4','Sector Y'),(18,'st6','Sector Z'),(3,'st6','Area 6'),(17,'st7','Bolse'),(9,'st7','Venom (Andross)')]:
    L.append(f'level {lid} {bd}   # {nm}')
L+=['# menus stb   # title screen / level select: off (original star dots)','dots 0','roll 1']
text='\n'.join(L)+'\n'; open(paths.f('sky_config.txt'),'w').write(text)
dd=text.encode()+b'\0'
blob=struct.pack('<IIIII',0,0x4F424C42,0,0xDEADBEEF,0xDEADBEEF)+bytes(0x40-20)+struct.pack('<I',len(dd))+dd
import zipfile
with zipfile.ZipFile(out,'a',zipfile.ZIP_STORED) as z: z.writestr('ast_sfz_sky/config',blob)
import os; print('built',len(plan),out,os.path.getsize(out)//2**20,'MB')
