# Central paths for the mod tools. Set SF_ROOT to the folder that holds romfs/, starship/ and "Star Fox Zero (USA)/".
import os
ROOT=os.environ.get('SF_ROOT', r'C:\Users\shaya\Documents\apollo\star fox 64 3d model port')
ROMFS=os.path.join(ROOT,'romfs','0004000000049000')+os.sep          # SF64 3D RomFS (extracted)
SF64_O2R=os.path.join(ROOT,'starship','sf64.o2r')                   # Starship's extracted N64 assets
SFZ_CONTENT=os.path.join(ROOT,'Star Fox Zero (USA)','content')      # SFZ content with the .cpk archives unpacked
TOOLS=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(TOOLS,'data')                                     # hand-made tables (mappings, hide lists, ...)
OUT=os.environ.get('SF_OUT',os.path.join(TOOLS,'out'))              # generated tables and built .o2r files
GTX=os.path.join(TOOLS,'third_party','GTX-Extractor')               # git clone https://github.com/aboood40091/GTX-Extractor
os.makedirs(OUT,exist_ok=True)
_DATA_FILES={'final_map.json','hide_ids.json','fill_tex.json','lr2eb_dls.json','catalog.pkl'}
def f(name):
    """resolve a bare table/file name: hand-made tables live in data/, generated ones in out/"""
    return os.path.join(DATA if name in _DATA_FILES else OUT, name)
