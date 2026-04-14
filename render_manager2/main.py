# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
from arcane.core.setenv.decorators import project_setter
from plugin.ui.arcane_utils import pipeline_names
from plugin.ui.loader_nuke import LoaderNuke
from plugin.ui.Qt import QtCompat

try:
    from PySide2 import QtCore, QtWidgets

    PYSIDE_VERSION = 2
except ImportError:
    from PySide6 import QtCore, QtWidgets

    PYSIDE_VERSION = 6

from pyside_ui_backpack import Colors, css, style_push_button
from qt_log.qt_ui_logger import QtUILogger
from qt_log.stream_log import get_stream_logger

from arcane import get_session
from RenderManager2.render_manager2.mvc.controller import Controller
from RenderManager2.render_manager2.version import __qt__, app_name, ui_file, version

log = get_stream_logger('RenderManager2 - main')
PLUGIN = 'MayaBatch'
OUTPUT_DIR = r'C:\temp\deadline_jobs'


class RenderManager(QtWidgets.QMainWindow):
    @project_setter(log)
    def __init__(self, parent=LoaderNuke().getNukeWindow(), debug: bool = False):
        """Initialize the RenderManager main window.

        Args:
            parent (QWidget, optional): Parent widget, defaults to the Nuke main window.
            debug (bool, optional): Enable debug mode. Defaults to False.
            Sets up the UI from the compiled resource file, establishes window properties
            (stays on top, fixed size, centered position), initializes logging, creates a
            session, sets up signal/slot connections, and instantiates the application
            controller.
        """
        super().__init__(parent)
        self.ui = QtCompat.loadUi(ui_file)
        self.setCentralWidget(self.ui)
        self.setObjectName(__qt__)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.Window)
        self.adjustSize()
        self.setWindowTitle(f'{app_name} {version}')
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
        """Sets qt connections and css."""
        self.ui.mnu_reset.triggered.connect(self.reset_ui)
        self.ui.mnu_quit.triggered.connect(lambda: self.close())

        style_push_button(self.ui, self.ui.btn_import, color=Colors.BG_BLUE)
        style_push_button(self.ui, self.ui.btn_remove, color=Colors.BG_RED)

        for grp_widget in self.ui.findChildren(QtWidgets.QGroupBox):
            grp_widget.setStyleSheet(css.groupbox_white_css)

    def reset_ui(self):
        """UI Reset."""
        log.info(' '.join([app_name, version]))
        self.setWindowTitle(f'{app_name} [{self.session.project_name()}]')
        self.refresh()

    def refresh(self):
        """Refresh the UI and update the render path."""
        self._path = 'not set'
        self.ui.cbox_shot.clear()
        self.ui.cbox_shot.addItem('Not in Context')

        sequence_name, shot_name = pipeline_names()
        if self.debug:
            sequence_name, shot_name = 'DEV', '030'
        shot = self.session.get_shot(sequence_name, shot_name)

        if not shot:
            return

        log.info(f'Current Context: {shot.parent_name()} {shot.name()}')
        self.ui.cbox_shot.clear()
        self.ui.cbox_shot.addItem(f'{shot.parent_name()}-{shot.name()}')
        # ? CONTINUAR PARA PODER IMPORTAR READS DE OTRO SHOTS
        # ?items = [f'{shot.parent_name()}-{shot.name()}', 'DEV_0010']
        # ? self.ui.cbox_shot.addItems(items)

        # json_file_path = collect_by_shot_with_json(
        # sequence_name, shot_name, PLUGIN, OUTPUT_DIR
        # )
        # self.controller.reset_db(self.load_json())

        self._path = shot.path_renders_cg()
        # log.info(f"Render Path: {self.path()}")
        # log.info(f"Path {self.path()}")
        # self.ui.le_path.setText(str(self.path()))
        # if self.path():
        #    self.controller.reset_db(self.path())

        self.controller.reset_db(self.path())

    def path(self):
        """Returns render path for current shot."""
        return self._path

    def closeEvent(self, event):
        """Final close event method."""
        self.loggers.close()
        self.close()


def run_test(debug: bool = False):
    """Run the RenderManager in test mode."""
    RenderManager(debug=debug)
