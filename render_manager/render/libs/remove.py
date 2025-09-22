# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Main RenderLayer Class
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import contextlib
from qt_log.stream_log import get_stream_logger
from render_manager.render.render_layer_types import Render

try:
    import nuke
except ImportError:
    import render_manager.mocks.nuke as nuke

log = get_stream_logger("RenderManager")


class RemoveRenderLayer:
    def __init__(self, render_layer: Render):
        self.render = render_layer

    def remove(self) -> None:
        """removes all elements for this render_layer"""
        log.info(f"Removing Render {self.render.name()}")

        backdrops = self.get_backdrops()
        if not backdrops:
            log.warning(f"No Backdrop found for {self.render.name()}")
            return ""

        self.remove_nodes_backdrop(backdrops)

        log.info(f"Removed all nodes inside of backdrop {self.render.name()}")

    def get_backdrops(self) -> str or bool:
        """returns all backdrops nodes with attribute ROLE_LAYER matching
        role_layer for this render layer object"""

        for bdrop in nuke.allNodes("BackdropNode"):
            with contextlib.suppress(NameError):
                if bdrop["subcontainer"].getValue():
                    if bdrop["name_layer"].getValue() == self.render.name():
                        return bdrop.name()
        return False

    def remove_nodes_backdrop(self, backdrop_name: str):
        """removes all nodes inside a backdrop"""
        backdrop = nuke.toNode(backdrop_name)
        nodes = backdrop.getNodes()
        nodes.append(backdrop)

        for node in nodes:
            nuke.delete(node)
