# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Tokens
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------

# Disk Collector
# Valid render layer prefixes
RENDER_PREFIX = ["RND"]
RENDER_PREFIX_VERSION = ["LGT", "VFX"]
RENDER_ROLE = ["BG", "MG", "FG", "ALL", "VFX", "VOL"]

# Disk Collector
# Used to sort the render layers by type or render layer and check valid layers
RENDER_LAYER_ORDER = [
    "CRYPTO",
    "TECH",
    "BTY"
]

# Disk Collector
# Used to get only the required aov's for each render layer
TECHS_AOVS_IN_LAYER = {'_TECH': ["Z", "motionvector", "P", "Pref", "N", "UV"],
                       '_CRYPTO': ["crypto_asset", "crypto_material", "crypto_object"]
                       }
