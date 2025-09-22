import pytest


class MockBackdropNode:

    def __init__(self, is_subcontainer=0, render_layer='', version=0, name=''):
        self._dict = {'subcontainer': DictValue('subcontainer', is_subcontainer),
                      'render_layer': DictValue('render_layer', render_layer),
                      'version': DictValue('version', version),
                      'name': DictValue('name', name),
                      }

    def name(self):
        return f'BackdropNode_{self._dict["render_layer"].getValue()}'

    def __getitem__(self, key: str):
        return self._dict[key]

    def getNodes(self):
        return []


class DictValue:

    def __init__(self, key_name: str, value: str):
        self._key_name = key_name
        self._value = value

    def getValue(self):
        return self._value


class MockNuke:

    def __init__(self, data):
        self.data = data

    def allNodes(self, node_type):
        return self.data

    def message(self, message: str):
        print(message)

    def toNode(self, node_name: str):
        for n in self.data:
            if n.name() == node_name:
                return n

    def delete(self, node):
        pass


# Define different sets of backdrops for MockNuke instances
read_no_version = [MockBackdropNode(),
                   MockBackdropNode(1, 'RND_BG', 21, 'RND_BG_TECH')]
read_same_version = [MockBackdropNode(1, 'RND_FG', 26, 'RND_FG_BTY'),
                     MockBackdropNode(1, 'RND_BG', 21, 'RND_BG_TECH')]
read_outdated_version = [MockBackdropNode(1, 'RND_FG', 24, 'RND_FG_BTY')]


@pytest.fixture(scope='function')
def mocked_nuke_no_nodes(monkeypatch):
    monkeypatch.setattr('render_manager.render.render_layer.nuke', MockNuke(read_no_version))
    monkeypatch.setattr('render_manager.render.libs.remove.nuke', MockNuke(read_no_version))


@pytest.fixture(scope='function')
def read_node_same_version(monkeypatch):
    monkeypatch.setattr('render_manager.render.render_layer.nuke', MockNuke(read_same_version))
    monkeypatch.setattr('render_manager.render.libs.remove.nuke', MockNuke(read_same_version))


@pytest.fixture(scope='function')
def read_node_outdated_version(monkeypatch):
    monkeypatch.setattr('render_manager.render.render_layer.nuke', MockNuke(read_outdated_version))
    monkeypatch.setattr('render_manager.render.libs.remove.nuke', MockNuke(read_outdated_version))


@pytest.fixture(scope='session')
def shot_render_frames_path():
    '''mock render object for tests'''
    return 'I:/GizmoRD/FRAMES/PYTEST/030/CG'
