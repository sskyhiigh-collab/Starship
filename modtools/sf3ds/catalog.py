import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import os,glob,struct,json,pickle
from gdb import GDB
from stream import tree,load_stream
R=paths.ROMFS
cat={}   # rid -> {name,type,chunks:{seg:(stream,off,size)}}
for g in sorted(glob.glob(R+'*.resourcestreamgdb')):
    pre=g[:-len('.resourcestreamgdb')]; st=os.path.basename(pre)
    try: ch=load_stream(pre)
    except Exception as e: print('skip',st,e); continue
    for rid,lst in ch.items():
        e=cat.setdefault(rid,{'chunks':{}})
        for seg,off,size in lst: e['chunks'].setdefault(seg,(st,off,size))
data={}
def read(st,off,size):
    if st not in data: data[st]=open(R+st+'.resourcestreambin','rb').read()
    return data[st][off:off+size]
META=0xc09676d2
for rid,e in cat.items():
    if META in e['chunks']:
        b=read(*e['chunks'][META]); g=GDB(b); t=tree(g,g.hdr[6])
        e['name']=t.get('Name'); e['type']=t.get('ResourceType')
pickle.dump(cat,open(paths.f('catalog.pkl'),'wb'))
from collections import Counter
print(len(cat), Counter(e.get('type') for e in cat.values()))
segs=Counter((e.get('type'),s) for e in cat.values() for s in e['chunks']); print(segs)
