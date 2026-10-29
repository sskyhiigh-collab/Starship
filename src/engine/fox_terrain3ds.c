// Star Fox 64 3D terrain drawn in place of / over the N64 ground.
//
// Everything level-specific (sectors, placement, fill planes, waterfalls, hidden scenery, lighting) is read at
// runtime from the text resource "ast_sf3ds_gnd/config" inside the terrain .o2r mod, so tweaks only need a new
// .o2r, not a new build. Without that resource (mod not installed) nothing here does anything.
//
// Config format: one directive per line, '#' starts a comment. Directives apply to the latest "level" line.
//   level <id> <name> <rails|allrange> <sectorLength> <repeatLast 0/1> <hideAfter>
//   sector <dl> <ox> <oz> <scale> <zmin> <zmax>
//   fill <dl> <tileSize> <gridX> <gridZnear> <gridZfar>
//   fall <dl> <ox> <oz> <scale> <zmin> <zmax> <parts 1-4> then <texW> <texH> <speed> per part
//   hide <objId> <objId> ...
//   waterfirst <0/1>          draw the terrain before the N64 water when the ground surface is water
//   light <ambientAdd> <diffuseMul>  dynamic lighting (only with lit 1)
//   lit <0/1>                 0: shading baked into vertex colours (default), 1: lit with vertex normals
//   water <rowsAhead> <halfColumns>  extra N64 water tiles ahead of / beside the default ones (over water only)
//   global cull <near> <far>
//   global yoffset <y>
#include "global.h"

#define T3DS_MAX_LEVELS 12
#define T3DS_MAX_SECTORS 192
#define T3DS_MAX_FALLS 8
#define T3DS_MAX_HIDE 64
#define T3DS_POOL 32768

typedef struct {
    const char* dl;
    f32 ox, oz, scale, zmin, zmax;
} T3DSSector;

typedef struct {
    const char* mat[4];
    const char* tri[4];
    s32 n;
    s32 dw[4], dh[4];
    f32 speed[4];
    f32 ox, oz, scale, zmin, zmax;
    s32 level;
} T3DSFall;

typedef struct {
    s32 level;
    s32 allRange;
    f32 length;
    s32 repeatLast;
    f32 hideAfter;
    s32 firstSector;
    s32 sectorCount;
    const char* fillDl;
    f32 fillTile;
    s32 fillGridX, fillGridNear, fillGridFar;
    s16 hide[T3DS_MAX_HIDE];
    s32 hideCount;
    s32 waterFirst;
    f32 ambientAdd;
    f32 diffuseMul;
    s32 lit;
    s32 waterRows;
    s32 waterCols;
} T3DSLevel;

static T3DSLevel sLevels[T3DS_MAX_LEVELS];
static s32 sLevelCount = 0;
static T3DSSector sSectors[T3DS_MAX_SECTORS];
static s32 sSectorCount = 0;
static T3DSFall sFalls[T3DS_MAX_FALLS];
static s32 sFallCount = 0;
static char sPool[T3DS_POOL];
static s32 sPoolUsed = 0;
static f32 sCullNear = 4000.0f;
static f32 sCullFar = 40000.0f;
static f32 sYOffset = -3.0f;
static s32 sLoaded = 0; // 0 = not tried, 1 = loaded, -1 = no config

// "__OTR__" + path, kept alive for the display list commands
static const char* T3DS_Intern(const char* path, const char* suffix) {
    s32 len = strlen("__OTR__") + strlen(path) + strlen(suffix) + 1;
    char* out;
    if (sPoolUsed + len > T3DS_POOL) {
        return NULL;
    }
    out = &sPool[sPoolUsed];
    sprintf(out, "__OTR__%s%s", path, suffix);
    sPoolUsed += len;
    return out;
}

static void T3DS_ParseLine(char* line) {
    char cmd[32];
    char a[160];
    char b[32];
    T3DSLevel* lv = (sLevelCount > 0) ? &sLevels[sLevelCount - 1] : NULL;
    char* p;
    s32 n = 0;

    if ((p = strchr(line, '#')) != NULL) {
        *p = '\0';
    }
    if (sscanf(line, "%31s%n", cmd, &n) != 1) {
        return;
    }
    p = line + n;

    if (!strcmp(cmd, "global")) {
        f32 x, y = 0.0f;
        if (sscanf(p, "%31s %f %f", b, &x, &y) >= 2) {
            if (!strcmp(b, "cull")) {
                sCullNear = x;
                sCullFar = y;
            } else if (!strcmp(b, "yoffset")) {
                sYOffset = x;
            }
        }
        return;
    }
    if (!strcmp(cmd, "level") && (sLevelCount < T3DS_MAX_LEVELS)) {
        T3DSLevel* l = &sLevels[sLevelCount];
        s32 id;
        memset(l, 0, sizeof(*l));
        if (sscanf(p, "%d %159s %31s %f %d %f", &id, a, b, &l->length, &l->repeatLast, &l->hideAfter) == 6) {
            l->level = id;
            l->allRange = !strcmp(b, "allrange");
            l->firstSector = sSectorCount;
            l->ambientAdd = 110.0f;
            l->diffuseMul = 1.5f;
            sLevelCount++;
        }
    } else if (lv == NULL) {
        return;
    } else if (!strcmp(cmd, "sector") && (sSectorCount < T3DS_MAX_SECTORS)) {
        T3DSSector* s = &sSectors[sSectorCount];
        if (sscanf(p, "%159s %f %f %f %f %f", a, &s->ox, &s->oz, &s->scale, &s->zmin, &s->zmax) == 6) {
            s->dl = T3DS_Intern(a, "");
            if (s->dl != NULL) {
                sSectorCount++;
                lv->sectorCount++;
            }
        }
    } else if (!strcmp(cmd, "fill")) {
        lv->fillGridX = 3;
        lv->fillGridNear = 1;
        lv->fillGridFar = 3;
        if (sscanf(p, "%159s %f %d %d %d", a, &lv->fillTile, &lv->fillGridX, &lv->fillGridNear, &lv->fillGridFar) >=
            2) {
            lv->fillDl = T3DS_Intern(a, "");
        }
    } else if (!strcmp(cmd, "fall") && (sFallCount < T3DS_MAX_FALLS)) {
        T3DSFall* f = &sFalls[sFallCount];
        memset(f, 0, sizeof(*f));
        if (sscanf(p, "%159s %f %f %f %f %f %d%n", a, &f->ox, &f->oz, &f->scale, &f->zmin, &f->zmax, &f->n, &n) == 7) {
            s32 k;
            p += n;
            f->n = CLAMP(f->n, 1, 4);
            f->level = lv->level;
            for (k = 0; k < f->n; k++) {
                char sfx[8];
                if (sscanf(p, "%d %d %f%n", &f->dw[k], &f->dh[k], &f->speed[k], &n) != 3) {
                    f->n = k;
                    break;
                }
                p += n;
                sprintf(sfx, "_mat%d", k);
                f->mat[k] = T3DS_Intern(a, sfx);
                sprintf(sfx, "_tri%d", k);
                f->tri[k] = T3DS_Intern(a, sfx);
            }
            if ((f->n > 0) && (f->mat[f->n - 1] != NULL) && (f->tri[f->n - 1] != NULL)) {
                sFallCount++;
            }
        }
    } else if (!strcmp(cmd, "hide")) {
        s32 id;
        while ((sscanf(p, "%d%n", &id, &n) == 1) && (lv->hideCount < T3DS_MAX_HIDE)) {
            lv->hide[lv->hideCount++] = id;
            p += n;
        }
    } else if (!strcmp(cmd, "waterfirst")) {
        sscanf(p, "%d", &lv->waterFirst);
    } else if (!strcmp(cmd, "lit")) {
        sscanf(p, "%d", &lv->lit);
    } else if (!strcmp(cmd, "water")) {
        sscanf(p, "%d %d", &lv->waterRows, &lv->waterCols);
    } else if (!strcmp(cmd, "light")) {
        sscanf(p, "%f %f", &lv->ambientAdd, &lv->diffuseMul);
    }
}

static void T3DS_Load(void) {
    const char* data;
    size_t size;
    char line[512];
    size_t i;
    s32 len = 0;

    sLoaded = -1;
    data = (const char*) ResourceGetDataByName("ast_sf3ds_gnd/config");
    if (data == NULL) {
        return;
    }
    size = ResourceGetSizeByName("ast_sf3ds_gnd/config");
    for (i = 0; i <= size; i++) {
        char c = (i < size) ? data[i] : '\n';
        if ((c == '\n') || (c == '\r') || (c == '\0')) {
            line[len] = '\0';
            T3DS_ParseLine(line);
            len = 0;
            if (c == '\0') {
                break;
            }
        } else if (len < (s32) sizeof(line) - 1) {
            line[len++] = c;
        }
    }
    if (sLevelCount > 0) {
        sLoaded = 1;
    }
}

static const T3DSLevel* Terrain3DS_GetLevel(void) {
    static s32 sCheckedLevel = -1;
    static const T3DSLevel* sCur = NULL;
    s32 i;

    if (sLoaded == 0) {
        T3DS_Load();
    }
    if (sLoaded != 1) {
        return NULL;
    }
    if (sCheckedLevel != gCurrentLevel) {
        sCheckedLevel = gCurrentLevel;
        sCur = NULL;
        for (i = 0; i < sLevelCount; i++) {
            if ((sLevels[i].level == gCurrentLevel) && (sLevels[i].sectorCount > 0)) {
                sCur = &sLevels[i];
                break;
            }
        }
    }
    if (sCur == NULL) {
        return NULL;
    }
    // only during actual gameplay (not the title screen / menus, where the default level is Corneria)
    if (gGameState != GSTATE_PLAY) {
        return NULL;
    }
    if ((sCur->allRange != 0) != (gLevelMode == LEVELMODE_ALL_RANGE)) {
        return NULL;
    }
    return sCur;
}

bool Terrain3DS_Active(void) {
    return Terrain3DS_GetLevel() != NULL;
}

// True when the static 3DS ground plane replaces the N64 ground (not over water, where the N64 water surface stays).
bool Terrain3DS_ReplacesGround(void) {
    const T3DSLevel* lv = Terrain3DS_GetLevel();
    return (lv != NULL) && (lv->fillDl != NULL) && (gGroundSurface != SURFACE_WATER);
}

// Over water, draw the terrain before the N64 water so the (depth-tested) water covers submerged parts.
bool Terrain3DS_DrawBeforeWater(void) {
    const T3DSLevel* lv = Terrain3DS_GetLevel();
    return (lv != NULL) && lv->waterFirst && (gGroundSurface == SURFACE_WATER);
}

// Extra N64 water tiles (rows ahead, columns to each side) so the sea reaches the fog over the 3DS terrain.
s32 Terrain3DS_WaterRows(void) {
    const T3DSLevel* lv = Terrain3DS_GetLevel();
    return (lv != NULL) ? lv->waterRows : 0;
}

s32 Terrain3DS_WaterCols(void) {
    const T3DSLevel* lv = Terrain3DS_GetLevel();
    return (lv != NULL) ? lv->waterCols : 0;
}

// N64 scenery that SF64 3D never draws on this level because its terrain already contains it.
// Only drawing is skipped; collision and game logic are untouched.
bool Terrain3DS_HidesScenery(s32 id) {
    const T3DSLevel* lv = Terrain3DS_GetLevel();
    s32 i;
    if (lv == NULL) {
        return false;
    }
    for (i = 0; i < lv->hideCount; i++) {
        if (lv->hide[i] == id) {
            return true;
        }
    }
    return false;
}

static void Terrain3DS_DrawSector(const T3DSSector* s, f32 zShift) {
    f32 zNear = s->zmax + zShift + gPathProgress;
    f32 zFar = s->zmin + zShift + gPathProgress;

    if ((zFar > sCullNear) || (zNear < -sCullFar * CLAMP(CVarGetFloat("gDrawDistanceMul", 1.0f), 1.0f, 8.0f))) {
        return;
    }
    Matrix_Push(&gGfxMatrix);
    Matrix_Translate(gGfxMatrix, s->ox, sYOffset + gCameraShakeY, s->oz + zShift + gPathProgress, MTXF_APPLY);
    if (s->scale != 1.0f) {
        Matrix_Scale(gGfxMatrix, s->scale, s->scale, s->scale, MTXF_APPLY);
    }
    Matrix_SetGfxMtx(&gMasterDisp);
    gSPDisplayList(gMasterDisp++, (Gfx*) s->dl);
    Matrix_Pop(&gGfxMatrix);
}

void Terrain3DS_Draw(void) {
    const T3DSLevel* lv = Terrain3DS_GetLevel();
    const T3DSSector* secs;
    s32 i;
    s32 k;

    if (lv == NULL) {
        return;
    }
    if ((lv->hideAfter > 0.0f) && (gPathProgress > lv->hideAfter)) {
        return;
    }
    secs = &sSectors[lv->firstSector];

    // static ground plane (3DS ground texture) in place of the scrolling N64 ground.
    // Under the terrain it is a depth-less backdrop (it can't cut through dips in the terrain); past the end of the
    // terrain (boss areas) it is depth-tested like the N64 ground, so objects can sink into it.
    if ((lv->fillDl != NULL) && (lv->allRange == 0) && (gGroundSurface != SURFACE_WATER) && (lv->fillTile > 0.0f)) {
        f32 tile = lv->fillTile;
        f32 camZ = floorf(-gPathProgress / tile) * tile;
        f32 terrainEnd = 0.0f;
        s32 gx, gz, pass;
        for (i = 0; i < lv->sectorCount; i++) {
            terrainEnd = MIN(terrainEnd, secs[i].zmin);
        }
        if (lv->repeatLast) {
            terrainEnd = -1.0e30f;
        }
        for (pass = 0; pass < 2; pass++) {
            if (pass == 0) {
                RCP_SetupDL_20(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
            } else {
                RCP_SetupDL_29(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
            }
            gSPClearGeometryMode(gMasterDisp++, G_LIGHTING | G_CULL_BACK);
            for (gz = -lv->fillGridNear; gz <= lv->fillGridFar; gz++) {
                f32 centre = camZ - gz * tile;
                s32 beyond = (centre + tile * 0.5f) < terrainEnd;
                if (beyond != pass) {
                    continue;
                }
                for (gx = -lv->fillGridX; gx <= lv->fillGridX; gx++) {
                    Matrix_Push(&gGfxMatrix);
                    Matrix_Translate(gGfxMatrix, gx * tile, sYOffset + gCameraShakeY, centre + gPathProgress, MTXF_APPLY);
                    Matrix_SetGfxMtx(&gMasterDisp);
                    gSPDisplayList(gMasterDisp++, (Gfx*) lv->fillDl);
                    Matrix_Pop(&gGfxMatrix);
                }
            }
        }
    }

    // lit with the level's sun direction; brighter ambient than the N64 object lighting so slopes facing away
    // from the sun don't go black
    RCP_SetupDL_29(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
    if (!lv->lit) {
        // shading (3DS ambient occlusion, vertex tint and the level's sun direction) is baked into the vertex colours
        gSPClearGeometryMode(gMasterDisp++, G_LIGHTING | G_CULL_BACK);
    } else {
        gSPClearGeometryMode(gMasterDisp++, G_CULL_BACK); // terrain is drawn two-sided on 3DS
    }
    if (lv->lit) Lights_SetOneLight(&gMasterDisp, gLight1x, gLight1y, gLight1z, MIN(255, (s32) (gLight1R * lv->diffuseMul)),
                       MIN(255, (s32) (gLight1G * lv->diffuseMul)), MIN(255, (s32) (gLight1B * lv->diffuseMul)),
                       MIN(255, (s32) (gAmbientR + lv->ambientAdd)), MIN(255, (s32) (gAmbientG + lv->ambientAdd)),
                       MIN(255, (s32) (gAmbientB + lv->ambientAdd)));
    for (i = 0; i < lv->sectorCount; i++) {
        Terrain3DS_DrawSector(&secs[i], 0.0f);
    }
    if (lv->repeatLast && (lv->allRange == 0)) {
        for (k = 1; k <= 8; k++) {
            Terrain3DS_DrawSector(&secs[lv->sectorCount - 1], -lv->length * k);
        }
    }
    // restore the scene lighting for whatever is drawn next
    if (lv->lit) Lights_SetOneLight(&gMasterDisp, gLight1x, gLight1y, gLight1z, gLight1R, gLight1G, gLight1B, gAmbientR, gAmbientG,
                       gAmbientB);

    // waterfalls: unlit translucent sheets with the texture scrolling downwards
    for (i = 0; i < sFallCount; i++) {
        const T3DSFall* w = &sFalls[i];
        f32 zNear;
        f32 zFar;
        if ((w->level != lv->level) || (lv->allRange != 0)) {
            continue;
        }
        zNear = w->zmax + gPathProgress;
        zFar = w->zmin + gPathProgress;
        if ((zFar > sCullNear) || (zNear < -sCullFar * CLAMP(CVarGetFloat("gDrawDistanceMul", 1.0f), 1.0f, 8.0f))) {
            continue;
        }
        RCP_SetupDL_29(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
        gSPClearGeometryMode(gMasterDisp++, G_LIGHTING | G_CULL_BACK);
        gDPSetRenderMode(gMasterDisp++, G_RM_FOG_SHADE_A, G_RM_AA_ZB_XLU_SURF2);
        Matrix_Push(&gGfxMatrix);
        Matrix_Translate(gGfxMatrix, w->ox, sYOffset + gCameraShakeY, w->oz + gPathProgress, MTXF_APPLY);
        if (w->scale != 1.0f) {
            Matrix_Scale(gGfxMatrix, w->scale, w->scale, w->scale, MTXF_APPLY);
        }
        Matrix_SetGfxMtx(&gMasterDisp);
        for (k = 0; k < w->n; k++) {
            // speed in texels per frame; positive moves the texture towards increasing T
            s32 period = MAX(1, w->dh[k]) << 2;
            s32 t = ((s32) (gGameFrameCount * w->speed[k] * -4.0f)) % period;
            if (t < 0) {
                t += period;
            }
            gSPDisplayList(gMasterDisp++, (Gfx*) w->mat[k]);
            gDPSetTileSize(gMasterDisp++, G_TX_RENDERTILE, 0, t, (w->dw[k] - 1) << 2, t + ((w->dh[k] - 1) << 2));
            gSPDisplayList(gMasterDisp++, (Gfx*) w->tri[k]);
        }
        Matrix_Pop(&gGfxMatrix);
    }
}
