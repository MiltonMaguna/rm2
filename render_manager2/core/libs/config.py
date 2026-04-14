COLOR_SPACE = "ACES - ACEScg"

COLORS_BACKDROP_SUFFIX = {
    "CRYPTO": 1131563519,
    "TECH": 1145467647,
    "VOL": 1917993983,
    "VFX": 1317993983,
    "BTY": 1917088255
}


RENDER_LAYERS_ORDER_TOKENS = [
    "RND_BG",
    "RND_MG",
    "RND_FG",
    "RND_ALL",
    "RND_VFX"
]

SUFIJO_ORDER_AOVS_BTY = [
    "RGBA_LG_dome",
    "RGBA_LG_key",
    "RGBA_LG",
    "emission",
    "beauty"
]

SUFIJO_ORDER_AOVS_TECH = [
    "Z",
    "motionvector",
    "P",
    "N",
    "UV"
]

SUFIJO_ORDER_AOVS_CRYPTO = [
    "crypto_asset",
    "crypto_material",
    "crypto_object"
]

SORTED_TOKENS = ["CRYPTO",
                 "TECH",
                 "VOL",
                 "VFX",
                 "BTY"]

ROL = [
    "BG",
    "MG",
    "FG",
    "ALL",
    "VFX"]

PASS = [
    "BTY",
    "TECH",
    "CRYPTO",
    "VFX",
    "VOL"]


NODE_CUSTOM = {'font': 25,
               'note_font': 'Arial Black',
               'hide_input': True,
               'postage_stamp': False,
               "tile_color_noop": 1717987071}

ATTR_CUSTOM = {"rnd_layer": "render_layers",
               "rol": "rol",
               "suffix": "suffix",
               "aov": "aovs",
               "v_name": "version_name",
               "v_render": "version_render"}

GET_KNOBS_READ = ["name", "file", "format", "first", "last", "colorspace",
                  "render_layers", "rol", "suffix", "aovs", "version_name",
                  "version_render"]


BACKDROP_EXTRA = {
    "fake_fog": 814649087,
    "CC": 1915579647,
    "zdefocus": 2391288831,
}

POSITION_READ = {
    "BTY": [180, -360],
    "TECH": [180, -700],
    "CRYPTO": [1280, -700]}


OFFSET_INITIAL_POSITION = 200
OFFSET_READ_X = 30
ANCHOR_READ = 80
