from rm2.render_manager.render.render_layer import Render


data = {}

render_layer_bg = Render(
    path="I:/GizmoRD/FRAMES/DEV/030/CG/RND_BG_BTY/LGT_KAF_010_v0026",
    name="RND_BG_BTY",
    aovs=[
        "AO",
        "beauty",
        "crypto_asset",
        "crypto_material",
        "crypto_object",
        "emission",
    ],
)

render_layer_fg = Render(
    path="I:/GizmoRD/FRAMES/DEV/030/CG/RND_FG_BTY/LGT_KAF_010_v0026",
    name="RND_FG_BTY",
    aovs=[
        "AO",
        "beauty",
        "crypto_asset",
        "crypto_material",
        "crypto_object",
        "emission",
    ],
)

# Render layer for testing for create_all_aovs function
render_layer_bg_rzk = Render(
    path="I:/WARZONE/FRAMES/RZK/080/CG/RND_BG_BTY/LGT_RZK_080_v0010",
    name="RND_BG_BTY",
    aovs=[
        "AO",
        "beauty",
        "emission",
        "specular_direct",
        "specular_indirect",
        "RGBA_LG_dra_cst_001_spec",
        "RGBA_LG_nat_amb_001_top",
        "RGBA_LG_nat_amb_001_warm",
        "RGBA_LG_nat_amb_001_warmb",
        "RGBA_LG_nat_amb_007_warmb",
        "RGBA_LG_nat_cst_001_SHDWS",
        "RGBA_LG_pra_amb_001_tube",
        "RGBA_LG_pra_amb_002_tube",
        "RGBA_LG_pra_amb_002_tubeB",
        "RGBA_LG_pra_bnc_001_tubeb",
        "RGBA_LG_pra_cst_001_back",
        "RGBA_LG_pra_cst_001_flgobo",
        "RGBA_LG_pra_cst_001_muzzle",
        "RGBA_LG_pra_cst_001_pc",
        "RGBA_LG_pra_cst_001_red",
        "RGBA_LG_pra_cst_001_yellow",
        "RGBA_LG_pra_cst_002_muzzle",
    ],
)
