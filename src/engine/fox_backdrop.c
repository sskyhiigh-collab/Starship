// Space backdrops (sky sphere + nebula/galaxy/planet layers) drawn in place of the starfield dots.
//
// Everything comes from the text resource "ast_sfz_sky/config" inside a .o2r mod, so backdrops can be added or
// reassigned without a rebuild. Without that resource nothing changes. Format, one directive per line ('#' comment):
//   bd <name> <skyDL> [<layersDL>]   declare a backdrop
//   level <levelId> <name>           backdrop for a level (gameplay)
//   menus <name>                     backdrop for the title screen and other non-gameplay full-screen starfields
//   dots <0/1>                       also draw the original star dots on top (default 0)
//   roll <1/-1>                      direction the sky follows the camera roll (default 1)
#include "global.h"

extern float gCurrentScreenWidth;
extern float gCurrentScreenHeight;

static s32 Backdrop_Int(const char* s) {
    s32 v = 0;
    sscanf(s, "%d", &v);
    return v;
}

#define BD_MAX 16
#define BD_LEVELS 32

typedef struct {
    char name[16];
    char sky[96];
    char fx[96];
} Backdrop;

static Backdrop sBackdrops[BD_MAX];
static s32 sBackdropCount = 0;
static s8 sLevelBackdrop[BD_LEVELS];
static s8 sMenuBackdrop = -1;
static s32 sKeepDots = 0;
static f32 sRollSign = 1.0f;
static s32 sBackdropLoaded = 0;

static Gfx sBackdropSetupDL[] = {
    gsDPPipeSync(),
    gsSPClearGeometryMode(G_ZBUFFER | G_SHADE | G_CULL_BOTH | G_FOG | G_LIGHTING | G_TEXTURE_GEN |
                          G_TEXTURE_GEN_LINEAR | G_LOD | G_SHADING_SMOOTH),
    gsSPSetGeometryMode(G_SHADE | G_SHADING_SMOOTH),
    gsSPTexture(0xFFFF, 0xFFFF, 0, G_TX_RENDERTILE, G_ON),
    gsDPSetCombineMode(G_CC_MODULATEIA, G_CC_MODULATEIA),
    gsDPSetOtherMode(G_AD_NOTPATTERN | G_CD_MAGICSQ | G_CK_NONE | G_TC_FILT | G_TF_BILERP | G_TT_NONE | G_TL_TILE |
                         G_TD_CLAMP | G_TP_PERSP | G_CYC_1CYCLE | G_PM_NPRIMITIVE,
                     G_AC_NONE | G_ZS_PIXEL | G_RM_OPA_SURF | G_RM_OPA_SURF2),
    gsSPEndDisplayList(),
};

static s32 Backdrop_Find(const char* name) {
    s32 i;
    for (i = 0; i < sBackdropCount; i++) {
        if (!strcmp(sBackdrops[i].name, name)) {
            return i;
        }
    }
    return -1;
}

static void Backdrop_ParseLine(char* line) {
    char cmd[16];
    char a[96];
    char b[96];
    char c[96];
    s32 id;
    s32 n;
    char* p = strchr(line, '#');

    if (p != NULL) {
        *p = '\0';
    }
    n = sscanf(line, "%15s %95s %95s %95s", cmd, a, b, c);
    if (n < 2) {
        return;
    }
    if (!strcmp(cmd, "bd") && (n >= 3) && (sBackdropCount < BD_MAX)) {
        Backdrop* bd = &sBackdrops[sBackdropCount];
        snprintf(bd->name, sizeof(bd->name), "%s", a);
        snprintf(bd->sky, sizeof(bd->sky), "__OTR__%s", b);
        if (n >= 4) {
            snprintf(bd->fx, sizeof(bd->fx), "__OTR__%s", c);
        } else {
            bd->fx[0] = '\0';
        }
        // only keep backdrops whose display lists are actually present
        if (ResourceGetDataByName(bd->sky + 7) != NULL) {
            sBackdropCount++;
        }
    } else if (!strcmp(cmd, "level") && (n >= 3)) {
        id = Backdrop_Int(a);
        if ((id >= 0) && (id < BD_LEVELS)) {
            sLevelBackdrop[id] = Backdrop_Find(b);
        }
    } else if (!strcmp(cmd, "menus")) {
        sMenuBackdrop = Backdrop_Find(a);
    } else if (!strcmp(cmd, "dots")) {
        sKeepDots = Backdrop_Int(a);
    } else if (!strcmp(cmd, "roll")) {
        sRollSign = (Backdrop_Int(a) < 0) ? -1.0f : 1.0f;
    }
}

static void Backdrop_Load(void) {
    const char* data;
    size_t size;
    size_t i;
    char line[256];
    s32 len = 0;

    sBackdropLoaded = 1;
    for (i = 0; i < BD_LEVELS; i++) {
        sLevelBackdrop[i] = -1;
    }
    data = (const char*) ResourceGetDataByName("ast_sfz_sky/config");
    if (data == NULL) {
        return;
    }
    size = ResourceGetSizeByName("ast_sfz_sky/config");
    for (i = 0; i <= size; i++) {
        char ch = (i < size) ? data[i] : '\n';
        if ((ch == '\n') || (ch == '\r') || (ch == '\0')) {
            line[len] = '\0';
            Backdrop_ParseLine(line);
            len = 0;
            if (ch == '\0') {
                break;
            }
        } else if (len < (s32) sizeof(line) - 1) {
            line[len++] = ch;
        }
    }
}

static const Backdrop* Backdrop_Current(void) {
    s32 idx = -1;

    if (!sBackdropLoaded) {
        Backdrop_Load();
    }
    if (gGameState == GSTATE_PLAY) {
        if ((gCurrentLevel >= 0) && (gCurrentLevel < BD_LEVELS)) {
            idx = sLevelBackdrop[gCurrentLevel];
        }
    } else {
        idx = sMenuBackdrop;
    }
    return (idx >= 0) ? &sBackdrops[idx] : NULL;
}

// Draws the backdrop for the current level/screen. Returns true when the original star dots should be skipped.
bool Backdrop_Draw(void) {
    const Backdrop* bd = Backdrop_Current();
    f32 yaw;
    f32 pitch;

    if (bd == NULL) {
        return false;
    }

    Lib_InitPerspective(&gMasterDisp);
    gSPDisplayList(gMasterDisp++, sBackdropSetupDL);

    // Orientation: in gameplay the sky follows the camera exactly; elsewhere it follows the starfield scroll
    // (one full screen of scroll = one full turn), which is what the menus animate.
    if ((gGameState == GSTATE_PLAY) && (gPlayer != NULL)) {
        f32 dx = gPlayer[0].cam.at.x - gPlayer[0].cam.eye.x;
        f32 dy = gPlayer[0].cam.at.y - gPlayer[0].cam.eye.y;
        f32 dz = gPlayer[0].cam.at.z - gPlayer[0].cam.eye.z;
        yaw = Math_Atan2F(dx, -dz);
        pitch = Math_Atan2F(dy, sqrtf(SQ(dx) + SQ(dz)));
    } else {
        yaw = gStarfieldX / MAX(1.0f, gCurrentScreenWidth) * 2.0f * M_PI;
        pitch = gStarfieldY / MAX(1.0f, gCurrentScreenHeight) * 0.25f * M_PI;
    }

    Matrix_Push(&gGfxMatrix);
    Matrix_RotateZ(gGfxMatrix, sRollSign * gStarfieldRoll, MTXF_NEW);
    Matrix_RotateX(gGfxMatrix, pitch, MTXF_APPLY);
    Matrix_RotateY(gGfxMatrix, yaw, MTXF_APPLY);
    Matrix_SetGfxMtx(&gMasterDisp);

    gSPDisplayList(gMasterDisp++, (Gfx*) bd->sky);
    if (bd->fx[0] != '\0') {
        gDPPipeSync(gMasterDisp++);
        gDPSetRenderMode(gMasterDisp++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
        gSPDisplayList(gMasterDisp++, (Gfx*) bd->fx);
    }
    Matrix_Pop(&gGfxMatrix);

    gDPPipeSync(gMasterDisp++);
    gDPSetColorDither(gMasterDisp++, G_CD_MAGICSQ);
    return !sKeepDots;
}
