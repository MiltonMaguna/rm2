# ----------------------------------------------------------------------------------------
# RenderManager Nuke
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
from PySide2 import QtCore
from PySide2.QtWidgets import QMenu, QAction, QTableView, QMainWindow, QDialog
from PySide2.QtGui import QIcon, QCursor
from PySide2.QtCore import Qt
from qt_log.stream_log import get_stream_logger
from backpack.folder_utils import browse_folder

from rm2.render_manager.mvc.config import MODEL_DATA
from rm2.render_manager.mvc.model import RenderTableModel
from rm2.render_manager.mvc.libs.edit_render_dialog import (
    EditRenderDialog,
)
from CG_Template.cg_template.main import run
from CG_Template.cg_template.libs.create_init_constant import create_init_constant

log = get_stream_logger("RenderManager - View")


class RendersView:
    def __init__(self, parent, ui: QMainWindow, table_widget: QTableView):
        """controls list view widget and model for a given version type
        Args:
            ui (version parent ui)
            table_widget (table widget to load)
        """
        self.parent = parent
        self.ui = ui
        self.model = RenderTableModel(self.ui, {})
        self.table_view = table_widget
        self.table_view.setModel(self.model)
        self.table_view.verticalHeader().setDefaultSectionSize(16)
        self.table_view.setIconSize(QtCore.QSize(16, 16))
        self.table_view.clicked.connect(self.item_selected)
        self.table_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.open_menu)
        self.table_view.verticalHeader().setDefaultSectionSize(20)
        for index, _, width in MODEL_DATA:
            self.table_view.setColumnWidth(index, width)

    def update_view(self, renders: dict):
        """main update method for this view"""
        self.table_view.clearSelection()
        self.model.renders = self.get_last_version(renders)
        self.model.layoutChanged.emit()

    def update_render_in_view(self, old_render, new_render):
        """Update a specific render in the view without reloading all data"""
        # Find the render in the current model data
        for i, render in enumerate(self.model.renders):
            if render.name() == old_render.name():
                # Replace the old render with the new one
                self.model.renders[i] = new_render

                # Notify the model that this specific row has changed
                top_left = self.model.index(i, 0)
                bottom_right = self.model.index(i, self.model.columnCount(None) - 1)
                self.model.dataChanged.emit(top_left, bottom_right)

                log.debug(f"Updated render {new_render.name()} in view at row {i}")
                return True

        log.warning(f"Could not find render {old_render.name()} in current view")
        return False

    def get_view_selection(self):
        """returns list of selected render_layers"""
        indexes = self.ui.table_view.selectionModel().selectedRows()
        return [self.model.renders[index.row()] for index in indexes]

    def item_selected(self, QModelindex):
        """call for item selection"""
        self.rl = None

        # take first selected item
        indexes = self.ui.table_view.selectionModel().selectedRows()
        if not indexes:
            return

        self.rl = self.model.renders[indexes[0].row()]

    def open_menu(self, _):
        """context menu for items"""
        self.menu = QMenu()
        load = self._add_menu_action(":/nuke", "Load Selected Layers")
        load.triggered.connect(self.parent.load_callback)
        self.menu.addSeparator()
        s_all = self._add_menu_action(":/dot_green_32", "Select All")
        s_all.triggered.connect(lambda: self.table_view.selectAll())
        s_none = self._add_menu_action(":/dot_red_32", "Select None")
        s_none.triggered.connect(lambda: self.table_view.clearSelection())
        self.menu.addSeparator()
        browse = self._add_menu_action(":/nuke", "Submit to Deadline: Reformat 50%")
        browse.triggered.connect(self.reformat_callback)
        constant = self._add_menu_action(":/nuke", "Init Constant")
        constant.triggered.connect(create_init_constant)
        template = self._add_menu_action(":/nuke", "CG Template")
        template.triggered.connect(self.template_structure_callback)
        browse = self._add_menu_action(":/browse", "Browse Folder")
        browse.triggered.connect(self.browse_render_layer)
        self.menu.popup(QCursor.pos())
        select_version = self._add_menu_action(":/version", "Select Version")
        select_version.triggered.connect(self.version_selector_callback)
        # select version

    def version_selector_callback(self):
        """Seleccionar versión del render sin modificar el original"""
        selection = self.get_view_selection()
        if not selection:
            log.warning("Nothing Selected!")
            return

        if len(selection) > 1:
            log.warning("Select only one render to change version!")
            return

        render = selection[0]
        # log.debug(f"Version selector callback: {render}")
        selected_render = self.open_version_selector_dialog(render)

        if selected_render:
            log.info(
                f"Successfully changed version for {render.name()} to v{selected_render.int_version()}"
            )
        else:
            log.info("Version selection cancelled")

    def open_version_selector_dialog(self, render):
        """Abrir diálogo para seleccionar versión sin modificar el render original"""

        log.debug(f"OPENING DIALOG: Original render version: {render.int_version()}")
        dialog = EditRenderDialog(render, self.parent.renders(), None)
        if dialog.exec_() == QDialog.Accepted:
            # Aplicar cambios de forma segura DESPUÉS de cerrar el diálogo
            success, selected_render = dialog.apply_changes_safely()

            if success and selected_render:
                log.debug(
                    f"AFTER DIALOG: Original render version: {render.int_version()}"
                )
                log.debug(
                    f"AFTER DIALOG: Selected render version: {selected_render.int_version()}"
                )
                log.debug(f"Nueva versión: {selected_render.int_version()}")
                log.debug(f"Nuevo usuario: {selected_render.user()}")
                log.debug(f"Nuevos frames: {selected_render.frame_range()}")
                log.debug(f"Nueva ruta: {selected_render.path()}")

                log.info(
                    f"Updated {selected_render.name()} to version {selected_render.int_version()}"
                )

                # Actualizar solo el render específico en la vista
                if self.update_render_in_view(render, selected_render):
                    log.debug("View updated successfully")
                else:
                    log.warning("Failed to update view, falling back to full reload")
                    self.update_view(self.parent.renders())

                return selected_render
            else:
                log.warning("Error applying changes to selected version")
                return None
        else:
            log.info("Version selection cancelled")
            return None

    def _add_menu_action(self, icon: str, text: str):
        """creates menu action and adds to menu"""
        self.menu.addSeparator()
        result = QAction(QIcon(icon), text, self.menu)
        self.menu.addAction(result)
        return result

    def reformat_callback(self):
        """calls for reformat module"""
        selection = self.get_view_selection()

        if not selection:
            log.warning("Nothing Selected!")

        for render in selection:
            render.reformat()

    def template_structure_callback(self):
        selection = self.get_view_selection()

        last_node = [0]

        for render in selection:
            if render.suffix() != "BTY":
                log.warning(f"NOT A BEAUTY LAYER {render.name()}")
                continue

            log.info(f"SELECTED NAME {render.name()}")
            last_node.append(run(render, last_node[-1]))

    def browse_render_layer(self):
        """opens render layers location on explorer"""
        if self.rl:
            browse_folder(self.rl.path())

    def get_last_version(self, renders):
        """Get the latest version of each render class from a collection of renders.
        This method processes a dictionary of renders organized by roles and returns
        a list containing only the highest version of each unique render class.

        Args:
            renders (dict): A dictionary where keys are role names and values are
                           lists of render objects. Each render object must have
                           name() and int_version() methods.
        Returns:
            list: A list of render objects, each representing the latest version
                  of its respective render class.
        Note:
            - Renders are grouped by their name() method return value
            - Version comparison is done using the int_version() method
            - If a render class appears multiple times, only the one with the
              highest version number is included in the result
            - Handles edge case where current_latest might be a list (though
              this shouldn't normally occur)
        """

        latest_renders = {}

        for rol in renders.keys():
            for render in renders[rol]:
                render_class = render.name()  # o el criterio que uses para agrupar

                if render_class not in latest_renders:
                    latest_renders[render_class] = render
                else:
                    current_latest = latest_renders[render_class]

                    # Verificar si current_latest es una lista (no debería serlo)
                    if isinstance(current_latest, list):
                        # Si es una lista, tomar el de mayor versión
                        current_latest = max(
                            current_latest, key=lambda r: r.int_version()
                        )
                        latest_renders[render_class] = current_latest
                    elif render.int_version() > current_latest.int_version():
                        latest_renders[render_class] = render

        return list(latest_renders.values())
