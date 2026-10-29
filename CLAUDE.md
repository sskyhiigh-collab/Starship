# Starship modding fork — handoff notes

This fork (branch `terrain-3ds`) extends Starship (SF64 PC port, v2.0.0 "Barnard Alfa", base cb19785) with runtime
systems for a set of personal `.o2r` mods, plus the Python tools in `modtools/` that build those mods from the
user's own game dumps (Star Fox 64 3D RomFS, Star Fox Zero content, Starship's `sf64.o2r`).

## The user and how to work

- Owner: sskyhiigh-collab. Commit as `-c user.name="sskyhiigh-collab" -c user.email="sskyhiigh@gmail.com"`.
- Usage-cost sensitive: avoid exploratory detours; measure/verify from data before changing things; batch work.
- The user tests in-game and sends screenshots. Visual changes can't be verified from code alone: say what to check.
- Mods live in `starship\mods` (load order = file name order, later wins):
  `0 LR2EB Textures`, `1 LR2EB HD Models` (third-party), `2 SF64 3D Team Models`, `3 Corneria SFA Music`,
  `3 SF64 3D Models`, `4 SF64 3D Terrain`, `5 SFZ Space`, `6 SFZ Models`, `HD boost dial`.
- Bonus-text fix must NOT use the 3DS text.

## Building

- Game: GitHub Actions "GenerateBuilds" on this branch, or locally per Starship's own build docs (Windows: VS 2022
  build tools + CMake). Quick syntax check used so far (Linux):
  `gcc -fsyntax-only -w -Werror=implicit-function-declaration -std=gnu11 -DF3DEX_GBI=1 -DGBI_FLOATS -D_LANGUAGE_C -DNON_MATCHING -DAVOID_UB -I include -I src -I . -I <build>/ -I libultraship/include -I libultraship/include/libultraship -I libultraship/src -I libultraship/src/public -I libultraship/extern -I libultraship/src/public/libultra <file.c>`
- Tools: Python 3.11+, `pip install numpy scipy pillow`; `git clone https://github.com/aboood40091/GTX-Extractor modtools/third_party/GTX-Extractor`.
  Set `SF_ROOT` (default `C:\Users\shaya\Documents\apollo\star fox 64 3d model port`); outputs go to `modtools/out` (`SF_OUT`).
  First run: `python modtools/sf3ds/catalog.py` (writes `modtools/data/catalog.pkl`, the SF64 3D resource index; not in git).

| Mod | Command (from `modtools/`) |
|---|---|
| 3 SF64 3D Models | `python sf3ds/build_models.py "out/3 SF64 3D Models.o2r"` (mapping: `data/final_map.json`, `TMPL:<name>` = city building template from the terrain) |
| 4 SF64 3D Terrain | `python sf3ds/gen_ground.py "out/4 SF64 3D Terrain.o2r"` then `python sf3ds/gen_cfg.py "out/4 SF64 3D Terrain.o2r"` |
| 5 SFZ Space | `python sfz/build_sky.py "out/5 SFZ Space.o2r"` |
| 6 SFZ Models | `python sfz/build_sfz.py "out/6 SFZ Models.o2r"` (table `MODELS` at the top) |
| music | `python music/build_music.py <audio> "out/3 Corneria SFA Music.o2r"` (loop points at the top; stereo = 2 channels/samples) |

`gen_cfg.py` only rewrites the terrain settings (`ast_sf3ds_gnd/config`) and patched object lists inside the
existing terrain .o2r — tweaks there need no rebuild of geometry or of the game.

## Runtime systems (C)

- `src/engine/fox_terrain3ds.c` — 3DS terrain. Everything comes from text resource `ast_sf3ds_gnd/config`
  (format documented at the top of the file: level/sector/fill/fall/hide/waterfirst/lit/light/water/fog/global).
  Hooks: `fox_bg.c` (Background_DrawGround: ground replacement, draw-before-water, extra sea tiles),
  `fox_display.c` (Titania, `Terrain3DS_ApplyFog` after the camera LookAt), `fox_edisplay.c` (Scenery_Draw hide list).
  Ground fill plane is depth-less under the terrain and depth-tested past its end (boss areas).
- `src/engine/fox_backdrop.c` — SFZ sky sphere + layers in place of the starfield dots; config `ast_sfz_sky/config`
  (bd/level/menus/dots/roll). Gameplay uses the exact camera rotation via `Backdrop_SetView` from fox_display.c.
  `menus` is off: level select and title share the same starfield call, splitting them needs code.
- Draw Distance: CVar `gDrawDistanceMul` (Enhancements menu slider, `ImguiUI.cpp`). Scales the far plane
  (`sys_lib.c` Lib_InitPerspective), spawns static scenery early in `Object_LoadLevelObjects` (fox_enmy.c, keeps 12
  scenery slots free), scales terrain cull distance.

## Format notes (hard-won — trust these)

SF64 3D (RomFS, little-endian GDB1 + bin streams; `cat3ds.py`, `modelfull.py`, `geom3ds.py`):
- Node `geometryIndces` arrays are `(type tag, entries...)`; count at +0, entries start after the tag. (An
  off-by-one here once dropped the last geometry of every node — roads/craters/building pieces went missing.)
- Terrain: world = model×100, rails levels shifted z −3000 (object-spawn coords). Corneria city chunks 02–05 have no
  stored placement: ground/other nodes use seam-fitted offsets, `_road` nodes the N64-highway fit (+1.235 model units
  up), `_bases` dropped. Parts far outside their chunk become their own `_x` chunk (bounds drive culling; a stretched
  chunk renders over the camera when drawn beyond the depth range).
- Translucency: only `DepthMask==0` (or crater/shadow decals) is translucent; `TranslucencyKind` alone = "has alpha".
- Materials using fragment lighting (combiner source 8/9) ignore vertex colour and get ×0.6.
- Shading is baked (AO × vertex tint × 3DS ColorScale × directional sun from the level's N64 env rotation);
  scorched-earth gets a warm tint (3DS adds an ember colour at runtime). Per-level brightness: `LEVEL_SHADE`.
- 3DS removed two Corneria trees (patched out of `aCoOnRailsLevelObjects` by gen_cfg); object lists otherwise match.

Star Fox Zero (Wii U, big-endian; `sfz/`):
- `.dat` = PlatinumGames DAT; textures `.wta` (GX2 surface headers, stride 0xC0) + `.wtp` (data), GX2 tiled →
  untile with GTX-Extractor's addrlib, then BC1/BC3 decode (`wtex.py`).
- Stage scenery `.scr`: entries (name, pos/rot/scale at +0x44); model base = entry+0x100; `SCR_MESH` header;
  vertex stride 28 (pos f32×3, uv f16×2 …); u16 triangle LIST right after the header (~+0x102; found by scoring).
- Models `.wmb` = Bayonetta-1 style WMB (`wmb.py`): vertex stride 32 (+8 bytes ex data), meshes → batches
  (material = low u16 of field 1, vertex range, prim 4 = list, indices + vertexOffset). Material's first texture id
  that exists in the archive's .wta is the colour map. Normals are recomputed (packed format unverified).
- Wolfen = `data000/em/em5100.dat` (Body, Glass, pilots wolf/leon/piguma/oikonny); scale ×96.5 to N64; same axes.
  Arwing = `pl0000`. Executable `code/PRJ_030.rpx` (zlib sections) has class/asset names useful for finding models.

## Open items / next steps (agreed order)

1. Verify in-game: Aquas fog (tune in gen_cfg `fog`), Wolfen scale/engine-glow position.
2. SFZ model batches → `6 SFZ Models.o2r`: send the user a mapping list (N64 DL ↔ SFZ asset) before each batch.
   The user wants ALL enemies on SFZ models; static props/ships first, skinned enemies need per-limb mapping.
   Falls back to the 3DS model when there is no counterpart.
3. Modern lighting (libultraship renderer: per-pixel lighting → normal maps → rim/specular/reflections), staged.
Known issues: bonus/hit text missing (not caused by mod data; ask the user to A/B test without mod 3),
Sector Y "PlanetA" + ring in the SFZ sky don't decode (excluded), Wolfen pilots excluded (one shared DL for all 4),
Venom's upgraded Wolfen uses the standard body.
