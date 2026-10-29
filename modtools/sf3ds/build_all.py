import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import sys,os,json,struct,zipfile,numpy as np
sys.path.insert(0,os.path.join(paths.TOOLS,'sf3ds'))
from cat3ds import *; from modelfull import load; from geom3ds import decode
from texsel import pick_diffuse
from etc1 import decode as etc_decode
from n64lit import litness
from scipy import ndimage
from PIL import Image, ImageDraw
GAMMA=float(os.environ.get('SF_GAMMA','2.2'))
HDR=bytes.fromhex('000000005845544f01000000efbeaddeefbeadde0000000001000000')+bytes(36)
TEXDIR='ast_sf3ds'
def tex_rgba(rid,inf):
    e=cat[rid]
    data=chunk(e,TEXB) if TEXB in e['chunks'] else open(R+f'Resources/{rid:08x}.texturebin','rb').read()
    w,h=inf['Width'],inf['Height']
    return etc_decode(data,w,h,alpha=inf['Format']==18)
DECL_MAX={}
def decl_size(w,h,rid=None):
    if rid in DECL_MAX:
        m=DECL_MAX[rid]; dw,dh=decl_size(w,h)
        while max(dw,dh)>m and min(dw,dh)>1: dw//=2; dh//=2
        return dw,dh
    if w>=h: dw=min(64,w); dh=max(1,dw*h//w)
    else: dh=min(64,h); dw=max(1,dh*w//h)
    while dw*dh>4096: dw//=2; dh//=2
    return dw,dh
def log2(x): return int(x).bit_length()-1
def node_world(nodes):
    W=[]
    for i,n in enumerate(nodes):
        m=np.eye(4)
        if 'LocalMtx' in n: m[:3,:4]=np.array(n['LocalMtx']).reshape(3,4)
        p=n.get('ParentIndex',0xffffffff)
        W.append(W[p]@m if p!=0xffffffff and p<i else m)
    return W
def model_parts(name):
    e=cat[byname[name]]; gs,ms,ns=load(chunk(e,GDB_SEG),chunk(e,BIN_SEG))
    W=node_world(ns); gmat={}
    for i,n in enumerate(ns):
        gi=n.get('geometryIndces')
        if isinstance(gi,tuple):
            for g in gi[1:]: gmat[g]=W[i]   # gi[0] is a type tag
    parts=[]
    for g in gs:
        m=decode(g); M=gmat.get(g['gi'],np.eye(4))
        if not np.allclose(M,np.eye(4)):
            m['pos']=(M[:3,:3]@m['pos'].T).T+M[:3,3]
            if m['nrm'] is not None: m['nrm']=(M[:3,:3]@m['nrm'].T).T
        mat=ms[g['mat']]; rid,inf,t=pick_diffuse(mat)
        # 3DS: translucent only when the material doesn't write depth; TranslucencyKind alone just means "has alpha"
        effect=mat.get('DepthMask',1)==0 or (mat.get('TranslucencyKind',0) in (1,3) and any(k in (mat.get('Name') or '').lower() for k in ('crater','shadow','decal','kage')))
        mode='xlu' if effect else ('cutout' if (mat.get('AlphaTest',0) and inf is not None and inf['Format']==18) else 'opaque')
        la=bool(effect and inf is not None and inf['Format']!=18)
        m.update(rid=rid,inf=inf,mode=mode,la=la,matname=mat.get('Name'))
        parts.append(m)
    return post_parts(name,parts)
def post_parts(name,parts):
    # flat untextured translucent decals are 3DS blob shadows (black via a combiner constant); N64 has none
    H=max((np.ptp(p['pos'][:,1]) for p in parts if len(p['pos'])),default=0)
    parts=[p for p in parts if not (p['rid'] is None and not p.get('texpath') and p['mode']=='xlu' and np.ptp(p['pos'][:,1])<=0.03*max(H,1))]
    if name in LIFT:
        mode,target=LIFT[name]
        sel=[p for p in parts if p['mode']==mode]
        lo=min(p['pos'][:,1].min() for p in sel)
        for p in sel: p['pos']=p['pos']+np.array([0,target-lo,0])
    for p in parts:
        # damage decals sit exactly on the walls: push them out a little so they don't z-fight
        if (p.get('matname') or '').startswith('Damage') and p.get('nrm') is not None:
            nn=p['nrm']/np.maximum(np.linalg.norm(p['nrm'],axis=1,keepdims=True),1e-6)
            p['pos']=p['pos']+nn*1.5
    return parts
# model pivot sits mid-height on the 3DS tree: only the foliage is offset (trunk already stands on y=0)
LIFT={'CN_Tree_01':('cutout',40.0)}
COMB_OPA='<SetCombineLERP A0="G_CCMUX_TEXEL0" B0="G_CCMUX_0" C0="G_CCMUX_SHADE" D0="G_CCMUX_0" Aa0="G_ACMUX_0" Ab0="G_ACMUX_0" Ac0="G_ACMUX_0" Ad0="{a0}" A1="G_CCMUX_COMBINED" B1="G_CCMUX_0" C1="G_CCMUX_PRIMITIVE" D1="G_CCMUX_0" Aa1="G_ACMUX_0" Ab1="G_ACMUX_0" Ac1="G_ACMUX_0" Ad1="G_ACMUX_COMBINED"/>'
def mat_xml(texpath,dw,dh,wrapS,wrapT):
    # texture load only, like vanilla SF64 DLs: combiner/render mode/geometry/prim are inherited from the game's setup
    lineb=dw*2//8; lrs=dw*dh-1; dxt=(2048+lineb-1)//lineb
    cms='G_TX_WRAP' if wrapS else 'G_TX_CLAMP'; cmt='G_TX_WRAP' if wrapT else 'G_TX_CLAMP'
    ms,mt=log2(dw),log2(dh)
    return f'''<DisplayList Version="0">
	<SetTextureLUT Mode="G_TT_NONE"/>
	<TileSync/>
	<SetTextureImage Path="{texpath}" Format="G_IM_FMT_RGBA" Size="G_IM_SIZ_16b_LOAD_BLOCK" Width="1"/>
	<SetTile Format="G_IM_FMT_RGBA" Size="G_IM_SIZ_16b_LOAD_BLOCK" Line="0" TMem="0" Tile="7" Palette="0" Cms0="{cms}" Cms1="G_TX_NOMIRROR" Cmt0="{cmt}" Cmt1="G_TX_NOMIRROR" MaskS="{ms}" ShiftS="0" MaskT="{mt}" ShiftT="0"/>
	<LoadSync/>
	<LoadBlock Tile="7" Uls="0" Ult="0" Lrs="{lrs}" Dxt="{dxt}"/>
	<PipeSync/>
	<SetTile Format="G_IM_FMT_RGBA" Size="G_IM_SIZ_16b" Line="{lineb}" TMem="0" Tile="0" Palette="0" Cms0="{cms}" Cms1="G_TX_NOMIRROR" Cmt0="{cmt}" Cmt1="G_TX_NOMIRROR" MaskS="{ms}" ShiftS="0" MaskT="{mt}" ShiftT="0"/>
	<SetTileSize T="0" Uls="0" Ult="0" Lrs="{(dw-1)*4}" Lrt="{(dh-1)*4}"/>
	<EndDisplayList/>
</DisplayList>
'''
WHITE=f'{TEXDIR}/tex_white'
BRIGHT={}   # rid -> texture brightness factor (terrain lit mode)
# bit-range toggles (LUS ORs the named value, clears only Sft..Sft+Length)
XLU_ON ='\t<PipeSync/>\n\t<SetOtherMode Cmd="G_SETOTHERMODE_L" Sft="16" Length="2" />\n\t<SetOtherMode Cmd="G_SETOTHERMODE_L" Sft="5" Length="1" />\n'
XLU_OFF='\t<PipeSync/>\n\t<SetOtherMode Cmd="G_SETOTHERMODE_L" Sft="16" Length="2" G_RM_AA_ZB_OPA_SURF2="1" />\n'
CUT_ON ='\t<PipeSync/>\n\t<SetOtherMode Cmd="G_SETOTHERMODE_L" Sft="12" Length="1" G_RM_AA_ZB_TEX_EDGE2="1" />\n'
CUT_OFF='\t<PipeSync/>\n\t<SetOtherMode Cmd="G_SETOTHERMODE_L" Sft="12" Length="1" />\n'
def batches(tris,maxv=32):
    out=[];cur=[];cv={}
    for t in tris:
        if len(cv)+len([v for v in set(t) if v not in cv])>maxv: out.append((list(cv),cur)); cur=[];cv={}
        for v in t:
            if v not in cv: cv[v]=len(cv)
        cur.append(tuple(cv[v] for v in t))
    if cur: out.append((list(cv),cur))
    return out
def main_xml(dl,modes,toggle):
    out=['<DisplayList Version="0">']; cur='opaque'
    for i,md in enumerate(modes):
        if toggle and md!=cur:
            if cur=='cutout': out.append(CUT_OFF.rstrip('\n'))
            if cur=='xlu': out.append(XLU_OFF.rstrip('\n'))
            if md=='cutout': out.append(CUT_ON.rstrip('\n'))
            if md=='xlu': out.append(XLU_ON.rstrip('\n'))
            cur=md
        out.append(f'\t<CallDisplayList Path="{dl}_mat{i}"/>\n\t<CallDisplayList Path="{dl}_tri{i}"/>')
    if toggle:
        if cur=='cutout': out.append(CUT_OFF.rstrip('\n'))
        if cur=='xlu': out.append(XLU_OFF.rstrip('\n'))
    out+=['\t<EndDisplayList/>','</DisplayList>','']
    return '\n'.join(out)
from sf64res import O2R
_V=O2R(paths.SF64_O2R,'ast_')
def vanilla_alpha(dl):
    b=_V.raw(dl); p=0x48
    while p+8<=len(b):
        w0,w1=struct.unpack_from('<II',b,p); op=w0>>24; p+=8
        if op in (0x33,0x32,0x31,0x20):
            h=struct.unpack_from('<II',b,p); p+=8
            if op==0x20:
                n=_V.h.get((h[0]<<32)|h[1])
                if not n: continue
                r=_V.raw(n); typ,w,hh,sz=struct.unpack_from('<IIII',r,0x40); d=r[0x50:0x50+sz]
                if typ in (5,6,7,8,9): return True
                if typ==2 and len(d)>=2 and (np.frombuffer(d[:len(d)//2*2],'>u2')&1).min()==0: return True
                if typ==1 and len(d)>=4 and np.frombuffer(d[:len(d)//4*4],np.uint8)[3::4].min()<255: return True
        elif op==0xb8: break
    return False
def build(mapping,out,log=print):
    files={}; texuse={}   # rid -> (inf, [uv triangle arrays])
    plan=[]
    for dl,name in sorted(mapping.items()):
        try: parts=model_parts(name)
        except Exception as ex: log('FAIL',dl,name,ex); continue
        lit=litness(dl)!='unlit'
        order={'opaque':0,'cutout':1,'xlu':2}
        parts=[p for p in parts if len(p['tris'])]
        parts.sort(key=lambda p:order[p['mode']])
        vx=['<Vertex Version="0">']; base=0; nmat=0
        for i,p in enumerate(parts):
            P=np.rint(p['pos']).astype(int)
            if np.abs(P).max()>32000: log('RANGE',dl,name); break
            if lit and p['nrm'] is not None:
                p['nrm']=np.where(np.isfinite(p['nrm']).all(1,keepdims=True)&(np.abs(p['nrm']).sum(1,keepdims=True)>1e-6),p['nrm'],[0.0,1.0,0.0])
                C=(np.clip(np.rint(p['nrm']/np.maximum(np.linalg.norm(p['nrm'],axis=1,keepdims=True),1e-6)*127),-127,127).astype(int))&0xff
            elif p['col'] is not None: C=np.clip(np.rint(p['col'][:,:3]*255),0,255).astype(int)
            else: C=np.full((len(P),3),255)
            A=np.full(len(P),255)
            if p.get('valpha') and p['col'] is not None and p['col'].shape[1]>3: A=np.clip(np.rint(p['col'][:,3]*255),0,255).astype(int)
            if p.get('texpath') and p['uv'] is not None:
                dw,dh=p['decl']; uv=p['uv']
                S=np.clip(np.rint(uv[:,0]*dw*32-16),-32768,32767).astype(int); T=np.clip(np.rint((1-uv[:,1])*dh*32-16),-32768,32767).astype(int)
                files[f'{dl}_mat{i}']=mat_xml(p['texpath'],dw,dh,True,True).encode()
            elif p['rid'] is not None and p['uv'] is not None:
                inf=p['inf']; dw,dh=decl_size(inf['Width'],inf['Height'],p['rid'])
                uv=p['uv']; wrapS=bool(uv[:,0].min()<-0.01 or uv[:,0].max()>1.01); wrapT=bool(uv[:,1].min()<-0.01 or uv[:,1].max()>1.01)
                S=np.rint(uv[:,0]*dw*32-16).astype(int); T=np.rint((1-uv[:,1])*dh*32-16).astype(int)
                if np.abs(S).max()>32767 or np.abs(T).max()>32767: log('UVRANGE',dl,name)
                S=np.clip(S,-32768,32767); T=np.clip(T,-32768,32767)
                texpath=f'{TEXDIR}/tex_{p["rid"]:08x}'+('_la' if p['la'] else '')
                files[f'{dl}_mat{i}']=mat_xml(texpath,dw,dh,wrapS,wrapT).encode()
                texuse.setdefault((p['rid'],p['la']),[inf,[]])[1].append(uv[p['tris']])
            else:
                S=T=np.full(len(P),64,int); files[f'{dl}_mat{i}']=mat_xml(WHITE,8,8,False,False).encode()
            tri=['<DisplayList Version="0">']
            for vids,ts in batches([tuple(t) for t in p['tris']]):
                for v in vids: vx.append(f'\t<Vtx X="{P[v,0]}" Y="{P[v,1]}" Z="{P[v,2]}" S="{S[v]}" T="{T[v]}" R="{C[v,0]}" G="{C[v,1]}" B="{C[v,2]}" A="{A[v]}"/>')
                tri.append(f'\t<LoadVertices Path="{dl}_vtx" VertexBufferIndex="0" VertexOffset="{base}" Count="{len(vids)}"/>')
                tri+= [f'\t<Triangle1 V00="{a}" V01="{b}" V02="{c}"/>' for a,b,c in ts]
                base+=len(vids)
            tri+=['\t<EndDisplayList/>','</DisplayList>']
            files[f'{dl}_tri{i}']=('\n'.join(tri)+'\n').encode(); nmat+=1
        vx.append('</Vertex>')
        files[f'{dl}_vtx']=('\n'.join(vx)+'\n').encode()
        va=vanilla_alpha(dl); files[dl]=main_xml(dl,[p['mode'] for p in parts[:nmat]],not va).encode()
        plan.append((dl,name,lit,[p['mode'] for p in parts],va))
    for (rid,la),(inf,uvs) in texuse.items():
        img=tex_rgba(rid,inf); h,w=img.shape[:2]
        if la: img=img.copy(); img[...,3]=img[...,:3].max(-1)
        rgb=(np.clip((np.clip(img[...,:3]/255.0,0,1)**GAMMA)*BRIGHT.get(rid,1.0),0,1)*255).round().astype(np.uint8)
        # pad islands (only for clamp-free use the mask from UVs)
        mk=Image.new('L',(w*2,h*2),0); d=ImageDraw.Draw(mk)
        for U in uvs:
            for t in U:
                d.polygon([(float(u)*w*2,(1-float(v))*h*2) for u,v in t],fill=255,outline=255)
        mask=np.array(mk.resize((w,h),Image.BOX))>0
        tiled=any(((U<-0.01)|(U>1.01)).any() for U in uvs)
        if mask.any() and not mask.all() and not tiled:
            _,(iy,ix)=ndimage.distance_transform_edt(~mask,return_indices=True); rgb=rgb[iy,ix]; a=img[...,3][iy,ix]
        else: a=img[...,3]
        out_img=np.dstack([rgb, a if (inf['Format']==18 or la) else np.full((h,w),255,np.uint8)]).astype(np.uint8)
        dw,dh=decl_size(w,h,rid)
        files[f'{TEXDIR}/tex_{rid:08x}'+('_la' if la else '')]=HDR+struct.pack('<IIIIffI',2,w,h,1,(w*4)/(dw*2),h/dh,w*h*4)+out_img.tobytes()
    files[WHITE]=HDR+struct.pack('<IIIIffI',2,8,8,1,2.0,1.0,256)+b'\xff'*256
    with zipfile.ZipFile(out,'w',zipfile.ZIP_STORED) as z:
        for k in sorted(files): z.writestr(k,files[k])
    return plan
if __name__=='__main__':
    mapping=json.load(open(sys.argv[1]))
    plan=build(mapping,sys.argv[2])
    json.dump(plan,open(sys.argv[2]+'.plan.json','w'))
    print('built',len(plan),'DLs ->',sys.argv[2],os.path.getsize(sys.argv[2])//1024//1024,'MB')
