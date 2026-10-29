import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import json,sys,os
import ground, build_all, tmpl     # ground: texture lookup with RomFS Resources fallback
orig=build_all.model_parts
build_all.model_parts=lambda name: tmpl.parts(name[5:]) if name.startswith('TMPL:') else orig(name)
m=json.load(open(paths.f('final_map.json')))
plan=build_all.build(m,sys.argv[1])
json.dump(plan,open(sys.argv[1]+'.plan.json','w'))
print('built',len(plan),'DLs ->',sys.argv[1],os.path.getsize(sys.argv[1])//1024//1024,'MB')
