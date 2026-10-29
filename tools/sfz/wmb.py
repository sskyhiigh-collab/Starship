# PlatinumGames WMB (Bayonetta-1 style "WMB\0", big-endian on Wii U) header reader
import struct
FIELDS=['id','unkA','vfmt','nverts','nmap_unkE_F','offPos','offVerts','offVertsEx','g0','g1','g2','g3','nBones','offBoneHier','offBoneRel','offBonePos','offBoneTT',
        'nMats','offMatOffs','offMats','nMeshes','offMeshOffs','offMeshes','unkK','unkL','offUnkJ','offBoneSym','offBoneFlags','ex0','ex1','ex2','ex3']
def header(d):
    v=struct.unpack_from('>4s31I',d,0)
    return dict(zip(FIELDS,v))
import numpy as np
def meshes(d):
    """-> list of dict(name, batches=[dict(mat, pos, nrm, uv, col, tris)]) ; Bayonetta-1 style WMB, big-endian"""
    h=header(d); nv=h['nverts']
    V=np.frombuffer(d[h['offVerts']:h['offVerts']+nv*32],np.uint8).reshape(nv,32)
    P=V[:,:12].copy().view('>f4').reshape(nv,3).astype(float)
    UV=V[:,12:16].copy().view('>f2').reshape(nv,2).astype(float)
    nr=V[:,16:20].copy().view('>u4').reshape(nv).astype(np.int64)
    def s10(x): x=x&0x3ff; return np.where(x>=512,x-1024,x)/511.0
    N=np.stack([s10(nr>>20),s10(nr>>10),s10(nr)],-1)       # 10:10:10 packed normal (best guess; only used for lighting)
    exsz=8
    E=np.frombuffer(d[h['offVertsEx']:h['offVertsEx']+nv*exsz],np.uint8).reshape(nv,exsz)
    C=E[:,:4].astype(float)/255
    out=[]
    offs=struct.unpack_from('>%dI'%h['nMeshes'],d,h['offMeshOffs'])
    for o in offs:
        m=h['offMeshes']+o; nb=struct.unpack_from('>h',d,m+2)[0]
        name=d[m+0x20:m+0x40].split(b'\0')[0].decode()
        bos=struct.unpack_from('>%dI'%nb,d,m+0x80); bl=[]
        for b in bos:
            B=m+0x80+b; f=struct.unpack_from('>16I',d,B)
            mat=f[1]&0xffff; v0,v1,prim,ioff,ni,voff=f[3],f[4],f[5],f[6],f[7],f[8]
            I=np.frombuffer(d[B+ioff:B+ioff+ni*2],'>u2').astype(int)+voff
            if prim==5:   # strip
                T=[];
                for i in range(len(I)-2):
                    a,b_,c=I[i],I[i+1],I[i+2]
                    if a!=b_ and b_!=c and a!=c: T.append((a,b_,c) if i%2==0 else (b_,a,c))
                T=np.array(T,int)
            else: T=I[:len(I)//3*3].reshape(-1,3)
            bl.append(dict(mat=mat,tris=T,v0=v0,v1=v1,prim=prim))
        out.append(dict(name=name,batches=bl))
    return dict(P=P,UV=UV,N=N,C=C,meshes=out,h=h)
def material_textures(d):
    h=header(d); mo=struct.unpack_from('>%dI'%h['nMats'],d,h['offMatOffs'])
    out=[]
    for i,o in enumerate(mo):
        M=h['offMats']+o; nxt=h['offMats']+(mo[i+1] if i+1<len(mo) else o+104)
        out.append(list(struct.unpack_from('>%dI'%((nxt-M-4)//4),d,M+4)))
    return out
