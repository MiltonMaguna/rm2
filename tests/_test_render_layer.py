import pytest
from render_manager.core.disk_collector import collect_render_layers_from
from render_manager.render.render_states import OUTDATED, SYNC, UNLOADED


def test_collector_and_render_layer(shot_render_frames_path, mocked_nuke_no_nodes):

    renders = collect_render_layers_from(shot_render_frames_path)
    assert len(renders) == 2
    render = renders[1] if renders else None

    # ! we need another test creating the render_layer object from scratch without the collector
    # render = Render(path=shot_render_frames_path, name='RND_FG_BTY', aovs=['AO', 'beauty'])

    assert str(render) is not None
    assert render.name() == 'RND_FG_BTY'
    assert render.suffix() == 'BTY'
    assert render.rol_layer() == 'FG'
    assert render.rol_main() == 'FG'
    assert render.prefix_rol_layer() == 'RND_FG'
    assert render.path() == 'I:/GizmoRD/FRAMES/PYTEST/030/CG/RND_FG_BTY/LGT_KAF_010_v0026'
    assert render.aovs() == ['AO', 'beauty', 'crypto_asset', 'crypto_material',
                             'crypto_object', 'emission', 'specular']
    assert render.version() == 'LGT_KAF_010_v0026'
    assert render.int_version() == 26
    assert render.frames() == 10
    assert render.frame_range() == '1001-1010'
    assert render.oiio_action() == 'reformat'
    assert render.get_aov_data('AO') == {'files': 'RND_FG_BTY_AO',
                                         'frames': 10,
                                         'first': 1001,
                                         'last': 1010,
                                         'range': '1001-1010',
                                         'extension': 'exr'
                                         }
    assert render.status() == UNLOADED.value
    assert render.status_text() == UNLOADED.label
    assert render.version_from_read() == 0


def test_collector_and_render_layer_in_sync(shot_render_frames_path, read_node_same_version):

    renders = collect_render_layers_from(shot_render_frames_path)
    render = renders[1] if renders else None

    assert render.status() == SYNC.value
    assert render.status_text() == SYNC.label
    assert render.version_from_read() == 26


def test_collector_and_render_layer_outdated(shot_render_frames_path, read_node_outdated_version):

    renders = collect_render_layers_from(shot_render_frames_path)
    render = renders[1] if renders else None

    assert render.version_from_read() == 24
    assert render.status() == OUTDATED.value
    assert render.status_text() == OUTDATED.label


def test_remove_render_layer_no_nodes(shot_render_frames_path, mocked_nuke_no_nodes):
    renders = collect_render_layers_from(shot_render_frames_path)
    render = renders[1] if renders else None
    assert render.remove() is None


def test_remove_render_layer_with_nodes(shot_render_frames_path, read_node_same_version):
    renders = collect_render_layers_from(shot_render_frames_path)
    render = renders[1] if renders else None
    assert render.remove() is None


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
