# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Main RenderLayer Class
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import contextlib
import os

try:
    import nuke
except ImportError:
    import RenderManager2.render_manager2.mocks.nuke as nuke

from RenderManager2.render_manager2.core.libs.reformat import ReformatRenderLayer
from RenderManager2.render_manager2.render.libs.create import Create
from RenderManager2.render_manager2.render.libs.remove import RemoveRenderLayer
from RenderManager2.render_manager2.render.render_states import OUTDATED, SYNC, UNLOADED


class Render:
    def __init__(self, path: str, name: str, aovs: list, info_json: dict) -> None:
        """Render Layer Object.

        Args:
            path (str): disk path to this render layer.
            name (str): name of this render layer.
            aovs (list): list of aovs for this render layer.
            info_json (dict): info json dict for this render layer.
        """
        self._path = path
        self._name = name
        self._aovs = aovs
        self._info_json = info_json

    def __str__(self) -> str:
        return f'RENDER LAYER {self.name()}, path {self.path()}, aovs {self.aovs()}'

    def name(self) -> str:
        """Return render layer name.

        Example:
            RND_BG_TECH
            RND_ALL_CRYPTO
        """
        return self._name

    def suffix(self) -> str:
        """Return suffix name.

        Example:
            TECH
            CRYPTO
        """
        return self._name.split('_')[-1]

    def rol_layer(self) -> str:
        """Return rol layer name.

        Example:
            BG
            ALL
        """
        return ('_').join(self._name.split('_')[1:-1])

    def rol_main(self) -> str:
        """Return rol main name.

        Example:
            BG
            ALL
        """
        return self._name.split('_')[1]

    def prefix_rol_layer(self) -> str:
        """Return prefix rol layer name.

        Example:
            RND_BG
            RND_ALL
        """
        return self._name.rsplit('_', 1)[0]

    def path(self) -> str:
        """Return normalized windows path.

        Example:
            'I:/GizmoRD/FRAMES/DEV/030/CG/RND_BG_TECH/LGT_KAF_010_v0026'
            'I:/GizmoRD/FRAMES/DEV/030/CG/RND_ALL_CRYPTO/LGT_KAF_010_v0026'
        """
        return self._path.replace('\\', '/')

    def version(self) -> str:
        """Return version of this render layer.

        Example:
            LGT_KAF_010_v0026
        """
        _version = os.path.split(self.path())
        return _version[-1]

    def int_version(self) -> int:
        """Return int version of this render layer.

        Example:
            26
        """
        version = os.path.split(self.path())
        version = version[-1].rsplit('_', 2)[-1]
        version = ''.join([i for i in version if i.isdigit()])
        return int(version) if version else 0

    def name_version(self) -> str:
        """Return name of this render layer.

        Example:
            LGT_KAF_010
        """
        return self.version().rsplit('_', 1)[0]

    def aovs(self) -> list:
        """Return the list of aovs names for this render layer.

        Example:
            ['motionvector', 'N', 'P', 'UV', 'Z']
            ['crypto_asset', 'crypto_material', 'crypto_object']
        """
        return self._aovs

    def user(self) -> str:
        """Return user who created this render layer."""
        return self._info_json.get('user', 'jdo')

    def abc_versions(self) -> list:
        """Return list of alembic files used in this render layer."""
        return self._info_json.get('abc_versions', [])

    def get_aov_data(self, aov_name: str) -> dict:
        """Get all the data for this aov from disk files.

        Args:
            aov_name (str): name of the aov to get data for.
        """

        # filter only exr files
        aov_path = os.path.join(self.path(), aov_name)
        exr_files = [f for f in os.listdir(aov_path) if f.endswith('.exr')]

        if not exr_files:
            raise FileNotFoundError(f'No .exr files found in AOV path: {aov_path}')

        # get first and last frame name
        name, ver_ext = exr_files[0].rsplit('_', 1)
        first, extension = ver_ext.split('.')
        _, last_ver_ext = exr_files[-1].rsplit('_', 1)
        last = last_ver_ext.split('.')[0]

        return {
            'files': name,
            'frames': len(exr_files),
            'first': int(first),
            'last': int(last),
            'range': f'{first}-{last}',
            'extension': extension,
        }

    def frames(self) -> int:
        """Return range from first aov or 0."""
        return self.get_aov_data(self.aovs()[0])['frames'] if self.aovs() else 0

    def frame_range(self) -> str:
        """Return formatted frame range taken from first aov.

        Example:
            '1001-1020'
        """
        aov = self.aovs()[0] if self.aovs() else None
        return self.get_aov_data(aov)['range'] if aov else '0-0'

    def oiio_action(self) -> str:
        """Return script used for reformat render 50% over deadline."""
        return 'reformat' if self.suffix() == 'BTY' else 'resample'

    def status(self) -> int:
        """Return state of this render layer."""
        if not self.version_from_read():
            return UNLOADED.value
        return (
            OUTDATED.value
            if self.version_from_read() < self.int_version()
            else SYNC.value
        )

    def status_text(self) -> str:
        """Return text for status column."""
        if not self.status():
            return UNLOADED.label
        return OUTDATED.label if self.status() == OUTDATED.value else SYNC.label

    def version_from_read(self) -> int:
        """Return version of this render layer READ from current nukescript."""
        for bdrop in nuke.allNodes('BackdropNode'):
            with contextlib.suppress(NameError, ValueError):
                if not int(bdrop['subcontainer'].getValue()):
                    continue

                if bdrop['name_layer'].getValue() != self.name():
                    continue

                return int(bdrop['version'].getValue())

        return 0

    def abc_version_from_backdrop(self) -> str:
        """Return the abc version string from the backdrop node."""
        for bdrop in nuke.allNodes('BackdropNode'):
            with contextlib.suppress(NameError, ValueError):
                if not int(bdrop['subcontainer'].getValue()):
                    continue

                if bdrop['name_layer'].getValue() != self.name():
                    continue

                abc_versions = bdrop['abc_version'].getValue()

                return [item.strip() for item in abc_versions.split(',')]

        return 'Not Found'

    def ranges_from_read(self) -> tuple:
        """Return range and frame count of this render layer READ from current nukescript."""
        for bdrop in nuke.allNodes('BackdropNode'):
            with contextlib.suppress(NameError, ValueError):
                if not int(bdrop['subcontainer'].getValue()):
                    continue

                if bdrop['name_layer'].getValue() != self.name():
                    continue

                return bdrop['range'].getValue(), bdrop['frames'].getValue()

        return '0', '0'

    def load(self):
        """Load this render layer into nuke."""
        Create().load(self)

    def remove(self):
        """Remove backdrop and all read nodes."""
        RemoveRenderLayer(self).remove()

    def reformat(self):
        """Call for reformat 4k renders."""
        ReformatRenderLayer(self)
