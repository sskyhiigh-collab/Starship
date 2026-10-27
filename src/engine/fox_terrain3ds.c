// Generated: 3DS (Star Fox 64 3D) terrain sectors drawn over the N64 ground.
// Active only when the matching "ast_sf3ds_gnd/*" display lists are present in a loaded .o2r mod.
#include "global.h"

typedef struct { const char* dl; f32 ox, oz, scale, zmin, zmax; } Terrain3DSSector;
typedef struct { s32 level; s32 allRange; const Terrain3DSSector* secs; s32 count; f32 length; s32 repeatLast; f32 hideAfter; } Terrain3DSLevel;

static const Terrain3DSSector sTerrain3DS_Corneria[] = {
    { "__OTR__ast_sf3ds_gnd/corneria_01", 140.0f, -37820.0f, 1.0f, -43038.5f, -32602.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_02", 19.0f, -48072.0f, 1.0f, -53200.4f, -42943.4f },
    { "__OTR__ast_sf3ds_gnd/corneria_03", 18.0f, -58308.0f, 1.0f, -63418.2f, -53196.8f },
    { "__OTR__ast_sf3ds_gnd/corneria_04", 21.0f, -68049.0f, 1.0f, -73631.6f, -62467.2f },
    { "__OTR__ast_sf3ds_gnd/corneria_05", 23.0f, -78388.0f, 1.0f, -83882.2f, -72893.6f },
    { "__OTR__ast_sf3ds_gnd/corneria_06", 23.0f, -88791.0f, 1.0f, -94397.3f, -83184.5f },
    { "__OTR__ast_sf3ds_gnd/corneria_07", 20.0f, -99202.0f, 1.0f, -104388.6f, -94014.7f },
    { "__OTR__ast_sf3ds_gnd/corneria_08", 8.0f, -109230.0f, 1.0f, -114501.1f, -103958.2f },
    { "__OTR__ast_sf3ds_gnd/corneria_09", 25.0f, -119602.0f, 1.0f, -124713.6f, -114490.9f },
    { "__OTR__ast_sf3ds_gnd/corneria_10", 26.0f, -129854.0f, 1.0f, -134999.6f, -124708.1f },
    { "__OTR__ast_sf3ds_gnd/corneria_11", 27.0f, -140062.0f, 1.0f, -145200.0f, -134923.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_12", 27.0f, -149804.0f, 1.0f, -154467.5f, -145140.5f },
    { "__OTR__ast_sf3ds_gnd/corneria_13", 28.0f, -160378.0f, 1.0f, -165607.7f, -155148.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_14", 304.0f, -171060.0f, 1.0f, -176573.4f, -165546.6f },
    { "__OTR__ast_sf3ds_gnd/corneria_15", 2239.0f, -180875.0f, 1.0f, -186012.1f, -175738.1f },
    { "__OTR__ast_sf3ds_gnd/corneria_16", 2402.0f, -191125.0f, 1.0f, -196327.0f, -185923.0f },
    { "__OTR__ast_sf3ds_gnd/corneria_17", 4382.0f, -201295.0f, 1.0f, -206440.5f, -196149.5f },
};
static const Terrain3DSSector sTerrain3DS_Macbeth[] = {
    { "__OTR__ast_sf3ds_gnd/macbeth_01", 0.0f, -2340.0f, 1.0f, -8100.0f, 3420.7f },
    { "__OTR__ast_sf3ds_gnd/macbeth_02", 1078.0f, -23933.0f, 1.0f, -40533.2f, -7333.0f },
    { "__OTR__ast_sf3ds_gnd/macbeth_03", 0.0f, -23294.0f, 1.0f, -28776.8f, -17811.6f },
    { "__OTR__ast_sf3ds_gnd/macbeth_04", 1041.0f, -34303.0f, 1.0f, -40471.0f, -28135.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_05", 0.0f, -44133.0f, 1.0f, -50841.6f, -37425.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_06", 0.0f, -53867.0f, 1.0f, -60295.0f, -47438.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_07", 0.0f, -64459.0f, 1.0f, -71558.8f, -57358.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_08", 0.0f, -74129.0f, 1.0f, -79545.1f, -68713.3f },
    { "__OTR__ast_sf3ds_gnd/macbeth_09", 0.0f, -84280.0f, 1.0f, -89858.7f, -78701.5f },
    { "__OTR__ast_sf3ds_gnd/macbeth_10", 0.0f, -94888.0f, 1.0f, -100295.2f, -89479.9f },
    { "__OTR__ast_sf3ds_gnd/macbeth_11", 0.0f, -104915.0f, 1.0f, -110100.4f, -99729.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_12", 4350.0f, -114884.0f, 1.0f, -120488.3f, -109279.7f },
    { "__OTR__ast_sf3ds_gnd/macbeth_13", 8700.0f, -125311.0f, 1.0f, -130860.2f, -119760.9f },
    { "__OTR__ast_sf3ds_gnd/macbeth_14", 8700.0f, -135832.0f, 1.0f, -141695.8f, -129968.2f },
    { "__OTR__ast_sf3ds_gnd/macbeth_15", 8700.0f, -145635.0f, 1.0f, -150899.8f, -140370.2f },
    { "__OTR__ast_sf3ds_gnd/macbeth_16", 0.0f, -155811.0f, 1.0f, -161233.8f, -150388.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_17", 0.0f, -166391.0f, 1.0f, -172015.6f, -160766.5f },
    { "__OTR__ast_sf3ds_gnd/macbeth_18", 0.0f, -176203.0f, 1.0f, -181500.3f, -170905.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_19", 0.0f, -186548.0f, 1.0f, -192161.4f, -180935.0f },
    { "__OTR__ast_sf3ds_gnd/macbeth_20", 0.0f, -197059.0f, 1.0f, -202451.2f, -191667.2f },
    { "__OTR__ast_sf3ds_gnd/macbeth_21", 0.0f, -207182.0f, 1.0f, -212630.0f, -201734.5f },
    { "__OTR__ast_sf3ds_gnd/macbeth_22", 0.0f, -217319.0f, 1.0f, -222751.6f, -211886.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_23", 0.0f, -227435.0f, 1.0f, -232839.2f, -222030.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_24", 0.0f, -237482.0f, 1.0f, -242700.3f, -232263.9f },
    { "__OTR__ast_sf3ds_gnd/macbeth_25", 0.0f, -247422.0f, 1.0f, -253005.2f, -241839.1f },
    { "__OTR__ast_sf3ds_gnd/macbeth_26", 0.0f, -258019.0f, 1.0f, -263450.7f, -252587.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_27", 0.0f, -268200.0f, 1.0f, -273300.0f, -263100.0f },
};
static const Terrain3DSSector sTerrain3DS_Titania[] = {
    { "__OTR__ast_sf3ds_gnd/titania_01", 0.0f, 200.0f, 1.0f, -10140.0f, 10540.0f },
    { "__OTR__ast_sf3ds_gnd/titania_02", 0.0f, -15310.0f, 1.0f, -20480.0f, -10140.0f },
    { "__OTR__ast_sf3ds_gnd/titania_03", 0.0f, -25650.0f, 1.0f, -30820.0f, -20480.0f },
    { "__OTR__ast_sf3ds_gnd/titania_04", 0.0f, -35990.0f, 1.0f, -41160.0f, -30820.0f },
    { "__OTR__ast_sf3ds_gnd/titania_05", 0.0f, -46330.0f, 1.0f, -51500.0f, -41160.0f },
    { "__OTR__ast_sf3ds_gnd/titania_06", 0.0f, -56647.0f, 1.0f, -61840.0f, -51453.2f },
    { "__OTR__ast_sf3ds_gnd/titania_07", 0.0f, -67010.0f, 1.0f, -72180.0f, -61840.0f },
    { "__OTR__ast_sf3ds_gnd/titania_08", 0.0f, -77374.0f, 1.0f, -82568.4f, -72180.0f },
    { "__OTR__ast_sf3ds_gnd/titania_09", 0.0f, -87690.0f, 1.0f, -92860.0f, -82520.0f },
    { "__OTR__ast_sf3ds_gnd/titania_10", 0.0f, -98030.0f, 1.0f, -103200.0f, -92860.0f },
};
static const Terrain3DSSector sTerrain3DS_Aquas[] = {
    { "__OTR__ast_sf3ds_gnd/aquas_01", 0.0f, 1491.0f, 1.0f, -9334.8f, 12316.1f },
    { "__OTR__ast_sf3ds_gnd/aquas_02", 0.0f, -13876.0f, 1.0f, -19636.9f, -8115.3f },
    { "__OTR__ast_sf3ds_gnd/aquas_03", 0.0f, -24320.0f, 1.0f, -30308.5f, -18331.2f },
    { "__OTR__ast_sf3ds_gnd/aquas_04", 0.0f, -34616.0f, 1.0f, -40684.8f, -28547.1f },
    { "__OTR__ast_sf3ds_gnd/aquas_05", 0.0f, -44691.0f, 1.0f, -50619.6f, -38762.5f },
    { "__OTR__ast_sf3ds_gnd/aquas_06", 0.0f, -54087.0f, 1.0f, -59196.2f, -48978.6f },
    { "__OTR__ast_sf3ds_gnd/aquas_07", 451.0f, -63033.0f, 1.0f, -69412.1f, -56653.9f },
    { "__OTR__ast_sf3ds_gnd/aquas_08", 129.0f, -74451.0f, 1.0f, -79521.7f, -69380.3f },
    { "__OTR__ast_sf3ds_gnd/aquas_09", 0.0f, -85182.0f, 1.0f, -90842.9f, -79521.6f },
    { "__OTR__ast_sf3ds_gnd/aquas_10", 0.0f, -94951.0f, 1.0f, -100059.7f, -89842.1f },
    { "__OTR__ast_sf3ds_gnd/aquas_11", 0.0f, -105167.0f, 1.0f, -110275.8f, -100058.2f },
    { "__OTR__ast_sf3ds_gnd/aquas_12", 0.0f, -115383.0f, 1.0f, -120491.8f, -110274.2f },
};
static const Terrain3DSSector sTerrain3DS_Venom1[] = {
    { "__OTR__ast_sf3ds_gnd/venom_1_01", 4.0f, 2100.0f, 1.0f, -8116.4f, 12316.5f },
    { "__OTR__ast_sf3ds_gnd/venom_1_02", 8.0f, -12444.0f, 1.0f, -18333.4f, -6553.6f },
    { "__OTR__ast_sf3ds_gnd/venom_1_03", 11.0f, -23474.0f, 1.0f, -28804.6f, -18143.8f },
    { "__OTR__ast_sf3ds_gnd/venom_1_04", 11.0f, -33932.0f, 1.0f, -39319.2f, -28545.5f },
    { "__OTR__ast_sf3ds_gnd/venom_1_05", 14.0f, -44434.0f, 1.0f, -50107.5f, -38761.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_06", 18.0f, -54086.0f, 1.0f, -59195.7f, -48977.3f },
    { "__OTR__ast_sf3ds_gnd/venom_1_07", 21.0f, -64316.0f, 1.0f, -70078.3f, -58553.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_08", 21.0f, -75189.0f, 1.0f, -80968.7f, -69408.8f },
    { "__OTR__ast_sf3ds_gnd/venom_1_09", 24.0f, -85477.0f, 1.0f, -91330.9f, -79623.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_10", 27.0f, -95326.0f, 1.0f, -101312.9f, -89339.6f },
    { "__OTR__ast_sf3ds_gnd/venom_1_11", 30.0f, -105678.0f, 1.0f, -111298.8f, -100056.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_12", 30.0f, -115050.0f, 1.0f, -120489.2f, -109610.5f },
    { "__OTR__ast_sf3ds_gnd/venom_1_13", 29.0f, -125964.0f, 1.0f, -132248.7f, -119679.3f },
    { "__OTR__ast_sf3ds_gnd/venom_1_14", 32.0f, -135769.0f, 1.0f, -140944.7f, -130593.3f },
    { "__OTR__ast_sf3ds_gnd/venom_1_15", 36.0f, -146028.0f, 1.0f, -151136.7f, -140919.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_16", 39.0f, -163336.0f, 1.0f, -175538.0f, -151135.0f },
    { "__OTR__ast_sf3ds_gnd/venom_1_17", 42.0f, -166675.0f, 1.0f, -171999.2f, -161351.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_18", 45.0f, -176676.0f, 1.0f, -181784.2f, -171567.0f },
};
static const Terrain3DSSector sTerrain3DS_Venom2[] = {
    { "__OTR__ast_sf3ds_gnd/venom_2_01", -718.0f, 199.0f, 4.0f, -66037.4f, 66435.8f },
};
static const Terrain3DSSector sTerrain3DS_Training[] = {
    { "__OTR__ast_sf3ds_gnd/training_01", -6527.0f, -6521.0f, 1.0f, -26085.7f, 13042.8f },
};

static const Terrain3DSLevel sTerrain3DSLevels[] = {
    { LEVEL_CORNERIA, 0, sTerrain3DS_Corneria, ARRAY_COUNT(sTerrain3DS_Corneria), 10215.0f, 0, 0.0f },
    { LEVEL_MACBETH, 0, sTerrain3DS_Macbeth, ARRAY_COUNT(sTerrain3DS_Macbeth), 10215.0f, 0, 0.0f },
    { LEVEL_TITANIA, 0, sTerrain3DS_Titania, ARRAY_COUNT(sTerrain3DS_Titania), 10340.0f, 1, 0.0f },
    { LEVEL_AQUAS, 0, sTerrain3DS_Aquas, ARRAY_COUNT(sTerrain3DS_Aquas), 10215.0f, 0, 0.0f },
    { LEVEL_VENOM_1, 0, sTerrain3DS_Venom1, ARRAY_COUNT(sTerrain3DS_Venom1), 10215.0f, 0, 176000.0f },
    { LEVEL_VENOM_2, 1, sTerrain3DS_Venom2, ARRAY_COUNT(sTerrain3DS_Venom2), 10215.0f, 0, 176000.0f },
    { LEVEL_TRAINING, 1, sTerrain3DS_Training, ARRAY_COUNT(sTerrain3DS_Training), 15000.0f, 1, 0.0f },
};

// scrolling waterfall sheets (3DS: texture-animated), drawn separately so the tile offset can move
typedef struct { s32 level; const char* mat[2]; const char* tri[2]; s32 n; s32 dw[2], dh[2]; f32 ox, oz, scale, zmin, zmax; } Terrain3DSFall;
static const Terrain3DSFall sTerrain3DSFalls[] = {
    { LEVEL_CORNERIA, { "__OTR__ast_sf3ds_gnd/corneria_14_wf_mat0", "__OTR__ast_sf3ds_gnd/corneria_14_wf_mat1" }, { "__OTR__ast_sf3ds_gnd/corneria_14_wf_tri0", "__OTR__ast_sf3ds_gnd/corneria_14_wf_tri1" }, 2, { 64, 64 }, { 64, 64 }, 304.0f, -171060.0f, 1.0f, -176573.4f, -165546.6f },
};

typedef struct { s32 level; const char* dl; f32 tile; } Terrain3DSFill;
static const Terrain3DSFill sTerrain3DSFills[] = {
    { LEVEL_CORNERIA, "__OTR__ast_sf3ds_gnd/corneria_fill", 15000.0f },
    { LEVEL_MACBETH, "__OTR__ast_sf3ds_gnd/macbeth_fill", 15000.0f },
    { LEVEL_TITANIA, "__OTR__ast_sf3ds_gnd/titania_fill", 15000.0f },
    { LEVEL_VENOM_1, "__OTR__ast_sf3ds_gnd/venom_1_fill", 15000.0f },
};

#define TERRAIN3DS_FAR 40000.0f
#define TERRAIN3DS_NEAR 4000.0f

static s32 sTerrain3DSCheckedLevel = -1;
static const Terrain3DSLevel* sTerrain3DSCur = NULL;

static const Terrain3DSLevel* Terrain3DS_GetLevel(void) {
    s32 i;
    if (sTerrain3DSCheckedLevel != gCurrentLevel) {
        sTerrain3DSCheckedLevel = gCurrentLevel;
        sTerrain3DSCur = NULL;
        for (i = 0; i < ARRAY_COUNT(sTerrain3DSLevels); i++) {
            if (sTerrain3DSLevels[i].level == gCurrentLevel) {
                // only enable when the terrain mod is installed
                if (ResourceGetDataByName(sTerrain3DSLevels[i].secs[0].dl + 7) != NULL) {
                    sTerrain3DSCur = &sTerrain3DSLevels[i];
                }
                break;
            }
        }
    }
    if (sTerrain3DSCur == NULL) {
        return NULL;
    }
    // only during actual gameplay (not the title screen / menus, where the default level is Corneria)
    if (gGameState != GSTATE_PLAY) {
        return NULL;
    }
    if ((sTerrain3DSCur->allRange != 0) != (gLevelMode == LEVELMODE_ALL_RANGE)) {
        return NULL;
    }
    return sTerrain3DSCur;
}

bool Terrain3DS_Active(void) {
    return Terrain3DS_GetLevel() != NULL;
}

// True when the static 3DS ground plane replaces the N64 ground (not over water, where the N64 water surface stays).
bool Terrain3DS_ReplacesGround(void) {
    s32 i;
    if (!Terrain3DS_Active() || (gGroundSurface == SURFACE_WATER)) {
        return false;
    }
    for (i = 0; i < ARRAY_COUNT(sTerrain3DSFills); i++) {
        if (sTerrain3DSFills[i].level == gCurrentLevel) {
            return true;
        }
    }
    return false;
}

static const s16 sHide_Corneria[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 24, 25, 26, 27, 28, 54, 55 };
static const s16 sHide_Macbeth[] = { 59, 60, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75 };
static const s16 sHide_Aquas[] = { 117, 118, 119, 120, 121, 122, 124, 125 };
static const s16 sHide_Venom1[] = { 50, 51, 53 };
static const s16 sHide_Venom2[] = { 160 };

// N64 scenery that SF64 3D never draws on these levels: its object info table points them at models the level
// doesn't load, because the terrain already contains them (hills, cliffs, highways, roads, ...).
// Only drawing is skipped; collision and game logic are untouched.
bool Terrain3DS_HidesScenery(s32 id) {
    const s16* list = NULL;
    s32 n = 0;
    s32 i;

    if (!Terrain3DS_Active()) {
        return false;
    }
    switch (gCurrentLevel) {
        case LEVEL_CORNERIA:
            list = sHide_Corneria; n = ARRAY_COUNT(sHide_Corneria);
            break;
        case LEVEL_MACBETH:
            list = sHide_Macbeth; n = ARRAY_COUNT(sHide_Macbeth);
            break;
        case LEVEL_AQUAS:
            list = sHide_Aquas; n = ARRAY_COUNT(sHide_Aquas);
            break;
        case LEVEL_VENOM_1:
            list = sHide_Venom1; n = ARRAY_COUNT(sHide_Venom1);
            break;
        case LEVEL_VENOM_2:
            list = sHide_Venom2; n = ARRAY_COUNT(sHide_Venom2);
            break;
        default:
            return false;
    }
    for (i = 0; i < n; i++) {
        if (list[i] == id) {
            return true;
        }
    }
    return false;
}

static void Terrain3DS_DrawSector(const Terrain3DSSector* s, f32 zShift) {
    f32 zNear = s->zmax + zShift + gPathProgress;
    f32 zFar = s->zmin + zShift + gPathProgress;

    if ((zFar > TERRAIN3DS_NEAR) || (zNear < -TERRAIN3DS_FAR)) {
        return;
    }
    Matrix_Push(&gGfxMatrix);
    Matrix_Translate(gGfxMatrix, s->ox, -3.0f + gCameraShakeY, s->oz + zShift + gPathProgress, MTXF_APPLY);
    if (s->scale != 1.0f) {
        Matrix_Scale(gGfxMatrix, s->scale, s->scale, s->scale, MTXF_APPLY);
    }
    Matrix_SetGfxMtx(&gMasterDisp);
    gSPDisplayList(gMasterDisp++, s->dl);
    Matrix_Pop(&gGfxMatrix);
}

void Terrain3DS_Draw(void) {
    const Terrain3DSLevel* lv = Terrain3DS_GetLevel();
    s32 i;
    s32 k;

    if (lv == NULL) {
        return;
    }
    if ((lv->hideAfter > 0.0f) && (gPathProgress > lv->hideAfter)) {
        return;
    }
    // static ground plane (3DS ground texture) in place of the scrolling N64 ground, drawn as a depth-less backdrop
    for (i = 0; i < ARRAY_COUNT(sTerrain3DSFills); i++) {
        const Terrain3DSFill* f = &sTerrain3DSFills[i];
        f32 camZ;
        s32 gx, gz;
        if ((f->level != gCurrentLevel) || (lv->allRange != 0) || (gGroundSurface == SURFACE_WATER)) {
            continue;
        }
        RCP_SetupDL_20(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
        gSPClearGeometryMode(gMasterDisp++, G_LIGHTING | G_CULL_BACK);
        camZ = floorf(-gPathProgress / f->tile) * f->tile;
        for (gz = -1; gz <= 3; gz++) {
            for (gx = -3; gx <= 3; gx++) {
                Matrix_Push(&gGfxMatrix);
                Matrix_Translate(gGfxMatrix, gx * f->tile, -3.0f + gCameraShakeY, camZ - gz * f->tile + gPathProgress,
                                 MTXF_APPLY);
                Matrix_SetGfxMtx(&gMasterDisp);
                gSPDisplayList(gMasterDisp++, f->dl);
                Matrix_Pop(&gGfxMatrix);
            }
        }
    }

    // lit with the level's sun direction; brighter ambient than the N64 object lighting so slopes facing away
    // from the sun don't go black (the 3DS terrain has no dynamic lighting, only baked shading)
    RCP_SetupDL_29(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
    gSPClearGeometryMode(gMasterDisp++, G_CULL_BACK); // terrain is drawn two-sided on 3DS
    Lights_SetOneLight(&gMasterDisp, gLight1x, gLight1y, gLight1z, MIN(255, gLight1R * 3 / 2), MIN(255, gLight1G * 3 / 2),
                       MIN(255, gLight1B * 3 / 2), MIN(255, gAmbientR + 110), MIN(255, gAmbientG + 110),
                       MIN(255, gAmbientB + 110));
    for (i = 0; i < lv->count; i++) {
        Terrain3DS_DrawSector(&lv->secs[i], 0.0f);
    }
    if (lv->repeatLast && (lv->allRange == 0)) {
        for (k = 1; k <= 8; k++) {
            Terrain3DS_DrawSector(&lv->secs[lv->count - 1], -lv->length * k);
        }
    }
    // restore the scene lighting for whatever is drawn next
    Lights_SetOneLight(&gMasterDisp, gLight1x, gLight1y, gLight1z, gLight1R, gLight1G, gLight1B, gAmbientR, gAmbientG,
                       gAmbientB);

    // waterfalls: unlit translucent sheets with the texture scrolling downwards
    for (i = 0; i < ARRAY_COUNT(sTerrain3DSFalls); i++) {
        const Terrain3DSFall* w = &sTerrain3DSFalls[i];
        f32 zNear;
        f32 zFar;
        if ((w->level != gCurrentLevel) || (lv->allRange != 0)) {
            continue;
        }
        zNear = w->zmax + gPathProgress;
        zFar = w->zmin + gPathProgress;
        if ((zFar > TERRAIN3DS_NEAR) || (zNear < -TERRAIN3DS_FAR)) {
            continue;
        }
        RCP_SetupDL_29(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
        gSPClearGeometryMode(gMasterDisp++, G_LIGHTING | G_CULL_BACK);
        gDPSetRenderMode(gMasterDisp++, G_RM_FOG_SHADE_A, G_RM_AA_ZB_XLU_SURF2);
        Matrix_Push(&gGfxMatrix);
        Matrix_Translate(gGfxMatrix, w->ox, -3.0f + gCameraShakeY, w->oz + gPathProgress, MTXF_APPLY);
        if (w->scale != 1.0f) {
            Matrix_Scale(gGfxMatrix, w->scale, w->scale, w->scale, MTXF_APPLY);
        }
        Matrix_SetGfxMtx(&gMasterDisp);
        for (k = 0; k < w->n; k++) {
            // texture T grows downwards on the falling sheet: a decreasing offset moves the streaks down
            s32 period = w->dh[k] << 2;
            s32 t = period - (((gGameFrameCount * (k == 0 ? 6 : 2)) % period));
            gSPDisplayList(gMasterDisp++, w->mat[k]);
            gDPSetTileSize(gMasterDisp++, G_TX_RENDERTILE, 0, t, (w->dw[k] - 1) << 2, t + ((w->dh[k] - 1) << 2));
            gSPDisplayList(gMasterDisp++, w->tri[k]);
        }
        Matrix_Pop(&gGfxMatrix);
    }
}
