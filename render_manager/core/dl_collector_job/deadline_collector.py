from collections import defaultdict
from typing import List, Dict

from qt_log.stream_log import get_stream_logger
from Test_RenderManager.render_manager.core.dl_collector_job.libs.render.render_layer import (
    Render,
)
from Test_RenderManager.render_manager.render.tokens import (
    RENDER_PREFIX,
    RENDER_PREFIX_VERSION,
    RENDER_ROLE,
)

log = get_stream_logger("RenderManager - Deadline Collector")


def collect_render_layers_from_deadline(data: dict) -> Dict[str, List[Render]]:
    """
    Collects valid render layers from Deadline job data.
    Iterates over jobs grouped by status in the provided data dictionary, validates each render layer and version name,
    and collects them as Render objects if valid.
    Args:
        data (dict): A dictionary containing Deadline job data, expected to have a 'jobs_by_status' key mapping statuses to job lists.
    Returns:
        List[Render]: A list of Render objects representing valid render layers collected from the job data.
    """

    render_layers = defaultdict(list)

    for status in data["jobs_by_status"]:
        log.info(f"Collecting render layers for status: {status}")

        for layer in data["jobs_by_status"][status]:
            # log.info(f"Layer: {layer}")
            # log.info(f"Job Name: {layer['job_name']}")

            if not _get_valid_render_layers(layer["render_layer"]):
                log.warning(f"Invalid render layer: {layer['render_layer']}")
                continue

            if not _get_valid_version_name(layer["batch_name"]):
                log.warning(f"Invalid version name: {layer['batch_name']}")
                continue

            # collect aovs and data for this render layer
            render = Render(layer)
            rol_main = render.rol_main()
            if rol_main in RENDER_ROLE:
                render_layers[rol_main].append(render)

    return dict(render_layers)


def _get_valid_version_name(version_name: str) -> bool:
    """
    Checks if the given version name starts with any of the valid prefixes defined in RENDER_PREFIX_VERSION.
    Args:
        version_name (str): The version name to validate.
        ex: LGT_KIT_0070_v0019
    Returns:
        bool: True if the version name starts with a valid prefix, False otherwise.
    """

    for suffix in RENDER_PREFIX_VERSION:
        if version_name.startswith(suffix):
            return True

    return False


def _get_valid_render_layers(layer_name: str) -> bool:
    """
    Checks if the given layer name starts with any of the valid render layer prefixes.
    Args:
        layer_name (str): The name of the render layer to validate.
        ex: RND_BG_MAIN_BTY
    Returns:
        bool: True if the layer name starts with a valid prefix, False otherwise.
    """

    for suffix in RENDER_PREFIX:
        if layer_name.startswith(suffix):
            return True

    return False
