from collections import defaultdict

# Backdrops
# User to create main backdrops containers for render layers
BACKDROP_SIZE = {'GENERAL': {"xpos": 0,
                             "bdwidth": 2500,
                             "ypos": -1100,
                             "bdheight": 1100,
                             'tile_color': 2290649088,
                             'z_order': -1,
                             'note_font_size': 200},
                 'BTY': {"xpos": 100,
                         "bdwidth": 2300,
                         "ypos": -500,
                         "bdheight": 400,
                         'tile_color': 1917088255,
                         'z_order': 0,
                         'note_font_size': 100},
                 'TECH': {"xpos": 100,
                          "bdwidth": 1000,
                          "ypos": -850,
                          "bdheight": 300,
                          'tile_color': 1145467647,
                          'z_order': 0,
                          'note_font_size': 100},
                 'CRYPTO': {"xpos": 1200,
                            "bdwidth": 600,
                            "ypos": -850,
                            "bdheight": 300,
                            'tile_color': 1131563519,
                            'z_order': 0,
                            'note_font_size': 100}
                 }

# Backdrops
# Colors for backdrop containers
COLOR_BACKDROP_RL = defaultdict(lambda: 2290649088, {
    "BG": 1713910271,
    "MG": 677784063,
    "FG": 1716201727,
    "ALL": 1680369407,
    "VFX": 1099401471,
    "FX": 1099401471,
    "VOL": 1097304319
})


# Backdrops
# Set column and row values in backdrops
ROL_POSITION_X = {"BG": 1,
                  "MG": 2,
                  "FG": 3,
                  "ALL": 4,
                  "VFX": 5,
                  "FX": 5,
                  "VOL": 6
                  }

# Backdrops
# Offsets for custom position backdrops
OFFSET_BDROP_X, OFFSET_BDROP_Y = 2600, -1200

# Reads
# position inital of first read
POSITION_READ = {
    "BTY": [180, -360],
    "TECH": [180, -700],
    "CRYPTO": [1280, -700]}

OFFSET_BORDER_BACKDROP = -40

# Reads
# Values for node custom
NODE_CUSTOM = {'font': 25,
               'note_font': 'Arial Black',
               'hide_input': True,
               'postage_stamp': False,
               "tile_color_noop": 1717987071}
# Reads
# Width of read node
ANCHOR_READ = 80
# Reads
# Offset beetwen read nodes
OFFSET_READ_X = 30
