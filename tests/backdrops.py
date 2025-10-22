"""
import sys
for name in list(sys.modules.keys()):
    for pack in ["render_manager."]:
        if name.startswith(pack):
            print('removing module', name)
            del sys.modules[name]

from rm2.render_manager.mocks.mocked_render_layer import render_layer_bg, render_layer_fg
from rm2.render_manager.render.libs.helpers.backdrops import (get_next_row_container,
                                                        get_next_row_subcontainer,
                                                        create_backdrop_container,
                                                        create_backdrop_subcontainer)


row = get_next_row_container(render_layer_bg)
print('row for RND_BG', row)
row = get_next_row_subcontainer(render_layer_bg)
print('row for RND_BG_BTY', row)

container = create_backdrop_container(render_layer_bg, row)
print(container.name())
print(container.xpos(), container.ypos())
create_backdrop_subcontainer(render_layer_bg, row)

row = get_next_row_container(render_layer_fg)
print('row for RND_FG', row)
row = get_next_row_subcontainer(render_layer_fg)
print('row for RND_FG_BTY', row)

container = create_backdrop_container(render_layer_fg, row)
print(container.name())
print(container.xpos(), container.ypos())
create_backdrop_subcontainer(render_layer_fg, row)
"""
