import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import pickle,struct,numpy as np
R=paths.ROMFS
cat=pickle.load(open(paths.f('catalog.pkl'),'rb'))
GDB_SEG=0x1da22213; BIN_SEG=0xf589c343; TEXG=0xb898cf0d; TEXB=0x9351db83
_data={}
def chunk(e,seg):
    if seg not in e['chunks']: return None
    st,off,size=e['chunks'][seg]
    if st not in _data: _data[st]=open(R+st+'.resourcestreambin','rb').read()
    return _data[st][off:off+size]
byname={}
for rid,e in cat.items():
    if e.get('type')=='Model' and e.get('name'): byname.setdefault(e['name'],rid)
