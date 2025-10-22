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

from rm2.render_manager.core.libs.reformat import ReformatRenderLayer
from rm2.render_manager.render.libs.create import Create
from rm2.render_manager.render.libs.remove import RemoveRenderLayer
from rm2.render_manager.render.render_states import OUTDATED, SYNC, UNLOADED


class Render:
    def __init__(self, path: str, name: str, aovs: list, info_json: dict) -> None:
        """Render Layer Object
        Args:
            path (str): disk path to this render layer
            name (str): name of this render layer
            aovs (list): list of aovs for this render layer
        """
        self._path = path
        self._name = name
        self._aovs = aovs
        self._info_json = info_json

    def __str__(self) -> str:
        return f"RENDER LAYER {self.name()}, path {self.path()}, aovs {self.aovs()}"

    def name(self) -> str:
        """returns render layer name
        Eg: RND_BG_TECH
        Eg: RND_ALL_CRYPTO
        """
        return self._name

    def suffix(self) -> str:
        """returns suffix name
        Eg: TECH
        Eg: CRYPTO
        """
        return self._name.split("_")[-1]

    def rol_layer(self) -> str:
        """returns rol layer name
        Eg: BG
        Eg: ALL
        """
        return ("_").join(self._name.split("_")[1:-1])

    def rol_main(self) -> str:
        """returns rol main name
        Eg: BG
        Eg: ALL
        """
        return self._name.split("_")[1]

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
        return self._path.replace("\\", "/")

    def version(self) -> str:
        """returns version of this render layer
        Eg: LGT_KAF_010_v0026
        """
        _version = os.path.split(self.path())
        return _version[-1]

    def int_version(self) -> int:
        """returns int version of this render layer
        Eg: 26
        """
        version = os.path.split(self.path())
        version = version[-1].rsplit("_", 2)[-1]
        version = "".join([i for i in version if i.isdigit()])
        return int(version)

    def name_version(self) -> str:
        """returns name of this render layer
        Eg: LGT_KAF_010
        """
        return self.version().rsplit("_", 1)[0]

    def aovs(self) -> list:
        """returns the list of aovs names for this render layer
        Eg: ['motionvector', 'N', 'P', 'UV', 'Z']
        Eg: ['crypto_asset', 'crypto_material', 'crypto_object']
        """
        return self._aovs

    def user(self) -> str:
        """returns user who created this render layer"""
        return self._info_json.get("user", "jdo")

    def abc_versions(self) -> list:
        """returns list of alembic files used in this render layer"""
        return self._info_json.get("abc_versions", [])

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
        return self.get_aov_data(self.aovs()[0])["frames"] if self.aovs() else 0

    def frame_range(self) -> str:
        """returns formatted frame range taken from first aov
        Eg: '1001-1020'
        """
        aov = self.aovs()[0] if self.aovs() else None
        return self.get_aov_data(aov)["range"] if aov else "0-0"

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

    def abc_version_from_backdrop(self) -> str:
        """Returns the abc version string from the backdrop node"""
        for bdrop in nuke.allNodes("BackdropNode"):
            with contextlib.suppress(NameError, ValueError):
                if not int(bdrop["subcontainer"].getValue()):
                    continue

                if bdrop["name_layer"].getValue() != self.name():
                    continue

                abc_versions = bdrop["abc_version"].getValue()

                return [item.strip() for item in abc_versions.split(",")]

        return "Not Found"

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
