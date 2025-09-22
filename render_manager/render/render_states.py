from collections import namedtuple

# RenderLayer States named tuple
state = namedtuple('state', ['value', 'label'])

UNLOADED = state(0, 'UNLOADED')
OUTDATED = state(1, 'OUTDATED')
SYNC = state(2, 'SYNC')
