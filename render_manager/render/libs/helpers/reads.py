try:
    import nuke
except ImportError:
    import render_manager.mocks.nuke as nuke
from render_manager.render.render_layer_types import Render
from render_manager.render.libs.helpers.config import POSITION_READ, NODE_CUSTOM
from render_manager.render.libs.helpers.config import ANCHOR_READ, OFFSET_READ_X
from render_manager.render.libs.helpers.config import BACKDROP_SIZE, OFFSET_BORDER_BACKDROP
from plugin.utils_nuke.config_colorspace import EXR_CG


def create_all_aovs(render: Render) -> None:
    ''' Create all reads for all aovs renders in a shot '''

    offset_x = 0
    second_line = False
    # print(f'OFFSET START {offset_x}')
    for aov_name in render.aovs():

        pos_read_x = POSITION_READ[render.suffix()][0]
        pos_read_y = POSITION_READ[render.suffix()][1]
        # print(f"POS READ X Y {pos_read_x} {pos_read_y}")

        if second_line:
            # print('SECOND LINE')
            pos_read_y = POSITION_READ[render.suffix()][1] + 150

        if offset_x > pos_read_x:
            pos_read_x = offset_x

        node_xpos = create_node(render, aov_name, pos_read_x, pos_read_y)
        # print(f'NODE XPOS{node_xpos}')

        offset_x = node_xpos + ANCHOR_READ + OFFSET_READ_X

        if node_xpos > BACKDROP_SIZE["BTY"]['bdwidth'] + OFFSET_BORDER_BACKDROP:
            # print('the last node is mayor than the backdrop size')
            offset_x = 0
            second_line = True

        # print(f'OFFSET END {offset_x}')
        # print('-' * 10)


def create_node(render: Render, aov_name: str, pos_read_x: int, pos_read_y: int) -> int:
    ''' Create nodes for all aovs renders in a shot '''

    node = nuke.nodes.Read()
    node.setName(f'{render.rol_layer()}_{aov_name}_00')

    arcane_tab = nuke.Tab_Knob('ARCANE')
    node.addKnob(arcane_tab)

    aov_data = render.get_aov_data(aov_name)
    file = f'{render.path()}/{aov_name}/{aov_data["files"]}_####.{aov_data["extension"]}'

    node['file'].setValue(file)
    node['xpos'].setValue(pos_read_x)
    node['ypos'].setValue(pos_read_y)
    node['first'].setValue(aov_data["first"])
    node['last'].setValue(aov_data["last"])
    node['label'].setValue(aov_name)
    node['colorspace'].setValue(EXR_CG)
    node['postage_stamp'].setValue(NODE_CUSTOM['postage_stamp'])

    name_knob = nuke.String_Knob('name_layer', 'name_layer')
    node.addKnob(name_knob)
    name_knob.setValue(render.name())

    rol_layer_knob = nuke.String_Knob('rol_layer', 'rol_layer')
    node.addKnob(rol_layer_knob)
    rol_layer_knob.setValue(render.rol_layer())

    suffix_knob = nuke.String_Knob('suffix', 'suffix')
    node.addKnob(suffix_knob)
    suffix_knob.setValue(render.suffix())

    aov_name_knob = nuke.String_Knob('aov_name', 'aov_name')
    node.addKnob(aov_name_knob)
    aov_name_knob.setValue(aov_name)

    version_label_knob = nuke.String_Knob('version_label', 'version_label')
    node.addKnob(version_label_knob)
    version_label_knob.setValue(render.version())

    version_knob = nuke.String_Knob('version_short', 'version_short')
    node.addKnob(version_knob)
    version_knob.setValue(str(render.int_version()))

    return node.xpos()
