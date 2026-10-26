// Generated: 3DS (Star Fox 64 3D) terrain sectors drawn over the N64 ground.
// Active only when the matching "ast_sf3ds_gnd/*" display lists are present in a loaded .o2r mod.
#include "global.h"

typedef struct { const char* dl; f32 ox, oz, scale, zmin, zmax; } Terrain3DSSector;
typedef struct { s32 level; s32 allRange; const Terrain3DSSector* secs; s32 count; f32 length; s32 repeatLast; f32 hideAfter; } Terrain3DSLevel;

static const Terrain3DSSector sTerrain3DS_Corneria[] = {
    { "__OTR__ast_sf3ds_gnd/corneria_01", 140.0f, -34820.0f, 1.0f, -40038.5f, -29602.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_02", 0.0f, -45015.0f, 1.0f, -50143.5f, -39886.5f },
    { "__OTR__ast_sf3ds_gnd/corneria_03", 0.0f, -55230.0f, 1.0f, -60340.7f, -50119.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_04", 0.0f, -65445.0f, 1.0f, -70872.8f, -60017.2f },
    { "__OTR__ast_sf3ds_gnd/corneria_05", -0.0f, -75660.0f, 1.0f, -80830.8f, -70489.2f },
    { "__OTR__ast_sf3ds_gnd/corneria_06", 23.0f, -85791.0f, 1.0f, -91397.3f, -80184.5f },
    { "__OTR__ast_sf3ds_gnd/corneria_07", 20.0f, -96202.0f, 1.0f, -101388.6f, -91014.7f },
    { "__OTR__ast_sf3ds_gnd/corneria_08", 8.0f, -106230.0f, 1.0f, -111501.1f, -100958.2f },
    { "__OTR__ast_sf3ds_gnd/corneria_09", 25.0f, -116602.0f, 1.0f, -121713.6f, -111490.9f },
    { "__OTR__ast_sf3ds_gnd/corneria_10", 26.0f, -126854.0f, 1.0f, -131999.6f, -121708.1f },
    { "__OTR__ast_sf3ds_gnd/corneria_11", 27.0f, -137062.0f, 1.0f, -142200.0f, -131923.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_12", 27.0f, -146804.0f, 1.0f, -151467.5f, -142140.5f },
    { "__OTR__ast_sf3ds_gnd/corneria_13", 28.0f, -157378.0f, 1.0f, -162607.7f, -152148.3f },
    { "__OTR__ast_sf3ds_gnd/corneria_14", 304.0f, -168060.0f, 1.0f, -173573.4f, -162546.6f },
    { "__OTR__ast_sf3ds_gnd/corneria_15", 2239.0f, -177875.0f, 1.0f, -183012.1f, -172738.1f },
    { "__OTR__ast_sf3ds_gnd/corneria_16", 2402.0f, -188125.0f, 1.0f, -193327.0f, -182923.0f },
    { "__OTR__ast_sf3ds_gnd/corneria_17", 4382.0f, -198295.0f, 1.0f, -203440.5f, -193149.5f },
    { "__OTR__ast_sf3ds_gnd/corneria_18", 5833.0f, -208533.0f, 1.0f, -213641.6f, -203424.4f },
};
static const Terrain3DSSector sTerrain3DS_Macbeth[] = {
    { "__OTR__ast_sf3ds_gnd/macbeth_01", 0.0f, 660.0f, 1.0f, -5100.0f, 6420.7f },
    { "__OTR__ast_sf3ds_gnd/macbeth_02", 1078.0f, -20933.0f, 1.0f, -37533.2f, -4333.0f },
    { "__OTR__ast_sf3ds_gnd/macbeth_03", 0.0f, -20294.0f, 1.0f, -25776.8f, -14811.6f },
    { "__OTR__ast_sf3ds_gnd/macbeth_04", 1041.0f, -31303.0f, 1.0f, -37471.0f, -25135.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_05", 0.0f, -41133.0f, 1.0f, -47841.6f, -34425.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_06", 0.0f, -50867.0f, 1.0f, -57295.0f, -44438.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_07", 0.0f, -61459.0f, 1.0f, -68558.8f, -54358.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_08", 0.0f, -71129.0f, 1.0f, -76545.1f, -65713.3f },
    { "__OTR__ast_sf3ds_gnd/macbeth_09", 0.0f, -81280.0f, 1.0f, -86858.7f, -75701.5f },
    { "__OTR__ast_sf3ds_gnd/macbeth_10", 0.0f, -91888.0f, 1.0f, -97295.2f, -86479.9f },
    { "__OTR__ast_sf3ds_gnd/macbeth_11", 0.0f, -101915.0f, 1.0f, -107100.4f, -96729.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_12", 4350.0f, -111884.0f, 1.0f, -117488.3f, -106279.7f },
    { "__OTR__ast_sf3ds_gnd/macbeth_13", 8700.0f, -122311.0f, 1.0f, -127860.2f, -116760.9f },
    { "__OTR__ast_sf3ds_gnd/macbeth_14", 8700.0f, -132832.0f, 1.0f, -138695.8f, -126968.2f },
    { "__OTR__ast_sf3ds_gnd/macbeth_15", 8700.0f, -142635.0f, 1.0f, -147899.8f, -137370.2f },
    { "__OTR__ast_sf3ds_gnd/macbeth_16", 0.0f, -152811.0f, 1.0f, -158233.8f, -147388.4f },
    { "__OTR__ast_sf3ds_gnd/macbeth_17", 0.0f, -163391.0f, 1.0f, -169015.6f, -157766.5f },
    { "__OTR__ast_sf3ds_gnd/macbeth_18", 0.0f, -173203.0f, 1.0f, -178500.3f, -167905.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_19", 0.0f, -183548.0f, 1.0f, -189161.4f, -177935.0f },
    { "__OTR__ast_sf3ds_gnd/macbeth_20", 0.0f, -194059.0f, 1.0f, -199451.2f, -188667.2f },
    { "__OTR__ast_sf3ds_gnd/macbeth_21", 0.0f, -204182.0f, 1.0f, -209630.0f, -198734.5f },
    { "__OTR__ast_sf3ds_gnd/macbeth_22", 0.0f, -214319.0f, 1.0f, -219751.6f, -208886.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_23", 0.0f, -224435.0f, 1.0f, -229839.2f, -219030.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_24", 0.0f, -234482.0f, 1.0f, -239700.3f, -229263.9f },
    { "__OTR__ast_sf3ds_gnd/macbeth_25", 0.0f, -244422.0f, 1.0f, -250005.2f, -238839.1f },
    { "__OTR__ast_sf3ds_gnd/macbeth_26", 0.0f, -255019.0f, 1.0f, -260450.7f, -249587.8f },
    { "__OTR__ast_sf3ds_gnd/macbeth_27", 0.0f, -265200.0f, 1.0f, -270300.0f, -260100.0f },
};
static const Terrain3DSSector sTerrain3DS_Titania[] = {
    { "__OTR__ast_sf3ds_gnd/titania_01", 0.0f, 3200.0f, 1.0f, -7140.0f, 13540.0f },
    { "__OTR__ast_sf3ds_gnd/titania_02", 0.0f, -12310.0f, 1.0f, -17480.0f, -7140.0f },
    { "__OTR__ast_sf3ds_gnd/titania_03", 0.0f, -22650.0f, 1.0f, -27820.0f, -17480.0f },
    { "__OTR__ast_sf3ds_gnd/titania_04", 0.0f, -32990.0f, 1.0f, -38160.0f, -27820.0f },
    { "__OTR__ast_sf3ds_gnd/titania_05", 0.0f, -43330.0f, 1.0f, -48500.0f, -38160.0f },
    { "__OTR__ast_sf3ds_gnd/titania_06", 0.0f, -53647.0f, 1.0f, -58840.0f, -48453.2f },
    { "__OTR__ast_sf3ds_gnd/titania_07", 0.0f, -64010.0f, 1.0f, -69180.0f, -58840.0f },
    { "__OTR__ast_sf3ds_gnd/titania_08", 0.0f, -74374.0f, 1.0f, -79568.4f, -69180.0f },
    { "__OTR__ast_sf3ds_gnd/titania_09", 0.0f, -84690.0f, 1.0f, -89860.0f, -79520.0f },
    { "__OTR__ast_sf3ds_gnd/titania_10", 0.0f, -95030.0f, 1.0f, -100200.0f, -89860.0f },
};
static const Terrain3DSSector sTerrain3DS_Aquas[] = {
    { "__OTR__ast_sf3ds_gnd/aquas_01", 0.0f, 4491.0f, 1.0f, -6334.8f, 15316.1f },
    { "__OTR__ast_sf3ds_gnd/aquas_02", 0.0f, -10876.0f, 1.0f, -16636.9f, -5115.3f },
    { "__OTR__ast_sf3ds_gnd/aquas_03", 0.0f, -21320.0f, 1.0f, -27308.5f, -15331.2f },
    { "__OTR__ast_sf3ds_gnd/aquas_04", 0.0f, -31616.0f, 1.0f, -37684.8f, -25547.1f },
    { "__OTR__ast_sf3ds_gnd/aquas_05", 0.0f, -41691.0f, 1.0f, -47619.6f, -35762.5f },
    { "__OTR__ast_sf3ds_gnd/aquas_06", 0.0f, -51087.0f, 1.0f, -56196.2f, -45978.6f },
    { "__OTR__ast_sf3ds_gnd/aquas_07", 451.0f, -60033.0f, 1.0f, -66412.1f, -53653.9f },
    { "__OTR__ast_sf3ds_gnd/aquas_08", 129.0f, -71451.0f, 1.0f, -76521.7f, -66380.3f },
    { "__OTR__ast_sf3ds_gnd/aquas_09", 0.0f, -82182.0f, 1.0f, -87842.9f, -76521.6f },
    { "__OTR__ast_sf3ds_gnd/aquas_10", 0.0f, -91951.0f, 1.0f, -97059.7f, -86842.1f },
    { "__OTR__ast_sf3ds_gnd/aquas_11", 0.0f, -102167.0f, 1.0f, -107275.8f, -97058.2f },
    { "__OTR__ast_sf3ds_gnd/aquas_12", 0.0f, -112383.0f, 1.0f, -117491.8f, -107274.2f },
};
static const Terrain3DSSector sTerrain3DS_Venom1[] = {
    { "__OTR__ast_sf3ds_gnd/venom_1_01", 4.0f, 5100.0f, 1.0f, -5116.4f, 15316.5f },
    { "__OTR__ast_sf3ds_gnd/venom_1_02", 8.0f, -9444.0f, 1.0f, -15333.4f, -3553.6f },
    { "__OTR__ast_sf3ds_gnd/venom_1_03", 11.0f, -20474.0f, 1.0f, -25804.6f, -15143.8f },
    { "__OTR__ast_sf3ds_gnd/venom_1_04", 11.0f, -30932.0f, 1.0f, -36319.2f, -25545.5f },
    { "__OTR__ast_sf3ds_gnd/venom_1_05", 14.0f, -41434.0f, 1.0f, -47107.5f, -35761.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_06", 18.0f, -51086.0f, 1.0f, -56195.7f, -45977.3f },
    { "__OTR__ast_sf3ds_gnd/venom_1_07", 21.0f, -61316.0f, 1.0f, -67078.3f, -55553.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_08", 21.0f, -72189.0f, 1.0f, -77968.7f, -66408.8f },
    { "__OTR__ast_sf3ds_gnd/venom_1_09", 24.0f, -82477.0f, 1.0f, -88330.9f, -76623.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_10", 27.0f, -92326.0f, 1.0f, -98312.9f, -86339.6f },
    { "__OTR__ast_sf3ds_gnd/venom_1_11", 30.0f, -102678.0f, 1.0f, -108298.8f, -97056.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_12", 30.0f, -112050.0f, 1.0f, -117489.2f, -106610.5f },
    { "__OTR__ast_sf3ds_gnd/venom_1_13", 29.0f, -122964.0f, 1.0f, -129248.7f, -116679.3f },
    { "__OTR__ast_sf3ds_gnd/venom_1_14", 32.0f, -132769.0f, 1.0f, -137944.7f, -127593.3f },
    { "__OTR__ast_sf3ds_gnd/venom_1_15", 36.0f, -143028.0f, 1.0f, -148136.7f, -137919.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_16", 39.0f, -160336.0f, 1.0f, -172538.0f, -148135.0f },
    { "__OTR__ast_sf3ds_gnd/venom_1_17", 42.0f, -163675.0f, 1.0f, -168999.2f, -158351.4f },
    { "__OTR__ast_sf3ds_gnd/venom_1_18", 45.0f, -173676.0f, 1.0f, -178784.2f, -168567.0f },
};
static const Terrain3DSSector sTerrain3DS_Venom2[] = {
    { "__OTR__ast_sf3ds_gnd/venom_2_01", -718.0f, 199.0f, 4.0f, -66037.4f, 66435.8f },
};
static const Terrain3DSSector sTerrain3DS_Training[] = {
    { "__OTR__ast_sf3ds_gnd/training_01", -6527.0f, -6521.0f, 1.0f, -26085.7f, 13042.8f },
};

static const Terrain3DSLevel sTerrain3DSLevels[] = {
    { LEVEL_CORNERIA, 0, sTerrain3DS_Corneria, ARRAY_COUNT(sTerrain3DS_Corneria), 10215.0f, 1, 0.0f },
    { LEVEL_MACBETH, 0, sTerrain3DS_Macbeth, ARRAY_COUNT(sTerrain3DS_Macbeth), 10215.0f, 0, 0.0f },
    { LEVEL_TITANIA, 0, sTerrain3DS_Titania, ARRAY_COUNT(sTerrain3DS_Titania), 10340.0f, 1, 0.0f },
    { LEVEL_AQUAS, 0, sTerrain3DS_Aquas, ARRAY_COUNT(sTerrain3DS_Aquas), 10215.0f, 0, 0.0f },
    { LEVEL_VENOM_1, 0, sTerrain3DS_Venom1, ARRAY_COUNT(sTerrain3DS_Venom1), 10215.0f, 0, 176000.0f },
    { LEVEL_VENOM_2, 1, sTerrain3DS_Venom2, ARRAY_COUNT(sTerrain3DS_Venom2), 10215.0f, 0, 176000.0f },
    { LEVEL_TRAINING, 1, sTerrain3DS_Training, ARRAY_COUNT(sTerrain3DS_Training), 15000.0f, 1, 0.0f },
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
    if ((sTerrain3DSCur->allRange != 0) != (gLevelMode == LEVELMODE_ALL_RANGE)) {
        return NULL;
    }
    return sTerrain3DSCur;
}

bool Terrain3DS_Active(void) {
    return Terrain3DS_GetLevel() != NULL;
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
    RCP_SetupDL_29(gFogRed, gFogGreen, gFogBlue, gFogAlpha, gFogNear, gFogFar);
    for (i = 0; i < lv->count; i++) {
        Terrain3DS_DrawSector(&lv->secs[i], 0.0f);
    }
    if (lv->repeatLast && (lv->allRange == 0)) {
        for (k = 1; k <= 8; k++) {
            Terrain3DS_DrawSector(&lv->secs[lv->count - 1], -lv->length * k);
        }
    }
}
