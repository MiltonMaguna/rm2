import sys

for name in list(sys.modules.keys()):
    for pack in ['RenderManager2']:
        if name.startswith(pack):
            print('removing module', name)
            del sys.modules[name]
            del name

from RenderManager2.render_manager2.main import run_test

run_test()
