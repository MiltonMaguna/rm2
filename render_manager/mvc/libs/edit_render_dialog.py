from PySide2.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QHeaderView,
    QLabel,
    QAbstractItemView,
)
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QFont
from Test_RenderManager.render_manager.core.dl_collector_job.libs.render.render_layer import (
    Render,
)
from qt_log.stream_log import get_stream_logger

log = get_stream_logger("RenderManager - TEST - EditRenderDialog")


class VersionTableModel(QAbstractTableModel):
    def __init__(self, versions):
        super().__init__()
        self.versions = versions
        self.headers = ["Version", "User", "Progress", "Frames", "Path"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.versions)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        version = self.versions[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:  # Version
                return str(version.int_version())
            elif column == 1:  # User
                return version.user()
            elif column == 2:  # Progress
                return version.progress_bar()
            elif column == 3:  # Frames
                return version.frame_range()
            elif column == 4:  # Path
                return version.path()

        elif role == Qt.FontRole:
            # Hacer bold la versión más alta
            if index.row() == 0:  # Asumiendo que está ordenado
                font = QFont()
                font.setBold(True)
                return font

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
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

    def __init__(
        self, render: Render, all_renders: dict[str, list[Render]], parent=None
    ):
        super().__init__(parent)
        self.render = render
        self.all_renders = all_renders
        self.selected_version = None

        log.debug(f"Editing render: {self.render.name()} v{self.render.int_version()}")

        self.setWindowTitle(f"Select Version for: {render.name()}")
        self.setModal(True)
        self.resize(800, 400)

        self.setup_ui()
        self.load_versions()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Label de información
        info_label = QLabel(f"Available versions for: {self.render.name()}")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(info_label)

        # Tabla de versiones
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setAlternatingRowColors(True)

        # Configurar headers
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        layout.addWidget(self.table_view)

        # Botones
        button_layout = QHBoxLayout()

        self.select_btn = QPushButton("Select Version")
        self.cancel_btn = QPushButton("Cancel")

        self.select_btn.clicked.connect(self.select_version)
        self.cancel_btn.clicked.connect(self.reject)
        self.select_btn.setEnabled(False)

        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def load_versions(self):
        """Cargar todas las versiones del mismo render"""
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
        """Callback cuando cambia la selección"""
        has_selection = len(selected.indexes()) > 0
        self.select_btn.setEnabled(has_selection)

        if has_selection:
            row = selected.indexes()[0].row()
            self.selected_version = self.model.versions[row]

    def select_version(self):
        """Seleccionar la versión elegida"""
        if self.selected_version:
            # En lugar de modificar self.render, simplemente asignamos la versión seleccionada
            self.render = self.selected_version
            log.debug(
                f"Selected version: {self.render.name()} v{self.render.int_version()}"
            )
            self.accept()
