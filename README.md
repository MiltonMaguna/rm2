# Nuke-RenderManager
Nuke Render Manager

# dev run

import sys
sys.path.append('F:/nuke/arcane/dev/RenderManager')
for name in list(sys.modules.keys()):
    for pack in ['render_manager', 'RenderManager']:
        if name.startswith(pack):
            del sys.modules[name]

import RenderManager.render_manager.main as rm
rm.run(1)

# run

import sys
for name in list(sys.modules.keys()):
    for pack in ["render_manager."]:
        if name.startswith(pack):
            print('removing module', name)
            del sys.modules[name]


from render_manager.main import run
run()