# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt, QAbstractTableModel
from qt_log.stream_log import get_stream_logger

from rm2.render_manager.mvc.config import MODEL_DATA, MODEL_DISPLAYROLE

log = get_stream_logger("RenderManager - Model")


class RenderTableModel(QAbstractTableModel):
    # colors for status text: red, yellow, green
    STATUS_COLOR = [QColor(255, 100, 100), QColor(0, 250, 250), QColor(20, 250, 20)]

    def __init__(self, parent: QMainWindow, renders: dict, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.renders = renders

    def rowCount(self, parent):
        return len(self.renders)

    def columnCount(self, parent):
        return len(MODEL_DATA)

    def data(self, index, role):
        if not index.isValid():
            return None

        # align role
        if role == Qt.TextAlignmentRole:
            # Alineación específica por columna
            if index.column() == 0:  # Columna del nombre
                return Qt.AlignLeft | Qt.AlignVCenter
            else:  # Resto de columnas
                return Qt.AlignCenter

        render = self.renders[index.row()]

        # ColorRole for Sync Status
        if role == Qt.ForegroundRole and index.column():
            if index.column() == 5:
                return self.STATUS_COLOR[render.status()]

            return QColor(230, 230, 230)

        # display role filter
        if role != Qt.DisplayRole:
            return None

        # render object data
        column_data = dict(MODEL_DISPLAYROLE)
        column_data[0] = render.name()
        column_data[1] = render.version_from_read()
        nrange, nframes = render.ranges_from_read()
        column_data[2] = nrange
        column_data[3] = nframes
        column_data[4] = len(render.aovs())
        column_data[5] = render.status_text()

        return column_data[index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return MODEL_DATA[col][1]
        return None
