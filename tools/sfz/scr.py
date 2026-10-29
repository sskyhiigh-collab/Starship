# PlatinumGames SCR (Star Fox Zero stage scenery) reader: entries -> meshes (pos, uv, colour, tris, texture id)
import struct,numpy as np
def entries(d):
    n=struct.unpack_from('>H',d,6)[0]; tab=struct.unpack_from('>I',d,8)[0]
    offs=struct.unpack_from('>%dI'%n,d,tab)
    out=[]
    for i,o in enumerate(offs):
        end=offs[i+1] if i+1<n else len(d)
        name=d[o+4:o+0x44].split(b'\0')[0].decode()
        pos=struct.unpack_from('>3f',d,o+0x44); rot=struct.unpack_from('>3f',d,o+0x50); scl=struct.unpack_from('>3f',d,o+0x5c)
        out.append(dict(name=name,o=o,end=end,base=o+0x100,pos=pos,rot=rot,scl=scl))
    return out
def find_vb(d,b,k,nv):
    # vertex buffer: nv x 28 bytes (pos f32x3, uv f16x2, normal, tangent, colour) somewhere between the model base and its mesh header
    for s in range(b,k-nv*28+1,4):
        V=np.frombuffer(d[s:s+nv*28],np.uint8).reshape(nv,28)
        P=V[:,:12].copy().view('>f4').reshape(nv,3); UV=V[:,12:16].copy().view('>f2').reshape(nv,2)
        with np.errstate(all='ignore'):
            ok=np.isfinite(P).all() and np.isfinite(UV).all() and np.abs(P).max()<1e6 and np.abs(UV).max()<64 and (np.abs(P).max(1)>1e-3).all()
        if ok: return s
    return None
def find_ib(d,k,ni,P):
    # u16 triangle list right after the mesh header (normally +0x102). Score each candidate start:
    # most vertices used, then fewest degenerate triangles, then most compact triangles.
    nv=len(P); best=None; r=max(np.linalg.norm(P,axis=1).max(),1e-6)
    for o in range(k+0x100,min(len(d)-ni*2,k+0x140)+1,2):
        I=np.frombuffer(d[o:o+ni*2],'>u2').astype(int)
        if I.max()>=nv: continue
        T=I[:len(I)//3*3].reshape(-1,3); p=P[T]
        A=0.5*np.linalg.norm(np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0]),axis=1)
        deg=int((A<1e-6*r*r).sum())
        e=max(np.linalg.norm(p[:,1]-p[:,0],axis=1).max(),np.linalg.norm(p[:,2]-p[:,1],axis=1).max(),np.linalg.norm(p[:,0]-p[:,2],axis=1).max())/r
        key=(-len(np.unique(T)),deg,round(e,3),o)
        if best is None or key<best[0]: best=(key,I)
    return best[1] if best else np.zeros(0,int)
def strip_to_list(I):
    # SCR meshes are triangle strips (degenerate triangles join the strips)
    out=[]
    for i in range(len(I)-2):
        a,b,c=I[i],I[i+1],I[i+2]
        if a==b or b==c or a==c: continue
        out+= [a,b,c] if i%2==0 else [b,a,c]
    return np.array(out,int)
def meshes(d,e):
    b=e['base']; res=[]; k=d.find(b'SCR_MESH',e['o'],e['end'])
    while k!=-1:
        nv,unk,voff,ni=struct.unpack_from('>4I',d,k+0x90)
        vs=find_vb(d,b,k,nv)
        if vs is None: k=d.find(b'SCR_MESH',k+8,e['end']); continue
        V=np.frombuffer(d[vs:vs+nv*28],np.uint8).reshape(nv,28)
        P=V[:,:12].copy().view('>f4').reshape(nv,3).astype(float)
        UV=V[:,12:16].copy().view('>f2').reshape(nv,2).astype(float)
        C=V[:,24:28].astype(float)/255
        I=find_ib(d,k,ni,P)
        res.append(dict(pos=P,uv=UV,col=C,idx=I[:len(I)//3*3],hdr=k))
        k=d.find(b'SCR_MESH',k+8,e['end'])
    return res
