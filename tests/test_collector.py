import os
import pytest
from render_manager.core.disk_collector import collect_render_layers_from
from render_manager.core.disk_collector import _get_render_layer_names, _get_last_version_path
from render_manager.core.disk_collector import _get_valid_render_layers, _get_aovs
from render_manager.core.disk_collector import check_for_empty_subfolders
from render_manager.core.disk_collector import check_for_files_exr


def test_collector(shot_render_frames_path):
    # test invalid path
    renders = collect_render_layers_from('Z:/invalid_path')
    assert len(renders) == 0

    # test individual functions

    empty = check_for_empty_subfolders(os.path.join(shot_render_frames_path, 'RND_MG_BAD'))
    assert empty is True

    empty = check_for_empty_subfolders(os.path.join(shot_render_frames_path, 'IGNORE'))
    assert empty is True

    empty = check_for_files_exr(os.path.join(shot_render_frames_path, 'WITHOUT_EXR'))
    assert empty is True

    layers = _get_valid_render_layers(shot_render_frames_path)
    assert layers == ['RND_FG', 'RND_MG']

    names = _get_render_layer_names(shot_render_frames_path, 'RND_FG')
    assert names == ['RND_FG_CRYPTO', 'RND_FG_BTY']

    version = _get_last_version_path(os.path.join(shot_render_frames_path, 'RND_FG_BTY'))
    assert version == 'I:/GizmoRD/FRAMES/PYTEST/030/CG/RND_FG_BTY/LGT_KAF_010_v0026'

    version = _get_last_version_path(os.path.join(shot_render_frames_path, 'RND_FG_BAD'))
    assert version is None

    aovs = _get_aovs(name='RND_FG_BTY', path=os.path.join(
        shot_render_frames_path, 'RND_FG_BTY', 'LGT_KAF_010_v0026'))
    assert aovs == ['AO', 'beauty', 'crypto_asset', 'crypto_material',
                    'crypto_object', 'emission', 'specular']

    # test main collector
    renders = collect_render_layers_from(shot_render_frames_path)
    assert len(renders) == 2


if __name__ == '__main__':
    pytest.main(['-v', '-s'])
