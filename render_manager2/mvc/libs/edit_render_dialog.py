try:
    from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
    from PySide2.QtGui import QFont
    from PySide2.QtWidgets import (
        QAbstractItemView,
        QDialog,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QPushButton,
        QTableView,
        QVBoxLayout,
    )

    PYSIDE_VERSION = 2
except ImportError:
    from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import (
        QAbstractItemView,
        QDialog,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QPushButton,
        QTableView,
        QVBoxLayout,
    )

    PYSIDE_VERSION = 6

from qt_log.stream_log import get_stream_logger
from RenderManager2.render_manager2.core.dl_collector_job.libs.render.render_layer import (
    Render,
)

log = get_stream_logger('RenderManager - EditRenderDialog')


class VersionTableModel(QAbstractTableModel):
    def __init__(self, versions):
        """Inicializa el modelo de tabla con las versiones proporcionadas.

        Args:
            versions (list[Render]): Lista de objetos Render que representan las versiones disponibles.
        """

        super().__init__()
        self.versions = versions
        self.headers = ['Version', 'Frames', 'Path']

    def rowCount(self, parent=QModelIndex()):  # noqa: N802
        """Retorna el número de filas en el modelo."""
        return len(self.versions)

    def columnCount(self, parent=QModelIndex()):  # noqa: N802
        """Retorna el número de columnas en el modelo."""
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        """Retorna los datos para una celda específica en el modelo."""
        if not index.isValid():
            return None

        version = self.versions[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return str(version.int_version())
            elif column == 1:
                return version.frame_range()
            elif column == 2:
                return version.path()

        elif role == Qt.FontRole:
            if index.row() == 0:
                font = QFont()
                font.setBold(True)
                return font

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):  # noqa: N802
        """Retorna los datos para los encabezados de columna."""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None


class EditRenderDialog(QDialog):
    """A dialog for selecting different versions of a render.

    This dialog displays a table of all available versions for a given render,
    allowing the user to select a specific version. The versions are sorted
    by version number in descending order (highest first).

    Args:
        render (Render): The current render object to find versions for.
        all_renders (dict[str, list[Render]]): Dictionary containing all available
            renders organized by role, where each role maps to a list of Render objects.
        parent (QWidget, optional): Parent widget for the dialog. Defaults to None.

    Attributes:
        render (Render): The currently selected render object.
        all_renders (dict[str, list[Render]]): All available renders by role.

    Methods:
        setup_ui(): Creates and configures the user interface elements.
        load_versions(): Loads and displays all versions of the current render.
        on_selection_changed(selected, deselected): Handles table selection changes.
        select_version(): Confirms the selected version and closes the dialog.
    """

    def __init__(self, render: Render, all_renders: dict[str, list[Render]], parent=None):
        """Inicializa el diálogo de edición de render.

        Args:
            render (Render): El objeto Render actual para el cual se buscan versiones.
            all_renders (dict[str, list[Render]]): Diccionario que contiene todos los renders disponibles organizados por rol.
            parent (QWidget, optional): Widget padre para el diálogo. Por defecto es None.
        """
        super().__init__(parent)
        self.render = render
        self.all_renders = all_renders
        self.selected_version = None

        self.setWindowTitle(f'Select Version for: {render.name()}')
        self.setModal(True)
        self.resize(800, 400)

        self.setup_ui()
        self.load_versions()

    def setup_ui(self):
        """Crea y configura los elementos de la interfaz de usuario."""
        layout = QVBoxLayout(self)

        info_label = QLabel(f'Available versions for: {self.render.name()}')
        info_label.setStyleSheet('font-weight: bold; margin-bottom: 10px;')
        layout.addWidget(info_label)

        self.table_view = QTableView()

        # PySide6 movió algunas flags a Qt.ItemFlag y enums a sus propias clases
        if PYSIDE_VERSION == 6:
            self.table_view.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )
            self.table_view.setSelectionMode(
                QAbstractItemView.SelectionMode.SingleSelection
            )
        else:
            self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table_view.setAlternatingRowColors(True)

        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)

        if PYSIDE_VERSION == 6:
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        else:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)

        layout.addWidget(self.table_view)

        button_layout = QHBoxLayout()

        self.select_btn = QPushButton('Select Version')
        self.cancel_btn = QPushButton('Cancel')

        self.select_btn.clicked.connect(self.select_version)
        self.cancel_btn.clicked.connect(self.reject)
        self.select_btn.setEnabled(False)

        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def load_versions(self):
        """Cargar todas las versiones del mismo render."""
        same_name_renders = []

        # Iterar sobre la estructura de diccionario con roles
        for rol in self.all_renders.keys():
            for layer in self.all_renders[rol]:
                # Filtrar layers con el mismo nombre
                if layer.name() == self.render.name():
                    same_name_renders.append(layer)

        # Ordenar por versión (más alta primero)
        same_name_renders.sort(key=lambda x: x.int_version(), reverse=True)

        # Crear y asignar modelo
        self.model = VersionTableModel(same_name_renders)
        self.table_view.setModel(self.model)

        # Conectar la señal después de asignar el modelo
        self.table_view.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )

        # Remover la selección automática de la versión actual
        self.table_view.clearSelection()

    def on_selection_changed(self, selected, deselected):
        """Callback cuando cambia la selección."""
        has_selection = len(selected.indexes()) > 0
        self.select_btn.setEnabled(has_selection)

        if has_selection:
            row = selected.indexes()[0].row()
            self.selected_version = self.model.versions[row]

    def select_version(self):
        """Seleccionar la versión elegida."""
        if self.selected_version:
            # NO modificar self.render, solo guardamos la versión seleccionada
            log.info(
                f'Selected version: {self.selected_version.name()} v{self.selected_version.int_version()}'
            )
            self.accept()
        else:
            log.warning('No version selected')
            self.reject()

    def apply_changes_safely(self):
        """Aplica los cambios de forma segura después de cerrar el diálogo.

        Esta función retorna el render seleccionado para que la vista padre
        pueda actualizar correctamente su estructura de datos.

        Returns:
            tuple: (bool, Render|None) - (success, selected_render)
        """
        if not hasattr(self, 'selected_version') or self.selected_version is None:
            log.debug('No hay versión seleccionada para aplicar cambios')
            return False, None

        try:
            log.debug(
                f'Aplicando cambios desde versión {self.selected_version.int_version()}'
            )
            log.debug(
                f'Render seleccionado: {self.selected_version.name()} v{self.selected_version.int_version()}'
            )
            log.debug(f'Usuario: {self.selected_version.user()}')
            log.debug(f'Frames: {self.selected_version.frame_range()}')
            log.debug(f'Path: {self.selected_version.path()}')

            log.info(
                f'Cambios aplicados exitosamente a {self.selected_version.name()} v{self.selected_version.int_version()}'
            )
            return True, self.selected_version

        except Exception as e:
            log.error(f'Error al aplicar cambios: {e}')
            return False, None

    def get_selected_render(self):
        """Retorna el render seleccionado.

        Returns:
            Render|None: El render seleccionado o None si no hay selección
        """
        return getattr(self, 'selected_version', None)
