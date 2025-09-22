# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
from PySide2 import QtCore, QtWidgets

from plugin.ui.Qt import QtCompat
from plugin.ui.loader_nuke import LoaderNuke
from plugin.ui.arcane_utils import pipeline_names

from qt_log.stream_log import get_stream_logger
from qt_log.qt_ui_logger import QtUILogger
from pyside_ui_backpack import style_push_button, Colors, css

from arcane import get_session
from arcane.core.setenv.decorators import project_setter
from .mvc.controller import Controller

from .core.dl_collector_job.collect_from_deadline import collect_by_shot_with_json
from .version import __qt__, version, app_name, ui_file

log = get_stream_logger("RenderManager - TEST")
PLUGIN = "MayaBatch"
OUTPUT_DIR = r"C:\temp\deadline_jobs"


class RenderManager(QtWidgets.QMainWindow):
    @project_setter(log)
    def __init__(self, parent=LoaderNuke().getNukeWindow(), debug: bool = False):
        super().__init__(parent)
        self.ui = QtCompat.loadUi(ui_file)
        self.setCentralWidget(self.ui)
        self.setObjectName(__qt__)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.Window)
        self.adjustSize()
        self.setWindowTitle(f"{app_name} {version}")
        self.setFixedSize(self.ui.maximumWidth(), self.ui.maximumHeight())
        self.move(parent.geometry().center() - self.ui.geometry().center())
        self.loggers = QtUILogger(self, self.ui.log_layout, [log])
        self.session = get_session()
        self.set_connections()
        self.show()
        self.debug = debug
        self.controller = Controller(self)
        self.reset_ui()

    def set_connections(self):
        """sets qt connections and css"""
        self.ui.mnu_reset.triggered.connect(self.reset_ui)
        self.ui.mnu_quit.triggered.connect(lambda: self.close())

        style_push_button(self.ui, self.ui.btn_import, color=Colors.BG_BLUE)
        style_push_button(self.ui, self.ui.btn_remove, color=Colors.BG_RED)

        for grp_widget in self.ui.findChildren(QtWidgets.QGroupBox):
            grp_widget.setStyleSheet(css.groupbox_white_css)

    def reset_ui(self):
        """UI Reset"""
        log.info(" ".join([app_name, version]))
        self.setWindowTitle(f"{app_name} [{self.session.project_name()}]")
        self.refresh()

    def refresh(self):
        """returns path from parser"""
        self._path = "not set"
        self.ui.cbox_shot.clear()
        self.ui.cbox_shot.addItem("Not in Context")

        sequence_name, shot_name = pipeline_names()
        if self.debug:
            sequence_name, shot_name = "DEV", "030"
        shot = self.session.get_shot(sequence_name, shot_name)

        if not shot:
            return

        log.info(f"Current Context: {shot.parent_name()} {shot.name()}")
        self.ui.cbox_shot.clear()
        self.ui.cbox_shot.addItem(f"{shot.parent_name()}-{shot.name()}")

        json_file_path = collect_by_shot_with_json(
            sequence_name, shot_name, PLUGIN, OUTPUT_DIR
        )
        # self.controller.reset_db(self.load_json())

        self._path = shot.path_renders_cg()
        # log.info(f"Render Path: {self.path()}")
        # log.info(f"Path {self.path()}")
        # self.ui.le_path.setText(str(self.path()))
        # if self.path():
        #    self.controller.reset_db(self.path())

        self.controller.reset_db(json_file_path)

    def path(self):
        """returns render path for current shot"""
        return self._path

    def closeEvent(self, event):
        """Final close event method"""
        self.loggers.close()
        self.close()


def run_test(debug: bool = False):
    RenderManager(debug=debug)
