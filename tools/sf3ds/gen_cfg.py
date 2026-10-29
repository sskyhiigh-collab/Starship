import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
# Writes ast_sf3ds_gnd/config (text, LUS Blob resource) into the terrain .o2r.
# Hand-tweakable values live in TWEAKS below; everything else comes from gnd_table.json / gnd_fill.json.
import json,struct,sys,zipfile,shutil,os
LEVEL_ID={'CORNERIA':0,'VENOM_1':6,'TRAINING':10,'MACBETH':11,'TITANIA':12,'AQUAS':13,'VENOM_2':19}
HIDE={'CORNERIA':[0,1,2,3,4,5,6,7,8,9,11,13,24,25,26,27,28,54,55],'MACBETH':[59,60,62,63]+list(range(66,76)),
      'AQUAS':[117,118,119,120,121,122,124,125],'VENOM_1':[50,51,53],'VENOM_2':[160]}
TWEAKS=dict(
    light={'*':(110,1.5)},                 # ambient added to the level's ambient, multiplier on its sun colour
    waterfirst={'CORNERIA':1},
    water={'CORNERIA':(6,2)},
    fog={'AQUAS':(12,38,52,500,5500)},     # r g b start end (world units): thick underwater fog like SF64 3D              # extra N64 sea tiles: rows ahead, columns each side
    fall_speed=[1.5,0.5],                  # texels per frame: falling sheet, foam
    fill_grid=(3,1,3),                     # tiles left/right, behind, ahead
    fill_levels={'CORNERIA','MACBETH','TITANIA','VENOM_1'},   # static ground plane replaces the N64 ground
    cull=(4000,40000), yoffset=-3.0)
def build(T,F):
    L=['# Star Fox 64 3D terrain config (read by Starship at runtime; edit and repack, no rebuild needed)',
       f'global cull {TWEAKS["cull"][0]} {TWEAKS["cull"][1]}', f'global yoffset {TWEAKS["yoffset"]}','']
    for lv,v in T.items():
        L.append(f'level {LEVEL_ID[lv]} {lv} {"allrange" if v.get("allrange") else "rails"} {v["length"]:.1f} {int(v["repeat"])} {float(v["hideafter"]):.1f}')
        a,m=TWEAKS['light'].get(lv,TWEAKS['light']['*']); L.append(f'light {a} {m}')
        if TWEAKS['waterfirst'].get(lv): L.append('waterfirst 1')
        if lv in TWEAKS['water']: L.append('water %d %d'%TWEAKS['water'][lv])
        if lv in TWEAKS['fog']: L.append('fog %d %d %d %.0f %.0f'%TWEAKS['fog'][lv])
        if lv in HIDE: L.append('hide '+' '.join(map(str,HIDE[lv])))
        if lv in F and lv in TWEAKS['fill_levels']: g=TWEAKS['fill_grid']; L.append(f'fill {F[lv]["dl"]} {F[lv]["tile"]:.1f} {g[0]} {g[1]} {g[2]}')
        for r in v['rows']:
            L.append(f'sector {r["dl"]} {r["ox"]:.1f} {r["oz"]:.1f} {r["f"]:.1f} {r["zmin"]:.1f} {r["zmax"]:.1f}')
        for r in v['rows']:
            if 'wf' in r:
                w=r['wf']; ps=' '.join(f'{d[0]} {d[1]} {s}' for d,s in zip(w['parts'],w.get('speeds',TWEAKS['fall_speed'])))
                L.append(f'fall {w["dl"]} {r["ox"]:.1f} {r["oz"]:.1f} {r["f"]:.1f} {r["zmin"]:.1f} {r["zmax"]:.1f} {len(w["parts"])} {ps}')
        L.append('')
    return '\n'.join(L)
# N64 scenery that SF64 3D removed from the level's object list (removing them also removes their collision)
REMOVE={'ast_corneria/aCoOnRailsLevelObjects':[(138317.7,-4035,857,162),(138319.7,-4035,483,162)]}
def objlists():
    SF=paths.SF64_O2R
    out={}
    with zipfile.ZipFile(SF) as z:
        for path,rm in REMOVE.items():
            raw=z.read(path); hdr,d=raw[:0x40],raw[0x40:]; n=struct.unpack_from('<I',d)[0]
            keep=[]; dropped=0
            for k in range(n):
                e=d[4+18*k:4+18*k+18]; zp1,zp2,x,y,rx,ry,rz,oid=struct.unpack('<fhhhhhhh',e)
                if any(abs(zp1-a)<0.2 and zp2==b and x==c and oid==i for a,b,c,i in rm): dropped+=1; continue
                keep.append(e)
            assert dropped==len(rm),(path,dropped)
            out[path]=hdr+struct.pack('<I',len(keep))+b''.join(keep)+d[4+18*n:]
    return out
def blob(text):
    d=text.encode()+b'\0'
    hdr=struct.pack('<IIIII',0,0x4F424C42,0,0xDEADBEEF,0xDEADBEEF)+bytes(0x40-20)
    return hdr+struct.pack('<I',len(d))+d
if __name__=='__main__':
    T=json.load(open(paths.f('gnd_table.json'))); F=json.load(open(paths.f('gnd_fill.json')))
    text=build(T,F); open(paths.f('terrain_config.txt'),'w').write(text)
    if len(sys.argv)>1:
        o2r=sys.argv[1]; tmp=o2r+'.tmp'
        with zipfile.ZipFile(o2r) as zi, zipfile.ZipFile(tmp,'w',zipfile.ZIP_STORED) as zo:
            for it in zi.infolist():
                if it.filename!='ast_sf3ds_gnd/config' and it.filename not in REMOVE: zo.writestr(it,zi.read(it.filename))
            zo.writestr('ast_sf3ds_gnd/config',blob(text))
            for path,data in objlists().items(): zo.writestr(path,data)
        os.replace(tmp,o2r)
    print(text[:1500]); print('...',len(text),'chars')
