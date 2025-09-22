# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - CreateRead for RenderLayer
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
from qt_log.stream_log import get_stream_logger
from render_manager.render.render_layer_types import Render
from render_manager.render.libs.helpers.backdrops import (
    create_backdrop_container,
    create_backdrop_subcontainer,
    get_next_row_container,
    get_next_row_subcontainer,
)

log = get_stream_logger("RenderManager")


class Create:
    def load(self, render_layer: Render) -> None:
        """Create all reads for all renders in a shot"""
        log.info(f"Loading Render Layer {render_layer.name()}.{render_layer.version()}")

        next_row_container = get_next_row_container(render_layer)
        create_backdrop_container(render_layer, next_row_container)
        next_row_subcontainer = get_next_row_subcontainer(render_layer)
        create_backdrop_subcontainer(render_layer, next_row_subcontainer)

        log.info(f"{render_layer.name()} Reads Created.")
