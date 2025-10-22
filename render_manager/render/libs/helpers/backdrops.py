# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - CreateRead for RenderLayer
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import contextlib

try:
    import nuke
    import nukescripts
except ImportError:
    import render_manager.mocks.nuke as nuke
from rm2.render_manager.render.render_layer_types import Render
from rm2.render_manager.render.libs.helpers.reads import create_all_aovs
from rm2.render_manager.render.libs.helpers.config import BACKDROP_SIZE, ROL_POSITION_X
from rm2.render_manager.render.libs.helpers.config import OFFSET_BDROP_X, OFFSET_BDROP_Y
from rm2.render_manager.render.libs.helpers.config import COLOR_BACKDROP_RL


def get_next_row_container(render: Render) -> int:
    """Get the maximum row number of the backdrop node for this layer in the script."""

    same_name_backdrops = []  # Lista para almacenar los backdrops con el mismo nombre

    for backdrop in nuke.allNodes("BackdropNode"):
        try:
            if backdrop["container"].getValue():
                if render.rol_main() == backdrop["rol_main"].getValue():
                    same_name_backdrops.append(backdrop)
        except (NameError, AttributeError):
            continue

    return get_max_row_backrops(same_name_backdrops)


def get_next_row_subcontainer(render: Render) -> int:
    """Get the maximum row number of the backdrop node for this layer in the script."""

    for backdrop in nuke.allNodes("BackdropNode"):
        try:
            if backdrop["container"].getValue():
                if render.rol_layer() == backdrop["rol_layer"].getValue():
                    return int(backdrop["row"].getValue())
        except (NameError, AttributeError):
            continue


def get_max_row_backrops(same_name_backdrops: list) -> int:
    """Get the maximum row number of the backdrop node for this layer in the script."""
    if same_name_backdrops:
        # Obtener la fila máxima entre los backdrops con el mismo nombre
        max_row = max(
            int(backdrop["row"].getValue()) for backdrop in same_name_backdrops
        )
        return max_row + 1
    else:
        return 1


def create_backdrop_container(render: Render, row: int) -> str:
    """Create backdrop container for all renders"""

    # check in nuke if a backdrop node for this Render already exists
    for n in nuke.allNodes("BackdropNode"):
        with contextlib.suppress(NameError):
            if (
                n["rol_layer"].getValue() == render.rol_layer()
                and n["container"].getValue()
            ):
                return n

    node = _create_backdrop(render.prefix_rol_layer(), BACKDROP_SIZE["GENERAL"])
    node["tile_color"].setValue(COLOR_BACKDROP_RL[render.rol_main()])
    _add_attributes_tab(node, render, row, container=True)
    _move_backdrop(node)

    return node


def create_backdrop_subcontainer(render: Render, row: int):
    """Create backdrop for all renders"""

    connections = {}

    for bd in nuke.allNodes("BackdropNode"):
        with contextlib.suppress(NameError):
            if (
                bd["name_layer"].getValue() == render.name()
                and bd["subcontainer"].getValue()
            ):
                for node in bd.getNodes():
                    # Save current connections in dict
                    dependent_node = []

                    for _ in node.dependent():
                        dependent_node.append(_)

                    connections[node.name()] = dependent_node
                    nuke.delete(node)

                # overwrite current row before delete the subcontainer
                row = int(bd["row"].getValue())
                nuke.delete(bd)

    for backdrop_type in BACKDROP_SIZE:
        if backdrop_type == render.suffix():
            node = _create_backdrop(
                backdrop_type, BACKDROP_SIZE[backdrop_type], subcontainer=True
            )
            _add_attributes_tab(node, render, row, container=False)
            create_all_aovs(render)
            _move_backdrop(node)

            # restore connections
            for read in connections:
                for _node in connections[read]:
                    _node.setInput(0, nuke.toNode(read))


def _add_attributes_tab(
    node, render: Render, row: int, container: bool = False
) -> None:
    # sourcery skip: extract-duplicate-method
    """Create Arcane tab with knobs attributes"""
    Arcane_tab = nuke.Tab_Knob("ARCANE")
    node.addKnob(Arcane_tab)

    rol_main = nuke.String_Knob("rol_main", "rol_main")
    node.addKnob(rol_main)
    rol_main.setValue(render.rol_main())

    rol_layer = nuke.String_Knob("rol_layer", "rol_layer")
    node.addKnob(rol_layer)
    rol_layer.setValue(render.rol_layer())

    prefix_rol_layer = nuke.String_Knob("prefix_rol_layer", "prefix_rol_layer")
    node.addKnob(prefix_rol_layer)
    prefix_rol_layer.setValue(render.prefix_rol_layer())

    range_knob = nuke.String_Knob("range", "range")
    node.addKnob(range_knob)
    range_knob.setValue(render.frame_range())

    frames_knob = nuke.String_Knob("frames", "frames")
    node.addKnob(frames_knob)
    frames_knob.setValue(str(render.frames()))

    column = nuke.Int_Knob("column", "column")
    node.addKnob(column)
    column.setValue(ROL_POSITION_X[render.rol_main()])

    row_knob = nuke.Int_Knob("row", "row")
    node.addKnob(row_knob)
    row_knob.setValue(row)
    row_knob.clearFlag(nuke.STARTLINE)

    if container:
        container_knob = nuke.Boolean_Knob("container", "container")
        node.addKnob(container_knob)
        container_knob.setValue(container)
    else:
        subcontainer = nuke.Boolean_Knob("subcontainer", "subcontainer")
        node.addKnob(subcontainer)
        subcontainer.setValue(True)
        name = nuke.String_Knob("name_layer", "name_layer")
        node.addKnob(name)
        name.setValue(render.name())

    path_render = nuke.String_Knob("path_render", "path_render")
    node.addKnob(path_render)
    path_render.setValue(render.path())

    abc_version_knob = nuke.String_Knob("abc_version", "abc_version")
    node.addKnob(abc_version_knob)
    abc_version_knob.setValue(", ".join(render.abc_versions()))

    version_knob = nuke.String_Knob("version", "version")
    node.addKnob(version_knob)
    version_knob.setValue(str(render.int_version()))


def _move_backdrop(backdrop_node: str) -> None:
    """Custom position for backdrop"""

    backdrop = nuke.toNode(backdrop_node.name())
    column = int(backdrop["column"].getValue())
    row = int(backdrop["row"].getValue())

    node_in_backdrop = backdrop.getNodes()
    node_in_backdrop.append(backdrop_node)

    for node in node_in_backdrop:
        _xpos = int(node["xpos"].getValue())
        _ypos = int(node["ypos"].getValue())

        xpos_custom = OFFSET_BDROP_X * column
        ypos_custom = OFFSET_BDROP_Y * row

        node.setXYpos(_xpos + xpos_custom, _ypos + ypos_custom)

    nukescripts.clear_selection_recursive()


def _create_backdrop(
    backdrop_name: str, backdrop_size: dict, subcontainer: bool = False
):
    """creates and returns a backdrop node, sets pos/size/label attributes"""

    _label = backdrop_name
    if subcontainer:
        _label += " v[value version]"

    node = nuke.nodes.BackdropNode(
        label=_label,
        xpos=backdrop_size["xpos"],
        bdwidth=backdrop_size["bdwidth"],
        ypos=backdrop_size["ypos"],
        bdheight=backdrop_size["bdheight"],
        tile_color=backdrop_size["tile_color"],
        z_order=backdrop_size["z_order"],
        note_font_size=backdrop_size["note_font_size"],
    )

    return node
