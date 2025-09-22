# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke - Disk Collector Module
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import os
from typing import List
from qt_log.stream_log import get_stream_logger
from render_manager.render.render_layer import Render
from render_manager.render.tokens import (
    RENDER_PREFIX,
    RENDER_PREFIX_VERSION,
    RENDER_ROLE,
    RENDER_LAYER_ORDER,
    TECHS_AOVS_IN_LAYER,
)

log = get_stream_logger("RenderManager")


def collect_render_layers_from(path: str) -> List[Render]:
    """return a list of Render objects
    Args:
        path (str): path to search on shot frames
    Returns:
        list: list of Render objects
    """
    if not os.path.exists(path):
        log.warning(f"Path does not exist: {path}")
        return []

    render_layers = []
    layers = _get_valid_render_layers(path)

    for layer in layers:
        for name in _get_render_layer_names(path, layer):
            base_path = os.path.join(path, name)
            version_path = _get_last_version_path(base_path)

            # filter out invalid paths or folders
            if version_path is None:
                log.warning(f"Discarding invalid path: {version_path}")
                continue

            # collect aovs and data for this render layer
            aovs = _get_aovs(version_path, name)
            render = Render(path=version_path, name=name, aovs=aovs)
            render_layers.append(render)

    return render_layers


def _get_valid_render_layers(frame_path: str) -> tuple:
    """get names of render layers with the correct pipeline naming
    Returns:
        list: list of valid render layers names
    """
    rnd_layers = []

    for name in list(os.listdir(frame_path)):
        split_name = name.split("_")
        # filter only valid prefixes folders
        if split_name[0] not in RENDER_PREFIX:
            continue
        # filter only valid rol folders
        if split_name[1] not in RENDER_ROLE:
            continue
        # filter only valid render layer type of folders
        if split_name[-1] in RENDER_LAYER_ORDER:
            rnd_layers.append(("_").join(split_name[:-1]))
        else:
            log.warning(f"Invalid Render Layers Found: {name}")

    unique_render_layers = list(set(rnd_layers))

    # ! how to sort?

    return sorted(unique_render_layers)


def _get_render_layer_names(path: str, layer: str) -> list:
    """return a list of name rnd layers
    Args:
        path (str): path to search on shot frames
        layer (str): layer name
    Returns:
        list: list of rnd layers full names with suffix

    # ! this method is duplicated from the get_valid_render_layers, we already
    # ! have the layer name, we should not be doing this again
    # ! we use this method only to sort the render layers by type
    # ! move the sort to the get_valid_render_layers method and remove this one
    """
    render_layer_names = []

    for suffix in RENDER_LAYER_ORDER:
        full_name = f"{layer}_{suffix}"
        if os.path.exists(os.path.join(path, full_name)):
            render_layer_names.append(full_name)

    return render_layer_names


def _get_last_version_path(path_layer: str) -> str:
    """get the last version folder of a render layer with LGT in the name
        if the folder is empty, get the previous one
    Args:
        path_layer (str): full path of last render version
    """

    versions = []
    for suffix in RENDER_PREFIX_VERSION:
        for _path in os.listdir(path_layer):
            if _path.startswith(suffix):
                versions.append(_path)

    versions.sort(reverse=True)

    for folder in versions:
        path = os.path.join(path_layer, folder)

        if check_for_empty_subfolders(path):
            continue

        return path.replace("\\", "/")


def _get_aovs(path: str, name: str) -> list:
    """return a list of aovs by reading subfolders of a render layer
    Args:
        path (str): path to search for shot frames
        name (str): name of the render layer
    Returns:
        list: list of aovs from valid directories
    """
    aovs = os.listdir(path)

    # collecting specific aovs for technical layers
    for key, values in TECHS_AOVS_IN_LAYER.items():
        if name.endswith(key):
            aovs = [aov for aov in aovs if aov in values]

    return [p for p in aovs if os.path.isdir(os.path.join(path, p))]


def check_for_files_exr(folder_path: str) -> bool:
    # Obtener la lista de archivos en la carpeta
    files = [file for file in os.listdir(folder_path) if file.endswith(".exr")]

    if len(files) == 0:
        return True

    return False


def check_for_empty_subfolders(folder_path: str) -> bool:  # sourcery skip: use-any
    """
    Check if a folder and all its subfolders are empty.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        bool: True if the folder and all its subfolders are empty, False otherwise.
    """

    # full empty folder case
    if len(os.listdir(folder_path)) == 0:
        return True

    # Recursively check if the folder and all its subfolders are empty
    for root, dirs, _ in os.walk(folder_path):
        if not dirs:
            return True

        for folder in dirs:
            aov_path = os.path.join(root, folder)

            if check_for_files_exr(aov_path):
                return True

        return False
