'''
import sys
for name in list(sys.modules.keys()):
    for pack in ["render_manager."]:
        if name.startswith(pack):
            print('removing module', name)
            del sys.modules[name]

from render_manager.mocks.mocked_render_layer import render_layer_bg_rzk
from render_manager.render.libs.helpers.reads import create_all_aovs
create_all_aovs(render_layer_bg_rzk)

'''
