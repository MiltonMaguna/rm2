import sys

repo_test2 = r"D:\repo\Test_RenderManager"
repo_test3 = r"D:\repo"
sys.path.append(repo_test2)
nuke.pluginAddPath(repo_test2)
sys.path.append(repo_test3)
nuke.pluginAddPath(repo_test3)

import sys

for name in list(sys.modules.keys()):
    for pack in ["Test_RenderManager"]:
        if name.startswith(pack):
            print("removing module", name)
            del sys.modules[name]
            del name

# from Test_RenderManager.render_manager.main import run_test
# run_test()
