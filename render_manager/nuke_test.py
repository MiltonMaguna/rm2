import sys

for name in list(sys.modules.keys()):
    for pack in ["rm2"]:
        if name.startswith(pack):
            print("removing module", name)
            del sys.modules[name]
            del name

from rm2.render_manager.main import run_test

run_test()

