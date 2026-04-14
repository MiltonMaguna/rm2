# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
try:
    from PySide2.QtCore import QAbstractTableModel, Qt
    from PySide2.QtGui import QColor
    from PySide2.QtWidgets import QMainWindow

    PYSIDE_VERSION = 2
except ImportError:
    from PySide6.QtCore import QAbstractTableModel, Qt
    from PySide6.QtGui import QColor
    from PySide6.QtWidgets import QMainWindow

    PYSIDE_VERSION = 6
from qt_log.stream_log import get_stream_logger

from RenderManager2.render_manager2.mvc.config import MODEL_DATA, MODEL_DISPLAYROLE

log = get_stream_logger('RenderManager2 - Model')


class RenderTableModel(QAbstractTableModel):
    # colors for status text: red, yellow, green
    STATUS_COLOR = [QColor(255, 100, 100), QColor(0, 250, 250), QColor(20, 250, 20)]

    def __init__(self, parent: QMainWindow, renders: dict, *args):  # noqa: D417
        """Initialize the render table model.

        Args:
            parent (QMainWindow): parent widget for the model.
            renders (dict): dictionary of render objects to display in the table.
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.renders = renders

    def rowCount(self, parent):  # noqa: N802
        """Returns the number of rows in the model."""
        return len(self.renders)

    def columnCount(self, parent):  # noqa: N802
        """Returns the number of columns in the model."""
        return len(MODEL_DATA)

    def data(self, index, role):
        """Returns the data for a given index and role."""
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

        # ColorRole for Sync Status and Render Roles
        if role == Qt.ForegroundRole:
            # Status column gets specific status colors
            if index.column() == 4:
                return self.STATUS_COLOR[render.status()]
            return QColor(230, 230, 230)

        # ToolTip role for ABC versions column
        if role == Qt.ToolTipRole:
            if index.column() == 6:  # ABC versions column
                abc_versions = render.abc_version_from_backdrop()
                if abc_versions == 'Not Found':
                    return 'Not Found'
                if abc_versions:
                    tooltip_text = 'ABC Versions:\n' + '\n'.join(
                        [f'• {version}' for version in abc_versions]
                    )
                    return tooltip_text
                else:
                    return 'Not Found'
            return None

        # display role filter
        if role != Qt.DisplayRole:
            return None

        # render object data
        column_data = dict(MODEL_DISPLAYROLE)
        column_data[0] = render.name()
        column_data[1] = f'v00{render.version_from_read()}'
        column_data[2] = (
            f'v00{render.int_version()}'  # Mostrar la versión actual del render, no la cargada en Nuke            render.int_version()
        )
        nrange, _ = render.ranges_from_read()
        column_data[3] = nrange
        column_data[4] = render.status_text()
        column_data[5] = render.user()
        abc = render.abc_version_from_backdrop()
        column_data[6] = 'Not found.' if abc == 'Not Found' else ', '.join(abc)

        return column_data[index.column()]

    def headerData(self, col, orientation, role):  # noqa: N802
        """Returns the header data for a given column and role."""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return MODEL_DATA[col][1]
        return None
