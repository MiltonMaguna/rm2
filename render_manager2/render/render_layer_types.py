# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Main RenderLayer Class
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------


class Render():
    def __init__(self, path: str, name: str, aovs: list) -> None:
        self._path = path
        self._name = name
        self._aovs = aovs
