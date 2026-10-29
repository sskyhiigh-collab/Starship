import numpy as np
SIZES={0:1,1:1,2:2,3:4}
COMPS=[3,3,4,2,3,2,2,4,4,4]
def decode(g):
    fmt=g['fmt']; mask=fmt&0xffff; types=fmt>>16
    raw=g['raw']; off=0; out={}
    for a in range(10):
        if not mask>>a&1: continue
        t=(types>>(2*a))&3; n=COMPS[a]; sz=SIZES[t]*n
        if off+sz>raw.shape[1]: break
        b=raw[:,off:off+sz].copy()
        if t==3: v=b.view('<f4')
        elif t==2: v=b.view('<i2').astype(np.float32)
        elif t==1: v=b.astype(np.float32)
        else: v=b.view(np.int8).astype(np.float32)
        out[a]=(v,t); off+=sz
    s0=g['s0'] or (1,1,1,1); s1=g['s1'] or (1,1,1,1)
    pos=out[0][0]*(s0[0] if out[0][1]!=3 else 1)
    nrm=out[1][0]*(s0[1] if out[1][1]!=3 else 1) if 1 in out else None
    col=out[2][0]/255.0 if 2 in out else None
    uv=out[3][0]*(s1[0] if out[3][1]!=3 else 1) if 3 in out else None
    def sc(a,k):
        if a not in out: return None
        v,t=out[a]; return v*(s1[k] if t!=3 else 1)
    uv1=sc(5,1); uv2=sc(6,2)
    idx=g['idx']
    if g['prim']==1:
        t=[]
        for i in range(len(idx)-2):
            a,b,c=idx[i],idx[i+1],idx[i+2]
            if a==b or b==c or a==c: continue
            t.append((a,b,c) if i%2==0 else (b,a,c))
        tris=np.array(t,int).reshape(-1,3)
    else: tris=idx.reshape(-1,3)
    return dict(pos=pos,nrm=nrm,col=col,uv=uv,uv1=uv1,uv2=uv2,tris=tris,mat=g['mat'],attrmask=mask)
