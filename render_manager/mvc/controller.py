# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import json
from PySide2.QtWidgets import QMainWindow
from qt_log.stream_log import get_stream_logger
from backpack.test_utils import time_function_decorator
from backpack.cache import timed_lru_cache

from Test_RenderManager.render_manager.mvc.view import RendersView

# from Test_RenderManager.render_manager.core.disk_collector import collect_render_layers_from
from Test_RenderManager.render_manager.core.dl_collector_job.deadline_collector import (
    collect_render_layers_from_deadline,
)
from Test_RenderManager.render_manager.render.render_states import SYNC

log = get_stream_logger("RenderManager")

# json_file_path = (
# r"D:\repo\Test_RenderManager\tests\test_data\jobs_KIT_0070_MayaBatch.json"
# )


class Controller:
    def __init__(self, parent: QMainWindow):
        self.parent = parent
        self.ui = parent.ui
        self.view = RendersView(self, self.ui, self.ui.table_view)

        log.debug(f"Parent: {self.parent}")

        # signal connections
        self.ui.btn_import.clicked.connect(self.load_callback)
        self.ui.btn_remove.clicked.connect(self.remove_callback)

    def renders(self):
        """
        Get the list of renders.
        Returns:
            list: The list of renders managed by this controller.
        """

        return self._renders

    @time_function_decorator
    @timed_lru_cache(seconds=30)
    def reset_db(self, json_file_path: str):
        """clear find cache for shaders"""
        log.process("Reloading Renders....")
        # self._renders = collect_render_layers_from(path)
        self._renders = collect_render_layers_from_deadline(
            self.load_json(json_file_path)
        )
        # log.info(f"Done. {len(self.renders())} Renders's found")
        self.view.update_view(self.renders())

    # ------------------------------------------------------------------------------------
    # ASSETS CALLBACKS
    # ------------------------------------------------------------------------------------

    def get_view_selection(self):
        """returns list of selected render_layers"""
        indexes = self.ui.table_view.selectionModel().selectedRows()
        return [self.view.model.renders[index.row()] for index in indexes]

    def load_callback(self):
        """load selected render_layers"""
        selection = self.get_view_selection()
        if not selection:
            log.warning("Nothing Selected!")
            return

        counter, count_max = 1, len(selection)
        for render in selection:
            log.process(f"Loading: {render.name()} ({counter} of {count_max})")

            if render.status() != SYNC.value:
                render.load()

            counter += 1

        log.done("RenderLayers loaded.")
        self.parent.refresh()

    def remove_callback(self):
        """removes selected assets and their shaders"""
        selection = self.get_view_selection()
        if not selection:
            log.warning("Nothing Selected!")

        for render in selection:
            render.remove()

        self.parent.refresh()

    def load_json(self, json_file_path: str) -> dict:
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except ImportError:
            print("❌ ImportError: RenderCollector module not found.")
            return {}

    def edit_callback(self):
        """editar render seleccionado"""
        selection = self.get_view_selection()
        if not selection:
            log.warning("Nothing Selected!")
            return

        if len(selection) > 1:
            log.warning("Select only one render to edit!")
            return

        render = selection[0]
        self.view.open_edit_dialog(render)
