# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import json

try:
    from PySide2.QtWidgets import QMainWindow

    PYSIDE_VERSION = 2
except ImportError:
    from PySide6.QtWidgets import QMainWindow

    PYSIDE_VERSION = 6
from backpack.cache import timed_lru_cache
from backpack.test_utils import time_function_decorator
from qt_log.stream_log import get_stream_logger

from RenderManager2.render_manager2.core.disk_collector import (
    collect_render_layers_by_role,
)
from RenderManager2.render_manager2.mvc.view import RendersView

log = get_stream_logger('RenderManager2 - Controller')


class Controller:
    def __init__(self, parent: QMainWindow):
        """Initialize the controller with the parent widget.

        Args:
            parent (QMainWindow): The parent widget for this controller.
        """
        self.parent = parent
        self.ui = parent.ui
        self.view = RendersView(self, self.ui, self.ui.table_view)

        log.debug(f'Parent: {self.parent}')

        # signal connections
        self.ui.btn_import.clicked.connect(self.load_callback)
        self.ui.btn_remove.clicked.connect(self.remove_callback)

    def renders(self):
        """Get the list of renders.

        Returns:
            list: The list of renders managed by this controller.
        """

        return self._renders

    @time_function_decorator
    @timed_lru_cache(seconds=30)
    def reset_db(self, path):
        """Clear find cache for shaders."""
        log.process('Reloading Renders....')
        self._renders = collect_render_layers_by_role(path)
        self.view.update_view(self.renders())

    # ------------------------------------------------------------------------------------
    # ASSETS CALLBACKS
    # ------------------------------------------------------------------------------------

    def get_view_selection(self):
        """Returns list of selected render_layers."""
        indexes = self.ui.table_view.selectionModel().selectedRows()
        return [self.view.model.renders[index.row()] for index in indexes]

    def load_callback(self):
        """Load selected render_layers."""
        selection = self.get_view_selection()
        log.debug(f'Selection: {selection}')

        if not selection:
            log.warning('Nothing Selected!')
            return

        counter, count_max = 1, len(selection)
        for render in selection:
            log.process(
                f'Loading: {render.name()}_{render.version()} ({counter} of {count_max})'
            )

            # if render.status() != SYNC.value:
            render.load()

            counter += 1

        log.done('RenderLayers loaded.')
        self.parent.refresh()

    def remove_callback(self):
        """Removes selected assets and their shaders."""
        selection = self.get_view_selection()
        if not selection:
            log.warning('Nothing Selected!')

        for render in selection:
            render.remove()

        self.parent.refresh()

    def load_json(self, json_file_path: str) -> dict:
        """Load a JSON file and return its contents as a dictionary.

        Args:
            json_file_path (str): The path to the JSON file to load.

        Returns:
            dict: The contents of the JSON file as a dictionary.
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except ImportError:
            print('❌ ImportError: RenderCollector module not found.')
            return {}
