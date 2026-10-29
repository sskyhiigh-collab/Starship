import struct
from gdb import GDB
from cat3ds import cat,chunk,TEXG,TEXB
def texinfo(rid):
    e=cat.get(rid)
    if not e or TEXG not in e['chunks']: return None
    g=GDB(chunk(e,TEXG)); n=g.hdr[3]>>8; f={}
    for o in struct.unpack_from('<%dI'%n,g.d,0x18):
        nm=g.name(g.u32(o+4)); f[nm]=g.u32(o+12)
    f['name']=e.get('name'); return f
BAD=('_n','_normal','_normals','_nor','_sdw','_ao','_spec')
def pick_diffuse(m):
    for slot in ('Texture0','Texture1','Texture2'):
        t=m.get(slot)
        if not isinstance(t,dict) or not t.get('ResourceID'): continue
        inf=texinfo(t['ResourceID'])
        if not inf: continue
        nm=(inf['name'] or '').lower()
        if inf['Format'] in (16,14) or nm.endswith(BAD) or 'normal' in nm: continue
        return t['ResourceID'],inf,t
    return None,None,None
