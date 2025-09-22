# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Main RenderLayer Class
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import contextlib
import os

try:
    import nuke
except ImportError:
    import render_manager.mocks.nuke as nuke

from render_manager.core.libs.reformat import ReformatRenderLayer
from render_manager.render.libs.create import Create
from render_manager.render.libs.remove import RemoveRenderLayer
from render_manager.render.render_states import OUTDATED, SYNC, UNLOADED


class Render:
    def __init__(self, layer: dict) -> None:
        """Render Layer Object"""
        self._name = layer.get("job_name", "NO_NAME")
        self._batch_name = layer.get("batch_name", "RND_NONAME_BTY")
        self._render_layer = layer.get("render_layer", "RND_NONAME_BTY")
        self._version = layer.get("version", "0")
        self._user = layer.get("user", "johndoe")
        self._frames = layer.get("frames", "0,0")
        self._output_dir = layer.get("output_directories", "C:\\temp\\")
        self._progress = layer.get("progress", "100 %")
        self._aovs = []

    def __str__(self) -> str:
        return f"RENDER LAYER {self.name()}, path {self.path()}, aovs {self.aovs()}"

    def name(self) -> str:
        """returns render layer name
        Eg: RND_ALL_CRYPTO
        """
        return self._render_layer

    def full_name(self) -> str:
        """returns full render layer name
        Eg: RND_ALL_CRYPTO_LGT_KAF_010_v0026
        """
        return self._name

    def suffix(self) -> str:
        """returns suffix name
        Eg: TECH
        Eg: CRYPTO
        """
        return self._render_layer.split("_")[-1]

    def rol_layer(self) -> str:
        """returns rol layer name
        Eg: BG_MAIN
        Eg: ALL_MAIN
        """
        return ("_").join(self._render_layer.split("_")[1:-1])

    def rol_main(self) -> str:
        """returns rol main name
        Eg: BG
        Eg: ALL
        """
        return self._render_layer.split("_")[1]

    def prefix_rol_layer(self) -> str:
        """returns prefix rol layer name
        Eg: RND_BG
        Eg: RND_ALL
        """
        return self._name.rsplit("_", 1)[0]

    def path(self) -> str:
        """returns normalized windows path
        Eg: 'I:/GizmoRD/FRAMES/DEV/030/CG/RND_BG_TECH/LGT_KAF_010_v0026'
        Eg: 'I:/GizmoRD/FRAMES/DEV/030/CG/RND_ALL_CRYPTO/LGT_KAF_010_v0026'
        """
        return self._output_dir

    def version(self) -> str:
        """returns version of this render layer
        Eg: LGT_KAF_010_v0026
        """
        return self._batch_name

    def int_version(self) -> int:
        """returns int version of this render layer
        Eg: 26
        """
        return int(self._version)

    def name_version(self) -> str:
        """returns name of this render layer
        Eg: LGT_KAF_010
        """
        return self._batch_name.rsplit("_", 1)[0]

    def progress_bar(self) -> str:
        """returns progress bar value for this render layer
        Eg: '100 %'
        """
        return self._progress

    def user(self) -> str:
        """returns user name
        Eg: 'maxirocamora'
        """
        return self._user

    def aovs(self) -> list:
        """returns the list of aovs names for this render layer
        Eg: ['motionvector', 'N', 'P', 'UV', 'Z']
        Eg: ['crypto_asset', 'crypto_material', 'crypto_object']
        """
        return self._aovs

    def get_aov_data(self, aov_name: str) -> dict:
        """get all the data for this aov from disk files"""

        # filter only exr files
        aov_path = os.path.join(self.path(), aov_name)
        exr_files = [f for f in os.listdir(aov_path) if f.endswith(".exr")]

        # get first and last frame name
        name, ver_ext = exr_files[0].rsplit("_", 1)
        first, extension = ver_ext.split(".")
        _, last_ver_ext = exr_files[-1].rsplit("_", 1)
        last = last_ver_ext.split(".")[0]

        return {
            "files": name,
            "frames": len(exr_files),
            "first": int(first),
            "last": int(last),
            "range": f"{first}-{last}",
            "extension": extension,
        }

    def frames(self) -> int:
        """returns range from first aov or 0"""
        _frames = self._frames.replace(",", "-")
        _frames = _frames.split("-")
        return (int(_frames[1]) - int(_frames[0])) + 1 if len(_frames) > 1 else 0

    def frame_range(self) -> str:
        """returns formatted frame range taken from first aov
        Eg: '1001-1020'
        """
        return self._frames.replace(",", "-")

    def oiio_action(self) -> str:
        """returns script used for reformat render 50% over deadline"""
        return "reformat" if self.suffix() == "BTY" else "resample"

    def status(self) -> int:
        """returns state of this render layer"""
        if not self.version_from_read():
            return UNLOADED.value
        return (
            OUTDATED.value
            if self.version_from_read() < self.int_version()
            else SYNC.value
        )

    def status_text(self) -> str:
        """returns text for status column"""
        if not self.status():
            return UNLOADED.label
        return OUTDATED.label if self.status() == OUTDATED.value else SYNC.label

    def version_from_read(self) -> int:
        """returns version of this render layer READ from current nukescript"""
        for bdrop in nuke.allNodes("BackdropNode"):
            with contextlib.suppress(NameError, ValueError):
                if not int(bdrop["subcontainer"].getValue()):
                    continue

                if bdrop["name_layer"].getValue() != self.name():
                    continue

                return int(bdrop["version"].getValue())

        return 0

    def ranges_from_read(self) -> tuple:
        """returns range and frame count of this render
        layer READ from current nukescript"""
        for bdrop in nuke.allNodes("BackdropNode"):
            with contextlib.suppress(NameError, ValueError):
                if not int(bdrop["subcontainer"].getValue()):
                    continue

                if bdrop["name_layer"].getValue() != self.name():
                    continue

                return bdrop["range"].getValue(), bdrop["frames"].getValue()

        return "0", "0"

    def load(self):
        """load this render layer into nuke"""
        Create().load(self)

    def remove(self):
        """removes backdrop and all read nodes"""
        RemoveRenderLayer(self).remove()

    def reformat(self):
        """calls for reformat 4k renders"""
        ReformatRenderLayer(self)
